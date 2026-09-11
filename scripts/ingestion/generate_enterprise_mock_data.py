"""
Enterprise Human Capital & Operational Efficiency Diagnostics
Module: generate_enterprise_mock_data.py
Purpose: Generates realistic enterprise test datasets representing 5 integrated source systems.
Architecture: Galaxy Schema (Fact Constellation)
"""

import csv
import json
import os
import random
from datetime import datetime, timedelta, time
from pathlib import Path
from typing import List, Dict, Any

import sys

# Ensure UTF-8 stdout for Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# Reference Domains & Lookups
# -----------------------------------------------------------------------------
FIRST_NAMES_MALE = ["أحمد", "محمد", "محمود", "عمر", "علي", "خالد", "يوسف", "كريم", "مصطفى", "طارق", "حسام", "إبراهيم", "هاني", "سامح", "عمرو"]
FIRST_NAMES_FEMALE = ["سارة", "فاطمة", "مريم", "نور", "ياسمين", "منى", "رنا", "هبة", "آية", "دينا", "شيرين", "مي", "ندى", "سلمى", "هدى"]
LAST_NAMES = ["السيد", "حسن", "إبراهيم", "علي", "محمود", "خليل", "عثمان", "مصطفى", "الشريف", "عبد الرحمن", "منصور", "جاد", "سليمان", "فهمي", "شحاتة"]

DEPARTMENTS = [
    "الموارد البشرية",
    "تقنية المعلومات",
    "المالية والمحاسبة",
    "المبيعات والتسويق",
    "العمليات واللوجستيات",
    "خدمة العملاء",
    "الشؤون القانونية",
]

BRANCHES = [
    "فرع المعادي",
    "فرع مدينة نصر",
    "فرع التجمع الخامس",
    "فرع المهندسين",
    "فرع الإسكندرية - سموحة",
    "فرع أسيوط",
    "فرع المنصورة",
]

JOB_ROLES_BY_DEPT = {
    "الموارد البشرية": ["أخصائي موارد بشرية", "مسؤول توظيف", "مدير الموارد البشرية", "منسق تدريب", "أخصائي شؤون العاملين"],
    "تقنية المعلومات": ["مهندس برمجيات", "مهندس بيانات", "مسؤول نظم وشبكات", "محلل أمن سيبراني", "مدير تقنية المعلومات", "أخصائي دعم فني"],
    "المالية والمحاسبة": ["محاسب أول", "محلل مالي", "محاسب تكاليف", "مراجع داخلي", "مدير مالي"],
    "المبيعات والتسويق": ["مسؤول مبيعات أول", "مسؤول تسويق رقمي", "أخصائي تطوير أعمال", "مدير مبيعات", "ممثل مبيعات"],
    "العمليات واللوجستيات": ["مشرف عمليات", "أخصائي سلاسل إمداد", "مدير العمليات", "منسق شحن ولوجستيات"],
    "خدمة العملاء": ["ممثل خدمة عملاء", "مشرف جودة الخدمة", "أخصائي تجربة العملاء", "مدير خدمة العملاء"],
    "الشؤون القانونية": ["مستشار قانوني", "أخصائي عقود وتوافق", "محامي شركات", "مدير الشؤون القانونية"],
}

CONTRACT_TYPES = ["دوام كامل (حضوري)", "هجين", "عن بعد"]
MARITAL_STATUSES = ["أعزب", "متزوج", "مطلق", "أرمل"]

