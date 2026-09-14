# Enterprise Data Dictionary & Schema Mapping Specification

This document defines the canonical schema, attribute definitions, data types, and mapping relationships for the **Enterprise Human Capital & Operational Efficiency Diagnostics** data platform.

---

## 1. Source Schema Mapping: Core HRIS (`employees_data_7000.tmdl`)

The transactional core system uses localized Arabic field names. The table below provides the canonical enterprise mapping to the Kimball Dimensional Model:

| Source Arabic Field | Enterprise Canonical Name | Physical Data Type | Business Description | Target Dimensional Table |
| :--- | :--- | :--- | :--- | :--- |
| **`الرقم التعريفي`** | `EmployeeID` | `NVARCHAR(50)` | Natural business identifier (e.g. `EMP-00124`). Unique per person. | `Dim_Employee` (`NaturalKey`) |
| **`الاسم`** | `FullName` | `NVARCHAR(150)` | Full employee name in Arabic. | `Dim_Employee` |
| **`السن`** | `Age` | `INT` | Employee age in completed years. | `Dim_Employee` |
| **`الجنس`** | `Gender` | `NVARCHAR(20)` | Gender classification (`ذكر` / `أنثى`). | `Dim_Employee` |
| **`المسمى الوظيفي`** | `JobRole` | `NVARCHAR(100)` | Standard job title (e.g. `مهندس برمجيات`, `محلل مالي`). | `Dim_Employee` |
| **`القسم`** | `DepartmentName` | `NVARCHAR(100)` | Functional department (e.g. `تقنية المعلومات`). | `Dim_Department` (`DepartmentName`) |
| **`الفرع`** | `BranchName` | `NVARCHAR(100)` | Primary work branch location (e.g. `فرع المعادي`). | `Dim_Branch` (`BranchName`) |
| **`تاريخ التعيين`** | `HireDate` | `DATE` | Official hire/onboarding date. | `Dim_Employee` (`HireDate`) |
| **`الراتب الأساسي`** | `BaseSalary` | `DECIMAL(18,2)` | Monthly base compensation in local currency. | `Dim_Employee`, `Fact_WorkforceSnapshot` |
| **`العملة`** | `Currency` | `NVARCHAR(10)` | Currency ISO code (Standard: `EGP`). | `Dim_Employee` |
| **`نوع العقد`** | `ContractType` | `NVARCHAR(50)` | Employment model (`دوام كامل (حضوري)`, `هجين`, `عن بعد`). | `Dim_Employee` |
| **`تقييم الأداء السنوي`**| `AnnualPerformanceRating`| `DECIMAL(4,2)` | Performance appraisal score on a 1.00 to 5.00 scale. | `Fact_WorkforceSnapshot` |
| **`الحالة الاجتماعية`** | `MaritalStatus` | `NVARCHAR(50)` | Marital status (`أعزب`, `متزوج`, etc.). | `Dim_Employee` |
| **`البريد الإلكتروني`** | `Email` | `NVARCHAR(150)` | Corporate email address. | `Dim_Employee` |

---

## 2. Conformed Dimensions (`mart` Schema)

### 2.1 `Dim_Employee` (Slowly Changing Dimension Type 2)
* **Grain**: One row per employee version.
* **Storage**: `[mart].[Dim_Employee]`

| Column Name | Data Type | Nullable | Key Type | Description |
| :--- | :--- | :---: | :---: | :--- |
| `EmployeeKey` | `INT IDENTITY(1,1)` | No | PK | Surrogate key uniquely identifying an employee record version. |
| `EmployeeID` | `NVARCHAR(50)` | No | Natural Key | Business identifier across HR systems (`الرقم التعريفي`). |
| `FullName` | `NVARCHAR(150)` | No | None | Employee full legal name (`الاسم`). |
| `Age` | `INT` | Yes | None | Current age. |
| `Gender` | `NVARCHAR(20)` | Yes | None | Gender. |
| `JobRole` | `NVARCHAR(100)` | No | None | Standardized job role. |
| `DepartmentKey` | `INT` | No | FK | Reference to `Dim_Department.DepartmentKey`. |
| `BranchKey` | `INT` | No | FK | Reference to `Dim_Branch.BranchKey`. |
| `HireDate` | `DATE` | No | None | Original company hire date. |
| `BaseSalary` | `DECIMAL(18,2)` | No | None | Monthly base salary in EGP at this version. |
| `Currency` | `NVARCHAR(10)` | No | None | Currency code (Default: `EGP`). |
| `ContractType` | `NVARCHAR(50)` | No | None | Work mode contract (`دوام كامل (حضوري)`, `هجين`, `عن بعد`). |
| `MaritalStatus` | `NVARCHAR(50)` | Yes | None | Marital status. |
| `Email` | `NVARCHAR(150)` | Yes | None | Official email. |
| `EffectiveDate` | `DATE` | No | SCD2 | Start date when this employee profile version became active. |
| `ExpiryDate` | `DATE` | No | SCD2 | End date of this version (`9999-12-31` if active). |
| `IsCurrent` | `BIT` | No | SCD2 | `1` if this is the active current record; `0` if historical. |
| `CreatedAt` | `DATETIME2(7)` | No | Audit | System ingestion timestamp. |

