-- =============================================================================
-- Enterprise Human Capital & Operational Efficiency Diagnostics
-- DDL Script 04: Software House & Multi-Currency Constellation Enrichment
-- Database Engine: Microsoft SQL Server (T-SQL)
-- Schemas: mart, raw, stg
-- =============================================================================

USE EnterpriseHR_DWH;
GO

SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
GO

-- 1. [mart].[Dim_CurrencyRates]: Conformed Multi-Currency Spot Rate Dimension
IF OBJECT_ID(N'[mart].[Dim_CurrencyRates]', N'U') IS NULL
BEGIN
    CREATE TABLE [mart].[Dim_CurrencyRates] (
        [CurrencyKey]         INT               NOT NULL,
        [CurrencyCode]        NVARCHAR(10)      NOT NULL,
        [CurrencyName]        NVARCHAR(100)     NOT NULL,
        [RateToEGP]           DECIMAL(18,4)     NOT NULL,
        [OneEGPInCurrency]    DECIMAL(18,6)     NOT NULL,
        [RateType]            NVARCHAR(50)      NOT NULL CONSTRAINT [DF_Dim_Currency_Type] DEFAULT (N'Central Bank Spot'),
        [LastUpdated]         DATETIME2(7)      NOT NULL CONSTRAINT [DF_Dim_Currency_Updated] DEFAULT (SYSUTCDATETIME()),
        CONSTRAINT [PK_Dim_CurrencyRates] PRIMARY KEY CLUSTERED ([CurrencyKey] ASC),
        CONSTRAINT [UQ_Dim_Currency_Code] UNIQUE NONCLUSTERED ([CurrencyCode] ASC)
    );
    PRINT 'Created table [mart].[Dim_CurrencyRates].';
END;
GO

-- 2. [mart].[Fact_ProjectTasks]: International Client Delivery & Milestone Tasks Fact
IF OBJECT_ID(N'[mart].[Fact_ProjectTasks]', N'U') IS NULL
BEGIN
    CREATE TABLE [mart].[Fact_ProjectTasks] (
        [TaskKey]                   BIGINT IDENTITY(1,1) NOT NULL,
        [TaskID]                    NVARCHAR(50)         NOT NULL,
        [ProjectID]                 NVARCHAR(50)         NOT NULL,
        [ProjectName]               NVARCHAR(150)        NOT NULL,
        [ClientName]                NVARCHAR(150)        NOT NULL,
        [ClientCountry]             NVARCHAR(100)        NOT NULL,
        [ClientRegion]              NVARCHAR(100)        NOT NULL,
        [Industry]                  NVARCHAR(100)        NOT NULL,
        [AssignedEmployeeID]        NVARCHAR(50)         NOT NULL,
        [CurrencyCode]              NVARCHAR(10)         NOT NULL CONSTRAINT [DF_Fact_Tasks_Curr] DEFAULT (N'USD'),
        [StartDateKey]              INT                  NULL,
        [DeadlineDateKey]           INT                  NULL,
        [CompletionDateKey]         INT                  NULL,
        [TaskTitle]                 NVARCHAR(200)        NOT NULL,
        [SkillDomain]               NVARCHAR(100)        NOT NULL,
        [ComplexityTier]            NVARCHAR(100)        NOT NULL,
        [PlannedHours]              DECIMAL(8,2)         NOT NULL,
        [ActualHours]               DECIMAL(8,2)         NOT NULL,
        [ScopeOverrunHours]         DECIMAL(8,2)         NOT NULL CONSTRAINT [DF_Fact_Tasks_OverrunH] DEFAULT (0.00),
        [ScopeOverrunPct]           DECIMAL(6,4)         NOT NULL CONSTRAINT [DF_Fact_Tasks_OverrunP] DEFAULT (0.0000),
        [IsHoursOverrun]            BIT                  NOT NULL CONSTRAINT [DF_Fact_Tasks_IsOverrun] DEFAULT (0),
        [BillableHourlyRate_USD]    DECIMAL(10,2)        NOT NULL,
        [TotalBilling_USD]          DECIMAL(18,2)        NOT NULL,
        [TotalBilling_EGP]          DECIMAL(18,2)        NOT NULL,
        [TaskStatus]                NVARCHAR(50)         NOT NULL,
        [ClientSatisfactionRating]  DECIMAL(3,2)         NULL,
        [IsDeliveryDelayed]         BIT                  NOT NULL CONSTRAINT [DF_Fact_Tasks_IsDelayed] DEFAULT (0),
        [CreatedAt]                 DATETIME2(7)         NOT NULL CONSTRAINT [DF_Fact_Tasks_CreatedAt] DEFAULT (SYSUTCDATETIME()),
        CONSTRAINT [PK_Fact_ProjectTasks] PRIMARY KEY CLUSTERED ([TaskKey] ASC),
        CONSTRAINT [UQ_Fact_ProjectTasks_TaskID] UNIQUE NONCLUSTERED ([TaskID] ASC)
    );

    CREATE NONCLUSTERED INDEX [IX_Fact_Tasks_Employee] ON [mart].[Fact_ProjectTasks] ([AssignedEmployeeID] ASC);
    CREATE NONCLUSTERED INDEX [IX_Fact_Tasks_Currency] ON [mart].[Fact_ProjectTasks] ([CurrencyCode] ASC);
    CREATE NONCLUSTERED INDEX [IX_Fact_Tasks_StartDate] ON [mart].[Fact_ProjectTasks] ([StartDateKey] ASC);
    CREATE NONCLUSTERED INDEX [IX_Fact_Tasks_Status] ON [mart].[Fact_ProjectTasks] ([TaskStatus] ASC) INCLUDE ([TotalBilling_USD], [ActualHours]);
    PRINT 'Created table [mart].[Fact_ProjectTasks].';
