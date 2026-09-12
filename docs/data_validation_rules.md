# Enterprise Data Quality & Validation Rules Specification

This specification establishes the automated data quality contracts, schema integrity constraints, and domain boundary assertions enforced across the **Enterprise Human Capital & Operational Efficiency Diagnostics** platform.

---

## 1. Dimensional Integrity & Primary Key Constraints

| Dimension | Primary Key | Key Type | Uniqueness Constraint | Nullability | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`Dim_Employee`** | `EmployeeKey` | Surrogate (`INT IDENTITY` / Index) | **100% Unique (7,000 keys)** | `NOT NULL` | Surrogate key identifying specific historical employee version (SCD Type 2). |
| **`Dim_Department`**| `DepartmentKey`| Surrogate (`INT IDENTITY` / Index) | **100% Unique (6 keys)** | `NOT NULL` | Conformed corporate department and division key. |
| **`Dim_Branch`** | `BranchKey` | Surrogate (`INT IDENTITY` / Index) | **100% Unique (14 keys)** | `NOT NULL` | Geographic office, branch, and regional hub key. |
| **`Dim_Date`** | `DateKey` | Smart Key (`YYYYMMDD`) | **100% Unique (1,096 keys)** | `NOT NULL` | Canonical enterprise calendar key (range 2024–2026). |
| **`Dim_Course`** | `CourseKey` | Surrogate (`INT IDENTITY` / Index) | **100% Unique (10 keys)** | `NOT NULL` | Catalog key for professional training programs. |

---

## 2. Master Text Dataset Grounding & Fidelity Contract

To ensure 100% data authenticity and prevent synthetic drift or artificial mocking of core human attributes, the entire pipeline is grounded strictly against `data/raw/employees_data_7000.txt`.

* **Rule `VAL-FID-001` (Exact Employee Count)**:
  $$N_{\text{Employees}} \equiv 7,000 \quad \text{across raw, staging, mart, and Power BI semantic models}$$
* **Rule `VAL-FID-002` (Deterministic ID Sequence)**:
  $$\text{EmployeeID} \in \{\text{'EMP-10001'}, \dots, \text{'EMP-17000'}\} \quad (\text{Strict 1-to-1 sequential mapping})$$
* **Rule `VAL-FID-003` (Authentic Arabic Identity Preservation)**:
  $$\forall e \in \text{Employees}: \text{FullName} \ne \emptyset, \quad \text{Gender} \in \{\text{'ذكر'}, \text{'أنثى'}\}, \quad \text{Email contains '@'}$$
* **Rule `VAL-FID-004` (Non-Mutated Employment Attributes)**:
  $$\text{HireDate}, \text{Department}, \text{Branch}, \text{ContractType}, \text{MaritalStatus} \quad \text{must match source text records verbatim.}$$

---

## 3. Foreign Key Referential Integrity (Galaxy Schema)

Every fact table in the constellation must adhere to strict foreign key referential integrity against conformed dimensions. **Orphaned records (FK with no matching PK) are strictly rejected (0 tolerance).**

```
Fact_WorkforceSnapshot.EmployeeKey     ───► Dim_Employee.EmployeeKey   (Zero Orphans)
Fact_WorkforceSnapshot.DepartmentKey   ───► Dim_Department.DepartmentKey (Zero Orphans)
Fact_WorkforceSnapshot.BranchKey       ───► Dim_Branch.BranchKey         (Zero Orphans)
Fact_WorkforceSnapshot.SnapshotDateKey ───► Dim_Date.DateKey             (Zero Orphans)

Fact_DailyAttendance.EmployeeKey       ───► Dim_Employee.EmployeeKey   (Zero Orphans)
Fact_DailyAttendance.BranchKey         ───► Dim_Branch.BranchKey         (Zero Orphans)
Fact_DailyAttendance.AccessDateKey     ───► Dim_Date.DateKey             (Zero Orphans)

Fact_DepartmentBudget.DepartmentKey    ───► Dim_Department.DepartmentKey (Zero Orphans)
Fact_DepartmentBudget.BranchKey        ───► Dim_Branch.BranchKey         (Zero Orphans)
Fact_DepartmentBudget.DateKey          ───► Dim_Date.DateKey             (Zero Orphans)

Fact_TrainingCompletions.EmployeeKey   ───► Dim_Employee.EmployeeKey   (Zero Orphans)
Fact_TrainingCompletions.CourseKey     ───► Dim_Course.CourseKey         (Zero Orphans)
Fact_TrainingCompletions.DateKey       ───► Dim_Date.DateKey             (Zero Orphans)
```

