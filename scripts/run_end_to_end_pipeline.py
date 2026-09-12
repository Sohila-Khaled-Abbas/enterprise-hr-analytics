"""
Enterprise Human Capital & Operational Efficiency Diagnostics
Module: run_end_to_end_pipeline.py
Purpose: Master pipeline orchestrator that executes the complete end-to-end workflow:
         1. Source Data Verification (7,000 employee master text file)
         2. Galaxy Schema Dimensional Mart Generation (pipeline_runner.py)
         3. Microsoft SQL Server Ingestion & Staging
         4. Staging SCD2 Transformations (00_stg_hr_audit.sql)
         5. Automated Data Quality & Contract Test Suite (pytest)
         6. Executive Summary & Table Audit Verification

Usage:
    python scripts/run_end_to_end_pipeline.py [--skip-ingest] [--skip-tests]
"""

import argparse
import logging
import os
import subprocess
import sys
import time
from pathlib import Path

# Ensure UTF-8 output on Windows terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
from sqlalchemy import text
from scripts.ingestion.ingest_hr_audit import get_db_engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-8s │ %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("EndToEndPipeline")


def step_header(step_num: int, title: str):
    logger.info("═" * 70)
    logger.info(f"▶ STEP {step_num}: {title.upper()}")
    logger.info("═" * 70)


def verify_master_raw_data() -> bool:
    """Checks the master 7,000 employee dataset file for integrity."""
    master_txt = PROJECT_ROOT / "data" / "raw" / "employees_data_7000.txt"
    if not master_txt.exists():
        logger.error(f"❌ Master raw dataset not found: {master_txt}")
        return False

    with open(master_txt, "r", encoding="utf-8") as f:
        content = f.read()
    records = [r for r in content.split("------") if r.strip()]
    logger.info(f"📄 Master text file verified: {len(records)} employee records found.")
    if len(records) != 7000:
        logger.error(f"❌ Expected exactly 7,000 records, found {len(records)}.")
        return False

    return True


def run_galaxy_mart_build() -> bool:
    """Executes pipeline_runner.py to construct all Galaxy Schema dimensional tables."""
    from scripts.pipeline_runner import run_pipeline
    logger.info("⚙️  Running dimensional mart generator (pipeline_runner.py)...")
    run_pipeline()
    logger.info("✅ Dimensional mart build complete.")
    return True


def run_sql_ingestion() -> bool:
    """Ingests dimensional and fact data into Microsoft SQL Server."""
    from scripts.ingestion.ingest_hr_audit import main as ingest_mart_main
    from scripts.ingestion.ingest_badge_logs import ingest_badge_logs
    from scripts.ingestion.ingest_finance_plan import ingest_finance_data
    from scripts.ingestion.ingest_lms_data import ingest_lms_logs

    logger.info("📥 Ingesting conformed dimensions and facts into mart schema (idempotent reload)...")
    ingest_mart_main(target_schema="mart", truncate=True)

    logger.info("📥 Ingesting raw badge logs into raw.Badge_Access_Logs...")
    badge_json = PROJECT_ROOT / "data" / "raw" / "api_badge_logs_202605.json"
    if badge_json.exists():
        ingest_badge_logs(str(badge_json), "raw", "Badge_Access_Logs")

    logger.info("📥 Ingesting raw finance budget plan into raw.Finance_Budget_Plan...")
    budget_xlsx = PROJECT_ROOT / "data" / "raw" / "finance_budget_2026.xlsx"
    if budget_xlsx.exists():
        ingest_finance_data(str(budget_xlsx), "raw", "Finance_Budget_Plan")

    logger.info("📥 Ingesting raw LMS certifications into raw.LMS_Certifications...")
    lms_csv = PROJECT_ROOT / "data" / "raw" / "lms_certifications.csv"
    if lms_csv.exists():
        ingest_lms_logs(str(lms_csv), "raw", "LMS_Certifications")

    return True




def run_staging_transformations() -> bool:
    """Executes 00_stg_hr_audit.sql via run_stg_transformations.py."""
    from scripts.transformations.run_stg_transformations import run_sql_script
    sql_script = PROJECT_ROOT / "sql" / "transformations" / "00_stg_hr_audit.sql"
    logger.info(f"⚙️  Executing staging transformation script: {sql_script.name}...")
    run_sql_script(str(sql_script))
    return True