### 2.2 `Dim_Department`
* **Grain**: One row per organizational department.
* **Storage**: `[mart].[Dim_Department]`

| Column Name | Data Type | Nullable | Key Type | Description |
| :--- | :--- | :---: | :---: | :--- |
| `DepartmentKey` | `INT IDENTITY(1,1)` | No | PK | Surrogate key for department. |
| `DepartmentID` | `NVARCHAR(50)` | No | UQ | Enterprise cost center / department code (e.g. `DEPT-001`). |
| `DepartmentName` | `NVARCHAR(100)` | No | None | Department name in Arabic (e.g. `الموارد البشرية`). |
| `Division` | `NVARCHAR(100)` | No | None | High-level corporate division. |
| `CostCenterCode` | `NVARCHAR(50)` | Yes | None | ERP GL cost center reference. |

### 2.3 `Dim_Branch`
* **Grain**: One row per geographic office/branch.
* **Storage**: `[mart].[Dim_Branch]`

| Column Name | Data Type | Nullable | Key Type | Description |
| :--- | :--- | :---: | :---: | :--- |
| `BranchKey` | `INT IDENTITY(1,1)` | No | PK | Surrogate key for branch location. |
| `BranchID` | `NVARCHAR(50)` | No | UQ | Unique branch code (e.g. `BR-001`). |
| `BranchName` | `NVARCHAR(100)` | No | None | Formal branch name in Arabic (e.g. `فرع المعادي`). |
| `CanonicalName` | `NVARCHAR(100)` | No | None | Standardized string used for fuzzy reconciliation. |
| `Region` | `NVARCHAR(100)` | No | None | Geographic region (`Greater Cairo`, `Alexandria & North`, `Delta`, etc.). |
| `City` | `NVARCHAR(100)` | No | None | City name (`Cairo`, `Giza`, `Alexandria`, `Asyut`, etc.). |
| `Capacity` | `INT` | No | None | Maximum physical desk capacity. |

### 2.4 `Dim_Course`
* **Grain**: One row per training program/certification.
* **Storage**: `[mart].[Dim_Course]`

| Column Name | Data Type | Nullable | Key Type | Description |
| :--- | :--- | :---: | :---: | :--- |
| `CourseKey` | `INT IDENTITY(1,1)` | No | PK | Surrogate key for course catalog. |
| `CourseID` | `NVARCHAR(50)` | No | UQ | Canonical LMS course code (e.g. `CRS-TECH-01`). |
| `CourseName` | `NVARCHAR(200)` | No | None | Course title. |
| `SkillDomain` | `NVARCHAR(100)` | No | None | Classification domain (`Tech`, `Soft Skills`, `Leadership`, `Compliance`). |
| `TargetCompetency` | `NVARCHAR(150)` | Yes | None | Target capability. |
| `EstimatedHours` | `DECIMAL(6,2)` | No | None | Standard completion duration in hours. |

### 2.5 `Dim_Date`
* **Grain**: One row per calendar day.
* **Storage**: `[mart].[Dim_Date]`

