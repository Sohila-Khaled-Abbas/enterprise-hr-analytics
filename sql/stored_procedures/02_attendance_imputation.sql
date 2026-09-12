-- =============================================================================
-- Enterprise Human Capital & Operational Efficiency Diagnostics
-- Transformation Script 02: Attendance Cleansing & Heuristic Imputation
-- Database Engine: Microsoft SQL Server (T-SQL)
-- Architecture: Galaxy Schema (Fact Constellation)
-- =============================================================================

USE EnterpriseHR_DWH;
GO

SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
GO

CREATE OR ALTER PROCEDURE [stg].[usp_Transform_Fact_DailyAttendance]
    @StartDate DATE = NULL,
    @EndDate   DATE = NULL
AS
BEGIN
    SET NOCOUNT ON;

    IF @StartDate IS NULL SET @StartDate = DATEADD(MONTH, -1, CAST(SYSUTCDATETIME() AS DATE));
    IF @EndDate   IS NULL SET @EndDate   = CAST(SYSUTCDATETIME() AS DATE);

    -- 1. Temporary Staging Table with Imputed Timestamps and Durations
    WITH RawAttendance AS (
        SELECT 
            raw.[LogID],
            raw.[EmployeeID],
            raw.[AccessDate],
            raw.[CheckInTime],
            raw.[CheckOutTime],
            raw.[BuildingID],
            raw.[DeclaredWorkMode],
            -- Detection: Missing clock out
            CASE 
                WHEN raw.[CheckInTime] IS NOT NULL AND raw.[CheckOutTime] IS NULL THEN 1 
                ELSE 0 
            END AS IsMissingClockOut,
            -- Detection: Night shift crossover (CheckOut is earlier than CheckIn)
            CASE 
                WHEN raw.[CheckOutTime] < raw.[CheckInTime] THEN 1 
                ELSE 0 
            END AS IsNightShift
        FROM [stg].[Daily_Attendance_Logs] raw
        WHERE raw.[AccessDate] BETWEEN @StartDate AND @EndDate
    ),
    EmployeeMedianDurations AS (
        -- Calculate typical duration per employee to use as imputation baseline
        SELECT 
            raw.[EmployeeID],
            ISNULL(AVG(
                CASE 
                    WHEN raw.[CheckOutTime] >= raw.[CheckInTime] 
                    THEN DATEDIFF(MINUTE, raw.[CheckInTime], raw.[CheckOutTime]) / 60.0
                    WHEN raw.[CheckOutTime] < raw.[CheckInTime]
                    THEN (DATEDIFF(MINUTE, raw.[CheckInTime], '23:59:59') + DATEDIFF(MINUTE, '00:00:00', raw.[CheckOutTime]) + 1) / 60.0
                    ELSE 8.0
                END
            ), 8.0) AS MedianShiftHours
        FROM [stg].[Daily_Attendance_Logs] raw
        WHERE raw.[CheckInTime] IS NOT NULL AND raw.[CheckOutTime] IS NOT NULL
        GROUP BY raw.[EmployeeID]
    ),
    ImputedAttendance AS (
        SELECT 
            ra.[EmployeeID],
            ra.[AccessDate],
            CONVERT(INT, CONVERT(VARCHAR(8), ra.[AccessDate], 112)) AS AccessDateKey,
            ra.[CheckInTime],
            -- If clock out is missing, impute check out time based on employee median or 8 hours
            CASE 
                WHEN ra.[IsMissingClockOut] = 1 
                THEN DATEADD(MINUTE, CAST(ISNULL(emd.[MedianShiftHours], 8.0) * 60 AS INT), CAST(ra.[CheckInTime] AS DATETIME))
                ELSE ra.[CheckOutTime]
            END AS CleanCheckOutTime,
            -- Calculate precise duration
            CASE 
                WHEN ra.[IsMissingClockOut] = 1 
                THEN ISNULL(emd.[MedianShiftHours], 8.0)
                WHEN ra.[IsNightShift] = 1
                THEN (DATEDIFF(MINUTE, ra.[CheckInTime], '23:59:59') + DATEDIFF(MINUTE, '00:00:00', ra.[CheckOutTime]) + 1) / 60.0
                ELSE DATEDIFF(MINUTE, ra.[CheckInTime], ra.[CheckOutTime]) / 60.0
            END AS DurationHours,
            ra.[DeclaredWorkMode],
            CASE 
                WHEN ra.[BuildingID] IS NOT NULL AND ra.[BuildingID] <> N'REMOTE_GATE' THEN N'On-site'
                ELSE N'Remote'
            END AS ActualWorkMode,
            ra.[IsMissingClockOut],
            ra.[IsMissingClockOut] AS IsImputedClockOut,
            ra.[IsNightShift]
        FROM RawAttendance ra
        LEFT JOIN EmployeeMedianDurations emd ON ra.[EmployeeID] = emd.[EmployeeID]
    )
    -- 2. Insert into Fact_DailyAttendance with Contract Violation Flagging
    INSERT INTO [mart].[Fact_DailyAttendance] (
        [AccessDateKey],
        [EmployeeKey],
        [BranchKey],
        [CheckInTime],
        [CheckOutTime],
        [DurationHours],
        [DeclaredWorkMode],
        [ActualWorkMode],
        [IsMissingClockOut],
        [IsImputedClockOut],
        [IsNightShift],
        [IsContractViolation]
    )
    SELECT 
        ia.[AccessDateKey],
        emp.[EmployeeKey],
        emp.[BranchKey],
        ia.[CheckInTime],
        CAST(ia.[CleanCheckOutTime] AS TIME(0)),
        ROUND(ia.[DurationHours], 2),
        ia.[DeclaredWorkMode],
        ia.[ActualWorkMode],
        ia.[IsMissingClockOut],
        ia.[IsImputedClockOut],
        ia.[IsNightShift],
        -- Contract Violation Diagnostic:
        -- E.g., Contract is "دوام كامل (حضوري)" but employee worked remotely, or hybrid worker with unapproved remote day
        CASE 
            WHEN emp.[ContractType] = N'دوام كامل (حضوري)' AND ia.[ActualWorkMode] = N'Remote' THEN 1
            ELSE 0 
        END AS IsContractViolation
    FROM ImputedAttendance ia
    INNER JOIN [mart].[Dim_Employee] emp 
        ON ia.[EmployeeID] = emp.[EmployeeID]
       AND emp.[IsCurrent] = 1;
