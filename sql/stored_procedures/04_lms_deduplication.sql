-- =============================================================================
-- Enterprise Human Capital & Operational Efficiency Diagnostics
-- Transformation Script 04: LMS Course Completions Deduplication & Talent ROI
-- Database Engine: Microsoft SQL Server (T-SQL)
-- Architecture: Galaxy Schema (Fact Constellation)
-- =============================================================================

USE EnterpriseHR_DWH;
GO

SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
GO

CREATE OR ALTER PROCEDURE [stg].[usp_Transform_Fact_TrainingCompletions]
AS
BEGIN
    SET NOCOUNT ON;

    -- 1. Deduplicate & rank repeated certification attempts
    WITH RankedAttempts AS (
        SELECT 
            lms.[EmployeeID],
            lms.[CourseID],
            lms.[CompletionDate],
            CONVERT(INT, CONVERT(VARCHAR(8), lms.[CompletionDate], 112)) AS CompletionDateKey,
            lms.[Score],
            CASE WHEN lms.[Score] >= 70.0 THEN 1 ELSE 0 END AS IsPassed,
            lms.[CertificationCost_EGP],
            -- Chronological Attempt Number
            ROW_NUMBER() OVER (
                PARTITION BY lms.[EmployeeID], lms.[CourseID] 
                ORDER BY lms.[CompletionDate] ASC
            ) AS AttemptNumber,
            -- Highest Score Flag (1 for best score achieved)
            ROW_NUMBER() OVER (
                PARTITION BY lms.[EmployeeID], lms.[CourseID] 
                ORDER BY lms.[Score] DESC, lms.[CompletionDate] DESC
            ) AS BestScoreRank
        FROM [stg].[LMS_Course_Completions] lms
    )
    -- 2. Insert into Fact_TrainingCompletions joining on conformed Dim_Employee and Dim_Course
    INSERT INTO [mart].[Fact_TrainingCompletions] (
        [CompletionDateKey],
        [EmployeeKey],
        [CourseKey],
        [AttemptNumber],
        [Score],
        [IsPassed],
        [CertificationCost_EGP],
        [IsHighestScoreAttempt]
    )
    SELECT 
        ra.[CompletionDateKey],
        emp.[EmployeeKey],
        c.[CourseKey],
        ra.[AttemptNumber],
        ra.[Score],
        ra.[IsPassed],
        ra.[CertificationCost_EGP],
        CASE WHEN ra.[BestScoreRank] = 1 THEN 1 ELSE 0 END AS IsHighestScoreAttempt
    FROM RankedAttempts ra
    INNER JOIN [mart].[Dim_Employee] emp 
        ON ra.[EmployeeID] = emp.[EmployeeID]
       AND emp.[IsCurrent] = 1
    INNER JOIN [mart].[Dim_Course] c 
        ON ra.[CourseID] = c.[CourseID];
END;
GO

-- 3. Diagnostic View: Upskilling ROI & Performance Score Velocity
-- Compares average certification investment against performance rating velocity
CREATE OR ALTER VIEW [mart].[vw_Diagnostic_Upskilling_ROI]
AS
WITH TrainingSummary AS (
    SELECT 
        tc.[EmployeeKey],
        COUNT(DISTINCT tc.[CourseKey])           AS CompletedCoursesCount,
        SUM(tc.[CertificationCost_EGP])          AS TotalTrainingInvestment_EGP,
        AVG(tc.[Score])                          AS AvgCourseScore,
        MAX(d.[FullDate])                        AS LatestCourseDate
    FROM [mart].[Fact_TrainingCompletions] tc
    INNER JOIN [mart].[Dim_Date] d ON tc.[CompletionDateKey] = d.[DateKey]
    WHERE tc.[IsPassed] = 1 AND tc.[IsHighestScoreAttempt] = 1
    GROUP BY tc.[EmployeeKey]
),
PerformanceProgression AS (
    SELECT 
        wf.[EmployeeKey],
        wf.[AnnualPerformanceRating] AS CurrentPerformanceScore,
        wf.[TenureYears],
        wf.[BaseSalary]
    FROM [mart].[Fact_WorkforceSnapshot] wf
    WHERE wf.[SnapshotDateKey] = (SELECT MAX(SnapshotDateKey) FROM [mart].[Fact_WorkforceSnapshot])
)
SELECT 
    emp.[EmployeeID],
    emp.[FullName],
    emp.[JobRole],
    dept.[DepartmentName],
    ISNULL(ts.[CompletedCoursesCount], 0)        AS CertifiedCoursesCount,
    ISNULL(ts.[TotalTrainingInvestment_EGP], 0)  AS TotalTrainingCost_EGP,
    ROUND(ts.[AvgCourseScore], 2)                AS AvgCertificationScore,
    pp.[CurrentPerformanceScore],
    pp.[TenureYears],
    pp.[BaseSalary],
    -- Training ROI Indicator
    CASE 
        WHEN ISNULL(ts.[TotalTrainingInvestment_EGP], 0) > 0 
        THEN ROUND(pp.[CurrentPerformanceScore] / (ts.[TotalTrainingInvestment_EGP] / 1000.0), 4)
        ELSE NULL 
    END AS PerformancePointsPerThousandEGP
FROM [mart].[Dim_Employee] emp
INNER JOIN [mart].[Dim_Department] dept ON emp.[DepartmentKey] = dept.[DepartmentKey]
LEFT JOIN TrainingSummary ts ON emp.[EmployeeKey] = ts.[EmployeeKey]
LEFT JOIN PerformanceProgression pp ON emp.[EmployeeKey] = pp.[EmployeeKey]
WHERE emp.[IsCurrent] = 1;
GO
