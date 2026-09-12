-- sql/transformations/02_mart_dimensional_model.sql
USE EnterpriseHR_DWH;
GO

-- 1. Create Dim_Employee (Latest Master Record)
IF OBJECT_ID('mart.Dim_Employee', 'U') IS NOT NULL DROP TABLE mart.Dim_Employee;
GO

WITH LatestEmployeeState AS (
    SELECT 
        EmployeeID,
        BranchOrSalaryContext AS LatestBranch,
        Salary_EGP AS LatestSalary,
        IsTerminated,
        ROW_NUMBER() OVER (PARTITION BY EmployeeID ORDER BY ValidFrom DESC) as rn
    FROM stg.Stg_HR_Audit
)
SELECT 
    EmployeeID,
    LatestBranch,
    LatestSalary,
    CASE WHEN IsTerminated = 1 THEN 'Inactive' ELSE 'Active' END AS EmploymentStatus
INTO mart.Dim_Employee
FROM LatestEmployeeState
WHERE rn = 1;

ALTER TABLE mart.Dim_Employee ADD CONSTRAINT PK_Dim_Employee PRIMARY KEY(EmployeeID);
GO

-- 2. Create Fact_Employee_SCD2 (For historical point-in-time analysis)
IF OBJECT_ID('mart.Fact_Employee_SCD2', 'U') IS NOT NULL DROP TABLE mart.Fact_Employee_SCD2;
GO

SELECT 
    StagingKey,
    EmployeeID,
    EventType,
    ValidFrom,
    ValidTo,
    IsCurrent,
    BranchOrSalaryContext,
    Salary_EGP,
    IsTerminated
INTO mart.Fact_Employee_SCD2
FROM stg.Stg_HR_Audit;
GO

-- 3. Create Fact_Daily_Badge (IoT Badge Logs Cleanup & Duration)
IF OBJECT_ID('mart.Fact_Daily_Badge', 'U') IS NOT NULL DROP TABLE mart.Fact_Daily_Badge;
GO

SELECT 
    LogID,
    EmployeeID,
    CAST(AccessDate AS DATE) AS AccessDate,
    FacilityCode,
    SystemSource,
    CAST(CheckInTime AS DATETIME) AS CheckInTime,
    -- Real-world problem solved: Imputing missing check-outs for forgotten swipes
    COALESCE(CAST(CheckOutTime AS DATETIME), DATEADD(hour, 8, CAST(CheckInTime AS DATETIME))) AS CheckOutTime,
    -- Calculate work duration in hours
    DATEDIFF(minute, CAST(CheckInTime AS DATETIME), COALESCE(CAST(CheckOutTime AS DATETIME), DATEADD(hour, 8, CAST(CheckInTime AS DATETIME)))) / 60.0 AS WorkDurationHours
INTO mart.Fact_Daily_Badge
FROM raw.Badge_Access_Logs;
GO

-- 4. Create Fact_LMS_Training (Retake & Failure Filtering)
IF OBJECT_ID('mart.Fact_LMS_Training', 'U') IS NOT NULL DROP TABLE mart.Fact_LMS_Training;
GO

WITH CastAttempts AS (
    SELECT 
        CAST(EmployeeID AS VARCHAR(20)) AS EmployeeID,
        CAST(CourseID AS VARCHAR(20)) AS CourseID,
        CAST(CourseName AS VARCHAR(150)) AS CourseName,
        CAST(SkillDomain AS VARCHAR(50)) AS SkillDomain,
        CAST(CompletionDate AS DATE) AS CompletionDate,
        CAST(Score AS FLOAT) AS Score,
        CAST(Cost_EGP AS DECIMAL(12, 2)) AS Cost_EGP
    FROM raw.LMS_Certifications
    WHERE Status = 'Completed' -- Real-world constraint: Only pay/credit for valid completions
),
RankedAttempts AS (
    SELECT 
        EmployeeID,
        CourseID,
        CourseName,
        SkillDomain,
        CompletionDate,
        Score,
        Cost_EGP,
        -- Keep only successful completions, or if all failed, keep the highest score attempt
        ROW_NUMBER() OVER (
            PARTITION BY EmployeeID, CourseID 
            ORDER BY Score DESC
        ) AS AttemptRank
    FROM CastAttempts
)
SELECT 
    EmployeeID,
    CourseID,
    CourseName,
    SkillDomain,
    CompletionDate,
    Score,
    Cost_EGP
INTO mart.Fact_LMS_Training
FROM RankedAttempts
WHERE AttemptRank = 1;
GO
