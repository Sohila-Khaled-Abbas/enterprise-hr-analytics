## Description
Provide a concise summary of the changes proposed in this pull request and the business problem addressed.

## Architecture & Schema Area
- [ ] Conformed Dimensions (`Dim_Employee`, `Dim_Department`, `Dim_Branch`, `Dim_Date`, `Dim_Course`)
- [ ] Galaxy Fact Tables (`Fact_WorkforceSnapshot`, `Fact_DailyAttendance`, `Fact_DepartmentBudget`, `Fact_TrainingCompletions`)
- [ ] Microsoft SQL Server (T-SQL) DDL / Migrations
- [ ] Power BI Semantic Model (TMDL / DAX Measures)
- [ ] Data Engineering Pipeline / Heuristic Cleaner Scripts

## Data Quality & Software Engineering Checklist
- [ ] All 11 automated pytest tests pass: `pytest -v tests/test_data_quality.py`
- [ ] **No modifications have been introduced to existing files in `powerbi/`**
- [ ] Data validation rules in `docs/data_validation_rules.md` have been satisfied
- [ ] Foreign key referential integrity has 0 orphaned records
- [ ] T-SQL scripts adhere to `EnterpriseHR_DWH` schema conventions (`raw`, `stg`, `mart`)
