# scripts/ingestion/ingest_badge_logs.py
import json
import logging
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

def ingest_badge_logs(file_path: str, schema_name: str, table_name: str):
    """Flattens nested JSON and loads it into the SQL Server staging area."""
    try:
        resolved_path = Path(file_path)
        if not resolved_path.is_absolute():
            resolved_path = BASE_DIR / file_path

        logging.info(f"Parsing JSON payload from {resolved_path}...")
        with open(resolved_path, "r", encoding="utf-8") as f:
            payload = json.load(f)
            
        # Flatten the nested JSON structure
        # Normalizes: event.timestamps.first_in -> event.timestamps.first_in
        df = pd.json_normalize(payload['data'])
        
        # Rename columns to remove JSON path artifacts for SQL compatibility
        df = df.rename(columns={
            "meta.log_id": "LogID",
            "meta.source": "SystemSource",
            "event.employee_id": "EmployeeID",
            "event.access_date": "AccessDate",
            "event.facility_code": "FacilityCode",
            "event.timestamps.first_in": "CheckInTime",
            "event.timestamps.last_out": "CheckOutTime"
        })
        
        from sqlalchemy.types import VARCHAR

        engine = get_db_engine()
        logging.info(f"Loading {len(df)} flattened records into {schema_name}.{table_name}...")
        
        badge_dtype_map = {
            "LogID": VARCHAR(50),
            "SystemSource": VARCHAR(50),
            "EmployeeID": VARCHAR(20),
            "AccessDate": VARCHAR(20),
            "FacilityCode": VARCHAR(20),
            "CheckInTime": VARCHAR(30),
            "CheckOutTime": VARCHAR(30)
        }

        df.to_sql(
            name=table_name,
            con=engine,
            schema=schema_name,
            if_exists='replace', # Use 'append' for daily rolling loads
            index=False,
            chunksize=10000,
            dtype=badge_dtype_map
        )
        logging.info("Badge log ingestion complete.")
        
    except Exception as e:
        logging.error(f"Ingestion failed: {str(e)}")
        raise e

if __name__ == "__main__":
    SOURCE_JSON = "data/raw/api_badge_logs_202605.json"
    ingest_badge_logs(SOURCE_JSON, "raw", "Badge_Access_Logs")
