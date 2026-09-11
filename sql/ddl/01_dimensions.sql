-- =============================================================================
-- Enterprise Human Capital & Operational Efficiency Diagnostics
-- DDL Script 01: Star Schema Dimensions
-- Database Engine: Microsoft SQL Server (T-SQL)
-- Schema: mart
-- =============================================================================

USE EnterpriseHR_DWH;
GO

SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
GO

-- 1. Dim_Department: Department & Cost Center Dimension
IF OBJECT_ID(N'[mart].[Dim_Department]', N'U') IS NULL
BEGIN
    CREATE TABLE [mart].[Dim_Department] (
        [DepartmentKey]       INT IDENTITY(1,1) NOT NULL,
        [DepartmentID]        NVARCHAR(50)      NOT NULL,
        [DepartmentName]      NVARCHAR(100)     NOT NULL,
        [Division]            NVARCHAR(100)     NOT NULL CONSTRAINT [DF_Dim_Department_Division] DEFAULT (N'Corporate Services'),
        [CostCenterCode]      NVARCHAR(50)      NULL,
        [CreatedAt]           DATETIME2(7)      NOT NULL CONSTRAINT [DF_Dim_Department_CreatedAt] DEFAULT (SYSUTCDATETIME()),
        CONSTRAINT [PK_Dim_Department] PRIMARY KEY CLUSTERED ([DepartmentKey] ASC),
        CONSTRAINT [UQ_Dim_Department_ID] UNIQUE NONCLUSTERED ([DepartmentID] ASC)
    );
END;
GO

-- 2. Dim_Branch: Geographic Branch & Regional Office Dimension
IF OBJECT_ID(N'[mart].[Dim_Branch]', N'U') IS NULL
BEGIN
    CREATE TABLE [mart].[Dim_Branch] (
        [BranchKey]           INT IDENTITY(1,1) NOT NULL,
        [BranchID]            NVARCHAR(50)      NOT NULL,
        [BranchName]          NVARCHAR(100)     NOT NULL, -- Localized name (e.g. فرع المعادي)
        [CanonicalName]       NVARCHAR(100)     NOT NULL, -- Standardized name for fuzzy reconciliation
        [Region]              NVARCHAR(100)     NOT NULL, -- Greater Cairo, Alexandria, Delta, Upper Egypt
        [City]                NVARCHAR(100)     NOT NULL,
        [Capacity]            INT               NOT NULL CONSTRAINT [DF_Dim_Branch_Capacity] DEFAULT (0),
        [CreatedAt]           DATETIME2(7)      NOT NULL CONSTRAINT [DF_Dim_Branch_CreatedAt] DEFAULT (SYSUTCDATETIME()),
        CONSTRAINT [PK_Dim_Branch] PRIMARY KEY CLUSTERED ([BranchKey] ASC),
        CONSTRAINT [UQ_Dim_Branch_ID] UNIQUE NONCLUSTERED ([BranchID] ASC)
    );
END;
GO

-- 3. Dim_Course: Learning & Talent Development Catalog Dimension
IF OBJECT_ID(N'[mart].[Dim_Course]', N'U') IS NULL
BEGIN
    CREATE TABLE [mart].[Dim_Course] (
        [CourseKey]           INT IDENTITY(1,1) NOT NULL,
        [CourseID]            NVARCHAR(50)      NOT NULL,
        [CourseName]          NVARCHAR(200)     NOT NULL,
        [SkillDomain]         NVARCHAR(100)     NOT NULL, -- Tech, Soft Skills, Leadership, Compliance
        [TargetCompetency]    NVARCHAR(150)     NULL,
        [EstimatedHours]      DECIMAL(6,2)      NOT NULL CONSTRAINT [DF_Dim_Course_Hours] DEFAULT (0.00),
        [CreatedAt]           DATETIME2(7)      NOT NULL CONSTRAINT [DF_Dim_Course_CreatedAt] DEFAULT (SYSUTCDATETIME()),
        CONSTRAINT [PK_Dim_Course] PRIMARY KEY CLUSTERED ([CourseKey] ASC),
        CONSTRAINT [UQ_Dim_Course_ID] UNIQUE NONCLUSTERED ([CourseID] ASC)
    );
END;
GO

