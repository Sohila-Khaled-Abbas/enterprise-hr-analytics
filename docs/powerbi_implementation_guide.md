# Enterprise Power BI Implementation & Analytical Diagnostics Masterclass
### Building a Kimball Galaxy Schema (Fact Constellation) from Raw Data with Full GUI & DAX Guidance

---

## 🎯 Executive Overview & Analytical Philosophy

In enterprise workforce analytics, data engineering is rarely clean. The operational reality of human capital analytics spans **5 heterogeneous, conflicting source systems** operating at disparate frequencies and grains:

```
                               ┌──────────────────────────────────────────────┐
                               │           RAW SOURCE LANDING ZONE            │
                               ├──────────────────────────────────────────────┤
                               │ • Raw Core HR Master (7,000 Arabic rows)     │
                               │ • Daily IoT Badge Access Logs (JSON streams) │
                               │ • Relational Exit Audits (SQL Server OLTP)   │
                               │ • FP&A Budget Worksheets (Messy Wide Excel)  │
                               │ • LMS Platform Course Records (REST / CSV)   │
                               └──────────────────────┬───────────────────────┘
                                                      │ Power Query Editor GUI
                                                      ▼
                               ┌──────────────────────────────────────────────┐
                               │     KIMBALL GALAXY SCHEMA (CONSTELLATION)    │
                               ├──────────────────────────────────────────────┤
                               │ Conformed Dimensions:                        │
                               │   Dim_Employee (SCD-2) │ Dim_Department      │
                               │   Dim_Branch           │ Dim_Date (Calendar) │
                               │   Dim_Course                                 │
                               │                                              │
                               │ Fact Tables:                                 │
                               │   Fact_WorkforceSnapshot (Monthly)           │
                               │   Fact_DailyAttendance   (Daily IoT)         │
                               │   Fact_DepartmentBudget  (Quarterly FP&A)    │
                               │   Fact_TrainingCompletions (Transactional)   │
                               └──────────────────────┬───────────────────────┘
                                                      │ Model View & DAX Engine
                                                      ▼
                               ┌──────────────────────────────────────────────┐
                               │       ENTERPRISE ANALYTICAL DIAGNOSTICS      │
                               ├──────────────────────────────────────────────┤
                               │ 1. Salary Compression & Flight Risk Index    │
                               │ 2. Bi-Temporal Budget & Headcount Variance   │
                               │ 3. Policy Compliance & Ghost Worker Audits   │
                               │ 4. Upskilling Velocity & Training ROI        │
                               │ 5. Survivorship Bias & Regrettable Loss      │
                               └──────────────────────┬───────────────────────┘
                                                      │ Report View GUI (1920x1080)
                                                      ▼
                               ┌──────────────────────────────────────────────┐
                               │          WEB APP STYLE DASHBOARD UI/UX       │
                               │ Persistent Sidebar │ Hero Cards │ 360° Dossier│
                               └──────────────────────────────────────────────┘
```

This guide equips you with:
1. **Critical Analytical Thinking Frameworks** to diagnose executive business problems before writing code.
2. **Step-by-Step Power Query GUI Clickpaths** to transform messy raw data into a pristine **Kimball Galaxy Schema** without being forced to write manual M code from scratch.
3. **Model View GUI Configuration** to wire up conformed dimensions, inactive relationships, and measure display folders.
4. **Advanced DAX Diagnostic Formulas** with deep context-transition explanations.
5. **Modern Web App-Style UI/UX Design** click-by-click instructions in the Report View GUI.

---

## 🧠 Module 1: Developing Enterprise Analytical Acumen

Before opening any software, elite analytics engineers analyze the **underlying operational friction**. Enterprise people analytics is uniquely challenging because human and organizational behavior introduces systemic data traps:

### Diagnostic Trap 1: The New-Hire Loyalty Penalty (Salary Compression)
* **The Business Reality**: When market wages escalate rapidly due to inflation or talent shortages, companies hire new staff at elevated rates. Long-tenured employees who receive standard annual merit increases (e.g. 5–8%) fall behind the market rate.
* **The Analytical Insight**: If an employee with 5 years of tenure earns less than the 50th percentile of brand-new hires in the exact same role, they suffer from **Salary Compression (Wage Inversion)**. If that employee is also a top performer (Rating $\ge 4.0$), their voluntary resignation probability is nearly 80%.
* **The Business Cost**: Replacing an experienced employee costs 1.5× to 2× their annual salary in lost institutional productivity, recruiter fees, and ramp-up time.

### Diagnostic Trap 2: Fact-to-Fact Granularity Collisions
* **The Business Reality**: Finance plans budgets quarterly by branch and department (e.g., *Cairo East Branch - Sales - 2026 Q1: Budget 5,400,000 EGP, Target Headcount: 85*). Meanwhile, Payroll and HR operate on individual employees at the monthly level.
* **The Analytical Insight**: If you attempt to merge the Finance budget table directly into the employee table, Power BI creates a Many-to-Many circular relationship or inflates budget figures 85 times!
* **The Solution**: A **Galaxy Schema** where neither fact table touches the other. Both fact tables connect strictly to **Conformed Dimensions** (`Dim_Department`, `Dim_Branch`, `Dim_Date`). All cross-grain calculations are evaluated through DAX measures.