def run_presentation_mart_transformations() -> bool:
    """Executes 02_mart_dimensional_model.sql via run_mart_transformations.py."""
    from scripts.transformations.run_mart_transformations import run_mart_script
    sql_script = PROJECT_ROOT / "sql" / "transformations" / "02_mart_dimensional_model.sql"
    logger.info(f"⚙️  Executing presentation mart transformation script: {sql_script.name}...")
    run_mart_script(str(sql_script))
    return True


def run_pytest_suite() -> bool:
    """Runs automated data quality test suite."""
    test_path = PROJECT_ROOT / "tests" / "test_data_quality.py"
    logger.info(f"🧪 Running Pytest validation suite on {test_path.name}...")
    cmd = [sys.executable, "-m", "pytest", str(test_path), "-v", "--tb=short"]
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True)

    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    if result.returncode != 0:
        logger.error(f"❌ Pytest failed with exit code {result.returncode}")
        return False

    logger.info("✅ All 14 data quality and referential integrity tests PASSED!")
    return True


def print_executive_summary():
    """Queries SQL Server and prints an executive summary table of all schemas and tables."""
    try:
        engine = get_db_engine()
        with engine.connect() as conn:
            query = text("""
                SELECT 
                    s.name AS SchemaName,
                    t.name AS TableName,
                    p.rows AS RowCounts
                FROM sys.tables t
                INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
                INNER JOIN sys.partitions p ON t.object_id = p.object_id
                WHERE p.index_id IN (0, 1)
                ORDER BY s.name, t.name;
            """)
            rows = conn.execute(query).fetchall()

            logger.info("═" * 70)
            logger.info("📊 ENTERPRISE DWH PRODUCTION INVENTORY SUMMARY")
            logger.info("═" * 70)
            logger.info(f"{'Schema':<10} │ {'Table Name':<35} │ {'Row Count':>12}")
            logger.info("─" * 10 + "─┼─" + "─" * 35 + "─┼─" + "─" * 12)

            total_rows = 0
            for r in rows:
                schema_name, table_name, count = r[0], r[1], r[2]
                total_rows += count
                logger.info(f"{schema_name:<10} │ {table_name:<35} │ {count:>12,}")

            logger.info("─" * 10 + "─┴─" + "─" * 35 + "─┴─" + "─" * 12)
            logger.info(f"{'TOTAL':<10} │ {'All Production DWH Tables':<35} │ {total_rows:>12,}")
            logger.info("═" * 70)

    except Exception as e:
        logger.warning(f"Could not print SQL Server inventory: {e}")


def main():
    parser = argparse.ArgumentParser(description="End-to-End Enterprise HR Analytics Pipeline")
    parser.add_argument("--skip-ingest", action="store_true", help="Skip SQL Server ingestion")
    parser.add_argument("--skip-tests", action="store_true", help="Skip pytest test execution")
    args = parser.parse_args()

    start_time = time.time()
    logger.info("🚀 Starting Enterprise HR Analytics End-to-End Execution")

    # Step 1: Master Raw Data Check
    step_header(1, "Master Raw Dataset Verification")
    if not verify_master_raw_data():
        sys.exit(1)

    # Step 2: Galaxy Schema Mart Build
    step_header(2, "Galaxy Schema Dimensional Mart Build")
    if not run_galaxy_mart_build():
        sys.exit(1)

    # Step 3: SQL Server Ingestion
    if not args.skip_ingest:
        step_header(3, "Microsoft SQL Server Ingestion")
        run_sql_ingestion()

        # Step 4: Staging Transformations
        step_header(4, "Staging SCD2 Transformation Execution")
        run_staging_transformations()

        # Step 5: Presentation Mart Dimensional Transformations
        step_header(5, "Presentation Mart Dimensional Materialization")
        run_presentation_mart_transformations()
    else:
        logger.info("⏩ Skipping SQL Server ingestion and transformations (--skip-ingest).")

    # Step 6: Pytest Verification
    if not args.skip_tests:
        step_header(6, "Automated Data Quality & Contract Testing")
        if not run_pytest_suite():
            sys.exit(1)
    else:
        logger.info("⏩ Skipping automated tests (--skip-tests).")

    # Step 7: Summary
    step_header(7, "Enterprise DWH Inventory Verification")
    print_executive_summary()

    elapsed = time.time() - start_time
    logger.info(f"🎉 Pipeline finished successfully in {elapsed:.2f} seconds!")


if __name__ == "__main__":
    main()
