-- =============================================================================
-- Enterprise Human Capital & Operational Efficiency Diagnostics
-- DDL Script 02: Star Schema Fact Tables
-- Database Engine: Microsoft SQL Server (T-SQL)
-- Schema: mart
-- =============================================================================

USE EnterpriseHR_DWH;
GO

SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
GO

-- 1. Fact_WorkforceSnapshot: Monthly Snapshot of Active Employees & Compensation
IF OBJECT_ID(N'[mart].[Fact_WorkforceSnapshot]', N'U') IS NULL
BEGIN
    CREATE TABLE [mart].[Fact_WorkforceSnapshot] (
        [SnapshotKey]             BIGINT IDENTITY(1,1) NOT NULL,
        [SnapshotDateKey]         INT                  NOT NULL,
        [EmployeeKey]             INT                  NOT NULL,
        [DepartmentKey]           INT                  NOT NULL,
        [BranchKey]               INT                  NOT NULL,
        [BaseSalary]              DECIMAL(18,2)        NOT NULL,
        [AnnualPerformanceRating] DECIMAL(4,2)         NULL,
        [TenureMonths]            INT                  NOT NULL,
        [TenureYears]             DECIMAL(5,2)         NOT NULL,
        [SalaryPercentileInRole]  DECIMAL(6,4)         NULL, -- 0.0000 to 1.0000 within JobRole
        [IsSalaryCompressed]      BIT                  NOT NULL CONSTRAINT [DF_Fact_WF_IsCompressed] DEFAULT (0),
        [EmploymentStatus]        NVARCHAR(50)         NOT NULL CONSTRAINT [DF_Fact_WF_Status] DEFAULT (N'Active'),
        [CreatedAt]               DATETIME2(7)         NOT NULL CONSTRAINT [DF_Fact_WF_CreatedAt] DEFAULT (SYSUTCDATETIME()),
        CONSTRAINT [PK_Fact_WorkforceSnapshot] PRIMARY KEY CLUSTERED ([SnapshotKey] ASC),
        CONSTRAINT [FK_Fact_WF_Date] FOREIGN KEY ([SnapshotDateKey]) REFERENCES [mart].[Dim_Date]([DateKey]),
        CONSTRAINT [FK_Fact_WF_Employee] FOREIGN KEY ([EmployeeKey]) REFERENCES [mart].[Dim_Employee]([EmployeeKey]),
        CONSTRAINT [FK_Fact_WF_Department] FOREIGN KEY ([DepartmentKey]) REFERENCES [mart].[Dim_Department]([DepartmentKey]),
        CONSTRAINT [FK_Fact_WF_Branch] FOREIGN KEY ([BranchKey]) REFERENCES [mart].[Dim_Branch]([BranchKey])
    );

    CREATE NONCLUSTERED INDEX [IX_Fact_WF_SnapshotDate] ON [mart].[Fact_WorkforceSnapshot] ([SnapshotDateKey] ASC);
    CREATE NONCLUSTERED INDEX [IX_Fact_WF_Employee] ON [mart].[Fact_WorkforceSnapshot] ([EmployeeKey] ASC);
    CREATE NONCLUSTERED INDEX [IX_Fact_WF_Compression] ON [mart].[Fact_WorkforceSnapshot] ([IsSalaryCompressed] ASC) INCLUDE ([BaseSalary], [TenureYears]);
END;
GO

-- 2. Fact_DailyAttendance: Daily Grain IoT Access & Clock Event Diagnostics
IF OBJECT_ID(N'[mart].[Fact_DailyAttendance]', N'U') IS NULL
BEGIN
    CREATE TABLE [mart].[Fact_DailyAttendance] (
        [AttendanceKey]           BIGINT IDENTITY(1,1) NOT NULL,
        [AccessDateKey]           INT                  NOT NULL,
        [EmployeeKey]             INT                  NOT NULL,
        [BranchKey]               INT                  NOT NULL,
        [CheckInTime]             TIME(0)              NULL,
        [CheckOutTime]            TIME(0)              NULL,
        [DurationHours]           DECIMAL(6,2)         NOT NULL,
        [DeclaredWorkMode]        NVARCHAR(50)         NOT NULL, -- On-site, Remote, Field
        [ActualWorkMode]          NVARCHAR(50)         NOT NULL, -- Physical Badge Detected vs Virtual
        [IsMissingClockOut]       BIT                  NOT NULL CONSTRAINT [DF_Fact_Att_MissingOut] DEFAULT (0),
        [IsImputedClockOut]       BIT                  NOT NULL CONSTRAINT [DF_Fact_Att_ImputedOut] DEFAULT (0),
        [IsNightShift]            BIT                  NOT NULL CONSTRAINT [DF_Fact_Att_NightShift] DEFAULT (0),
        [IsContractViolation]     BIT                  NOT NULL CONSTRAINT [DF_Fact_Att_Violation] DEFAULT (0),
        [CreatedAt]               DATETIME2(7)         NOT NULL CONSTRAINT [DF_Fact_Att_CreatedAt] DEFAULT (SYSUTCDATETIME()),
        CONSTRAINT [PK_Fact_DailyAttendance] PRIMARY KEY CLUSTERED ([AttendanceKey] ASC),
        CONSTRAINT [FK_Fact_Att_Date] FOREIGN KEY ([AccessDateKey]) REFERENCES [mart].[Dim_Date]([DateKey]),
        CONSTRAINT [FK_Fact_Att_Employee] FOREIGN KEY ([EmployeeKey]) REFERENCES [mart].[Dim_Employee]([EmployeeKey]),
        CONSTRAINT [FK_Fact_Att_Branch] FOREIGN KEY ([BranchKey]) REFERENCES [mart].[Dim_Branch]([BranchKey])
    );

    CREATE NONCLUSTERED INDEX [IX_Fact_Att_Date] ON [mart].[Fact_DailyAttendance] ([AccessDateKey] ASC);
    CREATE NONCLUSTERED INDEX [IX_Fact_Att_Employee] ON [mart].[Fact_DailyAttendance] ([EmployeeKey] ASC);
    CREATE NONCLUSTERED INDEX [IX_Fact_Att_Violation] ON [mart].[Fact_DailyAttendance] ([IsContractViolation] ASC);