| Column Name | Data Type | Nullable | Key Type | Description |
| :--- | :--- | :---: | :---: | :--- |
| `DateKey` | `INT` | No | PK | Integer smart key formatted as `YYYYMMDD`. |
| `FullDate` | `DATE` | No | UQ | Standard ISO calendar date (`YYYY-MM-DD`). |
| `DayNumberOfWeek` | `TINYINT` | No | None | 1 (Monday) through 7 (Sunday). |
| `DayNameOfWeek` | `NVARCHAR(20)` | No | None | Full name of day (`Sunday`, `Monday`, etc.). |
| `MonthName` | `NVARCHAR(20)` | No | None | Full name of month (`January`, `February`, etc.). |
| `CalendarQuarter` | `TINYINT` | No | None | 1, 2, 3, or 4. |
| `CalendarYear` | `SMALLINT` | No | None | Calendar year (e.g. `2026`). |
| `IsWeekend` | `BIT` | No | None | `1` for Middle East weekend (Friday & Saturday); `0` otherwise. |
| `IsWorkingDay` | `BIT` | No | None | `1` for standard business work days; `0` otherwise. |

---

## 3. Galaxy Fact Tables (`mart` Schema)

### 3.1 `Fact_WorkforceSnapshot`
* **Grain**: One row per active employee per monthly reporting cutoff.
* **Storage**: `[mart].[Fact_WorkforceSnapshot]`

| Column Name | Data Type | Nullable | Key Type | Description |
| :--- | :--- | :---: | :---: | :--- |
| `SnapshotKey` | `BIGINT IDENTITY(1,1)` | No | PK | Surrogate key for snapshot event. |
| `SnapshotDateKey` | `INT` | No | FK | Reference to `Dim_Date.DateKey`. |
| `EmployeeKey` | `INT` | No | FK | Reference to `Dim_Employee.EmployeeKey`. |
| `DepartmentKey` | `INT` | No | FK | Reference to `Dim_Department.DepartmentKey`. |
| `BranchKey` | `INT` | No | FK | Reference to `Dim_Branch.BranchKey`. |
| `BaseSalary` | `DECIMAL(18,2)` | No | Metric | Active base salary in EGP for the period. |
| `AnnualPerformanceRating` | `DECIMAL(4,2)` | Yes | Metric | Latest annual performance appraisal score (1.00–5.00). |
| `TenureMonths` | `INT` | No | Metric | Cumulative tenure in whole months. |
| `TenureYears` | `DECIMAL(5,2)` | No | Metric | Cumulative tenure in decimal years. |
| `SalaryPercentileInRole` | `DECIMAL(6,4)` | Yes | Metric | Percentile rank (0.0000–1.0000) of salary within JobRole. |
| `IsSalaryCompressed` | `BIT` | No | Flag | `1` if tenured (>=3 yrs) earning below new-hire median; `0` otherwise. |
| `EmploymentStatus` | `NVARCHAR(50)` | No | Attribute | `Active`, `OnLeave`, or `Separated`. |

### 3.2 `Fact_DailyAttendance`
* **Grain**: One row per employee per workday access event.
* **Storage**: `[mart].[Fact_DailyAttendance]`

| Column Name | Data Type | Nullable | Key Type | Description |
| :--- | :--- | :---: | :---: | :--- |
| `AttendanceKey` | `BIGINT IDENTITY(1,1)` | No | PK | Surrogate key for attendance event. |
| `AccessDateKey` | `INT` | No | FK | Reference to `Dim_Date.DateKey`. |
| `EmployeeKey` | `INT` | No | FK | Reference to `Dim_Employee.EmployeeKey`. |
| `BranchKey` | `INT` | No | FK | Reference to `Dim_Branch.BranchKey`. |
| `CheckInTime` | `TIME(0)` | Yes | Attribute | First physical or system check-in timestamp. |
| `CheckOutTime` | `TIME(0)` | Yes | Attribute | Final check-out timestamp (cleansed / imputed). |
| `DurationHours` | `DECIMAL(6,2)` | No | Metric | Shift length in decimal hours (night shifts normalized). |
| `DeclaredWorkMode` | `NVARCHAR(50)` | No | Attribute | Mode reported by employee (`On-site`, `Remote`, `Field`). |
| `ActualWorkMode` | `NVARCHAR(50)` | No | Attribute | Verified badge presence (`On-site` vs `Remote`). |
| `IsMissingClockOut`| `BIT` | No | Flag | `1` if physical clock-out was omitted. |
| `IsImputedClockOut`| `BIT` | No | Flag | `1` if clock-out was reconstructed via heuristic median. |
| `IsNightShift` | `BIT` | No | Flag | `1` if shift crossed midnight. |
| `IsContractViolation` | `BIT` | No | Flag | `1` if onsite contract logged remote work or failed quota. |

