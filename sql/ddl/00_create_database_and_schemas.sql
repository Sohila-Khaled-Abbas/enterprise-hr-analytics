-- =============================================================================
-- Enterprise Human Capital & Operational Efficiency Diagnostics
-- DDL Script 00: Database & Logical Schemas Initialization
-- Database Engine: Microsoft SQL Server (T-SQL)
-- =============================================================================

-- 1. Create the Enterprise Data Warehouse database
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = N'EnterpriseHR_DWH')
BEGIN
    CREATE DATABASE EnterpriseHR_DWH;
END;
GO

USE EnterpriseHR_DWH;
GO

-- 2. Create logical schemas for layered data architecture
-- [raw]  : Raw ingestion layer / landing zone for external feeds
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N'raw')
BEGIN
    EXEC('CREATE SCHEMA raw;');
END;
GO

-- [stg]  : Staging layer for cleansing, type casting, deduplication, and heuristic imputation
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N'stg')
BEGIN
    EXEC('CREATE SCHEMA stg;');
END;
GO

-- [mart] : Production Dimensional Data Mart (Kimball Star Schema Dimensions & Facts)
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N'mart')
BEGIN
    EXEC('CREATE SCHEMA mart;');
END;
GO

-- 3. Verify schema creation
SELECT s.name AS SchemaName,
       s.schema_id AS SchemaID,
       u.name AS SchemaOwner
FROM sys.schemas s
INNER JOIN sys.sysusers u ON s.principal_id = u.uid
WHERE s.name IN ('raw', 'stg', 'mart');
GO
