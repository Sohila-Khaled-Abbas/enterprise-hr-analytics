# Enterprise Data Quality & Validation Rules Specification

This specification establishes the automated data quality contracts, schema integrity constraints, and domain boundary assertions enforced across the **Enterprise Human Capital & Operational Efficiency Diagnostics** platform.

---

## 1. Dimensional Integrity & Primary Key Constraints

| Dimension | Primary Key | Key Type | Uniqueness Constraint | Nullability | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`Dim_Employee`** | `EmployeeKey` | Surrogate (`INT IDENTITY`) | **100% Unique** | `NOT NULL` | Surrogate key identifying specific historical employee version (SCD Type 2). |
| **`Dim_Department`**| `DepartmentKey`| Surrogate (`INT IDENTITY`) | **100% Unique** | `NOT NULL` | Conformed department dimension key. |
| **`Dim_Branch`** | `BranchKey` | Surrogate (`INT IDENTITY`) | **100% Unique** | `NOT NULL` | Geographic office and branch key. |
| **`Dim_Date`** | `DateKey` | Smart Key (`YYYYMMDD`) | **100% Unique** | `NOT NULL` | Canonical enterprise calendar key (range 2024–2026). |
| **`Dim_Course`** | `CourseKey` | Surrogate (`INT IDENTITY`) | **100% Unique** | `NOT NULL` | Catalog key for learning and certification programs. |

---

## 2. Foreign Key Referential Integrity (Galaxy Schema)

Every fact table in the constellation must adhere to strict foreign key referential integrity against conformed dimensions. **Orphaned records (FK with no matching PK) are strictly rejected.**

```
Fact_WorkforceSnapshot.EmployeeKey   ───► Dim_Employee.EmployeeKey   (Zero Orphans)
Fact_WorkforceSnapshot.DepartmentKey ───► Dim_Department.DepartmentKey (Zero Orphans)
Fact_WorkforceSnapshot.BranchKey     ───► Dim_Branch.BranchKey         (Zero Orphans)
Fact_WorkforceSnapshot.SnapshotDateKey─► Dim_Date.DateKey             (Zero Orphans)

Fact_DailyAttendance.EmployeeKey     ───► Dim_Employee.EmployeeKey   (Zero Orphans)
Fact_DailyAttendance.BranchKey       ───► Dim_Branch.BranchKey         (Zero Orphans)
Fact_DailyAttendance.AccessDateKey   ───► Dim_Date.DateKey             (Zero Orphans)

Fact_DepartmentBudget.DepartmentKey  ───► Dim_Department.DepartmentKey (Zero Orphans)
Fact_DepartmentBudget.BranchKey      ───► Dim_Branch.BranchKey         (Zero Orphans)
Fact_DepartmentBudget.DateKey        ───► Dim_Date.DateKey             (Zero Orphans)

Fact_TrainingCompletions.EmployeeKey ───► Dim_Employee.EmployeeKey   (Zero Orphans)
Fact_TrainingCompletions.CourseKey   ───► Dim_Course.CourseKey         (Zero Orphans)
Fact_TrainingCompletions.DateKey     ───► Dim_Date.DateKey             (Zero Orphans)
```

---

## 3. Business Range & Domain Validation Rules

### 3.1 Compensation & Payroll Bounds
* **Rule `VAL-PAY-001` (Non-Negative Salary)**:
  $$\text{BaseSalary} > 0 \quad \forall \text{ active records}$$
* **Rule `VAL-PAY-002` (Reasonable Enterprise Range)**:
  $$5,000 \text{ EGP} \le \text{BaseSalary} \le 500,000 \text{ EGP}$$
* **Rule `VAL-PAY-003` (Standardized Currency)**:
  $$\text{Currency} \equiv \text{'EGP'} \quad (\text{Foreign currency conversions must be normalized at daily spot rate})$$

### 3.2 Time & Attendance Integrity
* **Rule `VAL-ATT-001` (Shift Duration Boundary)**:
  $$0.0 \text{ hours} \le \text{DurationHours} \le 24.0 \text{ hours}$$
* **Rule `VAL-ATT-002` (Night Shift Reconciliation)**:
  $$\text{If } \text{CheckOutTime} < \text{CheckInTime}, \quad \text{Duration} = (24 - \text{CheckInTime}) + \text{CheckOutTime}$$
* **Rule `VAL-ATT-003` (Heuristic Imputation Flag)**:
  $$\text{If } \text{CheckOutTime was NULL}, \quad \text{IsImputedClockOut} = 1 \text{ and } \text{Duration} = \text{MedianShiftHours}$$

### 3.3 Performance & Learning Metrics
* **Rule `VAL-PRF-001` (Rating Scale)**:
  $$1.00 \le \text{AnnualPerformanceRating} \le 5.00$$
* **Rule `VAL-LMS-001` (Exam Score Boundary)**:
  $$0.0 \le \text{Score} \le 100.0$$
* **Rule `VAL-LMS-002` (Passing Threshold Consistency)**:
  $$\text{IsPassed} = 1 \iff \text{Score} \ge 70.0$$
* **Rule `VAL-LMS-003` (Non-Negative Certification Investment)**:
  $$\text{CertificationCost\_EGP} \ge 0.00$$

---

## 4. Slowly Changing Dimension (SCD Type 2) Rules

For `Dim_Employee`:
* **Rule `VAL-SCD-001` (Temporal Chronology)**:
  $$\text{EffectiveDate} \le \text{ExpiryDate} \quad \forall \text{ dimension versions}$$
* **Rule `VAL-SCD-002` (Single Current Version)**:
  $$\sum_{\text{versions for EmployeeID}} \text{IsCurrent} \equiv 1$$
* **Rule `VAL-SCD-003` (Open-Ended Expiry)**:
  $$\text{If } \text{IsCurrent} = 1, \quad \text{ExpiryDate} \equiv \text{'9999-12-31'}$$

---

## 5. Diagnostic Anomaly Rules

### 5.1 Salary Compression Detection
$$\text{IsSalaryCompressed} = 1 \iff (\text{TenureYears} \ge 3.0) \land (\text{BaseSalary} < \text{Median}_{\text{NewHires}}(\text{Role}))$$

### 5.2 Ghost Worker Flag
$$\text{GhostWorker} = 1 \iff (\text{EmploymentStatus} = \text{'Active'}) \land (\text{DaysSinceLastPhysicalAccess} > 60)$$

### 5.3 Workplace Policy Contract Violation
$$\text{IsContractViolation} = 1 \iff (\text{ContractType} = \text{'دوام كامل (حضوري)'}) \land (\text{ActualWorkMode} = \text{'Remote'})$$

---

## 6. Automated Testing Implementation (Pytest Suite)

Automated tests in `tests/test_data_quality.py` run continuously in CI/CD to validate:
1. `test_dimensions_primary_key_uniqueness`: Asserts 0 duplicate surrogate keys.
2. `test_facts_referential_integrity`: Asserts 0 orphaned records across all fact foreign keys.
3. `test_salary_and_performance_domain_bounds`: Asserts non-negative compensation and valid ratings.
4. `test_attendance_duration_validity`: Asserts all durations are between 0 and 24 hours.
5. `test_scd2_consistency`: Asserts non-overlapping validity windows.
