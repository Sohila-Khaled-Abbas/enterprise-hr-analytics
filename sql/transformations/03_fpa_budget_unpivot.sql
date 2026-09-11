-- =============================================================================
-- Enterprise Human Capital & Operational Efficiency Diagnostics
-- Transformation Script 03: FP&A Department Budget Unpivot & Branch Reconciliation
-- Database Engine: Microsoft SQL Server (T-SQL)
-- Architecture: Galaxy Schema (Fact Constellation)
-- =============================================================================

USE EnterpriseHR_DWH;
GO

SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
GO

CREATE OR ALTER PROCEDURE [stg].[usp_Transform_Fact_DepartmentBudget]
AS
BEGIN
    SET NOCOUNT ON;

    -- 1. Unpivot horizontal quarterly budgets using CROSS APPLY
    WITH UnpivotedBudgets AS (
        SELECT 
            b.[FiscalYear],
            b.[Department],
            b.[RawBranch],
            q.[FiscalQuarter],
            q.[BudgetedHeadcount],
            q.[AllocatedSalaryBudget_EGP],
            ISNULL(b.[OvertimeAllowance_EGP] / 4.0, 0.00) AS OvertimeAllowance_EGP
        FROM [stg].[FP_A_Department_Budgets_Wide] b
        CROSS APPLY (
            VALUES 
                (1, b.[Q1_Headcount], b.[Q1_Budget_EGP]),
                (2, b.[Q2_Headcount], b.[Q2_Budget_EGP]),
                (3, b.[Q3_Headcount], b.[Q3_Budget_EGP]),
                (4, b.[Q4_Headcount], b.[Q4_Budget_EGP])
        ) q([FiscalQuarter], [BudgetedHeadcount], [AllocatedSalaryBudget_EGP])
        WHERE q.[BudgetedHeadcount] IS NOT NULL 
           OR q.[AllocatedSalaryBudget_EGP] IS NOT NULL
    ),
    NormalizedBranches AS (
        -- Fuzzy / Typographical reconciliation for Arabic Branch variations
        SELECT 
            ub.*,
            CASE 
                WHEN ub.[RawBranch] LIKE N'%المعادي%' OR ub.[RawBranch] LIKE N'%المعادى%' THEN N'فرع المعادي'
                WHEN ub.[RawBranch] LIKE N'%مدينة نصر%' THEN N'فرع مدينة نصر'
                WHEN ub.[RawBranch] LIKE N'%التجمع%' OR ub.[RawBranch] LIKE N'%القاهرة الجديدة%' THEN N'فرع التجمع الخامس'
                WHEN ub.[RawBranch] LIKE N'%المهندسين%' THEN N'فرع المهندسين'
                WHEN ub.[RawBranch] LIKE N'%الإسكندرية%' OR ub.[RawBranch] LIKE N'%اسكندرية%' THEN N'فرع الإسكندرية - سموحة'
                WHEN ub.[RawBranch] LIKE N'%أسيوط%' OR ub.[RawBranch] LIKE N'%اسيوط%' THEN N'فرع أسيوط'
                WHEN ub.[RawBranch] LIKE N'%المنصورة%' THEN N'فرع المنصورة'
                ELSE ub.[RawBranch]
            END AS StandardizedBranchName,
            -- Smart DateKey mapping: Quarter starting date (YYYY0101, YYYY0401, YYYY0701, YYYY1001)
            CASE ub.[FiscalQuarter]
                WHEN 1 THEN ub.[FiscalYear] * 10000 + 101
                WHEN 2 THEN ub.[FiscalYear] * 10000 + 401
                WHEN 3 THEN ub.[FiscalYear] * 10000 + 701
                WHEN 4 THEN ub.[FiscalYear] * 10000 + 1001
            END AS QuarterStartDateKey
        FROM UnpivotedBudgets ub
    )
    -- 2. Insert into Fact_DepartmentBudget joining on conformed dimensions
    INSERT INTO [mart].[Fact_DepartmentBudget] (
        [FiscalYear],
        [FiscalQuarter],
        [DateKey],
        [DepartmentKey],
        [BranchKey],
        [BudgetedHeadcount],
        [AllocatedSalaryBudget_EGP],
        [OvertimeAllowance_EGP]
    )
    SELECT 
        nb.[FiscalYear],
        nb.[FiscalQuarter],
        nb.[QuarterStartDateKey],
        d.[DepartmentKey],
        b.[BranchKey],
        nb.[BudgetedHeadcount],
        nb.[AllocatedSalaryBudget_EGP],
        nb.[OvertimeAllowance_EGP]
    FROM NormalizedBranches nb
    INNER JOIN [mart].[Dim_Department] d 
        ON nb.[Department] = d.[DepartmentName]
    INNER JOIN [mart].[Dim_Branch] b 
        ON nb.[StandardizedBranchName] = b.[BranchName];
END;
GO
