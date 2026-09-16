"""
Data Contract and Quality Assertions.
Provides a reusable validation engine for data engineering pipelines.
"""

from __future__ import annotations

from typing import List, Optional, Any
import pandas as pd

from enterprise_hr.core.exceptions import DataQualityValidationError, SchemaContractError
from enterprise_hr.core.logging import get_logger

logger = get_logger("DataContracts")


class DataContractValidator:
    """Automated validator ensuring data contracts and referential integrity."""

    @staticmethod
    def assert_required_columns(df: pd.DataFrame, required_columns: List[str], table_name: str = "") -> None:
        """Verifies that all specified columns exist in the DataFrame."""
        missing = [c for c in required_columns if c not in df.columns]
        if missing:
            raise SchemaContractError(
                f"Table '{table_name}' failed contract: Missing required columns: {missing}",
                violations=missing,
            )

    @staticmethod
    def assert_pk_uniqueness(df: pd.DataFrame, pk_column: str, table_name: str = "") -> None:
        """Verifies that the primary key contains no duplicates or nulls."""
        if pk_column not in df.columns:
            raise SchemaContractError(f"Primary key '{pk_column}' not found in '{table_name}'")

        null_count = df[pk_column].isnull().sum()
        if null_count > 0:
            raise DataQualityValidationError(
                f"Primary key '{pk_column}' in '{table_name}' contains {null_count} NULL values."
            )

        dup_count = df[pk_column].duplicated().sum()
        if dup_count > 0:
            raise DataQualityValidationError(
                f"Primary key '{pk_column}' in '{table_name}' contains {dup_count} duplicate values."
            )

    @staticmethod
    def assert_not_null(df: pd.DataFrame, columns: List[str], table_name: str = "") -> None:
        """Verifies that non-nullable columns contain no missing or empty values."""
        violations = []
        for col in columns:
            if col in df.columns:
                null_count = df[col].isnull().sum()
                if null_count > 0:
                    violations.append(f"Column '{col}' has {null_count} nulls")
        if violations:
            raise DataQualityValidationError(
                f"Table '{table_name}' violated NOT NULL constraint.", violations=violations
            )

    @staticmethod
    def assert_foreign_key(
        child_df: pd.DataFrame,
        child_fk_col: str,
        parent_df: pd.DataFrame,
        parent_pk_col: str,
        child_table_name: str = "Child",
        parent_table_name: str = "Parent",
    ) -> None:
        """Verifies referential integrity between a child foreign key and parent primary key."""
        if child_fk_col not in child_df.columns:
            raise SchemaContractError(f"FK column '{child_fk_col}' not found in '{child_table_name}'")
        if parent_pk_col not in parent_df.columns:
            raise SchemaContractError(f"PK column '{parent_pk_col}' not found in '{parent_table_name}'")

        parent_keys = set(parent_df[parent_pk_col].dropna().unique())
        orphan_keys = set(child_df[child_fk_col].dropna().unique()) - parent_keys

        if orphan_keys:
            sample = list(orphan_keys)[:5]
            raise DataQualityValidationError(
                f"Referential integrity failure: {len(orphan_keys)} orphan keys in '{child_table_name}.{child_fk_col}' "
                f"referencing '{parent_table_name}.{parent_pk_col}'. Sample: {sample}"
            )

    @staticmethod
    def assert_numeric_range(
        df: pd.DataFrame,
        column: str,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        table_name: str = "",
    ) -> None:
        """Verifies that a numeric column values are strictly within acceptable bounds."""
        if column not in df.columns:
            return

        series = pd.to_numeric(df[column], errors="coerce").dropna()
        if min_value is not None:
            under = (series < min_value).sum()
            if under > 0:
                raise DataQualityValidationError(
                    f"Column '{column}' in '{table_name}' has {under} values below minimum threshold {min_value}."
                )
        if max_value is not None:
            over = (series > max_value).sum()
            if over > 0:
                raise DataQualityValidationError(
                    f"Column '{column}' in '{table_name}' has {over} values above maximum threshold {max_value}."
                )