END;
GO

-- 3. Diagnostic View: Ghost Workers Detection
-- Identifies active employees on payroll who have zero physical/system access for 60+ consecutive days
CREATE OR ALTER VIEW [mart].[vw_Diagnostic_GhostWorkers]
AS
WITH RecentActivity AS (
    SELECT 
        f.[EmployeeKey],
        MAX(d.[FullDate]) AS LastAccessDate,
        DATEDIFF(DAY, MAX(d.[FullDate]), CAST(SYSUTCDATETIME() AS DATE)) AS DaysSinceLastAccess
    FROM [mart].[Fact_DailyAttendance] f
    INNER JOIN [mart].[Dim_Date] d ON f.[AccessDateKey] = d.[DateKey]
    GROUP BY f.[EmployeeKey]
)
SELECT 
    emp.[EmployeeID],
    emp.[FullName],
    emp.[JobRole],
    dept.[DepartmentName],
    br.[BranchName],
    emp.[BaseSalary],
    emp.[ContractType],
    ISNULL(ra.[DaysSinceLastAccess], 999) AS InactiveDaysCount,
    ra.[LastAccessDate]
FROM [mart].[Dim_Employee] emp
INNER JOIN [mart].[Dim_Department] dept ON emp.[DepartmentKey] = dept.[DepartmentKey]
INNER JOIN [mart].[Dim_Branch] br ON emp.[BranchKey] = br.[BranchKey]
LEFT JOIN RecentActivity ra ON emp.[EmployeeKey] = ra.[EmployeeKey]
WHERE emp.[IsCurrent] = 1
  AND (ra.[DaysSinceLastAccess] > 60 OR ra.[LastAccessDate] IS NULL);
GO
