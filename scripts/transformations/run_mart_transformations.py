# scripts/transformations/run_mart_transformations.py
import os
import sys
import re
import logging
from pathlib import Path
from sqlalchemy import text

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.ingestion.ingest_hr_audit import get_db_engine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def run_mart_script(file_path: str):
    """Executes the dimensional model SQL script against SQL Server."""
    resolved_path = Path(file_path)
    if not resolved_path.is_absolute():
        resolved_path = PROJECT_ROOT / file_path

    if not resolved_path.exists():
        logging.error(f"SQL file not found at {resolved_path}")
        return

    engine = get_db_engine()
    
    with open(resolved_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()

    sql_batches = re.split(r"^\s*GO\s*$", sql_script, flags=re.MULTILINE | re.IGNORECASE)
    sql_batches = [batch.strip() for batch in sql_batches if batch.strip()]

    try:
        with engine.connect() as connection:
            for i, batch in enumerate(sql_batches):
                if batch.upper().startswith("USE "):
                    continue
                logging.info(f"Executing mart batch {i + 1} of {len(sql_batches)}...")
                connection.execute(text(batch))
                connection.commit()
        logging.info("Dimensional mart tables created successfully.")
    except Exception as e:
        logging.error(f"Mart build failed: {str(e)}")
        raise

if __name__ == "__main__":
    SCRIPT_PATH = "sql/transformations/02_mart_dimensional_model.sql"
    run_mart_script(SCRIPT_PATH)
