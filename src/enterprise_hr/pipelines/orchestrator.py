"""
Enterprise Pipeline Orchestration Engine.
Orchestrates multi-stage data processing with telemetry, automated retries, and execution audit tracking.
"""

from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from sqlalchemy import text, Connection

from enterprise_hr.core.config import get_config
from enterprise_hr.core.constants import (
    MART_TABLE_MANIFEST,
    DIMENSION_LOAD_ORDER,
    FACT_LOAD_ORDER,
    RAW_TABLE_MANIFEST,
    AuditStatus,
)
from enterprise_hr.core.exceptions import PipelineStepError
from enterprise_hr.core.logging import get_logger
from enterprise_hr.infrastructure.database.connection import DatabaseManager, get_db_manager
from enterprise_hr.infrastructure.database.migrations import MigrationManager
from enterprise_hr.infrastructure.storage.file_handler import FileHandler, get_file_handler
from enterprise_hr.pipelines.loaders import SqlBulkLoader

logger = get_logger("PipelineOrchestrator")


class PipelineOrchestrator:
    """Master orchestrator for the Enterprise HR Analytics data platform."""

    def __init__(
        self,
        db_manager: Optional[DatabaseManager] = None,
        file_handler: Optional[FileHandler] = None,
    ):
        self.db = db_manager or get_db_manager()
        self.files = file_handler or get_file_handler()
        self.config = get_config()
        self.loader = SqlBulkLoader(self.db)
        self.migrations = MigrationManager(self.db)

    def ensure_audit_table(self) -> None:
        """Creates stg.Pipeline_Execution_Audit table if missing."""
        ddl = """
        IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'stg')
        BEGIN
            EXEC('CREATE SCHEMA stg');
        END;

        IF OBJECT_ID('stg.Pipeline_Execution_Audit', 'U') IS NULL
        BEGIN
            CREATE TABLE stg.Pipeline_Execution_Audit (
                AuditID BIGINT IDENTITY(1,1) PRIMARY KEY,
                PipelineName NVARCHAR(100) NOT NULL,
                StepName NVARCHAR(150) NOT NULL,
                TargetTable NVARCHAR(100) NULL,
                StartTime DATETIME2(7) NOT NULL,
                EndTime DATETIME2(7) NULL,
                DurationSeconds DECIMAL(10,2) NULL,
                RowsProcessed INT NOT NULL DEFAULT (0),
                Status NVARCHAR(50) NOT NULL,
                ErrorMessage NVARCHAR(MAX) NULL
            );
        END;
        """
        try:
            with self.db.engine.connect() as conn:
                conn.execute(text(ddl))
                conn.commit()
        except Exception as e:
            logger.warning("Could not create audit table: %s", e)

    def log_audit(
        self,
        step_name: str,
        target_table: Optional[str],
        start_time: datetime,
        end_time: datetime,
        rows_processed: int,
        status: AuditStatus,
        error_message: Optional[str] = None,
    ) -> None:
        """Records execution telemetry into SQL Server audit table."""
        duration = (end_time - start_time).total_seconds()
        query = """
        INSERT INTO stg.Pipeline_Execution_Audit
            (PipelineName, StepName, TargetTable, StartTime, EndTime, DurationSeconds, RowsProcessed, Status, ErrorMessage)
        VALUES
            (:pipeline, :step, :target, :start, :end, :duration, :rows, :status, :err);
        """
        try:
            with self.db.engine.connect() as conn:
                conn.execute(
                    text(query),
                    {
                        "pipeline": "EnterpriseHR_Galaxy_Pipeline",
                        "step": step_name,
                        "target": target_table,
                        "start": start_time,
                        "end": end_time,
                        "duration": duration,
                        "rows": rows_processed,
                        "status": status.value,
                        "err": error_message,
                    },
                )
                conn.commit()
        except Exception as e:
            logger.debug("Failed to record audit row: %s", e)

    def verify_master_raw_data(self) -> bool:
        """Verifies integrity of the master 7,000 employee text file."""
        master_path = self.config.paths.raw_dir / "employees_data_7000.txt"
        if not master_path.exists():
            logger.error("❌ Master dataset file missing: %s", master_path)
            return False

        with open(master_path, "r", encoding="utf-8") as f:
            content = f.read()
        records = [r for r in content.split("------") if r.strip()]
        logger.info("📄 Master text file verified: %d records found.", len(records))
        return len(records) == self.config.pipeline.expected_employee_count

    def run_galaxy_mart_build(self) -> bool:
        """Invokes dimensional mart generator (pipeline_runner)."""
        logger.info("⚙️  Running dimensional mart generator (pipeline_runner.py)...")
        from scripts.pipeline_runner import run_pipeline
        run_pipeline()
        logger.info("✅ Dimensional mart CSV build complete.")
        return True

    def ingest_mart_tables(self, truncate: bool = True) -> int:
        """Ingests conformed dimensions and fact tables from data/processed/ into mart schema."""
        self.ensure_audit_table()
        total_rows = 0

        # 1. Ingest Dimensions
        logger.info("\n📥 Ingesting Conformed Dimensions...")
        for csv_name in DIMENSION_LOAD_ORDER:
            file_path = self.config.paths.processed_dir / csv_name
            if not file_path.exists():
                logger.warning("Processed dimension file %s not found. Skipping.", csv_name)
                continue

            target_table, pk_col, _ = MART_TABLE_MANIFEST[csv_name]
            start_ts = datetime.utcnow()
            try:
                df = self.files.read_csv(file_path)
                rows = self.loader.load(df, target_table, truncate=truncate, pk_column=pk_col)
                total_rows += rows
                self.log_audit(f"Ingest {csv_name}", target_table, start_ts, datetime.utcnow(), rows, AuditStatus.SUCCESS)
            except Exception as e:
                self.log_audit(f"Ingest {csv_name}", target_table, start_ts, datetime.utcnow(), 0, AuditStatus.FAILED, str(e))
                raise PipelineStepError(f"Ingest {csv_name}", str(e), e)

        # 2. Ingest Fact Tables
        logger.info("\n📥 Ingesting Galaxy Fact Tables...")
        for csv_name in FACT_LOAD_ORDER:
            file_path = self.config.paths.processed_dir / csv_name
            if not file_path.exists():
                logger.warning("Processed fact file %s not found. Skipping.", csv_name)
                continue

            target_table, pk_col, _ = MART_TABLE_MANIFEST[csv_name]
            start_ts = datetime.utcnow()
            try:
                df = self.files.read_csv(file_path)
                rows = self.loader.load(df, target_table, truncate=truncate, pk_column=pk_col)
                total_rows += rows
                self.log_audit(f"Ingest {csv_name}", target_table, start_ts, datetime.utcnow(), rows, AuditStatus.SUCCESS)
            except Exception as e:
                self.log_audit(f"Ingest {csv_name}", target_table, start_ts, datetime.utcnow(), 0, AuditStatus.FAILED, str(e))
                raise PipelineStepError(f"Ingest {csv_name}", str(e), e)

        return total_rows

    def ingest_raw_sources(self) -> None:
        """Ingests raw external sources (IoT Badge logs, FP&A budget, LMS, software house tasks)."""
        logger.info("\n📥 Ingesting External Raw Sources...")
        from scripts.ingestion.ingest_badge_logs import ingest_badge_logs
        from scripts.ingestion.ingest_finance_plan import ingest_finance_data
        from scripts.ingestion.ingest_lms_data import ingest_lms_logs
        from scripts.ingestion.ingest_software_house_data import (
            ingest_client_projects_tasks,
            ingest_currency_rates,
        )

        badge_json = self.config.paths.raw_dir / "api_badge_logs_202605.json"
        if badge_json.exists():
            ingest_badge_logs(str(badge_json), "raw", "Badge_Access_Logs")

        budget_xlsx = self.config.paths.raw_dir / "finance_budget_2026.xlsx"
        if budget_xlsx.exists():
            ingest_finance_data(str(budget_xlsx), "raw", "Finance_Budget_Plan")

        lms_csv = self.config.paths.raw_dir / "lms_certifications.csv"
        if lms_csv.exists():
            ingest_lms_logs(str(lms_csv), "raw", "LMS_Certifications")

        tasks_csv = self.config.paths.raw_dir / "client_projects_tasks.csv"
        if tasks_csv.exists():
            ingest_client_projects_tasks(str(tasks_csv), "raw", "Client_Projects_Tasks")

        currency_csv = self.config.paths.raw_dir / "dim_currency_rates.csv"
        if currency_csv.exists():
            ingest_currency_rates(str(currency_csv), "raw", "Currency_Rates")

    def run_staging_and_mart_transformations(self) -> None:
        """Executes staging SQL procedures and presentations."""
        logger.info("\n⚙️  Running Staging & Dimensional Transformations...")
        from scripts.transformations.run_stg_transformations import run_sql_script
        from scripts.transformations.run_mart_transformations import run_mart_script

        stg_sql = self.config.paths.sql_dir / "transformations" / "00_stg_hr_audit.sql"
        if stg_sql.exists():
            run_sql_script(str(stg_sql))

        mart_sql = self.config.paths.sql_dir / "transformations" / "02_mart_dimensional_model.sql"
        if mart_sql.exists():
            run_mart_script(str(mart_sql))

    def get_inventory_summary(self) -> List[Tuple[str, str, int]]:
        """Queries production table row counts from SQL Server partitions."""
        query = """
        SELECT 
            s.name AS SchemaName,
            t.name AS TableName,
            p.rows AS RowCounts
        FROM sys.tables t
        INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
        INNER JOIN sys.partitions p ON t.object_id = p.object_id
        WHERE p.index_id IN (0, 1)
        ORDER BY s.name, t.name;
        """
        try:
            with self.db.engine.connect() as conn:
                rows = conn.execute(text(query)).fetchall()
                return [(r[0], r[1], r[2]) for r in rows]
        except Exception as e:
            logger.warning("Could not fetch inventory summary: %s", e)
            return []
