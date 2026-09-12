"""
Enterprise Human Capital & Operational Efficiency Diagnostics
Module: data_cleaners.py
Purpose: Reusable transformation, heuristic imputation, and data reconciliation utilities.
Architecture: Galaxy Schema (Fact Constellation)
"""

from datetime import datetime, timedelta, time
import math
import re
from typing import Dict, List, Optional, Tuple, Any


def parse_time(time_str: Optional[str]) -> Optional[time]:
    """Parse time string in HH:MM or HH:MM:SS format."""
    if not time_str or time_str.strip() == "":
        return None
    time_str = time_str.strip()
    for fmt in ("%H:%M:%S", "%H:%M", "%I:%M:%S %p", "%I:%M %p"):
        try:
            return datetime.strptime(time_str, fmt).time()
        except ValueError:
            pass
    return None


def impute_attendance_shift(
    check_in_str: Optional[str],
    check_out_str: Optional[str],
    median_shift_hours: float = 8.0,
) -> Dict[str, Any]:
    """
    Cleanses daily check-in/out timestamps and applies heuristic imputation:
    1. Detects missing clock-out and imputes checkout using median shift duration.
    2. Detects night shifts (checkout earlier than checkin) and calculates overnight duration.
    3. Normalizes duration in decimal hours.
    """
    t_in = parse_time(check_in_str)
    t_out = parse_time(check_out_str)

    if t_in is None and t_out is None:
        return {
            "check_in": None,
            "check_out": None,
            "duration_hours": 0.0,
            "is_missing_clock_out": False,
            "is_imputed_clock_out": False,
            "is_night_shift": False,
        }

    # Case 1: Missing Clock-in (Default to standard 09:00 if check-out exists)
    if t_in is None and t_out is not None:
        dummy_date = datetime(2026, 1, 1, t_out.hour, t_out.minute, t_out.second)
        imputed_in = (dummy_date - timedelta(hours=median_shift_hours)).time()
        return {
            "check_in": imputed_in.strftime("%H:%M:%S"),
            "check_out": t_out.strftime("%H:%M:%S"),
            "duration_hours": round(median_shift_hours, 2),
            "is_missing_clock_out": False,
            "is_imputed_clock_out": True,
            "is_night_shift": False,
        }

    # Case 2: Missing Clock-out (Night shift or forgotten sign-out)
    if t_in is not None and t_out is None:
        dummy_date = datetime(2026, 1, 1, t_in.hour, t_in.minute, t_in.second)
        imputed_out = (dummy_date + timedelta(hours=median_shift_hours)).time()
        return {
            "check_in": t_in.strftime("%H:%M:%S"),
            "check_out": imputed_out.strftime("%H:%M:%S"),
            "duration_hours": round(median_shift_hours, 2),
            "is_missing_clock_out": True,
            "is_imputed_clock_out": True,
            "is_night_shift": False,
        }

    # Case 3: Both timestamps exist
    dt_in = datetime(2026, 1, 1, t_in.hour, t_in.minute, t_in.second)
    if t_out < t_in:
        # Night shift crossing midnight
        dt_out = datetime(2026, 1, 2, t_out.hour, t_out.minute, t_out.second)
        duration = (dt_out - dt_in).total_seconds() / 3600.0
        return {
            "check_in": t_in.strftime("%H:%M:%S"),
            "check_out": t_out.strftime("%H:%M:%S"),
            "duration_hours": round(duration, 2),
            "is_missing_clock_out": False,
            "is_imputed_clock_out": False,
            "is_night_shift": True,
        }
    else:
        duration = (datetime(2026, 1, 1, t_out.hour, t_out.minute, t_out.second) - dt_in).total_seconds() / 3600.0
        return {
            "check_in": t_in.strftime("%H:%M:%S"),
            "check_out": t_out.strftime("%H:%M:%S"),
            "duration_hours": round(duration, 2),
            "is_missing_clock_out": False,
            "is_imputed_clock_out": False,
            "is_night_shift": False,
        }


# Canonical branch lookup dictionary matching the 14 branches in employees_data_7000.txt
CANONICAL_BRANCH_MAP = {
    "المعادي": "القاهرة - المعادي",
    "المعادى": "القاهرة - المعادي",
    "التجمع": "القاهرة - التجمع الخامس",
    "القاهرة الجديدة": "القاهرة - التجمع الخامس",
    "مصر الجديدة": "القاهرة - مصر الجديدة",
    "القرية الذكية": "القاهرة - القرية الذكية",
    "Smart Village": "القاهرة - القرية الذكية",
    "الدقي": "الجيزة - الدقي",
    "أكتوبر": "الجيزة - 6 أكتوبر",
    "6 أكتوبر": "الجيزة - 6 أكتوبر",
    "الشيخ زايد": "الجيزة - الشيخ زايد",
    "زايد": "الجيزة - الشيخ زايد",
    "سموحة": "الإسكندرية - سموحة",
    "لوران": "الإسكندرية - لوران",
    "المنصورة": "الدقهلية - المنصورة",
    "طنطا": "الغربية - طنطا",
    "دمياط": "دمياط - دمياط الجديدة",
    "بورسعيد": "بورسعيد - الشرق",
    "الشرق": "بورسعيد - الشرق",
    "أسيوط": "أسيوط - أسيوط الجديدة",
    "اسيوط": "أسيوط - أسيوط الجديدة",
}