END;
GO

-- 3. [raw].[Client_Projects_Tasks]: Raw Staging Landing Zone for Client Tasks
IF OBJECT_ID(N'[raw].[Client_Projects_Tasks]', N'U') IS NULL
BEGIN
    CREATE TABLE [raw].[Client_Projects_Tasks] (
        [RawTaskID]                 BIGINT IDENTITY(1,1) NOT NULL,
        [TaskID]                    NVARCHAR(50)         NULL,
        [ProjectID]                 NVARCHAR(50)         NULL,
        [ProjectName]               NVARCHAR(150)        NULL,
        [ClientName]                NVARCHAR(150)        NULL,
        [ClientCountry]             NVARCHAR(100)        NULL,
        [ClientRegion]              NVARCHAR(100)        NULL,
        [Industry]                  NVARCHAR(100)        NULL,
        [AssignedEmployeeID]        NVARCHAR(50)         NULL,
        [TaskTitle]                 NVARCHAR(200)        NULL,
        [SkillDomain]               NVARCHAR(100)        NULL,
        [ComplexityTier]            NVARCHAR(100)        NULL,
        [PlannedHours]              DECIMAL(8,2)         NULL,
        [ActualHours]               DECIMAL(8,2)         NULL,
        [IsHoursOverrun]            BIT                  NULL,
        [BillableHourlyRate_USD]    DECIMAL(10,2)        NULL,
        [TotalBilling_USD]          DECIMAL(18,2)        NULL,
        [TaskStatus]                NVARCHAR(50)         NULL,
        [ClientSatisfactionRating]  DECIMAL(3,2)         NULL,
        [TaskStartDate]             DATE                 NULL,
        [DeliveryDeadline]          DATE                 NULL,
        [ActualCompletionDate]      DATE                 NULL,
        [IsDeliveryDelayed]         BIT                  NULL,
        [IngestedAt]                DATETIME2(7)         NOT NULL CONSTRAINT [DF_Raw_Tasks_Ingested] DEFAULT (SYSUTCDATETIME()),
        CONSTRAINT [PK_raw_Client_Projects_Tasks] PRIMARY KEY CLUSTERED ([RawTaskID] ASC)
    );
    PRINT 'Created table [raw].[Client_Projects_Tasks].';
END;
GO

-- 4. [raw].[Currency_Rates]: Raw Ingestion Table for Central Bank Exchange Rates
IF OBJECT_ID(N'[raw].[Currency_Rates]', N'U') IS NULL
BEGIN
    CREATE TABLE [raw].[Currency_Rates] (
        [RawCurrencyID]       INT IDENTITY(1,1) NOT NULL,
        [CurrencyCode]        NVARCHAR(10)      NOT NULL,
        [CurrencyName]        NVARCHAR(100)     NOT NULL,
        [RateToEGP]           DECIMAL(18,4)     NOT NULL,
        [OneEGPInCurrency]    DECIMAL(18,6)     NOT NULL,
        [RateType]            NVARCHAR(50)      NULL,
        [LastUpdated]         DATETIME2(7)      NULL,
        [IngestedAt]          DATETIME2(7)      NOT NULL CONSTRAINT [DF_Raw_Currency_Ingested] DEFAULT (SYSUTCDATETIME()),
        CONSTRAINT [PK_raw_Currency_Rates] PRIMARY KEY CLUSTERED ([RawCurrencyID] ASC)
    );
    PRINT 'Created table [raw].[Currency_Rates].';
END;
GO
