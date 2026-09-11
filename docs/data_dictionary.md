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
