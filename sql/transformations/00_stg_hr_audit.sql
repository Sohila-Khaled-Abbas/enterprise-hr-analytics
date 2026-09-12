-- sql/transformations/00_stg_hr_audit.sql
-- ═══════════════════════════════════════════════════════════════════════════
-- Enterprise HR Analytics – Staging & Cleaning Layer
-- Transforms raw.HR_Audit_Events into stg.Stg_HR_Audit with:
--   1. Exact-duplicate deduplication (API retry / system glitch rows)
--   2. Deterministic Arabic branch-name normalization
--   3. SCD Type 2 ValidFrom / ValidTo date boundaries via LEAD()
-- ═══════════════════════════════════════════════════════════════════════════
USE EnterpriseHR_DWH;
GO

-- Drop staging table if it exists
IF OBJECT_ID('stg.Stg_HR_Audit', 'U') IS NOT NULL
    DROP TABLE stg.Stg_HR_Audit;
GO

-- Create explicit staging table with strongly typed columns
CREATE TABLE stg.Stg_HR_Audit (
    StagingKey INT IDENTITY(1,1) PRIMARY KEY CLUSTERED,
    EmployeeID VARCHAR(20) NOT NULL,
    EventType VARCHAR(50) NOT NULL,
    ValidFrom DATE NOT NULL,
    ValidTo DATE NOT NULL,
    IsCurrent BIT NOT NULL,
    BranchOrSalaryContext NVARCHAR(150),
    Salary_EGP DECIMAL(18,2),
    IsTerminated INT
);
GO

WITH CleanedRaw AS (
    -- Step 1: Remove exact duplicate event entries caused by API/system retry glitches
    SELECT 
        EmployeeID,
        UPPER(TRIM(EventType)) AS EventType,
        EffectiveDate,
        LOWER(TRIM(PreviousValue)) AS PreviousValue,
        LOWER(TRIM(NewValue)) AS NewValue,
        Salary_EGP,
        IsTerminated,
        ROW_NUMBER() OVER (
            PARTITION BY EmployeeID, EventType, EffectiveDate, NewValue, Salary_EGP 
            ORDER BY EffectiveDate DESC
        ) AS RowNum
    FROM raw.HR_Audit_Events
),
NormalizedBranches AS (
    -- Step 2: Handle string drift and typos in branch names via deterministic mapping
    SELECT 
        EmployeeID,
        EventType,
        EffectiveDate,
        PreviousValue,
        CASE 
            WHEN NewValue LIKE N'%معادي%' OR NewValue LIKE N'%المعادي%' THEN N'القاهرة - المعادي'
            WHEN NewValue LIKE N'%دقي%' OR NewValue LIKE N'%الدقي%' THEN N'الجيزة - الدقي'
            WHEN NewValue LIKE N'%سموحة%' THEN N'الإسكندرية - سموحة'
            WHEN NewValue LIKE N'%تجمع%' THEN N'القاهرة - التجمع الخامس'
            WHEN NewValue LIKE N'%بورسعيد%' THEN N'بورسعيد - الشرق'
            WHEN NewValue LIKE N'%مدينة نصر%' THEN N'القاهرة - مدينة نصر'
            WHEN NewValue LIKE N'%مكرم%' THEN N'القاهرة - مكرم عبيد'
            WHEN NewValue LIKE N'%عباس%' OR NewValue LIKE N'%العباسية%' THEN N'القاهرة - العباسية'
            ELSE ISNULL(NewValue, N'Unknown')
        END AS NewValue,
        Salary_EGP,
        IsTerminated
    FROM CleanedRaw
    WHERE RowNum = 1
),
SCD2_Window AS (
    -- Step 3: Construct SCD Type 2 ValidFrom and ValidTo date boundaries using LEAD()
    SELECT 
        EmployeeID,
        EventType,
        EffectiveDate AS ValidFrom,
        ISNULL(LEAD(EffectiveDate, 1) OVER (
            PARTITION BY EmployeeID 
            ORDER BY EffectiveDate ASC
        ), '9999-12-31') AS ValidTo,
        NewValue AS BranchOrSalaryContext,
        Salary_EGP,
        IsTerminated
    FROM NormalizedBranches
)
INSERT INTO stg.Stg_HR_Audit (
    EmployeeID, EventType, ValidFrom, ValidTo, IsCurrent, BranchOrSalaryContext, Salary_EGP, IsTerminated
)
SELECT 
    EmployeeID,
    EventType,
    ValidFrom,
    ValidTo,
    CASE WHEN ValidTo = '9999-12-31' THEN 1 ELSE 0 END AS IsCurrent,
    BranchOrSalaryContext,
    Salary_EGP,
    IsTerminated
FROM SCD2_Window;
GO

-- Create index on EmployeeID + ValidFrom for rapid SCD2 temporal point-in-time lookups
CREATE NONCLUSTERED INDEX IX_Stg_HR_Audit_Emp_Valid ON stg.Stg_HR_Audit(EmployeeID, ValidFrom, ValidTo);
GO

-- Verification: Row counts and sample
SELECT 'Total Staged Rows' AS Metric, COUNT(*) AS Value FROM stg.Stg_HR_Audit
UNION ALL
SELECT 'Unique Employees', COUNT(DISTINCT EmployeeID) FROM stg.Stg_HR_Audit
UNION ALL
SELECT 'Current Records (IsCurrent=1)', SUM(CAST(IsCurrent AS INT)) FROM stg.Stg_HR_Audit;
GO