### Diagnostic Trap 3: Survivorship Bias & Ghost Payroll Leakage
* **The Business Reality**: An active employee table only shows people who currently exist in the system today. Looking only at the active table makes turnover appear lower than reality (**Survivorship Bias**). Furthermore, employees who left or abandoned their posts can remain erroneously marked "Active" in ERP systems for months while direct deposit paychecks continue (**Ghost Workers**).
* **The Analytical Insight**: By cross-referencing physical badge IoT turnstile swipes against active payroll status, any employee with $\ge 60$ consecutive days of zero physical or virtual system access is flagged as an active ghost worker, preventing massive financial leakage.

---

## 🖱️ Module 2: Power Query Editor GUI Masterclass (Raw Data to Galaxy Schema)

You do not need to write complex M scripts manually. Power BI Desktop's **Power Query Editor GUI** provides full visual capabilities to build the entire Galaxy Schema.

Open Power BI Desktop and click **Home > Transform Data** to enter Power Query Editor.

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ File  Home  Transform  Add Column  View  Tools  Help                                                   │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [Close & Apply] [New Source] [Enter Data] [Manage Parameters] [Merge Queries ▼] [Append Queries ▼]    │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### Step 2.1: Ingesting & Cleansing Raw Core HR (`Dim_Employee`)

1. In the **Home** ribbon, click **New Source > Text/CSV**.
2. Browse to `data/raw/employees_core.csv` and click **Open**. Verify file origin is set to **65001: Unicode (UTF-8)** and click **OK**.
3. In the left **Queries** pane, right-click the imported query and select **Rename**; name it `Dim_Employee`.
4. **Setting Correct Data Types via GUI**:
   * Click the column header icon next to **`السن`** (Age) and select **Whole Number (`123`)**.
   * Click the column header icon next to **`تاريخ التعيين`** (Hire Date) and select **Date (`📅`)**.
   * Click the column header icon next to **`الراتب الأساسي`** (Base Salary) and select **Fixed Decimal Number (`$`)**.
   * Click the column header icon next to **`تقييم الأداء السنوي`** (Performance Rating) and select **Decimal Number (`1.2`)**.
5. **Adding Surrogate Primary Key (`EmployeeKey`) via GUI**:
   * Switch to the **Add Column** ribbon tab at the top.
   * Click **Index Column > From 1**.
   * A new column named `Index` appears at the right. Right-click its header, select **Rename**, and type `EmployeeKey`.
   * Drag the `EmployeeKey` column to make it the very first column on the left.
6. **Configuring SCD Type 2 Attributes via GUI**:
   * Go to **Add Column > Custom Column**.
   * In the dialog, set *New column name* to `EffectiveDate`. In the formula box, double-click `[تاريخ التعيين]` from the available columns list. Click **OK**.
   * Click **Add Column > Custom Column**.
   * Set *New column name* to `ExpiryDate`. In the formula box, enter:
     `#date(9999, 12, 31)`
   * Click **OK**. Set the data type of both columns to **Date (`📅`)**.
   * Click **Add Column > Custom Column**. Set *New column name* to `IsCurrent` and enter formula: `true`. Set data type to **True/False**.

---

### Step 2.2: Extracting Conformed Dimensions via Reference Queries

Never duplicate data sources manually. Use **Reference Queries** so changes in the source propagate downstream automatically.

#### Building `Dim_Department` via GUI:
1. In the left **Queries** pane, right-click `Dim_Employee` and select **Reference** (do *not* select Duplicate).
2. Right-click the new query and rename it to `Dim_Department`.
3. In the table preview, click the header of **`القسم`** (Department).
4. Right-click the header of `القسم` and select **Remove Other Columns**.
5. With the single `القسم` column selected, go to the **Home** ribbon tab and click **Remove Rows > Remove Duplicates**.
6. In the **Transform** ribbon, click **Sort Ascending**.
7. Go to **Add Column > Index Column > From 1**. Rename this column `DepartmentKey`.
8. Go to **Add Column > Custom Column**. Name it `DepartmentID` with formula:
   `"DEPT-" & Text.PadStart(Text.From([DepartmentKey]), 3, "0")`
9. Rename the original `القسم` column to `DepartmentName`.
10. Drag `DepartmentKey` to be the first column.

#### Building `Dim_Branch` via GUI:
1. In the left **Queries** pane, right-click `Dim_Employee` and select **Reference**.
2. Rename the new query to `Dim_Branch`.
3. Select the column **`الفرع`** (Branch). Right-click and choose **Remove Other Columns**.
4. Go to **Home > Remove Rows > Remove Duplicates**.
5. In **Transform**, click **Sort Ascending**.
6. Go to **Add Column > Index Column > From 1**. Rename to `BranchKey`.
7. Go to **Add Column > Custom Column**. Name it `BranchID` with formula:
   `"BR-" & Text.PadStart(Text.From([BranchKey]), 3, "0")`
8. **Adding Geographic Metadata via Conditional Column GUI**:
   * Go to **Add Column > Conditional Column**.
   * Set *New column name* to `Region`.
   * Configure rules:
     * If `الفرع` equals `فرع الإسكندرية - سموحة` then output `Alexandria & North`.
     * Else If `الفرع` equals `فرع أسيوط` then output `Upper Egypt`.
     * Else If `الفرع` equals `فرع المنصورة` then output `Delta`.
     * Else output `Greater Cairo`.
   * Click **OK**.
9. Rename `الفرع` to `BranchName`.

---

### Step 2.3: Ingesting & Cleansing IoT Daily Access Logs (`Fact_DailyAttendance`)

Raw IoT badge turnstile logs arrive in JSON format with night shifts, missing clock-outs, and contract violations.

