# Enterprise Power BI Implementation & Analytical Diagnostics Masterclass
### Building a Kimball Galaxy Schema (Fact Constellation) from Raw Data with Full GUI, TMDL & DAX Guidance

---

## 🎯 Executive Overview & The Modern Enterprise Paradigm

In enterprise human capital analytics, data engineering is rarely clean. The operational reality of enterprise workforce diagnostics spans **5 heterogeneous, conflicting source systems** operating at disparate frequencies and grains:

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
                                                      │ TMDL & Semantic Modeling
                                                      ▼
                               ┌──────────────────────────────────────────────┐
                               │     ENTERPRISE SEMANTIC MODEL & TMDL LAYER   │
                               ├──────────────────────────────────────────────┤
                               │ • Calculation Groups (Time Intelligence)     │
                               │ • Field Parameters (Dynamic Visual Slicing)  │
                               │ • Dynamic Format Strings (K / M / EGP)       │
                               │ • Row-Level (RLS) & Object-Level (OLS) Sec   │
                               │ • Incremental Refresh Policy (VertiPaq)      │
                               └──────────────────────┬───────────────────────┘
                                                      │ DAX Diagnostic Engine
                                                      ▼
                               ┌──────────────────────────────────────────────┐
                               │       7 ADVANCED ANALYTICAL DIAGNOSTICS      │
                               ├──────────────────────────────────────────────┤
                               │ 1. Salary Compression & Flight Risk Index    │
                               │ 2. Bi-Temporal Budget & Headcount Variance   │
                               │ 3. Policy Compliance & Ghost Worker Audits   │
                               │ 4. Upskilling Velocity & Training ROI        │
                               │ 5. Survivorship Bias & Regrettable Turnover  │
                               │ 6. Equal Pay & Role Compensation Parity      │
                               │ 7. Branch Space Utilization & Peak Stress    │
                               └──────────────────────┬───────────────────────┘
                                                      │ Report View GUI (1920x1080)
                                                      ▼
                               ┌──────────────────────────────────────────────┐
                               │          WEB APP STYLE DASHBOARD UI/UX       │
                               │ Persistent Sidebar │ Hero Cards │ 360° Dossier│
                               └──────────────────────────────────────────────┘
