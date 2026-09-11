-- =============================================================================
-- Enterprise Human Capital & Operational Efficiency Diagnostics
-- Master Execution Script: Database, Schemas, Tables, and Procedures
-- Database Engine: Microsoft SQL Server (T-SQL)
-- Architecture: Galaxy Schema (Fact Constellation)
-- =============================================================================

PRINT '=================================================================';
PRINT 'Starting EnterpriseHR_DWH Deployment & Migration Pipeline';
PRINT '=================================================================';

-- Step 1: Database & Schemas Initialization
PRINT 'Step 1: Initializing Database & Logical Schemas (raw, stg, mart)...';
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = N'EnterpriseHR_DWH')
BEGIN
    CREATE DATABASE EnterpriseHR_DWH;
    PRINT 'Database EnterpriseHR_DWH created.';
END
ELSE
BEGIN
    PRINT 'Database EnterpriseHR_DWH already exists.';
END
GO

USE EnterpriseHR_DWH;
GO

IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N'raw') EXEC('CREATE SCHEMA raw;');
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N'stg') EXEC('CREATE SCHEMA stg;');
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N'mart') EXEC('CREATE SCHEMA mart;');
PRINT 'Schemas raw, stg, mart verified.';
GO

-- Step 2: Verification of Schemas
SELECT s.name AS SchemaName, s.schema_id AS SchemaID, u.name AS SchemaOwner
FROM sys.schemas s
INNER JOIN sys.sysusers u ON s.principal_id = u.uid
WHERE s.name IN ('raw', 'stg', 'mart');
GO

PRINT '=================================================================';
PRINT 'Migration Script Completed Successfully.';
PRINT 'Proceed to execute DDL scripts 01_dimensions.sql, 02_facts.sql, and 03_staging_tables.sql';
PRINT '=================================================================';
GO
