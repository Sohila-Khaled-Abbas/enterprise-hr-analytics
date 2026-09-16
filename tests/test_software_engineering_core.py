"""
Unit and Integration Tests for Reusable Software Engineering Core Architecture.
Covers Configuration, Domain Entities, Data Contracts, File Handlers, and Migration Parser.
"""

import os
import sys
import tempfile
from pathlib import Path
import pandas as pd
import pytest

# Ensure src is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from enterprise_hr.core.config import AppConfig, DatabaseConfig, get_config
from enterprise_hr.core.constants import DatabaseSchema, MART_TABLE_MANIFEST, AuditStatus
from enterprise_hr.core.exceptions import (
    EnterpriseHRError,
    ConfigurationError,
    DataQualityValidationError,
    SchemaContractError,
)
from enterprise_hr.domain.models import (
    DepartmentEntity,
    BranchEntity,
    CurrencyRateEntity,
    ProjectTaskEntity,
)
from enterprise_hr.domain.contracts import DataContractValidator
from enterprise_hr.infrastructure.storage.file_handler import FileHandler
from enterprise_hr.infrastructure.database.migrations import MigrationManager


class TestCoreConfiguration:
    """Validates configuration loading and environment parsing."""

    def test_database_config_windows_auth(self):
        cfg = DatabaseConfig(user="", password="")
        assert cfg.is_windows_auth is True
        assert "Trusted_Connection=yes" in cfg.connection_string

    def test_database_config_sql_auth(self):
        cfg = DatabaseConfig(user="sa", password="SecretPassword123")
        assert cfg.is_windows_auth is False
        assert "UID=sa" in cfg.connection_string
        assert "PWD=SecretPassword123" in cfg.connection_string

    def test_app_config_paths(self):
        cfg = get_config()
        assert cfg.paths.project_root.exists()
        assert cfg.paths.raw_dir.name == "raw"
        assert cfg.paths.processed_dir.name == "processed"


class TestDomainModels:
    """Validates Pydantic domain models for data contracts."""

    def test_department_entity_valid(self):
        dept = DepartmentEntity(
            DepartmentKey=1,
            DepartmentID="DEP-01",
            DepartmentName="Technology & Engineering",
            Division="Technology",
            CostCenterCode="CC-TECH",
        )
        assert dept.department_id == "DEP-01"
        assert dept.department_name == "Technology & Engineering"

    def test_currency_rate_entity_valid(self):
        curr = CurrencyRateEntity(
            CurrencyKey=1,
            CurrencyCode="USD",
            CurrencyName="US Dollar",
            ExchangeRateToEGP=48.50,
            EffectiveDate="2026-01-01",
            IsActive=True,
        )
        assert curr.currency_code == "USD"
        assert curr.exchange_rate_to_egp == 48.50

    def test_project_task_entity_valid(self):
        task = ProjectTaskEntity(
            TaskID="TASK-001",
            ProjectID="PRJ-101",
            ProjectName="Core Banking Portal",
            ClientName="Commercial Bank",
            TaskName="API Integration",
            AssignedEmployeeID="EMP-1001",
            StartDate="2026-01-10",
            DueDate="2026-01-20",
            CompletionDate="2026-01-22",
            TaskStatus="Completed",
            EstimatedHours=40.0,
            ActualHours=48.0,
            HourlyRateUSD=65.0,
            TotalCostUSD=3120.0,
            CurrencyCode="USD",
            IsOverdue=True,
            OverrunHours=8.0,
        )
        assert task.is_overdue is True
        assert task.overrun_hours == 8.0


class TestDataContractValidator:
    """Validates the data contract assertion engine."""

    def test_assert_required_columns_success(self):
        df = pd.DataFrame({"ID": [1, 2], "Name": ["Alice", "Bob"]})
        DataContractValidator.assert_required_columns(df, ["ID", "Name"], "TestTable")

    def test_assert_required_columns_missing_raises(self):
        df = pd.DataFrame({"ID": [1, 2]})
        with pytest.raises(SchemaContractError):
            DataContractValidator.assert_required_columns(df, ["ID", "Name"], "TestTable")

    def test_assert_pk_uniqueness_success(self):
        df = pd.DataFrame({"ID": [1, 2, 3], "Val": ["A", "B", "C"]})
        DataContractValidator.assert_pk_uniqueness(df, "ID", "TestTable")

    def test_assert_pk_uniqueness_duplicate_raises(self):
        df = pd.DataFrame({"ID": [1, 2, 2], "Val": ["A", "B", "C"]})
        with pytest.raises(DataQualityValidationError):
            DataContractValidator.assert_pk_uniqueness(df, "ID", "TestTable")

    def test_assert_not_null_raises(self):
        df = pd.DataFrame({"ID": [1, 2], "Name": ["Alice", None]})
        with pytest.raises(DataQualityValidationError):
            DataContractValidator.assert_not_null(df, ["Name"], "TestTable")

    def test_assert_foreign_key_success(self):
        parent = pd.DataFrame({"DeptKey": [1, 2, 3]})
        child = pd.DataFrame({"EmpID": [101, 102], "DeptKey": [1, 2]})
        DataContractValidator.assert_foreign_key(child, "DeptKey", parent, "DeptKey")

    def test_assert_foreign_key_orphan_raises(self):
        parent = pd.DataFrame({"DeptKey": [1, 2]})
        child = pd.DataFrame({"EmpID": [101, 102], "DeptKey": [1, 999]})
        with pytest.raises(DataQualityValidationError) as exc:
            DataContractValidator.assert_foreign_key(child, "DeptKey", parent, "DeptKey")
        assert "orphan keys" in str(exc.value)


class TestFileHandler:
    """Validates atomic file operations."""

    def test_atomic_csv_write_and_read(self):
        handler = FileHandler()
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test_data.csv"
            df_in = pd.DataFrame({"Name": ["أحمد", "منى"], "Salary": [15000, 22000]})
            handler.write_csv(df_in, test_file)

            assert test_file.exists()
            df_out = handler.read_csv(test_file)
            assert len(df_out) == 2
            assert list(df_out["Name"]) == ["أحمد", "منى"]


class TestMigrationManagerScriptParsing:
    """Validates batch parsing for T-SQL migrations."""

    def test_parse_batches_with_go(self):
        sql = """
        USE EnterpriseHR_DWH;
        GO
        CREATE TABLE [dbo].[Test1] (ID INT);
        GO
        CREATE TABLE [dbo].[Test2] (ID INT);
        GO
        """
        migrator = MigrationManager.__new__(MigrationManager)
        batches = migrator.parse_batches(sql)
        assert len(batches) == 2
        assert "CREATE TABLE [dbo].[Test1]" in batches[0]
        assert "CREATE TABLE [dbo].[Test2]" in batches[1]