LMS_COURSES = [
    {"CourseID": "CRS-TECH-01", "CourseName": "Power BI & Enterprise DAX Modeling", "SkillDomain": "Tech", "Cost": 4500.0},
    {"CourseID": "CRS-TECH-02", "CourseName": "Advanced SQL & Modern Data Warehousing", "SkillDomain": "Tech", "Cost": 5200.0},
    {"CourseID": "CRS-TECH-03", "CourseName": "Python for Data Engineering & Analytics", "SkillDomain": "Tech", "Cost": 6000.0},
    {"CourseID": "CRS-TECH-04", "CourseName": "Cloud Architecture & Cybersecurity Fundamentals", "SkillDomain": "Tech", "Cost": 7500.0},
    {"CourseID": "CRS-LEAD-01", "CourseName": "Strategic People Leadership & Coaching", "SkillDomain": "Leadership", "Cost": 8000.0},
    {"CourseID": "CRS-LEAD-02", "CourseName": "Operational Excellence & Lean Six Sigma", "SkillDomain": "Leadership", "Cost": 9500.0},
    {"CourseID": "CRS-SOFT-01", "CourseName": "Executive Negotiation & Conflict Resolution", "SkillDomain": "Soft Skills", "Cost": 3200.0},
    {"CourseID": "CRS-SOFT-02", "CourseName": "Data-Driven Decision Making & Storytelling", "SkillDomain": "Soft Skills", "Cost": 3800.0},
    {"CourseID": "CRS-COMP-01", "CourseName": "Enterprise Labor Law & Compliance 2026", "SkillDomain": "Compliance", "Cost": 2500.0},
    {"CourseID": "CRS-COMP-02", "CourseName": "Information Governance & GDPR/Data Protection", "SkillDomain": "Compliance", "Cost": 3000.0},
]


def generate_core_employees(num_records: int = 7000) -> List[Dict[str, Any]]:
    """Generates 7,000 employee records matching the Arabic schema of employees_data_7000.tmdl"""
    print(f"[*] Generating {num_records} Core HR Employee master records...")
    employees = []
    base_start_date = datetime(2015, 1, 1)
    end_date = datetime(2026, 2, 1)
    total_days_range = (end_date - base_start_date).days

    for i in range(1, num_records + 1):
        emp_id = f"EMP-{i:05d}"
        is_female = random.random() < 0.38
        first_name = random.choice(FIRST_NAMES_FEMALE if is_female else FIRST_NAMES_MALE)
        last_name = random.choice(LAST_NAMES)
        family_name = random.choice(LAST_NAMES)
        full_name = f"{first_name} {last_name} {family_name}"
        gender = "أنثى" if is_female else "ذكر"
        age = random.randint(22, 60)

        dept = random.choice(DEPARTMENTS)
        branch = random.choice(BRANCHES)
        job_role = random.choice(JOB_ROLES_BY_DEPT[dept])

        # Tenure calculation
        hire_day_offset = random.randint(0, total_days_range)
        hire_date = base_start_date + timedelta(days=hire_day_offset)
        tenure_years = round((end_date - hire_date).days / 365.25, 2)

        # Realistic Base Salary in EGP with deliberate salary compression scenario
        base_pay_scale = {
            "أخصائي": 12000.0,
            "مسؤول": 14000.0,
            "منسق": 11000.0,
            "محاسب": 15000.0,
            "مهندس": 22000.0,
            "محلل": 18000.0,
            "مشرف": 25000.0,
            "مدير": 45000.0,
            "مستشار": 50000.0,
            "محامي": 20000.0,
            "ممثل": 10000.0,
        }
        role_prefix = job_role.split()[0]
        base_salary = base_pay_scale.get(role_prefix, 14000.0) * random.uniform(0.85, 1.35)

        # Inject realistic salary compression:
        # Long-tenured employees (tenure > 4 years) sometimes received minimal raises,
        # whereas brand new hires (tenure < 1 yr) entered at inflated market rates!
        if tenure_years > 4.0 and random.random() < 0.28:
            base_salary = base_salary * 0.90  # Compressed salary
        elif tenure_years <= 1.0 and random.random() < 0.40:
            base_salary = base_salary * 1.30  # Inflated new-hire market rate

        base_salary = round(base_salary, 2)
        contract = random.choices(CONTRACT_TYPES, weights=[0.60, 0.30, 0.10])[0]
        perf_score = round(random.uniform(2.10, 4.95), 2)
        marital_status = random.choice(MARITAL_STATUSES)
        email_clean = f"emp{i}.{first_name}@{dept.replace(' ', '')}.enterprise.eg"

        emp_record = {
            "الاسم": full_name,
            "الرقم التعريفي": emp_id,
            "السن": age,
            "الجنس": gender,
            "المسمى الوظيفي": job_role,
            "القسم": dept,
            "الفرع": branch,
            "تاريخ التعيين": hire_date.strftime("%Y-%m-%d"),
            "الراتب الأساسي": base_salary,
            "العملة": "EGP",
            "نوع العقد": contract,
            "تقييم الأداء السنوي": perf_score,
            "الحالة الاجتماعية": marital_status,
            "البريد الإلكتروني": email_clean,
        }
        employees.append(emp_record)

    return employees


