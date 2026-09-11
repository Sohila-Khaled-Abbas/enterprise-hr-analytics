<div align="center">

# Enterprise Human Capital & Operational Efficiency Diagnostics
### Enterprise Data Warehouse · Kimball Galaxy Schema · Microsoft SQL Server (T-SQL) · Power BI PBIP / TMDL

[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.14-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Database Engine](https://img.shields.io/badge/Database-Microsoft%20SQL%20Server%20(T--SQL)-CC292B?style=for-the-badge&logo=microsoftsqlserver&logoColor=white)](https://www.microsoft.com/sql-server)
[![Architecture](https://img.shields.io/badge/Architecture-Kimball%20Galaxy%20Schema-8B5CF6?style=for-the-badge)](docs/architecture.md)
[![Power BI PBIP](https://img.shields.io/badge/Power%20BI-PBIP%20%2F%20TMDL%20Dev%20Mode-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](powerbi/employess-report.pbip)
[![Data Quality Tests](https://img.shields.io/badge/Data%20Quality-11%2F11%20Passed%20(100%25)-10B981?style=for-the-badge&logo=pytest&logoColor=white)](tests/test_data_quality.py)
[![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)](LICENSE)

<br/>

<p align="center">
  <b>A production-grade, enterprise data engineering &amp; analytics platform transforming 5 heterogeneous HR and operational source feeds into a high-performance Kimball Galaxy Schema (Fact Constellation) for executive decision-making.</b>
</p>

</div>

---

## 🏛️ Enterprise System Architecture

The platform bridges the gap between transactional workforce records and executive strategic decision-making, resolving real-world data engineering friction across **Core HR, IoT Physical Turnstiles, Transactional Exit Audits, Messy Financial Workbooks, and LMS Learning APIs**.

<div align="center">
  <a href="docs/assets/enterprise_galaxy_architecture.svg">
    <img src="docs/assets/enterprise_galaxy_architecture.png" alt="Enterprise Galaxy Schema Architecture" width="100%"/>
  </a>
  <p><i>Figure 1: High-level System Architecture &amp; Kimball Galaxy Schema (Fact Constellation). <a href="docs/assets/enterprise_galaxy_architecture.svg">[View Vector SVG]</a></i></p>
</div>

---

## 📊 Heterogeneous Source Systems & Data Engineering Challenges

```
                    ┌────────────────────────┐
                    │    Core HR System      │
                    │   (Employees Table)    │
                    └───────────┬────────────┘
                                │
       ┌────────────────────────┼────────────────────────┬────────────────────────┐
       ▼                        ▼                        ▼                        ▼
┌──────────────┐         ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│ Daily Badge  │         │  Historical  │         │  LMS & Certs │         │ Finance Plan │
│ Access Logs  │         │  Exits & HR  │         │   Platform   │         │  & Headcount │
│ (JSON / IoT) │         │ (SQL Server) │         │ (REST / CSV) │         │(Messy Excel) │
└──────────────┘         └──────────────┘         └──────────────┘         └──────────────┘
```

| Source System | Grain | Format | Real-World Engineering Challenges Handled |
| :--- | :--- | :--- | :--- |
| **1. Core HR System** | 1 row / employee | Flat File / Relational | Master dataset with 7,000 employees mapped from 14 localized Arabic attributes (`الاسم`, `الرقم التعريفي`, `السن`, `الراتب الأساسي`, `نوع العقد`, etc.). |
| **2. Daily Badge & Remote Logs** | 1 row / employee / workday | Cloud Blob (JSON / Parquet) | **Missing Clock-Outs**: Night shifts and forgotten sign-outs produce negative or 24h+ durations requiring heuristic median imputation.<br/>**Ghost Workers**: Active payroll records showing 0 access events over 60+ consecutive days.<br/>**Contract Violations**: Employees contracted under `دوام كامل (حضوري)` logging >60% remote days. |
| **3. HR Attrition & Exit Audit** | 1 row / separated employee | Microsoft SQL Server (T-SQL) | **Temporal Misalignment**: Resignation notice submitted weeks before `ExitDate`.<br/>**Survivorship Bias**: Active tables only show survivors; historical turnover requires joining past headcount snapshots against termination dates.<br/>**SCD Type 2**: Tracking salary and branch *at the time of exit*. |
| **4. FP&A Budget & Headcount** | Quarterly / Dept / Branch | Network Shared Excel (`.xlsx`) | **Grain Mismatch**: Fact-to-fact comparison (monthly individual payroll vs. quarterly branch budget).<br/>**Structural Pivoting**: Quarters stored horizontally (`Q1_Budget`, `Q2_Budget`), requiring dynamic unpivoting.<br/>**Branch Inconsistencies**: Typographical variations (`القاهرة - المعادي` vs `فرع المعادي`) resolved via fuzzy normalization. |
| **5. LMS Platform & Certifications** | 1 row / completion attempt | REST API / CSV | **Many-to-Many Relationships**: Employees completing multiple certifications; direct links duplicate payroll totals without conformed dimensional modeling.<br/>**Repeated Attempts**: Filtering retakes to retain highest/latest scores. |

---

## 🌌 Target Kimball Galaxy Schema (Fact Constellation)

Unlike a simple single-fact Star Schema, this enterprise model implements a **Kimball Galaxy Schema (Fact Constellation)** featuring **5 Conformed Dimensions** shared across **4 Specialized Fact Tables**:

```mermaid
erDiagram
    Dim_Employee ||--o{ Fact_WorkforceSnapshot : "filters (1:*)"
    Dim_Department ||--o{ Fact_WorkforceSnapshot : "filters (1:*)"
    Dim_Branch ||--o{ Fact_WorkforceSnapshot : "filters (1:*)"
    Dim_Date ||--o{ Fact_WorkforceSnapshot : "filters (1:*)"

    Dim_Employee ||--o{ Fact_DailyAttendance : "filters (1:*)"
    Dim_Branch ||--o{ Fact_DailyAttendance : "filters (1:*)"
    Dim_Date ||--o{ Fact_DailyAttendance : "filters (1:*)"

    Dim_Department ||--o{ Fact_DepartmentBudget : "filters (1:*)"
    Dim_Branch ||--o{ Fact_DepartmentBudget : "filters (1:*)"
    Dim_Date ||--o{ Fact_DepartmentBudget : "filters (1:*)"

    Dim_Employee ||--o{ Fact_TrainingCompletions : "filters (1:*)"
    Dim_Course ||--o{ Fact_TrainingCompletions : "filters (1:*)"
    Dim_Date ||--o{ Fact_TrainingCompletions : "filters (1:*)"

    Dim_Employee {
        int EmployeeKey PK
        string EmployeeID NK
        string FullName
        string JobRole
        decimal BaseSalary
        string ContractType
        date EffectiveDate
        date ExpiryDate
        bit IsCurrent
    }

    Dim_Department {
        int DepartmentKey PK
        string DepartmentID UQ
        string DepartmentName
        string Division
    }

    Dim_Branch {
        int BranchKey PK
        string BranchID UQ
        string BranchName
        string Region
        string City
    }

    Dim_Date {
        int DateKey PK
        date FullDate UQ
        int CalendarQuarter
        int FiscalYear
        bit IsWorkingDay
    }

    Dim_Course {
        int CourseKey PK
        string CourseID UQ
        string CourseName
        string SkillDomain
    }

    Fact_WorkforceSnapshot {
        bigint SnapshotKey PK
        int SnapshotDateKey FK
        int EmployeeKey FK
        int DepartmentKey FK
        int BranchKey FK
        decimal BaseSalary
        decimal AnnualPerformanceRating
        decimal SalaryPercentileInRole
        bit IsSalaryCompressed
    }

    Fact_DailyAttendance {
        bigint AttendanceKey PK
        int AccessDateKey FK
        int EmployeeKey FK
        int BranchKey FK
        time CheckInTime
        time CheckOutTime
        decimal DurationHours
        bit IsContractViolation
        bit IsImputedClockOut
    }

    Fact_DepartmentBudget {
        int BudgetKey PK
        int DateKey FK
        int DepartmentKey FK
        int BranchKey FK
        int BudgetedHeadcount
        decimal AllocatedSalaryBudget_EGP
        decimal OvertimeAllowance_EGP
    }

    Fact_TrainingCompletions {
        bigint CompletionKey PK
        int CompletionDateKey FK
        int EmployeeKey FK
        int CourseKey FK
        int AttemptNumber
        decimal Score
        bit IsPassed
        decimal CertificationCost_EGP
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
├── scripts/                              # Data Engineering Pipelines
│   ├── ingestion/
│   │   └── generate_enterprise_mock_data.py # 5-system enterprise data generator
│   ├── utils/
│   │   └── data_cleaners.py              # Heuristic cleaners & unpivot utilities
│   └── pipeline_runner.py                # End-to-end data processing orchestrator
├── sql/                                  # Microsoft SQL Server (T-SQL) Layer
│   ├── ddl/                              # Schemas, dimensions, facts, staging DDL
│   ├── transformations/                  # SCD-2, imputation, unpivot procedures & views
│   └── run_all_migrations.sql            # Master database setup script
├── tests/                                # Automated Quality Assurance
│   └── test_data_quality.py              # 11 Pytest dimensional contract tests
├── .gitignore                            # Standard Python & Power BI ignore rules
├── requirements.txt                      # Project dependencies (pandas, openpyxl, pytest)
└── README.md                             # Project overview & documentation index
```

---

## 🚀 Getting Started

### 1. Environment Setup
```powershell
# Clone the repository
git clone https://github.com/your-org/enterprise-hr-analytics.git
cd enterprise-hr-analytics

# Activate Python Virtual Environment
.\venv\Scripts\Activate.ps1

# Install Dependencies
pip install -r requirements.txt
```

### 2. Generate Enterprise Source Datasets
Generate realistic test data for all 5 systems (7,000 Core employees, IoT access logs, exit audits, messy Excel budget, LMS attempts):
```powershell
python scripts/ingestion/generate_enterprise_mock_data.py
```

### 3. Run Galaxy Schema Transformation Pipeline
Transform raw data into the conformed dimensional model in `data/processed/`:
```powershell
python scripts/pipeline_runner.py
```

### 4. Execute Automated Data Quality Tests
Verify primary key uniqueness, foreign key referential integrity, and metric range constraints:
```powershell
pytest -v tests/test_data_quality.py
```

### 5. Deploy SQL Server Migrations
Connect to your Microsoft SQL Server instance (e.g. via SSMS or Azure Data Studio) and run:
```sql
:r sql/ddl/00_create_database_and_schemas.sql
:r sql/ddl/01_dimensions.sql
:r sql/ddl/02_facts.sql
:r sql/ddl/03_staging_tables.sql
```

### 6. Open Power BI Report
Open `powerbi/employess-report.pbip` in Power BI Desktop (with Developer Mode / PBIP enabled). Follow [`docs/powerbi_implementation_guide.md`](docs/powerbi_implementation_guide.md) to wire the transformed Galaxy facts and DAX measures.

---

## 🛡️ Software Engineering & Governance Principles

* **Zero Breaking Changes**: The existing Power BI semantic model files remain 100% intact.
* **Idempotent Data Engineering**: All pipelines and T-SQL transformations are re-runnable without state corruption.
* **Strict Referential Integrity**: Continuous CI/CD assertions ensure zero orphaned keys between facts and dimensions.
* **Git-Native BI Development**: Leverages PBIP and TMDL for enterprise source control and collaborative analytics.

---

## 📜 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