-- 4. Dim_Date: Enterprise Standard Calendar Dimension
IF OBJECT_ID(N'[mart].[Dim_Date]', N'U') IS NULL
BEGIN
    CREATE TABLE [mart].[Dim_Date] (
        [DateKey]             INT           NOT NULL, -- Smart Key: YYYYMMDD
        [FullDate]            DATE          NOT NULL,
        [DayNumberOfWeek]     TINYINT       NOT NULL,
        [DayNameOfWeek]       NVARCHAR(20)  NOT NULL,
        [DayNumberOfMonth]    TINYINT       NOT NULL,
        [DayNumberOfYear]     SMALLINT      NOT NULL,
        [MonthName]           NVARCHAR(20)  NOT NULL,
        [MonthNumberOfYear]   TINYINT       NOT NULL,
        [CalendarQuarter]     TINYINT       NOT NULL,
        [CalendarYear]        SMALLINT      NOT NULL,
        [FiscalQuarter]       TINYINT       NOT NULL,
        [FiscalYear]          SMALLINT      NOT NULL,
        [IsWeekend]           BIT           NOT NULL CONSTRAINT [DF_Dim_Date_IsWeekend] DEFAULT (0),
        [IsWorkingDay]        BIT           NOT NULL CONSTRAINT [DF_Dim_Date_IsWorkingDay] DEFAULT (1),
        CONSTRAINT [PK_Dim_Date] PRIMARY KEY CLUSTERED ([DateKey] ASC),
        CONSTRAINT [UQ_Dim_Date_FullDate] UNIQUE NONCLUSTERED ([FullDate] ASC)
    );
END;
GO

-- 5. Dim_Employee: Slowly Changing Dimension (SCD Type 2)
IF OBJECT_ID(N'[mart].[Dim_Employee]', N'U') IS NULL
BEGIN
    CREATE TABLE [mart].[Dim_Employee] (
        [EmployeeKey]         INT IDENTITY(1,1) NOT NULL, -- Surrogate Key
        [EmployeeID]          NVARCHAR(50)      NOT NULL, -- Natural Key (الرقم التعريفي)
        [FullName]            NVARCHAR(150)     NOT NULL, -- (الاسم)
        [Age]                 INT               NULL,     -- (السن)
        [Gender]              NVARCHAR(20)      NULL,     -- (الجنس)
        [JobRole]             NVARCHAR(100)     NOT NULL, -- (المسمى الوظيفي)
        [DepartmentKey]       INT               NOT NULL,
        [BranchKey]           INT               NOT NULL,
        [HireDate]            DATE              NOT NULL, -- (تاريخ التعيين)
        [BaseSalary]          DECIMAL(18,2)     NOT NULL, -- (الراتب الأساسي)
        [Currency]            NVARCHAR(10)      NOT NULL CONSTRAINT [DF_Dim_Employee_Currency] DEFAULT (N'EGP'), -- (العملة)
        [ContractType]        NVARCHAR(50)      NOT NULL, -- (نوع العقد: دوام كامل (حضوري), هجين, etc.)
        [MaritalStatus]       NVARCHAR(50)      NULL,     -- (الحالة الاجتماعية)
        [Email]               NVARCHAR(150)     NULL,     -- (البريد الإلكتروني)
        [EffectiveDate]       DATE              NOT NULL, -- SCD Type 2 Valid From
        [ExpiryDate]          DATE              NOT NULL CONSTRAINT [DF_Dim_Employee_Expiry] DEFAULT ('9999-12-31'), -- SCD Type 2 Valid To
        [IsCurrent]           BIT               NOT NULL CONSTRAINT [DF_Dim_Employee_IsCurrent] DEFAULT (1),
        [CreatedAt]           DATETIME2(7)      NOT NULL CONSTRAINT [DF_Dim_Employee_CreatedAt] DEFAULT (SYSUTCDATETIME()),
        CONSTRAINT [PK_Dim_Employee] PRIMARY KEY CLUSTERED ([EmployeeKey] ASC),
        CONSTRAINT [FK_Dim_Employee_Department] FOREIGN KEY ([DepartmentKey]) REFERENCES [mart].[Dim_Department]([DepartmentKey]),
        CONSTRAINT [FK_Dim_Employee_Branch] FOREIGN KEY ([BranchKey]) REFERENCES [mart].[Dim_Branch]([BranchKey])
    );

    CREATE NONCLUSTERED INDEX [IX_Dim_Employee_NaturalKey] ON [mart].[Dim_Employee] ([EmployeeID] ASC);
    CREATE NONCLUSTERED INDEX [IX_Dim_Employee_Current] ON [mart].[Dim_Employee] ([EmployeeID] ASC, [IsCurrent] ASC) INCLUDE ([DepartmentKey], [BranchKey], [BaseSalary]);
END;
GO