### 3.3 `Fact_DepartmentBudget`
* **Grain**: One row per Department per Branch per Fiscal Quarter.
* **Storage**: `[mart].[Fact_DepartmentBudget]`

| Column Name | Data Type | Nullable | Key Type | Description |
| :--- | :--- | :---: | :---: | :--- |
| `BudgetKey` | `INT IDENTITY(1,1)` | No | PK | Surrogate key for budget record. |
| `FiscalYear` | `SMALLINT` | No | Attribute | Fiscal year (e.g. `2026`). |
| `FiscalQuarter` | `TINYINT` | No | Attribute | Fiscal quarter (1, 2, 3, or 4). |
| `DateKey` | `INT` | No | FK | Reference to `Dim_Date.DateKey` (First day of quarter). |
| `DepartmentKey` | `INT` | No | FK | Reference to `Dim_Department.DepartmentKey`. |
| `BranchKey` | `INT` | No | FK | Reference to `Dim_Branch.BranchKey`. |
| `BudgetedHeadcount` | `INT` | No | Metric | Target authorized headcount allocation. |
| `AllocatedSalaryBudget_EGP` | `DECIMAL(18,2)` | No | Metric | Approved salary expenditure budget in EGP. |
| `OvertimeAllowance_EGP` | `DECIMAL(18,2)` | No | Metric | Overtime and incentive reserve pool in EGP. |

### 3.4 `Fact_TrainingCompletions`
* **Grain**: One row per certification/course completion attempt.
* **Storage**: `[mart].[Fact_TrainingCompletions]`

| Column Name | Data Type | Nullable | Key Type | Description |
| :--- | :--- | :---: | :---: | :--- |
| `CompletionKey` | `BIGINT IDENTITY(1,1)` | No | PK | Surrogate key for completion attempt. |
| `CompletionDateKey` | `INT` | No | FK | Reference to `Dim_Date.DateKey`. |
| `EmployeeKey` | `INT` | No | FK | Reference to `Dim_Employee.EmployeeKey`. |
| `CourseKey` | `INT` | No | FK | Reference to `Dim_Course.CourseKey`. |
| `AttemptNumber` | `INT` | No | Metric | Sequential attempt number for this employee & course (1, 2, ...). |
| `Score` | `DECIMAL(5,2)` | No | Metric | Examination score percentage (0.00 to 100.00). |
| `IsPassed` | `BIT` | No | Flag | `1` if Score >= 70.0; `0` otherwise. |
| `CertificationCost_EGP` | `DECIMAL(12,2)` | No | Metric | Direct program certification fee in EGP. |
| `IsHighestScoreAttempt` | `BIT` | No | Flag | `1` if this attempt is the top score achieved by the employee. |

---

## 4. Raw Landing Zone Schema: IoT Turnstiles & VPN Gateways

### 4.1 `raw.Badge_Access_Logs` (Semi-Structured JSON Ingestion)
* **Source**: High-velocity simulated IoT API / cloud blob endpoint (`api_badge_logs_YYYYMM.json`).
* **Storage**: `[raw].[Badge_Access_Logs]`
* **Grain**: 1 row per physical turnstile badge event or VPN gateway session.

| Column Name | Physical Data Type | Nullable | Key Type | Business Description |
| :--- | :--- | :---: | :---: | :--- |
| `LogID` | `NVARCHAR(50)` | No | PK / Unique | Event transaction identifier emitted by the device (e.g. `LOG-10482`). |
| `SystemSource` | `NVARCHAR(50)` | No | Metadata | Ingestion origin channel (`TURNSTILE` for physical turnstile, `GATEWAY` for remote VPN). |
| `EmployeeID` | `NVARCHAR(50)` | No | FK | Natural employee identifier (`EMP-10001` .. `EMP-17000`). |
| `AccessDate` | `DATE` / `VARCHAR` | No | Attribute | Calendar date of access event (`YYYY-MM-DD`). |
| `FacilityCode` | `NVARCHAR(50)` | No | Dimension Ref | Physical facility or access point (`HQ-CAIRO`, `TECH-GIZA`, `OPS-ALEX`, `REMOTE-VPN`). |
| `CheckInTime` | `DATETIME2` / `VARCHAR` | No | Timestamp | ISO-8601 UTC timestamp of initial entry or connection (`first_in`). |
| `CheckOutTime` | `DATETIME2` / `VARCHAR` | Yes | Timestamp | ISO-8601 UTC timestamp of departure or disconnect (`last_out`). `NULL` indicates missing clock-out. |

