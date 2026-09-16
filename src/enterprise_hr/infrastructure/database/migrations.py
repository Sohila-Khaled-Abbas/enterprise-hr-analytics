"""
Database Schema Migration Manager.
Executes declarative SQL DDL files idempotently and maintains a migration audit history.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Tuple, Optional
from sqlalchemy import text, Connection

from enterprise_hr.core.config import get_config
from enterprise_hr.core.exceptions import MigrationError
from enterprise_hr.core.logging import get_logger
from enterprise_hr.infrastructure.database.connection import DatabaseManager, get_db_manager

logger = get_logger("MigrationManager")


class MigrationManager:
    """Manages idempotent DDL executions and tracks migration state in SQL Server."""

    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db = db_manager or get_db_manager()
        self.config = get_config()
        self.ddl_dir = self.config.paths.sql_dir / "ddl"

    def ensure_migration_table(self, conn: Connection) -> None:
        """Creates the dbo._schema_migrations tracking table if it does not exist."""
        create_table_sql = """
        IF OBJECT_ID('dbo._schema_migrations', 'U') IS NULL
        BEGIN
            CREATE TABLE dbo._schema_migrations (
                MigrationID INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
                ScriptName NVARCHAR(255) NOT NULL UNIQUE,
                AppliedAt DATETIME2(7) NOT NULL DEFAULT (SYSUTCDATETIME()),
                BatchCount INT NOT NULL DEFAULT (0),
                Status NVARCHAR(50) NOT NULL DEFAULT ('SUCCESS')
            );
        END;
        """
        conn.execute(text(create_table_sql))

    def get_applied_migrations(self, conn: Connection) -> set[str]:
        """Returns the set of script names that have already succeeded."""
        try:
            res = conn.execute(text("SELECT ScriptName FROM dbo._schema_migrations WHERE Status = 'SUCCESS'"))
            return {r[0] for r in res.fetchall()}
        except Exception:
            return set()

    def discover_migrations(self) -> List[Path]:
        """Discovers all .sql files in the sql/ddl directory in alphanumeric order."""
        if not self.ddl_dir.exists():
            logger.warning("DDL directory does not exist: %s", self.ddl_dir)
            return []
        return sorted(list(self.ddl_dir.glob("*.sql")))

    def parse_batches(self, sql_content: str) -> List[str]:
        """Splits T-SQL script into discrete execution batches using 'GO' delimiters."""
        # Clean out USE Database commands if connecting directly to the target DB
        cleaned = re.sub(r"(?i)^\s*USE\s+\[?EnterpriseHR_DWH\]?\s*;\s*$", "", sql_content, flags=re.MULTILINE)
        
        # Split on GO statements that appear on their own line
        raw_batches = re.split(r"(?i)^\s*GO\s*$", cleaned, flags=re.MULTILINE)
        valid_batches = [b.strip() for b in raw_batches if b.strip()]
        return valid_batches

    def apply_migration(self, script_path: Path, force: bool = False) -> bool:
        """
        Applies a single DDL migration script.

        Args:
            script_path: Path to the .sql migration file
            force: If True, re-runs the script even if previously recorded

        Returns:
            True if applied successfully, False if already applied
        """
        script_name = script_path.name
        with self.db.engine.connect() as conn:
            self.ensure_migration_table(conn)
            applied = self.get_applied_migrations(conn)

            if script_name in applied and not force:
                logger.info("⏩ Migration already applied: %s", script_name)
                return False

            logger.info("🚀 Applying DDL Migration: %s", script_name)
            content = script_path.read_text(encoding="utf-8")
            batches = self.parse_batches(content)

            # Execute each batch within a dedicated transaction
            trans = conn.begin()
            try:
                for idx, batch in enumerate(batches, 1):
                    conn.execute(text(batch))
                
                # Record migration success
                conn.execute(
                    text("""
                        MERGE dbo._schema_migrations AS target
                        USING (SELECT :script_name AS ScriptName) AS source
                        ON target.ScriptName = source.ScriptName
                        WHEN MATCHED THEN
                            UPDATE SET AppliedAt = SYSUTCDATETIME(), BatchCount = :batches, Status = 'SUCCESS'
                        WHEN NOT MATCHED THEN
                            INSERT (ScriptName, AppliedAt, BatchCount, Status)
                            VALUES (:script_name, SYSUTCDATETIME(), :batches, 'SUCCESS');
                    """),
                    {"script_name": script_name, "batches": len(batches)}
                )
                trans.commit()
                logger.info("   ✅ Successfully applied %s (%d batches)", script_name, len(batches))
                return True
            except Exception as e:
                trans.rollback()
                logger.error("   ❌ Failed to apply %s: %s", script_name, e)
                raise MigrationError(f"Migration failed on script {script_name}: {e}") from e

    def run_all_migrations(self, force: bool = False) -> Tuple[int, int]:
        """
        Discovers and applies all pending DDL migrations.

        Returns:
            (applied_count, skipped_count)
        """
        scripts = self.discover_migrations()
        if not scripts:
            logger.warning("No migration scripts found in %s", self.ddl_dir)
            return (0, 0)

        applied = 0
        skipped = 0
        for s in scripts:
            if self.apply_migration(s, force=force):
                applied += 1
            else:
                skipped += 1

        logger.info("🏁 Migrations complete: %d applied, %d skipped.", applied, skipped)
        return (applied, skipped)
