"""
Database Connection & Session Management.
Encapsulates SQLAlchemy engine creation, pooling, and health verification for Microsoft SQL Server.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator, List, Dict, Any, Optional
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text, inspect, Engine, Connection

from enterprise_hr.core.config import DatabaseConfig, get_config
from enterprise_hr.core.exceptions import DatabaseConnectionError, DatabaseExecutionError
from enterprise_hr.core.logging import get_logger

logger = get_logger("DatabaseManager")


class DatabaseManager:
    """
    Thread-safe connection and pool manager for Microsoft SQL Server.
    Adheres to the Singleton and Repository infrastructure patterns.
    """
    _instance: Optional[DatabaseManager] = None
    _engine: Optional[Engine] = None

    def __init__(self, config: Optional[DatabaseConfig] = None):
        self.config = config or get_config().database
        self._initialize_engine()

    @classmethod
    def get_instance(cls, config: Optional[DatabaseConfig] = None) -> DatabaseManager:
        """Singleton accessor for the DatabaseManager."""
        if cls._instance is None:
            cls._instance = cls(config)
        return cls._instance

    def _initialize_engine(self) -> None:
        """Builds the SQLAlchemy engine using URL-encoded pyodbc connection string."""
        try:
            conn_str = self.config.connection_string
            engine_url = f"mssql+pyodbc:///?odbc_connect={quote_plus(conn_str)}"
            
            self._engine = create_engine(
                engine_url,
                fast_executemany=self.config.fast_executemany,
                pool_pre_ping=True,
                pool_size=self.config.pool_size,
                max_overflow=self.config.max_overflow,
            )
            auth_type = "Windows Integrated Security" if self.config.is_windows_auth else f"SQL User '{self.config.user}'"
            logger.info("📡 Initialized SQL Server Engine pool on '%s' via %s", self.config.server, auth_type)
        except Exception as e:
            raise DatabaseConnectionError(f"Failed to create SQLAlchemy engine: {e}") from e

    @property
    def engine(self) -> Engine:
        """Returns the underlying SQLAlchemy engine instance."""
        if self._engine is None:
            self._initialize_engine()
        return self._engine

    @contextmanager
    def get_connection(self) -> Generator[Connection, None, None]:
        """
        Context manager yielding an active connection with transaction management.
        Automatically commits on successful block exit, or rolls back on exception.
        """
        conn = self.engine.connect()
        trans = conn.begin()
        try:
            yield conn
            trans.commit()
        except Exception as e:
            trans.rollback()
            logger.error("Transaction rolled back due to error: %s", e)
            raise DatabaseExecutionError(f"Database transaction failed: {e}") from e
        finally:
            conn.close()

    def is_healthy(self) -> bool:
        """Verifies database connectivity and essential schemas."""
        try:
            with self.engine.connect() as conn:
                res = conn.execute(text("SELECT @@VERSION AS ServerVersion"))
                row = res.fetchone()
                if not row:
                    return False
                
                # Check for enterprise schemas
                schema_res = conn.execute(
                    text("SELECT s.name FROM sys.schemas s WHERE s.name IN ('raw', 'stg', 'mart')")
                )
                schemas = {r[0] for r in schema_res.fetchall()}
                missing = {'raw', 'stg', 'mart'} - schemas
                if missing:
                    logger.warning("Missing schemas in database: %s", missing)
                return True
        except Exception as e:
            logger.error("Healthcheck connection failed: %s", e)
            return False

    def get_table_row_count(self, full_table_name: str) -> int:
        """Returns row count for a given table safely."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {full_table_name}"))
                return int(result.scalar() or 0)
        except Exception:
            return 0

    def get_existing_columns(self, table_name: str, schema_name: str) -> List[str]:
        """Uses SQLAlchemy inspector to retrieve active column names."""
        try:
            inspector = inspect(self.engine)
            cols = inspector.get_columns(table_name, schema=schema_name)
            return [c["name"] for c in cols]
        except Exception as e:
            logger.warning("Could not inspect columns for %s.%s: %s", schema_name, table_name, e)
            return []

    def dispose(self) -> None:
        """Disposes connection pool resources."""
        if self._engine:
            self._engine.dispose()
            self._engine = None


def get_db_manager() -> DatabaseManager:
    """Convenience provider for DatabaseManager singleton."""
    return DatabaseManager.get_instance()