---

### 4.2 `raw.Finance_Budget_Plan` (Unpivoted Excel Planning Ingestion)
* **Source**: Shared finance planning workbook (`finance_budget_2026.xlsx`), unpivoted via Python `pandas.melt()`.
* **Storage**: `[raw].[Finance_Budget_Plan]`
* **Grain**: 1 row per Department + Branch + Quarter + Metric.

| Column Name | Physical Data Type | Nullable | Key Type | Business Description |
| :--- | :--- | :---: | :---: | :--- |
| `Department` | `NVARCHAR(100)` | No | Dimension Ref | Department name (e.g., `تكنولوجيا المعلومات`, `الموارد البشرية`). |
| `CostCenter_Branch` | `NVARCHAR(100)` | No | Dimension Ref | Non-standard branch identifier requiring normalization (`Alex Branch`, `سموحة`, `التجمع`). |
| `Quarter` | `NVARCHAR(10)` | No | Dimension Ref | Fiscal quarter (`Q1`, `Q2`, `Q3`, `Q4`). |
| `Headcount` | `FLOAT` / `INT` | Yes | Metric | Planned target headcount for the specified department and branch in the quarter. |
| `Budget_EGP` | `FLOAT` / `DECIMAL(18,2)` | Yes | Metric | Planned salary expenditure budget in Egyptian Pounds (EGP). |
| `FiscalYear` | `INT` | No | Dimension Ref | Fiscal planning year (`2026`). |

---

### 4.3 `raw.HR_Audit_Events` (Raw Temporal Audit Event Log)
* **Source**: Transactional HRIS audit stream (`hr_audit_events.csv`).
* **Storage**: `[raw].[HR_Audit_Events]`
* **Grain**: 1 row per employee lifecycle event (Hire, Promotion, Transfer, Salary Revision, Termination).

| Column Name | Physical Data Type | Nullable | Key Type | Business Description |
| :--- | :--- | :---: | :---: | :--- |
| `EmployeeID` | `VARCHAR(20)` | No | Natural Key | Natural employee identifier (`EMP-10001` .. `EMP-17000`). |
| `EventType` | `VARCHAR(50)` | No | Attribute | Audit event classification (`HIRE`, `PROMOTION`, `TRANSFER`, `SALARY_UPDATE`, `TERMINATION`). |
| `EffectiveDate` | `DATE` | No | Timestamp | Date when the HR event took operational effect. |
| `PreviousValue` | `NVARCHAR(150)` | Yes | History | Value prior to the event (job title, branch, or old compensation). |
| `NewValue` | `NVARCHAR(150)` | Yes | History | New value applied by the event (job title, branch, or new compensation). |
| `Salary_EGP` | `DECIMAL(18,2)` | Yes | Metric | Compensation at the time of the event. |
| `IsTerminated` | `INT` | Yes | Flag | `1` if employee reached terminal state; `0` otherwise. |

---

### 4.4 `raw.LMS_Certifications` (Raw Training & Certification Telemetry)
* **Source**: Learning Management System completion records (`lms_certifications.csv`).
* **Storage**: `[raw].[LMS_Certifications]`
* **Grain**: 1 row per employee course attempt.

| Column Name | Physical Data Type | Nullable | Key Type | Business Description |
| :--- | :--- | :---: | :---: | :--- |
| `EmployeeID` | `VARCHAR(50)` | No | Natural Key | Employee identifier. |
| `CourseID` | `VARCHAR(50)` | No | Dimension Ref | Course catalog ID (`CRS-101`, `CRS-102`, etc.). |
| `CourseName` | `NVARCHAR(200)` | No | Attribute | Full title of certification program. |
| `SkillDomain` | `NVARCHAR(100)` | No | Attribute | Competency domain (`Tech`, `Leadership`, `Soft Skills`, `Compliance`). |
| `CompletionDate` | `DATE` | No | Timestamp | Date of examination or completion. |
| `Score` | `FLOAT` | No | Metric | Final exam score percentage (0.0 to 100.0). |
| `Status` | `VARCHAR(50)` | No | Attribute | Completion outcome (`Completed`, `In Progress`, `Failed`). |
| `Cost_EGP` | `DECIMAL(18,2)` | No | Metric | Direct program tuition/certification expense. |

---

## 5. Cleansed Staging Layer Schema (`stg` Schema)