---

## 4. Slowly Changing Dimension (SCD Type 2) & Audit Event Rules

For `stg.Stg_HR_Audit` and `mart.Dim_Employee`:

* **Rule `VAL-SCD-001` (Deduplication of Retry Duplicates)**:
  $$\text{Raw events (12,516 rows)} \xrightarrow{\text{Deduplicate on (EmpID, EventType, EffectiveDate, NewVal, Salary)}} \text{Staged events (12,392 rows)}$$
* **Rule `VAL-SCD-002` (Temporal Chronology & Non-Overlapping Intervals)**:
  $$\text{ValidFrom} \le \text{ValidTo} \quad \forall \text{ employee audit versions}$$
* **Rule `VAL-SCD-003` (Exactly One Current Record per Employee)**:
  $$\sum_{v \in \text{versions}(e)} \mathbb{I}(v.\text{IsCurrent} = 1) \equiv 1 \quad \forall e \in \{1 \dots 7,000\}$$
* **Rule `VAL-SCD-004` (Open-Ended Current Expiry Sentinel)**:
  $$\text{If } \text{IsCurrent} = 1 \implies \text{ValidTo} \equiv \text{'9999-12-31'}$$
* **Rule `VAL-SCD-005` (Audit Employee Universe Coverage)**:
  $$|\text{Distinct Employees in } \text{stg.Stg\_HR\_Audit}| \equiv 7,000$$

---

## 5. Business Range & Domain Validation Rules

### 5.1 Compensation & Payroll Bounds
* **Rule `VAL-PAY-001` (Non-Negative Salary)**:
  $$\text{BaseSalary} > 0 \quad \forall \text{ active records}$$
* **Rule `VAL-PAY-002` (Reasonable Enterprise Range)**:
  $$5,000 \text{ EGP} \le \text{BaseSalary} \le 500,000 \text{ EGP}$$
* **Rule `VAL-PAY-003` (Standardized Currency)**:
  $$\text{Currency} \equiv \text{'EGP'} \quad (\text{Foreign currency conversions normalized at daily spot rate})$$

### 5.2 Time & Attendance Integrity
* **Rule `VAL-ATT-001` (Shift Duration Boundary)**:
  $$0.0 \text{ hours} \le \text{DurationHours} \le 24.0 \text{ hours}$$
* **Rule `VAL-ATT-002` (Night Shift Reconciliation)**:
  $$\text{If } \text{CheckOutTime} < \text{CheckInTime}, \quad \text{Duration} = (24 - \text{CheckInTime}) + \text{CheckOutTime}$$
* **Rule `VAL-ATT-003` (Heuristic Imputation Flag)**:
  $$\text{If } \text{CheckOutTime was NULL} \implies \text{IsImputedClockOut} = 1 \text{ and } \text{Duration} = \text{MedianShiftHours (8.0)}$$

### 5.3 Performance & Learning Metrics
* **Rule `VAL-PRF-001` (Rating Scale)**:
  $$1.00 \le \text{AnnualPerformanceRating} \le 5.00$$
* **Rule `VAL-LMS-001` (Exam Score Boundary)**:
  $$0.0 \le \text{Score} \le 100.0$$
* **Rule `VAL-LMS-002` (Passing Threshold Consistency)**:
  $$\text{IsPassed} = 1 \iff \text{Score} \ge 70.0$$
