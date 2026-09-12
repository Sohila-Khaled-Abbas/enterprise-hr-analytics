-- =============================================================================
-- Enterprise Human Capital & Operational Efficiency Diagnostics
-- DDL Script 03: Staging Layer Tables
-- Database Engine: Microsoft SQL Server (T-SQL)
-- Schema: stg
-- =============================================================================

USE EnterpriseHR_DWH;
GO

SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
GO

-- 1. [stg].[Employees_Core]: Core HR Master Ingestion (Mapped from Arabic Schema)
IF OBJECT_ID(N'[stg].[Employees_Core]', N'U') IS NULL
BEGIN
    CREATE TABLE [stg].[Employees_Core] (
        [StagingID]               INT IDENTITY(1,1) NOT NULL,
        [الاسم]                   NVARCHAR(150)     NULL, -- FullName
        [الرقم التعريفي]          NVARCHAR(50)      NOT NULL, -- EmployeeID
        [السن]                    INT               NULL, -- Age
        [الجنس]                   NVARCHAR(20)      NULL, -- Gender
        [المسمى الوظيفي]          NVARCHAR(100)     NULL, -- JobTitle
        [القسم]                   NVARCHAR(100)     NULL, -- Department
        [الفرع]                   NVARCHAR(100)     NULL, -- Branch
        [تاريخ التعيين]           DATE              NULL, -- HireDate
        [الراتب الأساسي]          DECIMAL(18,2)     NULL, -- BaseSalary
        [العملة]                  NVARCHAR(10)      NULL, -- Currency
        [نوع العقد]               NVARCHAR(50)      NULL, -- ContractType
        [تقييم الأداء السنوي]     DECIMAL(4,2)      NULL, -- AnnualPerformanceRating
        [الحالة الاجتماعية]       NVARCHAR(50)      NULL, -- MaritalStatus
        [البريد الإلكتروني]       NVARCHAR(150)     NULL, -- Email
        [IngestedAt]              DATETIME2(7)      NOT NULL CONSTRAINT [DF_Stg_Emp_Ingested] DEFAULT (SYSUTCDATETIME()),
        CONSTRAINT [PK_stg_Employees_Core] PRIMARY KEY CLUSTERED ([StagingID] ASC)
    );

    CREATE NONCLUSTERED INDEX [IX_stg_Employees_ID] ON [stg].[Employees_Core] ([الرقم التعريفي] ASC);
END;
GO

-- 2. [stg].[Daily_Attendance_Logs]: IoT Badge & Access Logs (Raw JSON Ingestion)
IF OBJECT_ID(N'[stg].[Daily_Attendance_Logs]', N'U') IS NULL
BEGIN
    CREATE TABLE [stg].[Daily_Attendance_Logs] (
        [LogID]                   BIGINT IDENTITY(1,1) NOT NULL,
        [EmployeeID]              NVARCHAR(50)         NOT NULL,
        [AccessDate]              DATE                 NOT NULL,
        [CheckInTime]             TIME(0)              NULL,
        [CheckOutTime]            TIME(0)              NULL,
        [BuildingID]              NVARCHAR(50)         NULL,
        [DeclaredWorkMode]        NVARCHAR(50)         NULL, -- On-site, Remote, Field
        [RawPayloadJSON]          NVARCHAR(MAX)        NULL,
        [IngestedAt]              DATETIME2(7)         NOT NULL CONSTRAINT [DF_Stg_Att_Ingested] DEFAULT (SYSUTCDATETIME()),
        CONSTRAINT [PK_stg_Daily_Attendance_Logs] PRIMARY KEY CLUSTERED ([LogID] ASC)
    );

    CREATE NONCLUSTERED INDEX [IX_stg_Att_EmpDate] ON [stg].[Daily_Attendance_Logs] ([EmployeeID] ASC, [AccessDate] ASC);
END;
GO

-- 3. [stg].[Exit_Attrition_Records]: Historical Exit & Resignation Audits
IF OBJECT_ID(N'[stg].[Exit_Attrition_Records]', N'U') IS NULL
BEGIN
    CREATE TABLE [stg].[Exit_Attrition_Records] (
        [ExitAuditID]             INT IDENTITY(1,1) NOT NULL,
        [EmployeeID]              NVARCHAR(50)      NOT NULL,
        [NoticeDate]              DATE              NULL,
        [ExitDate]                DATE              NOT NULL,
        [ExitType]                NVARCHAR(50)      NOT NULL, -- Voluntary / Involuntary
        [PrimaryExitReason]       NVARCHAR(100)     NOT NULL, -- Compensation, Management, Relocation, Burnout
        [LastPerformanceScore]    DECIMAL(4,2)      NULL,
        [RehireEligible]          BIT               NOT NULL CONSTRAINT [DF_Stg_Exit_Rehire] DEFAULT (1),
        [SeparationSalary]        DECIMAL(18,2)     NULL,
        [SeparationBranch]        NVARCHAR(100)     NULL,
        [IngestedAt]              DATETIME2(7)      NOT NULL CONSTRAINT [DF_Stg_Exit_Ingested] DEFAULT (SYSUTCDATETIME()),
        CONSTRAINT [PK_stg_Exit_Attrition] PRIMARY KEY CLUSTERED ([ExitAuditID] ASC)
    );

    CREATE NONCLUSTERED INDEX [IX_stg_Exit_Emp] ON [stg].[Exit_Attrition_Records] ([EmployeeID] ASC);