def generate_attendance_badge_logs(employees: List[Dict[str, Any]], num_days: int = 45) -> List[Dict[str, Any]]:
    """
    Generates IoT daily badge logs with deliberate real-world challenges:
    - Missing clock-outs (forgotten badges)
    - Night shifts crossing midnight
    - Ghost workers with 0 access events in 60+ days
    - Contract violation records
    """
    print(f"[*] Generating Daily IoT Badge Access Logs ({num_days} workdays)...")
    logs = []
    end_date = datetime(2026, 2, 28)
    
    # Designate 25 specific employees as "Ghost Workers" (on payroll but zero physical/virtual access)
    ghost_worker_ids = set(f"EMP-{i:05d}" for i in range(101, 126))

    # Sample an active active cohort for daily simulation
    sampled_employees = [e for e in employees if e["الرقم التعريفي"] not in ghost_worker_ids]

    for day_idx in range(num_days):
        current_day = end_date - timedelta(days=day_idx)
        # Skip weekends (Friday & Saturday in Egypt)
        if current_day.weekday() in (4, 5):
            continue

        for emp in sampled_employees[:800]: # Generate solid multi-thousand batch
            emp_id = emp["الرقم التعريفي"]
            contract = emp["نوع العقد"]
            branch = emp["الفرع"]

            # Determine actual presence mode
            is_contract_onsite = (contract == "دوام كامل (حضوري)")
            # Policy breach injection: Onsite worker logging remote
            if is_contract_onsite and random.random() < 0.15:
                declared_mode = "Remote"
                building_id = "REMOTE_GATE"
            elif contract == "هجين":
                declared_mode = "Remote" if random.random() < 0.50 else "On-site"
                building_id = "REMOTE_GATE" if declared_mode == "Remote" else f"BLD-{branch[-3:]}"
            else:
                declared_mode = "On-site"
                building_id = f"BLD-{branch[-3:]}"

            # Shift simulation
            is_night_shift = random.random() < 0.05
            is_missing_clock_out = random.random() < 0.08

            if is_night_shift:
                check_in = time(random.randint(21, 23), random.randint(0, 59))
                check_out = None if is_missing_clock_out else time(random.randint(5, 7), random.randint(0, 59))
            else:
                check_in = time(random.randint(7, 9), random.randint(0, 59))
                check_out = None if is_missing_clock_out else time(random.randint(16, 18), random.randint(0, 59))

            log_entry = {
                "EmployeeID": emp_id,
                "AccessDate": current_day.strftime("%Y-%m-%d"),
                "CheckInTime": check_in.strftime("%H:%M:%S") if check_in else None,
                "CheckOutTime": check_out.strftime("%H:%M:%S") if check_out else None,
                "BuildingID": building_id,
                "DeclaredWorkMode": declared_mode,
            }
            logs.append(log_entry)

    return logs