### 5.1 `stg.Stg_HR_Audit` (Deduplicated SCD Type 2 Audit Master)
* **Source**: Transformed from `raw.HR_Audit_Events` via `sql/transformations/00_stg_hr_audit.sql`.
* **Storage**: `[stg].[Stg_HR_Audit]`
* **Grain**: 1 row per valid temporal interval per employee.
* **Transformations Applied**:
  1. ROW_NUMBER deduplication over `(EmployeeID, EventType, EffectiveDate, NewValue, Salary_EGP)` to remove API retries.
  2. Deterministic Arabic branch name standardization.
  3. `LEAD()` window function to compute closed-interval `ValidFrom` and `ValidTo` boundaries.
  4. Flagging current active records (`ValidTo = '9999-12-31' → IsCurrent = 1`).

| Column Name | Physical Data Type | Nullable | Key Type | Business Description |
| :--- | :--- | :---: | :---: | :--- |
| `StagingKey` | `INT IDENTITY(1,1)` | No | PK | Surrogate staging identifier. |
| `EmployeeID` | `VARCHAR(20)` | No | Natural Key | Employee identifier. |
| `EventType` | `VARCHAR(50)` | No | Attribute | Audit event type. |
| `ValidFrom` | `DATE` | No | SCD2 | Effective start date of this historical state slice. |
| `ValidTo` | `DATE` | No | SCD2 | Expiry date of this state slice (`9999-12-31` for current). |
| `IsCurrent` | `BIT` | No | SCD2 | `1` if this is the employee's current state; `0` if historical. |
| `BranchOrSalaryContext` | `NVARCHAR(150)` | Yes | Attribute | Standardized branch or role context. |
| `Salary_EGP` | `DECIMAL(18,2)` | Yes | Metric | Applicable salary during this validity window. |
| `IsTerminated` | `INT` | Yes | Flag | Separation flag. |

---

### 5.2 `stg.Exit_Attrition_Records` (Separation & Attrition Audits)
* **Source**: Transactional exit survey records (`exit_attrition_records.csv`).
* **Storage**: `[stg].[Exit_Attrition_Records]`
* **Grain**: 1 row per separated employee.

| Column Name | Physical Data Type | Nullable | Key Type | Business Description |
| :--- | :--- | :---: | :---: | :--- |
| `ExitAuditID` | `INT IDENTITY(1,1)` | No | PK | Surrogate key for exit audit event. |
| `EmployeeID` | `NVARCHAR(50)` | No | FK | Natural employee identifier (`EMP-10001` .. `EMP-17000`). |
| `NoticeDate` | `DATE` | Yes | Timestamp | Date when formal resignation notice was submitted. |
| `ExitDate` | `DATE` | No | Timestamp | Official last day of employment. |
| `ExitType` | `NVARCHAR(50)` | No | Attribute | Separation classification (`Voluntary`, `Involuntary`). |
| `PrimaryExitReason` | `NVARCHAR(100)` | No | Attribute | Reason for departure (`Compensation`, `Career Opportunity`, `Relocation`, `Burnout`). |
| `LastPerformanceScore`| `DECIMAL(4,2)` | Yes | Metric | Performance appraisal rating prior to departure. |
| `RehireEligible` | `BIT` | No | Flag | `1` if eligible for corporate rehire; `0` otherwise. |
| `SeparationSalary` | `DECIMAL(18,2)` | Yes | Metric | Base salary at separation. |
| `SeparationBranch` | `NVARCHAR(100)` | Yes | Dimension Ref | Branch where the employee was located at departure. |

---

## 6. Analytical Presentation Mart Tables (`mart` Schema)

Materialized via `sql/transformations/02_mart_dimensional_model.sql` and `scripts/transformations/run_mart_transformations.py`:

### 6.1 `mart.Dim_Employee` (Current Master Employee State)
* **Source**: Filtered from `stg.Stg_HR_Audit` where `rn = 1` ordered by `ValidFrom DESC`.
* **Grain**: Exactly 1 row per employee (7,000 rows).
* **Primary Key**: `EmployeeID` (Primary Key constraint `PK_Dim_Employee`).