END;
GO

-- 4. [stg].[FP_A_Department_Budgets_Wide]: Messy Finance Plan Shared Excel Landing
IF OBJECT_ID(N'[stg].[FP_A_Department_Budgets_Wide]', N'U') IS NULL
BEGIN
    CREATE TABLE [stg].[FP_A_Department_Budgets_Wide] (
        [ImportID]                INT IDENTITY(1,1) NOT NULL,
        [FiscalYear]              SMALLINT          NOT NULL,
        [Department]              NVARCHAR(100)     NOT NULL,
        [RawBranch]               NVARCHAR(100)     NOT NULL, -- Non-standardized branch strings (e.g. فرع المعادي)
        [Q1_Budget_EGP]           DECIMAL(18,2)     NULL,
        [Q2_Budget_EGP]           DECIMAL(18,2)     NULL,
        [Q3_Budget_EGP]           DECIMAL(18,2)     NULL,
        [Q4_Budget_EGP]           DECIMAL(18,2)     NULL,
        [Q1_Headcount]            INT               NULL,
        [Q2_Headcount]            INT               NULL,
        [Q3_Headcount]            INT               NULL,
        [Q4_Headcount]            INT               NULL,
        [OvertimeAllowance_EGP]   DECIMAL(18,2)     NULL,
        [SourceFileName]          NVARCHAR(260)     NULL,
        [IngestedAt]              DATETIME2(7)      NOT NULL CONSTRAINT [DF_Stg_Budget_Ingested] DEFAULT (SYSUTCDATETIME()),
        CONSTRAINT [PK_stg_FP_A_Budgets_Wide] PRIMARY KEY CLUSTERED ([ImportID] ASC)
    );
END;
GO

-- 5. [stg].[LMS_Course_Completions]: Learning Management Platform Transactional Feed
IF OBJECT_ID(N'[stg].[LMS_Course_Completions]', N'U') IS NULL
BEGIN
    CREATE TABLE [stg].[LMS_Course_Completions] (
        [AttemptID]               BIGINT IDENTITY(1,1) NOT NULL,
        [EmployeeID]              NVARCHAR(50)         NOT NULL,
        [CourseID]                NVARCHAR(50)         NOT NULL,
        [CourseName]              NVARCHAR(200)        NOT NULL,
        [SkillDomain]             NVARCHAR(100)        NOT NULL,
        [CompletionDate]          DATE                 NOT NULL,
        [Score]                   DECIMAL(5,2)         NOT NULL,
        [CertificationCost_EGP]   DECIMAL(12,2)        NOT NULL CONSTRAINT [DF_Stg_LMS_Cost] DEFAULT (0.00),
        [IngestedAt]              DATETIME2(7)         NOT NULL CONSTRAINT [DF_Stg_LMS_Ingested] DEFAULT (SYSUTCDATETIME()),
        CONSTRAINT [PK_stg_LMS_Course_Completions] PRIMARY KEY CLUSTERED ([AttemptID] ASC)
    );

    CREATE NONCLUSTERED INDEX [IX_stg_LMS_EmpCourse] ON [stg].[LMS_Course_Completions] ([EmployeeID] ASC, [CourseID] ASC);
END;
GO

-- 6. [stg].[Stg_HR_Audit]: Cleansed & Deduplicated SCD Type 2 HR Event Log
IF OBJECT_ID(N'[stg].[Stg_HR_Audit]', N'U') IS NULL
BEGIN
    CREATE TABLE [stg].[Stg_HR_Audit] (
        [StagingKey]              INT IDENTITY(1,1)    NOT NULL,
        [EmployeeID]              VARCHAR(20)          NOT NULL,
        [EventType]               VARCHAR(50)          NOT NULL,
        [ValidFrom]               DATE                 NOT NULL,
        [ValidTo]                 DATE                 NOT NULL,
        [IsCurrent]               BIT                  NOT NULL,
        [BranchOrSalaryContext]   NVARCHAR(150)        NULL,
        [Salary_EGP]              DECIMAL(18,2)        NULL,
        [IsTerminated]            INT                  NULL,
        [IngestedAt]              DATETIME2(7)         NOT NULL CONSTRAINT [DF_Stg_Audit_Ingested] DEFAULT (SYSUTCDATETIME()),
        CONSTRAINT [PK_stg_Stg_HR_Audit] PRIMARY KEY CLUSTERED ([StagingKey] ASC)
    );

    CREATE NONCLUSTERED INDEX [IX_Stg_HR_Audit_Emp_Valid] ON [stg].[Stg_HR_Audit] ([EmployeeID] ASC, [ValidFrom] ASC, [ValidTo] ASC);
END;
GO

