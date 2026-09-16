"""
Database connectivity, session pooling, and migration subpackage.
"""

from enterprise_hr.infrastructure.database.connection import DatabaseManager, get_db_manager
from enterprise_hr.infrastructure.database.migrations import MigrationManager

__all__ = ["DatabaseManager", "get_db_manager", "MigrationManager"]
