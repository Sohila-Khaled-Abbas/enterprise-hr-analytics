"""
Enterprise Data Generator: generate_enriched_datasets.py
Domain: Software House & L&D Academy (Nexora Tech Solutions)
Generates:
1. data/raw/client_projects_tasks.csv & .json (Client projects, freelance tasks, billable hours)
2. data/raw/dim_currency_rates.csv (Multi-currency conversion matrix)
3. data/raw/lms_curriculum_catalog.csv (L&D academy course tiers & accreditation)
"""

import os
import json
import random
import csv
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_RAW = BASE_DIR / "data" / "raw"
DATA_PROCESSED = BASE_DIR / "data" / "processed"
DATA_RAW.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# 1. GENERATE DIM_CURRENCY_RATES
# -------------------------------------------------------------
def generate_currency_rates():
    rates_data = [
        {"CurrencyKey": 1, "CurrencyCode": "EGP", "CurrencyName": "Egyptian Pound", "RateToEGP": 1.0000, "OneEGPInCurrency": 1.000000, "RateType": "Base Operational Currency", "LastUpdated": "2026-09-14 00:00:00"},
        {"CurrencyKey": 2, "CurrencyCode": "USD", "CurrencyName": "United States Dollar", "RateToEGP": 48.8500, "OneEGPInCurrency": 0.020471, "RateType": "Central Bank Spot Rate", "LastUpdated": "2026-09-14 00:00:00"},
        {"CurrencyKey": 3, "CurrencyCode": "EUR", "CurrencyName": "Euro", "RateToEGP": 53.2000, "OneEGPInCurrency": 0.018797, "RateType": "Central Bank Spot Rate", "LastUpdated": "2026-09-14 00:00:00"},
        {"CurrencyKey": 4, "CurrencyCode": "GBP", "CurrencyName": "British Pound", "RateToEGP": 63.5000, "OneEGPInCurrency": 0.015748, "RateType": "Central Bank Spot Rate", "LastUpdated": "2026-09-14 00:00:00"},
        {"CurrencyKey": 5, "CurrencyCode": "SAR", "CurrencyName": "Saudi Riyal", "RateToEGP": 13.0200, "OneEGPInCurrency": 0.076805, "RateType": "Regional Pegged Spot", "LastUpdated": "2026-09-14 00:00:00"},
        {"CurrencyKey": 6, "CurrencyCode": "AED", "CurrencyName": "UAE Dirham", "RateToEGP": 13.3000, "OneEGPInCurrency": 0.075188, "RateType": "Regional Pegged Spot", "LastUpdated": "2026-09-14 00:00:00"}
    ]

    csv_path = DATA_RAW / "dim_currency_rates.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rates_data[0].keys()))
        writer.writeheader()
        writer.writerows(rates_data)

    # Also copy to processed
    proc_path = DATA_PROCESSED / "Dim_CurrencyRates.csv"
    with open(proc_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rates_data[0].keys()))
        writer.writeheader()
        writer.writerows(rates_data)

    print(f"[OK] Generated {csv_path} ({len(rates_data)} currencies)")


