"""
Enterprise Human Capital & Operational Efficiency Diagnostics
Module: ingest_hr_audit.py
Purpose: Ingests processed Galaxy Schema dimensional model (CSV exports from
         the pipeline_runner.py) into Microsoft SQL Server staging and mart
         tables using SQLAlchemy + pyodbc with Windows Authentication.

Usage:
    python scripts/ingestion/ingest_hr_audit.py [--schema mart] [--truncate]

Environment Variables (from .env):
    DB_DRIVER   - ODBC driver name (default: {ODBC Driver 17 for SQL Server})
    DB_SERVER   - SQL Server instance (default: localhost\\SQLEXPRESS)
    DB_DATABASE - Target database (default: EnterpriseHR_DWH)
    DB_USER     - SQL Auth username (leave empty for Windows Auth)
    DB_PASS     - SQL Auth password (leave empty for Windows Auth)
"""

import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.engine import Engine

# ──────────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-8s │ %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────
# Mapping: processed CSV filename → (schema.table, primary_key_col)
# ──────────────────────────────────────────────────────────────────
TABLE_MANIFEST = {
    # Conformed Dimensions
    "Dim_Employee.csv": ("mart.Dim_Employee", "EmployeeKey"),
    "Dim_Department.csv": ("mart.Dim_Department", "DepartmentKey"),
    "Dim_Branch.csv": ("mart.Dim_Branch", "BranchKey"),
    "Dim_Date.csv": ("mart.Dim_Date", "DateKey"),
    "Dim_Course.csv": ("mart.Dim_Course", "CourseKey"),
    # Fact Tables (Galaxy Constellation)
    "Fact_WorkforceSnapshot.csv": ("mart.Fact_WorkforceSnapshot", "SnapshotKey"),
    "Fact_DailyAttendance.csv": ("mart.Fact_DailyAttendance", "AttendanceKey"),
    "Fact_DepartmentBudget.csv": ("mart.Fact_DepartmentBudget", "BudgetKey"),
    "Fact_TrainingCompletions.csv": ("mart.Fact_TrainingCompletions", "CompletionKey"),
}


def get_db_engine() -> Engine:
    """
    Establishes a SQLAlchemy connection to Microsoft SQL Server.

    - Uses Windows Authentication (Trusted_Connection) when DB_USER is empty.
    - Uses SQL Server Authentication when DB_USER is provided.

    Returns:
        SQLAlchemy Engine instance.
    """
    load_dotenv(BASE_DIR / ".env")

    driver = os.getenv("DB_DRIVER", "{ODBC Driver 17 for SQL Server}")
    server = os.getenv("DB_SERVER", "localhost")
    database = os.getenv("DB_DATABASE", "EnterpriseHR_DWH")
    user = os.getenv("DB_USER", "").strip()
    password = os.getenv("DB_PASS", "").strip()

    # Build the ODBC connection string
    if user:
        # SQL Server Authentication
        conn_str = (
            f"DRIVER={driver};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={user};"
            f"PWD={password};"
            f"TrustServerCertificate=yes;"
        )
        logger.info("🔑 Using SQL Server Authentication for user '%s'", user)
    else:
        # Windows Authentication (Integrated Security)
        conn_str = (
            f"DRIVER={driver};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"Trusted_Connection=yes;"
            f"TrustServerCertificate=yes;"
        )
        logger.info("🔑 Using Windows Authentication (Trusted_Connection)")

    # URL-encode the ODBC connection string for SQLAlchemy
    from urllib.parse import quote_plus

    engine_url = f"mssql+pyodbc:///?odbc_connect={quote_plus(conn_str)}"

    engine = create_engine(
        engine_url,
        fast_executemany=True,  # Bulk insert optimization for pyodbc
        pool_pre_ping=True,     # Validate connections before use
        pool_size=5,
        max_overflow=10,
    )

    return engine


