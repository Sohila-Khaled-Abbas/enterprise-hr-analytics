# Enterprise Infrastructure as Code (IaC) & Containerization Guide

## 1. Overview & Topology

The Enterprise HR Analytics platform supports dual deployment topologies:
1. **Local Containerized Stack**: Fully reproducible local environment powered by **Docker & Docker Compose**, running Microsoft SQL Server 2022 alongside the Python data pipeline worker.
2. **Cloud Enterprise Stack**: Declarative **Terraform (IaC)** modules provisioning Azure SQL Data Warehouse and Azure Data Lake Storage Gen2 (ADLS Gen2) with hierarchical namespaces.

```mermaid
graph TD
    subgraph "Local Development (Docker Compose)"
        DC[docker compose up]
        MSSQL_C[mssql: Microsoft SQL Server 2022<br/>Port 1433 | Volume: mssql_data]
        WORKER_C[pipeline-worker: Python 3.12 + ODBC 18<br/>Auto-Migrate + Ingest + Validate]
        DC --> MSSQL_C
        DC --> WORKER_C
        WORKER_C -.->|healthcheck wait| MSSQL_C
    end

    subgraph "Cloud Production (Terraform IaC)"
        TF[terraform apply]
        RG[Resource Group: rg-enterprise-hr-analytics-prod]
        SQL_SVR[Azure SQL Server: sql-enterprise-hr-prod]
        SQL_DB[Azure SQL DWH: EnterpriseHR_DWH]
        ADLS[ADLS Gen2 Storage Account<br/>Containers: raw / processed]
        
        TF --> RG
        RG --> SQL_SVR
        SQL_SVR --> SQL_DB
        RG --> ADLS
    end
```

---

## 2. Containerized Deployment (Docker & Docker Compose)

### 2.1 Multi-Stage Production Dockerfile (`Dockerfile`)
- **Base Image**: `python:3.12-slim-bookworm`
- **Database Driver**: Official Microsoft SQL Server ODBC Driver 18 (`msodbcsql18`) installed via Microsoft package repositories.
- **Security Compliance**: Non-root execution using dedicated unprivileged `appuser` (UID 1000).
- **Environment Isolation**: `PYTHONPATH=/app/src`, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUNBUFFERED=1`.

### 2.2 Docker Compose Stack (`docker-compose.yml`)
The stack defines two tightly coupled services:
- **`mssql`**: SQL Server 2022 Developer edition container with an integrated healthcheck running `sqlcmd` every 10 seconds.
- **`pipeline-worker`**: Application container configured with `depends_on: mssql: condition: service_healthy`. Once SQL Server is ready, the worker automatically runs migrations (`migrate`), builds the pipeline (`run`), and outputs the warehouse summary (`summary`).

### 2.3 Quick Start Commands
```bash
# 1. Build and run the entire platform locally
docker compose up --build

# 2. Run only the SQL Server container
docker compose up -d mssql

# 3. Trigger pipeline manually inside container
docker compose run --rm pipeline-worker python -m enterprise_hr.cli run

# 4. View table inventory
docker compose run --rm pipeline-worker python -m enterprise_hr.cli summary

# 5. Teardown stack
docker compose down -v
```

---

## 3. Database Migrations as Code (`MigrationManager`)

The platform implements automated, version-controlled database schema migrations:
- **Migration Discovery**: Automatically discovers DDL scripts in `sql/ddl/` in alphanumeric sequence:
  1. `00_create_database_and_schemas.sql` (Creates database and `raw`, `stg`, `mart` schemas)
  2. `01_dimensions.sql` (Creates conformed dimension tables)
  3. `02_facts.sql` (Creates core fact tables)
  4. `03_staging_tables.sql` (Creates staging tables)
  5. `04_software_house_enrichment.sql` (Creates client projects and currency rate tables)
- **Tracking Table (`dbo._schema_migrations`)**: Records every executed migration script with timestamp and status.
- **Idempotency**: Previously applied scripts are skipped unless `--force` is specified.
- **T-SQL Batch Parser**: Intelligently splits SQL scripts by `GO` boundaries and executes each batch in isolated transactions.

### Running Migrations via CLI
```bash
# Apply pending migrations
python -m enterprise_hr.cli migrate

# Force re-execution of all migrations
python -m enterprise_hr.cli migrate --force
```

---

## 4. Cloud Infrastructure as Code (Terraform)

The `terraform/` directory contains modular HCL code to provision production enterprise infrastructure on Microsoft Azure.

### 4.1 Module Architecture
```
terraform/
├── main.tf                    # Root composition & provider configuration
├── variables.tf               # Environment variables, locations, SKUs
├── outputs.tf                 # Connection strings & storage endpoints
├── terraform.tfvars.example   # Sample production settings
└── modules/
    ├── database/              # Azure SQL Server, firewall rules, and DWH database
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    └── storage/               # ADLS Gen2 storage account & raw/processed filesystems
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

### 4.2 Provisioning Workflow
```bash
# 1. Navigate to terraform directory
cd terraform

# 2. Copy example variables and configure
cp terraform.tfvars.example terraform.tfvars

# 3. Initialize Terraform plugins
terraform init

# 4. Plan deployment
terraform plan -out=tfplan

# 5. Apply infrastructure
terraform apply tfplan

# 6. View outputs (ODBC connection string, storage URLs)
terraform output
```

---

## 5. Automated CI/CD Pipeline (`.github/workflows/ci.yml`)

Every commit and pull request triggers four automated validation stages:
1. **Software Engineering Core & Data Contracts**: Executes 29 automated Pytest unit and integration tests across data quality, referential integrity, and domain contracts.
2. **Power BI Immutability**: Ensures binary `.pbix` models remain intact without unauthorized alterations.
3. **Docker Build Verification**: Validates `Dockerfile` compilation and multi-stage image generation.
4. **Terraform Validation**: Enforces formatting standards (`terraform fmt -check`) and validates HCL syntax (`terraform validate`).
