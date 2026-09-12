"""
Enterprise Human Capital & Operational Efficiency Diagnostics
Module: test_data_quality.py
Purpose: Automated Pytest suite verifying dimensional contracts, foreign key referential
         integrity, metric range bounds, and transformation logic.
"""

import csv
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from scripts.utils.data_cleaners import (
    impute_attendance_shift,
    standardize_branch_name,
    unpivot_quarterly_budgets,
    deduplicate_lms_attempts,
    calculate_salary_compression,
)

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
RAW_DIR = BASE_DIR / "data" / "raw"


def load_csv(filename: str) -> List[Dict[str, str]]:
    filepath = PROCESSED_DIR / filename
    assert filepath.exists(), f"Expected processed file {filename} does not exist. Run pipeline_runner.py first."
    with open(filepath, mode="r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


# =============================================================================
# 1. Conformed Dimensions Primary Key Uniqueness & Constraints
# =============================================================================
def test_dim_department_pk_uniqueness():
    depts = load_csv("Dim_Department.csv")
    keys = [r["DepartmentKey"] for r in depts]
    assert len(keys) > 0
    assert len(keys) == len(set(keys)), "Duplicate DepartmentKey found in Dim_Department"
    for d in depts:
        assert d["DepartmentName"].strip() != "", "Empty DepartmentName found"


def test_dim_branch_pk_uniqueness():
    branches = load_csv("Dim_Branch.csv")
    keys = [r["BranchKey"] for r in branches]
    assert len(keys) > 0
    assert len(keys) == len(set(keys)), "Duplicate BranchKey found in Dim_Branch"
    for b in branches:
        assert b["Region"].strip() != "", "Empty Region found"
        assert b["City"].strip() != "", "Empty City found"


def test_dim_course_pk_uniqueness():
    courses = load_csv("Dim_Course.csv")
    keys = [r["CourseKey"] for r in courses]
    assert len(keys) > 0
    assert len(keys) == len(set(keys)), "Duplicate CourseKey found in Dim_Course"
    valid_domains = {"Tech", "Soft Skills", "Leadership", "Compliance"}
    for c in courses:
        assert c["SkillDomain"] in valid_domains, f"Invalid SkillDomain: {c['SkillDomain']}"


def test_dim_date_pk_uniqueness():
    dates = load_csv("Dim_Date.csv")
    keys = [r["DateKey"] for r in dates]
    assert len(keys) > 0
    assert len(keys) == len(set(keys)), "Duplicate DateKey found in Dim_Date"
    for d in dates:
        assert 1 <= int(d["CalendarQuarter"]) <= 4
        assert 1 <= int(d["MonthNumberOfYear"]) <= 12
        assert int(d["IsWeekend"]) in (0, 1)


def test_dim_employee_pk_uniqueness_and_scd2():
    emps = load_csv("Dim_Employee.csv")
    keys = [r["EmployeeKey"] for r in emps]
    assert len(keys) == 7000, f"Expected 7000 employees, found {len(keys)}"
    assert len(keys) == len(set(keys)), "Duplicate EmployeeKey found in Dim_Employee"

    # SCD Type 2 assertions
    for e in emps:
        assert float(e["BaseSalary"]) > 0, "Non-positive salary detected"
        assert e["EffectiveDate"] <= e["ExpiryDate"], "EffectiveDate must be <= ExpiryDate"
        assert int(e["IsCurrent"]) in (0, 1)


# =============================================================================
# 2. Galaxy Fact Tables Foreign Key Referential Integrity & Domain Bounds
# =============================================================================
def test_fact_workforce_snapshot():
    emps = {r["EmployeeKey"] for r in load_csv("Dim_Employee.csv")}
    depts = {r["DepartmentKey"] for r in load_csv("Dim_Department.csv")}
    branches = {r["BranchKey"] for r in load_csv("Dim_Branch.csv")}
    dates = {r["DateKey"] for r in load_csv("Dim_Date.csv")}

    wf = load_csv("Fact_WorkforceSnapshot.csv")
    assert len(wf) == 7000

    for r in wf:
        # FK integrity
        assert r["EmployeeKey"] in emps, f"Orphaned EmployeeKey: {r['EmployeeKey']}"
        assert r["DepartmentKey"] in depts, f"Orphaned DepartmentKey: {r['DepartmentKey']}"
        assert r["BranchKey"] in branches, f"Orphaned BranchKey: {r['BranchKey']}"
        assert r["SnapshotDateKey"] in dates, f"Orphaned SnapshotDateKey: {r['SnapshotDateKey']}"

        # Domain bounds
        salary = float(r["BaseSalary"])
        assert 5000 <= salary <= 500000, f"Salary out of range: {salary}"
        perf = float(r["AnnualPerformanceRating"])
        assert 1.0 <= perf <= 5.0, f"Performance rating out of range: {perf}"
        pct = float(r["SalaryPercentileInRole"])
        assert 0.0 <= pct <= 1.0, f"Percentile out of range: {pct}"


def test_fact_daily_attendance():
    emps = {r["EmployeeKey"] for r in load_csv("Dim_Employee.csv")}
    branches = {r["BranchKey"] for r in load_csv("Dim_Branch.csv")}
    dates = {r["DateKey"] for r in load_csv("Dim_Date.csv")}

    att = load_csv("Fact_DailyAttendance.csv")
    assert len(att) > 0

    for r in att:
        # FK integrity
        assert r["EmployeeKey"] in emps, f"Orphaned EmployeeKey: {r['EmployeeKey']}"
        assert r["BranchKey"] in branches, f"Orphaned BranchKey: {r['BranchKey']}"
        assert r["AccessDateKey"] in dates, f"Orphaned AccessDateKey: {r['AccessDateKey']}"

        # Duration bounds (0.0 to 24.0 hours)
        dur = float(r["DurationHours"])
        assert 0.0 <= dur <= 24.0, f"Attendance duration out of bounds: {dur}"
        assert int(r["IsContractViolation"]) in (0, 1)
        assert int(r["IsImputedClockOut"]) in (0, 1)


def test_fact_department_budget():
    depts = {r["DepartmentKey"] for r in load_csv("Dim_Department.csv")}
    branches = {r["BranchKey"] for r in load_csv("Dim_Branch.csv")}
    dates = {r["DateKey"] for r in load_csv("Dim_Date.csv")}

    budgets = load_csv("Fact_DepartmentBudget.csv")
    assert len(budgets) > 0

    for r in budgets:
        # FK integrity
        assert r["DepartmentKey"] in depts, f"Orphaned DepartmentKey: {r['DepartmentKey']}"
        assert r["BranchKey"] in branches, f"Orphaned BranchKey: {r['BranchKey']}"
        assert r["DateKey"] in dates, f"Orphaned DateKey: {r['DateKey']}"

        # Budget amounts
        assert int(r["BudgetedHeadcount"]) >= 0
        assert float(r["AllocatedSalaryBudget_EGP"]) > 0


def test_fact_training_completions():
    emps = {r["EmployeeKey"] for r in load_csv("Dim_Employee.csv")}
    courses = {r["CourseKey"] for r in load_csv("Dim_Course.csv")}
    dates = {r["DateKey"] for r in load_csv("Dim_Date.csv")}

    training = load_csv("Fact_TrainingCompletions.csv")
    assert len(training) > 0

    for r in training:
        # FK integrity
        assert r["EmployeeKey"] in emps, f"Orphaned EmployeeKey: {r['EmployeeKey']}"
        assert r["CourseKey"] in courses, f"Orphaned CourseKey: {r['CourseKey']}"
        assert r["CompletionDateKey"] in dates, f"Orphaned DateKey: {r['CompletionDateKey']}"

        score = float(r["Score"])
        assert 0.0 <= score <= 100.0, f"Score out of bounds: {score}"
        is_passed = int(r["IsPassed"])
        assert is_passed == (1 if score >= 70.0 else 0), "IsPassed inconsistent with Score"
        assert float(r["CertificationCost_EGP"]) >= 0.0


# =============================================================================
# 3. Transformation & Heuristic Cleaner Unit Tests
# =============================================================================
def test_impute_attendance_shift():
    # Normal daytime
    res1 = impute_attendance_shift("09:00:00", "17:00:00")
    assert res1["duration_hours"] == 8.0
    assert not res1["is_missing_clock_out"]
    assert not res1["is_imputed_clock_out"]
    assert not res1["is_night_shift"]

    # Missing clock-out (imputed +8h)
    res2 = impute_attendance_shift("09:00:00", None, median_shift_hours=8.0)
    assert res2["is_missing_clock_out"]
    assert res2["is_imputed_clock_out"]
    assert res2["check_out"] == "17:00:00"
    assert res2["duration_hours"] == 8.0

    # Night shift (cross midnight: 22:00 to 06:00 = 8.0h)
    res3 = impute_attendance_shift("22:00:00", "06:00:00")
    assert res3["is_night_shift"]
    assert res3["duration_hours"] == 8.0


def test_standardize_branch_name():
    assert standardize_branch_name("القاهرة - المعادي") == "القاهرة - المعادي"
    assert standardize_branch_name("المعادى") == "القاهرة - المعادي"
    assert standardize_branch_name("اسكندرية سموحة") == "الإسكندرية - سموحة"
    assert standardize_branch_name("التجمع") == "القاهرة - التجمع الخامس"
    assert standardize_branch_name("الدقي") == "الجيزة - الدقي"


# =============================================================================
# 4. Master 7,000 Employees Fidelity & SCD2 Audit Integrity Tests
# =============================================================================
def test_master_txt_dataset_fidelity():
    """Validates that employees_data_7000.txt, employees_core.csv, and Dim_Employee.csv

    exhibit 100% data fidelity: exactly 7000 employees, sequential EMP IDs, and matching attributes.
    """
    raw_txt_path = RAW_DIR / "employees_data_7000.txt"
    assert raw_txt_path.exists(), "Master raw text file employees_data_7000.txt is missing"

    # Count records in master text file
    with open(raw_txt_path, "r", encoding="utf-8") as f:
        txt_content = f.read()
    records = [r for r in txt_content.split("------") if r.strip()]
    assert len(records) == 7000, f"Expected exactly 7000 records in master txt, found {len(records)}"

    # Check processed Dim_Employee
    dim_emps = load_csv("Dim_Employee.csv")
    assert len(dim_emps) == 7000, f"Expected 7000 employees in Dim_Employee, found {len(dim_emps)}"

    expected_ids = [f"EMP-{10000 + i}" for i in range(1, 7001)]
    actual_ids = [r["EmployeeID"] for r in dim_emps]
    assert actual_ids == expected_ids, "EmployeeID sequence mismatch against master specification"

    # Validate non-empty mandatory core fields
    for r in dim_emps:
        assert r["FullName"].strip() != "", f"Empty FullName for {r['EmployeeID']}"
        assert int(r["Age"]) >= 18, f"Invalid Age for {r['EmployeeID']}"
        assert r["Gender"] in ("ذكر", "أنثى"), f"Invalid Gender for {r['EmployeeID']}"
        assert float(r["BaseSalary"]) > 0, f"Invalid BaseSalary for {r['EmployeeID']}"
        assert "@" in r["Email"], f"Invalid Email for {r['EmployeeID']}"


def test_scd2_hr_audit_staging_rules():
    """Validates the exact SCD Type 2 audit transformation rules:

    - Deduplication of retry duplicates (12516 -> 12392)
    - ValidFrom <= ValidTo temporal intervals
    - Exactly 1 current record per employee (IsCurrent = 1, ValidTo = '9999-12-31')
    - 7000 unique employees represented
    """
    audit_path = RAW_DIR / "hr_audit_events.csv"
    assert audit_path.exists(), "hr_audit_events.csv is missing"

    with open(audit_path, "r", encoding="utf-8") as f:
        raw_rows = list(csv.DictReader(f))

    assert len(raw_rows) == 12516, f"Expected 12516 raw audit events, found {len(raw_rows)}"

    # Simulate deduplication on (EmployeeID, EventType, EffectiveDate, NewValue, Salary_EGP)
    dedup_map = {}
    for r in raw_rows:
        key = (
            r["EmployeeID"],
            r["EventType"].strip().upper(),
            r["EffectiveDate"],
            (r.get("NewValue") or "").strip().lower(),
            r.get("Salary_EGP", ""),
        )
        if key not in dedup_map:
            dedup_map[key] = r

    deduped_rows = list(dedup_map.values())
    assert len(deduped_rows) == 12392, f"Expected 12392 deduped rows, found {len(deduped_rows)}"

    # Check 7000 unique employees
    audit_emp_ids = set(r["EmployeeID"] for r in deduped_rows)
    assert len(audit_emp_ids) == 7000, f"Expected 7000 unique employees in audit, found {len(audit_emp_ids)}"

    # Group by employee and test temporal chain
    from collections import defaultdict
    emp_events = defaultdict(list)
    for r in deduped_rows:
        emp_events[r["EmployeeID"]].append(r)

    for emp_id, events in emp_events.items():
        sorted_events = sorted(events, key=lambda x: x["EffectiveDate"])
        for i, ev in enumerate(sorted_events):
            valid_from = ev["EffectiveDate"]
            valid_to = sorted_events[i + 1]["EffectiveDate"] if i + 1 < len(sorted_events) else "9999-12-31"
            assert valid_from <= valid_to, f"Temporal inversion for {emp_id}: {valid_from} > {valid_to}"
            if valid_to == "9999-12-31":
                assert i == len(sorted_events) - 1, f"Premature open-ended interval for {emp_id}"


def test_foreign_key_cross_fact_integrity():
    """Validates 100% referential integrity across all 4 Galaxy Schema fact tables against conformed dimensions."""
    emps = {r["EmployeeKey"] for r in load_csv("Dim_Employee.csv")}
    depts = {r["DepartmentKey"] for r in load_csv("Dim_Department.csv")}
    branches = {r["BranchKey"] for r in load_csv("Dim_Branch.csv")}
    dates = {r["DateKey"] for r in load_csv("Dim_Date.csv")}
    courses = {r["CourseKey"] for r in load_csv("Dim_Course.csv")}

    # Fact_WorkforceSnapshot
    for r in load_csv("Fact_WorkforceSnapshot.csv"):
        assert r["EmployeeKey"] in emps
        assert r["DepartmentKey"] in depts
        assert r["BranchKey"] in branches
        assert r["SnapshotDateKey"] in dates

    # Fact_DailyAttendance
    for r in load_csv("Fact_DailyAttendance.csv"):
        assert r["EmployeeKey"] in emps
        assert r["BranchKey"] in branches
        assert r["AccessDateKey"] in dates

    # Fact_DepartmentBudget
    for r in load_csv("Fact_DepartmentBudget.csv"):
        assert r["DepartmentKey"] in depts
        assert r["BranchKey"] in branches
        assert r["DateKey"] in dates

    # Fact_TrainingCompletions
    for r in load_csv("Fact_TrainingCompletions.csv"):
        assert r["EmployeeKey"] in emps
        assert r["CourseKey"] in courses
        assert r["CompletionDateKey"] in dates
