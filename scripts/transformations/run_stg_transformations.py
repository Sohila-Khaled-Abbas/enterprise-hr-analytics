# scripts/transformations/run_stg_transformations.py
# ═══════════════════════════════════════════════════════════════════════
# Enterprise HR Analytics – Staging Transformation Orchestrator
# Executes T-SQL transformation scripts against SQL Server,
# splitting on GO batch separators for proper multi-statement execution.
# ═══════════════════════════════════════════════════════════════════════
import os
import re
import sys
import logging
from pathlib import Path

# Ensure project root is on the path for cross-module imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from sqlalchemy import text
from scripts.ingestion.ingest_hr_audit import get_db_engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-8s │ %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def run_sql_script(file_path: str) -> None:
    """Executes a multi-statement T-SQL script file against SQL Server.

    Splits the script on GO batch terminators (case-insensitive, line-only)
    and executes each batch in its own transaction.
    """
    abs_path = Path(file_path).resolve()
    if not abs_path.exists():
        logger.error(f"SQL file not found at {abs_path}")
        raise FileNotFoundError(abs_path)

    logger.info(f"📄 Reading SQL script: {abs_path.name}")
    sql_script = abs_path.read_text(encoding="utf-8")

    # Split on GO statements that appear on their own line
    # (handles optional surrounding whitespace)
    sql_batches = re.split(r"^\s*GO\s*$", sql_script, flags=re.MULTILINE | re.IGNORECASE)
    sql_batches = [b.strip() for b in sql_batches if b.strip()]

    logger.info(f"🔀 Found {len(sql_batches)} batch(es) to execute")

    engine = get_db_engine()

    try:
        with engine.connect() as connection:
            for i, batch in enumerate(sql_batches, 1):
                # Skip USE statements – SQLAlchemy connection already targets the DB
                if batch.upper().startswith("USE "):
                    logger.info(f"  Batch {i}/{len(sql_batches)}: Skipped USE statement")
                    continue

                logger.info(f"  Batch {i}/{len(sql_batches)}: Executing ({len(batch)} chars)...")
                result = connection.execute(text(batch))

                # If the batch returns rows (e.g., verification SELECT), print them
                if result.returns_rows:
                    rows = result.fetchall()
                    if rows:
                        logger.info(f"  📊 Result ({len(rows)} rows):")
                        for row in rows:
                            logger.info(f"     {dict(row._mapping)}")

                connection.commit()
                logger.info(f"  ✅ Batch {i} committed successfully")

        logger.info("═" * 60)
        logger.info("🎉 Staging transformation completed successfully!")
        logger.info("═" * 60)

    except Exception as e:
        logger.error(f"❌ SQL execution failed: {e}")
        raise


if __name__ == "__main__":
    SCRIPT_PATH = PROJECT_ROOT / "sql" / "transformations" / "00_stg_hr_audit.sql"
    run_sql_script(str(SCRIPT_PATH))