# -------------------------------------------------------------
# 2. GENERATE LMS CURRICULUM CATALOG
# -------------------------------------------------------------
def generate_lms_catalog():
    courses = [
        {
            "CourseKey": 1, "CourseID": "CRS-101", "CourseName": "Cloud Foundations & Azure Fundamentals",
            "SkillDomain": "Cloud Architecture", "CourseLevel": "Level 1 (Foundational)", "AccreditationBody": "Microsoft Learn",
            "DurationHours": 24, "Cost_EGP": 4500.00, "PassingThreshold": 70, "ExpectedSalaryDelta_Pct": 0.06
        },
        {
            "CourseKey": 2, "CourseID": "CRS-102", "CourseName": "Python for Enterprise Data Analytics",
            "SkillDomain": "Data & AI Engineering", "CourseLevel": "Level 1 (Foundational)", "AccreditationBody": "Python Institute",
            "DurationHours": 32, "Cost_EGP": 5200.00, "PassingThreshold": 70, "ExpectedSalaryDelta_Pct": 0.07
        },
        {
            "CourseKey": 3, "CourseID": "CRS-103", "CourseName": "Agile Scrum & Client Consulting Practices",
            "SkillDomain": "Leadership & Strategy", "CourseLevel": "Level 1 (Foundational)", "AccreditationBody": "Scrum.org",
            "DurationHours": 16, "Cost_EGP": 3800.00, "PassingThreshold": 75, "ExpectedSalaryDelta_Pct": 0.05
        },
        {
            "CourseKey": 4, "CourseID": "CRS-201", "CourseName": "AWS Solutions Architect Associate",
            "SkillDomain": "Cloud Architecture", "CourseLevel": "Level 2 (Intermediate)", "AccreditationBody": "Amazon Web Services",
            "DurationHours": 48, "Cost_EGP": 9500.00, "PassingThreshold": 72, "ExpectedSalaryDelta_Pct": 0.12
        },
        {
            "CourseKey": 5, "CourseID": "CRS-202", "CourseName": "Databricks & PySpark Lakehouse Engineering",
            "SkillDomain": "Data & AI Engineering", "CourseLevel": "Level 2 (Intermediate)", "AccreditationBody": "Databricks Academy",
            "DurationHours": 60, "Cost_EGP": 12500.00, "PassingThreshold": 70, "ExpectedSalaryDelta_Pct": 0.15
        },
        {
            "CourseKey": 6, "CourseID": "CRS-203", "CourseName": "CI/CD Automation with Docker & GitHub Actions",
            "SkillDomain": "DevOps & SRE", "CourseLevel": "Level 2 (Intermediate)", "AccreditationBody": "Linux Foundation",
            "DurationHours": 40, "Cost_EGP": 8200.00, "PassingThreshold": 70, "ExpectedSalaryDelta_Pct": 0.10
        },
        {
            "CourseKey": 7, "CourseID": "CRS-204", "CourseName": "Full-Stack Next.js & Microservices Architecture",
            "SkillDomain": "Software Engineering", "CourseLevel": "Level 2 (Intermediate)", "AccreditationBody": "Vercel / Node.js Org",
            "DurationHours": 45, "Cost_EGP": 8900.00, "PassingThreshold": 70, "ExpectedSalaryDelta_Pct": 0.11
        },
        {
            "CourseKey": 8, "CourseID": "CRS-301", "CourseName": "Kubernetes Administration (CKA) & Mesh Engineering",
            "SkillDomain": "DevOps & SRE", "CourseLevel": "Level 3 (Advanced)", "AccreditationBody": "Cloud Native Computing Foundation",
            "DurationHours": 75, "Cost_EGP": 18000.00, "PassingThreshold": 75, "ExpectedSalaryDelta_Pct": 0.20
        },
        {
            "CourseKey": 9, "CourseID": "CRS-302", "CourseName": "Enterprise Data Governance & Fabric Solution Architecture",
            "SkillDomain": "Data & AI Engineering", "CourseLevel": "Level 3 (Advanced)", "AccreditationBody": "Microsoft Fabric Alliance",
            "DurationHours": 65, "Cost_EGP": 16500.00, "PassingThreshold": 75, "ExpectedSalaryDelta_Pct": 0.18
        },
        {
            "CourseKey": 10, "CourseID": "CRS-303", "CourseName": "Zero-Trust Cybersecurity & DevSecOps Leadership",
            "SkillDomain": "Cybersecurity", "CourseLevel": "Level 3 (Advanced)", "AccreditationBody": "ISC2 / CISSP Partner",
            "DurationHours": 80, "Cost_EGP": 22000.00, "PassingThreshold": 80, "ExpectedSalaryDelta_Pct": 0.22
        }
    ]

    csv_path = DATA_RAW / "lms_curriculum_catalog.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(courses[0].keys()))
        writer.writeheader()
        writer.writerows(courses)
    print(f"[OK] Generated {csv_path} ({len(courses)} courses)")


