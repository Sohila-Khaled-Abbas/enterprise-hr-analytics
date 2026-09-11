"""
Enterprise Human Capital & Operational Efficiency Diagnostics
Module: pipeline_runner.py
Purpose: End-to-end data pipeline orchestrator that ingests raw sources,
         applies heuristic cleansing & transformations, and outputs
         the production Galaxy Schema (Fact Constellation) dimensional model.
"""

import csv
import json
import os
import sys
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Dict, List, Any

# Ensure UTF-8 stdout on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

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

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def build_dim_date(start_year: int = 2024, end_year: int = 2026) -> List[Dict[str, Any]]:
    """Builds enterprise canonical date dimension table."""
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)
    delta = timedelta(days=1)

    records = []
    curr = start_date
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    while curr <= end_date:
        date_key = curr.year * 10000 + curr.month * 100 + curr.day
        weekday = curr.weekday() # 0 = Monday, 6 = Sunday
        # In Egypt / Middle East, Weekend is Friday (4) and Saturday (5)
        is_weekend = (weekday in (4, 5))
        is_working_day = not is_weekend
        quarter = (curr.month - 1) // 3 + 1

        records.append({
            "DateKey": date_key,
            "FullDate": curr.isoformat(),
            "DayNumberOfWeek": weekday + 1,
            "DayNameOfWeek": day_names[weekday],
            "DayNumberOfMonth": curr.day,
            "DayNumberOfYear": curr.timetuple().tm_yday,
            "MonthName": month_names[curr.month - 1],
            "MonthNumberOfYear": curr.month,
            "CalendarQuarter": quarter,
            "CalendarYear": curr.year,
            "FiscalQuarter": quarter,
            "FiscalYear": curr.year,
            "IsWeekend": 1 if is_weekend else 0,
            "IsWorkingDay": 1 if is_working_day else 0,
        })
        curr += delta

    return records