1. Go to **Home > New Source > JSON**.
2. Browse to `data/raw/attendance_badge_logs.json` and click **Open**.
3. In the Power Query ribbon, click **Transform > To Table** and click **OK**.
4. At the top-right of the column header `Column1`, click the **Expand Column icon (`↔`)**.
5. Ensure all fields are checked: `EmployeeID`, `AccessDate`, `CheckInTime`, `CheckOutTime`, `BuildingID`, `DeclaredWorkMode`. Uncheck *Use original column name as prefix*. Click **OK**.
6. Select `AccessDate` and set type to **Date (`📅`)**.
7. Select `CheckInTime` and `CheckOutTime` and set types to **Time (`🕒`)**.
8. **Imputing Missing Clock-Outs via Conditional Column GUI**:
   * Go to **Add Column > Custom Column**.
   * Name it `CleanCheckOutTime`.
   * Enter formula:
     ```powerquery
     if [CheckOutTime] <> null then [CheckOutTime]
     else if [CheckInTime] <> null then Time.From(DateTime.From([CheckInTime]) + #duration(0, 8, 0, 0))
     else null
     ```
   * Click **OK** and set its data type to **Time (`🕒`)**.
9. **Calculating Duration Hours via GUI**:
   * Go to **Add Column > Custom Column**. Name it `DurationHours`.
   * Enter formula:
     ```powerquery
     if [CheckInTime] = null or [CleanCheckOutTime] = null then 0.0
     else if [CleanCheckOutTime] >= [CheckInTime] then Duration.TotalHours([CleanCheckOutTime] - [CheckInTime])
     else Duration.TotalHours((#time(23, 59, 59) - [CheckInTime]) + ([CleanCheckOutTime] - #time(0, 0, 0))) + (1 / 3600)
     ```
   * Click **OK** and set data type to **Decimal Number (`1.2`)**.
10. **Flagging Contract Violations via Conditional Column GUI**:
    * Go to **Add Column > Conditional Column**. Name it `ActualWorkMode`.
    * Rule: If `BuildingID` equals `REMOTE_GATE` then output `Remote`, Else output `On-site`. Click **OK**.
11. **Adding DateKey (Smart Integer Key)**:
    * Go to **Add Column > Custom Column**. Name it `AccessDateKey`.
    * Formula: `Date.Year([AccessDate]) * 10000 + Date.Month([AccessDate]) * 100 + Date.Day([AccessDate])`. Set type to **Whole Number**.
12. Go to **Add Column > Index Column > From 1**. Name it `AttendanceKey`. Rename the query to `Fact_DailyAttendance`.

---

### Step 2.4: Transforming Messy Wide FP&A Excel Spreadsheets (`Fact_DepartmentBudget`)

Finance spreadsheets typically present quarters horizontally across columns (`Q1_Budget`, `Q2_Budget`, `Q1_Headcount`), creating an un-pivotable layout with branch spelling typos.

1. Go to **Home > New Source > Text/CSV** (or Excel).
2. Select `data/raw/fpa_department_budget_messy.csv`. Click **OK**.
3. Rename the query to `Fact_DepartmentBudget`.
4. **Normalizing Branch Typos via Conditional Column GUI**:
   * Go to **Add Column > Conditional Column**. Name it `StandardizedBranch`.
   * Rules:
     * If `RawBranch` contains `المعادي` then output `فرع المعادي`.
     * Else If `RawBranch` contains `المعادى` then output `فرع المعادي`.
     * Else If `RawBranch` contains `مدينة نصر` then output `فرع مدينة نصر`.
     * Else If `RawBranch` contains `التجمع` then output `فرع التجمع الخامس`.
     * Else If `RawBranch` contains `القاهرة الجديدة` then output `فرع التجمع الخامس`.
     * Else If `RawBranch` contains `المهندسين` then output `فرع المهندسين`.
     * Else If `RawBranch` contains `الإسكندرية` then output `فرع الإسكندرية - سموحة`.
     * Else If `RawBranch` contains `اسكندرية` then output `فرع الإسكندرية - سموحة`.
     * Else If `RawBranch` contains `أسيوط` then output `فرع أسيوط`.
     * Else If `RawBranch` contains `اسيوط` then output `فرع أسيوط`.
     * Else If `RawBranch` contains `المنصورة` then output `فرع المنصورة`.
     * Else output `RawBranch`.
   * Click **OK**.
5. **Dynamic Unpivoting via GUI**:
   * Hold the `Ctrl` key and select the non-quarter columns: `FiscalYear`, `Department`, `StandardizedBranch`, `OvertimeAllowance_EGP`.
   * Right-click any of the highlighted headers and select **Unpivot Other Columns**.
   * Power BI collapses all horizontal `Q1_Budget_EGP`, `Q2_Budget_EGP`, `Q1_Headcount` columns into two columns: `Attribute` and `Value`.
6. **Extracting Quarter & Metric via GUI**:
   * Select the new `Attribute` column. Go to **Add Column > Extract > Text Range**.
   * Starting index: `1`, Number of characters: `1`. Click **OK**. Rename this column `FiscalQuarter` and set type to **Whole Number**.
   * Go to **Add Column > Conditional Column**. Name it `MetricType`.
   * Rule: If `Attribute` contains `Headcount` then output `BudgetedHeadcount`, Else output `AllocatedSalaryBudget_EGP`. Click **OK**.