# -------------------------------------------------------------
# 3. GENERATE CLIENT PROJECTS & FREELANCE DELIVERY TASKS
# -------------------------------------------------------------
def generate_client_projects_tasks():
    emp_ids = []
    emp_txt = DATA_RAW / "employees_data_7000.txt"
    if emp_txt.exists():
        with open(emp_txt, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) >= 2 and parts[0].startswith("EMP-"):
                    emp_ids.append(parts[0])
    if not emp_ids:
        emp_ids = [f"EMP-{i:05d}" for i in range(10001, 17001)]

    projects = [
        {"ProjectID": "PRJ-901", "ProjectName": "Fintech Mobile Banking Engine", "ClientName": "Aramco Tech Ventures", "ClientCountry": "Saudi Arabia", "ClientRegion": "Gulf / MENA", "Industry": "Fintech & Banking", "BaseRate_USD": 65.0},
        {"ProjectID": "PRJ-902", "ProjectName": "Cloud Data Lakehouse Migration", "ClientName": "Emirates Digital Holdings", "ClientCountry": "United Arab Emirates", "ClientRegion": "Gulf / MENA", "Industry": "Energy & Logistics", "BaseRate_USD": 75.0},
        {"ProjectID": "PRJ-903", "ProjectName": "AI Medical Diagnostic Assistant", "ClientName": "HealthBridge BioSystems", "ClientCountry": "United States", "ClientRegion": "North America", "Industry": "Healthcare", "BaseRate_USD": 85.0},
        {"ProjectID": "PRJ-904", "ProjectName": "Omnichannel E-Commerce Modernization", "ClientName": "RetailNext Global", "ClientCountry": "United Kingdom", "ClientRegion": "Europe", "Industry": "Retail & Consumer", "BaseRate_USD": 70.0},
        {"ProjectID": "PRJ-905", "ProjectName": "Microservices Core Banking Gateway", "ClientName": "Banque du Caire Digital", "ClientCountry": "Egypt", "ClientRegion": "Domestic Egypt", "Industry": "Fintech & Banking", "BaseRate_USD": 45.0},
        {"ProjectID": "PRJ-906", "ProjectName": "Fleet Telematics & IoT Tracking API", "ClientName": "LogiTrans Gulf Express", "ClientCountry": "Saudi Arabia", "ClientRegion": "Gulf / MENA", "Industry": "Supply Chain", "BaseRate_USD": 60.0},
        {"ProjectID": "PRJ-907", "ProjectName": "Zero-Trust Security Identity Mesh", "ClientName": "Nordic Cyber Defence", "ClientCountry": "Germany", "ClientRegion": "Europe", "Industry": "Cybersecurity", "BaseRate_USD": 95.0},
        {"ProjectID": "PRJ-908", "ProjectName": "Enterprise HR & Talent SaaS Portal", "ClientName": "Apex Workforce Solutions", "ClientCountry": "United States", "ClientRegion": "North America", "Industry": "Human Capital", "BaseRate_USD": 68.0}
    ]

    task_templates = [
        ("Design & Implement RESTful Payment Endpoints", "Software Engineering", 40, "Level 2 - Specialized"),
        ("PySpark ETL Pipeline for Turnstile Telemetry", "Data & AI Engineering", 50, "Level 2 - Specialized"),
        ("Kubernetes Cluster Hardening & Istio Service Mesh", "DevOps & SRE", 35, "Level 3 - Enterprise Architect"),
        ("Next.js 14 Responsive Executive Dashboard", "Software Engineering", 30, "Level 1 - Core"),
        ("PostgreSQL to Snowflake Lakehouse Replication", "Data & AI Engineering", 60, "Level 3 - Enterprise Architect"),
        ("OAuth2.0 / OpenID Multi-Tenant Auth Integration", "Cybersecurity", 25, "Level 2 - Specialized"),
        ("End-to-End Cypress Integration & Performance Suite", "Quality Engineering", 30, "Level 1 - Core"),
        ("Fine-Tuning Llama-3 Model for Customer Ticket RAG", "Data & AI Engineering", 70, "Level 3 - Enterprise Architect"),
        ("AWS Terraform Infrastructure as Code Provisioning", "Cloud Architecture", 45, "Level 2 - Specialized"),
        ("GraphQL Gateway Federation & Schema Stitching", "Software Engineering", 35, "Level 2 - Specialized"),
        ("Penetration Testing & Remediation of API Endpoints", "Cybersecurity", 20, "Level 2 - Specialized"),
        ("Mobile Flutter Biometric Authentication Module", "Software Engineering", 28, "Level 1 - Core"),
        ("Real-time Kafka Event Streaming for Turnstiles", "Data & AI Engineering", 55, "Level 3 - Enterprise Architect"),
        ("CI/CD Pipeline Optimization with Docker BuildKit", "DevOps & SRE", 18, "Level 1 - Core"),
        ("SOC2 Compliance Evidence Collection Automation", "Cybersecurity", 32, "Level 2 - Specialized")
    ]

    start_date = datetime(2025, 1, 1)
    end_date = datetime(2026, 8, 31)
    delta_days = (end_date - start_date).days

    task_records = []
    num_tasks = 3600

    for i in range(1, num_tasks + 1):
        task_id = f"TSK-{i:05d}"
        proj = random.choice(projects)
        tmpl_title, skill_domain, planned_hrs, complexity = random.choice(task_templates)
        
        hours_noise = random.uniform(0.85, 1.35)
        actual_hrs = round(planned_hrs * hours_noise, 1)
        is_overrun = actual_hrs > planned_hrs

        status_rand = random.random()
        if status_rand < 0.78:
            status = "Completed"
            rating = round(random.choices([5.0, 4.5, 4.0, 3.5, 3.0], weights=[40, 35, 15, 7, 3])[0], 1)
        elif status_rand < 0.90:
            status = "Under Review"
            rating = None
        elif status_rand < 0.96:
            status = "In Progress"
            rating = None
        else:
            status = "Scope Revision Requested"
            rating = 2.5 if random.random() < 0.5 else 3.0

        assigned_emp = random.choice(emp_ids)

        task_start = start_date + timedelta(days=random.randint(0, delta_days - 30))
        deadline = task_start + timedelta(days=int(planned_hrs / 4) + random.randint(2, 7))
        if status == "Completed":
            completion_date = deadline + timedelta(days=random.randint(-3, 6))
            is_delayed = completion_date > deadline
        else:
            completion_date = None
            is_delayed = datetime(2026, 9, 14) > deadline

        rate_multiplier = 1.0
        if complexity == "Level 3 - Enterprise Architect":
            rate_multiplier = 1.35
        elif complexity == "Level 2 - Specialized":
            rate_multiplier = 1.15
        billable_rate_usd = round(proj["BaseRate_USD"] * rate_multiplier, 2)
        total_billing_usd = round(billable_rate_usd * (actual_hrs if status == "Completed" else planned_hrs), 2)

        record = {
            "TaskID": task_id,
            "ProjectID": proj["ProjectID"],
            "ProjectName": proj["ProjectName"],
            "ClientName": proj["ClientName"],
            "ClientCountry": proj["ClientCountry"],
            "ClientRegion": proj["ClientRegion"],
            "Industry": proj["Industry"],
            "AssignedEmployeeID": assigned_emp,
            "TaskTitle": f"{tmpl_title} ({proj['ProjectID']})",
            "SkillDomain": skill_domain,
            "ComplexityTier": complexity,
            "PlannedHours": planned_hrs,
            "ActualHours": actual_hrs,
            "IsHoursOverrun": is_overrun,
            "BillableHourlyRate_USD": billable_rate_usd,
            "TotalBilling_USD": total_billing_usd,
            "TaskStatus": status,
            "ClientSatisfactionRating": rating,
            "TaskStartDate": task_start.strftime("%Y-%m-%d"),
            "DeliveryDeadline": deadline.strftime("%Y-%m-%d"),
            "ActualCompletionDate": completion_date.strftime("%Y-%m-%d") if completion_date else None,
            "IsDeliveryDelayed": is_delayed if status == "Completed" else False
        }
        task_records.append(record)

    csv_file = DATA_RAW / "client_projects_tasks.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(task_records[0].keys()))
        writer.writeheader()
        writer.writerows(task_records)

    json_file = DATA_RAW / "client_projects_tasks.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(task_records, f, indent=2, ensure_ascii=False)

    print(f"[OK] Generated {csv_file} & {json_file} ({len(task_records)} client delivery tasks)")


def main():
    print("Enriching project data with Software House & L&D datasets (Nexora Tech Solutions)...")
    generate_currency_rates()
    generate_lms_catalog()
    generate_client_projects_tasks()
    print("Data enrichment completed successfully!")

if __name__ == "__main__":
    main()