def run_pipeline():
    print("=================================================================")
    print("Enterprise Human Capital Pipeline: Executing Galaxy Schema Build")
    print("=================================================================")

    # 1. Load Raw Core HR
    core_path = RAW_DIR / "employees_core.csv"
    if not core_path.exists():
        raise FileNotFoundError(f"Missing core raw data at {core_path}. Run generate_enterprise_mock_data.py first.")

    with open(core_path, mode="r", encoding="utf-8-sig") as f:
        core_records = list(csv.DictReader(f))
    print(f"[OK] Loaded {len(core_records)} raw Core HR employee records.")

    # 2. Extract Conformed Dimensions: Dim_Department & Dim_Branch
    unique_depts = sorted(list(set(r["القسم"] for r in core_records if r.get("القسم"))))
    dim_dept = []
    dept_name_to_key = {}
    for idx, d_name in enumerate(unique_depts, start=1):
        dept_name_to_key[d_name] = idx
        dim_dept.append({
            "DepartmentKey": idx,
            "DepartmentID": f"DEPT-{idx:03d}",
            "DepartmentName": d_name,
            "Division": "Corporate Services",
            "CostCenterCode": f"CC-{idx * 100}",
        })

    unique_branches = sorted(list(set(r["الفرع"] for r in core_records if r.get("الفرع"))))
    dim_branch = []
    branch_name_to_key = {}
    regions_map = {
        "فرع المعادي": ("Greater Cairo", "Cairo"),
        "فرع مدينة نصر": ("Greater Cairo", "Cairo"),
        "فرع التجمع الخامس": ("Greater Cairo", "New Cairo"),
        "فرع المهندسين": ("Greater Cairo", "Giza"),
        "فرع الإسكندرية - سموحة": ("Alexandria & North", "Alexandria"),
        "فرع أسيوط": ("Upper Egypt", "Asyut"),
        "فرع المنصورة": ("Delta", "Mansoura"),
    }
    for idx, b_name in enumerate(unique_branches, start=1):
        branch_name_to_key[b_name] = idx
        reg, city = regions_map.get(b_name, ("Egypt", "Cairo"))
        dim_branch.append({
            "BranchKey": idx,
            "BranchID": f"BR-{idx:03d}",
            "BranchName": b_name,
            "CanonicalName": b_name,
            "Region": reg,
            "City": city,
            "Capacity": 250,
        })

    # 3. Extract Dim_Course from LMS completions
    lms_path = RAW_DIR / "lms_course_completions.csv"
    lms_records = []
    if lms_path.exists():
        with open(lms_path, mode="r", encoding="utf-8-sig") as f:
            lms_records = list(csv.DictReader(f))

    course_dict = {}
    dim_course = []
    course_id_to_key = {}
    for r in lms_records:
        cid = r["CourseID"]
        if cid not in course_dict:
            c_key = len(dim_course) + 1
            course_id_to_key[cid] = c_key
            course_dict[cid] = {
                "CourseKey": c_key,
                "CourseID": cid,
                "CourseName": r["CourseName"],
                "SkillDomain": r["SkillDomain"],
                "TargetCompetency": f"{r['SkillDomain']} Mastery",
                "EstimatedHours": 32.0,
            }
            dim_course.append(course_dict[cid])

    # 4. Build Dim_Date
    dim_date = build_dim_date(2024, 2026)

    # 5. Build Dim_Employee with Tenure and SCD-2
    dim_employee = []
    emp_id_to_key = {}
    today_date = date(2026, 3, 1)

    for idx, r in enumerate(core_records, start=1):
        emp_id = r["الرقم التعريفي"]
        emp_id_to_key[emp_id] = idx
        dept_key = dept_name_to_key.get(r["القسم"], 1)
        branch_key = branch_name_to_key.get(r["الفرع"], 1)

        dim_employee.append({
            "EmployeeKey": idx,
            "EmployeeID": emp_id,
            "FullName": r["الاسم"],
            "Age": int(r["السن"]),
            "Gender": r["الجنس"],
            "JobRole": r["المسمى الوظيفي"],
            "DepartmentKey": dept_key,
            "BranchKey": branch_key,
            "HireDate": r["تاريخ التعيين"],
            "BaseSalary": float(r["الراتب الأساسي"]),
            "Currency": r.get("العملة", "EGP"),
            "ContractType": r["نوع العقد"],
            "MaritalStatus": r["الحالة الاجتماعية"],
            "Email": r["البريد الإلكتروني"],
            "EffectiveDate": r["تاريخ التعيين"],
            "ExpiryDate": "9999-12-31",
            "IsCurrent": 1,
        })

    # 6. Build Fact_WorkforceSnapshot with Salary Compression & Percentiles
    # Pre-calculate tenure in years
    for emp in core_records:
        h_date = datetime.strptime(emp["تاريخ التعيين"], "%Y-%m-%d").date()
        tenure_days = (today_date - h_date).days
        emp["TenureYears"] = round(tenure_days / 365.25, 2)
        emp["TenureMonths"] = int(tenure_days // 30.4375)

    enriched_emps = calculate_salary_compression(core_records)
    snapshot_date_key = 20260228
    fact_workforce = []

    for idx, e in enumerate(enriched_emps, start=1):
        emp_id = e["الرقم التعريفي"]
        emp_key = emp_id_to_key.get(emp_id)
        if not emp_key:
            continue
        dept_key = dept_name_to_key.get(e["القسم"], 1)
        branch_key = branch_name_to_key.get(e["الفرع"], 1)

        fact_workforce.append({
            "SnapshotKey": idx,
            "SnapshotDateKey": snapshot_date_key,
            "EmployeeKey": emp_key,
            "DepartmentKey": dept_key,
            "BranchKey": branch_key,
            "BaseSalary": float(e["الراتب الأساسي"]),
            "AnnualPerformanceRating": float(e["تقييم الأداء السنوي"]),
            "TenureMonths": e["TenureMonths"],
            "TenureYears": e["TenureYears"],
            "SalaryPercentileInRole": e["SalaryPercentileInRole"],
            "IsSalaryCompressed": 1 if e["IsSalaryCompressed"] else 0,
            "EmploymentStatus": "Active",
        })

    # 7. Build Fact_DailyAttendance with Imputation
    att_path = RAW_DIR / "attendance_badge_logs.json"
    fact_attendance = []
    if att_path.exists():
        with open(att_path, mode="r", encoding="utf-8") as f:
            raw_att = json.load(f)

        for idx, log in enumerate(raw_att, start=1):
            emp_id = log["EmployeeID"]
            emp_key = emp_id_to_key.get(emp_id)
            if not emp_key:
                continue

            emp_ref = dim_employee[emp_key - 1]
            branch_key = emp_ref["BranchKey"]
            contract = emp_ref["ContractType"]

            imputed = impute_attendance_shift(log.get("CheckInTime"), log.get("CheckOutTime"))
            declared_mode = log.get("DeclaredWorkMode", "On-site")
            actual_mode = "Remote" if (log.get("BuildingID") == "REMOTE_GATE" or declared_mode == "Remote") else "On-site"

            # Contract Violation diagnostic
            is_contract_violation = (contract == "دوام كامل (حضوري)" and actual_mode == "Remote")

            acc_date = log["AccessDate"]
            date_key = int(acc_date.replace("-", ""))

            fact_attendance.append({
                "AttendanceKey": idx,
                "AccessDateKey": date_key,
                "EmployeeKey": emp_key,
                "BranchKey": branch_key,
                "CheckInTime": imputed["check_in"],
                "CheckOutTime": imputed["check_out"],
                "DurationHours": imputed["duration_hours"],
                "DeclaredWorkMode": declared_mode,
                "ActualWorkMode": actual_mode,
                "IsMissingClockOut": 1 if imputed["is_missing_clock_out"] else 0,
                "IsImputedClockOut": 1 if imputed["is_imputed_clock_out"] else 0,
                "IsNightShift": 1 if imputed["is_night_shift"] else 0,
                "IsContractViolation": 1 if is_contract_violation else 0,
            })

    # 8. Build Fact_DepartmentBudget (Unpivot + Branch Standardization)
    budget_path = RAW_DIR / "fpa_department_budget_messy.csv"
    fact_budget = []
    if budget_path.exists():
        with open(budget_path, mode="r", encoding="utf-8-sig") as f:
            raw_budgets = list(csv.DictReader(f))
        unpivoted_b = unpivot_quarterly_budgets(raw_budgets)

        for idx, b in enumerate(unpivoted_b, start=1):
            dept_key = dept_name_to_key.get(b["Department"], 1)
            b_key = branch_name_to_key.get(b["Branch"], 1)

            fact_budget.append({
                "BudgetKey": idx,
                "FiscalYear": b["FiscalYear"],
                "FiscalQuarter": b["FiscalQuarter"],
                "DateKey": b["DateKey"],
                "DepartmentKey": dept_key,
                "BranchKey": b_key,
                "BudgetedHeadcount": b["BudgetedHeadcount"],
                "AllocatedSalaryBudget_EGP": b["AllocatedSalaryBudget_EGP"],
                "OvertimeAllowance_EGP": b["OvertimeAllowance_EGP"],
            })

    # 9. Build Fact_TrainingCompletions with Deduplication
    fact_training = []
    if lms_records:
        deduped_lms = deduplicate_lms_attempts(lms_records)
        for idx, attempt in enumerate(deduped_lms, start=1):
            emp_key = emp_id_to_key.get(attempt["EmployeeID"])
            c_key = course_id_to_key.get(attempt["CourseID"])
            if not emp_key or not c_key:
                continue

            comp_date = attempt["CompletionDate"]
            date_key = int(comp_date.replace("-", ""))

            fact_training.append({
                "CompletionKey": idx,
                "CompletionDateKey": date_key,
                "EmployeeKey": emp_key,
                "CourseKey": c_key,
                "AttemptNumber": attempt["AttemptNumber"],
                "Score": float(attempt["Score"]),
                "IsPassed": 1 if attempt["IsPassed"] else 0,
                "CertificationCost_EGP": float(attempt["CertificationCost_EGP"]),
                "IsHighestScoreAttempt": 1 if attempt["IsHighestScoreAttempt"] else 0,
            })

    # 10. Persist All Dimensional Tables to data/processed/
    def save_csv(data: List[Dict[str, Any]], filename: str):
        if not data:
            return
        p = PROCESSED_DIR / filename
        with open(p, mode="w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
            writer.writeheader()
            writer.writerows(data)
        print(f"[OK] Wrote {len(data):6d} rows -> {p.name}")

    print("\n--- Saving Conformed Dimensions ---")
    save_csv(dim_dept, "Dim_Department.csv")
    save_csv(dim_branch, "Dim_Branch.csv")
    save_csv(dim_course, "Dim_Course.csv")
    save_csv(dim_date, "Dim_Date.csv")
    save_csv(dim_employee, "Dim_Employee.csv")

    print("\n--- Saving Galaxy Schema Fact Constellation Tables ---")
    save_csv(fact_workforce, "Fact_WorkforceSnapshot.csv")
    save_csv(fact_attendance, "Fact_DailyAttendance.csv")
    save_csv(fact_budget, "Fact_DepartmentBudget.csv")
    save_csv(fact_training, "Fact_TrainingCompletions.csv")

    print("\n=================================================================")
    print("[SUCCESS] Galaxy Schema Data Mart transformation complete!")
    print("=================================================================")


if __name__ == "__main__":
    run_pipeline()
