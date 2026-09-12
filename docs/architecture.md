# Enterprise Kimball Galaxy Schema Architecture Deep Dive

This document details the architectural design and Kimball dimensional modeling principles implemented in the **Enterprise Human Capital & Operational Efficiency Diagnostics** platform.

![Enterprise Project Lifecycle & Data Architecture](assets/project_lifecycle_architecture.svg)

---

## 1. Why a Galaxy Schema (Fact Constellation)?

A classic **Star Schema** organizes one single business process around a single central fact table (e.g. Sales, Orders). However, enterprise workforce analytics encompasses multiple, distinct operational processes operating at differing grains:

1. **Monthly Workforce State**: Periodic snapshot of active personnel, compensation, and annual appraisal scores.
2. **Daily IoT Attendance**: High-frequency transactional clock events, turnstile swipes, and remote work flags.
3. **Quarterly FP&A Budgeting**: Aggregated departmental headcount quotas and salary expenditure limits.
4. **Talent & Certification Events**: Discrete training completions, exam scores, and educational investment fees.

Attempting to merge these distinct business processes into a single fact table leads to severe **grain mismatch**, **null inflation**, or **fact duplication** (e.g., repeating an employee's monthly salary on every single training attempt or daily badge log).

A **Kimball Galaxy Schema (Fact Constellation)** solves this by maintaining separate fact tables for each business process while sharing **Conformed Dimensions**.

```
                           ┌─────────────────┐
                           │   Dim_Branch    │
                           └────────┬────────┘
                                    │
               ┌────────────────────┼────────────────────┐
               │                    │                    │
               ▼                    ▼                    ▼
     ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
     │  Fact_Workforce  │  │   Fact_Daily     │  │ Fact_Department  │
     │     Snapshot     │  │   Attendance     │  │     Budget       │
     └─────────┬────────┘  └────────┬─────────┘  └────────┬─────────┘
               │                    │                     │
               ├────────────────────┼─────────────────────┘
               │                    │
               ▼                    ▼
     ┌──────────────────┐  ┌──────────────────┐
     │   Dim_Employee   │  │     Dim_Date     │
     └──────────────────┘  └──────────────────┘
```

---

## 2. Conformed Dimensions

A dimension is **conformed** when it has consistent meaning and keys across all business processes:

1. **`Dim_Employee`**:
   * Shared by `Fact_WorkforceSnapshot`, `Fact_DailyAttendance`, and `Fact_TrainingCompletions`.
   * Implements **Slowly Changing Dimensions (SCD Type 2)**: Tracks changes in salary, branch, and role over time using `EffectiveDate`, `ExpiryDate`, and `IsCurrent`.
2. **`Dim_Date`**:
   * Canonical enterprise calendar dimension.
   * Connects to all four fact tables:
     * `Fact_WorkforceSnapshot` via `SnapshotDateKey` (Monthly cutoff).
     * `Fact_DailyAttendance` via `AccessDateKey` (Daily access date).
     * `Fact_DepartmentBudget` via `DateKey` (Quarter starting date).
     * `Fact_TrainingCompletions` via `CompletionDateKey` (Certification date).
3. **`Dim_Department`**:
   * Connects to `Fact_WorkforceSnapshot` and `Fact_DepartmentBudget`.
4. **`Dim_Branch`**:
   * Connects to `Fact_WorkforceSnapshot`, `Fact_DailyAttendance`, and `Fact_DepartmentBudget`.
5. **`Dim_Course`**:
   * Connects to `Fact_TrainingCompletions`.

---

## 3. Fact-to-Fact Cross-Filtering Best Practices in Power BI

In Power BI, multiple fact tables connected to conformed dimensions should follow these rules:

1. **Single-Direction Filtering**:
   * Conformed Dimensions filter Fact Tables ($1 \to *$).
   * Relationships must never be Bi-directional.
2. **Fact-to-Fact Comparison via Measures**:
   * Never join two fact tables directly in the relationship diagram.
   * Use DAX measures to compare metrics across facts (e.g., `Headcount Variance = [Actual Active Headcount] - [Budgeted Target Headcount]`).
   * Filter context flows naturally from the conformed dimension (e.g. slicing by `Dim_Department[DepartmentName]`) down to both fact tables simultaneously, computing the correct variance at any level of aggregation.
3. **Bi-temporal Modeling with `USERELATIONSHIP`**:
   * When a fact has multiple date relationships (e.g., `NoticeDate` vs `ExitDate`), establish one active relationship to `Dim_Date` and use `USERELATIONSHIP()` in DAX for alternative date perspectives.