7. **Pivoting Metrics into Columnar Facts via GUI**:
   * In the **Queries** table preview, select the `MetricType` column.
   * Go to the **Transform** ribbon tab and click **Pivot Column**.
   * In the dialog, set *Values Column* to `Value`.
   * Expand *Advanced options* and set *Aggregate Value Function* to **Don't Aggregate** (or **Sum**). Click **OK**.
8. Set types: `BudgetedHeadcount` to **Whole Number**, `AllocatedSalaryBudget_EGP` to **Fixed Decimal Number**.
9. **Adding DateKey via Custom Column GUI**:
   * Go to **Add Column > Custom Column**. Name it `DateKey`.
   * Formula:
     ```powerquery
     if [FiscalQuarter] = 1 then [FiscalYear] * 10000 + 101
     else if [FiscalQuarter] = 2 then [FiscalYear] * 10000 + 401
     else if [FiscalQuarter] = 3 then [FiscalYear] * 10000 + 701
     else [FiscalYear] * 10000 + 1001
     ```
   * Set type to **Whole Number**.
10. Go to **Add Column > Index Column > From 1**. Name it `BudgetKey`.

---

### Step 2.5: Ingesting LMS Training Records & Deduplication (`Fact_TrainingCompletions`)

1. Go to **Home > New Source > Text/CSV**. Select `data/raw/lms_course_completions.csv`. Click **OK**.
2. Rename query to `Fact_TrainingCompletions`.
3. Set types: `CompletionDate` to **Date**, `Score` to **Decimal Number**, `CertificationCost_EGP` to **Fixed Decimal**.
4. **Extracting Course Dimension via Reference Query**:
   * Right-click `Fact_TrainingCompletions` in the left pane and select **Reference**. Rename to `Dim_Course`.
   * Select columns `CourseID`, `CourseName`, `SkillDomain`. Right-click and choose **Remove Other Columns**.
   * Go to **Home > Remove Rows > Remove Duplicates**.
   * Go to **Add Column > Index Column > From 1**. Rename to `CourseKey`.
5. In `Fact_TrainingCompletions`:
   * Go to **Add Column > Conditional Column**. Name it `IsPassed`.
   * Rule: If `Score` is greater than or equal to `70` then output `1`, Else output `0`. Set type to **Whole Number**.
   * Go to **Add Column > Custom Column**. Name it `CompletionDateKey`. Formula: `Date.Year([CompletionDate]) * 10000 + Date.Month([CompletionDate]) * 100 + Date.Day([CompletionDate])`. Set type to **Whole Number**.
   * Go to **Add Column > Index Column > From 1**. Name it `CompletionKey`.

---

### Step 2.6: Generating Conformed Enterprise Calendar (`Dim_Date`)

1. Go to **Home > New Source > Blank Query**.
2. Rename the query to `Dim_Date`.
3. In the formula bar at the top, paste this one-liner list generator:
   `= List.Dates(#date(2024, 1, 1), 1096, #duration(1, 0, 0, 0))`
4. In the ribbon, click **Transform > To Table**. Click **OK**.
5. Rename column to `FullDate` and set type to **Date (`📅`)**.
6. **Adding Calendar Attributes via GUI**:
   * With `FullDate` selected, go to **Add Column > Date > Year > Year**.
   * With `FullDate` selected, go to **Add Column > Date > Quarter > Quarter of Year**.
   * With `FullDate` selected, go to **Add Column > Date > Month > Month**.
   * With `FullDate` selected, go to **Add Column > Date > Month > Name of Month**.
   * With `FullDate` selected, go to **Add Column > Date > Day > Day of Week**.
7. **Middle East Weekend Indicator via Conditional Column GUI**:
   * Go to **Add Column > Conditional Column**. Name it `IsWeekend`.
   * Rule: If `Day of Week` equals `5` (Friday) then output `1`, Else If `Day of Week` equals `6` (Saturday) then output `1`, Else output `0`. Set type to **Whole Number**.
8. Add `DateKey` via Custom Column: `Date.Year([FullDate]) * 10000 + Date.Month([FullDate]) * 100 + Date.Day([FullDate])`.

Click **Home > Close & Apply** to load all transformed tables into the Power BI Tabular Engine!

---

## 📐 Module 3: Model View GUI Setup (The Kimball Galaxy Constellation)

Switch to the **Model View** tab on the far left navigation bar (icon showing three connected tables).

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  [Report View]   │  [Data View]   │  [Model View 🗂️]                                                   │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                        │
│         [Dim_Department]        [Dim_Branch]          [Dim_Date]          [Dim_Course]                 │
│                 │                     │                    │                    │                      │
│                 └───────────┬─────────┴──────────┬─────────┴──────────┬─────────┘                      │
│                             ▼                    ▼                    ▼                                │
│                   [Fact_WorkforceSnapshot] [Fact_DailyAttendance] [Fact_TrainingCompletions]           │
│                                                  │                                                     │
│                                                  ▼                                                     │
│                                       [Fact_DepartmentBudget]                                          │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.1 Establishing Relationship Lines in the GUI
1. **Drag-and-Drop Foreign Keys to Primary Keys**:
   * Drag `Dim_Employee[EmployeeKey]` $\to$ `Fact_WorkforceSnapshot[EmployeeKey]`
   * Drag `Dim_Department[DepartmentKey]` $\to$ `Fact_WorkforceSnapshot[DepartmentKey]`
   * Drag `Dim_Branch[BranchKey]` $\to$ `Fact_WorkforceSnapshot[BranchKey]`
   * Drag `Dim_Date[DateKey]` $\to$ `Fact_WorkforceSnapshot[SnapshotDateKey]`
   * Drag `Dim_Employee[EmployeeKey]` $\to$ `Fact_DailyAttendance[EmployeeKey]`
   * Drag `Dim_Branch[BranchKey]` $\to$ `Fact_DailyAttendance[BranchKey]`
   * Drag `Dim_Date[DateKey]` $\to$ `Fact_DailyAttendance[AccessDateKey]`
   * Drag `Dim_Department[DepartmentKey]` $\to$ `Fact_DepartmentBudget[DepartmentKey]`
   * Drag `Dim_Branch[BranchKey]` $\to$ `Fact_DepartmentBudget[BranchKey]`
   * Drag `Dim_Date[DateKey]` $\to$ `Fact_DepartmentBudget[DateKey]`
   * Drag `Dim_Employee[EmployeeKey]` $\to$ `Fact_TrainingCompletions[EmployeeKey]`
   * Drag `Dim_Course[CourseKey]` $\to$ `Fact_TrainingCompletions[CourseKey]`
   * Drag `Dim_Date[DateKey]` $\to$ `Fact_TrainingCompletions[CompletionDateKey]`