END;
GO

-- 3. Fact_DepartmentBudget: Quarterly Aggregated Budget Targets (FP&A)
IF OBJECT_ID(N'[mart].[Fact_DepartmentBudget]', N'U') IS NULL
BEGIN
    CREATE TABLE [mart].[Fact_DepartmentBudget] (
        [BudgetKey]                 INT IDENTITY(1,1) NOT NULL,
        [FiscalYear]                SMALLINT          NOT NULL,
        [FiscalQuarter]             TINYINT           NOT NULL,
        [DateKey]                   INT               NOT NULL, -- First calendar date of quarter
        [DepartmentKey]             INT               NOT NULL,
        [BranchKey]                 INT               NOT NULL,
        [BudgetedHeadcount]         INT               NOT NULL,
        [AllocatedSalaryBudget_EGP] DECIMAL(18,2)     NOT NULL,
        [OvertimeAllowance_EGP]     DECIMAL(18,2)     NOT NULL CONSTRAINT [DF_Fact_Budget_OT] DEFAULT (0.00),
        [CreatedAt]                 DATETIME2(7)      NOT NULL CONSTRAINT [DF_Fact_Budget_CreatedAt] DEFAULT (SYSUTCDATETIME()),
        CONSTRAINT [PK_Fact_DepartmentBudget] PRIMARY KEY CLUSTERED ([BudgetKey] ASC),
        CONSTRAINT [FK_Fact_Budget_Date] FOREIGN KEY ([DateKey]) REFERENCES [mart].[Dim_Date]([DateKey]),
        CONSTRAINT [FK_Fact_Budget_Department] FOREIGN KEY ([DepartmentKey]) REFERENCES [mart].[Dim_Department]([DepartmentKey]),
        CONSTRAINT [FK_Fact_Budget_Branch] FOREIGN KEY ([BranchKey]) REFERENCES [mart].[Dim_Branch]([BranchKey])
    );

    CREATE NONCLUSTERED INDEX [IX_Fact_Budget_Quarter] ON [mart].[Fact_DepartmentBudget] ([FiscalYear] ASC, [FiscalQuarter] ASC);
    CREATE NONCLUSTERED INDEX [IX_Fact_Budget_Dept_Branch] ON [mart].[Fact_DepartmentBudget] ([DepartmentKey] ASC, [BranchKey] ASC);
END;
GO

-- 4. Fact_TrainingCompletions: Transactional Course Completions & Talent ROI
IF OBJECT_ID(N'[mart].[Fact_TrainingCompletions]', N'U') IS NULL
BEGIN
    CREATE TABLE [mart].[Fact_TrainingCompletions] (
        [CompletionKey]           BIGINT IDENTITY(1,1) NOT NULL,
        [CompletionDateKey]       INT                  NOT NULL,
        [EmployeeKey]             INT                  NOT NULL,
        [CourseKey]               INT                  NOT NULL,
        [AttemptNumber]           INT                  NOT NULL CONSTRAINT [DF_Fact_Train_Attempt] DEFAULT (1),
        [Score]                   DECIMAL(5,2)         NOT NULL,
        [IsPassed]                BIT                  NOT NULL,
        [CertificationCost_EGP]   DECIMAL(12,2)        NOT NULL CONSTRAINT [DF_Fact_Train_Cost] DEFAULT (0.00),
        [IsHighestScoreAttempt]   BIT                  NOT NULL CONSTRAINT [DF_Fact_Train_Highest] DEFAULT (1),
        [CreatedAt]               DATETIME2(7)         NOT NULL CONSTRAINT [DF_Fact_Train_CreatedAt] DEFAULT (SYSUTCDATETIME()),
        CONSTRAINT [PK_Fact_TrainingCompletions] PRIMARY KEY CLUSTERED ([CompletionKey] ASC),
        CONSTRAINT [FK_Fact_Train_Date] FOREIGN KEY ([CompletionDateKey]) REFERENCES [mart].[Dim_Date]([DateKey]),
        CONSTRAINT [FK_Fact_Train_Employee] FOREIGN KEY ([EmployeeKey]) REFERENCES [mart].[Dim_Employee]([EmployeeKey]),
        CONSTRAINT [FK_Fact_Train_Course] FOREIGN KEY ([CourseKey]) REFERENCES [mart].[Dim_Course]([CourseKey])
    );

    CREATE NONCLUSTERED INDEX [IX_Fact_Train_Employee] ON [mart].[Fact_TrainingCompletions] ([EmployeeKey] ASC);
    CREATE NONCLUSTERED INDEX [IX_Fact_Train_Course] ON [mart].[Fact_TrainingCompletions] ([CourseKey] ASC);
END;
GO
