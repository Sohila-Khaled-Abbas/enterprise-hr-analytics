import sys
from sqlalchemy import text
from scripts.ingestion.ingest_hr_audit import get_db_engine

def list_tables():
    engine = get_db_engine()
    with engine.connect() as conn:
        res = conn.execute(text("SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' ORDER BY TABLE_SCHEMA, TABLE_NAME"))
        tables = [f"{r[0]}.{r[1]}" for r in res]
        print(f"Total tables found: {len(tables)}")
        for t in tables:
            print(f" - {t}")

if __name__ == '__main__':
    list_tables()
