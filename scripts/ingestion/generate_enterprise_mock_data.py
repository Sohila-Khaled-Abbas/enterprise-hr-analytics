"""
Enterprise Human Capital & Operational Efficiency Diagnostics
Module: generate_enterprise_mock_data.py
Purpose: Generates and synchronizes all 5 enterprise source system datasets
         based on the authoritative master employee data in data/raw/employees_data_7000.txt.
"""

import csv
import json
import os
import random
from datetime import datetime, time, timedelta
from pathlib import Path
from typing import Any, Dict, List

# Reproducibility seed
random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# Canonical Reference Domains from employees_data_7000.txt
# -----------------------------------------------------------------------------
CANONICAL_DEPARTMENTS = [
    "الإدارة المالية",
    "التسويق والمبيعات",
    "العمليات وسلاسل الإمداد",
    "الموارد البشرية",
    "تكنولوجيا المعلومات",
    "خدمة العملاء والعمليات المساندة",
]

CANONICAL_BRANCHES = [
    "أسيوط - أسيوط الجديدة",
    "الإسكندرية - سموحة",
    "الإسكندرية - لوران",
    "الجيزة - 6 أكتوبر",
    "الجيزة - الدقي",
    "الجيزة - الشيخ زايد",
    "الدقهلية - المنصورة",
    "الغربية - طنطا",
    "القاهرة - التجمع الخامس",
    "القاهرة - القرية الذكية",
    "القاهرة - المعادي",
    "القاهرة - مصر الجديدة",
    "بورسعيد - الشرق",
    "دمياط - دمياط الجديدة",
]

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


