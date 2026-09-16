# Enterprise Pipeline Operations, CLI & Deployment Runbook

This runbook provides end-to-end operational procedures, deployment instructions, environment configuration guidelines, and troubleshooting protocols for the **Enterprise Human Capital, Software House & Operational Diagnostics Platform**.

---

## 1. System Requirements & Prerequisites

### 1.1 Software Requirements
* **Python Runtime**: Python 3.10 to 3.14 (x64) with `pip` and virtual environment support.
* **Database Engine**: Microsoft SQL Server 2017+ (Local or Azure SQL) or Docker container.
* **Database Driver**: `ODBC Driver 17 for SQL Server` or `ODBC Driver 18 for SQL Server`.
* **Container Engine**: Docker Desktop 20+ with Docker Compose v2.
* **Infrastructure as Code**: Terraform 1.5+ (optional for Azure cloud deployments).
* **Business Intelligence**: Power BI Desktop (supporting `.pbip` and Git-native TMDL format).

### 1.2 Environment Configuration (`.env`)
Create a `.env` file at the root of the project:
```ini
# Database Connection
DB_DRIVER={ODBC Driver 17 for SQL Server}
DB_SERVER=localhost
DB_DATABASE=EnterpriseHR_DWH
DB_USER=
DB_PASS=
DB_TRUST_CERT=true

# Pipeline Settings
LOG_LEVEL=INFO
PIPELINE_CHUNK_SIZE=1000
EXPECTED_EMPLOYEE_COUNT=7000
```
*(Leave `DB_USER` and `DB_PASS` empty to use secure Windows Integrated Authentication).*

---

## 2. Command Line Interface (CLI) Runbook

The platform includes a unified CLI under `enterprise_hr.cli`:

```bash
# Set PYTHONPATH to include src/
export PYTHONPATH=src    # Linux / macOS
$env:PYTHONPATH="src"    # Windows PowerShell

# 1. System Connectivity & Asset Healthcheck
python -m enterprise_hr.cli healthcheck

# 2. Database Schema Migrations (Applies all 5 DDL scripts in order)
python -m enterprise_hr.cli migrate

# 3. Master Pipeline Execution (Extraction, Building, Ingestion, Transformations)
python -m enterprise_hr.cli run

# 4. View Production Warehouse Table Inventory
python -m enterprise_hr.cli summary
```

---

## 3. Containerized Operations (Docker Compose)

To run the complete data platform and database in isolated containers:

```bash
# 1. Start SQL Server 2022 and auto-execute pipeline worker
docker compose up --build

# 2. Run SQL Server in background only
docker compose up -d mssql

# 3. Trigger manual pipeline run in container
docker compose run --rm pipeline-worker python -m enterprise_hr.cli run

# 4. Check warehouse summary in container
docker compose run --rm pipeline-worker python -m enterprise_hr.cli summary

# 5. Stop and clean up containers and volumes
docker compose down -v
```

---

## 4. End-to-End Orchestration Workflow

The master orchestrator can also be invoked via the existing script wrapper:

```bash
python scripts/run_end_to_end_pipeline.py
```

### Orchestration Lifecycle Steps:
```
┌────────────────────────────────────────────────────────────────────────┐
│ STEP 1: Verify Master Raw Text File (employees_data_7000.txt)          │
│         -> Asserts 7,000 records, sequential EMP-10001..17000          │
├────────────────────────────────────────────────────────────────────────┤
│ STEP 2: Build Galaxy Dimensional Mart (pipeline_runner.py)             │
│         -> Cleans raw feeds, parses text, builds conformed dims & facts│
├────────────────────────────────────────────────────────────────────────┤
│ STEP 3: Apply Database Migrations (MigrationManager)                   │
│         -> Applies 00..04 DDL scripts and records in _schema_migrations│
├────────────────────────────────────────────────────────────────────────┤
│ STEP 4: Ingest Data into SQL Server Data Warehouse (EnterpriseHR_DWH)  │
│         -> Ingests raw, staging, and mart tables (idempotent reload)   │
├────────────────────────────────────────────────────────────────────────┤
│ STEP 5: Execute Staging Transformations (00_stg_hr_audit.sql)          │
│         -> Deduplicates 12,516 -> 12,392 rows, computes LEAD() validity│
├────────────────────────────────────────────────────────────────────────┤
│ STEP 6: Execute Presentation Mart Materializations                     │
│         -> Materializes Fact_Daily_Badge, Fact_LMS_Training            │
├────────────────────────────────────────────────────────────────────────┤
│ STEP 7: Automated Quality Assurance Suite (Pytest)                     │
│         -> Runs 29 unit and data quality contract tests                │
├────────────────────────────────────────────────────────────────────────┤
│ STEP 8: Production Table Inventory Verification                        │
│         -> Queries metadata, asserting 322,217 total production rows   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Execution Telemetry & Audit Catalog (`stg.Pipeline_Execution_Audit`)

Every pipeline execution logs detailed audit metrics into Microsoft SQL Server:
```sql
SELECT 
    AuditID,
    PipelineName,
    StepName,
    TargetTable,
    StartTime,
    DurationSeconds,
    RowsProcessed,
    Status,
    ErrorMessage
FROM stg.Pipeline_Execution_Audit
ORDER BY StartTime DESC;
```

---

## 6. Automated Testing Protocols

Execute the complete test suite with verbose output:

```bash
$env:PYTHONPATH="src"
python -m pytest tests/ -v
```

### Verified Test Categories (29 Tests):
* **Conformed Dimension Uniqueness**: Department, Branch, Course, Date, Employee, CurrencyRates.
* **Galaxy Fact Foreign Key Integrity**: Cross-fact referential validation.
* **Metric Boundaries**: Compa-ratio bounds, positive salary rules, overdue delivery flag rules.
* **Data Cleansing Algorithms**: Attendance shift imputation, branch fuzzy matching, LMS score ranking.
* **Software Engineering Architecture**: Config settings, domain entities, atomic file handlers, and migration script parsers.