2. **Verifying Relationship Properties Dialog**:
   * Double-click any relationship connector line.
   * Verify **Cardinality** is set to **One to many (1:*)** (Dimension to Fact).
   * Verify **Cross filter direction** is set strictly to **Single**.
   * Ensure **Make this relationship active** is **Checked**. Click **OK**.

### 3.2 Organizing DAX Measures into Display Folders via GUI
1. In the **Data** pane on the far right, create a dedicated disconnected table for measures (Home > Enter Data > Table name: `_DAX Measures` > Load).
2. Select any measure in the Data pane.
3. In the **Properties** pane in the middle, locate the **Display folder** box.
4. Type the folder name and hit Enter:
   * `01 Headcount & Payroll`
   * `02 Flight Risk & Compression`
   * `03 Budget & Variance`
   * `04 Workplace Compliance`
   * `05 Upskilling ROI`
5. You can drag and drop measures directly into folders in the Model View GUI!

---

## ⚡ Module 4: Advanced DAX Diagnostics & Analytical Problem Solving

### Problem 1: Salary Compression & Flight Risk Dynamics

#### Analytical Reasoning:
To calculate whether an individual employee is compressed, we cannot simply take the overall company average salary because software engineers earn differently than HR specialists. We must:
1. Identify the specific **Job Role** of the selected employee in filter context.
2. Remove the filter on the individual employee using `ALL()` while keeping the filter on their `JobRole`.
3. Isolate the subset of employees in that exact role who were hired within the last 1.0 year (`TenureYears <= 1.0`).
4. Calculate the **Median** of their base salaries.
5. If the current employee has $\ge 3.0$ years of tenure but earns *less* than this new-hire median, they suffer from salary compression.

```dax
// Measure 1: New-Hire Benchmark Salary in Same Role
Role Median New Hire Salary = 
VAR CurrentRole = SELECTEDVALUE('Dim_Employee'[JobRole])
RETURN
    CALCULATE(
        MEDIAN('Fact_WorkforceSnapshot'[BaseSalary]),
        FILTER(
            ALL('Fact_WorkforceSnapshot'),
            RELATED('Dim_Employee'[JobRole]) = CurrentRole &&
            'Fact_WorkforceSnapshot'[TenureYears] <= 1.0
        )
    )

// Measure 2: Role Salary Inversion Ratio (Compa-Ratio vs New Hires)
Role Salary Inversion Ratio = 
VAR CurrentSalary = SELECTEDVALUE('Fact_WorkforceSnapshot'[BaseSalary])
VAR Benchmark = [Role Median New Hire Salary]
RETURN
    IF(
        NOT(ISBLANK(CurrentSalary)) && Benchmark > 0,
        DIVIDE(CurrentSalary, Benchmark, BLANK()),
        BLANK()
    )

// Measure 3: Flight Risk Severity Score (1-100 Index)
// Combines Inversion (< 1.0), Performance Rating (1-5), and Tenure (Years)
Flight Risk Severity Score = 
VAR CurrentSalary = SELECTEDVALUE('Fact_WorkforceSnapshot'[BaseSalary])
VAR Benchmark = [Role Median New Hire Salary]
VAR PerfRating = SELECTEDVALUE('Fact_WorkforceSnapshot'[AnnualPerformanceRating], 3.0)
VAR Tenure = SELECTEDVALUE('Fact_WorkforceSnapshot'[TenureYears], 1.0)
VAR InversionRatio = DIVIDE(CurrentSalary, Benchmark, 1.0)
RETURN
    IF(
        InversionRatio < 1.0 && Tenure >= 3.0,
        // High performer with compressed salary = Extreme flight risk
        MIN(100, ROUND((PerfRating / 5.0) * 50 + ((1.0 - InversionRatio) * 100) * 0.35 + (Tenure * 3), 0)),
        // Normal distribution
        ROUND((PerfRating / 5.0) * 30 + (1.0 - MIN(1.0, InversionRatio)) * 20, 0)
    )

// Measure 4: Total Retained Payroll at Risk (EGP)
Payroll Value at Critical Flight Risk = 
CALCULATE(
    SUM('Fact_WorkforceSnapshot'[BaseSalary]),
    FILTER(
        'Fact_WorkforceSnapshot',
        [Flight Risk Severity Score] >= 80
    )
)
```

---

### Problem 2: Multi-Grain Bi-Temporal Budget Burn & Headcount Variance

