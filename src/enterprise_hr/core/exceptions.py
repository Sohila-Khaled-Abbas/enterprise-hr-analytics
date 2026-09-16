"""
Enterprise HR Custom Exception Hierarchy.
Provides clear, actionable error types across configuration, database, data quality, and pipelines.
"""

from typing import Optional, List, Dict, Any


class EnterpriseHRError(Exception):
    """Base exception for all Enterprise HR platform errors."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message


class ConfigurationError(EnterpriseHRError):
    """Raised when environment configuration or settings are invalid or missing."""
    pass


class DatabaseConnectionError(EnterpriseHRError):
    """Raised when the database engine fails to connect or ping."""
    pass


class DatabaseExecutionError(EnterpriseHRError):
    """Raised when a SQL statement, DDL, or stored procedure fails execution."""
    pass


class MigrationError(EnterpriseHRError):
    """Raised when a schema migration script fails to apply."""
    pass


class DataQualityValidationError(EnterpriseHRError):
    """Raised when data contracts, nullability, or uniqueness checks fail."""
    def __init__(self, message: str, violations: Optional[List[str]] = None):
        super().__init__(message, {"violations": violations or []})
        self.violations = violations or []


class SchemaContractError(DataQualityValidationError):
    """Raised when columns or data types do not conform to expected contracts."""
    pass


class PipelineStepError(EnterpriseHRError):
    """Raised when a specific ETL pipeline stage fails."""
    def __init__(self, step_name: str, message: str, cause: Optional[Exception] = None):
        super().__init__(f"Step '{step_name}' failed: {message}", {"cause": str(cause) if cause else None})
        self.step_name = step_name
        self.cause = cause


class StorageError(EnterpriseHRError):
    """Raised when file I/O or data lake serialization fails."""
    pass