| Column Name | Physical Data Type | Nullable | Key Type | Business Description |
| :--- | :--- | :---: | :---: | :--- |
| `EmployeeID` | `VARCHAR(20)` | No | PK | Natural employee identifier (`EMP-10001` .. `EMP-17000`). |
| `LatestBranch` | `NVARCHAR(150)` | Yes | Attribute | Most recently recorded operational branch. |
| `LatestSalary` | `DECIMAL(18,2)` | Yes | Metric | Current base monthly compensation in EGP. |
| `EmploymentStatus` | `VARCHAR(8)` | No | Attribute | Derived status: `'Active'` or `'Inactive'`. |

---

### 6.2 `mart.Fact_Employee_SCD2` (Historical Point-in-Time Headcount & Salary Fact)
* **Source**: Directly exposed from `stg.Stg_HR_Audit`.
* **Grain**: 1 row per validity interval per employee (12,392 rows).

| Column Name | Physical Data Type | Nullable | Key Type | Business Description |
| :--- | :--- | :---: | :---: | :--- |
| `StagingKey` | `INT` | No | PK / Identity | Staging transaction key. |
| `EmployeeID` | `VARCHAR(20)` | No | FK | Natural employee identifier. |
| `EventType` | `VARCHAR(50)` | No | Attribute | Lifecycle change event (`HIRE`, `PROMOTION`, `TRANSFER`, etc.). |
| `ValidFrom` | `DATE` | No | Timestamp | Beginning of validity interval. |
| `ValidTo` | `DATE` | No | Timestamp | End of validity interval (`9999-12-31` for current). |
| `IsCurrent` | `BIT` | No | Flag | `1` if record represents current state; `0` otherwise. |
| `BranchOrSalaryContext` | `NVARCHAR(150)` | Yes | Attribute | Historical branch or role context during interval. |
| `Salary_EGP` | `DECIMAL(18,2)` | Yes | Metric | Historical salary during interval. |
| `IsTerminated` | `INT` | Yes | Flag | `1` if terminated at this event; `0` otherwise. |

---

### 6.3 `mart.Fact_Daily_Badge` (IoT Access Telemetry with Imputed Durations)
* **Source**: Cleaned and transformed from `raw.Badge_Access_Logs`.
* **Grain**: 1 row per badge access log (114,952 rows).

| Column Name | Physical Data Type | Nullable | Key Type | Business Description |
| :--- | :--- | :---: | :---: | :--- |
| `LogID` | `VARCHAR(50)` | No | PK / Identity | Badge transaction identifier. |
| `EmployeeID` | `VARCHAR(50)` | No | FK | Employee identifier. |
| `AccessDate` | `DATE` | No | Date FK | Calendar access date. |
| `FacilityCode` | `VARCHAR(50)` | Yes | Attribute | Building identifier (`HQ-CAIRO`, `TECH-GIZA`, `OPS-ALEX`, etc.). |
| `SystemSource` | `VARCHAR(50)` | Yes | Attribute | Device channel (`TURNSTILE` or `GATEWAY`). |
| `CheckInTime` | `DATETIME` | Yes | Timestamp | First physical or virtual clock-in timestamp. |
| `CheckOutTime` | `DATETIME` | Yes | Timestamp | Clock-out timestamp (heurisically imputed +8 hours if missing). |
| `WorkDurationHours` | `DECIMAL(10,2)` | Yes | Metric | Total shift duration calculated in hours. |

---

### 6.4 `mart.Dim_Course` (Conformed Learning & Certification Catalog)
* **Source**: Conformed dimension deduplicated from LMS master telemetry.
* **Grain**: 1 row per professional course offering (10 distinct enterprise courses).
* **Storage**: In-memory Power BI VertiPaq tabular model / `mart.Dim_Course`.

| Column Name | Physical Data Type | Nullable | Key Type | Business Description |
| :--- | :--- | :---: | :---: | :--- |
| `CourseKey` | `INT` / `Whole Number` | No | PK | Surrogate primary key (1 to 10). |
| `CourseID` | `VARCHAR(20)` | No | Natural Key | Course code (`CRS-TECH-01..04`, `CRS-LEAD-01..02`, `CRS-SOFT-01..02`, `CRS-COMP-01..02`). |
| `CourseName` | `NVARCHAR(150)` | No | Attribute | Formal program title. |
| `SkillDomain` | `VARCHAR(50)` | No | Attribute | Capability domain (`Tech`, `Leadership`, `Soft Skills`, `Compliance`). |
| `CourseLevel` | `VARCHAR(50)` | No | Attribute | Level tier: `Level 100 - Foundational Core`, `Level 200 - Intermediate & Professional`, `Level 300 - Advanced Architecture & Strategic`. |
| `StrategicPillar` | `VARCHAR(100)` | No | Attribute | Executive capability pillar alignment. |
| `Cost_EGP` | `DECIMAL(12,2)` | No | Metric | Standard catalog course fee / tuition expense. |
| `PassingScoreThreshold` | `INT` | No | Metric | Minimum examination score required to pass (default 70). |
| `ValidityPeriodMonths` | `INT` | No | Metric | Audit validity lifespan (12 months for Compliance, 24 months for others). |
| `DeliveryModality` | `VARCHAR(50)` | No | Attribute | Delivery channel: `Virtual Lab & Sandbox`, `Executive Workshop`, `Self-Paced E-Learning`. |