def load_core_employees_from_txt() -> List[Dict[str, Any]]:
    """Loads and parses the true 7,000 master employees from employees_data_7000.txt."""
    txt_path = RAW_DATA_DIR / "employees_data_7000.txt"
    if not txt_path.exists():
        raise FileNotFoundError(f"Missing master employee file at {txt_path}")

    print(f"[*] Loading 7,000 Core HR Employee master records from {txt_path}...")
    employees = []
    current: Dict[str, str] = {}
    with open(txt_path, mode="r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line == "------":
                if current:
                    employees.append(current)
                    current = {}
            elif " : " in line:
                k, v = line.split(" : ", 1)
                current[k.strip()] = v.strip()
        if current:
            employees.append(current)

    formatted_employees: List[Dict[str, Any]] = []
    for emp in employees:
        formatted_employees.append({
            "الاسم": emp.get("الاسم", ""),
            "الرقم التعريفي": emp.get("الرقم التعريفي", ""),
            "السن": int(emp.get("السن", 30)),
            "الجنس": emp.get("الجنس", "ذكر"),
            "المسمى الوظيفي": emp.get("المسمى الوظيفي", ""),
            "القسم": emp.get("القسم", ""),
            "الفرع": emp.get("الفرع", ""),
            "تاريخ التعيين": emp.get("تاريخ التعيين", "2020-01-01"),
            "الراتب الأساسي": float(emp.get("الراتب الأساسي", 15000.0)),
            "العملة": emp.get("العملة", "EGP"),
            "نوع العقد": emp.get("نوع العقد", "دوام كامل (حضوري)"),
            "تقييم الأداء السنوي": float(emp.get("تقييم الأداء السنوي", 3.0)),
            "الحالة الاجتماعية": emp.get("الحالة الاجتماعية", "أعزب"),
            "البريد الإلكتروني": emp.get("البريد الإلكتروني", ""),
        })

    print(f"[OK] Successfully loaded {len(formatted_employees)} master employee records ({formatted_employees[0]['الرقم التعريفي']} to {formatted_employees[-1]['الرقم التعريفي']}).")
    return formatted_employees


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
    ghost_worker_ids = set(employees[i]["الرقم التعريفي"] for i in range(100, 125))

    sampled_employees = [e for e in employees if e["الرقم التعريفي"] not in ghost_worker_ids]

    for day_idx in range(num_days):
        current_day = end_date - timedelta(days=day_idx)
        # Skip weekends (Friday & Saturday in Egypt)
        if current_day.weekday() in (4, 5):
            continue

        for emp in sampled_employees[:800]:
            emp_id = emp["الرقم التعريفي"]
            contract = emp["نوع العقد"]
            branch = emp["الفرع"]

            is_contract_onsite = ("حضوري" in contract)
            if is_contract_onsite and random.random() < 0.15:
                declared_mode = "Remote"
                building_id = "REMOTE_GATE"
            elif "هجين" in contract or "عن بعد" in contract:
                declared_mode = "Remote" if random.random() < 0.60 else "On-site"
                building_id = "REMOTE_GATE" if declared_mode == "Remote" else f"BLD-{branch[-4:]}"
            else:
                declared_mode = "On-site"
                building_id = f"BLD-{branch[-4:]}"

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
    """
    Generates HR Attrition & Exit Audit records strictly sampled from the 7,000 master employees,
    grounded directly in the diagnostic criteria documented in docs/business_diagnostics.md:
    1. Low performers (rating < 2.5) -> Involuntary terminations (Performance & Reorganization).
    2. High performers (rating >= 3.8) with salary compression / below role median -> Voluntary resignations (Compensation / Growth).
    3. Long-tenured employees (hired before 2021) -> Voluntary resignations (Burnout & Overwork).
    4. Branch distance / contract friction -> Voluntary resignations (Relocation).
    """
    print(f"[*] Generating {num_exits} HR Exit & Attrition Audit records grounded on employees_data_7000.txt...")
    import statistics
    from collections import defaultdict

    # Compute median salary per job role across the 7,000 master employees
    role_salaries = defaultdict(list)
    for e in employees:
        role_salaries[e["المسمى الوظيفي"]].append(float(e["الراتب الأساسي"]))
    role_medians = {r: statistics.median(s) for r, s in role_salaries.items()}

    # Cohort 1: Underperformers (< 2.5 rating) -> Involuntary exits
    underperformers = [e for e in employees if float(e["تقييم الأداء السنوي"]) < 2.5]
    sample_under = random.sample(underperformers, min(65, len(underperformers)))

    # Cohort 2: High performers with salary compression (< role median) -> Flight risk exits
    compressed_high_performers = [
        e for e in employees
        if float(e["تقييم الأداء السنوي"]) >= 3.8
        and float(e["الراتب الأساسي"]) < role_medians.get(e["المسمى الوظيفي"], 20000.0)
        and e not in sample_under
    ]
    sample_compressed = random.sample(compressed_high_performers, min(130, len(compressed_high_performers)))

    # Cohort 3: Veteran employees (hired before 2021) -> Burnout & Overwork
    veterans = [
        e for e in employees
        if e["تاريخ التعيين"] < "2021-01-01"
        and e not in sample_under and e not in sample_compressed
    ]
    sample_veterans = random.sample(veterans, min(80, len(veterans)))

    # Cohort 4: General pool for relocation and other voluntary exits
    remaining_pool = [
        e for e in employees
        if e not in sample_under and e not in sample_compressed and e not in sample_veterans
    ]
    sample_other = random.sample(remaining_pool, num_exits - (len(sample_under) + len(sample_compressed) + len(sample_veterans)))

    exit_records = []

    # Process underperformers
    for emp in sample_under:
        exit_date = datetime(2025, random.randint(1, 12), random.randint(1, 28))
        notice_date = exit_date - timedelta(days=random.randint(14, 30))
        exit_records.append({
            "EmployeeID": emp["الرقم التعريفي"],
            "NoticeDate": notice_date.strftime("%Y-%m-%d"),
            "ExitDate": exit_date.strftime("%Y-%m-%d"),
            "ExitType": "Involuntary",
            "PrimaryExitReason": "Performance & Reorganization",
            "LastPerformanceScore": float(emp["تقييم الأداء السنوي"]),
            "RehireEligible": 0,
            "SeparationSalary": float(emp["الراتب الأساسي"]),
            "SeparationBranch": emp["الفرع"],
        })

    # Process compressed high performers
    for emp in sample_compressed:
        exit_date = datetime(2025, random.randint(1, 12), random.randint(1, 28))
        notice_date = exit_date - timedelta(days=random.randint(21, 45))
        reason = random.choice(["Compensation & Market Rate", "Career Growth"])
        exit_records.append({
            "EmployeeID": emp["الرقم التعريفي"],
            "NoticeDate": notice_date.strftime("%Y-%m-%d"),
            "ExitDate": exit_date.strftime("%Y-%m-%d"),
            "ExitType": "Voluntary",
            "PrimaryExitReason": reason,
            "LastPerformanceScore": float(emp["تقييم الأداء السنوي"]),
            "RehireEligible": 1,
            "SeparationSalary": float(emp["الراتب الأساسي"]),
            "SeparationBranch": emp["الفرع"],
        })

    # Process veterans
    for emp in sample_veterans:
        exit_date = datetime(2025, random.randint(1, 12), random.randint(1, 28))
        notice_date = exit_date - timedelta(days=random.randint(21, 45))
        exit_records.append({
            "EmployeeID": emp["الرقم التعريفي"],
            "NoticeDate": notice_date.strftime("%Y-%m-%d"),
            "ExitDate": exit_date.strftime("%Y-%m-%d"),
            "ExitType": "Voluntary",
            "PrimaryExitReason": "Burnout & Overwork",
            "LastPerformanceScore": float(emp["تقييم الأداء السنوي"]),
            "RehireEligible": 1,
            "SeparationSalary": float(emp["الراتب الأساسي"]),
            "SeparationBranch": emp["الفرع"],
        })

    # Process other exits
    for emp in sample_other:
        exit_date = datetime(2025, random.randint(1, 12), random.randint(1, 28))
        notice_date = exit_date - timedelta(days=random.randint(14, 40))
        reason = random.choice(["Relocation", "Direct Management", "Personal Reasons"])
        rehire_ok = 1 if reason != "Direct Management" else 0
        exit_records.append({
            "EmployeeID": emp["الرقم التعريفي"],
            "NoticeDate": notice_date.strftime("%Y-%m-%d"),
            "ExitDate": exit_date.strftime("%Y-%m-%d"),
            "ExitType": "Voluntary",
            "PrimaryExitReason": reason,
            "LastPerformanceScore": float(emp["تقييم الأداء السنوي"]),
            "RehireEligible": rehire_ok,
            "SeparationSalary": float(emp["الراتب الأساسي"]),
            "SeparationBranch": emp["الفرع"],
        })

    # Shuffle to avoid ordered blocks
    random.shuffle(exit_records)
    print(f"[OK] Generated {len(exit_records)} diagnostic-grounded exit records.")
    return exit_records


def generate_fpa_department_budgets(employees: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generates messy horizontal FP&A budgets anchored directly on the actual employee counts
    and average salary per (Department, Branch) from employees_data_7000.txt.
    """
    print("[*] Generating Messy Horizontal FP&A Budget records anchored on employees_data_7000.txt...")
    from collections import defaultdict

    dept_branch_counts = defaultdict(int)
    dept_branch_salaries = defaultdict(list)
    for e in employees:
        key = (e["القسم"], e["الفرع"])
        dept_branch_counts[key] += 1
        dept_branch_salaries[key].append(float(e["الراتب الأساسي"]))

    budget_rows = []
    years = [2025, 2026]
    branch_variations = {
        "القاهرة - المعادي": ["القاهرة - المعادي", "فرع المعادي", "المعادى"],
        "القاهرة - التجمع الخامس": ["القاهرة - التجمع الخامس", "التجمع", "القاهرة الجديدة"],
        "القاهرة - مصر الجديدة": ["القاهرة - مصر الجديدة", "مصر الجديدة", "فرع مصر الجديدة"],
        "القاهرة - القرية الذكية": ["القاهرة - القرية الذكية", "القرية الذكية", "Smart Village"],
        "الجيزة - الدقي": ["الجيزة - الدقي", "الدقي", "فرع الدقي"],
        "الجيزة - 6 أكتوبر": ["الجيزة - 6 أكتوبر", "6 أكتوبر", "أكتوبر"],
        "الجيزة - الشيخ زايد": ["الجيزة - الشيخ زايد", "الشيخ زايد", "زايد"],
        "الإسكندرية - سموحة": ["الإسكندرية - سموحة", "اسكندرية سموحة", "الإسكندرية", "سموحة"],
        "الإسكندرية - لوران": ["الإسكندرية - لوران", "لوران", "الإسكندرية - فرع لوران"],
        "الدقهلية - المنصورة": ["الدقهلية - المنصورة", "المنصورة دقهلية", "المنصورة"],
        "الغربية - طنطا": ["الغربية - طنطا", "طنطا", "فرع طنطا"],
        "دمياط - دمياط الجديدة": ["دمياط - دمياط الجديدة", "دمياط", "دمياط الجديدة"],
        "بورسعيد - الشرق": ["بورسعيد - الشرق", "بورسعيد", "حي الشرق"],
        "أسيوط - أسيوط الجديدة": ["أسيوط - أسيوط الجديدة", "اسيوط صعيد مصر", "أسيوط"],
    }

    for year in years:
        for dept in CANONICAL_DEPARTMENTS:
            for canonical_branch, variations in branch_variations.items():
                raw_branch = random.choice(variations)
                
                # Use actual headcount and actual average salary from the 7,000 employees
                key = (dept, canonical_branch)
                actual_hc = dept_branch_counts.get(key, 50)
                salaries = dept_branch_salaries.get(key, [18000.0])
                avg_salary = sum(salaries) / len(salaries)

                # Realistic FP&A planning baseline:
                base_hc = actual_hc
                base_salary_per_head = avg_salary

                q1_hc = base_hc
                q2_hc = base_hc + random.randint(-1, 3)
                q3_hc = q2_hc + random.randint(0, 4)
                q4_hc = q3_hc + random.randint(0, 4)

                q1_b = round(q1_hc * base_salary_per_head * 3, 2)
                q2_b = round(q2_hc * base_salary_per_head * 3 * 1.02, 2)
                q3_b = round(q3_hc * base_salary_per_head * 3 * 1.04, 2)
                q4_b = round(q4_hc * base_salary_per_head * 3 * 1.06, 2)
                ot_allowance = round(q1_b * 0.05, 2)

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
    print(f"[OK] Generated {len(budget_rows)} realistic budget records grounded in master employee counts.")
    return budget_rows


def generate_lms_course_completions(employees: List[Dict[str, Any]], num_attempts: int = 3500) -> List[Dict[str, Any]]:
    """
    Generates transactional LMS completions with retakes sampled from the 7,000 master employees,
    targeting courses relevant to their actual department and job role.
    """
    print(f"[*] Generating {num_attempts} LMS Training & Certification attempts grounded on employees_data_7000.txt...")
    dept_course_map = {
        "تكنولوجيا المعلومات": ["CRS-TECH-01", "CRS-TECH-02", "CRS-TECH-03", "CRS-TECH-04"],
        "الموارد البشرية": ["CRS-COMP-01", "CRS-LEAD-01", "CRS-SOFT-01"],
        "الإدارة المالية": ["CRS-TECH-01", "CRS-TECH-02", "CRS-COMP-02"],
        "التسويق والمبيعات": ["CRS-SOFT-02", "CRS-SOFT-01", "CRS-TECH-01"],
        "خدمة العملاء والعمليات المساندة": ["CRS-SOFT-01", "CRS-LEAD-02", "CRS-COMP-01"],
        "العمليات وسلاسل الإمداد": ["CRS-LEAD-02", "CRS-LEAD-01", "CRS-TECH-01"],
    }
    course_by_id = {c["CourseID"]: c for c in LMS_COURSES}

    attempts = []
    eligible_employees = random.sample(employees, min(2200, len(employees)))

    for _ in range(num_attempts):
        emp = random.choice(eligible_employees)
        emp_id = emp["الرقم التعريفي"]
        dept = emp["القسم"]
        available_cids = dept_course_map.get(dept, ["CRS-SOFT-01", "CRS-LEAD-01"])
        course_id = random.choice(available_cids)
        course = course_by_id.get(course_id, LMS_COURSES[0])

        comp_date = datetime(2025, random.randint(1, 12), random.randint(1, 28))
        perf = float(emp["تقييم الأداء السنوي"])

        # High performers have higher pass rates
        if perf >= 4.0:
            is_fail = random.random() < 0.05
            score = round(random.uniform(82.0, 98.0), 1) if not is_fail else round(random.uniform(62.0, 68.0), 1)
        elif perf >= 3.0:
            is_fail = random.random() < 0.18
            score = round(random.uniform(72.0, 92.0), 1) if not is_fail else round(random.uniform(50.0, 68.0), 1)
        else:
            is_fail = random.random() < 0.45
            score = round(random.uniform(70.0, 84.0), 1) if not is_fail else round(random.uniform(42.0, 68.0), 1)

        attempts.append({
            "EmployeeID": emp_id,
            "CourseID": course["CourseID"],
            "CourseName": course["CourseName"],
            "SkillDomain": course["SkillDomain"],
            "CompletionDate": comp_date.strftime("%Y-%m-%d"),
            "Score": score,
            "CertificationCost_EGP": course["Cost"],
        })

        if is_fail and random.random() < 0.70:
            retake_date = comp_date + timedelta(days=random.randint(15, 60))
            retake_score = round(random.uniform(75.0, 95.0), 1)
            attempts.append({
                "EmployeeID": emp_id,
                "CourseID": course["CourseID"],
                "CourseName": course["CourseName"],
                "SkillDomain": course["SkillDomain"],
                "CompletionDate": retake_date.strftime("%Y-%m-%d"),
                "Score": retake_score,
                "CertificationCost_EGP": course["Cost"] * 0.50,
            })

    print(f"[OK] Generated {len(attempts)} LMS attempt records.")
    return attempts


def export_data():
    """Generates and writes all datasets to data/raw/ strictly based on employees_data_7000.txt"""
    # 1. Core Employees
    employees = load_core_employees_from_txt()
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

    # 3. Exit Attrition Records (350 exits strictly matching EMP-10001..EMP-17000)
    exits = generate_exit_attrition_records(employees, num_exits=350)
    exit_csv_path = RAW_DATA_DIR / "exit_attrition_records.csv"
    with open(exit_csv_path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(exits[0].keys()))
        writer.writeheader()
        writer.writerows(exits)
    print(f"[OK] Saved Exit Audit records to {exit_csv_path}")

    # 4. FP&A Budgets
    budgets = generate_fpa_department_budgets(employees)
    budget_csv_path = RAW_DATA_DIR / "fpa_department_budget_messy.csv"
    with open(budget_csv_path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(budgets[0].keys()))
        writer.writeheader()
        writer.writerows(budgets)
    print(f"[OK] Saved Messy Budget records to {budget_csv_path}")

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

    print("\n[SUCCESS] All Enterprise mock datasets synchronized with employees_data_7000.txt in data/raw/")


if __name__ == "__main__":
    export_data()
