# Enterprise Pipeline Operations & Deployment Runbook

This runbook provides end-to-end operational procedures, deployment instructions, environment configuration guidelines, and troubleshooting protocols for the **Enterprise Human Capital & Operational Efficiency Diagnostics** platform.

---

## 1. System Requirements & Prerequisites

### 1.1 Software Requirements
* **Python Runtime**: Python 3.10 to 3.14 (x64) with `pip` and virtual environment support.
* **Database Engine**: Microsoft SQL Server 2017+ (Default instance `MSSQLSERVER` on port 1433 or named instance `SQLEXPRESS`).
* **Database Driver**: `ODBC Driver 17 for SQL Server` or `ODBC Driver 18 for SQL Server`.
* **Business Intelligence**: Power BI Desktop (supporting `.pbip` and TMDL enhanced dataset format).
* **Operating System**: Windows 10/11 or Windows Server (utilizing Windows Integrated Authentication).

### 1.2 Environment Configuration (`.env`)
Create a `.env` file at the root of the project:
```ini
DB_DRIVER={ODBC Driver 17 for SQL Server}
DB_SERVER=localhost
DB_DATABASE=EnterpriseHR_DWH
DB_USER=
DB_PASS=
```
*(Leave `DB_USER` and `DB_PASS` empty to use secure Windows Authentication).*

---

## 2. Master Dataset Grounding

All data across the entire pipeline is grounded on:
```
data/raw/employees_data_7000.txt
```
This file contains the authoritative records of **exactly 7,000 employees** with authentic Arabic names, roles, departments, branches, salaries, and employment attributes. **Synthetic mock drift is strictly prohibited.**

---

## 3. End-to-End Orchestration (One-Command Execution)

The entire platform—from raw dataset verification, dimensional mart generation, SQL Server ingestion, SCD2 audit staging, to automated test validation—can be executed via the master orchestrator:

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
│ STEP 3: Ingest Data into SQL Server Data Warehouse (EnterpriseHR_DWH)  │
│         -> Ingests raw, staging, and mart tables (idempotent reload)   │
├────────────────────────────────────────────────────────────────────────┤
│ STEP 4: Execute Staging SCD2 Audit Transformation (00_stg_hr_audit.sql)│
│         -> Deduplicates 12,516 -> 12,392 rows, computes LEAD() validity│
├────────────────────────────────────────────────────────────────────────┤
│ STEP 5: Run Automated Data Quality & Integrity Suite (pytest -v)       │
│         -> 14/14 automated test assertions pass                        │
├────────────────────────────────────────────────────────────────────────┤
│ STEP 6: Execute Live Database Inventory Verification                   │
│         -> Prints row count across all 15 production tables            │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Modular Step-by-Step Execution

For fine-grained operational control, individual stages can be executed independently:

### Step 4.1: Database & Schema Initialization (DDL)
Execute the DDL scripts in `sql/ddl/` in numerical order:
```sql
-- In SQL Server Management Studio (SSMS) or sqlcmd:
:r sql/ddl/00_create_database_and_schemas.sql
:r sql/ddl/01_dimensions.sql
:r sql/ddl/02_facts.sql
:r sql/ddl/03_staging_tables.sql
```

### Step 4.2: Ingestion & Dimensional Transformation (Python)
```bash
# Build dimensional CSV marts under data/processed/ and ingest into SQL Server
python scripts/pipeline_runner.py --load-db --truncate
```

### Step 4.3: SCD2 Staging Transformation (T-SQL)
```bash
# Run the optimized SCD2 transformation procedure for HR audit logs
python scripts/transformations/run_stg_transformations.py
```

### Step 4.4: Presentation Mart Materialization (T-SQL & Python)
Materializes the core dimensional models directly from staged and raw records:
1. `mart.Dim_Employee` (Latest master employee records)
2. `mart.Fact_Employee_SCD2` (Historical temporal validity intervals)
3. `mart.Fact_Daily_Badge` (IoT badge logs with +8h missing clock-out imputation)
4. `mart.Fact_LMS_Training` (Deduplicated successful course completions)

```bash
# Execute the dimensional modeling script
python scripts/transformations/run_mart_transformations.py
```

### Step 4.5: Quality Assurance & Automated Testing
```bash
# Run the complete 14-test Pytest verification suite
python -m pytest tests/test_data_quality.py -v
```

---

## 5. Live Production DWH Inventory Baseline

After running the end-to-end pipeline, the data warehouse contains **182,108 rows across 15 tables**:

| Layer | Schema | Table Name | Verified Row Count | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Landing** | `raw` | `HR_Audit_Events` | 12,516 | ✅ Ingested |
| **Landing** | `raw` | `Badge_Access_Logs` | 114,952 | ✅ Ingested |
| **Landing** | `raw` | `Finance_Budget_Plan` | 168 | ✅ Ingested |
| **Landing** | `raw` | `LMS_Certifications` | 7,197 | ✅ Ingested |
| **Staging** | `stg` | `Stg_HR_Audit` | 12,392 | ✅ Transformed |
| **Staging** | `stg` | `Exit_Attrition_Records` | 350 | ✅ Ingested |
| **Mart** | `mart` | `Dim_Employee` | 7,000 | ✅ Loaded |
| **Mart** | `mart` | `Dim_Department` | 6 | ✅ Loaded |
| **Mart** | `mart` | `Dim_Branch` | 14 | ✅ Loaded |
| **Mart** | `mart` | `Dim_Date` | 1,096 | ✅ Loaded |
| **Mart** | `mart` | `Dim_Course` | 10 | ✅ Loaded |
| **Mart** | `mart` | `Fact_WorkforceSnapshot` | 7,000 | ✅ Loaded |
| **Mart** | `mart` | `Fact_DailyAttendance` | 16,000 | ✅ Loaded |
| **Mart** | `mart` | `Fact_DepartmentBudget` | 672 | ✅ Loaded |
| **Mart** | `mart` | `Fact_TrainingCompletions` | 2,735 | ✅ Loaded |
| **TOTAL** | | | **182,108** | **Production Ready** |

---

## 6. Power BI Semantic Model Refresh & Validation

1. **Open Project**: Launch Power BI Desktop and open `powerbi/employess-report.pbip`.
2. **Verify Native Model**: The semantic model automatically binds to the Git-native TMDL definitions in `powerbi/employess-report.SemanticModel/definition/`.
3. **Data Refresh**:
   * Click **Home > Refresh** to pull latest records from `EnterpriseHR_DWH` and `employees_data_7000.txt`.
   * Ensure all 9 tables load without errors:
     * 5 Conformed Dimensions: `Dim_Employee`, `Dim_Department`, `Dim_Branch`, `Dim_Date`, `Dim_Course`
     * 4 Galaxy Facts: `Fact_WorkforceSnapshot`, `Fact_DailyAttendance`, `Fact_DepartmentBudget`, `Fact_TrainingCompletions`
4. **Relationship Verification**:
   * Navigate to the **Model View** (`Ctrl + 3`).
   * Confirm that all 5 dimensions filter the fact tables via single-direction $1 \to *$ relationships.

---

## 7. Troubleshooting & Production Gotchas

### 7.1 SQL Server `RESOURCE_SEMAPHORE` Memory Grant Waits
* **Symptom**: Window function queries (`ROW_NUMBER()`, `LEAD()`) appear to hang indefinitely.
* **Root Cause**: Pandas default `to_sql` creates `VARCHAR(MAX)` columns. Multiple `VARCHAR(MAX)` columns in a window partition cause SQL Server to demand $> 73\text{ MB}$ memory grants. Under constrained physical memory ($< 800\text{ MB}$ free), Windows sets `process_physical_memory_low = 1`, causing the query to wait indefinitely in the `RESOURCE_SEMAPHORE` queue.
* **Resolution**: Ensure strongly-typed column definitions (`VARCHAR(20)`, `VARCHAR(50)`, `DATE`, `DECIMAL(18,2)`) and indexes on partition keys `(EmployeeID, EffectiveDate)` as implemented in `sql/ddl/03_staging_tables.sql` and `sql/transformations/00_stg_hr_audit.sql`.

### 7.2 Idempotent Database Ingestion
* **Symptom**: Successive pipeline runs multiply row counts.
* **Resolution**: In `scripts/pipeline_runner.py` and `scripts/run_end_to_end_pipeline.py`, the ingestion routines pass `truncate=True`. This ensures dimension and fact tables are truncated before loading, preserving exact counts (e.g., exactly 7,000 employees in `Dim_Employee`).

### 7.3 ODBC Driver Compatibility
* If `ODBC Driver 17 for SQL Server` is not installed on your system, install it from Microsoft or specify `ODBC Driver 18 for SQL Server` in your `.env`:
  ```ini
  DB_DRIVER={ODBC Driver 18 for SQL Server}
  ```
  *(If using Driver 18, add `TrustServerCertificate=yes;` if self-signed certificates are used).*
