import os
import random
import pandas as pd

def generate_finance_excel(output_path: str):
    """Generates a messy, pivoted Excel workbook for departmental budgets."""
    departments = [
        "تكنولوجيا المعلومات", "الإدارة المالية", "التسويق والمبيعات", 
        "الموارد البشرية", "العمليات وسلاسل الإمداد", "خدمة العملاء والعمليات المساندة"
    ]
    
    # Intentional typos and non-standard naming conventions to simulate manual entry
    messy_branches = [
        "القاهرة - المعادي", "فرع المعادي", "الجيزة - الدقي", 
        "Alex Branch", "سموحة", "التجمع", "بورسعيد"
    ]
    
    data = []
    for dept in departments:
        for branch in messy_branches:
            # Simulate slight growth quarter over quarter
            base_headcount = random.randint(5, 40)
            base_budget = base_headcount * random.randint(15000, 30000)
            
            data.append({
                "Department": dept,
                "CostCenter_Branch": branch,
                "Q1_Headcount": base_headcount,
                "Q1_Budget_EGP": base_budget,
                "Q2_Headcount": int(base_headcount * 1.05),
                "Q2_Budget_EGP": int(base_budget * 1.05),
                "Q3_Headcount": int(base_headcount * 1.10),
                "Q3_Budget_EGP": int(base_budget * 1.10),
                "Q4_Headcount": int(base_headcount * 1.15),
                "Q4_Budget_EGP": int(base_budget * 1.15),
            })
            
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_excel(output_path, index=False, sheet_name="Budget_2026")
    print(f"Generated messy Finance Excel with {len(df)} rows at {output_path}")

if __name__ == "__main__":
    generate_finance_excel("data/raw/finance_budget_2026.xlsx")
