# scripts/ingestion/ingest_software_house_data.py
import logging
import sys
from pathlib import Path
import pandas as pd
from sqlalchemy import text

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from scripts.ingestion.ingest_hr_audit import get_db_engine
except ImportError:
    from ingest_hr_audit import get_db_engine

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)


def ingest_client_projects_tasks(file_path: str = "data/raw/client_projects_tasks.csv", schema_name: str = "raw", table_name: str = "Client_Projects_Tasks"):
    """Ingests raw client tasks data into SQL Server."""
    resolved = BASE_DIR / file_path if not Path(file_path).is_absolute() else Path(file_path)
    if not resolved.exists():
        logger.warning("File not found: %s", resolved)
        return 0

    logger.info("Reading %s...", resolved.name)
    df = pd.read_csv(resolved, encoding="utf-8-sig")

    for date_col in ["TaskStartDate", "DeliveryDeadline", "ActualCompletionDate"]:
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce").dt.date

    engine = get_db_engine()
    try:
        with engine.connect() as conn:
            conn.execute(text(f"TRUNCATE TABLE {schema_name}.{table_name}"))
            conn.commit()
            logger.info("Truncated %s.%s", schema_name, table_name)
    except Exception as e:
        logger.warning("Could not truncate %s.%s: %s", schema_name, table_name, e)

    df.to_sql(
        name=table_name,
        schema=schema_name,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=1000,
    )
    logger.info("✅ Ingested %d rows into %s.%s", len(df), schema_name, table_name)
    return len(df)


def ingest_currency_rates(file_path: str = "data/raw/dim_currency_rates.csv", schema_name: str = "raw", table_name: str = "Currency_Rates"):
    """Ingests raw currency exchange rates into SQL Server."""
    resolved = BASE_DIR / file_path if not Path(file_path).is_absolute() else Path(file_path)
    if not resolved.exists():
        logger.warning("File not found: %s", resolved)
        return 0

    logger.info("Reading %s...", resolved.name)
    df = pd.read_csv(resolved, encoding="utf-8-sig")

    if "CurrencyKey" in df.columns:
        df = df.drop(columns=["CurrencyKey"])

    if "LastUpdated" in df.columns:
        df["LastUpdated"] = pd.to_datetime(df["LastUpdated"], errors="coerce")

    engine = get_db_engine()
    try:
        with engine.connect() as conn:
            conn.execute(text(f"TRUNCATE TABLE {schema_name}.{table_name}"))
            conn.commit()
            logger.info("Truncated %s.%s", schema_name, table_name)
    except Exception as e:
        logger.warning("Could not truncate %s.%s: %s", schema_name, table_name, e)

    df.to_sql(
        name=table_name,
        schema=schema_name,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=1000,
    )
    logger.info("✅ Ingested %d rows into %s.%s", len(df), schema_name, table_name)
    return len(df)


if __name__ == "__main__":
    ingest_client_projects_tasks()
    ingest_currency_rates()