#### Analytical Reasoning:
Finance sets quarterly department/branch targets. When viewing a visual at the monthly level or when filtering by an individual employee, how should the quarterly target respond?
* When sliced by `Dim_Department` or `Dim_Branch`, both `Fact_WorkforceSnapshot` and `Fact_DepartmentBudget` inherit the filter context cleanly through conformed dimensions.
* Monthly payroll must be compared against **one-third of the quarterly budget**.

```dax
// Measure 1: Actual Workforce Headcount
Actual Headcount = 
DISTINCTCOUNT('Fact_WorkforceSnapshot'[EmployeeKey])

// Measure 2: Budgeted Target Headcount
Budgeted Headcount Target = 
SUM('Fact_DepartmentBudget'[BudgetedHeadcount])

// Measure 3: Headcount Variance
Headcount Net Variance = 
[Actual Headcount] - [Budgeted Headcount Target]

// Measure 4: Actual Monthly Payroll Run Rate (EGP)
Actual Monthly Payroll EGP = 
SUM('Fact_WorkforceSnapshot'[BaseSalary])

// Measure 5: Monthly Allocated Salary Budget (Quarterly Budget / 3)
Allocated Monthly Salary Budget EGP = 
DIVIDE(SUM('Fact_DepartmentBudget'[AllocatedSalaryBudget_EGP]), 3, 0)

// Measure 6: Payroll Burn Rate %
Payroll Burn Rate Pct = 
DIVIDE([Actual Monthly Payroll EGP], [Allocated Monthly Salary Budget EGP], BLANK())
```

---

### Problem 3: Workplace Policy Compliance & Ghost Worker Auditing

#### Analytical Reasoning:
* To identify a **Ghost Worker**, we need to find employees who exist as `Active` in `Fact_WorkforceSnapshot`, but have **zero records** in `Fact_DailyAttendance` over the preceding 60 days.
* In DAX, we construct a virtual table of employee keys who logged access within the past 60 days using `CALCULATETABLE(VALUES('Fact_DailyAttendance'[EmployeeKey]), ...)`. We then count active employees who are `NOT IN` that virtual table!

```dax
// Measure 1: Physical On-Site Compliance Rate %
Physical Presence Compliance Rate = 
VAR TotalAccessEvents = COUNTROWS('Fact_DailyAttendance')
VAR OnSiteEvents = 
    CALCULATE(
        COUNTROWS('Fact_DailyAttendance'),
        'Fact_DailyAttendance'[ActualWorkMode] = "On-site"
    )
RETURN
    DIVIDE(OnSiteEvents, TotalAccessEvents, 0)

// Measure 2: Contract Violation Incidents
Contract Violation Breach Count = 
CALCULATE(
    COUNTROWS('Fact_DailyAttendance'),
    'Fact_DailyAttendance'[IsContractViolation] = 1
)

// Measure 3: Ghost Worker Count (Zero Access in >60 Days)
Ghost Worker Count = 
VAR MaxDate = MAX('Dim_Date'[FullDate])
VAR SixtyDaysPrior = MaxDate - 60
VAR ActiveEmployeesWithAccess = 
    CALCULATETABLE(
        VALUES('Fact_DailyAttendance'[EmployeeKey]),
        'Dim_Date'[FullDate] >= SixtyDaysPrior
    )
RETURN
    CALCULATE(
        DISTINCTCOUNT('Fact_WorkforceSnapshot'[EmployeeKey]),
        NOT('Fact_WorkforceSnapshot'[EmployeeKey] IN ActiveEmployeesWithAccess),
        'Fact_WorkforceSnapshot'[EmploymentStatus] = "Active"
    )

// Measure 4: Annualized Payroll Leakage from Ghost Workers (EGP)
Ghost Worker Payroll Leakage EGP = 
VAR MaxDate = MAX('Dim_Date'[FullDate])
VAR SixtyDaysPrior = MaxDate - 60
VAR ActiveEmployeesWithAccess = 
    CALCULATETABLE(
        VALUES('Fact_DailyAttendance'[EmployeeKey]),
        'Dim_Date'[FullDate] >= SixtyDaysPrior
    )
RETURN
    CALCULATE(
        SUM('Fact_WorkforceSnapshot'[BaseSalary]) * 12,
        NOT('Fact_WorkforceSnapshot'[EmployeeKey] IN ActiveEmployeesWithAccess),
        'Fact_WorkforceSnapshot'[EmploymentStatus] = "Active"
    )
```

---

### Problem 4: Upskilling ROI & Performance Score Velocity

#### Analytical Reasoning:
Did spending 9,500 EGP on a Lean Six Sigma certification actually improve employee performance?
We evaluate the **Performance Velocity Delta ($\Delta P$)**: the spread between the average performance rating of certified personnel versus uncertified staff across identical departments.

