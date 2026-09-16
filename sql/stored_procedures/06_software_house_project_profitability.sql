-- =============================================================================
-- Enterprise Human Capital & Software House Analytics
-- Stored Procedure: 06_software_house_project_profitability.sql
-- Database: EnterpriseHR_DWH | Schema: mart
-- Purpose: Analyzes client engagement profitability, delivery overruns,
--          effective hourly billing realization, and currency conversion impact.
-- =============================================================================

USE EnterpriseHR_DWH;
GO

SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
GO

CREATE OR ALTER PROCEDURE [mart].[usp_Analyze_Project_Delivery_Profitability]
    @ClientNamePattern   NVARCHAR(100) = NULL,
    @MinOverrunHours     DECIMAL(8,2)  = 0.0,
    @BaseCurrencyCode    NVARCHAR(10)  = 'USD'
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        -- 1. Fetch current exchange rate for currency conversion
        DECLARE @FxRateToEGP DECIMAL(18,4) = 48.85;

        SELECT TOP 1 @FxRateToEGP = RateToEGP
        FROM [mart].[Dim_CurrencyRates]
        WHERE CurrencyCode = @BaseCurrencyCode;

        -- 2. Execute aggregated profitability and delivery performance diagnostics
        SELECT 
            t.[ProjectID],
            t.[ProjectName],
            t.[ClientName],
            t.[TaskStatus],
            COUNT(t.[TaskKey]) AS [TotalTasks],
            
            -- Effort diagnostics
            SUM(t.[PlannedHours]) AS [TotalPlannedHours],
            SUM(t.[ActualHours]) AS [TotalActualHours],
            SUM(t.[ScopeOverrunHours]) AS [TotalOverrunHours],
            CASE 
                WHEN SUM(t.[PlannedHours]) > 0 
                THEN CAST((SUM(t.[ScopeOverrunHours]) / SUM(t.[PlannedHours])) * 100.0 AS DECIMAL(6,2))
                ELSE 0.00 
            END AS [OverrunPercentage],

            -- Financial realization
            AVG(t.[BillableHourlyRate_USD]) AS [AvgBillingRateUSD],
            SUM(t.[TotalBilling_USD]) AS [GrossRevenueUSD],
            SUM(t.[TotalBilling_EGP]) AS [GrossRevenueEGP],

            -- Delivery risk & client sentiment
            SUM(CASE WHEN t.[IsDeliveryDelayed] = 1 THEN 1 ELSE 0 END) AS [DelayedTaskCount],
            CAST(
                (SUM(CASE WHEN t.[IsDeliveryDelayed] = 1 THEN 1.0 ELSE 0.0 END) / COUNT(t.[TaskKey])) * 100.0 
                AS DECIMAL(5,2)
            ) AS [DelayRatioPct],
            AVG(t.[ClientSatisfactionRating]) AS [AvgCSAT]

        FROM [mart].[Fact_ProjectTasks] t
        WHERE (@ClientNamePattern IS NULL OR t.[ClientName] LIKE '%' + @ClientNamePattern + '%')
        GROUP BY 
            t.[ProjectID],
            t.[ProjectName],
            t.[ClientName],
            t.[TaskStatus]
        HAVING SUM(t.[ScopeOverrunHours]) >= @MinOverrunHours
        ORDER BY [GrossRevenueUSD] DESC, [TotalOverrunHours] DESC;

    END TRY
    BEGIN CATCH
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        DECLARE @ErrorSeverity INT = ERROR_SEVERITY();
        DECLARE @ErrorState INT = ERROR_STATE();

        RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH
END;
GO