```

This guide equips you with:
1. **Critical Analytical Thinking Frameworks** to formulate hypotheses on organizational behavior, wage friction, and operational leakage.
2. **Visual, Step-by-Step Power Query GUI Clickpaths** to transform messy raw data into a pristine **Kimball Galaxy Schema** without writing manual M code for data tables.
3. **Production M Code Exclusively for `Dim_Date`** providing a continuous enterprise calendar with Egyptian weekend rules and relative offsets.
4. **Advanced Semantic Model Engineering & TMDL Scripting** covering Calculation Groups, Field Parameters, Dynamic Format Strings, and VertiPaq memory optimization.
5. **Advanced DAX Formulas for 7 Complex Business Problems** with full filter context explanations.
6. **Modern Web App-Style UI/UX Design System** in the Report View GUI.

---

## 🧠 Module 1: Developing Enterprise Analytical Acumen (7 Core Diagnostic Problems)

Before opening Power BI, an analytics engineer must understand the **underlying business friction**.

### Diagnostic 1: The Loyalty Penalty & Wage Inversion (Salary Compression)
* **The Mechanism**: External market talent inflation forces recruiters to offer high compensation for new hires ($< 1$ year tenure). Existing employees receive standard annual merit increases ($5-8\%$), falling behind market value.
* **The Critical Trap**: If an employee with 4 years of tenure earns less than the 50th percentile of brand-new hires in the identical job role, they suffer from **Wage Inversion**. When that employee is also a top performer (Appraisal Score $\ge 4.0$), voluntary exit probability exceeds $80\%$.
* **Financial Impact**: Replacing institutional knowledge costs $1.5\times$ to $2.0\times$ the employee's annual salary in lost momentum and recruiting fees.

### Diagnostic 2: Fact-to-Fact Granularity Collisions (Multi-Grain Budgeting)
* **The Mechanism**: Finance plans headcount and payroll budgets quarterly by branch and department. HR and payroll operate on individual employees at the monthly level.
* **The Critical Trap**: Merging the budget table into the employee table causes Cartesian product inflation or creates circular Many-to-Many relationship loops.
* **The Solution**: Conformed dimensions (`Dim_Department`, `Dim_Branch`, `Dim_Date`) filter both fact tables independently, while DAX measures dynamically apportion quarterly budget figures ($\div 3$) for monthly run-rate comparison.

### Diagnostic 3: Survivorship Bias & Ghost Worker Payroll Leakage
* **The Mechanism**: Active employee databases only reflect currently employed survivors. Looking only at active staff underestimates historical attrition rates.
* **The Critical Trap**: Terminated, deceased, or unmonitored employees can remain marked "Active" in enterprise HRIS software for months due to administrative lag, disbursing automated direct deposits (**Ghost Workers**).
* **The Solution**: Cross-referencing IoT turnstile and badge records against active payroll records. Active staff with zero physical badge or system access over $\ge 60$ consecutive days are flagged for payroll freeze.

### Diagnostic 4: Upskilling Velocity & Training ROI Delta ($\Delta P$)
* **The Mechanism**: Enterprises invest millions in learning certifications without measuring if credentials drive tangible business outcomes.
* **The Solution**: Evaluating **Performance Score Velocity ($\Delta P$)**: the spread between annual appraisal scores of certified personnel versus uncertified peers in identical roles, computing the net training investment per rating point gained.

### Diagnostic 5: Early Resignation Notice Lead-Time & Regrettable Loss
* **The Mechanism**: Resignation notices are submitted 2 to 6 weeks before formal termination.
* **The Critical Trap**: Standard HR dashboards only register departures on the `ExitDate`, blinding management to pending talent drains.
* **The Solution**: Bi-temporal modeling tracking both `NoticeDate` and `ExitDate` with inactive relationships and DAX `USERELATIONSHIP()`.

### Diagnostic 6: Demographic Pay Equity Drift
* **The Mechanism**: Compensation disparities can emerge quietly across genders within the same department due to starting pay discrepancies.
* **The Solution**: Tenure-controlled regression metrics evaluating average base salary by role and gender.

### Diagnostic 7: Branch Space Utilization & Peak Occupancy Stress
* **The Mechanism**: In hybrid work environments, employees cluster their onsite days on Tuesdays and Wednesdays, causing branch capacity bottlenecks while branches sit empty on Sundays and Thursdays.
* **The Solution**: Comparing daily unique badge check-ins against branch physical desk capacity to calculate peak stress ratios.

---

## 🖱️ Module 2: Power Query Editor GUI Masterclass (Raw Data to Galaxy Schema)

Every transformation below is executed **entirely through the Power BI Desktop visual interface** (buttons, dialogs, and ribbons).

Open Power BI Desktop and click **Home > Transform Data** to launch Power Query Editor.

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ File  Home  Transform  Add Column  View  Tools  Help                                                   │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [Close & Apply] [New Source] [Enter Data] [Manage Parameters] [Merge Queries ▼] [Append Queries ▼]    │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### Step 2.1: Cleansing Core HR & Building `Dim_Employee` via GUI

> [!IMPORTANT]
> **Authoritative Master Grounding (`employees_data_7000.txt`)**:
> The single source of truth for all 7,000 employees is `data/raw/employees_data_7000.txt`. In this repository, the Power BI semantic model (`powerbi/employess-report.SemanticModel/definition/expressions.tmdl`) provides the native Power Query M script (`employees_data_7000`) that parses the raw text file directly (lines, headers, colon-delimited key-value pairs).
> 
> You have two easy ways to load `Dim_Employee`:
> * **Native Power Query / TMDL (Recommended)**: The pre-configured query `employees_data_7000` is already wired into `Dim_Employee`.
> * **Text/CSV File**: If importing manually via GUI, you can select `data/raw/employees_core.csv` (which is the direct UTF-8 CSV representation generated from `employees_data_7000.txt`).
> * **SQL Server**: Alternatively, select **New Source > SQL Server**, connect to `localhost` (`EnterpriseHR_DWH`), and select `[mart].[Dim_Employee]`.

1. In the **Home** ribbon, click **New Source > Text/CSV** (or use the existing `employees_data_7000` query).
2. Select `data/raw/employees_core.csv` (or browse to `data/raw/employees_data_7000.txt`) and click **Open**. Verify file origin is **65001: Unicode (UTF-8)** and click **OK**.
3. In the left **Queries** pane, right-click the imported query, choose **Rename**, and name it `Dim_Employee`.
4. **Setting Correct Data Types visually**:
   * Click the icon in the column header for **`السن`** (Age) $\to$ choose **Whole Number (`123`)**.
   * Click the icon for **`تاريخ التعيين`** (Hire Date) $\to$ choose **Date (`📅`)**.
   * Click the icon for **`الراتب الأساسي`** (Base Salary) $\to$ choose **Fixed Decimal Number (`$`)**.
   * Click the icon for **`تقييم الأداء السنوي`** (Performance Rating) $\to$ choose **Decimal Number (`1.2`)**.
5. **Adding Surrogate Primary Key (`EmployeeKey`) via GUI**:
   * Switch to the **Add Column** ribbon tab.
   * Click **Index Column > From 1**.
   * Right-click the new `Index` header, select **Rename**, and type `EmployeeKey`.
   * Drag `EmployeeKey` to become the first column on the left.
6. **Deriving Analytical Business Columns from Raw Employee Data**:

   The raw employee file is a **point-in-time snapshot** — it has no change history. SCD Type 2 versioning (tracking when an employee changed department, salary, or branch) is handled at the SQL Server ETL layer via the [`MERGE` procedure](../sql/stored_procedures/01_dim_employee_scd2.sql), not in Power Query. What Power Query *should* do is derive the **calculated business columns** that the downstream DAX diagnostics depend on.

   #### 6a. Tenure in Years (`TenureYears`) — Drives Flight Risk & Salary Compression Analysis

   Without tenure, you cannot identify wage inversion (veteran employees earning less than new hires). This column calculates how long each employee has been with the organization.

   * Go to **Add Column > Custom Column**.
   * Name: `TenureYears`
   * Formula:
     ```
     Duration.TotalDays(DateTime.LocalNow() - DateTime.From([تاريخ التعيين])) / 365.25
     ```
   * Click **OK** → set column type to **Decimal Number**.
   * Right-click the `TenureYears` header → **Round** → choose **Round Down** for whole-year floors, or keep decimals for precise analysis.

   > **💡 Why `365.25`?** Accounts for leap years. An employee hired on `2021-03-15` should show ~5.2 years in mid-2026, not a misleading 4.9 from integer division.

   #### 6b. Age Band (`AgeBand`) — Drives Demographic & Workforce Planning Analysis

   Raw age as a number is hard to slice visually. Grouping into HR-standard generational bands enables workforce planning by demographic cohort.

   * Go to **Add Column > Conditional Column**.
   * Column Name: `AgeBand`
   * Configure rules:

     | Condition | Output |
     |:---|:---|
     | If `السن` is less than 25 | `Gen Z (< 25)` |
     | Else if `السن` is less than 35 | `Millennial (25–34)` |
     | Else if `السن` is less than 45 | `Gen X (35–44)` |
     | Else if `السن` is less than 55 | `Senior (45–54)` |
     | Else | `Pre-Retirement (55+)` |

   * Click **OK** → verify type is **Text**.

   > **💡 Business Value:** HR uses these bands to forecast retirement waves — if 30% of a critical department is `Pre-Retirement (55+)`, succession planning must begin immediately.

   #### 6c. Salary Band (`SalaryBand`) — Drives Compensation Equity & Budget Analysis

   Individual salary values create noisy scatter plots. Banding into EGP ranges enables clean cross-tabulation against departments and branches.

   * Go to **Add Column > Conditional Column**.
   * Column Name: `SalaryBand`
   * Configure rules:

     | Condition | Output |
     |:---|:---|
     | If `الراتب الأساسي` is less than 5000 | `Entry (< 5K)` |
     | Else if `الراتب الأساسي` is less than 10000 | `Junior (5K–10K)` |
     | Else if `الراتب الأساسي` is less than 20000 | `Mid-Level (10K–20K)` |
     | Else if `الراتب الأساسي` is less than 35000 | `Senior (20K–35K)` |
     | Else | `Executive (35K+)` |

   * Click **OK** → verify type is **Text**.

   #### 6d. Performance Tier (`PerformanceTier`) — Drives Retention & Upskilling ROI

   The raw `تقييم الأداء السنوي` is a decimal (e.g., 3.7). Translating it into named tiers lets stakeholders immediately spot high performers at risk.

   * Go to **Add Column > Conditional Column**.
   * Column Name: `PerformanceTier`
   * Configure rules:

     | Condition | Output |
     |:---|:---|
     | If `تقييم الأداء السنوي` is less than 2.0 | `🔴 Underperformer` |
     | Else if `تقييم الأداء السنوي` is less than 3.0 | `🟡 Developing` |
     | Else if `تقييم الأداء السنوي` is less than 4.0 | `🟢 Meets Expectations` |
     | Else if `تقييم الأداء السنوي` is less than 4.5 | `🔵 High Performer` |
     | Else | `⭐ Exceptional (Top Talent)` |

   * Click **OK** → verify type is **Text**.

   > **💡 Business Value:** When crossed with `SalaryBand`, this instantly reveals the most dangerous flight risk pattern: `⭐ Exceptional` performers stuck in `Entry (< 5K)` or `Junior (5K–10K)` salary bands.

   #### 6e. Employment Status Modeling (`EmploymentStatus` & `IsActive`)

   > [!NOTE]
   > **Architectural Clarity & Dimensional Modeling Principles**:
   > In a dimensional galaxy schema, hardcoding a static `IsActive = true` column across all rows in a dimension is an anti-pattern because it provides zero discriminative filtering value. Furthermore, in Power BI, DAX measures cannot mutate or "override" physical column values in a dimension table.
   > 
   > Depending on your pipeline design, choose one of two enterprise patterns:

   * **Option A (Automatic Power Query Merge — Built into Dim_Employee M Code ✅ ACTIVE)**:

     > [!TIP]
     > **No Manual Merge Required!** The `Dim_Employee` partition in the `.tmdl` file already contains `Table.NestedJoin` M code that automatically merges `employees_data_7000` with `Exit_Attrition_Records` on `الرقم التعريفي = EmployeeID`. The three derived columns (`ExitDate`, `EmploymentStatus`, `IsActive`) are computed automatically.
     >
     > **What you need to do**: Simply open the Power BI project, refresh the data (**Home → Refresh All**), and the `Dim_Employee` table will contain:
     > - `ExitDate` — the date the employee left (null for active employees)
     > - `EmploymentStatus` — `"Active"` or `"Separated"`
     > - `IsActive` — `TRUE` / `FALSE` (boolean)
     >
     > **Expected result**: 6650 rows with `IsActive = TRUE`, 350 rows with `IsActive = FALSE`.

     **Pre-requisite**: Ensure the `Exit_Attrition_Records` query exists in the Queries pane:
     1. If it's missing, go to **Home > New Source > SQL Server**.
     2. Server: `localhost` (or `.` or `localhost\SQLEXPRESS`), Database: `EnterpriseHR_DWH`, Mode: **Import** → click **OK**.
     3. In **Navigator**, expand `stg` schema → check **`Exit_Attrition_Records`** → click **OK**.
     4. *(Best Practice)*: Right-click `Exit_Attrition_Records` in the left pane → uncheck **Enable Load** (keeps it as a staging-only query).

   * **Option B (Pure Galaxy Schema / Snapshot Modeling — Star Schema Standard)**:
     * In formal Kimball dimensional modeling, `Dim_Employee` stores conformed attributes (Demographics, Titles, Skills), while point-in-time employment status belongs in the periodic snapshot fact table (`Fact_WorkforceSnapshot[EmploymentStatus]`) or is evaluated dynamically in DAX.
     * **Ghost Worker Detection** does not rely on a dummy dimension flag; rather, the DAX engine dynamically cross-references employees active on payroll against physical/VPN turnstile swipes in `Fact_DailyAttendance`:
       ```dax
       // Ghost Worker Diagnostic Count (Active on Payroll with Zero Turnstile Access in >60 Days)
       Ghost Worker Count = 
       VAR MaxDate = MAX('Dim_Date'[FullDate])
       VAR SixtyDaysPrior = MaxDate - 60
       VAR EmployeesWithBadging = 
           CALCULATETABLE(
               VALUES('Fact_DailyAttendance'[EmployeeKey]),
               'Dim_Date'[FullDate] >= SixtyDaysPrior
           )
       RETURN
           CALCULATE(
               DISTINCTCOUNT('Fact_WorkforceSnapshot'[EmployeeKey]),
               NOT('Fact_WorkforceSnapshot'[EmployeeKey] IN EmployeesWithBadging),
               'Fact_WorkforceSnapshot'[EmploymentStatus] = "Active"
           )
       ```

---

### Step 2.2: Extracting Conformed Dimensions via Reference Queries in GUI

#### Building `Dim_Department` via GUI:
1. In the left **Queries** pane, right-click `Dim_Employee` and select **Reference** (creates a linked query without duplicating data).
2. Right-click the new query and rename it to `Dim_Department`.
3. In the table preview, click the column header for **`القسم`** (Department).
4. Right-click the header and choose **Remove Other Columns**.
5. With `القسم` selected, go to **Home > Remove Rows > Remove Duplicates**.
6. In **Transform**, click **Sort Ascending**.
7. Go to **Add Column > Index Column > From 1**. Rename to `DepartmentKey`.
8. Go to **Add Column > Custom Column**. Name it `DepartmentID` with expression:
   `"DEPT-" & Text.PadStart(Text.From([DepartmentKey]), 3, "0")`
9. Rename `القسم` to `DepartmentName`. Drag `DepartmentKey` to the left.

#### Building `Dim_Branch` via GUI:
1. Right-click `Dim_Employee` in the left pane and select **Reference**. Rename to `Dim_Branch`.
2. Click header **`الفرع`** (Branch) $\to$ right-click $\to$ **Remove Other Columns**.
3. Go to **Home > Remove Rows > Remove Duplicates**. In **Transform**, click **Sort Ascending**.
4. Go to **Add Column > Index Column > From 1**. Rename to `BranchKey`.
5. Go to **Add Column > Custom Column**. Name it `BranchID` with expression:
   `"BR-" & Text.PadStart(Text.From([BranchKey]), 3, "0")`
6. **Adding Geographic Metadata (`Region`) via Conditional Column GUI**:
   Your table contains exactly 14 distinct branches:
   * **Alexandria**: `الإسكندرية - لوران`, `الإسكندرية - سموحة`
   * **Delta & Canal Zone**: `الدقهلية - المنصورة`, `الغربية - طنطا`, `دمياط - دمياط الجديدة`, `بورسعيد - الشرق`
   * **Upper Egypt**: `أسيوط - أسيوط الجديدة`
   * **Greater Cairo (Cairo & Giza)**: `القاهرة - المعادي`, `القاهرة - التجمع الخامس`, `القاهرة - مصر الجديدة`, `القاهرة - القرية الذكية`, `الجيزة - 6 أكتوبر`, `الجيزة - الشيخ زايد`, `الجيزة - الدقي`

   * Go to **Add Column > Conditional Column**.
   * Set **New column name**: `Region`
   * Set **Column Name**: `الفرع`
   * Configure the dialog rules using either approach:

     **Method A: Using "begins with" (Recommended - Fast & Clean)**:
     * If `الفرع` **begins with** `الإسكندرية` then `Alexandria & North`
     * Else If `الفرع` **begins with** `أسيوط` then `Upper Egypt`
     * Else If `الفرع` **begins with** `الدقهلية` then `Delta`
     * Else If `الفرع` **begins with** `الغربية` then `Delta`
     * Else If `الفرع` **begins with** `دمياط` then `Delta`
     * Else If `الفرع` **begins with** `بورسعيد` then `Canal Zone`
     * Else `Greater Cairo` *(covers all 7 Cairo and Giza branches automatically)*

     **Method B: Using exact "equals" matching your 14 rows**:
     * If `الفرع` **equals** `الإسكندرية - لوران` then `Alexandria & North`
     * Else If `الفرع` **equals** `الإسكندرية - سموحة` then `Alexandria & North`
     * Else If `الفرع` **equals** `أسيوط - أسيوط الجديدة` then `Upper Egypt`
     * Else If `الفرع` **equals** `الدقهلية - المنصورة` then `Delta`
     * Else If `الفرع` **equals** `الغربية - طنطا` then `Delta`
     * Else If `الفرع` **equals** `دمياط - دمياط الجديدة` then `Delta`
     * Else If `الفرع` **equals** `بورسعيد - الشرق` then `Canal Zone`
     * Else `Greater Cairo`

7. Click **OK**. Set the data type of `Region` to **Text**.
8. Click the column header **`الفرع`** $\to$ right-click $\to$ select **Rename** $\to$ rename it to `BranchName`.
9. *(Optional)* Add physical desk capacity for branch occupancy stress analytics:
   * Go to **Add Column > Custom Column** $\to$ Name: `Capacity` $\to$ Formula: `250` $\to$ set type to **Whole Number (`123`)**.

---

### Step 2.3: Ingesting & Cleansing IoT Daily Access Logs (`Fact_DailyAttendance`) via GUI

1. Go to **Home > New Source > JSON** $\to$ select `data/raw/attendance_badge_logs.json` $\to$ click **Open**.
2. Click **Transform > To Table** $\to$ click **OK**.
3. Click the **Expand Column icon (`↔`)** at the top right of `Column1`.
4. Ensure all fields are checked: `EmployeeID`, `AccessDate`, `CheckInTime`, `CheckOutTime`, `BuildingID`, `DeclaredWorkMode`. Uncheck *Use original column name as prefix*. Click **OK**.
5. Select `AccessDate` $\to$ set type to **Date**. Select `CheckInTime` and `CheckOutTime` $\to$ set types to **Time**.

> [!NOTE]
> **Alphanumeric Facility Codes (`BuildingID`)**:
> `BuildingID` uses clean alphanumeric facility codes (`BLD-001` through `BLD-014`) directly mapped to the 14 regional branches from `employees_data_7000.txt` (`BLD-001` = `الإسكندرية - لوران`, `BLD-002` = `الدقهلية - المنصورة`, ..., `BLD-014` = `الغربية - طنطا`), or `REMOTE_GATE` for virtual/remote access sessions.

6. **Imputing Missing Clock-Outs visually**:
   * Go to **Add Column > Custom Column**. Name it `CleanCheckOutTime`.
   * Use the simple arithmetic expression:
     `if [CheckOutTime] <> null then [CheckOutTime] else if [CheckInTime] <> null then Time.From(DateTime.From([CheckInTime]) + #duration(0, 8, 0, 0)) else null`
   * Set type to **Time**.
7. **Calculating Duration Hours visually**:
   * Go to **Add Column > Custom Column**. Name it `DurationHours`.
   * Expression:
     `if [CheckInTime] = null or [CleanCheckOutTime] = null then 0.0 else if [CleanCheckOutTime] >= [CheckInTime] then Duration.TotalHours([CleanCheckOutTime] - [CheckInTime]) else Duration.TotalHours((#time(23, 59, 59) - [CheckInTime]) + ([CleanCheckOutTime] - #time(0, 0, 0))) + (1 / 3600)`
   * Set type to **Decimal Number**.
8. **Flagging Actual Work Mode**:
   * Go to **Add Column > Conditional Column**. Name it `ActualWorkMode`.
   * Rule: If `BuildingID` equals `REMOTE_GATE` then `Remote`, Else `On-site`. Click **OK**.
9. **Adding Smart Integer DateKey**:
   * Go to **Add Column > Custom Column**. Name it `AccessDateKey`.
   * Expression: `Date.Year([AccessDate]) * 10000 + Date.Month([AccessDate]) * 100 + Date.Day([AccessDate])`. Set type to **Whole Number**.
10. Go to **Add Column > Index Column > From 1**. Name it `AttendanceKey`. Rename query to `Fact_DailyAttendance`.

---

### Step 2.3b: Enterprise SQL Server Ingestion — Importing `raw.Badge_Access_Logs` via GUI

In a production enterprise architecture, rather than importing raw JSON files directly into Power BI Desktop, high-velocity device telemetry has already been flattened and landed into the Microsoft SQL Server data warehouse under `[raw].[Badge_Access_Logs]`.

This step guides you through connecting Power BI Desktop directly to Microsoft SQL Server via **Windows Authentication**, navigating the schema catalog, selecting the landing table, and leveraging **Query Folding** for high-performance ETL.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ SQL Server Database Connection Dialog                                                 │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ Server:   [ localhost                                                      ]           │
│ Database: [ EnterpriseHR_DWH                                               ]           │
│ Data Connectivity mode: (•) Import   ( ) DirectQuery                                   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 1. Connecting to SQL Server via the Power Query Ribbon:
1. In Power Query Editor, go to the **Home** ribbon tab.
2. Click **New Source > SQL Server** (or **Home > Get Data > SQL Server** in the main Power BI window).
3. In the **SQL Server database** dialog:
   * **Server**: Type `localhost` (or `.` or `localhost\SQLEXPRESS` or the server instance configured in your `.env`).
   * **Database (optional)**: Type `EnterpriseHR_DWH`.
   * **Data Connectivity mode**: Select **Import** (Recommended for in-memory columnar compression and maximum DAX performance).
   * Click **OK**.
4. In the **Authentication** window:
   * Select **Windows** on the left menu.
   * Choose **Use my current credentials** (Windows Authentication / Trusted Connection).
   * Click **Connect**.
   * *(If an "Encryption Support" prompt appears, click **OK** / **Trust Server Certificate**)*.

#### 2. Selecting the Raw Badge Logs Table in the Navigator:
1. In the **Navigator** pane, expand the `EnterpriseHR_DWH` database node.
2. Locate and expand the **`raw`** schema folder.
3. Check the checkbox next to **`Badge_Access_Logs`** (`[raw].[Badge_Access_Logs]`).
4. A live preview of the 114,952 flattened IoT records will display on the right (columns: `LogID`, `SystemSource`, `EmployeeID`, `AccessDate`, `FacilityCode`, `CheckInTime`, `CheckOutTime`).
5. Click **OK** (or **Transform Data**).

#### 3. Power Query Cleansing & Type Casting via GUI:
1. In the left **Queries** pane, right-click `Badge_Access_Logs` and rename it to **`Fact_Badge_Access_Logs_SQL`** (or `Fact_DailyAttendance`).
2. **Confirming & Setting Data Types visually**:
   * Click the type icon in header `LogID` $\to$ set to **Text (`ABC`)**.
   * Click the type icon in header `SystemSource` $\to$ set to **Text (`ABC`)**.
   * Click the type icon in header `EmployeeID` $\to$ set to **Text (`ABC`)**.
   * Click the type icon in header `AccessDate` $\to$ set to **Date (`📅`)**.
   * Click the type icon in header `FacilityCode` $\to$ set to **Text (`ABC`)**.
3. **Parsing ISO UTC Timestamps into Date/Time & Time via GUI**:
   * Select `CheckInTime` $\to$ click the type icon $\to$ choose **Date/Time (`📅🕒`)**.
   * Select `CheckOutTime` $\to$ click the type icon $\to$ choose **Date/Time (`📅🕒`)**.
4. **Heuristic Median Imputation for Forgotten Check-Outs (5% Null Swipes)**:
   * Go to **Add Column > Custom Column**.
   * Column Name: `CleanCheckOutTime`
   * Formula:
     ```powerquery
     if [CheckOutTime] <> null then [CheckOutTime] else if [CheckInTime] <> null then [CheckInTime] + #duration(0, 8, 30, 0) else null
     ```
   * Click **OK** $\to$ set type to **Date/Time (`📅🕒`)**.
5. **Calculating Physical Shift Duration Hours via GUI**:
   * Go to **Add Column > Custom Column**.
   * Column Name: `DurationHours`
   * Formula:
     ```powerquery
     if [CheckInTime] = null or [CleanCheckOutTime] = null then 0.0 else Number.Round(Duration.TotalHours([CleanCheckOutTime] - [CheckInTime]), 2)
     ```
   * Click **OK** $\to$ set type to **Decimal Number (`1.2`)**.
6. **Deriving Work Mode & Policy Compliance Flag via Conditional Column GUI**:
   * Go to **Add Column > Conditional Column**.
   * Column Name: `ActualWorkMode`
   * Rule setup:
     * If `FacilityCode` equals `REMOTE-VPN` then `Remote`
     * Else `On-site`
   * Click **OK** $\to$ set type to **Text (`ABC`)**.
7. **Generating Smart Integer Date Key for Galaxy Schema Joining**:
   * Go to **Add Column > Custom Column**.
   * Column Name: `AccessDateKey`
   * Formula:
     ```powerquery
     Date.Year([AccessDate]) * 10000 + Date.Month([AccessDate]) * 100 + Date.Day([AccessDate])
     ```
   * Click **OK** $\to$ set type to **Whole Number (`123`)**.

> [!TIP]
> **Query Folding Advantage**: Because this query connects directly to Microsoft SQL Server via `Sql.Database()`, transformations like column selection and type casting are automatically translated into optimized T-SQL statements executed on the SQL Server instance, accelerating Power BI data refreshes and minimizing memory usage.

---

### Step 2.4: Transforming Messy Wide FP&A Excel Budgets (`Fact_DepartmentBudget`) via GUI


1. Go to **Home > New Source > Text/CSV** $\to$ select `data/raw/fpa_department_budget_messy.csv` $\to$ click **OK**.
2. Rename query to `Fact_DepartmentBudget`.
3. **Normalizing Branch Typos via Conditional Column GUI**:
   * Go to **Add Column > Conditional Column**. Name it `StandardizedBranch`.
   * Rule setup:
     * If `RawBranch` contains `المعادي` then `فرع المعادي`
     * Else If `RawBranch` contains `المعادى` then `فرع المعادي`
     * Else If `RawBranch` contains `مدينة نصر` then `فرع مدينة نصر`
     * Else If `RawBranch` contains `التجمع` then `فرع التجمع الخامس`
     * Else If `RawBranch` contains `القاهرة الجديدة` then `فرع التجمع الخامس`
     * Else If `RawBranch` contains `المهندسين` then `فرع المهندسين`
     * Else If `RawBranch` contains `الإسكندرية` then `فرع الإسكندرية - سموحة`
     * Else If `RawBranch` contains `اسكندرية` then `فرع الإسكندرية - سموحة`
     * Else If `RawBranch` contains `أسيوط` then `فرع أسيوط`
     * Else If `RawBranch` contains `اسيوط` then `فرع أسيوط`
     * Else If `RawBranch` contains `المنصورة` then `فرع المنصورة`
     * Else `RawBranch`
   * Click **OK**.
4. **Dynamic Unpivoting via GUI**:
   > [!IMPORTANT]
   > **Avoid Unpivoting OvertimeAllowance_EGP**:
   > `OvertimeAllowance_EGP` is an **annual** department allowance, not a quarterly metric! If it gets unpivoted into `Attribute`, extracting index 1 will grab the letter **`v`** from `O-v-ertime...`, causing errors in `FiscalQuarter`.
   > 
   > **Recommended GUI Clickpath (Unpivot Only Selected Columns)**:
   > * Click the first quarterly column header: **`Q1_Budget_EGP`**.
   > * Hold `Shift` on your keyboard and click the last quarterly column: **`Q4_Headcount`** (this selects all 8 quarterly columns: `Q1_Budget_EGP` through `Q4_Headcount`).
   > * Right-click any of the highlighted column headers $\to$ select **Unpivot Only Selected Columns**.
   > * *(Alternative)*: If you prefer **Unpivot Other Columns**, make sure you select `FiscalYear`, `Department`, `StandardizedBranch`, **AND** hold `Ctrl` to also select `OvertimeAllowance_EGP` before clicking **Unpivot Other Columns**.
   > 
   > Power BI collapses *only* the 8 quarterly metrics into `Attribute` and `Value`, while keeping `FiscalYear`, `Department`, `StandardizedBranch`, and `OvertimeAllowance_EGP` as normal dimension columns.

5. **Extracting Quarter & Metric via GUI**:
   * Select `Attribute` $\to$ go to **Add Column > Extract > Text Range**. Starting index: `1`, length: `1`. Click **OK**. Rename to `FiscalQuarter` (Whole Number). *(It will now contain only `1`, `2`, `3`, `4`, with zero `'v'` errors!)*
   * Go to **Add Column > Conditional Column**. Name it `MetricType`.
   * Rule: If `Attribute` contains `Headcount` then `BudgetedHeadcount`, Else `AllocatedSalaryBudget_EGP`. Click **OK**.
6. **Pivoting Metrics into Columnar Facts via GUI**:
   * Select `MetricType` column $\to$ go to **Transform > Pivot Column**.
   * Set *Values Column* to `Value`. Expand *Advanced options* $\to$ select **Don't Aggregate** (or **Sum**). Click **OK**.
7. Set data types: `BudgetedHeadcount` to **Whole Number**, `AllocatedSalaryBudget_EGP` to **Fixed Decimal Number**.
8. Add `DateKey` via Custom Column:
   `if [FiscalQuarter] = 1 then [FiscalYear] * 10000 + 101 else if [FiscalQuarter] = 2 then [FiscalYear] * 10000 + 401 else if [FiscalQuarter] = 3 then [FiscalYear] * 10000 + 701 else [FiscalYear] * 10000 + 1001`
   Set type to **Whole Number**. Add Index Column as `BudgetKey`.

---

### Step 2.4b: Enterprise SQL Server Ingestion — Importing `raw.Finance_Budget_Plan` via GUI

In enterprise finance planning, FP&A departments maintain headcount forecasts in wide, pivoted Excel workbooks (`finance_budget_2026.xlsx`). Rather than loading aggressively pivoted files directly into Power BI (which burdens client-side Power Query data refreshes), in our production data stack Python (`scripts/ingestion/ingest_finance_plan.py`) unpivots the workbook and lands the normalized records into Microsoft SQL Server under **`[raw].[Finance_Budget_Plan]`**.

This step walks through importing this normalized planning table directly from SQL Server, cleaning manual branch typographical drift, and properly handling **mixed granularity** against your HR fact tables.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ SQL Server Database Connection Dialog                                                 │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ Server:   [ localhost                                                      ]           │
│ Database: [ EnterpriseHR_DWH                                               ]           │
│ Data Connectivity mode: (•) Import   ( ) DirectQuery                                   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 1. Connecting to SQL Server via Power Query Ribbon:
1. In Power Query Editor, go to the **Home** ribbon tab.
2. Click **New Source > SQL Server** (or **Home > Get Data > SQL Server** in the main Power BI window).
3. In the dialog:
   * **Server**: `localhost` (or `.` or `localhost\SQLEXPRESS`).
   * **Database**: `EnterpriseHR_DWH`.
   * **Data Connectivity mode**: **Import**.
   * Click **OK**.
4. In the **Authentication** window, choose **Windows > Use my current credentials** $\to$ click **Connect**.

#### 2. Selecting `raw.Finance_Budget_Plan` in the Navigator:
1. Expand `EnterpriseHR_DWH` $\to$ expand the **`raw`** schema folder.
2. Check the checkbox next to **`Finance_Budget_Plan`** (`[raw].[Finance_Budget_Plan]`).
3. The preview displays 168 unpivoted records with columns: `Department`, `CostCenter_Branch`, `Quarter`, `Budget_EGP`, `Headcount`, `FiscalYear`.
4. Click **OK** (or **Transform Data**).

#### 3. Power Query Cleansing, Branch Harmonization & Keys via GUI:
1. In the **Queries** pane, rename `Finance_Budget_Plan` to **`Fact_DepartmentBudget_SQL`** (or `Fact_DepartmentBudget`).
2. **Setting Data Types Visually**:
   * Click the icon in header `Department` $\to$ **Text (`ABC`)**.
   * Click the icon in header `CostCenter_Branch` $\to$ **Text (`ABC`)**.
   * Click the icon in header `Quarter` $\to$ **Text (`ABC`)**.
   * Click the icon in header `Headcount` $\to$ **Whole Number (`123`)**.
   * Click the icon in header `Budget_EGP` $\to$ **Fixed Decimal Number (`$`)**.
   * Click the icon in header `FiscalYear` $\to$ **Whole Number (`123`)**.
3. **Harmonizing Typographical Branch Drift via Advanced M Formula (Custom Column)**:
   Excel workbooks and SQL views often suffer from manual entry variations (e.g., `"Alex Branch"`, `"سموحة"`, `"التجمع"`, `"المعادي"`). Rather than configuring a long chain of GUI conditional clicks, you can deploy an advanced functional M formula that performs resilient keyword matching against your conformed `Dim_Branch` canonical names:

   * Go to **Add Column > Custom Column**.
   * Column Name: `StandardizedBranch`
   * **Formula (Advanced Functional M Pattern Matcher)**:
     ```powerquery
     let
         Raw = Text.Trim(Text.From([CostCenter_Branch])),
         // Pattern mapping rules: {Keyword, Canonical Dim_Branch Name}
         Rules = {
             {"Alex", "الإسكندرية - سموحة"},
             {"سموح", "الإسكندرية - سموحة"},
             {"معاد", "القاهرة - المعادي"},
             {"دقي", "الجيزة - الدقي"},
             {"الدقي", "الجيزة - الدقي"},
             {"تجمع", "القاهرة - التجمع الخامس"},
             {"بورسعيد", "بورسعيد - الشرق"},
             {"منصور", "الدقهلية - المنصورة"},
             {"طنطا", "الغربية - طنطا"},
             {"أكتوبر", "الجيزة - 6 أكتوبر"},
             {"اكتوبر", "الجيزة - 6 أكتوبر"},
             {"زايد", "الجيزة - الشيخ زايد"},
             {"أسيوط", "أسيوط - أسيوط الجديدة"},
             {"اسيوط", "أسيوط - أسيوط الجديدة"},
             {"دمياط", "دمياط - دمياط الجديدة"},
             {"ذكية", "القاهرة - القرية الذكية"},
             {"لوران", "الإسكندرية - لوران"},
             {"مصر الجديدة", "القاهرة - مصر الجديدة"}
         },
         // Find the first rule where the raw branch contains the keyword
         Match = List.First(
             List.Select(Rules, each Text.Contains(Raw, _{0}, Comparer.OrdinalIgnoreCase)),
             {null, Raw}
         ){1}
     in
         Match
     ```

   * *(Alternative: Fast Conditional Expression)*:
     ```powerquery
     if Text.Contains([CostCenter_Branch], "Alex", Comparer.OrdinalIgnoreCase) or Text.Contains([CostCenter_Branch], "سموحة") then "الإسكندرية - سموحة"
     else if Text.Contains([CostCenter_Branch], "معاد") then "القاهرة - المعادي"
     else if Text.Contains([CostCenter_Branch], "دقي") then "الجيزة - الدقي"
     else if Text.Contains([CostCenter_Branch], "تجمع") then "القاهرة - التجمع الخامس"
     else if Text.Contains([CostCenter_Branch], "بورسعيد") then "بورسعيد - الشرق"
     else [CostCenter_Branch]
     ```

   * Click **OK** $\to$ set column data type to **Text (`ABC`)**.
4. **Generating Smart Integer Date Key for Quarter Dimension Alignment**:
   Because budgets are set quarterly, we map each quarter to its quarter-start date key (`20260101`, `20260401`, `20260701`, `20261001`):
   * Go to **Add Column > Custom Column**.
   * Column Name: `DateKey`
   * Formula:
     ```powerquery
     if [Quarter] = "Q1" then [FiscalYear] * 10000 + 101 
     else if [Quarter] = "Q2" then [FiscalYear] * 10000 + 401 
     else if [Quarter] = "Q3" then [FiscalYear] * 10000 + 701 
     else [FiscalYear] * 10000 + 1001
     ```
   * Click **OK** $\to$ set type to **Whole Number (`123`)**.
5. **Adding Surrogate Primary Key**:
   * Go to **Add Column > Index Column > From 1**.
   * Rename to `BudgetKey` $\to$ set type to **Whole Number (`123`)**.

#### 4. Architectural Note: Handling Mixed Granularity in Power BI & DAX
> [!IMPORTANT]
> **Resolving Mixed Granularity (Quarterly Budget vs Daily/Monthly HR Events)**:
> - **The Problem**: `Fact_DepartmentBudget` is at the grain of `Department + Branch + Quarter`, whereas `Fact_DailyAttendance` is `Employee + Day` and `Fact_WorkforceSnapshot` is `Employee + Month`. Creating a direct relationship between them creates a toxic many-to-many ambiguity.
> - **The Solution**: Connect `Fact_DepartmentBudget` exclusively to conformed dimensions (`Dim_Department` on `DepartmentName`, `Dim_Branch` on `StandardizedBranch`, and `Dim_Date` on `DateKey`). Never join fact tables directly to each other!
> - **DAX Variance Analysis (Relative Measures Architecture)**: To compute budget vs actual variance without errors, create the base measures first, then derive the relative variance and burn-rate measures:
>
>   **1. Base Measure — Actual Monthly Payroll (EGP)**:
>   *(If using `Fact_WorkforceSnapshot`)*:
>   ```dax
>   Actual Monthly Payroll EGP = 
>   SUM('Fact_WorkforceSnapshot'[BaseSalary])
>   ```
>   *(Or if using `Dim_Employee`)*:
>   ```dax
>   Actual Monthly Payroll EGP = 
>   SUM('Dim_Employee'[الراتب الأساسي])
>   ```
>
>   **2. Base Measure — Allocated Monthly Budget (EGP)**:
>   *(Budgets are quarterly, so divide quarterly budget by 3 for monthly comparison)*:
>   ```dax
>   Allocated Monthly Salary Budget EGP = 
>   DIVIDE(SUM('Fact_DepartmentBudget'[AllocatedSalaryBudget_EGP]), 3, 0)
>   ```
>   *(Note: If your column was imported from SQL Server `raw.Finance_Budget_Plan`, replace `[AllocatedSalaryBudget_EGP]` with `[Budget_EGP]`)*.
>
>   **3. Relative Measure — Budget Variance (EGP)**:
>   ```dax
>   Budget Variance EGP = 
>   VAR ActualPayroll = [Actual Monthly Payroll EGP]
>   VAR MonthlyBudget = [Allocated Monthly Salary Budget EGP]
>   RETURN
>       IF(
>           NOT(ISBLANK(ActualPayroll)) && NOT(ISBLANK(MonthlyBudget)),
>           ActualPayroll - MonthlyBudget,
>           BLANK()
>       )
>   ```
>
>   **4. Relative Measure — Budget Variance %**:
>   ```dax
>   Budget Variance Pct = 
>   DIVIDE([Budget Variance EGP], [Allocated Monthly Salary Budget EGP], BLANK())
>   ```
>
>   **5. Relative Measure — Payroll Burn Rate %**:
>   ```dax
>   Payroll Burn Rate Pct = 
>   DIVIDE([Actual Monthly Payroll EGP], [Allocated Monthly Salary Budget EGP], BLANK())
>   ```
>
>   **6. Base Measure — Budgeted Target Headcount**:
>   *(Note: For SQL Server `raw.Finance_Budget_Plan`, the column is `[Headcount]`. If unpivoted from Excel, it was named `[BudgetedHeadcount]`)*:
>   ```dax
>   Budgeted Target Headcount = 
>   SUM('Fact_DepartmentBudget'[Headcount])
>   ```
>
>   **7. Base Measure — Actual Headcount**:
>   ```dax
>   Actual Headcount = 
>   COUNTROWS('Dim_Employee')
>   ```
>
>   **8. Relative Measure — Headcount Variance (Actual vs Target)**:
>   ```dax
>   Headcount Variance = 
>   VAR ActualHC = [Actual Headcount]
>   VAR TargetHC = [Budgeted Target Headcount]
>   RETURN
>       IF(NOT(ISBLANK(TargetHC)), ActualHC - TargetHC, BLANK())
>   ```
>
>   **9. Relative Measure — Headcount Variance %**:
>   ```dax
>   Headcount Variance Pct = 
>   DIVIDE([Headcount Variance], [Budgeted Target Headcount], BLANK())
>   ```
>
>   **10. Relative Measure — Headcount Fulfillment Rate %**:
>   ```dax
>   Headcount Fulfillment Pct = 
>   DIVIDE([Actual Headcount], [Budgeted Target Headcount], BLANK())
>   ```
>
>   *(Optional: Standalone All-In-One Formulas if you prefer single measures without precursor measures)*:
>   ```dax
>   Budget Variance EGP = 
>   VAR ActualPayroll = SUM('Dim_Employee'[الراتب الأساسي])
>   VAR MonthlyBudget = DIVIDE(SUM('Fact_DepartmentBudget'[Budget_EGP]), 3, 0)
>   RETURN
>       IF(NOT(ISBLANK(ActualPayroll)) && NOT(ISBLANK(MonthlyBudget)), ActualPayroll - MonthlyBudget, BLANK())
>   ```
>   ```dax
>   Headcount Variance = 
>   VAR ActualHC = COUNTROWS('Dim_Employee')
>   VAR TargetHC = SUM('Fact_DepartmentBudget'[Headcount])
>   RETURN
>       IF(NOT(ISBLANK(TargetHC)), ActualHC - TargetHC, BLANK())
>   ```

---

### Step 2.5: Ingesting LMS Training Records (`Fact_TrainingCompletions`) via GUI

1. Go to **Home > New Source > Text/CSV** $\to$ select `data/raw/lms_course_completions.csv` $\to$ click **OK**.
2. Rename query to `Fact_TrainingCompletions`.
3. Set types: `CompletionDate` to **Date**, `Score` to **Decimal Number**, `CertificationCost_EGP` to **Fixed Decimal**.
4. **Extracting `Dim_Course` via GUI**:
   * Right-click `Fact_TrainingCompletions` $\to$ **Reference** $\to$ rename to `Dim_Course`.
   * Select `CourseID`, `CourseName`, `SkillDomain` $\to$ right-click $\to$ **Remove Other Columns**.
   * Go to **Home > Remove Rows > Remove Duplicates**. Add Index Column as `CourseKey`.
5. In `Fact_TrainingCompletions`:
   * Go to **Add Column > Conditional Column** as `IsPassed`: If `Score` $\ge 70$ then `1`, Else `0`.
   * Add Custom Column as `CompletionDateKey`: `Date.Year([CompletionDate]) * 10000 + Date.Month([CompletionDate]) * 100 + Date.Day([CompletionDate])`.
   * Add Index Column as `CompletionKey`.

---

### Step 2.5b: Ingesting Talent Development Telemetry directly from Microsoft SQL Server (`raw.LMS_Certifications`) via GUI

When ingesting LMS certifications from Microsoft SQL Server instead of a flat CSV file, follow this native SQL Server import workflow:

#### 1. Connecting to SQL Server:
1. In Power Query Editor, go to **Home > New Source > SQL Server**.
2. In the connection dialog:
   * **Server**: `localhost` (or `.` or `localhost\SQLEXPRESS` or your machine name).
   * **Database**: `EnterpriseHR_DWH`.
   * **Data Connectivity mode**: **Import** $\to$ click **OK**.

#### 2. Selecting `raw.LMS_Certifications` in the Navigator:
1. Expand `EnterpriseHR_DWH` $\to$ expand the **`raw`** schema folder.
2. Check the checkbox next to **`LMS_Certifications`** (`[raw].[LMS_Certifications]`).
3. The preview displays 7,197 records with columns: `EmployeeID`, `CourseID`, `CourseName`, `SkillDomain`, `CompletionDate`, `Score`, `Status`, `Cost_EGP`.
4. Click **OK** (or **Transform Data**).

#### 3. Power Query Cleansing, Scoring & Keys via GUI:
1. In the **Queries** pane, rename `LMS_Certifications` to **`Fact_LMS_Certifications_SQL`** (or `Fact_TrainingCompletions`).
2. **Setting Data Types Visually**:
   * Click icon in header `EmployeeID` $\to$ **Text (`ABC`)**.
   * Click icon in header `CourseID` $\to$ **Text (`ABC`)**.
   * Click icon in header `CourseName` $\to$ **Text (`ABC`)**.
   * Click icon in header `SkillDomain` $\to$ **Text (`ABC`)**.
   * Click icon in header `CompletionDate` $\to$ **Date (`📅`)**.
   * Click icon in header `Score` $\to$ **Whole Number (`123`)**.
   * Click icon in header `Status` $\to$ **Text (`ABC`)**.
   * Click icon in header `Cost_EGP` $\to$ **Fixed Decimal Number (`$`)**.
3. **Deriving Boolean Pass Flag (`IsPassed`)**:
   * Go to **Add Column > Conditional Column**.
   * Column Name: `IsPassed`
   * Rule: If `Status` equals `Completed` then `1`, Else `0`.
   * Click **OK** $\to$ set type to **Whole Number (`123`)**.
4. **Generating Date Key for Galaxy Schema Joining**:
   * Go to **Add Column > Custom Column**.
   * Column Name: `CompletionDateKey`
   * Formula:
     ```powerquery
     Date.Year([CompletionDate]) * 10000 + Date.Month([CompletionDate]) * 100 + Date.Day([CompletionDate])
     ```
   * Click **OK** $\to$ set type to **Whole Number (`123`)**.
5. **Adding Surrogate Primary Key**:
   * Go to **Add Column > Index Column > From 1**.
   * Rename to `CompletionKey` $\to$ set type to **Whole Number (`123`)**.

---

### Step 2.6: Production M Code for `Dim_Date` (Enterprise Calendar)

> [!TIP]
> While data tables are best built visually via the GUI, an enterprise calendar requires over 25 synchronized temporal attributes (relative offsets, fiscal quarters, Middle East weekends).
> 
> **How to apply**: Go to **Home > New Source > Blank Query**, click **Advanced Editor** in the ribbon, replace the placeholder text with the production M script below, and click **Done**.

```powerquery
let
    // 1. Dynamic Boundary Definition
    StartDate = #date(2024, 1, 1),
    EndDate = #date(2026, 12, 31),
    Today = DateTime.Date(DateTime.LocalNow()),
    CurrentYear = Date.Year(Today),
    CurrentMonth = Date.Month(Today),

    // 2. Generate Continuous Date Series
    DayCount = Duration.Days(EndDate - StartDate) + 1,
    DateList = List.Dates(StartDate, DayCount, #duration(1, 0, 0, 0)),
    #"Converted to Table" = Table.FromList(DateList, Splitter.SplitByNothing(), {"FullDate"}, null, ExtraValues.Error),
    #"Typed FullDate" = Table.TransformColumnTypes(#"Converted to Table",{{"FullDate", type date}}),

    // 3. Calendar Dimensions
    #"Added DateKey" = Table.AddColumn(#"Typed FullDate", "DateKey", each Date.Year([FullDate]) * 10000 + Date.Month([FullDate]) * 100 + Date.Day([FullDate]), Int64.Type),
    #"Added Year" = Table.AddColumn(#"Added DateKey", "CalendarYear", each Date.Year([FullDate]), Int64.Type),
    #"Added Quarter" = Table.AddColumn(#"Added Year", "CalendarQuarter", each Date.QuarterOfYear([FullDate]), Int64.Type),
    #"Added QuarterName" = Table.AddColumn(#"Added Quarter", "CalendarQuarterName", each "Q" & Text.From([CalendarQuarter]) & "-" & Text.From([CalendarYear]), type text),
    #"Added Month" = Table.AddColumn(#"Added QuarterName", "MonthNumberOfYear", each Date.Month([FullDate]), Int64.Type),
    #"Added MonthName" = Table.AddColumn(#"Added Month", "MonthName", each Date.MonthName([FullDate], "en-US"), type text),
    #"Added MonthShort" = Table.AddColumn(#"Added MonthName", "MonthShortName", each Text.Start([MonthName], 3), type text),
    #"Added YearMonthKey" = Table.AddColumn(#"Added MonthShort", "YearMonthKey", each [CalendarYear] * 100 + [MonthNumberOfYear], Int64.Type),
    #"Added DayOfMonth" = Table.AddColumn(#"Added YearMonthKey", "DayNumberOfMonth", each Date.Day([FullDate]), Int64.Type),
    #"Added DayOfWeek" = Table.AddColumn(#"Added DayOfMonth", "DayNumberOfWeek", each Date.DayOfWeek([FullDate], Day.Monday) + 1, Int64.Type),
    #"Added DayName" = Table.AddColumn(#"Added DayOfWeek", "DayNameOfWeek", each Date.DayOfWeekName([FullDate], "en-US"), type text),
    #"Added DayOfYear" = Table.AddColumn(#"Added DayName", "DayNumberOfYear", each Date.DayOfYear([FullDate]), Int64.Type),

    // 4. Middle East (Egypt) Weekend & Workday Logic (Friday=5, Saturday=6 in 1-based Monday index)
    #"Added IsWeekend" = Table.AddColumn(#"Added DayOfYear", "IsWeekend", each if [DayNumberOfWeek] = 5 or [DayNumberOfWeek] = 6 then 1 else 0, Int64.Type),
    #"Added IsWorkDay" = Table.AddColumn(#"Added IsWeekend", "IsWorkingDay", each if [IsWeekend] = 0 then 1 else 0, Int64.Type),

    // 5. Fiscal Calendar Attributes (Standard Calendar Fiscal Year)
    #"Added FiscalYear" = Table.AddColumn(#"Added IsWorkDay", "FiscalYear", each [CalendarYear], Int64.Type),
    #"Added FiscalQuarter" = Table.AddColumn(#"Added FiscalYear", "FiscalQuarter", each [CalendarQuarter], Int64.Type),
    #"Added FiscalQuarterName" = Table.AddColumn(#"Added FiscalQuarter", "FiscalQuarterName", each "FQ" & Text.From([FiscalQuarter]) & " " & Text.From([FiscalYear]), type text),

    // 6. Relative Offsets (Crucial for Rolling Dynamic Slicers in Power BI)
    #"Added MonthOffset" = Table.AddColumn(#"Added FiscalQuarterName", "RelativeMonthOffset", each ((Date.Year([FullDate]) - CurrentYear) * 12) + (Date.Month([FullDate]) - CurrentMonth), Int64.Type),
    #"Added DayOffset" = Table.AddColumn(#"Added MonthOffset", "RelativeDayOffset", each Duration.Days([FullDate] - Today), Int64.Type),
    #"Added YearOffset" = Table.AddColumn(#"Added DayOffset", "RelativeYearOffset", each Date.Year([FullDate]) - CurrentYear, Int64.Type),
    #"Added IsCurrentMonth" = Table.AddColumn(#"Added YearOffset", "IsCurrentMonth", each if [RelativeMonthOffset] = 0 then 1 else 0, Int64.Type),
    #"Added IsCurrentYear" = Table.AddColumn(#"Added IsCurrentMonth", "IsCurrentYear", each if [RelativeYearOffset] = 0 then 1 else 0, Int64.Type)
in
    #"Added IsCurrentYear"
```

---

### Step 2.7: Ingesting Periodic Workforce Snapshot (`Fact_WorkforceSnapshot`) via GUI

#### Architectural Context: The Periodic Snapshot Fact Table
In Kimball dimensional architecture, human capital analytics requires distinguishing between:
1. **Transaction Fact Tables** (`Fact_DailyAttendance`, `Fact_TrainingCompletions`): Record discrete, instantaneous events (badge swipes, exam completions).
2. **Accumulating Snapshot Fact Tables** (`Fact_DepartmentBudget`): Track finite planning horizons with quarterly milestones.
3. **Periodic Snapshot Fact Tables (`Fact_WorkforceSnapshot`)**: Capture point-in-time states of all active entities at regular reporting intervals (e.g., monthly census cutoff).

`Fact_WorkforceSnapshot` forms the analytical spine for:
* **Diagnostic 1 (Salary Compression & Flight Risk Index)**: Quantifies wage inversion (tenured employees earning below newly hired peers in the same job role).
* **Diagnostic 3 (Ghost Worker Audits)**: Serves as the authoritative payroll denominator to cross-reference against physical turnstile entries in `Fact_DailyAttendance`.
* **Diagnostic 5 (Survivorship Bias & Attrition Velocity)**: Enables cohort tracking of performance ratings before employees resign.
* **Diagnostic 6 (Equal Pay & Compensation Parity)**: Computes percentile distributions and wage parity across organizational levels.

* **Grain**: Exactly 1 row per employee per monthly snapshot period (`EmployeeKey` + `SnapshotDateKey`).
* **Source Path**: `data/processed/Fact_WorkforceSnapshot.csv`.

#### 1. Ingesting `Fact_WorkforceSnapshot.csv` via Power Query Ribbon:
1. In Power Query Editor, go to the **Home** ribbon tab.
2. Click **New Source > Text/CSV** $\to$ navigate to `data/processed/Fact_WorkforceSnapshot.csv` $\to$ click **Open**.
3. In the preview dialog, ensure **File Origin** is set to `65001: Unicode (UTF-8)` and **Delimiter** is `Comma`.
4. Click **OK** (or **Transform Data**).
5. In the **Queries** pane, rename the query to **`Fact_WorkforceSnapshot`**.

#### 2. Visual Data Type Casting via Column Headers:
Click the data type icon in each column header and verify:
* `SnapshotKey`: **Whole Number (`123`)** *(Surrogate Primary Key)*
* `SnapshotDateKey`: **Whole Number (`123`)** *(FK to `Dim_Date.DateKey`)*
* `EmployeeKey`: **Whole Number (`123`)** *(FK to `Dim_Employee.EmployeeKey`)*
* `DepartmentKey`: **Whole Number (`123`)** *(FK to `Dim_Department.DepartmentKey`)*
* `BranchKey`: **Whole Number (`123`)** *(FK to `Dim_Branch.BranchKey`)*
* `BaseSalary`: **Fixed Decimal Number (`$`)** *(Monthly compensation in EGP)*
* `AnnualPerformanceRating`: **Decimal Number (`1.2`)** *(Appraisal score: 1.00 to 5.00)*
* `TenureMonths`: **Whole Number (`123`)** *(Cumulative service in whole months)*
* `TenureYears`: **Decimal Number (`1.2`)** *(Exact decimal tenure, e.g. 3.42)*
* `SalaryPercentileInRole`: **Decimal Number (`1.2`)** *(Percentile rank: 0.0000 to 1.0000)*
* `IsSalaryCompressed`: **Whole Number (`123`)** *(Boolean flag: `1` if tenured employee suffers wage compression)*
* `EmploymentStatus`: **Text (`ABC`)** *(`Active`, `OnLeave`, or `Separated`)*

#### 3. Recommended GUI Method: Deriving `Fact_WorkforceSnapshot` from `Dim_Employee` Reference Query

When building the data mart directly inside Power BI without relying on pre-processed CSVs or direct SQL marts, deriving `Fact_WorkforceSnapshot` via a **Reference Query** from `Dim_Employee` is the standard enterprise design pattern.

> [!IMPORTANT]
> **Why Reference Queries Initially Trigger the "One-to-One (1:1) Both" Trap**:
> When you right-click `Dim_Employee` and select **Reference**, the new query inherits the exact same 7,000 employee rows. If you leave it with only 1 snapshot cutoff date, both tables have identical 7,000 `EmployeeKey`s, causing Power BI to mistakenly default to `One to one (1:1)` with bidirectional `Both` filtering.
> 
> By adding dynamic **Multi-Period Snapshot Expansion** (Steps 3 & 4 below), each employee dynamically receives 3 rolling monthly snapshot records (21,000 rows total). This guarantees that Power BI's relationship engine **automatically and permanently detects Cardinality as `Many to one (*:1)` and Cross-filter direction as `Single`** with zero chance of refresh failure!

##### Step-by-Step GUI Clickpath:
1. In the **Queries** pane, right-click `Dim_Employee` $\to$ select **Reference**.
2. Rename the new query to **`Fact_WorkforceSnapshot`**.
3. **Select Relevant Analytical & Metric Columns**:
   * Go to **Home ribbon > Choose Columns**.
   * Select: `EmployeeKey`, `الرقم التعريفي`, `القسم`, `الفرع`, `الراتب الأساسي`, `تقييم الأداء السنوي`, `تاريخ التعيين`, `EmploymentStatus`.
   * Click **OK**.
4. **Generate Dynamic Multi-Period Snapshot Horizons (`{0..2}`)**:
   * Go to **Add Column > Custom Column**.
   * **Column Name**: `MonthOffset`
   * **Formula**:
     ```powerquery
     {0..2}
     ```
     *(Generates a dynamic in-memory list: `0` = current closed month, `1` = 1 month prior, `2` = 2 months prior).*
   * Click **OK**.
   * In the `MonthOffset` column header, click the **Expand icon (`↔`)** $\to$ select **Expand to New Rows**.
   * The query dynamically expands from 7,000 rows to **21,000 rows**!
5. **Add Dynamic `SnapshotDateKey` (Anchored to `MonthOffset`)**:
   * Go to **Add Column > Custom Column**.
   * **Column Name**: `SnapshotDateKey`
   * **Dynamic Formula**:
     ```powerquery
     let
         Today = DateTime.Date(DateTime.LocalNow()),
         SnapshotDate = Date.EndOfMonth(Date.AddMonths(Today, - [MonthOffset]))
     in
         Date.Year(SnapshotDate) * 10000 + Date.Month(SnapshotDate) * 100 + Date.Day(SnapshotDate)
     ```
   * Set type to **Whole Number (`123`)**.
6. **Calculate Dynamic Tenure in Years & Months (Anchored to Snapshot Date)**:
   * Go to **Add Column > Custom Column**. Name: `TenureYears`.
   * **Dynamic Formula**:
     ```powerquery
     let
         Today = DateTime.Date(DateTime.LocalNow()),
         SnapshotDate = Date.EndOfMonth(Date.AddMonths(Today, - [MonthOffset])),
         HireDate = DateTime.Date([تاريخ التعيين])
     in
         Number.Round(Duration.TotalDays(SnapshotDate - HireDate) / 365.25, 2)
     ```
   * Set type to **Decimal Number (`1.2`)**.

   * Go to **Add Column > Custom Column**. Name: `TenureMonths`.
   * **Dynamic Formula**:
     ```powerquery
     let
         Today = DateTime.Date(DateTime.LocalNow()),
         SnapshotDate = Date.EndOfMonth(Date.AddMonths(Today, - [MonthOffset])),
         HireDate = DateTime.Date([تاريخ التعيين])
     in
         Number.IntegerDivide(Duration.TotalDays(SnapshotDate - HireDate), 30.4375)
     ```
   * Set type to **Whole Number (`123`)**.
7. **Look up Surrogate Foreign Keys (`DepartmentKey` & `BranchKey`) via GUI Merge**:
   > [!NOTE]
   > Because `Fact_WorkforceSnapshot` was referenced from `Dim_Employee`, it initially contains the raw Arabic department and branch text names (`القسم` and `الفرع`) rather than integer keys. To establish integer relationships with `Dim_Department` and `Dim_Branch`, perform these two quick GUI merges:

   * **A. Looking up `DepartmentKey` from `Dim_Department`**:
     1. In the **Home** ribbon, click **Merge Queries > Merge Queries**.
     2. In the top table (`Fact_WorkforceSnapshot`), click the header **`القسم`**.
     3. In the dropdown below, select **`Dim_Department`** $\to$ click the header **`DepartmentName`** (or `القسم`).
     4. Join Kind: **Left Outer (all from first, matching from second)** $\to$ click **OK**.
     5. A new column `Dim_Department` with `[Table]` links appears on the far right. Click the **Expand icon (`↔`)** at the top right of the header:
        * Uncheck *(Select All Columns)* $\to$ check only **`DepartmentKey`**.
        * Uncheck *Use original column name as prefix*.
        * Click **OK**.
     6. Set the data type of `DepartmentKey` to **Whole Number (`123`)**.

   * **B. Looking up `BranchKey` from `Dim_Branch`**:
     1. In the **Home** ribbon, click **Merge Queries > Merge Queries**.
     2. In `Fact_WorkforceSnapshot`, click the header **`الفرع`**.
     3. In the dropdown below, select **`Dim_Branch`** $\to$ click the header **`BranchName`** (or `الفرع`).
     4. Join Kind: **Left Outer** $\to$ click **OK**.
     5. In the new `Dim_Branch` column header, click the **Expand icon (`↔`)**:
        * Check only **`BranchKey`**.
        * Uncheck *Use original column name as prefix*.
        * Click **OK**.
     6. Set the data type of `BranchKey` to **Whole Number (`123`)**.
     7. *(Optional Clean-Up)*: Select headers **`القسم`** and **`الفرع`** $\to$ right-click $\to$ select **Remove** (their dimensions now provide these names).

8. **Clean Up Helper Column & Add Surrogate PK**:
   * Right-click the `MonthOffset` column header $\to$ select **Remove**.
   * Go to **Add Column > Index Column > From 1**. Rename to `SnapshotKey`. Drag `SnapshotKey` to the far left $\to$ set type to **Whole Number (`123`)**.
9. **Verify Column Data Types**:
   * `SnapshotKey`: **Whole Number (`123`)**
   * `SnapshotDateKey`: **Whole Number (`123`)**
   * `EmployeeKey`: **Whole Number (`123`)**
   * `DepartmentKey`: **Whole Number (`123`)**
   * `BranchKey`: **Whole Number (`123`)**
   * `BaseSalary` (`الراتب الأساسي`): **Fixed Decimal Number (`$`)**
   * `AnnualPerformanceRating` (`تقييم الأداء السنوي`): **Decimal Number (`1.2`)**
   * `EmploymentStatus`: **Text (`ABC`)**
10. Click **Home > Close & Apply**.
11. In Power BI Desktop **Model View**, establish the Galaxy Schema relationships:
    * Drag `Fact_WorkforceSnapshot[EmployeeKey]` $\to$ `Dim_Employee[EmployeeKey]` (`Many-to-One (*:1)`, Single)
    * Drag `Fact_WorkforceSnapshot[DepartmentKey]` $\to$ `Dim_Department[DepartmentKey]` (`Many-to-One (*:1)`, Single)
    * Drag `Fact_WorkforceSnapshot[BranchKey]` $\to$ `Dim_Branch[BranchKey]` (`Many-to-One (*:1)`, Single)
    * Drag `Fact_WorkforceSnapshot[SnapshotDateKey]` $\to$ `Dim_Date[DateKey]` (`Many-to-One (*:1)`, Single)

> [!TIP]
> **Alternative: Relating Directly on Natural Text Keys (Zero Merge Required)**:
> If you prefer not to perform the merges in Power Query and want to keep your existing columns:
> * You can connect directly in the **Model View** using the text columns:
>   * `Fact_WorkforceSnapshot[القسم]` $\to$ `Dim_Department[DepartmentName]` (`Many-to-One (*:1)`, Single)
>   * `Fact_WorkforceSnapshot[الفرع]` $\to$ `Dim_Branch[BranchName]` (`Many-to-One (*:1)`, Single)
> * Both `DepartmentName` and `BranchName` are unique in their respective dimension tables, so Power BI creates valid `Many-to-One (*:1)` relationships directly without any errors. However, adding `DepartmentKey` and `BranchKey` via Merge Queries is the Kimball enterprise standard.

> [!TIP]
> **What if You Prefer Only a Single Month's Snapshot?**
> If you prefer not to expand across multiple months and keep exactly 7,000 rows, skip Step 4 (`MonthOffset`). When creating the relationship in Power BI Desktop's **New Relationship** dialog, simply click the **Cardinality** dropdown $\to$ select **`Many to one (*:1)`**, and set **Cross-filter direction** $\to$ **`Single`**. Power BI fully supports this and will never revert.

---

### Step 2.7b: Enterprise SQL Server Ingestion — Ingesting `mart.Fact_WorkforceSnapshot` & `mart.Fact_Employee_SCD2` via GUI

In enterprise deployments backed by Microsoft SQL Server (`EnterpriseHR_DWH`), the data warehouse maintains both periodic monthly snapshots and full historical change records (SCD Type 2):

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ SQL Server Database Connection Dialog                                                 │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ Server:   [ localhost                                                      ]           │
│ Database: [ EnterpriseHR_DWH                                               ]           │
│ Data Connectivity mode: (•) Import   ( ) DirectQuery                                   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 1. Connecting to SQL Server:
1. Go to **Home > New Source > SQL Server**.
2. Server: `localhost` (or `.` or `localhost\SQLEXPRESS`). Database: `EnterpriseHR_DWH`. Mode: **Import**.
3. Authentication: **Windows > Use my current credentials** $\to$ click **Connect**.

#### 2. Selecting the Workforce Mart Tables in the Navigator:
1. Expand `EnterpriseHR_DWH` $\to$ expand the **`mart`** schema folder.
2. Check the box for **`Fact_WorkforceSnapshot`** (7,000 monthly employee census records).
3. *(Optional for Career Lifecycle Diagnostics)*: Check **`Fact_Employee_SCD2`** (12,392 temporal audit events tracking promotions, transfers, and compensation changes from `stg.Stg_HR_Audit`).
4. Click **OK** (or **Transform Data**).

#### 3. Power Query Cleansing & Optimization:
1. In `Fact_WorkforceSnapshot`, verify column data types matching the schema contract.
2. Ensure **Query Folding** is preserved by confirming the native SQL query indicator in the **Applied Steps** pane.
3. If using `Fact_Employee_SCD2`:
   * Set `ValidFrom` and `ValidTo` to **Date (`📅`)**.
   * Set `Salary_EGP` to **Fixed Decimal Number (`$`)**.
   * Set `IsCurrent` to **Whole Number (`123`)**.

---

### Step 2.8: The Complete Kimball Galaxy Constellation Model Topology

Before committing all queries to the Power BI Tabular Engine, verify that your data model strictly implements the Kimball Fact Constellation architecture. The dimensional model comprises **5 Conformed Dimensions** sharing relationships across **4 Galaxy Fact Tables**:

```
                                  ┌───────────────────┐
                                  │   Dim_Department  │
                                  │   (DepartmentKey) │
                                  └─────────┬─────────┘
                                            │
               ┌────────────────────────────┼────────────────────────────┐
               │ 1:*                        │ 1:*                        │ 1:*
               ▼                            ▼                            ▼
   ┌───────────────────────┐    ┌───────────────────────┐    ┌───────────────────────┐
   │ Fact_WorkforceSnapshot│    │ Fact_DepartmentBudget │    │  Dim_Employee (SCD-2) │
   │   (Monthly Snapshot)  │    │   (Quarterly FP&A)    │    │     (EmployeeKey)     │
   └───────────┬───────────┘    └───────────┬───────────┘    └───────────┬───────────┘
               │ 1:*                        │ 1:*                        │ 1:*
               │                            │             ┌──────────────┼──────────────┐
               │                            │             │              │              │
               ▼                            ▼             ▼              ▼              ▼
   ┌───────────────────────┐    ┌──────────────────────────────────┐   ┌───────────────────────┐
   │       Dim_Date        │◄───┤      Fact_DailyAttendance        │   │Fact_TrainingCompletion│
   │       (DateKey)       │    │           (Daily IoT)            │   │    (LMS Attempts)     │
   └───────────▲───────────┘    └─────────────────▲────────────────┘   └───────────┬───────────┘
               │                                  │                                │ 1:*
               │ 1:*                              │ 1:*                            ▼
               │                        ┌─────────┴─────────┐            ┌───────────────────┐
               └────────────────────────┤     Dim_Branch    │            │    Dim_Course     │
                                        │    (BranchKey)    │            │    (CourseKey)    │
                                        └───────────────────┘            └───────────────────┘
```

#### Galaxy Schema Referential Integrity Matrix:

| Relationship Source (Fact Table) | Foreign Key Column | Dimension Target Table | Primary Key Column | Cardinality | Cross-Filter Direction | Business Grain |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **`Fact_WorkforceSnapshot`** | `EmployeeKey` | `Dim_Employee` | `EmployeeKey` | Many-to-One (`*:1`) | Single | 1 row per Employee per Month |
| **`Fact_WorkforceSnapshot`** | `DepartmentKey` | `Dim_Department` | `DepartmentKey` | Many-to-One (`*:1`) | Single | Monthly department snapshot |
| **`Fact_WorkforceSnapshot`** | `BranchKey` | `Dim_Branch` | `BranchKey` | Many-to-One (`*:1`) | Single | Monthly branch census |
| **`Fact_WorkforceSnapshot`** | `SnapshotDateKey` | `Dim_Date` | `DateKey` | Many-to-One (`*:1`) | Single | Monthly snapshot cutoff date |
| **`Fact_DailyAttendance`** | `EmployeeKey` | `Dim_Employee` | `EmployeeKey` | Many-to-One (`*:1`) | Single | 1 row per Employee per Day |
| **`Fact_DailyAttendance`** | `BranchKey` | `Dim_Branch` | `BranchKey` | Many-to-One (`*:1`) | Single | Physical access facility |
| **`Fact_DailyAttendance`** | `AccessDateKey` | `Dim_Date` | `DateKey` | Many-to-One (`*:1`) | Single | Calendar access date |
| **`Fact_DepartmentBudget`** | `DepartmentKey` | `Dim_Department` | `DepartmentKey` | Many-to-One (`*:1`) | Single | 1 row per Dept per Branch per Quarter |
| **`Fact_DepartmentBudget`** | `BranchKey` | `Dim_Branch` | `BranchKey` | Many-to-One (`*:1`) | Single | Regional branch allocation |
| **`Fact_DepartmentBudget`** | `DateKey` | `Dim_Date` | `DateKey` | Many-to-One (`*:1`) | Single | Quarter commencement date |
| **`Fact_TrainingCompletions`** | `EmployeeKey` | `Dim_Employee` | `EmployeeKey` | Many-to-One (`*:1`) | Single | 1 row per Course attempt |
| **`Fact_TrainingCompletions`** | `CourseKey` | `Dim_Course` | `CourseKey` | Many-to-One (`*:1`) | Single | Course catalog entity |
| **`Fact_TrainingCompletions`** | `CompletionDateKey` | `Dim_Date` | `DateKey` | Many-to-One (`*:1`) | Single | Examination completion date |

> [!CAUTION]
> **Kimball Galaxy Cardinality Rules**:
> 1. **Never Create Direct Fact-to-Fact Relationships**: Joining `Fact_DailyAttendance` directly to `Fact_WorkforceSnapshot` or `Fact_DepartmentBudget` creates a toxic Many-to-Many circular path resulting in double-counting and VertiPaq memory exhaustion.
> 2. **Always Filter Downward Through Dimensions**: Slicers on `Dim_Department[DepartmentName]`, `Dim_Branch[Region]`, or `Dim_Date[FiscalQuarter]` propagate naturally to all 4 fact tables simultaneously.
> 3. **Single Cross-Filter Direction (`→`)**: Keep all relationship cross-filtering set to **Single**. Bidirectional filtering introduces ambiguous filter paths and severe performance degradation on large datasets.

---

### ⚠️ Deep Dive: Resolving the "One to One (1:1) Both" Auto-Detection Trap

When connecting `Fact_WorkforceSnapshot` to `Dim_Employee` on `EmployeeKey` in Power BI Desktop's **New Relationship** dialog, Power BI will frequently auto-detect:
* **Cardinality**: `One to one (1:1)`
* **Cross-filter direction**: `Both`

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ New relationship Dialog (Power BI Desktop)                                             │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ From table: [ Fact_WorkforceSnapshot ]  ->  Column: [ EmployeeKey ]                    │
│ To table:   [ Dim_Employee           ]  ->  Column: [ EmployeeKey ]                    │
│                                                                                        │
│ Cardinality:            [ One to one (1:1)               ▼ ]  <-- ⚠️ ANTI-PATTERN      │
│ Cross-filter direction: [ Both                           ▼ ]  <-- ⚠️ AMBIGUOUS FILTER  │
│ [✔] Make this relationship active                                                      │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

#### Why Does Power BI Auto-Detect `One to one (1:1)`?
Power BI samples the distinct values of `EmployeeKey` in both tables:
1. In `Dim_Employee`, each employee appears once (7,000 unique keys, `1` to `7000`).
2. In the initial baseline snapshot of `Fact_WorkforceSnapshot`, there is currently **1 single monthly census cutoff** (`SnapshotDateKey = 20260228`). Thus, each employee also appears exactly once (7,000 unique keys).
3. Because both sides of the join have unique keys in the sample, Power BI heuristically assumes this is a 1:1 relationship with bidirectional cross-filtering.

#### Why `1:1 Both` is a Dangerous Modeling Anti-Pattern:
1. **Breaks Future Scheduled Refreshes**: A **Periodic Snapshot Fact Table** by definition accumulates multiple periodic snapshots over time (e.g. Month 1, Month 2, Month 3). As soon as the next month's census is appended, `EmployeeKey` will have duplicate values in `Fact_WorkforceSnapshot`. A `1:1` relationship will **immediately crash your scheduled refresh** with:
   > *"Column 'EmployeeKey' in Table 'Fact_WorkforceSnapshot' contains duplicate values, which is not allowed for the 'one' side of a one-to-one relationship."*
2. **Bidirectional Filter Ambiguity (`Both`)**: `Both` cross-filtering allows filter propagation from the fact table back up into the dimension, and sideways into `Fact_DailyAttendance` and `Fact_DepartmentBudget`. This causes circular evaluation loops, inaccurate measure totals, and VertiPaq memory bloat.

---

#### Solution 1: Direct Override in the Relationship Dialog (Recommended & Standard)
Power BI **always permits** defining a `Many to one (*:1)` relationship even if the "Many" table currently contains only distinct values:
1. In the **New relationship** (or **Edit relationship**) dialog:
   * Click the **Cardinality** dropdown $\to$ select **`Many to one (*:1)`** (with `Fact_WorkforceSnapshot` on the Many `*` side, and `Dim_Employee` on the One `1` side).
   * Click the **Cross-filter direction** dropdown $\to$ select **`Single`** (filter propagates from `Dim_Employee` $\to$ `Fact_WorkforceSnapshot`).
   * Ensure **Make this relationship active** is checked.
   * Click **Save**.
2. Power BI saves this explicitly in the tabular model (TMDL), guaranteeing that future monthly snapshots will ingest seamlessly without breaking.

---

#### Solution 2: Dynamic Source-Level Multi-Period Expansion in Power Query GUI (100% Automated & Reliable)

Rather than manually duplicating queries or hardcoding static calendar dates (which introduces schema maintenance overhead and stale data), you can configure Power Query to **dynamically generate rolling monthly census snapshots** using native M list expansion.

Because each employee will naturally have multiple snapshot rows across consecutive monthly cutoffs, Power BI's relationship engine will **organically, deterministically, and permanently detect Cardinality as `Many to one (*:1)` with `Single` cross-filter direction**—with zero chance of refresh errors!

##### Step-by-Step Power Query GUI Clickpath:
1. Open **Power Query Editor** (**Home > Transform Data**).
2. Select your `Fact_WorkforceSnapshot` query in the left **Queries** pane.
3. **Generate Dynamic Monthly Cutoff Offsets**:
   * Go to the **Add Column** ribbon tab $\to$ click **Custom Column**.
   * **New column name**: `MonthOffset`
   * **Custom column formula**:
     ```powerquery
     {0..2}
     ```
     *(This creates an in-memory list `{0, 1, 2}` representing the current snapshot month, 1 month prior, and 2 months prior).*
   * Click **OK**.
4. **Expand to Multi-Period Periodic Snapshots**:
   * In the `MonthOffset` column header, click the **Expand icon (`↔`)** $\to$ select **Expand to New Rows**.
   * The query dynamically expands from 7,000 rows to **21,000 rows** (each employee now appears exactly 3 times across 3 reporting horizons).
5. **Compute Dynamic `SnapshotDateKey`**:
   * Go to **Add Column > Custom Column**. Name: `DynamicDateKey`.
   * Formula:
     ```powerquery
     let
         Today = DateTime.Date(DateTime.LocalNow()),
         SnapshotDate = Date.EndOfMonth(Date.AddMonths(Today, - [MonthOffset]))
     in
         Date.Year(SnapshotDate) * 10000 + Date.Month(SnapshotDate) * 100 + Date.Day(SnapshotDate)
     ```
   * Set type to **Whole Number (`123`)**.
   * Replace the original `SnapshotDateKey` by removing it and renaming `DynamicDateKey` to `SnapshotDateKey`.
6. **Adjust Historical Tenure Dynamically**:
   * Go to **Add Column > Custom Column**. Name: `AdjustedTenureMonths`.
   * Formula:
     ```powerquery
     [TenureMonths] - [MonthOffset]
     ```
   * Set type to **Whole Number (`123`)**, remove old `TenureMonths`, and rename to `TenureMonths`.
   * Go to **Add Column > Custom Column**. Name: `AdjustedTenureYears`.
   * Formula:
     ```powerquery
     Number.Round([TenureMonths] / 12, 2)
     ```
   * Set type to **Decimal Number (`1.2`)**, remove old `TenureYears`, and rename to `TenureYears`.
7. **Clean Up & Re-Index**:
   * Select the `MonthOffset` helper column $\to$ right-click $\to$ select **Remove**.
   * Remove the old `SnapshotKey` column $\to$ go to **Add Column > Index Column > From 1** $\to$ rename to `SnapshotKey` $\to$ drag to the far left.
8. Click **Home > Close & Apply**.
9. In Power BI Desktop **Model View**, drag `Fact_WorkforceSnapshot[EmployeeKey]` onto `Dim_Employee[EmployeeKey]`:
   * Power BI detects multiple records per employee in `Fact_WorkforceSnapshot` and exactly 1 record in `Dim_Employee`.
   * **Cardinality is automatically locked to `Many to one (*:1)`** and **Cross-filter direction is locked to `Single`**!
   * Future scheduled refreshes will dynamically roll forward every month with 100% automated reliability.

#### Production M Code: `Fact_WorkforceSnapshot`
```powerquery
let
    // 1. Ingest processed monthly workforce snapshot
    Source = Csv.Document(File.Contents(Text.BeforeDelimiter(Extension.Contents(""), "powerbi") & "data/processed/Fact_WorkforceSnapshot.csv"), [Delimiter=",", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    
    // 2. Set strict enterprise types
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"SnapshotKey", Int64.Type},
        {"SnapshotDateKey", Int64.Type},
        {"EmployeeKey", Int64.Type},
        {"DepartmentKey", Int64.Type},
        {"BranchKey", Int64.Type},
        {"BaseSalary", Currency.Type},
        {"AnnualPerformanceRating", type number},
        {"TenureMonths", Int64.Type},
        {"TenureYears", type number},
        {"SalaryPercentileInRole", type number},
        {"IsSalaryCompressed", Int64.Type},
        {"EmploymentStatus", type text}
    })
in
    #"Changed Type"
```

---

Click **Home > Close & Apply** in Power Query Editor to commit all 5 Conformed Dimensions and 4 Galaxy Fact Tables to the tabular model!

## 🛠️ Module 3: Advanced Semantic Model Engineering & TMDL Scripting Masterclass

In enterprise Power BI deployments (Fabric Git integration, PBIP developer mode), models are authored in **TMDL (Tabular Model Definition Language)**. This section provides exact production TMDL definitions for advanced model features.

---

### 3.1 TMDL: Calculation Groups (Time Intelligence)

Calculation groups eliminate the need to write dozens of redundant measures (e.g. `Headcount YTD`, `Payroll YTD`, `Violations YTD`). Instead, a single calculation group applies Time Intelligence dynamically to **any selected measure**.

Save this script as `powerbi/employess-report.SemanticModel/definition/tables/time_intelligence.tmdl`:

```tmdl
table 'Time Intelligence'
	lineageTag: 7a8b9c0d-1111-2222-3333-444455556666

	calculationGroup
		precedence: 1

		calculationItem 'Current' = SELECTEDMEASURE()

		calculationItem 'YTD' =
			CALCULATE(
				SELECTEDMEASURE(),
				DATESYTD('Dim_Date'[FullDate])
			)

		calculationItem 'QTD' =
			CALCULATE(
				SELECTEDMEASURE(),
				DATESQTD('Dim_Date'[FullDate])
			)

		calculationItem 'Prior Month (MoM)' =
			CALCULATE(
				SELECTEDMEASURE(),
				DATEADD('Dim_Date'[FullDate], -1, MONTH)
			)

		calculationItem 'Prior Year (YoY)' =
			CALCULATE(
				SELECTEDMEASURE(),
				DATEADD('Dim_Date'[FullDate], -1, YEAR)
			)

		calculationItem 'YoY %' =
			VAR CurrentVal = SELECTEDMEASURE()
			VAR PriorYearVal =
				CALCULATE(
					SELECTEDMEASURE(),
					DATEADD('Dim_Date'[FullDate], -1, YEAR)
				)
			RETURN
				DIVIDE(CurrentVal - PriorYearVal, PriorYearVal, BLANK())
			formatStringDefinition = "0.0%"

		calculationItem '3M Moving Average' =
			CALCULATE(
				AVERAGEX(
					DATESINPERIOD('Dim_Date'[FullDate], MAX('Dim_Date'[FullDate]), -3, MONTH),
					SELECTEDMEASURE()
				)
			)

	column 'Calculation' = Name
		dataType: string
		lineageTag: 7a8b9c0d-1111-2222-3333-777788889999
		summarizeBy: none
		sourceColumn: Name
		sortByColumn: Ordinal

	column Ordinal
		dataType: int64
		isHidden
		lineageTag: 7a8b9c0d-1111-2222-3333-000011112222
		summarizeBy: none
		sourceColumn: Ordinal
```

---

### 3.2 TMDL: Field Parameters (Dynamic Visual Slicing)

Field parameters allow users to dynamically change the breakdown axis of any visual between **Department**, **Branch**, **Contract Type**, and **Job Role** using a single button slicer.

Save as `powerbi/employess-report.SemanticModel/definition/tables/parameter_dimension.tmdl`:

```tmdl
table 'Dynamic Dimension Slicer'
	lineageTag: 8b9c0d1e-2222-3333-4444-555566667777

	column 'Dynamic Dimension' =
		SWITCH(
			[Value],
			0, NAMEOF('Dim_Department'[DepartmentName]),
			1, NAMEOF('Dim_Branch'[BranchName]),
			2, NAMEOF('Dim_Employee'[ContractType]),
			3, NAMEOF('Dim_Employee'[JobRole])
		)
		dataType: string
		lineageTag: 8b9c0d1e-2222-3333-4444-888899990000
		summarizeBy: none
		sortByColumn: 'Ordinal'

		extendedProperty ParameterMetadata =
			{
			  "version": 3,
			  "kind": 2,
			  "parameter": {
			    "fields": [
			      "Dim_Department[DepartmentName]",
			      "Dim_Branch[BranchName]",
			      "Dim_Employee[ContractType]",
			      "Dim_Employee[JobRole]"
			    ]
			  }
			}

	column Ordinal
		dataType: int64
		isHidden
		lineageTag: 8b9c0d1e-2222-3333-4444-111122223333
		summarizeBy: none

	column Value
		dataType: int64
		isHidden
		lineageTag: 8b9c0d1e-2222-3333-4444-444455556666
		summarizeBy: none
```

---

### 3.3 TMDL: Row-Level Security (RLS) & Object-Level Security (OLS)

Enterprise human capital data demands strict governance:
* **Branch Managers** must only see their branch's workforce.
* **Non-HR Managers** must have base salary figures masked (**Object-Level Security**).

Add to `powerbi/employess-report.SemanticModel/definition/model.tmdl`:

```tmdl
role 'Branch Regional Manager'
	modelPermission: read

	tablePermission 'Dim_Branch' =
		'Dim_Branch'[BranchName] =
			LOOKUPVALUE(
				'SecurityMapping'[AuthorizedBranch],
				'SecurityMapping'[UserEmail],
				USERPRINCIPALNAME()
			)

role 'Restricted HR Viewer'
	modelPermission: read

	// Object-Level Security (OLS): Hides the BaseSalary column completely
	tablePermission 'Dim_Employee'
		columnPermission 'BaseSalary' = none

	tablePermission 'Fact_WorkforceSnapshot'
		columnPermission 'BaseSalary' = none
```

---

### 3.4 TMDL: Incremental Refresh Policy (VertiPaq Engine)

`Fact_DailyAttendance` accumulates millions of daily IoT rows. Instead of reloading the full history every night, configure **Incremental Refresh**:

```tmdl
table Fact_DailyAttendance
	refreshPolicy
		policyType: basic
		rollingWindow:
			granularity: month
			periods: 24
		incrementalWindow:
			granularity: day
			periods: 7
		sourceData:
			variable: RangeStart
			variable: RangeEnd
```

---

### 3.5 VertiPaq Engine Optimization Secrets

To ensure sub-second dashboard rendering over millions of records:

1. **Eliminate the Auto Date/Time Disaster**:
   * Power BI's default behavior creates hidden auto-date tables for every single date column in your dataset, swelling RAM usage by up to $80\%$.
   * **Verification**: Ensure `annotation __PBI_TimeIntelligenceEnabled = 0` is set in `model.tmdl`.
2. **Cardinality Reduction (Split Date & Time)**:
   * A `DateTime` column with timestamps down to the second has over $31,536,000$ unique values per year, defeating VertiPaq compression.
   * **Best Practice**: Always split into `Date` ($365$ unique values) and `Time` ($1,440$ unique values if minute-grain). Memory footprint drops by over $98\%$.
3. **Surrogate Keys vs Natural Keys**:
   * Hide all integer surrogate keys (`EmployeeKey`, `DepartmentKey`, `BranchKey`) by setting `isHidden: true` in TMDL. VertiPaq optimizes dictionary encoding when columns are not exposed to the visual layer.
4. **Sort By Column Enforcement**:
   * Always set `sortByColumn: MonthNumberOfYear` on `MonthName` to prevent embarrassing alphabetical sorting (e.g. April, August, December).

---

## ⚡ Module 4: Advanced DAX Diagnostics & Analytical Problem Solving

### Problem 1: Salary Compression & Flight Risk Dynamics

```dax
// 1. Benchmark: Role New-Hire Median (< 1 Year Tenure)
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

// 2. Wage Inversion Ratio (Current Salary vs Role Benchmark)
Wage Inversion Ratio = 
VAR CurrentSalary = SELECTEDVALUE('Fact_WorkforceSnapshot'[BaseSalary])
VAR Benchmark = [Role Median New Hire Salary]
RETURN
    IF(
        NOT(ISBLANK(CurrentSalary)) && Benchmark > 0,
        DIVIDE(CurrentSalary, Benchmark, BLANK()),
        BLANK()
    )

// 3. Flight Risk Severity Index (1-100 Score)
Flight Risk Severity Score = 
VAR CurrentSalary = SELECTEDVALUE('Fact_WorkforceSnapshot'[BaseSalary])
VAR Benchmark = [Role Median New Hire Salary]
VAR PerfRating = SELECTEDVALUE('Fact_WorkforceSnapshot'[AnnualPerformanceRating], 3.0)
VAR Tenure = SELECTEDVALUE('Fact_WorkforceSnapshot'[TenureYears], 1.0)
VAR InversionRatio = DIVIDE(CurrentSalary, Benchmark, 1.0)
RETURN
    IF(
        InversionRatio < 1.0 && Tenure >= 3.0,
        // High performer with compressed compensation = Critical retention threat
        MIN(100, ROUND((PerfRating / 5.0) * 50 + ((1.0 - InversionRatio) * 100) * 0.35 + (Tenure * 3), 0)),
        // Normal baseline
        ROUND((PerfRating / 5.0) * 30 + (1.0 - MIN(1.0, InversionRatio)) * 20, 0)
    )

// 4. Retained Payroll Value at Critical Flight Risk (EGP)
Payroll at Critical Flight Risk EGP = 
CALCULATE(
    SUM('Fact_WorkforceSnapshot'[BaseSalary]),
    FILTER(
        'Fact_WorkforceSnapshot',
        [Flight Risk Severity Score] >= 80
    )
)
```

---

### Problem 2: Fact-to-Fact Bi-Temporal Headcount & Budget Burn Variance

```dax
// 1. Actual Active Headcount
Actual Headcount = 
DISTINCTCOUNT('Fact_WorkforceSnapshot'[EmployeeKey])

// 2. Budgeted Headcount Target
Budgeted Target Headcount = 
SUM('Fact_DepartmentBudget'[BudgetedHeadcount])

// 3. Headcount Variance (Actual vs Target)
Headcount Variance = 
[Actual Headcount] - [Budgeted Target Headcount]

// 4. Actual Monthly Payroll Run Rate (EGP)
Actual Monthly Payroll EGP = 
SUM('Fact_WorkforceSnapshot'[BaseSalary])

// 5. Allocated Monthly Budget (Quarterly Budget / 3)
Allocated Monthly Salary Budget EGP = 
DIVIDE(SUM('Fact_DepartmentBudget'[AllocatedSalaryBudget_EGP]), 3, 0)

// 6. Payroll Burn Rate %
Payroll Burn Rate Pct = 
DIVIDE([Actual Monthly Payroll EGP], [Allocated Monthly Salary Budget EGP], BLANK())
```

---

### Problem 3: Workplace Policy Compliance & Ghost Worker Audits

```dax
// 1. Physical Presence Compliance Rate %
Physical Presence Compliance Rate = 
VAR TotalAccess = COUNTROWS('Fact_DailyAttendance')
VAR OnsiteAccess = 
    CALCULATE(
        COUNTROWS('Fact_DailyAttendance'),
        'Fact_DailyAttendance'[ActualWorkMode] = "On-site"
    )
RETURN
    DIVIDE(OnsiteAccess, TotalAccess, 0)

// 2. Contract Violation Incidents
Contract Violation Breach Count = 
CALCULATE(
    COUNTROWS('Fact_DailyAttendance'),
    'Fact_DailyAttendance'[IsContractViolation] = 1
)

// 3. Ghost Worker Diagnostic Count (Zero Access in >60 Days)
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

// 4. Annualized Payroll Leakage from Ghost Workers (EGP)
Ghost Worker Annualized Payroll Leakage EGP = 
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

### Problem 4: Upskilling Velocity & Training ROI ($\Delta P$)

```dax
// 1. Total Certification Investment (EGP)
Total Training Investment EGP = 
SUM('Fact_TrainingCompletions'[CertificationCost_EGP])

// 2. Certified Employee Count
Certified Employee Count = 
CALCULATE(
    DISTINCTCOUNT('Fact_TrainingCompletions'[EmployeeKey]),
    'Fact_TrainingCompletions'[IsPassed] = 1
)

// 3. Average Certified Performance Rating
Avg Certified Performance Rating = 
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

// 4. Baseline Non-Certified Performance Rating
Avg NonCertified Performance Rating = 
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

// 5. Performance Velocity Delta (Spread)
Performance Velocity Delta = 
[Avg Certified Performance Rating] - [Avg NonCertified Performance Rating]

// 6. Cost Per Performance Rating Point Gained (EGP)
Training Cost Per Rating Point Gain EGP = 
VAR Spread = [Performance Velocity Delta]
VAR TotalCost = [Total Training Investment EGP]
RETURN
    IF(Spread > 0, DIVIDE(TotalCost, Spread * [Certified Employee Count], BLANK()), BLANK())
```

---

### Problem 5: Survivorship Bias & Regrettable Attrition Dynamics

```dax
// 1. Total Exits in Period
Total Separations = 
DISTINCTCOUNT('Exit_Attrition_Records'[EmployeeID])

// 2. Regrettable Loss (High Performer Voluntary Exits)
Regrettable Turnover Count = 
CALCULATE(
    DISTINCTCOUNT('Exit_Attrition_Records'[EmployeeID]),
    'Exit_Attrition_Records'[ExitType] = "Voluntary",
    'Exit_Attrition_Records'[LastPerformanceScore] >= 4.0
)

// 3. Regrettable Loss % of Total Exits
Regrettable Turnover Rate Pct = 
DIVIDE([Regrettable Turnover Count], [Total Separations], 0)

// 4. Average Resignation Notice Lead-Time (Days)
Avg Resignation Notice Days = 
AVERAGEX(
    'Exit_Attrition_Records',
    DATEDIFF('Exit_Attrition_Records'[NoticeDate], 'Exit_Attrition_Records'[ExitDate], DAY)
)
```

---

### Problem 6: Demographic Pay Equity Drift

```dax
// 1. Male Average Salary in Role
Male Avg Salary in Role = 
CALCULATE(
    AVERAGE('Fact_WorkforceSnapshot'[BaseSalary]),
    RELATED('Dim_Employee'[Gender]) = "ذكر"
)

// 2. Female Average Salary in Role
Female Avg Salary in Role = 
CALCULATE(
    AVERAGE('Fact_WorkforceSnapshot'[BaseSalary]),
    RELATED('Dim_Employee'[Gender]) = "أنثى"
)

// 3. Gender Pay Ratio % (100% = Perfect Parity)
Gender Pay Parity Ratio = 
DIVIDE([Female Avg Salary in Role], [Male Avg Salary in Role], BLANK())
```

---

### Problem 7: Branch Space Utilization & Peak Occupancy Stress

```dax
// 1. Peak Daily Check-Ins in Selected Period
Peak Daily Attendance Count = 
MAXX(
    VALUES('Dim_Date'[FullDate]),
    CALCULATE(COUNTROWS('Fact_DailyAttendance'), 'Fact_DailyAttendance'[ActualWorkMode] = "On-site")
)

// 2. Branch Physical Desk Capacity
Branch Physical Capacity = 
SELECTEDVALUE('Dim_Branch'[Capacity], 250)

// 3. Peak Occupancy Stress Ratio % (> 100% means overcrowding)
Peak Occupancy Stress Ratio = 
DIVIDE([Peak Daily Attendance Count], [Branch Physical Capacity], BLANK())
```

---

## 🎨 Module 5: Modern Web App-Style UI/UX Design System (Report View GUI)

Following top Power BI report designers (Bas / *How to Power BI*, Guy in a Cube, Enterprise DNA), we construct a **SaaS Web App Experience**.

Switch to **Report View** in Power BI Desktop (top icon on the left bar).

---

### Step 5.1: Canvas & Visual Grid Setup via GUI
1. In the right pane, click the **Format report page icon (paintbrush)**.
2. Expand **Canvas settings**: Set *Type* to **Custom**, *Width* to **1920 px**, *Height* to **1080 px** (16:9 Full HD).
3. Expand **Canvas background**: Color: **`#0B0F19`** (Deep Charcoal Slate), Transparency: **0%**.

---

### Step 5.2: Building the Persistent Left App Navigation Sidebar via GUI
1. Go to **Insert > Shapes > Rectangle**.
   * Size & Position: Width: `200 px`, Height: `1080 px`, X: `0 px`, Y: `0 px`.
   * Fill: `#0F172A` (Elevated Nav Surface), Border: **Off**.
2. **App Branding**:
   * Insert Text Box at top-left: Font *Segoe UI Semibold*, Size *14pt*, Color `#60A5FA`. Text: `HR CAPITAL OPS`.
3. **Adding Nav Buttons with Hover & Selection States**:
   * Go to **Insert > Buttons > Blank**.
   * Width: `180 px`, Height: `44 px`.
   * Button States:
     * *Default*: Text: `📊 Executive Cockpit`, Font color: `#94A3B8`, Fill: `#0F172A`.
     * *On hover*: Fill: `#1E293B`, Font color: `#FFFFFF`.
     * *On press*: Fill: `#2563EB`, Font color: `#FFFFFF`.
   * In Format pane > **Action**, set *Type* to **Page navigation** and select destination.

---

### Step 5.3: Building KPI Hero Cards via the New Card Visual GUI
1. Go to **Visualizations pane > Card (new)**.
2. Drag metrics: `[Actual Headcount]`, `[Actual Monthly Payroll EGP]`, `[Contract Violation Breach Count]`, `[Payroll at Critical Flight Risk EGP]`.
3. Format visual pane:
   * **Shape**: Rounded rectangle, radius: `10 px`.
   * **Callout values**: Font *Segoe UI Bold*, Size `28pt`, Color `#F8FAFC`.
   * **Accent bar**: Toggle **On**, Position **Left**, Width **5 px**.
     * Blue (`#3B82F6`) for Headcount, Green (`#10B981`) for Payroll, Amber (`#F59E0B`) for Violations, Crimson (`#EF4444`) for Flight Risk.
   * **Background**: Fill `#1E293B`, Transparency `10%`. Border: `#334155`.
   * **Shadow**: Outside bottom-right.

---

### Step 5.4: Building the Wage Inversion Scatter Plot via GUI
1. Click **Visualizations pane > Scatter chart**.
2. Field wells:
   * **Values**: `Dim_Employee[FullName]`
   * **X Axis**: `Fact_WorkforceSnapshot[TenureYears]` (*Don't summarize*)
   * **Y Axis**: `Fact_WorkforceSnapshot[SalaryPercentileInRole]`
   * **Legend**: `Dim_Employee[JobRole]`
   * **Size**: `Fact_WorkforceSnapshot[BaseSalary]`
   * **Tooltips**: `Fact_WorkforceSnapshot[BaseSalary]`, `[Role Median New Hire Salary]`, `[Flight Risk Severity Score]`
3. Go to **Format visual pane > Reference lines**:
   * Constant line (X Axis): Value `3.0` (Tenure threshold), Style: `Dashed`, Color: `#EF4444`. Name: `Tenure > 3 Years`.
   * Constant line (Y Axis): Value `0.50` (50th Percentile), Style: `Dashed`, Color: `#F59E0B`. Name: `Role Median`.
4. **Interpretation**: Any employee in the **Bottom-Right Quadrant** ($X \ge 3.0$ and $Y < 0.50$) represents an active retention crisis.

---

### Step 5.5: Creating the 360° Employee Diagnostic Dossier Drill-Through Page
1. Click **`+`** at the bottom to create a page named `Employee_Dossier`.
2. Format report page $\to$ **Page information**: Set *Page type* to **Drill-through**.
3. In the **Drill-through fields** well, drag `Dim_Employee[EmployeeID]`.
4. Visuals on this page:
   * **Bio Card**: `FullName`, `JobRole`, `Department`, `Branch`, `HireDate`, `ContractType`.
   * **Compensation Audit**: `BaseSalary`, `Role Median New Hire Salary`, `Salary Percentile In Role`, `Flight Risk Severity Score`.
   * **30-Day IoT Access Timeline**: Bar chart of daily `DurationHours` colored by `ActualWorkMode`.
   * **LMS Credentials**: Table of `CourseName`, `SkillDomain`, `Score`, and `CertificationCost_EGP`.

---

## 🔬 Module 6: Modern Power BI Features (DAX Query View & Visual Calculations)

### 6.1 DAX Query View: Diagnosing Models Without Creating Visuals
In Power BI Desktop, click the **DAX Query View** icon on the left bar:

```dax
// Execute in DAX Query View to inspect salary compression without adding visuals
EVALUATE
TOPN(
    15,
    FILTER(
        ADDCOLUMNS(
            VALUES('Dim_Employee'[EmployeeID]),
            "FullName", RELATED('Dim_Employee'[FullName]),
            "JobRole", RELATED('Dim_Employee'[JobRole]),
            "BaseSalary", CALCULATE(SUM('Fact_WorkforceSnapshot'[BaseSalary])),
            "NewHireMedian", [Role Median New Hire Salary],
            "FlightRiskScore", [Flight Risk Severity Score]
        ),
        [FlightRiskScore] >= 80
    ),
    [FlightRiskScore],
    DESC
)
```

### 6.2 Visual Calculations (Visual-Level DAX)
Power BI allows calculations defined directly within a visual matrix (e.g. running totals, moving averages) without adding measures to the semantic model:

* Click any visual $\to$ in the ribbon, click **New visual calculation**.
* Expression for Running Payroll Total:
  `RunningPayroll = RUNNINGSUM([Actual Monthly Payroll EGP])`
* Expression for Moving Average:
  `MovingAttendanceAvg = MOVINGAVERAGE([Physical Presence Compliance Rate], 3)`

---

## 🚀 Module 7: Enterprise Best Practices, Tips & Tricks (Kimball, DAX & VertiPaq)

### 7.1 Kimball Dimensional Modeling Rules for Enterprise HR

1. **Enforce Single-Direction (1-to-Many) Relationships Exclusively**:
   * *The Problem*: Bi-directional cross-filtering introduces ambiguity into relationship topology, inflates memory footprints, and forces the VertiPaq engine into costly table-scan evaluation loops.
   * *The Rule*: Always keep relationship cross-filter direction set to **Single**. When filtering across facts (e.g., filtering `Fact_DailyAttendance` based on an attribute in `Fact_WorkforceSnapshot`), use conformed dimensions (`Dim_Employee`, `Dim_Date`) as the shared bridge.
2. **Semi-Additive Snapshots vs Discrete Events**:
   * *The Problem*: Headcount cannot simply be summed (`SUM(Headcount)`) across time — summing headcount across 12 months produces 12x the actual workforce.
   * *The Rule*: Model snapshot facts with temporal boundary filters in DAX. Use `CALCULATE([Metric], LASTDATE(Dim_Date[FullDate]))` or point-in-time evaluation:
     ```dax
     Headcount End of Period = 
     CALCULATE(
         COUNTROWS('Dim_Employee'),
         'Dim_Employee'[HireDate] <= MAX('Dim_Date'[FullDate]),
         ISBLANK('Dim_Employee'[TerminationDate]) || 'Dim_Employee'[TerminationDate] > MAX('Dim_Date'[FullDate])
     )
     ```
3. **Surrogate Keys vs Natural Keys**:
   * Always hide surrogate integer keys (`EmployeeKey`, `DateKey`, `BranchKey`) in the Report View. End users and report builders should only see natural codes (`EmployeeID`, `BranchCode`) and user-facing attributes (`FullName`, `BranchName`).

---

### 7.2 DAX Performance Tuning & Query Optimization

| Pattern | Anti-Pattern (Slow / Risky) | Best Practice (Fast / Optimized) | Rationale |
| :--- | :--- | :--- | :--- |
| **Row Count** | `COUNT('Dim_Employee'[EmployeeID])` | `COUNTROWS('Dim_Employee')` | Scans table metadata rather than reading individual column dictionary pages. |
| **Safe Division** | `[A] / [B]` or `IF([B]=0, 0, [A]/[B])` | `DIVIDE([A], [B], 0)` | Built-in C++ level divide that avoids branching and prevents division-by-zero crashes. |
| **Variable Scoping** | Repeating `[Total Salary] / CALCULATE([Total Salary], ALL(...))` | `VAR _Total = [Total Salary] RETURN ...` | `VAR` evaluates once into an immutable scalar constant, preventing redundant formula engine re-calculations. |
| **Filtering Tables** | `FILTER('Fact_WorkforceSnapshot', [BaseSalary] > 50000)` | `FILTER(VALUES('Fact_WorkforceSnapshot'[BaseSalary]), 'Fact_WorkforceSnapshot'[BaseSalary] > 50000)` | Filtering a single column reduces the filter context cardinality from millions of rows to distinct values. |
| **Context Transition** | Calling raw columns inside iterators without awareness | Wrap with explicit measures or understand `CALCULATE` context transition | Calling `CALCULATE` inside an iterator converts current row context into equivalent filter context, which can trigger costly query loops if unmonitored. |

---

### 7.3 VertiPaq In-Memory Storage Engine Optimization

1. **Split High-Cardinality DateTime Columns**:
   * An 8-byte DateTime column with timestamp precision down to the second has up to $86,400$ unique values per day, causing poor VertiPaq dictionary compression.
   * *Action*: Split `CheckInTime` and `CheckOutTime` into a separate `Date` column (`AccessDate`) and a rounded `Time` column (or 15-minute time bucket integer).
2. **Eliminate Default Auto Date/Time**:
   * *Action*: Go to **File > Options and settings > Options > Current File > Data Load**, and **uncheck "Auto Date/Time"**. Auto Date/Time creates hidden internal hierarchy tables for every date column, massively bloating `.pbix` file size.
3. **Configure Sort By Column**:
   * For non-alphabetical sorting (e.g., `MonthName` "January", "February"), set **Sort by Column** to `MonthNumberOfYear`. Ensure the sort-by column has a strict $1:1$ relationship with the attribute to prevent circular dependency errors.

---

## 🏆 Final Summary Checklist: Enterprise Analytics Delivery

- [x] **Diagnose Operational Friction**: Formulate hypotheses on Wage Inversion, Grain Collisions, Ghost Workers, and Attrition Survivorship before modeling.
- [x] **Power Query Editor GUI**: Use visual clickpaths to ingest raw CSVs, extract conformed dimensions via Reference queries, impute clock-outs, and unpivot wide FP&A budgets.
- [x] **Production M Script for `Dim_Date`**: Deploy the full enterprise calendar with Egyptian workweek rules and relative offsets.
- [x] **Semantic Model Engineering (TMDL)**: Implement Calculation Groups, Field Parameters, RLS/OLS, and Incremental Refresh policies.
- [x] **VertiPaq Memory Optimization**: Eliminate Auto Date/Time, split DateTime into Date and Time, hide surrogate keys, and enforce column sorting.
- [x] **Advanced DAX Formulas**: Deploy 7 analytical diagnostic solutions covering salary compression, ghost workers, upskilling ROI, and branch space stress.
- [x] **Kimball & Enterprise Best Practices**: Single-direction filter relationships, semi-additive snapshots, metadata row counts, and VertiPaq column splitting.
- [x] **Web App UX Design**: Build a 1920x1080 canvas with a persistent sidebar, New Card visuals, wage inversion quadrant scatter plots, and 360° employee dossiers.