```dax
// Measure 1: Total Training & Certification Investment (EGP)
Total Training Investment EGP = 
SUM('Fact_TrainingCompletions'[CertificationCost_EGP])

// Measure 2: Certified Employee Headcount
Certified Employee Count = 
CALCULATE(
    DISTINCTCOUNT('Fact_TrainingCompletions'[EmployeeKey]),
    'Fact_TrainingCompletions'[IsPassed] = 1
)

// Measure 3: Average Certified Performance Score
Avg Certified Performance Score = 
VAR CertifiedKeys = 
    CALCULATETABLE(
        VALUES('Fact_TrainingCompletions'[EmployeeKey]),
        'Fact_TrainingCompletions'[IsPassed] = 1
    )
RETURN
    CALCULATE(
        AVERAGE('Fact_WorkforceSnapshot'[AnnualPerformanceRating]),
        'Fact_WorkforceSnapshot'[EmployeeKey] IN CertifiedKeys
    )

// Measure 4: Average Non-Certified Performance Score
Avg NonCertified Performance Score = 
VAR CertifiedKeys = 
    CALCULATETABLE(
        VALUES('Fact_TrainingCompletions'[EmployeeKey]),
        'Fact_TrainingCompletions'[IsPassed] = 1
    )
RETURN
    CALCULATE(
        AVERAGE('Fact_WorkforceSnapshot'[AnnualPerformanceRating]),
        NOT('Fact_WorkforceSnapshot'[EmployeeKey] IN CertifiedKeys)
    )

// Measure 5: Performance Velocity Delta (Spread)
Performance Velocity Delta = 
[Avg Certified Performance Score] - [Avg NonCertified Performance Score]

// Measure 6: Investment Cost Per Rating Point Gain (EGP)
Cost Per Performance Point Gain EGP = 
VAR Spread = [Performance Velocity Delta]
VAR TotalCost = [Total Training Investment EGP]
RETURN
    IF(Spread > 0, DIVIDE(TotalCost, Spread * [Certified Employee Count], BLANK()), BLANK())
```

---

## 🎨 Module 5: Modern Dashboard UI/UX Design System (Report View GUI)

Following top Power BI report creators (Bas / *How to Power BI*, Guy in a Cube, Enterprise DNA), we construct a **Web Application-Style Experience**.

Switch to **Report View** in Power BI Desktop (top icon on the left bar).

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ [APP ICON]  Enterprise Human Capital Diagnostics      [🔍 Slicer: Dept] [📅 Slicer: Quarter] [👤 Admin]│
├──────────────┬─────────────────────────────────────────────────────────────────────────────────────────┤
│ 🏠 Executive │ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────────┐ │
│              │ │ Total Headcount  │ │ Monthly Payroll  │ │ Policy Violations│ │ High Flight Risk     │ │
│ ⚠️ Flight     │ │ 7,000 Staff      │ │ 118,420,000 EGP  │ │ 142 Events       │ │ 312 Personnel      │ │
│    Risk      │ │ ▲ +2.4% vs Q4    │ │ [Sparkline ~~~]  │ │ ▼ -18% vs Target │ │ 4,820,000 EGP Risk │ │
│              │ └──────────────────┘ └──────────────────┘ └──────────────────┘ └──────────────────────┘ │
│ ⏱️ Attendance │ ┌──────────────────────────────────────────────┐ ┌───────────────────────────────────┐  │
│              │ │ Salary Compression Inversion Scatter Plot    │ │ Department Headcount Variance     │  │
│ 💼 Budget FP&A│ │ (Tenure Years vs Role Salary Percentile)     │ │ (Actual vs FP&A Budgeted Target)  │  │
│              │ └──────────────────────────────────────────────┘ └───────────────────────────────────┘  │
│ 🎓 LMS ROI   │ ┌──────────────────────────────────────────────┐ ┌───────────────────────────────────┐  │
│              │ │ Weekly Physical Presence Rate by Branch      │ │ Upskilling Velocity Delta by Domain│ │
│              │ └──────────────────────────────────────────────┘ └───────────────────────────────────┘  │
└──────────────┴─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### Step 5.1: Canvas & Visual Grid Setup via GUI
1. Deselect all visuals by clicking empty canvas.
2. In the right pane, click the **Format report page icon (paintbrush)**.
3. Expand **Canvas settings**:
   * Set *Type* to **Custom**.
   * Set *Width* to **1920 px**, *Height* to **1080 px** (Full HD 16:9).
4. Expand **Canvas background**:
   * Set *Color* to **`#0B0F19`** (Deep Charcoal Slate).
   * Set *Transparency* to **0%**.

---

### Step 5.2: Building the Persistent Left App Navigation Sidebar via GUI
1. Go to **Insert > Shapes > Rectangle**.
2. Position it on the left edge:
   * Format pane > **Size & Position**: Width: `200 px`, Height: `1080 px`, X: `0 px`, Y: `0 px`.
   * Format pane > **Shape > Fill**: Color: `#0F172A` (Elevated Nav Surface).
   * Format pane > **Border**: Set to **Off**.
3. **Adding App Logo & Header**:
   * Go to **Insert > Text Box**. Place at top-left:
     * Font: *Segoe UI Semibold*, Size: *14pt*, Color: `#60A5FA` (Electric Blue).
     * Text: `HR CAPITAL OPS`.
4. **Adding Nav Buttons with Active States**:
   * Go to **Insert > Buttons > Blank**.
   * Position in sidebar (e.g. Y: `120 px`, Width: `180 px`, Height: `44 px`).
   * Format pane > **Button**:
     * Set *State* to **Default**: Text: `📊 Executive Cockpit`, Font color: `#94A3B8`, Fill color: `#0F172A`.
     * Set *State* to **On hover**: Fill color: `#1E293B`, Font color: `#FFFFFF`.
     * Set *State* to **On press**: Fill color: `#2563EB`, Font color: `#FFFFFF`.
   * Repeat for:
     * `⚠️ Flight Risk Engine`
     * `⏱️ Attendance & Policy`
     * `💼 FP&A Budget Matrix`
     * `🎓 Upskilling & LMS`
   * In Format pane > **Action**, set *Type* to **Page navigation** and choose destination page!

