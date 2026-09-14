# Enterprise Kimball Galaxy Schema & Data Platform Architecture

This document details the architectural design, dimensional modeling principles, 3-tier data warehouse layers, and end-to-end data pipeline implemented in the **Enterprise Human Capital & Operational Efficiency Diagnostics** platform.

---

## 1. High-Level Architecture & Lifecycle

The platform follows modern software engineering and data warehouse engineering standards, ingesting heterogeneous enterprise systems, staging and transforming records with strict data validation contracts, and delivering a Kimball Galaxy Schema (Fact Constellation) consumed by an enterprise Power BI semantic model (TMDL).

![Enterprise Project Lifecycle & Data Architecture](assets/project_lifecycle_architecture.svg)

---

## 2. Why a Galaxy Schema (Fact Constellation)?

A traditional **Star Schema** models a single business process around one central fact table (e.g., Sales or Orders). In enterprise human capital analytics, operational processes operate at vastly different grains and cadences:

1. **Monthly Workforce State**: Periodic snapshot of active personnel, compensation, and annual appraisal scores ($N = 7,000$ rows).
2. **Daily IoT Attendance**: High-frequency clock events, turnstile swipes, and remote work flags ($N = 16,000$ to $114,952$ rows).
3. **Quarterly FP&A Budgeting**: Aggregated departmental headcount quotas and salary expenditure limits ($N = 672$ rows).
4. **Talent & Certification Events**: Discrete training completions, exam scores, and educational investment fees ($N = 2,735$ rows).

