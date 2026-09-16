"""
Core abstractions, configurations, constants, exceptions, and interfaces.
"""

from enterprise_hr.core.config import AppConfig, get_config
from enterprise_hr.core.constants import (
    DatabaseSchema,
    MART_TABLE_MANIFEST,
    RAW_TABLE_MANIFEST,
    FileEncoding,
    AuditStatus,
)
from enterprise_hr.core.exceptions import (
    EnterpriseHRError,
    ConfigurationError,
    DatabaseConnectionError,
    DataQualityValidationError,
    PipelineStepError,
    MigrationError,
)
from enterprise_hr.core.logging import get_logger
from enterprise_hr.core.interfaces import (
    BaseExtractor,
    BaseTransformer,
    BaseLoader,
    BasePipelineStep,
)

__all__ = [
    "AppConfig",
    "get_config",
    "DatabaseSchema",
    "MART_TABLE_MANIFEST",
    "RAW_TABLE_MANIFEST",
    "FileEncoding",
    "AuditStatus",
    "EnterpriseHRError",
    "ConfigurationError",
    "DatabaseConnectionError",
    "DataQualityValidationError",
    "PipelineStepError",
    "MigrationError",
    "get_logger",
    "BaseExtractor",
    "BaseTransformer",
    "BaseLoader",
    "BasePipelineStep",
]