---

### 6.5 `mart.Fact_TrainingCompletions` / `Fact_LMS_Training` (Talent Development Telemetry)
* **Source**: Ingested from `raw.LMS_Certifications` (7,197 total attempts) and materialized into Kimball Galaxy Schema.
* **Grain**: 1 row per employee course attempt / examination.

| Column Name | Physical Data Type | Nullable | Key Type | Business Description |
| :--- | :--- | :---: | :---: | :--- |
| `CompletionKey` | `INT` / `Whole Number` | No | PK | Surrogate fact transaction key. |
| `CompletionDateKey` | `INT` / `Whole Number` | No | Date FK | Smart integer calendar key (`YYYYMMDD`) joining to `Dim_Date[DateKey]`. |
| `EmployeeKey` | `INT` / `Whole Number` | No | FK | Surrogate foreign key joining to `Dim_Employee[EmployeeKey]`. |
| `CourseKey` | `INT` / `Whole Number` | No | FK | Surrogate foreign key joining to `Dim_Course[CourseKey]`. |
| `EmployeeID` | `VARCHAR(20)` | No | Degenerate FK | Natural employee code (`EMP-10001` .. `EMP-17000`). |
| `CourseID` | `VARCHAR(20)` | No | Degenerate FK | Course catalog identifier (`CRS-101` .. `CRS-302`). |
| `CompletionDate` | `DATE` | No | Timestamp | Date of examination or completion. |
| `Score` | `FLOAT` / `INT` | No | Metric | Final examination grade (0 to 100). |
| `Status` | `VARCHAR(50)` | No | Attribute | Raw platform status (`Completed`, `In Progress`, `Failed`). |
| `Cost_EGP` | `DECIMAL(12,2)` | No | Metric | Actual expenditure for attempt. |
| `IsPassed` | `BIT` / `Whole Number` | No | Flag | `1` if passed benchmark ($\ge 70$ or `Completed`); `0` otherwise. |
| `ScoreTier` | `VARCHAR(50)` | No | Attribute | Evaluation band: `⭐ Distinction (90-100)`, `🟢 Proficient Pass (70-89)`, `🔴 Remediation Required (<70)`. |

---

### 6.6 `mart.Dim_CurrencyRates` (Live Exchange Rate Telemetry Dimension)
* **Source**: Real-time REST API (`https://open.er-api.com/v6/latest/USD`) ingested dynamically via Power Query `Web.Contents` with relative path security.
* **Grain**: 1 row per active target currency (USD, EGP, AED, SAR, EUR, GBP).
* **Storage**: In-memory Power BI VertiPaq tabular model.

| Column Name | Physical Data Type | Nullable | Key Type | Business Description |
| :--- | :--- | :---: | :---: | :--- |
| `CurrencyKey` | `INT` / `Whole Number` | No | PK | Primary surrogate currency key (1 to 6). |
| `CurrencyCode` | `VARCHAR(10)` | No | Natural Key | Standard ISO 3-letter currency code (`EGP`, `USD`, `AED`, `SAR`, `EUR`, `GBP`). |
| `ExchangeRateToUSD` | `DECIMAL(18,6)` | No | Metric | Direct conversion rate from USD base. |
| `RateToEGP` | `DECIMAL(18,6)` | No | Metric | Computed relative rate against Egyptian Pound base. |
| `OneEGPInCurrency` | `DECIMAL(18,6)` | No | Metric | Conversion multiplier: value of 1 EGP in foreign currency. |
| `LastRefreshedUTC` | `DATETIMEOFFSET` | No | Audit | UTC timestamp of last live exchange rate sync. |