def verify_connection(engine: Engine) -> bool:
    """Tests database connectivity and prints server version."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT @@VERSION AS ServerVersion"))
            row = result.fetchone()
            version_info = row[0].split("\n")[0] if row else "Unknown"
            logger.info("✅ Connected to: %s", version_info)

            # Verify target schemas exist
            result = conn.execute(
                text(
                    "SELECT s.name FROM sys.schemas s "
                    "WHERE s.name IN ('raw', 'stg', 'mart') "
                    "ORDER BY s.name"
                )
            )
            schemas = [r[0] for r in result.fetchall()]
            logger.info("📂 Available schemas: %s", ", ".join(schemas))
            return True
    except Exception as e:
        logger.error("❌ Connection failed: %s", e)
        return False


def get_available_csvs() -> dict:
    """Scans the processed directory for available CSV files (case-insensitive)."""
    available = {}
    if not PROCESSED_DIR.exists():
        logger.warning("⚠️  Processed data directory not found: %s", PROCESSED_DIR)
        return available

    manifest_lower = {k.lower(): k for k in TABLE_MANIFEST}

    for csv_file in sorted(PROCESSED_DIR.glob("*.csv")):
        lower_name = csv_file.name.lower()
        if lower_name in manifest_lower:
            canonical_name = manifest_lower[lower_name]
            available[canonical_name] = csv_file
        else:
            logger.debug("Skipping unmapped file: %s", csv_file.name)

    return available


def ingest_csv_to_table(
    engine: Engine,
    csv_path: Path,
    target_table: str,
    pk_column: str,
    truncate_first: bool = False,
) -> int:
    """
    Ingests a single CSV file into a SQL Server table.

    Args:
        engine: SQLAlchemy Engine
        csv_path: Path to the CSV file
        target_table: Fully qualified table name (e.g., 'mart.Dim_Employee')
        pk_column: Primary key column name for validation
        truncate_first: If True, truncates the table before inserting

    Returns:
        Number of rows inserted
    """
    schema_name, table_name = target_table.split(".")

    logger.info("📥 Loading %s → %s", csv_path.name, target_table)

    # Read CSV with pandas
    try:
        df = pd.read_csv(csv_path, encoding="utf-8-sig")
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, encoding="utf-8")

    if df.empty:
        logger.warning("   ⚠️  Empty CSV file: %s (0 rows)", csv_path.name)
        return 0

    row_count = len(df)
    col_count = len(df.columns)
    logger.info("   📊 Read %s rows × %s columns", f"{row_count:,}", col_count)

    # Validate primary key uniqueness in source
    if pk_column in df.columns:
        duplicates = df[pk_column].duplicated().sum()
        if duplicates > 0:
            logger.warning(
                "   ⚠️  %s duplicate primary keys found in '%s' — deduplicating",
                duplicates,
                pk_column,
            )
            df = df.drop_duplicates(subset=[pk_column], keep="last")
            logger.info("   🔄 Deduplicated to %s rows", f"{len(df):,}")

    # Parse date columns (heuristic detection - exclude surrogate keys)
    for col in df.columns:
        if col.endswith("Key") or col.endswith("ID") or col.endswith("Code"):
            continue
        col_lower = col.lower()
        if any(kw in col_lower for kw in ["fulldate", "effectivedate", "expirydate", "hiredate"]):
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce").dt.date
            except Exception:
                pass

    # Truncate target table if requested
    if truncate_first:
        try:
            with engine.connect() as conn:
                # Check if table exists first
                inspector = inspect(engine)
                if table_name in inspector.get_table_names(schema=schema_name):
                    conn.execute(text(f"TRUNCATE TABLE {target_table}"))
                    conn.commit()
                    logger.info("   🗑️  Truncated %s", target_table)
                else:
                    logger.warning(
                        "   ⚠️  Table %s does not exist — will attempt to create",
                        target_table,
                    )
        except Exception as e:
            logger.warning("   ⚠️  Could not truncate %s: %s", target_table, e)

    # Insert data using pandas to_sql with fast_executemany (do NOT use method="multi" with fast_executemany)
    try:
        df.to_sql(
            name=table_name,
            schema=schema_name,
            con=engine,
            if_exists="append",  # Use 'replace' for full reload
            index=False,
            chunksize=1000,
        )
        logger.info("   ✅ Inserted %s rows into %s", f"{len(df):,}", target_table)
        return len(df)
    except Exception as e:
        logger.error("   ❌ Failed to insert into %s: %s", target_table, e)
        return 0


def ingest_staging_attrition(engine: Engine, truncate: bool = True) -> int:
    """Ingests data/raw/exit_attrition_records.csv into stg.Exit_Attrition_Records."""
    raw_dir = BASE_DIR / "data" / "raw"
    csv_path = raw_dir / "exit_attrition_records.csv"
    if not csv_path.exists():
        logger.warning("   ⚠️  exit_attrition_records.csv not found in %s", raw_dir)
        return 0

    try:
        df = pd.read_csv(csv_path, encoding="utf-8-sig")
        for col in ["NoticeDate", "ExitDate"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce").dt.date

        with engine.connect() as conn:
            if truncate:
                conn.execute(text("TRUNCATE TABLE stg.Exit_Attrition_Records"))
                conn.commit()
                logger.info("   🗑️  Truncated stg.Exit_Attrition_Records")

        df.to_sql(
            name="Exit_Attrition_Records",
            schema="stg",
            con=engine,
            if_exists="append",
            index=False,
            chunksize=1000,
        )
        logger.info("   ✅ Ingested %s rows into stg.Exit_Attrition_Records", f"{len(df):,}")
        return len(df)
    except Exception as e:
        logger.error("   ❌ Failed to ingest stg.Exit_Attrition_Records: %s", e)
        return 0


def run_post_ingestion_validation(engine: Engine) -> None:
    """Runs post-ingestion row count validation queries."""
    logger.info("\n" + "═" * 60)
    logger.info("📋 POST-INGESTION VALIDATION REPORT")
    logger.info("═" * 60)

    validation_queries = [
        ("stg.Exit_Attrition_Records", "SELECT COUNT(*) FROM stg.Exit_Attrition_Records"),
        ("mart.Dim_Employee", "SELECT COUNT(*) FROM mart.Dim_Employee"),
        ("mart.Dim_Department", "SELECT COUNT(*) FROM mart.Dim_Department"),
        ("mart.Dim_Branch", "SELECT COUNT(*) FROM mart.Dim_Branch"),
        ("mart.Dim_Date", "SELECT COUNT(*) FROM mart.Dim_Date"),
        ("mart.Dim_Course", "SELECT COUNT(*) FROM mart.Dim_Course"),
        ("mart.Fact_WorkforceSnapshot", "SELECT COUNT(*) FROM mart.Fact_WorkforceSnapshot"),
        ("mart.Fact_DailyAttendance", "SELECT COUNT(*) FROM mart.Fact_DailyAttendance"),
        ("mart.Fact_DepartmentBudget", "SELECT COUNT(*) FROM mart.Fact_DepartmentBudget"),
        ("mart.Fact_TrainingCompletions", "SELECT COUNT(*) FROM mart.Fact_TrainingCompletions"),
    ]

    try:
        with engine.connect() as conn:
            for table_name, query in validation_queries:
                try:
                    result = conn.execute(text(query))
                    count = result.scalar()
                    status = "✅" if count and count > 0 else "⚠️"
                    logger.info(
                        "   %s %-40s → %s rows",
                        status,
                        table_name,
                        f"{count:,}" if count else "0",
                    )
                except Exception:
                    logger.info("   ❌ %-40s → TABLE NOT FOUND", table_name)
    except Exception as e:
        logger.error("❌ Validation failed: %s", e)

    logger.info("═" * 60)


def main(
    target_schema: str = "mart",
    truncate: bool = False,
    dry_run: bool = False,
) -> None:
    """
    Main ingestion entry point.

    Args:
        target_schema: Schema to ingest into ('raw', 'stg', or 'mart')
        truncate: Whether to truncate tables before inserting
        dry_run: If True, only validates connection and lists files
    """
    start_time = datetime.now()
    logger.info("=" * 60)
    logger.info("🚀 ENTERPRISE HR DATA INGESTION PIPELINE")
    logger.info("   Started: %s", start_time.strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("   Target Schema: %s", target_schema)
    logger.info("   Truncate Mode: %s", "ON" if truncate else "OFF")
    logger.info("   Dry Run: %s", "YES" if dry_run else "NO")
    logger.info("=" * 60)

    # Step 1: Establish connection
    logger.info("\n📡 Step 1: Establishing database connection...")
    engine = get_db_engine()

    if not verify_connection(engine):
        logger.error("💥 Cannot proceed without database connection. Exiting.")
        sys.exit(1)

    # Step 2: Discover available CSV files
    logger.info("\n📂 Step 2: Discovering processed CSV files...")
    available_csvs = get_available_csvs()

    if not available_csvs:
        logger.warning(
            "⚠️  No processed CSV files found in %s\n"
            "   Run the pipeline first:\n"
            "     python scripts/ingestion/generate_enterprise_mock_data.py\n"
            "     python scripts/pipeline_runner.py",
            PROCESSED_DIR,
        )
        sys.exit(0)

    # Display discovered files
    logger.info("   Found %d files ready for ingestion:", len(available_csvs))
    for filename, filepath in available_csvs.items():
        target_table, pk_col = TABLE_MANIFEST[filename]
        size_kb = filepath.stat().st_size / 1024
        logger.info("   📄 %-35s → %-35s (%.1f KB)", filename, target_table, size_kb)

    total_rows = 0
    tables_loaded = 0

    # Step 2b: Ingest Staging Exit Attrition Audit Records
    logger.info("\n📥 Step 2b: Ingesting stg.Exit_Attrition_Records...")
    stg_rows = ingest_staging_attrition(engine, truncate=truncate)
    if stg_rows > 0:
        total_rows += stg_rows
        tables_loaded += 1

    # Step 3: Ingest dimensions first (referential integrity order)
    logger.info("\n📥 Step 3: Ingesting conformed dimensions...")
    dim_order = [
        "Dim_Date.csv",
        "Dim_Department.csv",
        "Dim_Branch.csv",
        "Dim_Course.csv",
        "Dim_Employee.csv",
    ]

    for csv_name in dim_order:
        if csv_name in available_csvs:
            default_target_table, pk_col = TABLE_MANIFEST[csv_name]
            table_bare_name = default_target_table.split(".")[-1]
            target_table = f"{target_schema}.{table_bare_name}"
            rows = ingest_csv_to_table(
                engine, available_csvs[csv_name], target_table, pk_col, truncate
            )
            total_rows += rows
            if rows > 0:
                tables_loaded += 1

    # Step 4: Ingest fact tables
    logger.info("\n📥 Step 4: Ingesting fact tables...")
    fact_order = [
        "Fact_WorkforceSnapshot.csv",
        "Fact_DailyAttendance.csv",
        "Fact_DepartmentBudget.csv",
        "Fact_TrainingCompletions.csv",
    ]

    for csv_name in fact_order:
        if csv_name in available_csvs:
            default_target_table, pk_col = TABLE_MANIFEST[csv_name]
            table_bare_name = default_target_table.split(".")[-1]
            target_table = f"{target_schema}.{table_bare_name}"
            rows = ingest_csv_to_table(
                engine, available_csvs[csv_name], target_table, pk_col, truncate
            )
            total_rows += rows
            if rows > 0:
                tables_loaded += 1

    # Step 5: Post-ingestion validation
    logger.info("\n🔍 Step 5: Running post-ingestion validation...")
    run_post_ingestion_validation(engine)

    # Final summary
    elapsed = datetime.now() - start_time
    logger.info("\n" + "=" * 60)
    logger.info("🏁 INGESTION COMPLETE")
    logger.info("   Tables Loaded: %d / %d", tables_loaded, len(TABLE_MANIFEST))
    logger.info("   Total Rows Inserted: %s", f"{total_rows:,}")
    logger.info("   Elapsed Time: %s", str(elapsed).split(".")[0])
    logger.info("=" * 60)

    engine.dispose()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Enterprise HR Galaxy Schema → SQL Server Ingestion Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (validate connection and list files only)
  python scripts/ingestion/ingest_hr_audit.py --dry-run

  # Full ingestion into mart schema
  python scripts/ingestion/ingest_hr_audit.py --schema mart

  # Truncate and reload
  python scripts/ingestion/ingest_hr_audit.py --schema mart --truncate
        """,
    )
    parser.add_argument(
        "--schema",
        choices=["raw", "stg", "mart"],
        default="mart",
        help="Target schema for ingestion (default: mart)",
    )
    parser.add_argument(
        "--truncate",
        action="store_true",
        help="Truncate target tables before inserting",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate connection and list files without loading data",
    )

    args = parser.parse_args()
    main(target_schema=args.schema, truncate=args.truncate, dry_run=args.dry_run)
