# scripts/utils/generate_lms_data.py
import os
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def generate_lms_csv(output_path: str = "data/raw/lms_certifications.csv"):
    """Generates synthetic LMS and certification completion logs with real-world flaws."""
    resolved_path = Path(output_path)
    if not resolved_path.is_absolute():
        resolved_path = BASE_DIR / output_path
        
    resolved_path.parent.mkdir(parents=True, exist_ok=True)
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2026, 6, 1)
    
    # Strictly aligned with the 7,000 master employees (EMP-10001 to EMP-17000)
    emp_ids = [f"EMP-{10000 + i}" for i in range(1, 7001)]
    courses = [
        ("CRS-101", "Advanced SQL & Performance Tuning", "Tech", 1500),
        ("CRS-102", "Python for Data Engineering", "Tech", 2500),
        ("CRS-103", "Power BI DAX Masterclass", "Tech", 2000),
        ("CRS-201", "Agile Project Management", "Leadership", 1200),
        ("CRS-202", "Cross-Cultural Business Communication", "Soft Skills", 800),
        ("CRS-301", "Cloud Security & Compliance", "Compliance", 3000),
        ("CRS-302", "Modern Data Stack Architecture", "Tech", 4000)
    ]
    
    records = []
    selected_employees = random.sample(emp_ids, int(len(emp_ids) * 0.45))
    
    for emp in selected_employees:
        num_courses = random.choices([1, 2, 3, 4], weights=[0.5, 0.3, 0.15, 0.05])[0]
        chosen_courses = random.sample(courses, num_courses)
        
        for course in chosen_courses:
            course_id, course_name, domain, cost = course
            completion_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
            score = random.choices([random.randint(50, 69), random.randint(70, 100)], weights=[0.15, 0.85])[0]
            status = "Completed" if score >= 70 else "Failed"
            
            records.append({
                "EmployeeID": emp,
                "CourseID": course_id,
                "CourseName": course_name,
                "SkillDomain": domain,
                "CompletionDate": completion_date.strftime("%Y-%m-%d"),
                "Score": score,
                "Status": status,
                "Cost_EGP": cost if status == "Completed" else 0
            })
            
            # Simulate a retake attempt for low scores or failures
            if score < 75:
                retake_date = completion_date + timedelta(days=random.randint(14, 60))
                if retake_date < end_date:
                    records.append({
                        "EmployeeID": emp,
                        "CourseID": course_id,
                        "CourseName": course_name,
                        "SkillDomain": domain,
                        "CompletionDate": retake_date.strftime("%Y-%m-%d"),
                        "Score": random.randint(75, 100),
                        "Status": "Completed",
                        "Cost_EGP": cost
                    })

    df = pd.DataFrame(records)
    df.to_csv(resolved_path, index=False)
    print(f"Generated {len(df)} LMS training records at {resolved_path}.")

if __name__ == "__main__":
    generate_lms_csv("data/raw/lms_certifications.csv")