def generate_exit_attrition_records(employees: List[Dict[str, Any]], num_exits: int = 350) -> List[Dict[str, Any]]:
    """Generates HR Attrition & Exit Audit records with voluntary/involuntary breakdown."""
    print(f"[*] Generating {num_exits} HR Exit & Attrition Audit records...")
    exit_records = []
    exit_reasons = ["Compensation & Market Rate", "Career Growth", "Direct Management", "Relocation", "Burnout & Overwork", "Personal Reasons"]
    separated_sample = random.sample(employees, min(num_exits, len(employees)))

    for emp in separated_sample:
        emp_id = emp["الرقم التعريفي"]
        exit_type = "Voluntary" if random.random() < 0.78 else "Involuntary"
        reason = random.choice(exit_reasons) if exit_type == "Voluntary" else "Performance & Reorganization"
        exit_date = datetime(2025, random.randint(1, 12), random.randint(1, 28))
        notice_date = exit_date - timedelta(days=random.randint(14, 45))
        rehire_eligible = (exit_type == "Voluntary" and reason != "Direct Management") or random.random() < 0.20

        exit_records.append({
            "EmployeeID": emp_id,
            "NoticeDate": notice_date.strftime("%Y-%m-%d"),
            "ExitDate": exit_date.strftime("%Y-%m-%d"),
            "ExitType": exit_type,
            "PrimaryExitReason": reason,
            "LastPerformanceScore": emp["تقييم الأداء السنوي"],
            "RehireEligible": 1 if rehire_eligible else 0,
            "SeparationSalary": emp["الراتب الأساسي"],
            "SeparationBranch": emp["الفرع"],
        })
    return exit_records


def generate_fpa_department_budgets() -> List[Dict[str, Any]]:
    """Generates messy horizontal FP&A budgets with branch spelling variations."""
    print("[*] Generating Messy Horizontal FP&A Budget records...")
    budget_rows = []
    years = [2025, 2026]
    branch_variations = {
        "فرع المعادي": ["فرع المعادي", "المعادى", "القاهرة - المعادي"],
        "فرع مدينة نصر": ["فرع مدينة نصر", "مدينة نصر - الرئيسي"],
        "فرع التجمع الخامس": ["فرع التجمع الخامس", "التجمع", "القاهرة الجديدة"],
        "فرع المهندسين": ["فرع المهندسين", "الجيزة - المهندسين"],
        "فرع الإسكندرية - سموحة": ["فرع الإسكندرية - سموحة", "اسكندرية سموحة", "الإسكندرية"],
        "فرع أسيوط": ["فرع أسيوط", "اسيوط صعيد مصر"],
        "فرع المنصورة": ["فرع المنصورة", "المنصورة دقهلية"],
    }

    for year in years:
        for dept in DEPARTMENTS:
            for canonical_branch, variations in branch_variations.items():
                raw_branch = random.choice(variations)
                base_hc = random.randint(40, 180)
                base_salary_per_head = random.uniform(16000, 24000)

                q1_hc = base_hc
                q2_hc = base_hc + random.randint(-5, 10)
                q3_hc = q2_hc + random.randint(-5, 12)
                q4_hc = q3_hc + random.randint(-5, 15)

                q1_b = round(q1_hc * base_salary_per_head * 3, 2)
                q2_b = round(q2_hc * base_salary_per_head * 3 * 1.03, 2)
                q3_b = round(q3_hc * base_salary_per_head * 3 * 1.05, 2)
                q4_b = round(q4_hc * base_salary_per_head * 3 * 1.07, 2)
                ot_allowance = round(q1_b * 0.08, 2)

                budget_rows.append({
                    "FiscalYear": year,
                    "Department": dept,
                    "RawBranch": raw_branch,
                    "Q1_Budget_EGP": q1_b,
                    "Q2_Budget_EGP": q2_b,
                    "Q3_Budget_EGP": q3_b,
                    "Q4_Budget_EGP": q4_b,
                    "Q1_Headcount": q1_hc,
                    "Q2_Headcount": q2_hc,
                    "Q3_Headcount": q3_hc,
                    "Q4_Headcount": q4_hc,
                    "OvertimeAllowance_EGP": ot_allowance,
                })
    return budget_rows


