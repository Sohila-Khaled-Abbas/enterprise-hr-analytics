# scripts/ingestion/ingest_lms_data.py
import logging
import os
import sys
from pathlib import Path
import pandas as pd

# Add project root and current script directory to sys.path for flexible execution
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

try:
    from scripts.ingestion.ingest_hr_audit import get_db_engine
except ImportError:
    from ingest_hr_audit import get_db_engine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def ingest_lms_logs(file_path: str, schema_name: str, table_name: str):
    """Loads raw LMS training logs into the SQL Server staging/raw area."""
    resolved_path = Path(file_path)
    if not resolved_path.is_absolute():
        resolved_path = BASE_DIR / file_path

    if not resolved_path.exists():
        logging.error(f"Source file {resolved_path} not found.")
        return

    try:
        logging.info(f"Reading LMS data from {resolved_path}...")
        df = pd.read_csv(resolved_path)
        
        from sqlalchemy.types import VARCHAR, Float

        engine = get_db_engine()
        logging.info(f"Loading {len(df)} records into {schema_name}.{table_name}...")
        
        dtype_map = {
            "EmployeeID": VARCHAR(20),
            "CourseID": VARCHAR(20),
            "CourseName": VARCHAR(150),
            "SkillDomain": VARCHAR(50),
            "CompletionDate": VARCHAR(30),
            "Score": Float(),
            "Status": VARCHAR(30),
            "Cost_EGP": Float()
        }

        df.to_sql(
            name=table_name,
            con=engine,
            schema=schema_name,
            if_exists='replace',
            index=False,
            chunksize=5000,
            dtype=dtype_map
        )
        logging.info("LMS data ingestion complete.")
        
    except Exception as e:
        logging.error(f"Ingestion failed: {str(e)}")
        raise

if __name__ == "__main__":
    SOURCE_CSV = "data/raw/lms_certifications.csv"
    ingest_lms_logs(SOURCE_CSV, "raw", "LMS_Certifications")
