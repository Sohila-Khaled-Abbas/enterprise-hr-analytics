"""
Enterprise Configuration & Environment Management Module.
Implements strongly-typed configuration loaded from environment variables and .env files.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator


class DatabaseConfig(BaseModel):
    """Database connection settings."""
    driver: str = Field(default="{ODBC Driver 17 for SQL Server}", description="ODBC Driver string")
    server: str = Field(default="localhost", description="Database server address or hostname")
    database: str = Field(default="EnterpriseHR_DWH", description="Target database name")
    user: str = Field(default="", description="SQL Server username (empty for Windows Auth)")
    password: str = Field(default="", description="SQL Server password")
    trust_server_certificate: bool = Field(default=True, description="Trust self-signed server cert")
    fast_executemany: bool = Field(default=True, description="Enable pyodbc fast_executemany bulk loading")
    pool_size: int = Field(default=5, ge=1, le=50, description="SQLAlchemy pool size")
    max_overflow: int = Field(default=10, ge=0, le=100, description="SQLAlchemy connection pool overflow")

    @property
    def is_windows_auth(self) -> bool:
        """Returns True if Windows Integrated Authentication should be used."""
        return not bool(self.user and self.user.strip())

    @property
    def connection_string(self) -> str:
        """Generates the raw ODBC connection string."""
        trust_cert = "yes" if self.trust_server_certificate else "no"
        if self.is_windows_auth:
            return (
                f"DRIVER={self.driver};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"Trusted_Connection=yes;"
                f"TrustServerCertificate={trust_cert};"
            )
        return (
            f"DRIVER={self.driver};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            f"UID={self.user};"
            f"PWD={self.password};"
            f"TrustServerCertificate={trust_cert};"
        )


class PathConfig(BaseModel):
    """Filesystem path configuration for data lake and warehouse assets."""
    project_root: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent.parent.parent)
    data_dir: Path = Field(default=Path())
    raw_dir: Path = Field(default=Path())
    processed_dir: Path = Field(default=Path())
    sql_dir: Path = Field(default=Path())
    docs_dir: Path = Field(default=Path())

    def model_post_init(self, __context: any) -> None:
        if self.data_dir == Path():
            self.data_dir = self.project_root / "data"
        if self.raw_dir == Path():
            self.raw_dir = self.data_dir / "raw"
        if self.processed_dir == Path():
            self.processed_dir = self.data_dir / "processed"
        if self.sql_dir == Path():
            self.sql_dir = self.project_root / "sql"
        if self.docs_dir == Path():
            self.docs_dir = self.project_root / "docs"


class PipelineConfig(BaseModel):
    """Pipeline execution parameters and feature flags."""
    environment: str = Field(default="development", description="Environment: development, staging, production")
    chunk_size: int = Field(default=1000, ge=100, le=10000, description="Batch insert chunk size")
    log_level: str = Field(default="INFO", description="Logging level")
    dry_run: bool = Field(default=False, description="Dry run mode without committing data")
    expected_employee_count: int = Field(default=7000, description="Strict master employee count validation threshold")


class AppConfig(BaseModel):
    """Unified application configuration root."""
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    paths: PathConfig = Field(default_factory=PathConfig)
    pipeline: PipelineConfig = Field(default_factory=PipelineConfig)

    @classmethod
    def load(cls, env_file: Optional[Path] = None) -> AppConfig:
        """Loads configuration from environment variables and optional .env file."""
        root = Path(__file__).resolve().parent.parent.parent.parent
        if env_file is None:
            candidate_env = root / ".env"
            if candidate_env.exists():
                load_dotenv(candidate_env, override=False)
        else:
            load_dotenv(env_file, override=True)

        db_cfg = DatabaseConfig(
            driver=os.getenv("DB_DRIVER", "{ODBC Driver 17 for SQL Server}"),
            server=os.getenv("DB_SERVER", "localhost"),
            database=os.getenv("DB_DATABASE", "EnterpriseHR_DWH"),
            user=os.getenv("DB_USER", ""),
            password=os.getenv("DB_PASS", ""),
            trust_server_certificate=os.getenv("DB_TRUST_CERT", "true").lower() in ("true", "1", "yes"),
            pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
            max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
        )

        paths_cfg = PathConfig(project_root=root)
        pipe_cfg = PipelineConfig(
            environment=os.getenv("APP_ENV", "development"),
            chunk_size=int(os.getenv("PIPELINE_CHUNK_SIZE", "1000")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            dry_run=os.getenv("DRY_RUN", "false").lower() in ("true", "1", "yes"),
            expected_employee_count=int(os.getenv("EXPECTED_EMPLOYEE_COUNT", "7000")),
        )

        return cls(database=db_cfg, paths=paths_cfg, pipeline=pipe_cfg)


@lru_cache(maxsize=1)
def get_config() -> AppConfig:
    """Returns a memoized singleton instance of the application configuration."""
    return AppConfig.load()
