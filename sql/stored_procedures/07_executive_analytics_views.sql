-- =============================================================================
-- Enterprise Human Capital & Software House Analytics
-- Analytical Views: 07_executive_analytics_views.sql
-- Database: EnterpriseHR_DWH | Schema: mart
-- Purpose: Pre-aggregated enterprise dimensional views for DirectQuery,
--          Power BI semantic models, and executive dashboards.
-- =============================================================================

USE EnterpriseHR_DWH;
GO

SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
GO

-- ─────────────────────────────────────────────────────────────────────────────
-- 1. Executive Workforce & Compensation Diagnostics View
-- ─────────────────────────────────────────────────────────────────────────────
IF OBJECT_ID(N'[mart].[vw_Executive_Workforce_Summary]', N'V') IS NOT NULL
    DROP VIEW [mart].[vw_Executive_Workforce_Summary];
GO

CREATE VIEW [mart].[vw_Executive_Workforce_Summary]
AS
SELECT 
    d.[DepartmentName],
    d.[Division],
    b.[Region],
    b.[City],
    b.[BranchName],
    COUNT(wf.[SnapshotKey]) AS [ActiveHeadcount],
    SUM(wf.[BaseSalary]) AS [TotalMonthlyPayroll_EGP],
    AVG(wf.[BaseSalary]) AS [AvgMonthlySalary_EGP],
    MIN(wf.[BaseSalary]) AS [MinSalary_EGP],
    MAX(wf.[BaseSalary]) AS [MaxSalary_EGP],
    AVG(wf.[AnnualPerformanceRating]) AS [AvgPerformanceRating],
    SUM(CASE WHEN wf.[IsSalaryCompressed] = 1 THEN 1 ELSE 0 END) AS [CompressedSalariesCount]
FROM [mart].[Fact_WorkforceSnapshot] wf
INNER JOIN [mart].[Dim_Department] d ON wf.[DepartmentKey] = d.[DepartmentKey]
INNER JOIN [mart].[Dim_Branch] b ON wf.[BranchKey] = b.[BranchKey]
GROUP BY 
    d.[DepartmentName],
    d.[Division],
    b.[Region],
    b.[City],
    b.[BranchName];
GO

-- ─────────────────────────────────────────────────────────────────────────────
-- 2. Client Project Delivery & Consulting Profitability View
-- ─────────────────────────────────────────────────────────────────────────────
IF OBJECT_ID(N'[mart].[vw_Project_Delivery_Profitability]', N'V') IS NOT NULL
    DROP VIEW [mart].[vw_Project_Delivery_Profitability];
GO

CREATE VIEW [mart].[vw_Project_Delivery_Profitability]
AS
SELECT 
    t.[ProjectID],
    t.[ProjectName],
    t.[ClientName],
    t.[TaskStatus],
    COUNT(t.[TaskKey]) AS [TaskCount],
    SUM(t.[PlannedHours]) AS [BudgetedHours],
    SUM(t.[ActualHours]) AS [ActualBilledHours],
    SUM(t.[ScopeOverrunHours]) AS [VarianceHours],
    AVG(t.[BillableHourlyRate_USD]) AS [EffectiveHourlyRateUSD],
    SUM(t.[TotalBilling_USD]) AS [TotalBillingUSD],
    SUM(t.[TotalBilling_EGP]) AS [TotalBillingEGP],
    SUM(CASE WHEN t.[IsDeliveryDelayed] = 1 THEN 1 ELSE 0 END) AS [OverdueDeliverables],
    AVG(t.[ClientSatisfactionRating]) AS [AvgCSAT]
FROM [mart].[Fact_ProjectTasks] t
GROUP BY 
    t.[ProjectID],
    t.[ProjectName],
    t.[ClientName],
    t.[TaskStatus];
GO

-- ─────────────────────────────────────────────────────────────────────────────
-- 3. Daily IoT Attendance & Shift Compliance View
-- ─────────────────────────────────────────────────────────────────────────────
IF OBJECT_ID(N'[mart].[vw_Daily_Attendance_Compliance]', N'V') IS NOT NULL
    DROP VIEW [mart].[vw_Daily_Attendance_Compliance];
GO

CREATE VIEW [mart].[vw_Daily_Attendance_Compliance]
AS
SELECT 
    att.[AccessDateKey],
    b.[BranchName],
    b.[Region],
    COUNT(att.[AttendanceKey]) AS [LoggedEmployees],
    SUM(CASE WHEN att.[ActualWorkMode] = 'Remote' THEN 1 ELSE 0 END) AS [RemoteWorkersCount],
    SUM(CASE WHEN att.[IsMissingClockOut] = 1 THEN 1 ELSE 0 END) AS [MissingClockOutCount],
    AVG(att.[DurationHours]) AS [AvgDailyShiftHours]
FROM [mart].[Fact_DailyAttendance] att
INNER JOIN [mart].[Dim_Branch] b ON att.[BranchKey] = b.[BranchKey]
GROUP BY 
    att.[AccessDateKey],
    b.[BranchName],
    b.[Region];
GO
