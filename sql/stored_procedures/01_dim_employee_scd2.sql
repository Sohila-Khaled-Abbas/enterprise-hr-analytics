-- =============================================================================
-- Enterprise Human Capital & Operational Efficiency Diagnostics
-- Transformation Script 01: Dim_Employee Slowly Changing Dimension (SCD Type 2)
-- Database Engine: Microsoft SQL Server (T-SQL)
-- Architecture: Galaxy Schema (Fact Constellation)
-- =============================================================================

USE EnterpriseHR_DWH;
GO

SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;
GO

CREATE OR ALTER PROCEDURE [stg].[usp_Transform_Dim_Employee_SCD2]
    @BatchDate DATE = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    IF @BatchDate IS NULL
        SET @BatchDate = CAST(SYSUTCDATETIME() AS DATE);

    BEGIN TRANSACTION;

    BEGIN TRY
        -- 1. Identify Changed or New Records by joining staging to active dimension
        WITH StagedCore AS (
            SELECT 
                s.[الرقم التعريفي]        AS EmployeeID,
                s.[الاسم]                 AS FullName,
                s.[السن]                  AS Age,
                s.[الجنس]                 AS Gender,
                s.[المسمى الوظيفي]        AS JobRole,
                d.[DepartmentKey],
                b.[BranchKey],
                s.[تاريخ التعيين]         AS HireDate,
                s.[الراتب الأساسي]        AS BaseSalary,
                ISNULL(s.[العملة], N'EGP') AS Currency,
                s.[نوع العقد]             AS ContractType,
                s.[الحالة الاجتماعية]     AS MaritalStatus,
                s.[البريد الإلكتروني]     AS Email
            FROM [stg].[Employees_Core] s
            INNER JOIN [mart].[Dim_Department] d 
                ON s.[القسم] = d.[DepartmentName]
            INNER JOIN [mart].[Dim_Branch] b 
                ON s.[الفرع] = b.[BranchName]
        ),
        ChangedEmployees AS (
            SELECT 
                src.*,
                dim.[EmployeeKey] AS ExistingKey,
                dim.[BaseSalary]  AS OldSalary,
                dim.[BranchKey]   AS OldBranchKey,
                dim.[JobRole]     AS OldJobRole
            FROM StagedCore src
            INNER JOIN [mart].[Dim_Employee] dim
                ON src.[EmployeeID] = dim.[EmployeeID]
               AND dim.[IsCurrent] = 1
            WHERE src.[BaseSalary]   <> dim.[BaseSalary]
               OR src.[BranchKey]    <> dim.[BranchKey]
               OR src.[JobRole]      <> dim.[JobRole]
               OR src.[ContractType] <> dim.[ContractType]
        )
        -- 2. Expire old records in Dim_Employee
        UPDATE dim
        SET 
            dim.[ExpiryDate] = DATEADD(DAY, -1, @BatchDate),
            dim.[IsCurrent]  = 0
        FROM [mart].[Dim_Employee] dim
        INNER JOIN ChangedEmployees chg
            ON dim.[EmployeeKey] = chg.[ExistingKey];

        -- 3. Insert new versions of changed records and completely new employees
        INSERT INTO [mart].[Dim_Employee] (
            [EmployeeID],
            [FullName],
            [Age],
            [Gender],
            [JobRole],
            [DepartmentKey],
            [BranchKey],
            [HireDate],
            [BaseSalary],
            [Currency],
            [ContractType],
            [MaritalStatus],
            [Email],
            [EffectiveDate],
            [ExpiryDate],
            [IsCurrent]
        )
        SELECT 
            src.[الرقم التعريفي]        AS EmployeeID,
            src.[الاسم]                 AS FullName,
            src.[السن]                  AS Age,
            src.[الجنس]                 AS Gender,
            src.[المسمى الوظيفي]        AS JobRole,
            d.[DepartmentKey],
            b.[BranchKey],
            src.[تاريخ التعيين]         AS HireDate,
            src.[الراتب الأساسي]        AS BaseSalary,
            ISNULL(src.[العملة], N'EGP') AS Currency,
            src.[نوع العقد]             AS ContractType,
            src.[الحالة الاجتماعية]     AS MaritalStatus,
            src.[البريد الإلكتروني]     AS Email,
            @BatchDate                  AS EffectiveDate,
            '9999-12-31'                AS ExpiryDate,
            1                           AS IsCurrent
        FROM [stg].[Employees_Core] src
        INNER JOIN [mart].[Dim_Department] d 
            ON src.[القسم] = d.[DepartmentName]
        INNER JOIN [mart].[Dim_Branch] b 
            ON src.[الفرع] = b.[BranchName]
        LEFT JOIN [mart].[Dim_Employee] dim
            ON src.[الرقم التعريفي] = dim.[EmployeeID]
           AND dim.[IsCurrent] = 1
        WHERE dim.[EmployeeKey] IS NULL; -- Either brand new or expired in step 2

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO
