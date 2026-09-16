"""
SQL Server Bulk Loader.
High-throughput, schema-aware data loader handling table truncations, identity exclusions, and column alignments.
"""

from __future__ import annotations

from typing import Optional, List
import pandas as pd
from sqlalchemy import text, inspect

from enterprise_hr.core.config import get_config
from enterprise_hr.core.constants import AUTO_IDENTITY_COLUMNS
from enterprise_hr.core.interfaces import BaseLoader
from enterprise_hr.core.logging import get_logger
from enterprise_hr.infrastructure.database.connection import DatabaseManager, get_db_manager

logger = get_logger("SqlBulkLoader")


class SqlBulkLoader(BaseLoader):
    """Encapsulates fast batch loading of DataFrames into Microsoft SQL Server."""

    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db = db_manager or get_db_manager()
        self.config = get_config()

    def load(
        self,
        data: pd.DataFrame,
        target_table: str,
        truncate: bool = False,
        pk_column: Optional[str] = None,
    ) -> int:
        """
        Loads a pandas DataFrame into target table with column mapping and type safety.

        Args:
            data: DataFrame to load
            target_table: Fully qualified table name (e.g. 'mart.Dim_Employee')
            truncate: Whether to truncate the table before insert
            pk_column: Optional primary key for deduplication check

        Returns:
            Number of rows successfully inserted
        """
        if data.empty:
            logger.warning("Empty DataFrame provided for %s. Skipping.", target_table)
            return 0

        schema_name, table_name = target_table.split(".")
        df = data.copy()

        # Deduplicate on PK if present
        if pk_column and pk_column in df.columns:
            dups = df[pk_column].duplicated().sum()
            if dups > 0:
                logger.warning("Deduplicating %d duplicate keys on '%s' for %s", dups, pk_column, target_table)
                df = df.drop_duplicates(subset=[pk_column], keep="last")

        # Parse date columns
        for col in df.columns:
            if col.endswith("Key") or col.endswith("ID") or col.endswith("Code"):
                continue
            col_lower = col.lower()
            if any(kw in col_lower for kw in ["fulldate", "effectivedate", "expirydate", "hiredate", "duedate", "startdate", "completiondate"]):
                try:
                    df[col] = pd.to_datetime(df[col], errors="coerce").dt.date
                except Exception:
                    pass

        # Truncate if requested
        if truncate:
            try:
                with self.db.engine.connect() as conn:
                    inspector = inspect(self.db.engine)
                    if table_name in inspector.get_table_names(schema=schema_name):
                        conn.execute(text(f"TRUNCATE TABLE {target_table}"))
                        conn.commit()
                        logger.info("🗑️  Truncated %s", target_table)
            except Exception as e:
                logger.warning("Could not truncate %s: %s", target_table, e)

        # Inspect target table schema for column alignment and identity handling
        try:
            inspector = inspect(self.db.engine)
            existing_cols = [c["name"] for c in inspector.get_columns(table_name, schema=schema_name)]

            if existing_cols:
                # Drop auto-identity columns from DataFrame
                for id_col in AUTO_IDENTITY_COLUMNS:
                    if id_col in df.columns and id_col in existing_cols:
                        df = df.drop(columns=[id_col])

                # Support schema evolution variants for Dim_Employee
                if table_name == "Dim_Employee":
                    if "EmploymentStatus" in existing_cols and "EmploymentStatus" not in df.columns:
                        df["EmploymentStatus"] = "Active"
                    if "LatestSalary" in existing_cols and "LatestSalary" not in df.columns:
                        df["LatestSalary"] = df.get("BaseSalary", 0.0)
                    if "LatestBranch" in existing_cols and "LatestBranch" not in df.columns:
                        branch_val = df.get("BranchKey", 1)
                        df["LatestBranch"] = "Branch-" + branch_val.astype(str)

                # Filter down to common columns only
                common_cols = [c for c in df.columns if c in existing_cols]
                if common_cols:
                    df = df[common_cols]
        except Exception as ex:
            logger.warning("Schema inspection warning for %s: %s", target_table, ex)

        # Insert using fast_executemany
        try:
            chunk_size = self.config.pipeline.chunk_size
            df.to_sql(
                name=table_name,
                schema=schema_name,
                con=self.db.engine,
                if_exists="append",
                index=False,
                chunksize=chunk_size,
            )
            logger.info("   ✅ Inserted %s rows into %s", f"{len(df):,}", target_table)
            return len(df)
        except Exception as e:
            logger.error("   ❌ Failed to insert into %s: %s", target_table, e)
            raise
