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

def ingest_finance_data(file_path: str, schema_name: str, table_name: str):
    """Reads pivoted Excel, unpivots it, and loads to SQL Server staging."""
    try:
        resolved_path = Path(file_path)
        if not resolved_path.is_absolute():
            resolved_path = BASE_DIR / file_path

        logging.info(f"Reading messy Excel from {resolved_path}...")
        df = pd.read_excel(resolved_path, sheet_name="Budget_2026")
        
        # 1. Unpivot (Melt) the dataframe
        # Converts wide columns (Q1_Headcount, etc.) into two columns: Quarter_Metric and Value
        df_melted = df.melt(
            id_vars=["Department", "CostCenter_Branch"], 
            var_name="Quarter_Metric", 
            value_name="Value"
        )
        
        # 2. Extract Quarter and MetricType
        # Regex splits 'Q1_Headcount' into 'Q1' and 'Headcount'
        df_melted[['Quarter', 'MetricType']] = df_melted['Quarter_Metric'].str.extract(r'(Q[1-4])_(.*)')
        df_melted = df_melted.drop(columns=['Quarter_Metric'])
        
        # 3. Pivot the metrics back so 'Headcount' and 'Budget_EGP' are distinct columns
        df_final = df_melted.pivot_table(
            index=["Department", "CostCenter_Branch", "Quarter"],
            columns="MetricType",
            values="Value"
        ).reset_index()
        
        # 4. Append context
        df_final['FiscalYear'] = 2026
        
        engine = get_db_engine()
        logging.info(f"Loading {len(df_final)} normalized records into {schema_name}.{table_name}...")
        
        df_final.to_sql(
            name=table_name,
            con=engine,
            schema=schema_name,
            if_exists='replace',
            index=False
        )
        logging.info("Finance data ingestion complete.")
        
    except Exception as e:
        logging.error(f"Ingestion failed: {str(e)}")
        raise

if __name__ == "__main__":
    SOURCE_EXCEL = "data/raw/finance_budget_2026.xlsx"
    ingest_finance_data(SOURCE_EXCEL, "raw", "Finance_Budget_Plan")
