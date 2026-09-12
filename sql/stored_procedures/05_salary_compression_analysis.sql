-- =============================================================================
-- Enterprise Human Capital & Operational Efficiency Diagnostics
-- Transformation Script 05: Salary Compression & Flight Risk Diagnostics
-- Database Engine: Microsoft SQL Server (T-SQL)
-- Architecture: Galaxy Schema (Fact Constellation)
-- =============================================================================

USE EnterpriseHR_DWH;
GO

SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
GO

CREATE OR ALTER PROCEDURE [stg].[usp_Transform_Fact_WorkforceSnapshot]
    @SnapshotDate DATE = NULL
AS
BEGIN
    SET NOCOUNT ON;

    IF @SnapshotDate IS NULL 
        SET @SnapshotDate = CAST(SYSUTCDATETIME() AS DATE);

    DECLARE @SnapshotDateKey INT = CONVERT(INT, CONVERT(VARCHAR(8), @SnapshotDate, 112));

    -- 1. Calculate Tenures, Role-Specific Salary Percentiles, and New-Hire Benchmarks
    WITH ActiveWorkforce AS (
        SELECT 
            emp.[EmployeeKey],
            emp.[EmployeeID],
            emp.[JobRole],
            emp.[DepartmentKey],
            emp.[BranchKey],
            emp.[BaseSalary],
            core.[تقييم الأداء السنوي] AS AnnualPerformanceRating,
            DATEDIFF(MONTH, emp.[HireDate], @SnapshotDate) AS TenureMonths,
            ROUND(DATEDIFF(DAY, emp.[HireDate], @SnapshotDate) / 365.25, 2) AS TenureYears,
            -- Calculate salary percentile within the employee's Job Role
            PERCENT_RANK() OVER (
                PARTITION BY emp.[JobRole] 
                ORDER BY emp.[BaseSalary] ASC
            ) AS SalaryPercentileInRole
        FROM [mart].[Dim_Employee] emp
        LEFT JOIN [stg].[Employees_Core] core 
            ON emp.[EmployeeID] = core.[الرقم التعريفي]
        WHERE emp.[IsCurrent] = 1
    ),
    NewHireBenchmarks AS (
        -- Calculate median salary for new hires (tenure <= 1.0 year) per Job Role
        SELECT 
            aw.[JobRole],
            PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY aw.[BaseSalary]) 
                OVER (PARTITION BY aw.[JobRole]) AS NewHireMedianSalary
        FROM ActiveWorkforce aw
        WHERE aw.[TenureYears] <= 1.0
    ),
    DistinctNewHireBenchmarks AS (
        SELECT DISTINCT [JobRole], [NewHireMedianSalary]
        FROM NewHireBenchmarks
    )
    -- 2. Insert into Fact_WorkforceSnapshot with Salary Compression Flag
    INSERT INTO [mart].[Fact_WorkforceSnapshot] (
        [SnapshotDateKey],
        [EmployeeKey],
        [DepartmentKey],
        [BranchKey],
        [BaseSalary],
        [AnnualPerformanceRating],
        [TenureMonths],
        [TenureYears],
        [SalaryPercentileInRole],
        [IsSalaryCompressed],
        [EmploymentStatus]
    )
    SELECT 
        @SnapshotDateKey,
        aw.[EmployeeKey],
        aw.[DepartmentKey],
        aw.[BranchKey],
        aw.[BaseSalary],
        aw.[AnnualPerformanceRating],
        aw.[TenureMonths],
        aw.[TenureYears],
        ROUND(aw.[SalaryPercentileInRole], 4),
        -- Salary Compression Rule:
        -- Tenured employee (>= 3 years) earning LESS than the new-hire median in the same role
        CASE 
            WHEN aw.[TenureYears] >= 3.0 AND aw.[BaseSalary] < ISNULL(nhb.[NewHireMedianSalary], 0) THEN 1
            ELSE 0 
        END AS IsSalaryCompressed,
        N'Active' AS EmploymentStatus
    FROM ActiveWorkforce aw
    LEFT JOIN DistinctNewHireBenchmarks nhb ON aw.[JobRole] = nhb.[JobRole];
END;
GO

-- 3. Diagnostic View: High Flight Risk & Salary Compression Heatmap
-- Flags high-performing, long-tenured employees suffering salary compression
CREATE OR ALTER VIEW [mart].[vw_Diagnostic_SalaryCompression_FlightRisk]
AS
SELECT 
    emp.[EmployeeID],
    emp.[FullName],
    emp.[JobRole],
    dept.[DepartmentName],
    br.[BranchName],
    wf.[TenureYears],
    wf.[BaseSalary],
    wf.[AnnualPerformanceRating],
    ROUND(wf.[SalaryPercentileInRole] * 100.0, 1) AS RoleSalaryPercentilePct,
    wf.[IsSalaryCompressed],
    -- Flight Risk Score (1 to 10 Scale)
    -- High performers (Rating >= 4.0) with high tenure but low pay have extreme risk
    CASE 
        WHEN wf.[IsSalaryCompressed] = 1 AND wf.[AnnualPerformanceRating] >= 4.5 THEN N'Critical (Flight Imminent)'
        WHEN wf.[IsSalaryCompressed] = 1 AND wf.[AnnualPerformanceRating] >= 3.5 THEN N'High Risk'
        WHEN wf.[IsSalaryCompressed] = 1 THEN N'Medium Risk'
        WHEN wf.[SalaryPercentileInRole] < 0.25 AND wf.[TenureYears] >= 2.0 THEN N'Moderate Inversion Risk'
        ELSE N'Low Risk / Market Aligned'
    END AS FlightRiskSeverity
FROM [mart].[Fact_WorkforceSnapshot] wf
INNER JOIN [mart].[Dim_Employee] emp ON wf.[EmployeeKey] = emp.[EmployeeKey]
INNER JOIN [mart].[Dim_Department] dept ON wf.[DepartmentKey] = dept.[DepartmentKey]
INNER JOIN [mart].[Dim_Branch] br ON wf.[BranchKey] = br.[BranchKey]
WHERE wf.[SnapshotDateKey] = (SELECT MAX(SnapshotDateKey) FROM [mart].[Fact_WorkforceSnapshot]);
GO