def generate_lms_course_completions(employees: List[Dict[str, Any]], num_attempts: int = 4000) -> List[Dict[str, Any]]:
    """Generates transactional LMS completions with retakes and costs."""
    print(f"[*] Generating {num_attempts} LMS Training & Certification attempts...")
    attempts = []
    eligible_employees = random.sample(employees, min(2000, len(employees)))

    for _ in range(num_attempts):
        emp = random.choice(eligible_employees)
        emp_id = emp["الرقم التعريفي"]
        course = random.choice(LMS_COURSES)
        comp_date = datetime(2025, random.randint(1, 12), random.randint(1, 28))

        # Initial attempt might be a fail (< 70)
        is_first_pass = random.random() < 0.72
        score_1 = round(random.uniform(70.0, 98.5), 1) if is_first_pass else round(random.uniform(42.0, 68.0), 1)

        attempts.append({
            "EmployeeID": emp_id,
            "CourseID": course["CourseID"],
            "CourseName": course["CourseName"],
            "SkillDomain": course["SkillDomain"],
            "CompletionDate": comp_date.strftime("%Y-%m-%d"),
            "Score": score_1,
            "CertificationCost_EGP": course["Cost"],
        })

        # If failed, generate retake attempt
        if not is_first_pass and random.random() < 0.85:
            retake_date = comp_date + timedelta(days=random.randint(15, 60))
            attempts.append({
                "EmployeeID": emp_id,
                "CourseID": course["CourseID"],
                "CourseName": course["CourseName"],
                "SkillDomain": course["SkillDomain"],
                "CompletionDate": retake_date.strftime("%Y-%m-%d"),
                "Score": round(random.uniform(74.0, 96.0), 1),
                "CertificationCost_EGP": course["Cost"] * 0.50, # 50% re-exam fee
            })

    return attempts


def export_data():
    """Generates and writes all datasets to data/raw/"""
    # 1. Core Employees
    employees = generate_core_employees(7000)
    core_csv_path = RAW_DATA_DIR / "employees_core.csv"
    with open(core_csv_path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(employees[0].keys()))
        writer.writeheader()
        writer.writerows(employees)
    print(f"[OK] Saved Core HR data to {core_csv_path}")

    # 2. Daily Attendance Logs
    att_logs = generate_attendance_badge_logs(employees, num_days=30)
    att_json_path = RAW_DATA_DIR / "attendance_badge_logs.json"
    with open(att_json_path, mode="w", encoding="utf-8") as f:
        json.dump(att_logs, f, ensure_ascii=False, indent=2)
    print(f"[OK] Saved Daily Attendance Logs to {att_json_path}")

    # 3. Exit Attrition Records
    exits = generate_exit_attrition_records(employees, num_exits=350)
    exit_csv_path = RAW_DATA_DIR / "exit_attrition_records.csv"
    with open(exit_csv_path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(exits[0].keys()))
        writer.writeheader()
        writer.writerows(exits)
    print(f"[OK] Saved Exit Audit records to {exit_csv_path}")

    # 4. FP&A Budgets (CSV + XLSX if openpyxl available)
    budgets = generate_fpa_department_budgets()
    budget_csv_path = RAW_DATA_DIR / "fpa_department_budget_messy.csv"
    with open(budget_csv_path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(budgets[0].keys()))
        writer.writeheader()
        writer.writerows(budgets)
    print(f"[OK] Saved Messy Budget records to {budget_csv_path}")

    # Try saving as XLSX
    try:
        import openpyxl
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Department_Budget_Targets"
        headers = list(budgets[0].keys())
        ws.append(headers)
        for b in budgets:
            ws.append([b[h] for h in headers])
        xlsx_path = RAW_DATA_DIR / "fpa_department_budget_messy.xlsx"
        wb.save(xlsx_path)
        print(f"[OK] Saved Excel Workbook to {xlsx_path}")
    except Exception as e:
        print(f"[!] Excel export skipped: {e}")

    # 5. LMS Course Completions
    lms = generate_lms_course_completions(employees, num_attempts=2500)
    lms_csv_path = RAW_DATA_DIR / "lms_course_completions.csv"
    with open(lms_csv_path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(lms[0].keys()))
        writer.writeheader()
        writer.writerows(lms)
    print(f"[OK] Saved LMS Course Completions to {lms_csv_path}")

    print("\n[SUCCESS] All 5 Enterprise mock datasets generated successfully in data/raw/")


if __name__ == "__main__":
    export_data()
