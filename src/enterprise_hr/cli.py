"""
Enterprise HR Analytics Unified CLI.
Provides developer and production commands for migrations, pipelines, healthchecks, and validations.
"""

import argparse
import sys
import time
from typing import Optional

from enterprise_hr.core.config import get_config
from enterprise_hr.core.logging import get_logger
from enterprise_hr.infrastructure.database.connection import get_db_manager
from enterprise_hr.infrastructure.database.migrations import MigrationManager
from enterprise_hr.pipelines.orchestrator import PipelineOrchestrator

logger = get_logger("CLI")


def cmd_healthcheck(args: argparse.Namespace) -> int:
    """Executes platform connectivity and asset healthchecks."""
    logger.info("🩺 Running Platform Health Check...")
    cfg = get_config()
    db = get_db_manager()

    # 1. Database check
    if db.is_healthy():
        logger.info("   ✅ Database connection healthy (Server: %s, DB: %s)", cfg.database.server, cfg.database.database)
    else:
        logger.error("   ❌ Database connection failed!")
        return 1

    # 2. Master raw data check
    master_txt = cfg.paths.raw_dir / "employees_data_7000.txt"
    if master_txt.exists():
        logger.info("   ✅ Master employee text file found: %s", master_txt.name)
    else:
        logger.error("   ❌ Master employee text file missing!")
        return 1

    logger.info("🎉 All systems operational!")
    return 0


def cmd_migrate(args: argparse.Namespace) -> int:
    """Executes database schema migrations."""
    logger.info("🚀 Running Database Schema Migrations...")
    migrator = MigrationManager()
    applied, skipped = migrator.run_all_migrations(force=args.force)
    logger.info("✅ Migration finished: %d applied, %d skipped.", applied, skipped)
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    """Executes the master end-to-end data pipeline."""
    start_time = time.time()
    logger.info("🚀 Starting Master Enterprise HR Pipeline...")
    orchestrator = PipelineOrchestrator()

    # Step 1: Raw verification
    if not orchestrator.verify_master_raw_data():
        logger.error("Raw master verification failed.")
        return 1

    # Step 2: Build Galaxy Dimensional CSVs
    orchestrator.run_galaxy_mart_build()

    # Step 3: Ingest mart and raw tables
    if not args.skip_ingest:
        orchestrator.ingest_mart_tables(truncate=True)
        orchestrator.ingest_raw_sources()

        # Step 4: Transformations
        if not args.skip_transform:
            orchestrator.run_staging_and_mart_transformations()

    # Step 5: Summary
    cmd_summary(args)

    elapsed = time.time() - start_time
    logger.info("🎉 Pipeline completed successfully in %.2f seconds!", elapsed)
    return 0


def cmd_summary(args: argparse.Namespace) -> int:
    """Prints production table row count inventory."""
    orchestrator = PipelineOrchestrator()
    inventory = orchestrator.get_inventory_summary()

    logger.info("═" * 70)
    logger.info("📊 PRODUCTION WAREHOUSE INVENTORY SUMMARY")
    logger.info("═" * 70)
    logger.info(f"{'Schema':<10} │ {'Table Name':<35} │ {'Row Count':>12}")
    logger.info("─" * 10 + "─┼─" + "─" * 35 + "─┼─" + "─" * 12)

    total_rows = 0
    for schema_name, table_name, count in inventory:
        total_rows += count
        logger.info(f"{schema_name:<10} │ {table_name:<35} │ {count:>12,}")

    logger.info("─" * 10 + "─┴─" + "─" * 35 + "─┴─" + "─" * 12)
    logger.info(f"{'TOTAL':<10} │ {'All Production DWH Tables':<35} │ {total_rows:>12,}")
    logger.info("═" * 70)
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Enterprise HR Analytics & Software House Data System CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Healthcheck
    sub_health = subparsers.add_parser("healthcheck", help="Verify DB connection and raw assets")
    sub_health.set_defaults(func=cmd_healthcheck)

    # Migrations
    sub_migrate = subparsers.add_parser("migrate", help="Run database schema migrations")
    sub_migrate.add_argument("--force", action="store_true", help="Force re-run of existing migrations")
    sub_migrate.set_defaults(func=cmd_migrate)

    # Run pipeline
    sub_run = subparsers.add_parser("run", help="Run end-to-end data pipeline")
    sub_run.add_argument("--skip-ingest", action="store_true", help="Skip database ingestion")
    sub_run.add_argument("--skip-transform", action="store_true", help="Skip SQL transformations")
    sub_run.set_defaults(func=cmd_run)

    # Summary
    sub_summary = subparsers.add_parser("summary", help="Print production warehouse table inventory")
    sub_summary.set_defaults(func=cmd_summary)

    args = parser.parse_args()
    exit_code = args.func(args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