* **Rule `VAL-LMS-003` (Non-Negative Certification Investment)**:
  $$\text{CertificationCost\_EGP} \ge 0.00$$

---

## 6. Diagnostic Anomaly Rules

### 6.1 Salary Compression Detection
$$\text{IsSalaryCompressed} = 1 \iff (\text{TenureYears} \ge 3.0) \land (\text{BaseSalary} < \text{Median}_{\text{NewHires}}(\text{Role}))$$

### 6.2 Ghost Worker Flag
$$\text{GhostWorker} = 1 \iff (\text{EmploymentStatus} = \text{'Active'}) \land (\text{DaysSinceLastPhysicalAccess} > 60)$$

### 6.3 Workplace Policy Contract Violation
$$\text{IsContractViolation} = 1 \iff (\text{ContractType} = \text{'دوام كامل (حضوري)'}) \land (\text{ActualWorkMode} = \text{'Remote'})$$

---

## 7. Automated Testing Suite (Pytest Implementation)

The platform includes **14 automated data quality and transformation test cases** in `tests/test_data_quality.py`:

| Test Function | Target Scope | Verified Assertion |
| :--- | :--- | :--- |
| **`test_dim_department_pk_uniqueness`** | `Dim_Department` | 100% unique primary keys, non-empty department names. |
| **`test_dim_branch_pk_uniqueness`** | `Dim_Branch` | 100% unique primary keys, valid region and city strings. |
| **`test_dim_course_pk_uniqueness`** | `Dim_Course` | 100% unique primary keys, allowed domain values (`Tech`, `Soft Skills`, `Leadership`, `Compliance`). |
| **`test_dim_date_pk_uniqueness`** | `Dim_Date` | 100% unique calendar keys, valid quarters (1–4), months (1–12), weekend flags (0/1). |
| **`test_dim_employee_pk_uniqueness_and_scd2`** | `Dim_Employee` | Exactly 7,000 unique keys, positive salaries, `EffectiveDate <= ExpiryDate`. |
| **`test_fact_workforce_snapshot`** | `Fact_WorkforceSnapshot` | Exactly 7,000 records, zero FK orphans, salary bounds (5K–500K), rating bounds (1–5). |
| **`test_fact_daily_attendance`** | `Fact_DailyAttendance` | Zero FK orphans, duration hours bounded in [0, 24], valid boolean flags. |
| **`test_fact_department_budget`** | `Fact_DepartmentBudget` | Zero FK orphans, non-negative headcounts, positive salary budgets. |
| **`test_fact_training_completions`** | `Fact_TrainingCompletions` | Zero FK orphans, score in [0, 100], `IsPassed == (Score >= 70)`, non-negative costs. |
| **`test_impute_attendance_shift`** | Unit Transformation | Daytime duration, 8-hour missing clock-out imputation, night-shift crossover. |
| **`test_standardize_branch_name`** | Unit Transformation | Arabic fuzzy matching and canonicalization (e.g. `المعادى` $\to$ `القاهرة - المعادي`). |
| **`test_master_txt_dataset_fidelity`** | Master Grounding | Exactly 7,000 records in `employees_data_7000.txt`, sequential `EMP-10001`..`EMP-17000`, non-empty Arabic names, valid genders. |
| **`test_scd2_hr_audit_staging_rules`** | SCD Type 2 Audit | 12,516 $\to$ 12,392 deduplication, `ValidFrom <= ValidTo`, exactly 7,000 current records (`IsCurrent = 1`, `ValidTo = '9999-12-31'`). |
| **`test_foreign_key_cross_fact_integrity`** | Full Constellation | 100% referential integrity across all 4 galaxy facts against conformed dimensions with 0 orphans. |

### Running the Test Suite
```bash
# Run complete test suite with verbose output
python -m pytest tests/test_data_quality.py -v

# Expected Output: 14 passed in ~1.6 seconds
```
