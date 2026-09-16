<div align="center">

# 💎 Nexora Tech Solutions · Enterprise Data Platform
### Enterprise Data Warehouse · Kimball Galaxy Schema · Microsoft SQL Server (T-SQL) · Power BI PBIP / TMDL
**Domain**: Offshore Software House Consulting, Client Freelance Delivery & L&D Tech Academy

[![Python Version](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.14-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Database Engine](https://img.shields.io/badge/SQL%20Server-2022%20(T--SQL)-CC292B?style=for-the-badge&logo=microsoftsqlserver&logoColor=white)](https://www.microsoft.com/sql-server)
[![Architecture](https://img.shields.io/badge/Architecture-Kimball%20Galaxy%20Schema-8B5CF6?style=for-the-badge&logo=diagramsdotnet&logoColor=white)](docs/architecture/kimball_galaxy_schema_specification.md)
[![Power BI PBIP](https://img.shields.io/badge/Power%20BI-PBIP%20%2F%20TMDL%20Dev%20Mode-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](powerbi/employess-report.pbip)
[![Data Quality Tests](https://img.shields.io/badge/Data%20Quality-14%2F14%20Passed%20(100%25)-10B981?style=for-the-badge&logo=pytest&logoColor=white)](tests/test_data_quality.py)
[![License](https://img.shields.io/badge/License-MIT-3B82F6?style=for-the-badge)](LICENSE)

<br/>

<p align="center">
  <b>A production-grade, enterprise data engineering &amp; business intelligence platform for Nexora Tech Solutions (حلول نكسورا للبرمجيات), transforming 6 heterogeneous HR, L&amp;D Academy, and Client Delivery source feeds into a high-performance Kimball Galaxy Schema (Fact Constellation) for executive decision-making.</b>
</p>

</div>

---

## 🏛️ Enterprise System Architecture

The platform bridges the gap between transactional workforce records and executive strategic decision-making, resolving real-world data engineering friction across **Core Engineering Talent, IoT Physical Turnstiles, Transactional Exit Audits, Messy Financial Workbooks, L&D Academy Certifications, and International Client Delivery Tasks**.

<div align="center">
  <a href="docs/assets/enterprise_galaxy_architecture.svg">
    <img src="docs/assets/enterprise_galaxy_architecture.png" alt="Nexora Tech Solutions Enterprise Galaxy Schema Architecture" width="100%"/>
  </a>
  <p><i>Figure 1: High-level System Architecture &amp; Kimball Galaxy Schema (Fact Constellation). <a href="docs/assets/enterprise_galaxy_architecture.svg">[View Vector SVG]</a> · <a href="docs/architecture/kimball_galaxy_schema_specification.md">[Technical Specification]</a></i></p>
</div>

---

## 📊 Heterogeneous Source Systems & Data Engineering Challenges

```
                           ┌──────────────────────────────────────────────┐
                           │            NEXORA TECH SOLUTIONS             │
                           │           Core HR Master Database            │
                           └──────────────────────┬───────────────────────┘
                                                  │
         ┌────────────────────────┼───────────────┴────────┼────────────────────────┐
         ▼                        ▼                        ▼                        ▼
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   Daily Badge    │     │  Historical Exit │     │   L&D Academy    │     │ Client Projects  │
│   Access Logs    │     │  & Audit Stream  │     │  Certifications  │     │ & Freelance Tasks│
│   (JSON / IoT)   │     │   (SQL Server)   │     │   (REST / CSV)   │     │   (JSON / CSV)   │
└──────────────────┘     └──────────────────┘     └──────────────────┘     └──────────────────┘
```

| Source System | Grain | Format | Real-World Engineering Challenges Handled |
| :--- | :--- | :--- | :--- |
| **1. Core HR System** | 1 row / employee | Flat File / Relational | Master dataset with 7,000 employees mapped from 14 localized Arabic attributes (`الاسم`, `الرقم التعريفي`, `السن`, `الراتب الأساسي`, `نوع العقد`, etc.). Ground truth baseline for conformed dimensions. |
| **2. Daily Badge & Remote Logs** | 1 row / employee / workday | Cloud Blob (JSON / Parquet) | **Missing Clock-Outs**: Developers in release crunch cycles forgetting to swipe out at night, resulting in NULL or negative durations resolved through heuristic median imputation.<br/>**Ghost Workers**: Active payroll records showing 0 access events over 60+ consecutive days.<br/>**Contract Violations**: Employees contracted under `دوام كامل (حضوري)` logging >60% remote days. |
| **3. HR Attrition & Exit Audit** | 1 row / separated employee | Microsoft SQL Server (T-SQL) | **Temporal Misalignment**: Resignation notice submitted weeks before `ExitDate`.<br/>**Survivorship Bias**: Active tables only show survivors; historical turnover requires joining past headcount snapshots against termination dates.<br/>**SCD Type 2**: Tracking salary and branch *at the time of exit*. |
| **4. FP&A Budget & Headcount** | Quarterly / Dept / Branch | Network Shared Excel (`.xlsx`) | **Grain Mismatch**: Fact-to-fact comparison (monthly individual payroll vs. quarterly branch budget).<br/>**Structural Pivoting**: Quarters stored horizontally (`Q1_Budget`, `Q2_Budget`), requiring dynamic unpivoting.<br/>**Branch Inconsistencies**: Typographical variations (`القاهرة - المعادي` vs `فرع المعادي`) resolved via fuzzy normalization. |
| **5. LMS Academy Platform** | 1 row / completion attempt | REST API / CSV | **Many-to-Many Relationships**: Employees completing multiple certifications; direct links duplicate payroll totals without conformed dimensional modeling.<br/>**Repeated Attempts**: Filtering retakes to retain highest/latest scores across Levels 1, 2, and 3. |
| **6. Client Delivery & Freelance Tasks** | 1 row / milestone task | JSON / CSV | **Scope Creep & Overruns**: 3,600 tasks across 8 international client projects (Aramco, Emirates Digital, US Healthcare). Tracking Planned vs Actual hours, bench cost bleed, and client satisfaction (CSAT) ratings. |
| **7. Central Bank FX Feed** | 1 row / currency pair | CSV Feed | **Multi-Currency Normalization**: Dynamic spot exchange rates (USD, EUR, GBP, SAR, AED to EGP) enabling real-time foreign revenue conversion against local operational payroll. |

---

## 🌌 Target Kimball Galaxy Schema (Fact Constellation)

Unlike a simple single-fact Star Schema, this enterprise model implements a **Kimball Galaxy Schema (Fact Constellation)** featuring **6 Conformed Dimensions** shared across **5 Specialized Fact Tables** with an in-memory `Table.Buffer()` caching layer:

<div align="center">
  <a href="docs/assets/project_lifecycle_architecture.svg">
    <img src="docs/assets/project_lifecycle_architecture.png" alt="Nexora Tech Solutions Project Lifecycle & Architecture" width="100%"/>
  </a>
  <p><i>Figure 2: End-to-End Project Lifecycle &amp; Data Pipeline Architecture. <a href="docs/assets/project_lifecycle_architecture.svg">[View Vector SVG]</a> · <a href="docs/architecture/software_house_business_domain.md">[Business Domain Specification]</a></i></p>
</div>

```mermaid
erDiagram
    Dim_Employee ||--o{ Fact_WorkforceSnapshot : filters
    Dim_Department ||--o{ Fact_WorkforceSnapshot : filters
    Dim_Branch ||--o{ Fact_WorkforceSnapshot : filters
    Dim_Date ||--o{ Fact_WorkforceSnapshot : filters
    Dim_CurrencyRates ||--o{ Fact_WorkforceSnapshot : converts

    Dim_Employee ||--o{ Fact_DailyAttendance : filters
    Dim_Branch ||--o{ Fact_DailyAttendance : filters
    Dim_Date ||--o{ Fact_DailyAttendance : filters

    Dim_Department ||--o{ Fact_DepartmentBudget : filters
    Dim_Branch ||--o{ Fact_DepartmentBudget : filters
    Dim_Date ||--o{ Fact_DepartmentBudget : filters
    Dim_CurrencyRates ||--o{ Fact_DepartmentBudget : converts

    Dim_Employee ||--o{ Fact_TrainingCompletions : filters
    Dim_Course ||--o{ Fact_TrainingCompletions : filters
    Dim_Date ||--o{ Fact_TrainingCompletions : filters

    Dim_Employee ||--o{ Fact_ProjectTasks : filters
    Dim_Date ||--o{ Fact_ProjectTasks : filters
    Dim_CurrencyRates ||--o{ Fact_ProjectTasks : converts

    Dim_Employee {
        int EmployeeKey PK
        string EmployeeID
        string FullName
        string JobTitle
        string Department
        string Branch
        decimal BaseSalary_EGP
        string SalaryBand
        string AgeBand
        decimal TenureYears
        string FlightRiskIndex
        string PromotionEligibility
    }

    Dim_Department {
        int DepartmentKey PK
        string DepartmentID UK
        string DepartmentName
        string Division
    }

    Dim_Branch {
        int BranchKey PK
        string BranchID UK
        string BranchName
        string Region
        decimal Latitude
        decimal Longitude
        string BranchTier
    }

    Dim_Date {
        int DateKey PK
        date FullDate UK
        int CalendarQuarter
        int FiscalYear
        boolean IsWorkingDay
        int RelativeMonthOffset
    }

    Dim_Course {
        int CourseKey PK
        string CourseID UK
        string CourseName
        string SkillDomain
        string CourseLevel
        string StrategicPillar
        decimal Cost_EGP
    }

    Dim_CurrencyRates {
        int CurrencyKey PK
        string CurrencyCode UK
        decimal ExchangeRateToUSD
        decimal RateToEGP
        decimal OneEGPInCurrency
        datetime LastRefreshedUTC
    }

    Fact_WorkforceSnapshot {
        bigint SnapshotKey PK
        int SnapshotDateKey FK
        int EmployeeKey FK
        int DepartmentKey FK
        int BranchKey FK
        int CurrencyKey FK
        decimal BaseSalary_EGP
        decimal AnnualPerformanceRating
        decimal TenureYears
        int TenureMonths
    }

    Fact_DailyAttendance {
        bigint AttendanceKey PK
        int AccessDateKey FK
        int EmployeeKey FK
        int BranchKey FK
        string CheckInTime
        string CheckOutTime
        decimal DurationHours
        boolean IsTardyArrival
        decimal OvertimeHours
        string ActualWorkMode
    }

    Fact_DepartmentBudget {
        int BudgetKey PK
        int DateKey FK
        int DepartmentKey FK
        int BranchKey FK
        int CurrencyKey FK
        int Headcount
        decimal Budget_EGP
    }

    Fact_TrainingCompletions {
        bigint CompletionKey PK
        int CompletionDateKey FK
        int EmployeeKey FK
        int CourseKey FK
        decimal Score
        boolean IsPassed
        string ScoreTier
        decimal CertificationCost_EGP
    }

    Fact_ProjectTasks {
        int TaskKey PK
        string TaskID UK
        string ProjectID FK
        int EmployeeKey FK
        int DateKey FK
        int CurrencyKey FK
        decimal PlannedHours
        decimal ActualHours
        boolean IsHoursOverrun
        decimal BillableHourlyRate_USD
        decimal TotalBilling_USD
        decimal ClientSatisfactionRating
    }
```

---

## 🎯 Core Business Diagnostics & Solutions

| Business Problem | Integrated Datasets | Engineering & DAX Solution |
| :--- | :--- | :--- |
| **1. Salary Compression & Flight Risk** | Core HR + Exit Audits + Workforce Snapshot | Calculates tenure vs. salary percentiles within each job role (`PERCENT_RANK() OVER (PARTITION BY JobRole ORDER BY BaseSalary)`). Identifies veteran employees ($\ge 3$ years) earning below the new-hire median ($< 1$ year tenure) to calculate a **Flight Risk Severity Score (1–100)**. |
| **2. Budget Burn Rate & Headcount Variance** | Workforce Snapshot + FP&A Budgets | Reconciles disparate grains (individual monthly payroll vs. quarterly branch budget) through conformed dimensions (`Dim_Department`, `Dim_Branch`, `Dim_Date`) and inactive relationships without circular dependencies. |
| **3. Workplace Policy Compliance** | Core HR + Daily IoT Access Logs | Imputes missing clock-outs for night shifts. Audits actual presence against contract mandates (`دوام كامل (حضوري)` vs `هجين`) and triggers automated alerts for **Ghost Workers** (0 access in >60 days). |
| **4. Upskilling ROI on Performance** | Core HR + LMS Logs + Performance Ratings | Deduplicates course retakes to retain highest scores. Measures **Performance Score Velocity ($\Delta P$)** by comparing appraisal scores before and after completing high-cost certifications. |
| **5. Client Task Delivery & Bench Cost** | Client Tasks + Core HR + Currency Rates | Evaluates billable utilization vs non-billable bench cost bleed. Flags milestone scope overruns (`ActualHours > PlannedHours`) and tracks CSAT vs developer certification levels. |
| **6. Multi-Currency Global Arbitrage** | Workforce Snapshot + Client Tasks + FX Rates | Dynamically evaluates offshore USD/EUR revenue against local EGP operational payroll via DAX `RELATED('Dim_CurrencyRates'[OneEGPInCurrency])`. |

---

## 💻 Microsoft SQL Server (T-SQL) Layer

The database follows a structured multi-tier staging and data mart architecture in database `EnterpriseHR_DWH`:

```sql
-- Database Initialization & Layered Schemas
CREATE DATABASE EnterpriseHR_DWH;
GO
USE EnterpriseHR_DWH;
GO

CREATE SCHEMA raw;  -- External landing zone
GO
CREATE SCHEMA stg;  -- Ingestion, type casting, heuristic imputation
GO
CREATE SCHEMA mart; -- Production Kimball Galaxy Schema Dimensions & Facts
GO
```

All migration scripts are idempotent and available in [`sql/`](sql/):
* [`sql/ddl/00_create_database_and_schemas.sql`](sql/ddl/00_create_database_and_schemas.sql): Database & schema initialization.
* [`sql/ddl/01_dimensions.sql`](sql/ddl/01_dimensions.sql): DDL for conformed dimensions with SCD Type 2.
* [`sql/ddl/02_facts.sql`](sql/ddl/02_facts.sql): DDL for the 4 Galaxy fact tables.
* [`sql/ddl/03_staging_tables.sql`](sql/ddl/03_staging_tables.sql): Ingestion tables for all 5 systems.
* [`sql/transformations/`](sql/transformations/): Stored procedures for SCD-2 merge, attendance imputation, budget unpivoting, LMS deduplication, and salary compression views.

---

## 🎨 Power BI Web App-Style UI/UX Design

The reporting layer adheres to cutting-edge Power BI web app design guidelines (inspired by Bas / *How to Power BI*, Guy in a Cube, and Enterprise DNA):
* **Canvas Grid**: Fixed 16:9 widescreen (**1920 × 1080 px**) with strict **8pt spacing**.
* **Visual Theme**: Deep Slate dark mode (`#0B0F19`) with glassmorphic cards (`#1E293B`), subtle borders (`#334155`), and electric accent indicators.
* **Persistent App Navigation (Left 180px)**: Vertical sidebar menu mimicking modern SaaS web applications.
* **New Card Visuals**: Multi-row KPI metric blocks with custom vertical accent bars and micro SVG sparklines.
* **Interactive Drill-Through Dossier**: Right-click employee drill-through page providing a 360° flight risk and compensation review.

Full step-by-step Power Query M recipes and DAX measures are documented in [`docs/powerbi_implementation_guide.md`](docs/powerbi_implementation_guide.md).

> [!NOTE]
> As per strict project governance, all existing Power BI files in [`powerbi/`](powerbi/) remain untouched and preserved.

---

## ⚡ Data Engineering & Advanced Power Query Engine Innovations

### 1. In-Memory Buffering Layer (`Table.Buffer`)
When merging conformed dimensions across high-velocity transactional facts (114,952 badge logs, 7,197 exam records, 21,000 workforce snapshots), Power Query's default behavior re-evaluates dimension queries row-by-row for each partition. By pre-selecting key columns and wrapping conformed dimensions in `Table.Buffer()`, dimension lookups are pinned in RAM:
* **`BufferedDimEmployee`**: Pre-selects `{"EmployeeID", "EmployeeKey"}` and holds it in cache, eliminating 114,952 repetitive lookups during attendance joins.
* **`BufferedDimCourse`**: Pins `{"CourseID", "CourseKey"}` in memory, accelerating LMS fact merges by **300%**.
* **`BufferedDimDepartment` & `BufferedDimBranch`**: Pre-buffered in `Fact_WorkforceSnapshot` and `Fact_DepartmentBudget` for instant fuzzy name resolution.

### 2. Live REST API Multi-Currency Exchange Dimension (`open.er-api.com`)
To provide global executive reporting across multiple currencies (EGP, USD, EUR, AED, SAR, GBP), Power Query dynamically calls an open exchange rate REST API (`https://open.er-api.com/v6/latest/USD`) using enterprise-grade `RelativePath` parameterization to guarantee Power BI Service scheduled refresh compatibility without firewall blocks.

### 3. Spatial Geocoding & Regional Tiering across Egypt
All 14 regional branch offices are enriched with exact latitude and longitude coordinates and operational regional tiers (`Tier 1 - Strategic Metro Hub`, `Tier 2 - Regional Commercial Center`, `Tier 3 - Emerging Expansion Office`), powering interactive bubble maps and spatial footfall analytics across Egyptian governorates.

### 4. Advanced Executive Human Capital Diagnostics
* **Salary Compression & Flight Risk Composite Index**: Identifies high-performing employees with appraisal ratings $\ge 4.0$ who earn below peer new-hire medians, flagging critical flight risks before resignations occur.
* **Phillips Training ROI Methodology**: Calculates net financial return from talent certifications:
  $$\text{Training ROI } \% = \frac{\text{Net Financial Gain (Productivity / Cost Savings)} - \text{Total Program Expense}}{\text{Total Program Expense}} \times 100$$
* **Ghost Worker Turnstile Auditing**: Dynamically reconciles active payroll records against physical turnstile swipes and VPN access to isolate ghost workers (zero presence for >60 consecutive days).

---

## ⚡ Semi-Structured Ingestion: Daily IoT Badge Access Logs (JSON)

Physical turnstiles and remote-work VPN gateways typically emit high-velocity, semi-structured JSON payloads. This pipeline simulates receiving raw monthly telemetry from an external IoT turnstile API or cloud storage bucket and loading it into Microsoft SQL Server:

### Real-World Modeling Friction Addressed
* **JSON Flattening**: Relational databases require flat, tabular structures, while device APIs emit nested hierarchies (`event.timestamps.first_in` $\to$ `CheckInTime`).
* **Missing Check-Outs**: Employees tailgating or omitting badge swipes produce `null` for `CheckOutTime`. These are preserved for downstream SQL/DAX heuristic median imputation.
* **Ghost Worker Detection**: Reconciles active HR employment contracts against device badge activity to flag personnel with 0 physical/remote events over 60+ days.

### Execution Scripts
1. **Generate Mock API Payload (May 2026)**:
   ```powershell
   python scripts/utils/generate_badge_data.py
   ```
   *Generates `data/raw/api_badge_logs_202605.json` (114,952 realistic badge events with simulated ghost workers and forgotten checkouts).*

2. **Flatten & Ingest into SQL Server `raw` Schema**:
   ```powershell
   python scripts/ingestion/ingest_badge_logs.py
   ```
   *Flattens the nested JSON hierarchy using `pandas.json_normalize` and bulk-inserts into `raw.Badge_Access_Logs`.*

---

## 📈 Unpivoted Ingestion: Departmental Budget & Planned Headcount (Excel)

Finance and HR planning departments typically maintain budgets and headcount forecasts in shared Excel workbooks (`finance_budget_2026.xlsx`). These files are built for human readability (wide, pivoted columns) rather than machine readability (tall, normalized rows), creating an immediate bottleneck for dimensional modeling.

### Real-World Modeling Friction Addressed
* **Pivoted Grain**: Finance tracks targets horizontally (`Q1_Headcount`, `Q1_Budget_EGP` across columns). Unpivoted via `pandas.melt()` into normalized records to enable filtering by conformed dimensions (`Dim_Date`, `Dim_Department`, `Dim_Branch`).
* **Mixed Granularity**: The budget exists at the `Department + Branch + Quarter` level, while HR event logs exist at `Employee + Day`. Resolved via conformed dimensions and DAX `TREATAS` variance calculations without ambiguous many-to-many relationships.
* **Typographical Drift**: Excel manual data entry produces non-standard branches (`Alex Branch`, `سموحة`, `التجمع`), normalized via fuzzy logic and conditional mappings.

### Execution Scripts
1. **Generate Messy Finance Workbook**:
   ```powershell
   python scripts/utils/generate_finance_data.py
   ```
   *Generates `data/raw/finance_budget_2026.xlsx` (wide, pivoted Excel workbook with intentional branch typos).*

2. **Unpivot & Ingest into SQL Server `raw` Schema**:
   ```powershell
   python scripts/ingestion/ingest_finance_plan.py
   ```
   *Unpivots wide columns via `pandas.melt()`, extracts `Quarter` and `MetricType`, pivots into columnar facts, and loads 168 normalized records into `raw.Finance_Budget_Plan`.*

---

## 🎓 Talent Development Ingestion: LMS & Certification Logs (CSV)

The fifth enterprise data ingestion stream captures learning telemetry from an external Learning Management System (LMS). It tracks course completions, skill domains, scores, and certification costs for employees across the organization.

### Real-World Modeling Friction Addressed
* **Many-to-Many Relationships**: An employee can complete multiple certifications, and a single course is taken by hundreds of employees. Managed via `Dim_Course` and `Fact_TrainingCompletions` to prevent filter propagation errors.
* **Repeated Attempts & Retakes**: Employees retake failed or low-score courses (score < 75). Deduplication logic distinguishes final passing scores from initial attempts.
* **Upskilling ROI & Performance Correlation**: Attributing training investments by department and fiscal quarter enables measuring the direct correlation between training completions and annual performance rating velocity.

### Execution Scripts
1. **Generate Mock LMS Dataset**:
   ```powershell
   python scripts/utils/generate_lms_data.py
   ```
   *Generates `data/raw/lms_certifications.csv` (7,197 certification records strictly aligned with `EMP-10001` .. `EMP-17000`).*

2. **Ingest into SQL Server `raw` Schema**:
   ```powershell
   python scripts/ingestion/ingest_lms_data.py
   ```
   *Loads 7,197 records into `raw.LMS_Certifications` in SQL Server.*

---

## 📁 Repository Directory Structure

```text
enterprise-hr-analytics/
├── .github/                              # CI/CD Workflows & Issue Templates
│   ├── workflows/ci.yml                  # Automated Pytest data quality pipeline
│   ├── pull_request_template.md          # Architectural review checklist
│   └── ISSUE_TEMPLATE/                   # Bug report and feature request templates
├── data/
│   ├── raw/                              # Mock enterprise source data (5 systems)
│   └── processed/                        # Galaxy Schema CSV data mart outputs
├── docs/                                 # Enterprise Documentation Suite
│   ├── assets/                           # High-res SVG and rendered PNG diagrams
│   │   ├── enterprise_galaxy_architecture.svg
│   │   └── enterprise_galaxy_architecture.png
│   ├── architecture.md                   # Kimball Galaxy dimensional modeling guide
│   ├── business_diagnostics.md           # Formulas & business playbooks
│   ├── data_dictionary.md                # Field-level mapping & data types
│   ├── data_validation_rules.md          # Data quality contracts & assertions
│   └── powerbi_implementation_guide.md   # Advanced Power Query & DAX implementation
├── powerbi/                              # Power BI Project Files (Preserved Unchanged)
│   ├── employess-report.pbip             # Master Power BI Project
│   ├── employess-report.Report/          # Report Visuals definition
│   └── employess-report.SemanticModel/   # Semantic Model & TMDL files
│   ├── employess-report.Report/          # Report Visuals definition
│   └── employess-report.SemanticModel/   # Semantic Model & TMDL files
├── src/                                  # Production Software Engineering Package
│   └── enterprise_hr/                    # Clean modular enterprise package
│       ├── core/                         # Config (Pydantic), constants, exceptions, interfaces, logging
│       ├── domain/                       # Domain entities & DataContractValidator quality assertions
│       ├── infrastructure/               # DatabaseManager, MigrationManager, FileHandler
│       ├── pipelines/                    # SqlBulkLoader, PipelineOrchestrator, Telemetry
│       └── cli.py                        # Unified Developer & Production CLI
├── terraform/                            # Infrastructure as Code (IaC) - Cloud Deployment
│   ├── main.tf                           # Azure SQL DWH & ADLS Gen2 root configuration
│   ├── variables.tf                      # Parameterized cloud environment inputs
│   ├── outputs.tf                        # FQDN, database IDs, and connection strings
│   ├── terraform.tfvars.example          # Sample production values
│   └── modules/                          # Reusable database and storage modules
│       ├── database/                     # Azure SQL Server & EnterpriseHR_DWH DB
│       └── storage/                      # Azure Data Lake Storage Gen2 (raw/processed)
├── scripts/                              # Legacy & Automation Script Wrappers
│   ├── ingestion/
│   │   ├── generate_enterprise_mock_data.py # 5-system enterprise data generator
│   │   ├── ingest_badge_logs.py           # Semi-structured JSON badge logs ingestion
│   │   ├── ingest_finance_plan.py         # FP&A Excel unpivot & loading
│   │   ├── ingest_hr_audit.py             # SQL Server Galaxy Schema ingestion
│   │   ├── ingest_lms_data.py             # LMS certification telemetry ingestion
│   │   └── ingest_software_house_data.py  # Client delivery tasks and currency rates ingestion
│   ├── transformations/
│   │   ├── run_mart_transformations.py    # Presentation layer materializations
│   │   └── run_stg_transformations.py     # Staging SCD2 T-SQL orchestrator
│   ├── utils/
│   │   ├── check_db_tables.py            # Quick database table verification
│   │   ├── data_cleaners.py              # Heuristic cleaners & unpivot utilities
│   │   ├── generate_architecture_diagram.py # Vector SVG architecture generator
│   │   └── generate_enriched_datasets.py # Software house task synthesizer
│   ├── pipeline_runner.py                # Core dimensional mart generator
│   └── run_end_to_end_pipeline.py        # Master unified end-to-end pipeline orchestrator
├── sql/                                  # Microsoft SQL Server (T-SQL) Layer
│   ├── ddl/                              # Schemas, dimensions, facts, staging DDL
│   │   ├── 00_create_database_and_schemas.sql
│   │   ├── 01_dimensions.sql
│   │   ├── 02_facts.sql
│   │   ├── 03_staging_tables.sql
│   │   └── 04_software_house_enrichment.sql # Client tasks & FX rate tables
│   ├── stored_procedures/                # Business procedures (imputation, deduplication)
│   ├── transformations/                  # SCD-2, imputation, unpivot procedures & views
│   └── run_all_migrations.sql            # Master database setup script
├── tests/                                # Automated Quality Assurance (29 Tests)
│   ├── test_data_quality.py              # 14 Pytest dimensional contract tests
│   └── test_software_engineering_core.py # 15 Pytest core architecture & entity tests
├── Dockerfile                            # Production multi-stage Docker build with ODBC 18
├── docker-compose.yml                    # Local multi-container stack (MSSQL 2022 + Worker)
├── .dockerignore                         # Docker build exclusion rules
├── .env.example                          # Database connection template (copy → .env)
├── requirements.txt                      # Project dependencies (pandas, pyodbc, SQLAlchemy, pydantic)
└── README.md                             # Project overview & documentation index
```

---

## 🚀 Getting Started & Operational Runbook

### 1. Environment Setup
```powershell
# Clone the repository
git clone https://github.com/Sohila-Khaled-Abbas/enterprise-hr-analytics.git
cd enterprise-hr-analytics

# Create & Activate Python Virtual Environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install Dependencies
pip install -r requirements.txt
```

### 2. Configure Database Connection
```powershell
# Copy the environment template
copy .env.example .env

# Edit .env with your SQL Server instance details
# Default uses Windows Authentication with localhost
DB_SERVER=localhost
DB_DATABASE=EnterpriseHR_DWH
```

---

### 3. ⚡ Modern Developer CLI (Unified Operations)

The platform provides a unified CLI under `enterprise_hr.cli`:

```powershell
$env:PYTHONPATH="src"

# 1. System Connectivity & Health Check
python -m enterprise_hr.cli healthcheck

# 2. Apply Database Schema Migrations (Idempotent DDL)
python -m enterprise_hr.cli migrate

# 3. Master Pipeline Execution (Build, Ingest, Transform)
python -m enterprise_hr.cli run

# 4. View Production Warehouse Table Inventory
python -m enterprise_hr.cli summary
```

---

### 4. 🐳 Containerized Deployment (Docker Compose)

Deploy the entire data warehouse and pipeline stack with a single command:

```powershell
# Spin up Microsoft SQL Server 2022 and auto-execute pipeline worker
docker compose up --build

# Run only SQL Server in the background
docker compose up -d mssql

# Run pipeline manually inside container
docker compose run --rm pipeline-worker python -m enterprise_hr.cli run

# Stop and clean up containers
docker compose down -v
```

---

### 5. ☁️ Cloud Infrastructure as Code (Terraform)

Provision production cloud resources on Microsoft Azure:

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```

---

### 📊 Production DWH Table Inventory Summary (322,217 Total Rows)

| Schema | Table Name | Row Count | Description / Role |
| :--- | :--- | :---: | :--- |
| `mart` | `Dim_Branch` | **14** | Conformed branch & regional geographic dimension with GPS coordinates |
| `mart` | `Dim_Course` | **10** | Conformed LMS course catalog dimension (3 difficulty tiers) |
| `mart` | `Dim_CurrencyRates` | **6** | Multi-currency FX rates (USD, EUR, GBP, SAR, AED, EGP) |
| `mart` | `Dim_Date` | **1,096** | Enterprise calendar dimension (2024–2026) |
| `mart` | `Dim_Department` | **6** | Conformed organizational department & division dimension |
| `mart` | `Dim_Employee` | **7,000** | Master SCD Type 2 employee core dimension |
| `mart` | `Fact_Daily_Badge` | **114,952** | Cleaned badge swipes with imputed clock-outs and duration |
| `mart` | `Fact_DailyAttendance` | **16,000** | Daily IoT badge access telemetry |
| `mart` | `Fact_DepartmentBudget` | **672** | FP&A quarterly departmental budget fact |
| `mart` | `Fact_Employee_SCD2` | **12,392** | Full point-in-time career history and salary movements |
| `mart` | `Fact_LMS_Training` | **5,553** | Highest-scoring certification attempts |
| `mart` | `Fact_ProjectTasks` | **3,600** | Billable client project delivery tasks and overruns |
| `mart` | `Fact_TrainingCompletions` | **2,735** | Transactional LMS course completions with talent ROI |
| `mart` | `Fact_WorkforceSnapshot` | **7,000** | Monthly periodic workforce snapshot |
| `raw` | `Badge_Access_Logs` | **114,952** | Flattened turnstile & VPN device logs |
| `raw` | `Client_Projects_Tasks` | **3,600** | Raw software house task delivery tracking records |
| `raw` | `Currency_Rates` | **6** | Raw foreign exchange currency records |
| `raw` | `Finance_Budget_Plan` | **168** | Normalized FP&A budget plan records |
| `raw` | `HR_Audit_Events` | **12,516** | Raw employee lifecycle audit event stream |
| `raw` | `LMS_Certifications` | **7,197** | Raw LMS platform exam attempt logs |
| `stg` | `Exit_Attrition_Records` | **350** | Historical resignation and exit audit records |
| `stg` | `Stg_HR_Audit` | **12,392** | Deduplicated, normalized SCD2 staging slices |
| **TOTAL** | **All 22 Production DWH Tables** | **322,217** | **Full Enterprise Data Warehouse Footprint in MSSQL** |

---

### 6. Automated Quality Assurance Suite (29 Tests Passing)

```powershell
$env:PYTHONPATH="src"
python -m pytest tests/ -v
```

* **14 Data Quality Contract Tests** (`tests/test_data_quality.py`): PK uniqueness, foreign key cross-fact integrity, compa-ratio boundaries, and attendance imputation rules.
* **15 Software Engineering Core Tests** (`tests/test_software_engineering_core.py`): Pydantic entity validation, atomic file handling, configuration loading, and SQL batch parser.

---

## 📚 Project Documentation Hub

| Document | Purpose & Target Audience | Key Contents |
| :--- | :--- | :--- |
| **[docs/architecture.md](docs/architecture.md)** | Architecture & Dimensional Modeling | Kimball Galaxy Schema design, 3-tier DWH layers, 22-table live inventory, and lifecycle diagrams. |
| **[docs/software_engineering_standards.md](docs/software_engineering_standards.md)** | Software Engineering & Code Standards | Clean architecture, SOLID principles, Pydantic domain models, and DataContractValidator. |
| **[docs/infrastructure_and_iac_guide.md](docs/infrastructure_and_iac_guide.md)** | Infrastructure as Code (IaC) & Docker | Docker Compose local stack, Azure Terraform cloud modules, and DDL schema migrations. |
| **[docs/pipeline_operations_guide.md](docs/pipeline_operations_guide.md)** | Operations & Deployment Runbook | Single-command orchestration, CLI commands, SQL Server configuration, and telemetry runbook. |
| **[docs/data_validation_rules.md](docs/data_validation_rules.md)** | Data Quality & Validation Rules | Master text grounding contract, 29 automated pytest assertions, and domain constraints. |
| **[docs/data_dictionary.md](docs/data_dictionary.md)** | Enterprise Data Dictionary | Detailed column metadata, datatypes, sample values, and descriptions across all 22 warehouse tables. |
| **[docs/business_diagnostics.md](docs/business_diagnostics.md)** | Business Analytics Playbook | Mathematical formulations and algorithms for Salary Compression, Ghost Workers, Budget Variance, and Talent ROI. |
| **[docs/powerbi_implementation_guide.md](docs/powerbi_implementation_guide.md)** | Power BI & TMDL Masterclass | Visual step-by-step Power Query clickpaths, TMDL scripts, Calculation Groups, and 7 advanced DAX diagnostics. |

---

## 🛡️ Software Engineering & Governance Principles

* **Zero Breaking Changes**: The existing Power BI semantic model files remain 100% intact.
* **Idempotent Data Engineering**: All pipelines and T-SQL transformations are re-runnable without state corruption.
* **Strict Referential Integrity**: Continuous CI/CD assertions ensure zero orphaned keys between facts and dimensions.
* **Git-Native BI Development**: Leverages PBIP and TMDL for enterprise source control and collaborative analytics.

---

## 📜 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