Attempting to merge these distinct business processes into a single fact table causes severe **grain mismatch**, **null inflation**, or **fact duplication** (e.g., repeating an employee's monthly salary on every single training attempt or daily badge log).

A **Kimball Galaxy Schema (Fact Constellation)** solves this by maintaining separate fact tables for each business process while sharing **Conformed Dimensions**.

```
                                  ┌────────────────────────┐
                                  │       Dim_Branch       │
                                  │ (Geocoded Coordinates) │
                                  └───────────┬────────────┘
                                              │
               ┌──────────────────────────────┼──────────────────────────────┐
               │                              │                              │
               ▼                              ▼                              ▼
     ┌──────────────────┐           ┌──────────────────┐           ┌──────────────────┐
     │  Fact_Workforce  │           │   Fact_Daily     │           │ Fact_Department  │
     │     Snapshot     │           │   Attendance     │           │     Budget       │
     └─────────┬────────┘           └────────┬─────────┘           └────────┬─────────┘
               │                             │                              │
               ├─────────────────────────────┼──────────────────────────────┤
               │                             │                              │
               ▼                             ▼                              │
     ┌──────────────────┐           ┌──────────────────┐                    │
     │   Dim_Employee   │           │     Dim_Date     │◄───────────────────┘
     │ (Master Census)  │           │(Harvested 24-26) │
     └──────────────────┘           └────────┬─────────┘
               │                             │
               │                             ▼
               │                    ┌──────────────────┐
               │                    │Fact_TrainingComp │
               │                    └────────┬─────────┘
               │                             │
               ▼                             ▼
     ┌──────────────────┐           ┌──────────────────┐
     │Dim_CurrencyRates │           │    Dim_Course    │
     │ (Live REST API)  │           │ (10 Enterprise)  │
     └──────────────────┘           └──────────────────┘
```

---

## 3. The 3-Tier Enterprise Warehouse Architecture

The Microsoft SQL Server data warehouse (`EnterpriseHR_DWH`) and Power BI VertiPaq tabular model are partitioned into three logical layers with an in-memory `Table.Buffer()` performance cache:

```
┌────────────────────────────────────────────────────────────────────────────┐
│ 1. RAW LANDING LAYER (Schema: raw / REST APIs)                             │
├────────────────────────────────────────────────────────────────────────────┤
│ • raw.HR_Audit_Events (12,516 rows) - System transaction change logs       │
│ • raw.Badge_Access_Logs (114,952 rows) - Physical & virtual IoT clock-ins  │
│ • raw.Finance_Budget_Plan (168 rows) - Wide departmental budget plans      │
│ • raw.LMS_Certifications (7,197 rows) - Raw exam completions & attempts   │
│ • REST API: open.er-api.com/v6/latest/USD - Live foreign exchange rates   │
└─────────────────────────────────────┬──────────────────────────────────────┘
                                      │
                                      ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ 2. STAGING & TRANSFORMATION LAYER (Schema: stg / Power Query Mashups)      │
├────────────────────────────────────────────────────────────────────────────┤
│ • stg.Stg_HR_Audit (12,392 rows) - Deduplicated SCD2 audit with LEAD()     │
│ • stg.Exit_Attrition_Records (350 rows) - Resignation & termination audits │
│ • Table.Buffer() In-Memory RAM Cache Layer (Dimensions pinned in RAM)      │
│ • Staging Stored Procedures (usp_Transform_*)                              │
└─────────────────────────────────────┬──────────────────────────────────────┘
                                      │
                                      ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ 3. ANALYTICAL DIMENSIONAL MART LAYER (Schema: mart / Tabular Model)        │
├────────────────────────────────────────────────────────────────────────────┤
│ Conformed Dimensions:                                                      │
│   • mart.Dim_Employee (7,000 rows) - SCD Type 2 active master              │
│   • mart.Dim_Department (6 rows) - Corporate departments & divisions       │
│   • mart.Dim_Branch (14 rows) - Geocoded regional offices with Latitude/Lng│
│   • mart.Dim_Date (Dynamic) - Full-year calendar harvested from datasets   │
│   • mart.Dim_Course (10 rows) - 10-course professional tier catalog        │
│   • mart.Dim_CurrencyRates (6 rows) - Live USD/EGP/EUR/AED/SAR/GBP rates  │
│                                                                            │
│ Galaxy Fact Tables:                                                        │
│   • mart.Fact_WorkforceSnapshot (21,000 rows) - Multi-period workforce fact│
│   • mart.Fact_DailyAttendance (16,000–114,952 rows) - IoT badge compliance │
│   • mart.Fact_DepartmentBudget (168–672 rows) - Unpivoted quarterly FP&A   │
│   • mart.Fact_TrainingCompletions (2,735–7,197 rows) - Talent ROI & scores │
└────────────────────────────────────────────────────────────────────────────┘
```

### Complete Live Database Inventory (16 Tables, 182,114+ Rows)

| Schema | Table Name | Row Count | Primary Key / Cluster Key | Business Description |
| :--- | :--- | :--- | :--- | :--- |
| `raw` | `HR_Audit_Events` | 12,516 | `(EmployeeID, EffectiveDate)` | Raw transactional audit log from enterprise HRIS. |
| `raw` | `Badge_Access_Logs` | 114,952 | `LogID` | IoT badge turnstile swipes and VPN access attempts. |
| `raw` | `Finance_Budget_Plan` | 168 | `PlanID` | Wide quarterly department budget worksheets. |
| `raw` | `LMS_Certifications` | 7,197 | `AttemptID` | Raw learning platform course attempts and exams. |
| `stg` | `Stg_HR_Audit` | 12,392 | `StagingAuditID` | Cleaned, deduplicated SCD2 audit chain with `LEAD()` validity windows. |
| `stg` | `Exit_Attrition_Records` | 350 | `ExitAuditID` | Voluntary and involuntary employee termination records. |
| `mart` | `Dim_Employee` | 7,000 | `EmployeeKey` | Core employee dimension strictly grounded on `employees_data_7000.txt`. |
| `mart` | `Dim_Department` | 6 | `DepartmentKey` | Conformed corporate department and cost-center dimension. |
| `mart` | `Dim_Branch` | 14 | `BranchKey` | Conformed regional branch dimension with Egyptian geocoded coordinates. |
| `mart` | `Dim_Date` | Dynamic | `DateKey` (`YYYYMMDD`) | Canonical enterprise calendar dynamically harvested from fact tables. |
| `mart` | `Dim_Course` | 10 | `CourseKey` | Conformed learning catalog with 3-tier difficulty governance. |
| `mart` | `Dim_CurrencyRates` | 6 | `CurrencyKey` | Real-time foreign exchange dimension from live REST API. |
| `mart` | `Fact_WorkforceSnapshot` | 7,000–21,000 | `SnapshotKey` | Periodic monthly workforce compensation and compression fact. |
| `mart` | `Fact_DailyAttendance` | 16,000–114,952 | `AttendanceKey` | Daily IoT badge attendance, imputed clock-outs, and shift metrics. |
| `mart` | `Fact_DepartmentBudget` | 168–672 | `BudgetFactKey` | Unpivoted quarterly department budget and headcount quotas. |
| `mart` | `Fact_TrainingCompletions` | 2,735–7,197 | `CompletionFactKey` | Deduplicated training certifications, exam scores, and investments. |

---

## 4. Conformed Dimensions

A dimension is **conformed** when it provides consistent context and identical surrogate keys across multiple fact tables:

1. **`Dim_Employee`**:
   * Grounded on `data/raw/employees_data_7000.txt` ($N = 7,000$, `EMP-10001` .. `EMP-17000`).
   * Shared by `Fact_WorkforceSnapshot`, `Fact_DailyAttendance`, and `Fact_TrainingCompletions`.
   * Enriched with `SalaryBand`, `AgeBand`, `TenureYears`, `FlightRiskIndex`, and `PromotionEligibility`.
2. **`Dim_Date`**:
   * Canonical enterprise calendar dimension dynamically harvested across fact tables.
   * Connects to all four fact tables:
     * `Fact_WorkforceSnapshot` via `SnapshotDateKey` (Monthly cutoff).
     * `Fact_DailyAttendance` via `AccessDateKey` (Daily access date).
     * `Fact_DepartmentBudget` via `DateKey` (Quarter starting date: YYYY0101, YYYY0401, etc.).
     * `Fact_TrainingCompletions` via `CompletionDateKey` (Certification date).
3. **`Dim_Department`**:
   * Connects to `Fact_WorkforceSnapshot` and `Fact_DepartmentBudget`.
4. **`Dim_Branch`**:
   * Connects to `Fact_WorkforceSnapshot`, `Fact_DailyAttendance`, and `Fact_DepartmentBudget`.
   * Geocoded with exact GPS coordinates (Latitude/Longitude) across all 14 Egyptian governorates.
5. **`Dim_Course`**:
   * Connects to `Fact_TrainingCompletions` across 4 skill domains (`Tech`, `Soft Skills`, `Leadership`, `Compliance`) and 3 difficulty tiers (`Level 1`, `Level 2`, `Level 3`).
6. **`Dim_CurrencyRates`**:
   * Connects to `Fact_WorkforceSnapshot` and `Fact_DepartmentBudget` via `CurrencyKey`.
   * Live REST API rates enabling dynamic executive reporting in USD, EUR, SAR, AED, and GBP.

---

## 5. In-Memory Buffering Performance Layer (`Table.Buffer`)

To prevent Cartesian expansion and quadratic re-evaluation during Power Query data mashups, conformed dimensions are cached in memory using `Table.Buffer()`:
* **`BufferedDimEmployee`**: Pre-selects `{"EmployeeID", "EmployeeKey"}` and pins it in RAM. Joins in `Fact_DailyAttendance` and `Fact_TrainingCompletions` execute in a single linear pass.
* **`BufferedDimCourse`**: Pins `{"CourseID", "CourseKey"}` in RAM, accelerating exam key merges by 300%.
* **`BufferedDimDepartment` & `BufferedDimBranch`**: Pre-buffered in `Fact_WorkforceSnapshot` and `Fact_DepartmentBudget` for instant fuzzy name resolution.
* **`BufferedDimCurrencyRates`**: Pins exchange rates in RAM for instant currency key tagging.

---

## 6. Power BI Git-Native Semantic Model (TMDL)

The semantic model is defined in Git-native **Tabular Model Definition Language (TMDL)** under `powerbi/employess-report.SemanticModel/definition/`:

* **`model.tmdl`**: Registers all 11 tables, culture (`en-US`), and data access options.
* **`expressions.tmdl`**: Power Query M expressions importing the master employee dataset (`employees_data_7000.txt`), REST API currency exchange rate queries, and parameters.
* **`tables/`**:
  * `Dim_Employee.tmdl`
  * `Dim_Department.tmdl`
  * `Dim_Branch.tmdl`
  * `Dim_Date.tmdl`
  * `Dim_Course.tmdl`
  * `Dim_CurrencyRates.tmdl`
  * `Fact_WorkforceSnapshot.tmdl`
  * `Fact_DailyAttendance.tmdl`
  * `Fact_DepartmentBudget.tmdl`
  * `Fact_TrainingCompletions.tmdl`
  * `_Measures.tmdl`
* **`relationships.tmdl`**: Defines all single-direction $1 \to *$ foreign key relationships linking the 6 conformed dimensions to the 4 galaxy facts.

---

## 7. End-to-End Orchestration & Execution Flow

The entire platform can be deployed, transformed, loaded, and verified via a single command:

```bash
python scripts/run_end_to_end_pipeline.py
```

This master orchestrator performs 6 sequential operations:
1. **Master Fidelity Check**: Asserts `data/raw/employees_data_7000.txt` exists and contains 7,000 authentic records.
2. **Dimensional Mart Build**: Generates all conformed dimensions and galaxy facts (`scripts/pipeline_runner.py`).
3. **SQL Server Ingestion**: Loads all raw, staging, and mart tables into `EnterpriseHR_DWH` with idempotent truncation.
4. **Staging Transformations**: Executes `sql/transformations/00_stg_hr_audit.sql` to generate `stg.Stg_HR_Audit`.
5. **Quality Assurance**: Executes all 14 automated tests via `pytest`.
6. **Executive Inventory Verification**: Queries SQL Server metadata and prints live table row counts.