def standardize_branch_name(raw_branch: str) -> str:
    """
    Standardizes messy/typographical branch variations in FP&A spreadsheets
    to canonical Dim_Branch keys.
    """
    if not raw_branch:
        return "القاهرة - المعادي"

    cleaned = raw_branch.strip()
    for keyword, canonical in CANONICAL_BRANCH_MAP.items():
        if keyword in cleaned:
            return canonical
    return cleaned


def unpivot_quarterly_budgets(wide_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Unpivots horizontal FP&A quarterly budget tables into normalized rows:
    Grain: (FiscalYear, FiscalQuarter, Department, StandardizedBranch).
    """
    unpivoted = []
    for row in wide_rows:
        year = int(row.get("FiscalYear", 2026))
        dept = row.get("Department", "General")
        raw_branch = row.get("RawBranch", row.get("Branch", "فرع المعادي"))
        branch = standardize_branch_name(raw_branch)
        total_ot = float(row.get("OvertimeAllowance_EGP", 0.0) or 0.0)
        quarterly_ot = round(total_ot / 4.0, 2)

        for q in range(1, 5):
            hc_key = f"Q{q}_Headcount"
            bg_key = f"Q{q}_Budget_EGP"
            headcount = row.get(hc_key)
            budget = row.get(bg_key)

            if headcount is not None or budget is not None:
                # Calculate start date key: YYYY0101, YYYY0401, YYYY0701, YYYY1001
                start_months = {1: "0101", 2: "0401", 3: "0701", 4: "1001"}
                date_key = int(f"{year}{start_months[q]}")

                unpivoted.append({
                    "FiscalYear": year,
                    "FiscalQuarter": q,
                    "DateKey": date_key,
                    "Department": dept,
                    "Branch": branch,
                    "BudgetedHeadcount": int(headcount or 0),
                    "AllocatedSalaryBudget_EGP": float(budget or 0.0),
                    "OvertimeAllowance_EGP": quarterly_ot,
                })
    return unpivoted


def deduplicate_lms_attempts(attempts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Ranks repeated certification attempts by employee and course.
    Assigns sequential AttemptNumber and flags IsHighestScoreAttempt = True.
    """
    # Group by (EmployeeID, CourseID)
    grouped: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    for a in attempts:
        key = (a["EmployeeID"], a["CourseID"])
        grouped.setdefault(key, []).append(a)

    processed = []
    for key, records in grouped.items():
        # Sort chronologically for attempt number
        records_chrono = sorted(records, key=lambda x: x.get("CompletionDate", ""))
        for idx, rec in enumerate(records_chrono, start=1):
            rec["AttemptNumber"] = idx

        # Find highest score attempt
        highest_record = max(records, key=lambda x: (float(x.get("Score", 0.0)), x.get("CompletionDate", "")))
        for rec in records:
            rec["IsHighestScoreAttempt"] = (rec is highest_record)
            rec["IsPassed"] = float(rec.get("Score", 0.0)) >= 70.0
            processed.append(rec)

    return processed


def calculate_salary_compression(
    employees: List[Dict[str, Any]],
    benchmark_tenure_threshold_years: float = 3.0,
    new_hire_threshold_years: float = 1.0,
) -> List[Dict[str, Any]]:
    """
    Calculates salary percentiles within job roles and detects salary compression:
    Flags tenured employees (>= 3 yrs) earning below new-hire median in the same role.
    """
    # Group salaries by job role for new hires
    role_new_hire_salaries: Dict[str, List[float]] = {}
    role_all_salaries: Dict[str, List[float]] = {}

    for emp in employees:
        role = emp.get("JobRole", emp.get("المسمى الوظيفي", "Staff"))
        salary = float(emp.get("BaseSalary", emp.get("الراتب الأساسي", 0.0)))
        tenure = float(emp.get("TenureYears", 0.0))

        role_all_salaries.setdefault(role, []).append(salary)
        if tenure <= new_hire_threshold_years:
            role_new_hire_salaries.setdefault(role, []).append(salary)

    # Calculate medians
    role_new_hire_medians: Dict[str, float] = {}
    for role, salaries in role_new_hire_salaries.items():
        sorted_s = sorted(salaries)
        n = len(sorted_s)
        mid = n // 2
        role_new_hire_medians[role] = (sorted_s[mid] if n % 2 != 0 else (sorted_s[mid - 1] + sorted_s[mid]) / 2.0)

    # Calculate percentiles and compression flags
    enriched = []
    for emp in employees:
        role = emp.get("JobRole", emp.get("المسمى الوظيفي", "Staff"))
        salary = float(emp.get("BaseSalary", emp.get("الراتب الأساسي", 0.0)))
        tenure = float(emp.get("TenureYears", 0.0))
        salaries = sorted(role_all_salaries.get(role, [salary]))

        # Percentile rank: rank / (N - 1)
        if len(salaries) > 1:
            rank = sum(1 for s in salaries if s < salary)
            percentile = rank / (len(salaries) - 1)
        else:
            percentile = 0.5

        new_hire_med = role_new_hire_medians.get(role, 0.0)
        is_compressed = (tenure >= benchmark_tenure_threshold_years and salary < new_hire_med)

        emp_copy = dict(emp)
        emp_copy["SalaryPercentileInRole"] = round(percentile, 4)
        emp_copy["IsSalaryCompressed"] = is_compressed
        emp_copy["NewHireMedianSalary"] = round(new_hire_med, 2)
        enriched.append(emp_copy)

    return enriched