---

### Step 5.3: Building KPI Hero Cards via the New Card Visual GUI
1. Go to **Visualizations pane > Card (new)** (icon with multiple values).
2. Drag metrics into the visual fields well:
   * `[Actual Headcount]`
   * `[Actual Monthly Payroll EGP]`
   * `[Contract Violation Breach Count]`
   * `[Payroll Value at Critical Flight Risk]`
3. Go to **Format visual pane**:
   * Expand **Shape**: Set to **Rounded rectangle**, corner radius: `10 px`.
   * Expand **Callout values**: Font: *Segoe UI Bold*, Size: `28pt`, Color: `#F8FAFC`.
   * Expand **Cards > Accent bar**:
     * Set *Toggle* to **On**.
     * Set *Position* to **Left**, *Width* to **5 px**.
     * Color: `#3B82F6` for Headcount, `#10B981` for Payroll, `#F59E0B` for Policy, `#EF4444` for Flight Risk.
   * Expand **Cards > Background**: Fill: `#1E293B`, Transparency: `10%`.
   * Expand **Cards > Border**: Color: `#334155`, Width: `1 px`.
   * Expand **Cards > Shadow**: Toggle **On**, Color: `#000000`, Offset: `Outside`, Preset: `Bottom right`.

---

### Step 5.4: Building the Salary Compression Inversion Scatter Plot via GUI
This visual instantly communicates wage inversion to the Chief Human Resources Officer (CHRO):

1. Click **Visualizations pane > Scatter chart**.
2. Position on canvas: Width `800 px`, Height `420 px`.
3. Configure field wells:
   * **Values**: `Dim_Employee[FullName]`
   * **X Axis**: `Fact_WorkforceSnapshot[TenureYears]` (Summarization: *Don't summarize*)
   * **Y Axis**: `Fact_WorkforceSnapshot[SalaryPercentileInRole]`
   * **Legend**: `Dim_Employee[JobRole]` (or `Dim_Employee[Department]`)
   * **Size**: `Fact_WorkforceSnapshot[BaseSalary]`
   * **Tooltips**: `Fact_WorkforceSnapshot[BaseSalary]`, `[Role Median New Hire Salary]`, `[Flight Risk Severity Score]`
4. Go to **Format visual pane > Reference lines**:
   * Click **Add reference line > Constant line (X Axis)**: Value `3.0` (Tenure threshold), Style: `Dashed`, Color: `#EF4444`. Name: `Tenure > 3 Years`.
   * Click **Add reference line > Constant line (Y Axis)**: Value `0.50` (50th Percentile), Style: `Dashed`, Color: `#F59E0B`. Name: `Role Median`.
5. **Analytical Interpretation**:
   * Any dot located in the **Bottom-Right Quadrant** ($X \ge 3.0$ and $Y < 0.50$) represents a **compressed, high-flight-risk employee**!

---

### Step 5.5: Creating the 360° Employee Diagnostic Dossier Drill-Through Page
When an executive spots an at-risk employee in the scatter plot, they right-click to drill through into their dossier.

1. At the bottom of Power BI Desktop, click **`+`** to create a new report page. Name it `Employee_Dossier`.
2. With no visual selected, go to the **Format report page** pane:
   * Expand **Page information**: Set *Page type* to **Drill-through**.
   * Expand **Drill-through when**: Set *Used as* to **Selected fields**.
3. In the **Drill-through fields** well, drag `Dim_Employee[EmployeeID]`.
4. Power BI automatically generates a back arrow button in the top-left!
5. Add visuals to this page:
   * **Employee Bio Card**: `FullName`, `JobRole`, `Department`, `Branch`, `HireDate`, `ContractType`.
   * **Compensation Audit Table**: `BaseSalary`, `Role Median New Hire Salary`, `Salary Percentile In Role`, `Flight Risk Severity Score`.
   * **Attendance Log Timeline**: 30-day bar chart showing `DurationHours` and colored by `ActualWorkMode`.
   * **Completed LMS Certifications**: Table showing `CourseName`, `SkillDomain`, `Score`, and `CertificationCost_EGP`.

---

## 🔄 Module 6: Enterprise Governance & TMDL Best Practices

Because this project utilizes **Power BI Project (`.pbip`) format**:
1. All table definitions reside in individual human-readable TMDL files under:
   `powerbi/employess-report.SemanticModel/definition/tables/`
2. **Never modify TMDL files while Power BI Desktop has the PBIP file open** (Power BI Desktop holds an exclusive write lock).
3. Always make measure edits either:
   * Directly inside Power BI Desktop's formula bar, or
   * Using **Tabular Editor** connected to the local Analysis Services workspace port, or
   * Via TMDL when Power BI Desktop is closed, followed by `git commit`.

---

## 🏆 Summary Checklist: Mastering Your Analytics Delivery

- [x] **Diagnose First**: Formulate hypotheses on Wage Inversion, Grain Mismatches, and Policy Breaches before modeling.
- [x] **Power Query GUI**: Ingest raw files, create conformed dimensions via Reference queries, unpivot FP&A targets, and impute missing clock-outs.
- [x] **Model View GUI**: Verify 1-to-many single-direction relationships from conformed dimensions to fact tables.
- [x] **DAX Engine**: Evaluate multi-grain measures without circular dependencies; compute percentiles, burn rates, and velocity deltas.
- [x] **Web App UX**: Build a 1920x1080 canvas with a persistent sidebar, rounded cards, accent borders, and drill-through dossier.
