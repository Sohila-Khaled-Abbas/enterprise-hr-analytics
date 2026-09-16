"""
Enterprise HR Analytics Constants & Schemas.
Defines canonical schema names, table manifests, column names, and audit codes.
"""

from enum import Enum
from typing import Dict, Tuple, List


class DatabaseSchema(str, Enum):
    """Database schema namespaces in EnterpriseHR_DWH."""
    RAW = "raw"
    STG = "stg"
    MART = "mart"
    DBO = "dbo"


class AuditStatus(str, Enum):
    """Pipeline execution status enumeration."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


class FileEncoding(str, Enum):
    """Supported file encodings."""
    UTF8_SIG = "utf-8-sig"
    UTF8 = "utf-8"
    CP1256 = "windows-1256"


# Canonical mapping for Mart tables: CSV Filename -> (Full Table Name, Primary Key Column, IsFact)
MART_TABLE_MANIFEST: Dict[str, Tuple[str, str, bool]] = {
    # Conformed Dimensions (Ingested first)
    "Dim_Date.csv": ("mart.Dim_Date", "DateKey", False),
    "Dim_Department.csv": ("mart.Dim_Department", "DepartmentKey", False),
    "Dim_Branch.csv": ("mart.Dim_Branch", "BranchKey", False),
    "Dim_Course.csv": ("mart.Dim_Course", "CourseKey", False),
    "Dim_CurrencyRates.csv": ("mart.Dim_CurrencyRates", "CurrencyKey", False),
    "Dim_Employee.csv": ("mart.Dim_Employee", "EmployeeKey", False),
    # Galaxy Fact Tables (Ingested second)
    "Fact_WorkforceSnapshot.csv": ("mart.Fact_WorkforceSnapshot", "SnapshotKey", True),
    "Fact_DailyAttendance.csv": ("mart.Fact_DailyAttendance", "AttendanceKey", True),
    "Fact_DepartmentBudget.csv": ("mart.Fact_DepartmentBudget", "BudgetKey", True),
    "Fact_TrainingCompletions.csv": ("mart.Fact_TrainingCompletions", "CompletionKey", True),
    "Fact_ProjectTasks.csv": ("mart.Fact_ProjectTasks", "TaskKey", True),
}

DIMENSION_LOAD_ORDER: List[str] = [
    "Dim_Date.csv",
    "Dim_Department.csv",
    "Dim_Branch.csv",
    "Dim_Course.csv",
    "Dim_CurrencyRates.csv",
    "Dim_Employee.csv",
]

FACT_LOAD_ORDER: List[str] = [
    "Fact_WorkforceSnapshot.csv",
    "Fact_DailyAttendance.csv",
    "Fact_DepartmentBudget.csv",
    "Fact_TrainingCompletions.csv",
    "Fact_ProjectTasks.csv",
]

# Raw Ingestion Manifest: Source Filename -> (Full Target Table, PK Column)
RAW_TABLE_MANIFEST: Dict[str, Tuple[str, str]] = {
    "api_badge_logs_202605.json": ("raw.Badge_Access_Logs", "LogID"),
    "finance_budget_2026.xlsx": ("raw.Finance_Budget_Plan", "BudgetID"),
    "lms_certifications.csv": ("raw.LMS_Certifications", "LogID"),
    "client_projects_tasks.csv": ("raw.Client_Projects_Tasks", "RawTaskID"),
    "dim_currency_rates.csv": ("raw.Currency_Rates", "RawCurrencyID"),
}

# Identity columns that should not receive explicit inserts in SQL Server
AUTO_IDENTITY_COLUMNS = {
    "TaskKey",
    "RawTaskID",
    "RawCurrencyID",
    "StagingKey",
    "AuditID",
}
