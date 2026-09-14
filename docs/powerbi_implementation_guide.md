# 💎 Nexora Tech Solutions · Enterprise Power BI Implementation & Analytical Diagnostics Masterclass
### Building a Kimball Galaxy Schema (Fact Constellation) from Raw Data with Full GUI, TMDL & DAX Guidance
**Domain**: Offshore Software House Consulting, International Client Delivery & L&D Tech Academy

---

## 🎯 Executive Overview & The Modern Enterprise Paradigm

In enterprise human capital and software house operations, data engineering is rarely clean. The operational reality of **Nexora Tech Solutions (حلول نكسورا للبرمجيات والتحول الرقمي)** spans **7 heterogeneous source systems** operating at disparate frequencies and grains across engineering talent, IoT hardware, academy certifications, and offshore client contracts:

```
                               ┌──────────────────────────────────────────────┐
                               │           RAW SOURCE LANDING ZONE            │
                               ├──────────────────────────────────────────────┤
                               │ • Raw Core HR Master (7,000 Arabic rows)     │
                               │ • Daily IoT Badge Access Logs (JSON streams) │
                               │ • Relational Exit Audits (SQL Server OLTP)   │
                               │ • FP&A Budget Worksheets (Messy Wide Excel)  │
                               │ • LMS Platform Course Records (REST / CSV)   │
                               │ • Client Projects & Tasks (JSON / CSV, 3.6k) │
                               │ • Central Bank FX Spot Rates (CSV Feed)      │
                               └──────────────────────┬───────────────────────┘
                                                      │ Power Query Editor GUI
                                                      ▼
                               ┌──────────────────────────────────────────────┐
                               │     KIMBALL GALAXY SCHEMA (CONSTELLATION)    │
                               ├──────────────────────────────────────────────┤
                               │ Conformed Dimensions:                        │
                               │   Dim_Employee (SCD-2) │ Dim_Department      │
                               │   Dim_Branch           │ Dim_Date (Calendar) │
                               │   Dim_Course (L&D)     │ Dim_CurrencyRates   │
                               │                                              │
                               │ Fact Tables:                                 │
                               │   Fact_WorkforceSnapshot (Monthly)           │
                               │   Fact_DailyAttendance   (Daily IoT)         │
                               │   Fact_DepartmentBudget  (Quarterly FP&A)    │
                               │   Fact_TrainingCompletions (Transactional)   │
                               │   Fact_ProjectTasks      (Client Delivery)   │
                               └──────────────────────┬───────────────────────┘
                                                      │ TMDL & Semantic Modeling
                                                      ▼
                               ┌──────────────────────────────────────────────┐
                               │     ENTERPRISE SEMANTIC MODEL & TMDL LAYER   │
                               ├──────────────────────────────────────────────┤
                               │ • Calculation Groups (Time Intelligence)     │
                               │ • Field Parameters (Dynamic Visual Slicing)  │
                               │ • In-Memory Table.Buffer() Dimension Caching │
                               │ • Dynamic Multi-Currency Normalization (FX)  │
                               │ • Incremental Refresh Policy (VertiPaq)      │
                               └──────────────────────┬───────────────────────┘
                                                      │ DAX Diagnostic Engine
                                                      ▼
                               ┌──────────────────────────────────────────────┐
                               │       8 ADVANCED ANALYTICAL DIAGNOSTICS      │
                               ├──────────────────────────────────────────────┤
                               │ 1. Salary Compression & Flight Risk Index    │
                               │ 2. Bi-Temporal Budget & Headcount Variance   │
                               │ 3. Policy Compliance & Ghost Worker Audits   │
                               │ 4. Upskilling Velocity & Training ROI (ΔP)   │
                               │ 5. Client Task Delivery & Bench Cost Bleed   │
                               │ 6. Global Multi-Currency FX Realization      │
                               │ 7. Survivorship Bias & Regrettable Turnover  │
                               │ 8. Branch Space Utilization & Peak Stress    │
                               └──────────────────────┬───────────────────────┘
                                                      │ Report View GUI (1920x1080)
                                                      ▼
                               ┌──────────────────────────────────────────────┐
                               │          WEB APP STYLE DASHBOARD UI/UX       │
                               │ Persistent Sidebar │ Hero Cards │ 360° Dossier│
                               └──────────────────────────────────────────────┘
```

This guide equips you with:
1. **Critical Analytical Thinking Frameworks** to formulate hypotheses on organizational behavior, wage friction, bench utilization, and operational leakage.
2. **Visual, Step-by-Step Power Query GUI Clickpaths** to transform messy raw data into a pristine **Kimball Galaxy Schema** without writing manual M code for data tables.
3. **Production M Code Exclusively for `Dim_Date`** providing a dynamically harvested enterprise calendar with Egyptian weekend rules and relative offsets.
4. **Advanced Semantic Model Engineering & TMDL Scripting** covering Calculation Groups, Field Parameters, Dynamic Format Strings, and VertiPaq memory optimization.
5. **Advanced DAX Formulas for 8 Complex Business Problems** with full filter context explanations.
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
11. **Looking up Surrogate Foreign Key (`EmployeeKey`) via GUI Merge Queries (⭐ Kimball Standard)**:
    > [!IMPORTANT]
    > **Why `EmployeeKey` is Not in the Raw Attendance File**:
    > `Fact_DailyAttendance` arrives from IoT badge readers with the natural text identifier **`EmployeeID`** (e.g. `EMP-10001` through `EMP-17000`), whereas `Dim_Employee` has both the natural identifier **`الرقم التعريفي`** and the integer surrogate primary key **`EmployeeKey`**. To connect them on `EmployeeKey` in Power BI Model View, look up `EmployeeKey` in Power Query via this 4-click GUI merge:
    >
    > 1. In the **Home** ribbon, click **Merge Queries > Merge Queries**.
    > 2. In the top table (`Fact_DailyAttendance`), click the column header **`EmployeeID`**.
    > 3. In the lower dropdown, select **`Dim_Employee`** $\to$ click the column header **`الرقم التعريفي`** (Arabic employee code).
    > 4. Join Kind: **Left Outer (all from first, matching from second)** $\to$ notice the green checkmark: *"The selection matches all rows"* $\to$ click **OK**.
    > 5. A new column named `Dim_Employee` with `[Table]` links appears on the far right. Click the **Expand icon (`↔`)** at the top right of the column header:
    >    * **Uncheck** *(Select All Columns)*.
    >    * **Check ONLY** **`EmployeeKey`**.
    >    * **Uncheck** *Use original column name as prefix*.
    >    * Click **OK**.
    > 6. Click the data type icon in the new `EmployeeKey` column header $\to$ choose **Whole Number (`123`)**.
    > 7. *(Optional)*: Drag `EmployeeKey` to the left next to `AttendanceKey` or `EmployeeID`.

12. **(Optional) Looking up / Deriving `BranchKey` via GUI**:
    * If connecting `Fact_DailyAttendance` directly to `Dim_Branch` on physical access location:
      * **Method A (Arithmetic from `BuildingID`)**: Go to **Add Column > Custom Column** $\to$ Name: `BranchKey` $\to$ Expression: `if Text.StartsWith([BuildingID], "BLD-") then Value.FromText(Text.End([BuildingID], 3)) else null` $\to$ set type to **Whole Number (`123`)**. *(Maps `BLD-001` through `BLD-014` to integer branch keys 1 through 14)*.
      * **Method B (Employee Assigned Home Branch)**: In the Step 11 Merge with `Dim_Employee`, check both **`EmployeeKey`** and **`الفرع`** $\to$ then merge with `Dim_Branch` on `الفرع = BranchName` to expand `BranchKey`.

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
8. **Looking up Surrogate Foreign Key (`EmployeeKey`) via GUI Merge Queries**:
   * In the **Home** ribbon, click **Merge Queries > Merge Queries**.
   * Top table (`Fact_Badge_Access_Logs_SQL` / `Fact_DailyAttendance`): click header **`EmployeeID`**.
   * Lower table dropdown: select **`Dim_Employee`** $\to$ click header **`الرقم التعريفي`**.
   * Join Kind: **Left Outer** $\to$ click **OK**.
   * In the new `Dim_Employee` column, click the **Expand icon (`↔`)**:
     * Check ONLY **`EmployeeKey`**.
     * Uncheck *Use original column name as prefix*.
     * Click **OK**.
   * Set the data type of `EmployeeKey` to **Whole Number (`123`)**.

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

### Step 2.5: Ingesting LMS Training Records (`Fact_TrainingCompletions`) via GUI (CSV Path)

> [!IMPORTANT]
> **Data Consistency Note — Grounding on Master Employees**:
> All LMS records are strictly grounded on the master 7,000 workforce (`EMP-10001` through `EMP-17000` from `employees_data_7000.txt`).
> Depending on whether you are loading from flat CSV files or Microsoft SQL Server, choose **Step 2.5** (CSV) or **Step 2.5b** (SQL Server). Both follow identical dimensional modeling principles.

1. Go to **Home > New Source > Text/CSV** $\to$ select `data/raw/lms_certifications.csv` (7,197 records) or `data/raw/lms_course_completions.csv` $\to$ click **OK**.
2. Rename query in the left pane to **`Fact_TrainingCompletions`**.
3. **Setting Correct Column Types Visually**:
   * Click icon in header `EmployeeID` $\to$ set to **Text (`ABC`)**.
   * Click icon in header `CourseID` $\to$ set to **Text (`ABC`)**.
   * Click icon in header `CourseName` $\to$ set to **Text (`ABC`)**.
   * Click icon in header `SkillDomain` $\to$ set to **Text (`ABC`)**.
   * Click icon in header `CompletionDate` $\to$ set to **Date (`📅`)**.
   * Click icon in header `Score` $\to$ set to **Whole Number (`123`)** (or Decimal Number).
   * Click icon in header `Cost_EGP` (or `CertificationCost_EGP`) $\to$ set to **Fixed Decimal Number (`$`)**.

4. **Deriving Exam Pass Flag (`IsPassed`) via GUI**:
   * Go to **Add Column > Conditional Column**.
   * Column Name: `IsPassed`
   * Rule: If `Score` is greater than or equal to `70` (or `Status` equals `Completed`) then `1`, Else `0`.
   * Click **OK** $\to$ set type to **Whole Number (`123`)**.

5. **Deriving Performance Score Tier (`ScoreTier`) via GUI**:
   * Go to **Add Column > Conditional Column**.
   * Column Name: `ScoreTier`
   * Rules:
     * If `Score` is greater than or equal to `90` then `⭐ Distinction (90-100)`
     * Else If `Score` is greater than or equal to `70` then `🟢 Proficient Pass (70-89)`
     * Else `🔴 Remediation Required (< 70)`
   * Click **OK** $\to$ set type to **Text (`ABC`)**.

6. **Generating Smart Calendar Date Key (`CompletionDateKey`)**:
   * Go to **Add Column > Custom Column**.
   * Column Name: `CompletionDateKey`
   * Formula:
     ```powerquery
     Date.Year([CompletionDate]) * 10000 + Date.Month([CompletionDate]) * 100 + Date.Day([CompletionDate])
     ```
   * Click **OK** $\to$ set type to **Whole Number (`123`)**.

7. **Adding Surrogate Fact Primary Key (`CompletionKey`)**:
   * Go to **Add Column > Index Column > From 1**.
   * Rename header to **`CompletionKey`** $\to$ set type to **Whole Number (`123`)**.

---

### Step 2.5b: Enterprise SQL Server Ingestion — Importing `raw.LMS_Certifications` via GUI

In enterprise deployments, training telemetry lands directly in Microsoft SQL Server data warehouse under `[raw].[LMS_Certifications]`.

#### 1. Connecting to SQL Server:
1. In Power Query Editor, go to **Home > New Source > SQL Server**.
2. **Server**: `localhost` (or `.` or `localhost\SQLEXPRESS`). **Database**: `EnterpriseHR_DWH`. **Mode**: **Import** $\to$ click **OK**.
3. Authentication: **Windows > Use my current credentials** $\to$ click **Connect**.

#### 2. Selecting `raw.LMS_Certifications` in the Navigator:
1. Expand `EnterpriseHR_DWH` $\to$ expand the **`raw`** schema folder.
2. Check the checkbox next to **`LMS_Certifications`** (7,197 records).
3. Click **OK** (or **Transform Data**).

#### 3. Power Query Cleansing, Scoring & Keys via GUI:
1. In the **Queries** pane, rename `LMS_Certifications` to **`Fact_TrainingCompletions`**.
2. **Setting Data Types Visually**:
   * `EmployeeID`: **Text (`ABC`)**
   * `CourseID`: **Text (`ABC`)**
   * `CourseName`: **Text (`ABC`)**
   * `SkillDomain`: **Text (`ABC`)**
   * `CompletionDate`: **Date (`📅`)**
   * `Score`: **Whole Number (`123`)**
   * `Status`: **Text (`ABC`)**
   * `Cost_EGP`: **Fixed Decimal Number (`$`)**
3. **Deriving Boolean Pass Flag (`IsPassed`)**:
   * Go to **Add Column > Conditional Column** $\to$ Name: `IsPassed`.
   * Rule: If `Status` equals `Completed` then `1`, Else `0` $\to$ set type to **Whole Number (`123`)**.
4. **Deriving Performance Score Tier (`ScoreTier`)**:
   * Go to **Add Column > Conditional Column** $\to$ Name: `ScoreTier`.
   * If `Score` $\ge 90$ then `⭐ Distinction (90-100)`, Else If `Score` $\ge 70$ then `🟢 Proficient Pass (70-89)`, Else `🔴 Remediation Required (< 70)`.
5. **Generating Date Key (`CompletionDateKey`)**:
   * Go to **Add Column > Custom Column** $\to$ Name: `CompletionDateKey` $\to$ Formula:
     `Date.Year([CompletionDate]) * 10000 + Date.Month([CompletionDate]) * 100 + Date.Day([CompletionDate])` $\to$ set type to **Whole Number (`123`)**.
6. **Adding Primary Key (`CompletionKey`)**:
   * Go to **Add Column > Index Column > From 1** $\to$ Name: `CompletionKey` $\to$ set type to **Whole Number (`123`)**.

---

### Step 2.5c: Building & Enriching Conformed Dimension `Dim_Course` via GUI (Guaranteed 100% Match)

> [!CAUTION]
> **⚠️ Critical Gotcha — Why Power Query Showed "The selection matches 0 of 7197 rows"**:
> If you previously created `Dim_Course` by importing the separate CSV file `lms_course_completions.csv`, it contains course codes like `CRS-SOFT-01`, `CRS-LEAD-01`, and `CRS-TECH-01`.
> But your fact table `Fact_TrainingCompletions` was loaded from `raw.LMS_Certifications` (7,197 records), which uses canonical course codes `CRS-101`, `CRS-102`, `CRS-103`, `CRS-201`, `CRS-202`, `CRS-301`, `CRS-302`!
> 
> Because they came from two different source files with different naming schemes, **zero rows matched**! Furthermore, `Dim_Course` was mistakenly populated with transaction columns (`Score`, `CompletionKey`, `CompletionDateKey`, `IsPassed`) that violate star schema principles.
> 
> **The Golden Kimball Rule**: A conformed dimension must be extracted directly from your authoritative data source via **Query Reference**, guaranteeing that 100% of your course IDs match with zero discrepancies!

#### 1. Extracting the Clean Dimension via Reference in GUI:
1. In the left **Queries** pane, right-click **`Fact_TrainingCompletions`** $\to$ select **Reference**.
   *(If an old `Dim_Course` query already exists, right-click and delete it first, or edit its source to point to `Fact_TrainingCompletions`)*.
2. Right-click the newly created query in the left pane $\to$ **Rename** to **`Dim_Course`**.
3. **Removing Transactional Noise Columns**:
   * In the table preview, click the header **`CourseID`**.
   * Hold `Ctrl` on your keyboard and click **`CourseName`**, **`SkillDomain`**, and **`Cost_EGP`** (or `CertificationCost_EGP`).
   * Right-click any highlighted header $\to$ select **Remove Other Columns**.
   *(All completion-level noise like `EmployeeID`, `CompletionDate`, `Score`, `Status`, `IsPassed`, `CompletionKey`, `CompletionDateKey` is instantly purged!)*
4. **Deduplicating to the Unique Course Catalog**:
   * Click the column header **`CourseID`**.
   * Go to the **Home** ribbon tab $\to$ click **Remove Rows > Remove Duplicates**.
   *(The 7,197 rows instantly collapse down to the exact unique course catalog!)*
5. **Sorting Ascending**:
   * Click the dropdown arrow on header `CourseID` $\to$ select **Sort Ascending**.
6. **Adding Surrogate Primary Key (`CourseKey`)**:
   * Go to the **Add Column** ribbon tab $\to$ click **Index Column > From 1**.
   * Right-click the new `Index` header $\to$ select **Rename** $\to$ type `CourseKey`.
   * Drag `CourseKey` to the far left. Set its data type to **Whole Number (`123`)**.

#### 2. Enriching `Dim_Course` with Real-World Enterprise Attributes (GUI & M Options):
Based on your active 10-course enterprise catalog (`CRS-TECH-01..04`, `CRS-LEAD-01..02`, `CRS-SOFT-01..02`, `CRS-COMP-01..02`), enrich your dimension with strategic capability and governance attributes:

1. **Course Difficulty Level / Tier (`CourseLevel`)**:
   Categorizes the 10 programs into standard corporate learning tiers based on technical depth and strategic complexity:
   * **Level 1**: `CRS-COMP-01` (Labor Law 2026), `CRS-COMP-02` (GDPR/Information Governance), `CRS-SOFT-02` (Data Storytelling). *(Mandatory baseline compliance and organizational analytical literacy)*.
   * **Level 2**: `CRS-TECH-01` (Power BI & Enterprise DAX Modeling), `CRS-TECH-02` (Advanced SQL), `CRS-TECH-03` (Python Data Engineering), `CRS-SOFT-01` (Executive Negotiation). *(Role-specific technical mastery and commercial execution)*.
   * **Level 3**: `CRS-TECH-04` (Cloud Architecture & Cybersecurity), `CRS-LEAD-01` (Strategic People Leadership), `CRS-LEAD-02` (Lean Six Sigma / Operational Excellence). *(Enterprise system design and executive transformation)*.

   * **Method A (GUI Clickpath)**:
     * Go to **Add Column > Conditional Column** $\to$ Name: `CourseLevel`.
     * Configure rules:
       * If `CourseID` equals `CRS-COMP-01` then `Level 1`
       * Else If `CourseID` equals `CRS-COMP-02` then `Level 1`
       * Else If `CourseID` equals `CRS-SOFT-02` then `Level 1`
       * Else If `CourseID` equals `CRS-TECH-01` then `Level 2`
       * Else If `CourseID` equals `CRS-TECH-02` then `Level 2`
       * Else If `CourseID` equals `CRS-TECH-03` then `Level 2`
       * Else If `CourseID` equals `CRS-SOFT-01` then `Level 2`
       * Else `Level 3`
     * Click **OK** $\to$ set data type to **Text (`ABC`)**.

   * **Method B (M Formula via Add Column > Custom Column)**:
     ```powerquery
     if List.Contains({"CRS-COMP-01", "CRS-COMP-02", "CRS-SOFT-02"}, [CourseID]) then "Level 1"
     else if List.Contains({"CRS-TECH-01", "CRS-TECH-02", "CRS-TECH-03", "CRS-SOFT-01"}, [CourseID]) then "Level 2"
     else "Level 3"
     ```

2. **Strategic Capability Pillar (`StrategicPillar`)**:
   Aligns each course to corporate executive development pillars:
   * **GUI Clickpath**:
     * Go to **Add Column > Conditional Column** $\to$ Name: `StrategicPillar`.
     * Rules:
       * If `SkillDomain` equals `Tech` then `Digital, Cloud & Data Modernization`
       * Else If `SkillDomain` equals `Leadership` then `People Leadership & Operational Excellence`
       * Else If `SkillDomain` equals `Compliance` then `Enterprise Governance & Cyber Defense`
       * Else `Executive Communications & Storytelling`
     * Click **OK** $\to$ set type to **Text (`ABC`)**.
   * **M Formula**:
     ```powerquery
     if [SkillDomain] = "Tech" then "Digital, Cloud & Data Modernization"
     else if [SkillDomain] = "Leadership" then "People Leadership & Operational Excellence"
     else if [SkillDomain] = "Compliance" then "Enterprise Governance & Cyber Defense"
     else "Executive Communications & Storytelling"
     ```

3. **Accrediting Authority & External Vendor (`CertifyingVendor`)**:
   Tracks the external accrediting body for credential verification:
   * **GUI**: Go to **Add Column > Conditional Column** $\to$ Name: `CertifyingVendor`.
     * If `CourseID` equals `CRS-TECH-01` then `Microsoft Learn`
     * Else If `CourseID` equals `CRS-TECH-02` then `Snowflake & Microsoft`
     * Else If `CourseID` equals `CRS-TECH-03` then `Python Institute & Databricks`
     * Else If `CourseID` equals `CRS-TECH-04` then `AWS & CompTIA`
     * Else If `CourseID` equals `CRS-LEAD-01` then `Harvard ManageMentor`
     * Else If `CourseID` equals `CRS-LEAD-02` then `Six Sigma Global Institute`
     * Else If `CourseID` equals `CRS-COMP-01` then `Ministry of Manpower Egypt`
     * Else If `CourseID` equals `CRS-COMP-02` then `IAPP European Privacy Board`
     * Else `Corporate Talent Academy`
   * **M Formula**:
     ```powerquery
     if [CourseID] = "CRS-TECH-01" then "Microsoft Learn"
     else if [CourseID] = "CRS-TECH-02" then "Snowflake & Microsoft"
     else if [CourseID] = "CRS-TECH-03" then "Python Institute & Databricks"
     else if [CourseID] = "CRS-TECH-04" then "AWS & CompTIA"
     else if [CourseID] = "CRS-LEAD-01" then "Harvard ManageMentor"
     else if [CourseID] = "CRS-LEAD-02" then "Six Sigma Global Institute"
     else if [CourseID] = "CRS-COMP-01" then "Ministry of Manpower Egypt"
     else if [CourseID] = "CRS-COMP-02" then "IAPP European Privacy Board"
     else "Corporate Talent Academy"
     ```

4. **Continuous Professional Development Units (`CPD_Credits`)**:
   Recognized educational credit hours earned upon exam completion:
   * **GUI / Custom Column**: Name: `CPD_Credits` $\to$ Formula:
     ```powerquery
     if [CourseLevel] = "Level 3" then 40 else if [CourseLevel] = "Level 2" then 24 else 16
     ```
   * Set type to **Whole Number (`123`)**.

5. **Passing Score Benchmark (`PassingScoreThreshold`)**:
   * Go to **Add Column > Custom Column** $\to$ Name: `PassingScoreThreshold` $\to$ Formula: `70`.
   * Set type to **Whole Number (`123`)**.

6. **Certification Audit Validity Period (`ValidityPeriodMonths`)**:
   Compliance courses require annual renewal (12 months), while technical and leadership credentials remain valid for 24 months:
   * Go to **Add Column > Custom Column** $\to$ Name: `ValidityPeriodMonths`.
   * Formula:
     ```powerquery
     if [SkillDomain] = "Compliance" then 12 else 24
     ```
   * Set type to **Whole Number (`123`)**.

7. **Instructional Delivery Channel (`DeliveryModality`)**:
   * Go to **Add Column > Conditional Column** $\to$ Name: `DeliveryModality`.
   * If `SkillDomain` equals `Tech` then `Virtual Lab & Hands-on Sandbox`, Else If `SkillDomain` equals `Leadership` then `Executive Workshop & Cohort`, Else `Self-Paced E-Learning`. Click **OK**.

---

### Step 2.5d: Linking Surrogate Foreign Keys (`EmployeeKey` & `CourseKey`) in `Fact_TrainingCompletions` via GUI

Now that both master dimensions (`Dim_Employee` and `Dim_Course`) are properly prepared, link the surrogate foreign keys into `Fact_TrainingCompletions`:

#### 1. Looking up `EmployeeKey` from `Dim_Employee` via GUI Merge:
1. In the left **Queries** pane, select **`Fact_TrainingCompletions`**.
2. In the **Home** ribbon, click **Merge Queries > Merge Queries**.
3. In the Merge window:
   * Top table (`Fact_TrainingCompletions`): Click the column header **`EmployeeID`**.
   * Bottom table dropdown: Select **`Dim_Employee`** $\to$ click the column header **`الرقم التعريفي`**.
   * Join Kind: **Left Outer (all from first, matching from second)** $\to$ notice the green checkmark: *"The selection matches all rows"* $\to$ click **OK**.
4. In the table preview, scroll to the far right $\to$ click the **Expand Column icon (`↔`)** on `Dim_Employee`:
   * **Uncheck** `(Select All Columns)`.
   * **Check ONLY** **`EmployeeKey`**.
   * **Uncheck** `Use original column name as prefix` $\to$ click **OK**.
5. Set data type of `EmployeeKey` to **Whole Number (`123`)**.

#### 2. Looking up `CourseKey` from `Dim_Course` via GUI Merge (100% Match):
1. In the left **Queries** pane, ensure **`Fact_TrainingCompletions`** is selected.
2. In the **Home** ribbon, click **Merge Queries > Merge Queries**.
3. In the Merge window:
   * Top table (`Fact_TrainingCompletions`): Click the column header **`CourseID`**.
   * Bottom table dropdown: Select **`Dim_Course`** $\to$ click the column header **`CourseID`**.
   * Join Kind: **Left Outer (all from first, matching from second)**.
   * **Result**: Power Query will now proudly display:
     ```
     ✔ The selection matches 7197 of 7197 rows from the first table.
     ```
     *(Zero dropped records! 100% referential integrity!)*
   * Click **OK**.
4. Scroll to the far right $\to$ click the **Expand Column icon (`↔`)** on `Dim_Course`:
   * **Uncheck** `(Select All Columns)`.
   * **Check ONLY** **`CourseKey`**.
   * **Uncheck** `Use original column name as prefix` $\to$ click **OK**.
5. Set data type of `CourseKey` to **Whole Number (`123`)**.

#### 3. Column Pruning & VertiPaq Compression Optimization:
Because `Dim_Course` already stores the textual descriptions `CourseName` and `SkillDomain`, keeping them in the fact table duplicates strings across 7,197 rows and wastes columnar dictionary cache.
* Select column headers **`CourseName`** and **`SkillDomain`** in `Fact_TrainingCompletions` $\to$ right-click $\to$ select **Remove Columns**.
* *(Optional)*: Reorder columns so keys appear cleanly on the left:
  `CompletionKey`, `CompletionDateKey`, `EmployeeKey`, `CourseKey`, `Score`, `Status`, `Cost_EGP`, `IsPassed`, `ScoreTier`.

---

### Step 2.6: Production M Code for `Dim_Date` (Enterprise Calendar)

> [!TIP]
> While data tables are best built visually via the GUI, an enterprise calendar requires over 25 synchronized temporal attributes (relative offsets, fiscal quarters, Middle East weekends).
> 
> **How to apply**: Go to **Home > New Source > Blank Query**, click **Advanced Editor** in the ribbon, replace the placeholder text with the production M script below, and click **Done**.

```powerquery
let
    // 1. Dynamic Boundary Definition (Harvested Dynamically from Datasets)
    // Safely harvests date vectors across fact and dimension tables with fail-safe fallbacks:
    AttendanceDates = try List.Transform(List.RemoveNulls(Fact_DailyAttendance[AccessDate]), Date.From) 
                      otherwise (try List.Transform(List.RemoveNulls(Fact_DailyAttendance[Date]), Date.From) otherwise {}),
    
    TrainingDates   = try List.Transform(List.RemoveNulls(Fact_TrainingCompletions[CompletionDate]), Date.From) 
                      otherwise {},
    
    SnapshotDates   = try List.Transform(List.RemoveNulls(Fact_WorkforceSnapshot[SnapshotDate]), Date.From) 
                      otherwise (try List.Transform(List.RemoveNulls(Fact_WorkforceSnapshot[SnapshotMonth]), Date.From) otherwise {}),
    
    HireDates       = try List.Transform(List.RemoveNulls(Dim_Employee[HireDate]), Date.From) 
                      otherwise (try List.Transform(List.RemoveNulls(Dim_Employee[#"تاريخ التعيين"]), Date.From) otherwise {}),

    // Combine all date series across your loaded datasets
    // (Tip: If you only want the operational reporting period, remove HireDates from List.Combine)
    AllHarvestedDates = List.Combine({AttendanceDates, TrainingDates, SnapshotDates, HireDates}),

    // Determine dynamic earliest and latest dates with safety fallback if tables are loading
    MinHarvestedDate = if List.IsEmpty(AllHarvestedDates) then #date(2024, 1, 1) else List.Min(AllHarvestedDates),
    MaxHarvestedDate = if List.IsEmpty(AllHarvestedDates) then #date(2026, 12, 31) else List.Max(AllHarvestedDates),

    // Kimball Full-Year Calendar Boundaries:
    // Expand to complete calendar years (Jan 1 of earliest year to Dec 31 of latest year or current year)
    // Mandatory for DAX Time Intelligence (SAMEPERIODLASTYEAR, TOTALYTD, DATEADD) to operate with zero gaps.
    Today = DateTime.Date(DateTime.LocalNow()),
    CurrentYear = Date.Year(Today),
    CurrentMonth = Date.Month(Today),

    StartDate = #date(Date.Year(MinHarvestedDate), 1, 1),
    EndDate = #date(List.Max({Date.Year(MaxHarvestedDate), CurrentYear}), 12, 31),

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

### Step 2.7c: Ingesting & Cleansing Client Delivery & Milestone Tasks (`Fact_ProjectTasks`) via GUI

Nexora Tech Solutions operates as a high-end offshore software engineering and digital transformation consultancy. To track client delivery efficiency, project margins, scope creep, and billable engineering utilization, we ingest **3,600 delivery milestone tasks** across international client engagements (Aramco, Emirates Digital, UK RetailNext, US HealthBridge, etc.).

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Power Query Editor — Ingesting Client Projects & Tasks (Fact_ProjectTasks)                            │
├───────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [New Source > Text/CSV] ──► Select "data/raw/client_projects_tasks.csv" (or .json)                   │
│ [Data Types]            ──► TaskID (Text), PlannedHours (Decimal), ActualHours (Decimal), Rate (Fixed)│
│ [Merge Queries]         ──► Join Dim_Employee on AssignedEmployeeID = الرقم التعريفي (EmployeeKey)    │
│ [Merge Queries]         ──► Join Dim_CurrencyRates on USD = CurrencyCode (CurrencyKey)                │
│ [Add Custom Columns]    ──► ScopeOverrunHours, ScopeOverrunPct, TotalBilling_EGP                      │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 1. Ingesting Raw Task Data via GUI:
1. In Power Query Editor **Home** ribbon, click **New Source > Text/CSV** (or **New Source > JSON** if using `data/raw/client_projects_tasks.json`).
2. Browse to `data/raw/client_projects_tasks.csv` and click **Open**.
3. Verify file origin is **65001: Unicode (UTF-8)** and delimiter is **Comma**. Click **OK**.
4. In the left **Queries** pane, right-click the query and rename it to **`Fact_ProjectTasks`**.

#### 2. Setting Visual Column Data Types:
Click the type icon on each column header:
* `TaskID`, `ProjectID`, `ProjectName`, `ClientName`, `ClientCountry`, `ClientRegion`, `Industry`: **Text (`ABC`)**.
* `AssignedEmployeeID`: **Text (`ABC`)**.
* `TaskTitle`, `SkillDomain`, `ComplexityTier`, `TaskStatus`: **Text (`ABC`)**.
* `PlannedHours`, `ActualHours`: **Decimal Number (`1.2`)**.
* `IsHoursOverrun`, `IsDeliveryDelayed`: **True/False (`✔️/❌`)**.
* `BillableHourlyRate_USD`, `TotalBilling_USD`: **Fixed Decimal Number (`$`)**.
* `ClientSatisfactionRating`: **Decimal Number (`1.2`)**.
* `TaskStartDate`, `DeliveryDeadline`, `ActualCompletionDate`: **Date (`📅`)**.

#### 3. Resolving Surrogate Foreign Keys (`EmployeeKey` & `DateKey`) via GUI:

##### 3a. Merging with `Dim_Employee` to Link `EmployeeKey`:
1. In the **Home** ribbon, click **Merge Queries > Merge Queries**.
2. Select `Fact_ProjectTasks` on top; click the **`AssignedEmployeeID`** column header.
3. In the lower dropdown, select **`Dim_Employee`**; click the **`الرقم التعريفي`** (or `EmployeeID`) column header.
4. Join Kind: **Left Outer (all from first, matching from second)** $\to$ click **OK**.
5. Click the **Expand (`⤢`)** icon on the new column header $\to$ uncheck *(Select All Columns)* $\to$ check only **`EmployeeKey`** $\to$ uncheck *"Use original column name as prefix"* $\to$ click **OK**.
6. Set `EmployeeKey` type to **Whole Number (`123`)**.

##### 3b. Generating Calendar Surrogate Keys (`DateKey` format `YYYYMMDD`):
To link tasks to `Dim_Date` without expensive DateTime joins:
1. Switch to **Add Column > Custom Column**.
2. Name: `StartDateKey` $\to$ Formula:
   ```
   Date.Year([TaskStartDate]) * 10000 + Date.Month([TaskStartDate]) * 100 + Date.Day([TaskStartDate])
   ```
3. Repeat for `DeadlineDateKey`:
   ```
   Date.Year([DeliveryDeadline]) * 10000 + Date.Month([DeliveryDeadline]) * 100 + Date.Day([DeliveryDeadline])
   ```
4. Repeat for `CompletionDateKey` (with null-safety):
   ```
   if [ActualCompletionDate] <> null then Date.Year([ActualCompletionDate]) * 10000 + Date.Month([ActualCompletionDate]) * 100 + Date.Day([ActualCompletionDate]) else null
   ```
5. Set all three new key columns to **Whole Number (`123`)**.

#### 4. Adding Business Diagnostic Columns via GUI:

##### 4a. Scope Overrun Hours & Overrun %:
1. Go to **Add Column > Custom Column**.
2. Name: `ScopeOverrunHours` $\to$ Formula:
   ```
   [ActualHours] - [PlannedHours]
   ```
3. Go to **Add Column > Custom Column**.
4. Name: `ScopeOverrunPct` $\to$ Formula:
   ```
   if [PlannedHours] > 0 then ([ActualHours] - [PlannedHours]) / [PlannedHours] else 0
   ```
5. Set `ScopeOverrunHours` to **Decimal Number (`1.2`)** and `ScopeOverrunPct` to **Percentage (`%`)**.

##### 4b. Local Currency Realization (`TotalBilling_EGP`):
1. Go to **Add Column > Custom Column**.
2. Name: `TotalBilling_EGP` $\to$ Formula:
   ```
   [TotalBilling_USD] * 48.85
   ```
3. Set type to **Fixed Decimal Number (`$`)**.

#### 5. Production M Code for `Fact_ProjectTasks` (with In-Memory Caching):
For automated deployment or TMDL script injection:

```powerquery-m
let
    Source = Csv.Document(File.Contents("data/raw/client_projects_tasks.csv"), [Delimiter=",", Columns=22, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"TaskID", type text}, {"ProjectID", type text}, {"ProjectName", type text},
        {"ClientName", type text}, {"ClientCountry", type text}, {"ClientRegion", type text},
        {"Industry", type text}, {"AssignedEmployeeID", type text}, {"TaskTitle", type text},
        {"SkillDomain", type text}, {"ComplexityTier", type text}, {"PlannedHours", type number},
        {"ActualHours", type number}, {"IsHoursOverrun", type logical}, {"BillableHourlyRate_USD", Currency.Type},
        {"TotalBilling_USD", Currency.Type}, {"TaskStatus", type text}, {"ClientSatisfactionRating", type number},
        {"TaskStartDate", type date}, {"DeliveryDeadline", type date}, {"ActualCompletionDate", type date},
        {"IsDeliveryDelayed", type logical}
    }),
    
    // In-memory buffer for high-speed dimensional join
    BufferedEmployees = Table.Buffer(Dim_Employee),
    
    // Merge surrogate key from Dim_Employee
    #"Merged Dim_Employee" = Table.NestedJoin(#"Changed Type", {"AssignedEmployeeID"}, BufferedEmployees, {"الرقم التعريفي"}, "Dim_Employee", JoinKind.LeftOuter),
    #"Expanded Dim_Employee" = Table.ExpandTableColumn(#"Merged Dim_Employee", "Dim_Employee", {"EmployeeKey"}, {"EmployeeKey"}),
    
    // Generate YYYYMMDD surrogate date keys
    #"Added StartDateKey" = Table.AddColumn(#"Expanded Dim_Employee", "StartDateKey", each Date.Year([TaskStartDate]) * 10000 + Date.Month([TaskStartDate]) * 100 + Date.Day([TaskStartDate]), Int64.Type),
    #"Added DeadlineDateKey" = Table.AddColumn(#"Added StartDateKey", "DeadlineDateKey", each Date.Year([DeliveryDeadline]) * 10000 + Date.Month([DeliveryDeadline]) * 100 + Date.Day([DeliveryDeadline]), Int64.Type),
    #"Added CompletionDateKey" = Table.AddColumn(#"Added DeadlineDateKey", "CompletionDateKey", each if [ActualCompletionDate] <> null then Date.Year([ActualCompletionDate]) * 10000 + Date.Month([ActualCompletionDate]) * 100 + Date.Day([ActualCompletionDate]) else null, Int64.Type),
    
    // Derived Operational Metrics
    #"Added ScopeOverrunHours" = Table.AddColumn(#"Added CompletionDateKey", "ScopeOverrunHours", each [ActualHours] - [PlannedHours], type number),
    #"Added ScopeOverrunPct" = Table.AddColumn(#"Added ScopeOverrunHours", "ScopeOverrunPct", each if [PlannedHours] > 0 then ([ActualHours] - [PlannedHours]) / [PlannedHours] else 0, Percentage.Type),
    #"Added TotalBilling_EGP" = Table.AddColumn(#"Added ScopeOverrunPct", "TotalBilling_EGP", each [TotalBilling_USD] * 48.85, Currency.Type)
in
    #"Added TotalBilling_EGP"
```

---

### Step 2.7d: Ingesting & Standardizing Central Bank FX Spot Rates (`Dim_CurrencyRates`) via GUI

Nexora Tech Solutions bills offshore enterprise accounts in multiple global currencies (**USD, EUR, GBP, SAR, AED**) while managing domestic salaries and facility overhead in **EGP**. Ingesting daily FX spot rates enables seamless, dynamic currency conversions in DAX without hardcoding exchange multipliers.

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Dim_CurrencyRates Schema Contract & Normalization Factors                                             │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ CurrencyKey │ CurrencyCode │ CurrencyName          │ RateToEGP │ OneEGPInCurrency │ RateType           │
├─────────────┼──────────────┼───────────────────────┼───────────┼──────────────────┼────────────────────┤
│ 1           │ EGP          │ Egyptian Pound        │ 1.0000    │ 1.000000         │ Base Operational   │
│ 2           │ USD          │ United States Dollar  │ 48.8500   │ 0.020471         │ Central Bank Spot  │
│ 3           │ EUR          │ Euro                  │ 53.2000   │ 0.018797         │ Central Bank Spot  │
│ 4           │ GBP          │ British Pound         │ 63.5000   │ 0.015748         │ Central Bank Spot  │
│ 5           │ SAR          │ Saudi Riyal           │ 13.0200   │ 0.076805         │ Regional Pegged    │
│ 6           │ AED          │ UAE Dirham            │ 13.3000   │ 0.075188         │ Regional Pegged    │
└─────────────┴──────────────┴───────────────────────┴───────────┴──────────────────┴────────────────────┘
```

#### 1. Ingesting Currency Master Data via GUI:
1. Go to **Home > New Source > Text/CSV**.
2. Select `data/raw/dim_currency_rates.csv` (or `data/processed/Dim_CurrencyRates.csv`) and click **Open**.
3. Verify UTF-8 encoding and click **OK**. Rename the query to **`Dim_CurrencyRates`**.

#### 2. Visual Column Data Types:
* `CurrencyKey`: **Whole Number (`123`)**.
* `CurrencyCode`: **Text (`ABC`)**.
* `CurrencyName`: **Text (`ABC`)**.
* `RateToEGP`: **Decimal Number (`1.2`)**.
* `OneEGPInCurrency`: **Decimal Number (`1.2`)**.
* `RateType`: **Text (`ABC`)**.
* `LastUpdated`: **Date/Time (`📅🕒`)**.

#### 3. Production M Code for `Dim_CurrencyRates`:
```powerquery-m
let
    Source = Csv.Document(File.Contents("data/raw/dim_currency_rates.csv"), [Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"CurrencyKey", Int64.Type},
        {"CurrencyCode", type text},
        {"CurrencyName", type text},
        {"RateToEGP", type number},
        {"OneEGPInCurrency", type number},
        {"RateType", type text},
        {"LastUpdated", type datetime}
    }),
    #"Buffered Table" = Table.Buffer(#"Changed Type")
in
    #"Buffered Table"
```

---

### Step 2.7e: Enriching L&D Curriculum Catalog (`Dim_Course`) with Level 1, 2, 3 Hierarchy via GUI

To analyze training ROI ($\Delta P$) and skill advancement velocity, the L&D curriculum must be organized into standardized proficiency tiers:
* **Level 1 (Foundational)**: Entry-level certificates (Cloud Foundations, Python, Agile Scrum).
* **Level 2 (Intermediate)**: Role-specific certifications (AWS Solutions Architect, Databricks PySpark, Docker/GitHub Actions, Full-Stack Next.js).
* **Level 3 (Advanced)**: Enterprise architect credentials (Kubernetes CKA, Microsoft Fabric Governance, Zero-Trust Cybersecurity).

#### 1. Ingesting Curriculum Catalog via GUI:
1. Go to **Home > New Source > Text/CSV**.
2. Select `data/raw/lms_curriculum_catalog.csv` and click **Open**. Click **OK**.
3. Rename the query to **`Dim_Course`** (or merge it into existing `Dim_Course` created in Step 2.5c).
4. Verify column data types:
   * `CourseKey`: **Whole Number (`123`)**.
   * `CourseID`: **Text (`ABC`)**.
   * `CourseName`: **Text (`ABC`)**.
   * `SkillDomain`: **Text (`ABC`)**.
   * `CourseLevel`: **Text (`ABC`)** — Contains `Level 1 (Foundational)`, `Level 2 (Intermediate)`, `Level 3 (Advanced)`.
   * `AccreditationBody`: **Text (`ABC`)**.
   * `DurationHours`: **Whole Number (`123`)**.
   * `Cost_EGP`: **Fixed Decimal Number (`$`)**.
   * `PassingThreshold`: **Whole Number (`123`)**.
   * `ExpectedSalaryDelta_Pct`: **Percentage (`%`)**.

---

### Step 2.8: The Complete Kimball Galaxy Constellation Model Topology

Before committing all queries to the Power BI Tabular Engine, verify that your data model strictly implements the Kimball Fact Constellation architecture. The dimensional model comprises **6 Conformed Dimensions** sharing relationships across **5 Galaxy Fact Tables**:

```
                                  ┌────────────────────────┐
                                  │     Dim_Department     │
                                  │     (DepartmentKey)    │
                                  └───────────┬────────────┘
                                              │
                 ┌────────────────────────────┼────────────────────────────┐
                 │ 1:*                        │ 1:*                        │ 1:*
                 ▼                            ▼                            ▼
     ┌───────────────────────┐    ┌───────────────────────┐    ┌───────────────────────┐
     │ Fact_WorkforceSnapshot│    │ Fact_DepartmentBudget │    │  Dim_Employee (SCD-2) │
     │   (Monthly Census)    │    │   (Quarterly FP&A)    │    │     (EmployeeKey)     │
     └───────────┬───────────┘    └───────────┬───────────┘    └───────────┬───────────┘
                 │ 1:*                        │ 1:*                        │ 1:*
                 │                            │              ┌─────────────┼─────────────┐
                 │                            │              │             │             │
                 ▼                            ▼              ▼             ▼             ▼
     ┌───────────────────────┐    ┌────────────────────┐   ┌───────────────────┐   ┌───────────────────┐
     │       Dim_Date        │◄───┤Fact_DailyAttendance│   │Fact_TrainingCompl.│   │ Fact_ProjectTasks │
     │       (DateKey)       │    │    (Daily IoT)     │   │   (LMS Attempts)  │   │ (Client Delivery) │
     └───────────▲───────────┘    └───────────▲────────┘   └─────────┬─────────┘   └─────────┬─────────┘
                 │                            │                      │ 1:*                   │
                 │ 1:*                        │ 1:*                  ▼                       │ 1:*
                 │                  ┌─────────┴─────────┐  ┌───────────────────┐             │
                 └──────────────────┤     Dim_Branch    │  │    Dim_Course     │             │
                                    │    (BranchKey)    │  │    (CourseKey)    │             │
                                    └───────────────────┘  └───────────────────┘             ▼
                                                                                   ┌───────────────────┐
                                                                                   │ Dim_CurrencyRates │
                                                                                   │   (CurrencyKey)   │
                                                                                   └───────────────────┘
```

#### Galaxy Schema Referential Integrity Matrix (18 Active Relationships):

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
| **`Fact_TrainingCompletions`** | `CompletionDateKey`| `Dim_Date` | `DateKey` | Many-to-One (`*:1`) | Single | Examination completion date |
| **`Fact_ProjectTasks`** | `EmployeeKey` | `Dim_Employee` | `EmployeeKey` | Many-to-One (`*:1`) | Single | 1 row per delivery task / milestone |
| **`Fact_ProjectTasks`** | `StartDateKey` | `Dim_Date` | `DateKey` | Many-to-One (`*:1`) | Single | Task initiation calendar date |
| **`Fact_ProjectTasks`** | `DeadlineDateKey` | `Dim_Date` | `DateKey` | Many-to-One (`*:1`) | Single (Inactive) | Delivery commitment deadline |
| **`Fact_ProjectTasks`** | `CompletionDateKey`| `Dim_Date` | `DateKey` | Many-to-One (`*:1`) | Single (Inactive) | Final handover / signoff date |
| **`Fact_ProjectTasks`** | `CurrencyCode` | `Dim_CurrencyRates` | `CurrencyCode` | Many-to-One (`*:1`) | Single | Contract FX conversion rate |

> [!CAUTION]
> **Kimball Galaxy Cardinality Rules**:
> 1. **Never Create Direct Fact-to-Fact Relationships**: Joining `Fact_DailyAttendance` or `Fact_ProjectTasks` directly to `Fact_WorkforceSnapshot` creates a toxic Many-to-Many circular path resulting in double-counting and VertiPaq memory exhaustion.
> 2. **Always Filter Downward Through Dimensions**: Slicers on `Dim_Department[DepartmentName]`, `Dim_Branch[Region]`, `Dim_Employee[JobRole]`, or `Dim_Date[FiscalQuarter]` propagate naturally to all 5 fact tables simultaneously.
> 3. **Single Cross-Filter Direction (`→`)**: Keep all relationship cross-filtering set to **Single**. Bidirectional filtering introduces ambiguous filter paths and severe performance degradation on large datasets.
> 4. **Role-Playing Date Dimensions**: For `Fact_ProjectTasks`, `StartDateKey` is the active relationship. `DeadlineDateKey` and `CompletionDateKey` must be set to **Inactive**, activated on demand via DAX `USERELATIONSHIP()`.

---

### ⚠️ Deep Dive: Resolving Missing `EmployeeKey` in `Fact_DailyAttendance` via GUI

When establishing the relationship between `Fact_DailyAttendance` and `Dim_Employee` in Power BI Desktop **Model View**, you may find that you cannot locate **`EmployeeKey`** inside `Fact_DailyAttendance`.

**Why this occurs**: The raw IoT badge event logs arrive with the business string key **`EmployeeID`** (e.g. `EMP-10001` .. `EMP-17000`), whereas the numeric surrogate key **`EmployeeKey`** (integers `1` through `7000`) was generated as an index inside `Dim_Employee`.

You have two simple ways to resolve this in the Power BI GUI:

#### Method A: Add `EmployeeKey` via Power Query GUI Merge (Recommended Kimball Standard ⭐)
This keeps your Galaxy Schema pure with integer surrogate keys across all relationships:
1. In Power BI Desktop, click **Home > Transform Data** to open Power Query Editor.
2. In the left **Queries** pane, select **`Fact_DailyAttendance`** (or `Fact_Badge_Access_Logs_SQL`).
3. In the **Home** ribbon, click **Merge Queries > Merge Queries**.
4. In the **Merge** dialog window:
   * Select **`Fact_DailyAttendance`** (top table) $\to$ click the **`EmployeeID`** column header.
   * Select **`Dim_Employee`** (bottom dropdown) $\to$ click the **`الرقم التعريفي`** column header (which holds `EMP-10001` .. `EMP-17000`).
   * **Join Kind**: **Left Outer (all from first, matching from second)**.
   * The status indicator at the bottom will confirm: *"The selection matches all rows from the first table"*.
   * Click **OK**.
5. In the table preview, scroll to the far right $\to$ locate the new column named **`Dim_Employee`** containing `[Table]` links.
6. Click the **Expand Column icon (`↔`)** at the top right of the `Dim_Employee` header:
   * **Uncheck** *(Select All Columns)*.
   * **Check ONLY** **`EmployeeKey`**.
   * **Uncheck** *Use original column name as prefix*.
   * Click **OK**.
7. Click the data type icon next to the new `EmployeeKey` header $\to$ select **Whole Number (`123`)**.
8. *(Optional)*: If you also want to relate to `Dim_Branch`, you can derive `BranchKey` using **Add Column > Custom Column**:
   `if Text.StartsWith([BuildingID], "BLD-") then Value.FromText(Text.End([BuildingID], 3)) else null` (set type to **Whole Number (`123`)**).
9. Click **Home > Close & Apply**.
10. Switch to Power BI Desktop **Model View**:
    * Drag **`Fact_DailyAttendance[EmployeeKey]`** onto **`Dim_Employee[EmployeeKey]`**.
    * Power BI creates a clean **Many-to-One (`*:1`)** relationship with **Single** cross-filter direction!

#### Method B: Direct Relationship on Natural Keys in Model View (Zero Power Query Steps Needed)
If you prefer not to add an extra merge step in Power Query:
1. Switch to Power BI Desktop **Model View**.
2. Locate the **`Fact_DailyAttendance`** table card and the **`Dim_Employee`** table card.
3. Drag **`Fact_DailyAttendance[EmployeeID]`** directly onto **`Dim_Employee[الرقم التعريفي]`**.
4. Because each employee code appears exactly once in `Dim_Employee` (7,000 unique rows), Power BI will automatically create a valid **Many-to-One (`*:1`)** relationship with **Single** cross-filter direction (`Fact_DailyAttendance` $\to$ `Dim_Employee`).
5. All DAX measures and dimension slicers (`Dim_Employee[القسم]`, `Dim_Employee[الفرع]`, `Dim_Employee[AgeBand]`) will filter attendance records seamlessly!

---

### ⚠️ Deep Dive: Resolving "0 of 7197 Matches" in CourseID Merge & Cleaning `Dim_Course` via GUI

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ Merge Dialog (Power Query Editor)                                                      │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ Top Table:    Fact_TrainingCompletions  -> Column: [ CourseID ] (CRS-102, CRS-101...) │
│ Bottom Table: Dim_Course                -> Column: [ CourseID ] (CRS-SOFT-02...)       │
│                                                                                        │
│ Join Kind: Left Outer (all from first, matching from second)                           │
│                                                                                        │
│ [✔] The selection matches 0 of 7197 rows from the first table.  <-- ⚠️ ZERO MATCHES    │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

#### Why This Occurred (The Two-File Catalog Trap):
1. **Source Disconnect**: `Fact_TrainingCompletions` was loaded from SQL Server `raw.LMS_Certifications` (7,197 records), which uses canonical course IDs `CRS-101`, `CRS-102`, `CRS-103`, `CRS-201`, `CRS-202`, `CRS-301`, `CRS-302`.
2. **Dimension Disconnect**: `Dim_Course` was imported from the legacy CSV `lms_course_completions.csv` (2,735 records), which used an older prefix naming convention (`CRS-SOFT-02`, `CRS-LEAD-01`, etc.). Because the course codes belong to two completely separate taxonomies, **zero rows matched**!
3. **Dimensional Pollution**: `Dim_Course` was also mistakenly populated with transaction-level completion metrics (`CompletionKey`, `CompletionDateKey`, `Score`, `IsPassed`). A dimension table in a Kimball star schema must **only** describe the conformed entity (the course itself), never individual student exam attempts!

#### The 4-Step Visual Fix in Power Query GUI:

##### Step 1: Re-Source `Dim_Course` via Reference (Guarantees 100% Alignment)
1. In the left **Queries** pane, right-click your existing **`Dim_Course`** query $\to$ select **Delete** (or delete all its applied steps after `Source`).
2. Right-click **`Fact_TrainingCompletions`** in the left **Queries** pane $\to$ select **Reference** (creates a lightweight linked query).
3. Rename this new query to **`Dim_Course`**.

##### Step 2: Strip Out Transaction Columns
1. In the table preview, click the header **`CourseID`**.
2. Hold `Ctrl` and click headers: **`CourseName`**, **`SkillDomain`**, and **`Cost_EGP`**.
3. Right-click any highlighted header $\to$ select **Remove Other Columns**.
   *(All transactional columns: `EmployeeID`, `CompletionDate`, `Score`, `Status`, `IsPassed`, `CompletionKey`, `CompletionDateKey` disappear instantly!)*

##### Step 3: Deduplicate to Distinct Course Catalog
1. Click the header **`CourseID`**.
2. Go to **Home > Remove Rows > Remove Duplicates**.
   *(The 7,197 rows instantly collapse down to the exact distinct course catalog!)*
3. Click the dropdown on `CourseID` $\to$ select **Sort Ascending**.
4. Go to **Add Column > Index Column > From 1**.
5. Rename the new column to **`CourseKey`** $\to$ set data type to **Whole Number (`123`)**. Drag it to the far left.

##### Step 4: Re-Run the Merge in `Fact_TrainingCompletions` (100% Match!)
1. In the left **Queries** pane, click **`Fact_TrainingCompletions`**.
2. In the **Home** ribbon, click **Merge Queries > Merge Queries**.
3. Top table (`Fact_TrainingCompletions`): Click **`CourseID`**.
4. Bottom table dropdown: Select **`Dim_Course`** $\to$ click **`CourseID`**.
5. Join Kind: **Left Outer**.
6. **Behold the Status Indicator**:
   ```
   ✔ The selection matches 7197 of 7197 rows from the first table.
   ```
   *(Zero dropped records! Exactly 7,197 of 7,197 matches!)*
7. Click **OK** $\to$ scroll to the far right $\to$ click the **Expand icon (`↔`)** on `Dim_Course`:
   * Check ONLY **`CourseKey`**.
   * Uncheck *Use original column name as prefix*.
   * Click **OK** $\to$ set type to **Whole Number (`123`)**.

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

### Step 2.9: Enterprise Data Enrichment, Parameters, Live REST APIs & Advanced M Techniques

To elevate your semantic model from an academic prototype to an enterprise-grade corporate solution, apply these production patterns combining **Power Query GUI workflows** and **high-performance M language formulas**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ Modern Enterprise Power Query Architecture                                             │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. Parameters        -> Dynamic connection routing (Dev / Test / Prod)                 │
│ 2. Live REST API     -> Real-time FX exchange rates (USD / EUR / AED / EGP) via Web API│
│ 3. Spatial Enrichment-> GPS coordinates & branch tiers for Azure Map visual analytics   │
│ 4. M Functions       -> Table buffering, Arabic text cleansing & try-otherwise guards  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 1. Dynamic Environment Parameters via GUI (`Manage Parameters`):
Hardcoding file paths and database connection strings creates broken reports when deploying between environments. Power Query Parameters allow one-click environment switching:

##### How to Create Parameters via the Ribbon GUI:
1. In Power Query Editor, go to the **Home** ribbon tab.
2. Click **Manage Parameters > New Parameter**.
3. Create the following 4 enterprise parameters:

| Parameter Name | Description | Type | Suggested Values | Current / Default Value |
| :--- | :--- | :---: | :---: | :--- |
| **`pServerName`** | Database host address | `Text` | List: `localhost`, `sql-staging.corp`, `sql-prod.database.windows.net` | `localhost` |
| **`pDatabaseName`** | Target DWH catalog | `Text` | Any value | `EnterpriseHR_DWH` |
| **`pDataDirectory`** | Raw file system directory | `Text` | Any value | `D:\courses\Data Science\Data Engineering\Projects\enterprise-hr-analytics\data\raw` |
| **`pTargetCurrency`** | Reporting currency target | `Text` | List: `EGP`, `USD`, `AED`, `SAR`, `EUR` | `EGP` |

4. Click **OK**.
5. **Binding Parameters to Queries**:
   * For SQL Server queries (`Fact_WorkforceSnapshot`, `raw.Badge_Access_Logs`): In the **Source** step formula, replace `"localhost"` with `pServerName`, and `"EnterpriseHR_DWH"` with `pDatabaseName`.
   * For flat files (`employees_data_7000.txt`): In the **Source** step, replace the hardcoded path with `pDataDirectory & "\employees_data_7000.txt"`.
   * Now, whenever you clone the project or deploy to another workstation, you only change the parameter values in one dialog!

---

#### 2. Ingesting Live Macroeconomic & Currency Rates via REST API (`Web.Contents`):
In multinational organizations, training course licensing (AWS, Microsoft, Databricks) and executive compensation are benchmarked in USD or EUR. Integrating a live REST API provides real-time currency conversions.

##### A. GUI Clickpath:
1. In Power Query Editor, go to **Home > New Source > Web**.
2. Select **Basic** $\to$ enter the public Open Exchange endpoint:
   `https://open.er-api.com/v6/latest/USD`
3. Click **OK** $\to$ select **Anonymous** authentication $\to$ click **Connect**.
4. Power Query displays a root record. Click the yellow word **`Record`** next to field **`rates`**.
5. Go to the **Transform** ribbon $\to$ click **To Table** $\to$ click **OK**.
6. Rename column `Name` to `CurrencyCode`, and `Value` to `ExchangeRateToUSD`.
7. Filter `CurrencyCode` to key trading currencies: `USD`, `EGP`, `AED`, `SAR`, `EUR`, `GBP`.
8. Set `ExchangeRateToUSD` to **Decimal Number (`1.2`)**.

##### B. Production Service-Safe M Code (RelativePath Pattern):
> [!IMPORTANT]
> **Why `RelativePath` is Mandatory**: If you concatenate dynamic strings directly inside `Web.Contents(url & param)`, Power BI Service will refuse to refresh on a schedule due to security firewall rules. Using `RelativePath` keeps the base domain static so Power BI can authenticate and whitelist the data source.

Click **Home > New Source > Blank Query** $\to$ **Advanced Editor** $\to$ paste:

```powerquery
let
    // 1. Static base URL for Power BI Service scheduled refresh safety
    BaseUrl = "https://open.er-api.com",
    
    // 2. Fetch live JSON payload
    Source = Json.Document(
        Web.Contents(BaseUrl, [
            RelativePath = "/v6/latest/USD",
            Headers = [#"Accept" = "application/json"]
        ])
    ),
    
    // 3. Extract rates table
    RatesRecord = Source[rates],
    RatesTable = Record.ToTable(RatesRecord),
    #"Renamed Columns" = Table.RenameColumns(RatesTable, {{"Name", "CurrencyCode"}, {"Value", "ExchangeRateToUSD"}}),
    #"Filtered Currencies" = Table.SelectRows(#"Renamed Columns", each List.Contains({"USD", "EGP", "AED", "SAR", "EUR", "GBP"}, [CurrencyCode])),
    #"Changed Type" = Table.TransformColumnTypes(#"Filtered Currencies", {{"CurrencyCode", type text}, {"ExchangeRateToUSD", type number}}),
    
    // 4. Compute EGP relative conversion rates
    EgpRate = #"Changed Type"{[CurrencyCode="EGP"]}[ExchangeRateToUSD],
    #"Added RateToEGP" = Table.AddColumn(#"Changed Type", "RateToEGP", each [ExchangeRateToUSD] / EgpRate, type number),
    #"Added EGPToCurrency" = Table.AddColumn(#"Added RateToEGP", "OneEGPInCurrency", each 1 / ([ExchangeRateToUSD] / EgpRate), type number),
    #"Added RefreshTimestamp" = Table.AddColumn(#"Added EGPToCurrency", "LastRefreshedUTC", each DateTimeZone.UtcNow(), type datetimezone),

    // 5. Add Primary Surrogate Key (CurrencyKey) for Data Modeling Relationships
    #"Sorted Currencies" = Table.Sort(#"Added RefreshTimestamp", {{"CurrencyCode", Order.Ascending}}),
    #"Added CurrencyKey" = Table.AddIndexColumn(#"Sorted Currencies", "CurrencyKey", 1, 1, Int64.Type),
    #"Reordered Columns" = Table.ReorderColumns(#"Added CurrencyKey", {"CurrencyKey", "CurrencyCode", "ExchangeRateToUSD", "RateToEGP", "OneEGPInCurrency", "LastRefreshedUTC"})
in
    #"Reordered Columns"
```
Rename this query to **`Dim_CurrencyRates`**.

> [!TIP]
> **GUI Clickpath to Add `CurrencyKey` Visually**:
> 1. In `Dim_CurrencyRates`, go to **Add Column > Index Column > From 1**.
> 2. Right-click the new `Index` header $\to$ **Rename** to **`CurrencyKey`**.
> 3. Drag `CurrencyKey` to the far left $\to$ ensure data type is **Whole Number (`123`)**.

---

#### 3. Spatial Geocoding & Regional Tiering in `Dim_Branch`:
To enable Power BI's interactive Map visual and Azure Maps with bubble sizing by headcount or budget, enrich `Dim_Branch` with exact Egyptian geographic coordinates:

##### GUI / Custom Column Steps:
1. In the left pane, select **`Dim_Branch`**.
2. **Add Latitude via Custom Column**:
   * Go to **Add Column > Custom Column** $\to$ Name: `Latitude`.
   * Formula:
     ```powerquery
     if Text.Contains([BranchName], "المعادي") then 29.9599
     else if Text.Contains([BranchName], "التجمع") then 30.0074
     else if Text.Contains([BranchName], "مصر الجديدة") then 30.0898
     else if Text.Contains([BranchName], "القرية الذكية") then 30.0716
     else if Text.Contains([BranchName], "أكتوبر") or Text.Contains([BranchName], "اكتوبر") then 29.9678
     else if Text.Contains([BranchName], "زايد") then 30.0435
     else if Text.Contains([BranchName], "الدقي") then 30.0385
     else if Text.Contains([BranchName], "لوران") then 31.2464
     else if Text.Contains([BranchName], "سموحة") then 31.2156
     else if Text.Contains([BranchName], "المنصورة") then 31.0409
     else if Text.Contains([BranchName], "طنطا") then 30.7865
     else if Text.Contains([BranchName], "دمياط") then 31.4367
     else if Text.Contains([BranchName], "بورسعيد") then 31.2653
     else 27.1809 // أسيوط - أسيوط الجديدة
     ```
   * Set type to **Decimal Number (`1.2`)**.

3. **Add Longitude via Custom Column**:
   * Go to **Add Column > Custom Column** $\to$ Name: `Longitude`.
   * Formula:
     ```powerquery
     if Text.Contains([BranchName], "المعادي") then 31.2595
     else if Text.Contains([BranchName], "التجمع") then 31.4913
     else if Text.Contains([BranchName], "مصر الجديدة") then 31.3285
     else if Text.Contains([BranchName], "القرية الذكية") then 31.0216
     else if Text.Contains([BranchName], "أكتوبر") or Text.Contains([BranchName], "اكتوبر") then 30.9388
     else if Text.Contains([BranchName], "زايد") then 30.9998
     else if Text.Contains([BranchName], "الدقي") then 31.2117
     else if Text.Contains([BranchName], "لوران") then 29.9723
     else if Text.Contains([BranchName], "سموحة") then 29.9489
     else if Text.Contains([BranchName], "المنصورة") then 31.3785
     else if Text.Contains([BranchName], "طنطا") then 31.0004
     else if Text.Contains([BranchName], "دمياط") then 31.6738
     else if Text.Contains([BranchName], "بورسعيد") then 32.3019
     else 31.1837 // أسيوط - أسيوط الجديدة
     ```
   * Set type to **Decimal Number (`1.2`)**.

4. **Add Operational Branch Tier via Conditional Column**:
   * Go to **Add Column > Conditional Column** $\to$ Name: `BranchTier`.
   * Rules:
     * If `Region` equals `Greater Cairo` then `Tier 1 - Strategic Metro Hub`
     * Else If `Region` equals `Alexandria & North` then `Tier 1 - Strategic Metro Hub`
     * Else If `Region` equals `Delta` then `Tier 2 - Regional Commercial Center`
     * Else `Tier 3 - Emerging Expansion Office`
   * Set type to **Text (`ABC`)**.

---

#### 4. Workforce & Attendance Behavioral Enrichments:

##### A. In `Fact_DailyAttendance`:
1. **Tardiness Violation Flag (`IsTardyArrival`)**:
   Core enterprise working hours commence at 09:00 AM with a 15-minute grace window:
   * Go to **Add Column > Custom Column** $\to$ Name: `IsTardyArrival`.
   * Formula:
     ```powerquery
     if [CheckInTime] <> null and [CheckInTime] > #time(9, 15, 0) then 1 else 0
     ```
   * Set type to **Whole Number (`123`)**.

2. **Overtime Shift Hours (`OvertimeHours`)**:
   Standard physical shift is 8.5 hours (including lunch):
   * Go to **Add Column > Custom Column** $\to$ Name: `OvertimeHours`.
   * Formula:
     ```powerquery
     if [DurationHours] > 8.5 then Number.Round([DurationHours] - 8.5, 2) else 0.0
     ```
   * Set type to **Decimal Number (`1.2`)**.

##### B. In `Dim_Employee`:

#### 1. Converting Arabic Column Headers & Table Names to English in ONE Step:
When ingesting the master census from `employees_data_7000.txt`, all 14 attribute headers arrive in Arabic (`الرقم التعريفي`, `الاسم الكامل`, `القسم`, `الفرع`, `الراتب الأساسي`, etc.). To make your data model clean, professional, and DAX-friendly, convert them to English in **one single step**:

* **Method A (The Instant 1-Step M Formula — Recommended)**:
  1. In the left pane, select **`Dim_Employee`**.
  2. Click the **`fx` (Insert Step)** button next to the Formula Bar (or open **Home > Advanced Editor**).
  3. Paste the following one-line expression:
  ```powerquery
  #"Renamed Columns to English" = Table.RenameColumns(#"PreviousStepName", {
      {"الرقم التعريفي", "EmployeeID"},
      {"الاسم الكامل", "FullName"},
      {"العمر", "Age"},
      {"الجنس", "Gender"},
      {"المسمى الوظيفي", "JobTitle"},
      {"القسم", "Department"},
      {"الفرع", "Branch"},
      {"تاريخ التعيين", "HireDate"},
      {"الراتب الأساسي", "BaseSalary_EGP"},
      {"العملة", "Currency"},
      {"نوع عقد العمل", "ContractType"},
      {"تقييم الأداء السنوي", "PerformanceRating"},
      {"الحالة الوظيفية", "EmploymentStatus"},
      {"البريد الإلكتروني", "Email"}
  }, MissingField.Ignore)
  ```
  *(Replace `#"PreviousStepName"` with the name of your preceding step, e.g. `Source` or `#"Changed Type"`).*

* **Method B (Visual GUI Clickpath)**:
  * In the table preview, double-click the column header **`الرقم التعريفي`** $\to$ type `EmployeeID` $\to$ press `Enter`.
  * Continue double-clicking each remaining header in sequence:
    * `الاسم الكامل` $\to$ `FullName`
    * `العمر` $\to$ `Age`
    * `الجنس` $\to$ `Gender`
    * `المسمى الوظيفي` $\to$ `JobTitle`
    * `القسم` $\to$ `Department`
    * `الفرع` $\to$ `Branch`
    * `تاريخ التعيين` $\to$ `HireDate`
    * `الراتب الأساسي` $\to$ `BaseSalary_EGP`
    * `العملة` $\to$ `Currency`
    * `نوع عقد العمل` $\to$ `ContractType`
    * `تقييم الأداء السنوي` $\to$ `PerformanceRating`
    * `الحالة الوظيفية` $\to$ `EmploymentStatus`
    * `البريد الإلكتروني` $\to$ `Email`
  * *Power Query automatically bundles all 14 sequential column renames into **a single `Renamed Columns` step** in your **Applied Steps** pane!*

* **Renaming Query/Table Names in the Queries Pane**:
  * If your query was loaded with an Arabic name like `الموظفين` or `بيانات_الموظفين`:
    * Right-click the query in the left **Queries** pane $\to$ select **Rename** $\to$ type **`Dim_Employee`** $\to$ press `Enter`.

---

#### 2. Visual GUI Enrichment Suite for `Dim_Employee`:
Enrich the master employee dimension with strategic demographic, compensation, and talent lifecycle attributes using the Power Query ribbon:

1. **Compensation Tier (`SalaryBand`)**:
   * Go to **Add Column > Conditional Column**.
   * **Column Name**: `SalaryBand`
   * Rules:
     * If `BaseSalary_EGP` is less than `5000` then `Entry (< 5K)`
     * Else If `BaseSalary_EGP` is less than or equal to `10000` then `Junior (5K–10K)`
     * Else If `BaseSalary_EGP` is less than or equal to `20000` then `Mid-Level (10K–20K)`
     * Else If `BaseSalary_EGP` is less than or equal to `35000` then `Senior (20K–35K)`
     * Else `Executive (35K+)`
   * Click **OK** $\to$ set data type to **Text (`ABC`)**.

2. **Age Demographics Tier (`AgeBand`)**:
   * Go to **Add Column > Conditional Column**.
   * **Column Name**: `AgeBand`
   * Rules:
     * If `Age` is less than `25` then `Young Talent (<25)`
     * Else If `Age` is less than or equal to `35` then `Early Career (25–35)`
     * Else If `Age` is less than or equal to `50` then `Mid Career (36–50)`
     * Else `Pre-Retirement (50+)`
   * Click **OK** $\to$ set data type to **Text (`ABC`)**.

3. **Continuous Service Tenure in Years (`TenureYears`)**:
   * Go to **Add Column > Custom Column**.
   * **Column Name**: `TenureYears`
   * **Formula**:
     ```powerquery
     Number.Round(Duration.Days(DateTime.Date(DateTime.LocalNow()) - [HireDate]) / 365.25, 1)
     ```
   * Click **OK** $\to$ set data type to **Decimal Number (`1.2`)**.

4. **Tenure Experience Cohort (`TenureBand`)**:
   * Go to **Add Column > Conditional Column**.
   * **Column Name**: `TenureBand`
   * Rules:
     * If `TenureYears` is less than `1` then `< 1 Year (Onboarding)`
     * Else If `TenureYears` is less than or equal to `3` then `1–3 Years (Established)`
     * Else If `TenureYears` is less than or equal to `5` then `3–5 Years (Tenured)`
     * Else `5+ Years (Veteran)`
   * Click **OK** $\to$ set data type to **Text (`ABC`)**.

5. **Flight Risk Composite Index (`FlightRiskIndex`)**:
   Identifies high-performing employees experiencing salary compression who are vulnerable to attrition:
   * Go to **Add Column > Custom Column**.
   * **Column Name**: `FlightRiskIndex`
   * **Formula**:
     ```powerquery
     if [PerformanceRating] >= 4.0 and ([SalaryBand] = "Entry (< 5K)" or [SalaryBand] = "Junior (5K–10K)") then "🔴 Critical Risk (High Talent, Low Comp)"
     else if [TenureYears] > 4.0 and [SalaryBand] = "Junior (5K–10K)" then "🟡 Moderate Risk (Tenured Compression)"
     else "🟢 Retained & Stable"
     ```
   * Click **OK** $\to$ set data type to **Text (`ABC`)**.

6. **Retirement Succession Planning Proximity (`RetirementProximity`)**:
   * Go to **Add Column > Conditional Column**.
   * **Column Name**: `RetirementProximity`
   * Rules:
     * If `AgeBand` equals `Pre-Retirement (50+)` then `Succession Planning Required (< 5 Years)`
     * Else `Normal Horizon`
   * Click **OK** $\to$ set data type to **Text (`ABC`)**.

7. **Talent Mobility & Promotion Eligibility (`PromotionEligibility`)**:
   * Go to **Add Column > Custom Column**.
   * **Column Name**: `PromotionEligibility`
   * **Formula**:
     ```powerquery
     if [PerformanceRating] >= 4.0 and [TenureYears] >= 2.0 then "⭐ Ready for Promotion"
     else if [PerformanceRating] >= 3.5 then "📈 Developing in Role"
     else "🔄 Retain / Standard Progression"
     ```
   * Click **OK** $\to$ set data type to **Text (`ABC`)**.

---

#### 3. Connecting `Dim_CurrencyRates` to Fact Tables via GUI:
To enable real-time multi-currency conversion (EGP, USD, EUR, SAR, AED, GBP) across payroll, training costs, and department budgets, join `Dim_CurrencyRates` to your fact tables:

##### Step 1: Add Foreign Key `CurrencyKey` to Fact Tables:
Since the master payroll in `Fact_WorkforceSnapshot` and department budgets in `Fact_DepartmentBudget` are denominated in base currency (`EGP`):

* **Method A (Instant Custom Column)**:
  1. Select **`Fact_WorkforceSnapshot`** in the left pane.
  2. Go to **Add Column > Custom Column** $\to$ Name: `CurrencyKey` $\to$ Formula: `1` *(matches `CurrencyKey = 1` for `EGP` in `Dim_CurrencyRates`)*.
  3. Set data type to **Whole Number (`123`)**.
  4. Repeat the exact same step on **`Fact_DepartmentBudget`**.

* **Method B (Dynamic Merge Queries via GUI)**:
  1. Select **`Fact_WorkforceSnapshot`** $\to$ go to **Home > Merge Queries**.
  2. In the top table, select column **`Currency`**.
  3. In the bottom dropdown, select **`Dim_CurrencyRates`** $\to$ select column **`CurrencyCode`**.
  4. Join Kind: **Left Outer (all from first, matching from second)** $\to$ click **OK**.
  5. In the merged column header, click the **Expand icon (`↔`)** $\to$ check only **`CurrencyKey`** $\to$ uncheck *Use original column name as prefix* $\to$ click **OK**.
  6. Set data type to **Whole Number (`123`)**.

##### Step 2: Configure Relationships in Power BI Model View:
After clicking **Close & Apply**, switch to **Model View**:
1. Drag **`Dim_CurrencyRates[CurrencyKey]`** onto **`Fact_WorkforceSnapshot[CurrencyKey]`**.
   * Cardinality: **Many to one (`*:1`)** (`Fact_WorkforceSnapshot` $\to$ `Dim_CurrencyRates`).
   * Cross-filter direction: **Single**.
2. Drag **`Dim_CurrencyRates[CurrencyKey]`** onto **`Fact_DepartmentBudget[CurrencyKey]`**.
   * Cardinality: **Many to one (`*:1`)** (`Fact_DepartmentBudget` $\to$ `Dim_CurrencyRates`).
   * Cross-filter direction: **Single**.

##### Step 3: Dynamic Multi-Currency DAX Measures:
Add these measures to `_Measures` to let executives toggle any report currency via a slicer on `Dim_CurrencyRates[CurrencyCode]`:
```dax
// Dynamically converts total base payroll into the user-selected currency
Total Payroll (Selected Currency) = 
SUMX(
    'Fact_WorkforceSnapshot',
    'Fact_WorkforceSnapshot'[BaseSalary_EGP] * RELATED('Dim_CurrencyRates'[OneEGPInCurrency])
)

// Dynamically converts department budget into the user-selected currency
Total Budget (Selected Currency) = 
SUMX(
    'Fact_DepartmentBudget',
    'Fact_DepartmentBudget'[AllocatedBudget_EGP] * RELATED('Dim_CurrencyRates'[OneEGPInCurrency])
)
```

---

#### 4. Enterprise Power Query M Performance Enhancements:
To optimize memory footprint and refresh performance when dealing with tens of thousands of IoT attendance swipes, training records, and monthly snapshots:

1. **In-Memory Buffering with `Table.Buffer()` for Every Table Joined to `Dim_Employee`**:
   When joining dimension tables into large fact tables via `Table.NestedJoin`, Power Query re-evaluates the dimension query for each partition. Wrapping conformed dimensions in `Table.Buffer()` pins them in RAM, accelerating merges by up to **300%**!

   Below is the complete, drop-in production M code for each table in your model that joins to or derives from `Dim_Employee`:

   ##### Table A: `Fact_DailyAttendance` (Buffers `Dim_Employee` for Fast `EmployeeKey` Lookup)
   ```powerquery
   let
       Source = attendance_badge_logs,
       #"Fixed CheckOutTime" = Table.AddColumn(Source, "CleanCheckOutTime", each if [CheckOutTime] <> null then [CheckOutTime] else if [CheckInTime] <> null then Time.From(DateTime.From([CheckInTime]) + #duration(0, 8, 0, 0)) else null, Time.Type),
       #"Added DurationHours" = Table.AddColumn(#"Fixed CheckOutTime", "DurationHours", each if [CheckInTime] = null or [CleanCheckOutTime] = null then 0.0 else if [CleanCheckOutTime] >= [CheckInTime] then Duration.TotalHours([CleanCheckOutTime] - [CheckInTime]) else Duration.TotalHours((#time(23, 59, 59) - [CheckInTime]) + ([CleanCheckOutTime] - #time(0, 0, 0))) + (1 / 3600), Decimal.Type),
       #"Removed Columns" = Table.RemoveColumns(#"Added DurationHours",{"CheckOutTime"}),
       #"Renamed Columns" = Table.RenameColumns(#"Removed Columns",{{"CleanCheckOutTime", "CheckOutTime"}}),
       #"Reordered Columns" = Table.ReorderColumns(#"Renamed Columns",{"EmployeeID", "AccessDate", "CheckInTime", "CheckOutTime", "DurationHours", "BuildingID", "DeclaredWorkMode"}),
       #"Added ActualWorkMode" = Table.AddColumn(#"Reordered Columns", "ActualWorkMode", each if [BuildingID] = "REMOTE_GATE" then "Remote" else "On-site", type text),
       #"Added AccessDateKey" = Table.AddColumn(#"Added ActualWorkMode", "AccessDateKey", each Date.Year([AccessDate]) * 10000 + Date.Month([AccessDate]) * 100 + Date.Day([AccessDate]), Int64.Type),
       #"Added AttendanceKey" = Table.AddIndexColumn(#"Added AccessDateKey", "AttendanceKey", 1, 1, Int64.Type),
       #"Reordered Columns1" = Table.ReorderColumns(#"Added AttendanceKey",{"AccessDateKey", "AttendanceKey", "EmployeeID", "AccessDate", "CheckInTime", "CheckOutTime", "DurationHours", "BuildingID", "DeclaredWorkMode", "ActualWorkMode"}),
       
       // ⭐ Enterprise In-Memory Buffer: Pins Dim_Employee key pair in RAM
       BufferedDimEmployee = Table.Buffer(Table.SelectColumns(Dim_Employee, {"EmployeeID", "EmployeeKey"})),
       #"Merged Queries" = Table.NestedJoin(#"Reordered Columns1", {"EmployeeID"}, BufferedDimEmployee, {"EmployeeID"}, "Dim_Employee", JoinKind.LeftOuter),
       #"Expanded Dim_Employee" = Table.ExpandTableColumn(#"Merged Queries", "Dim_Employee", {"EmployeeKey"}, {"EmployeeKey"}),
       
       #"Reordered Columns2" = Table.ReorderColumns(#"Expanded Dim_Employee",{"AccessDateKey", "AttendanceKey", "EmployeeKey", "EmployeeID", "AccessDate", "CheckInTime", "CheckOutTime", "DurationHours", "BuildingID", "DeclaredWorkMode", "ActualWorkMode"}),
       #"Removed Columns1" = Table.RemoveColumns(#"Reordered Columns2",{"EmployeeID"}),
       #"Added BranchKey" = Table.AddColumn(#"Removed Columns1", "BranchKey", each if Text.StartsWith([BuildingID], "BLD-") then Value.FromText(Text.End([BuildingID], 3)) else null),
       #"Changed Type" = Table.TransformColumnTypes(#"Added BranchKey",{{"BranchKey", Int64.Type}}),
       #"Reordered Columns3" = Table.ReorderColumns(#"Changed Type",{"AccessDateKey", "AttendanceKey", "EmployeeKey", "BranchKey", "AccessDate", "CheckInTime", "CheckOutTime", "DurationHours", "BuildingID", "DeclaredWorkMode", "ActualWorkMode"}),
       #"Added IsTardyArrival" = Table.AddColumn(#"Reordered Columns3", "IsTardyArrival", each if [CheckInTime] <> null and [CheckInTime] > #time(9, 15, 0) then 1 else 0),
       #"Changed Type1" = Table.TransformColumnTypes(#"Added IsTardyArrival",{{"IsTardyArrival", type logical}}),
       #"Added OvertimeHours" = Table.AddColumn(#"Changed Type1", "OvertimeHours", each if [DurationHours] > 8.5 then Number.Round([DurationHours] - 8.5, 2) else 0.0, Decimal.Type)
   in
       #"Added OvertimeHours"
   ```

   ##### Table B: `Fact_TrainingCompletions` (Buffers `Dim_Employee` and `Dim_Course`)
   ```powerquery
   let
       Source = lms_course_completions,
       #"Changed Type" = Table.TransformColumnTypes(Source,{{"CertificationCost_EGP", Currency.Type}}),
       #"Added IsPassed" = Table.AddColumn(#"Changed Type", "IsPassed", each if [Score] >= 70 then 1 else 0),
       #"Changed Type1" = Table.TransformColumnTypes(#"Added IsPassed",{{"IsPassed", type logical}}),
       #"Added ScoreTier" = Table.AddColumn(#"Changed Type1", "ScoreTier", each if [Score] >= 90 then "⭐ Distinction (90-100)" else if [Score] >= 70 then "🟢 Proficient Pass (70-89)" else "🔴 Remediation Required (< 70)", type text),
       #"Added CompletionDateKey" = Table.AddColumn(#"Added ScoreTier", "CompletionDateKey", each Date.Year([CompletionDate]) * 10000 + Date.Month([CompletionDate]) * 100 + Date.Day([CompletionDate]), Int64.Type),
       #"Reordered Columns" = Table.ReorderColumns(#"Added CompletionDateKey",{"CompletionDateKey", "EmployeeID", "CourseID", "CourseName", "SkillDomain", "CompletionDate", "Score", "CertificationCost_EGP", "IsPassed", "ScoreTier"}),
       #"Added CompletionKey" = Table.AddIndexColumn(#"Reordered Columns", "CompletionKey", 1, 1, Int64.Type),
       #"Reordered Columns1" = Table.ReorderColumns(#"Added CompletionKey",{"CompletionKey", "CompletionDateKey", "EmployeeID", "CourseID", "CourseName", "SkillDomain", "CompletionDate", "Score", "CertificationCost_EGP", "IsPassed", "ScoreTier"}),
       
       // ⭐ Enterprise In-Memory Buffer: Pins Dim_Employee in RAM
       BufferedDimEmployee = Table.Buffer(Table.SelectColumns(Dim_Employee, {"EmployeeID", "EmployeeKey"})),
       #"Merged Queries" = Table.NestedJoin(#"Reordered Columns1", {"EmployeeID"}, BufferedDimEmployee, {"EmployeeID"}, "Dim_Employee", JoinKind.LeftOuter),
       #"Expanded Dim_Employee" = Table.ExpandTableColumn(#"Merged Queries", "Dim_Employee", {"EmployeeKey"}, {"EmployeeKey"}),
       
       #"Reordered Columns2" = Table.ReorderColumns(#"Expanded Dim_Employee",{"CompletionKey", "CompletionDateKey", "EmployeeKey", "EmployeeID", "CourseID", "CourseName", "SkillDomain", "CompletionDate", "Score", "CertificationCost_EGP", "IsPassed", "ScoreTier"}),
       #"Removed Columns" = Table.RemoveColumns(#"Reordered Columns2",{"EmployeeID"}),
       
       // ⭐ Enterprise In-Memory Buffer: Pins Dim_Course in RAM
       BufferedDimCourse = Table.Buffer(Table.SelectColumns(Dim_Course, {"CourseID", "CourseKey"})),
       #"Merged Queries1" = Table.NestedJoin(#"Removed Columns", {"CourseID"}, BufferedDimCourse, {"CourseID"}, "Dim_Course", JoinKind.LeftOuter),
       #"Expanded Dim_Course" = Table.ExpandTableColumn(#"Merged Queries1", "Dim_Course", {"CourseKey"}, {"CourseKey"}),
       
       #"Reordered Columns3" = Table.ReorderColumns(#"Expanded Dim_Course",{"CompletionKey", "CompletionDateKey", "EmployeeKey", "CourseKey", "CourseID", "CourseName", "SkillDomain", "CompletionDate", "Score", "CertificationCost_EGP", "IsPassed", "ScoreTier"}),
       #"Removed Columns1" = Table.RemoveColumns(#"Reordered Columns3",{"CourseID", "CourseName", "SkillDomain"})
   in
       #"Removed Columns1"
   ```

   ##### Table C: `Fact_WorkforceSnapshot` (Buffers `Dim_Employee` Source & Conformed Lookup Dimensions)
   ```powerquery
   let
       // ⭐ Enterprise In-Memory Buffer: Pins master Dim_Employee in RAM before list expansion
       Source = Table.Buffer(Dim_Employee),
       #"Removed Other Columns" = Table.SelectColumns(Source,{"EmployeeKey", "EmployeeID", "Department", "Branch", "HireDate", "BaseSalary_EGP", "Currency", "PerformanceRating", "EmploymentStatus"}),
       #"Added MonthOffset" = Table.AddColumn(#"Removed Other Columns", "MonthOffset", each {0..2}),
       #"Expanded MonthOffset" = Table.ExpandListColumn(#"Added MonthOffset", "MonthOffset"),
       #"Added SnapshotDateKey" = Table.AddColumn(#"Expanded MonthOffset", "SnapshotDateKey", each let
            Today = DateTime.Date(DateTime.LocalNow()),
            SnapshotDate = Date.EndOfMonth(Date.AddMonths(Today, - [MonthOffset]))
        in
            Date.Year(SnapshotDate) * 10000 + Date.Month(SnapshotDate) * 100 + Date.Day(SnapshotDate)),
       #"Changed Type" = Table.TransformColumnTypes(#"Added SnapshotDateKey",{{"SnapshotDateKey", Int64.Type}}),
       #"Added TenureYears" = Table.AddColumn(#"Changed Type", "TenureYears", each let
            Today = DateTime.Date(DateTime.LocalNow()),
            SnapshotDate = Date.EndOfMonth(Date.AddMonths(Today, - [MonthOffset])),
            HireDate = DateTime.Date([HireDate])
        in
            Number.Round(Duration.TotalDays(SnapshotDate - HireDate) / 365.25, 2)),
       #"Changed Type1" = Table.TransformColumnTypes(#"Added TenureYears",{{"TenureYears", type number}}),
       #"Added TenureMonths" = Table.AddColumn(#"Changed Type1", "TenureMonths", each let
            Today = DateTime.Date(DateTime.LocalNow()),
            SnapshotDate = Date.EndOfMonth(Date.AddMonths(Today, - [MonthOffset])),
            HireDate = DateTime.Date([HireDate])
        in
            Number.IntegerDivide(Duration.TotalDays(SnapshotDate - HireDate), 30.4375)),
       #"Changed Type2" = Table.TransformColumnTypes(#"Added TenureMonths",{{"TenureMonths", Int64.Type}}),
       #"Added SnapshotKey" = Table.AddIndexColumn(#"Changed Type2", "SnapshotKey", 1, 1, Int64.Type),
       #"Removed Columns" = Table.RemoveColumns(#"Added SnapshotKey",{"MonthOffset"}),

       // ⭐ Enterprise In-Memory Buffering: Pins Dim_Department, Dim_Branch, and Dim_CurrencyRates
       BufferedDimDepartment = Table.Buffer(Table.SelectColumns(Dim_Department, {"DepartmentKey", "DepartmentName"})),
       #"Merged Queries" = Table.NestedJoin(#"Removed Columns", {"Department"}, BufferedDimDepartment, {"DepartmentName"}, "Dim_Department", JoinKind.LeftOuter),
       #"Expanded Dim_Department" = Table.ExpandTableColumn(#"Merged Queries", "Dim_Department", {"DepartmentKey"}, {"DepartmentKey"}),

       BufferedDimBranch = Table.Buffer(Table.SelectColumns(Dim_Branch, {"BranchKey", "BranchName"})),
       #"Merged Queries1" = Table.NestedJoin(#"Expanded Dim_Department", {"Branch"}, BufferedDimBranch, {"BranchName"}, "Dim_Branch", JoinKind.LeftOuter),
       #"Expanded Dim_Branch" = Table.ExpandTableColumn(#"Merged Queries1", "Dim_Branch", {"BranchKey"}, {"BranchKey"}),

       #"Reordered Columns" = Table.ReorderColumns(#"Expanded Dim_Branch",{"SnapshotKey", "DepartmentKey", "BranchKey", "EmployeeKey", "EmployeeID", "Department", "Branch", "HireDate", "BaseSalary_EGP", "Currency", "PerformanceRating", "EmploymentStatus", "SnapshotDateKey", "TenureYears", "TenureMonths"}),
       #"Removed Columns1" = Table.RemoveColumns(#"Reordered Columns",{"EmployeeID", "Department", "Branch"}),
       #"Reordered Columns1" = Table.ReorderColumns(#"Removed Columns1",{"SnapshotKey", "DepartmentKey", "BranchKey", "EmployeeKey", "SnapshotDateKey", "HireDate", "BaseSalary_EGP", "Currency", "PerformanceRating", "EmploymentStatus", "TenureYears", "TenureMonths"}),

       BufferedDimCurrencyRates = Table.Buffer(Table.SelectColumns(Dim_CurrencyRates, {"CurrencyKey", "CurrencyCode"})),
       #"Merged Queries2" = Table.NestedJoin(#"Reordered Columns1", {"Currency"}, BufferedDimCurrencyRates, {"CurrencyCode"}, "Dim_CurrencyRates", JoinKind.LeftOuter),
       #"Expanded Dim_CurrencyRates" = Table.ExpandTableColumn(#"Merged Queries2", "Dim_CurrencyRates", {"CurrencyKey"}, {"CurrencyKey"}),
       #"Reordered Columns2" = Table.ReorderColumns(#"Expanded Dim_CurrencyRates",{"SnapshotKey", "DepartmentKey", "BranchKey", "EmployeeKey", "SnapshotDateKey", "CurrencyKey", "HireDate", "BaseSalary_EGP", "Currency", "PerformanceRating", "EmploymentStatus", "TenureYears", "TenureMonths"}),
       #"Removed Columns2" = Table.RemoveColumns(#"Reordered Columns2",{"Currency"})
   in
       #"Removed Columns2"
   ```

   ##### Table D: `Fact_DepartmentBudget` (Buffers `Dim_Department`, `Dim_Branch`, and `Dim_CurrencyRates`)
   ```powerquery
   let
       Source = Sql.Database(pServerName, pDatabaseName),
       #"Navigation 1" = Source{[Schema = "raw", Item = "Finance_Budget_Plan"]}[Data],
       #"Added StandardizedBranch" = Table.AddColumn(#"Navigation 1", "StandardizedBranch", each let
            Raw = Text.Trim(Text.From([CostCenter_Branch])),
            Rules = {
                {"Alex", "الإسكندرية - سموحة"}, {"سموح", "الإسكندرية - سموحة"},
                {"معاد", "القاهرة - المعادي"}, {"دقي", "الجيزة - الدقي"},
                {"الدقي", "الجيزة - الدقي"}, {"تجمع", "القاهرة - التجمع الخامس"},
                {"بورسعيد", "بورسعيد - الشرق"}, {"منصور", "الدقهلية - المنصورة"},
                {"طنطا", "الغربية - طنطا"}, {"أكتوبر", "الجيزة - 6 أكتوبر"},
                {"اكتوبر", "الجيزة - 6 أكتوبر"}, {"زايد", "الجيزة - الشيخ زايد"},
                {"أسيوط", "أسيوط - أسيوط الجديدة"}, {"اسيوط", "أسيوط - أسيوط الجديدة"},
                {"دمياط", "دمياط - دمياط الجديدة"}, {"ذكية", "القاهرة - القرية الذكية"},
                {"لوران", "الإسكندرية - لوران"}, {"مصر الجديدة", "القاهرة - مصر الجديدة"}
            },
            Match = List.First(List.Select(Rules, each Text.Contains(Raw, _{0}, Comparer.OrdinalIgnoreCase)), {null, Raw}){1}
        in
            Match),
       #"Changed Type" = Table.TransformColumnTypes(#"Added StandardizedBranch",{{"StandardizedBranch", type text}, {"Budget_EGP", Currency.Type}, {"Headcount", Int64.Type}}),
       #"Added DateKey" = Table.AddColumn(#"Changed Type", "DateKey", each if [Quarter] = "Q1" then [FiscalYear] * 10000 + 101 
   else if [Quarter] = "Q2" then [FiscalYear] * 10000 + 401 
   else if [Quarter] = "Q3" then [FiscalYear] * 10000 + 701 else [FiscalYear] * 10000 + 1001, Int64.Type),
       #"Added BudgetKey" = Table.AddIndexColumn(#"Added DateKey", "BudgetKey", 1, 1, Int64.Type),
       #"Reordered Columns" = Table.ReorderColumns(#"Added BudgetKey",{"BudgetKey", "DateKey", "Department", "CostCenter_Branch", "Quarter", "Budget_EGP", "Headcount", "FiscalYear", "StandardizedBranch"}),
       #"Removed Columns" = Table.RemoveColumns(#"Reordered Columns",{"CostCenter_Branch"}),
       #"Reordered Columns1" = Table.ReorderColumns(#"Removed Columns",{"BudgetKey", "DateKey", "Department", "StandardizedBranch", "Quarter", "Budget_EGP", "Headcount", "FiscalYear"}),

       // ⭐ Enterprise In-Memory Buffering: Pins Dim_Department and Dim_Branch
       BufferedDimDepartment = Table.Buffer(Table.SelectColumns(Dim_Department, {"DepartmentKey", "DepartmentName"})),
       #"Merged Queries" = Table.NestedJoin(#"Reordered Columns1", {"Department"}, BufferedDimDepartment, {"DepartmentName"}, "Dim_Department", JoinKind.LeftOuter),
       #"Expanded Dim_Department" = Table.ExpandTableColumn(#"Merged Queries", "Dim_Department", {"DepartmentKey"}, {"DepartmentKey"}),

       BufferedDimBranch = Table.Buffer(Table.SelectColumns(Dim_Branch, {"BranchKey", "BranchName"})),
       #"Merged Queries1" = Table.NestedJoin(#"Expanded Dim_Department", {"StandardizedBranch"}, BufferedDimBranch, {"BranchName"}, "Dim_Branch", JoinKind.LeftOuter),
       #"Expanded Dim_Branch" = Table.ExpandTableColumn(#"Merged Queries1", "Dim_Branch", {"BranchKey"}, {"BranchKey"}),

       #"Added CurrencyKey" = Table.AddColumn(#"Expanded Dim_Branch", "CurrencyKey", each 1, Int64.Type),
       #"Removed Columns1" = Table.RemoveColumns(#"Added CurrencyKey",{"Department", "StandardizedBranch"})
   in
       #"Removed Columns1"
   ```

2. **Early Column Pruning**:
   Purge unused transactional fields immediately after source ingestion via `Table.SelectColumns()` or **Remove Other Columns** in the GUI. Discarding 5 unused columns on a 100,000-row table saves megabytes of working memory during mashup execution.

3. **Strict Primitive Typing**:
   Ensure every column has an explicit type (`Int64.Type`, `Currency.Type`, `type date`, `type text`). Do not leave columns as `any` (untyped), which forces the VertiPaq engine into slower string dictionary lookups.

4. **Disable "Enable Load" on Staging Queries**:
   In the left **Queries** pane, right-click raw staging sources (`employees_data_7000`, `attendance_badge_logs`, `fpa_department_budgets`, `lms_course_completions`) and **uncheck "Enable Load"**.
   * *The result*: These raw queries remain active as transformation building blocks in Power Query, but are **excluded from the final VertiPaq tabular model**, reducing PBIX file size by over **50%** and doubling visual rendering speeds!

---

#### 5. Data Modeling Best Practices for End Users & Model Designers:
Once tables are loaded into Power BI Desktop, follow these industry-standard model governance practices:

1. **Hide Technical Foreign Keys in Report View**:
   * In **Model View**, select foreign key columns in all fact tables:
     `Fact_WorkforceSnapshot[EmployeeKey]`, `Fact_WorkforceSnapshot[DepartmentKey]`, `Fact_WorkforceSnapshot[BranchKey]`, `Fact_WorkforceSnapshot[SnapshotDateKey]`, `Fact_WorkforceSnapshot[CurrencyKey]`.
   * In the **Properties** pane, toggle **Is Hidden: On (Yes)**.
   * *Why*: Business users should only slice by clean dimension attributes (e.g. `Dim_Department[DepartmentName]`), never by raw integer surrogate keys.

2. **Set Default Summarization to "Do Not Summarize"**:
   * For all Key columns, IDs, Year numbers (`CalendarYear`, `FiscalYear`), and Age values:
     Select the column $\to$ Properties pane $\to$ **Advanced > Summarize By: None**.
   * *Why*: Prevents Power BI from mistakenly creating `Sum of EmployeeKey` or `Sum of Year` when users drag fields onto visuals.

3. **Set Sort by Column for Categorical Tiers**:
   * To prevent alphabetical sorting errors in visuals (e.g. `Q1, Q2, Q3, Q4` or `Level 1, Level 2, Level 3` or `Entry, Junior, Mid-Level`):
     * Click `Dim_Date[MonthName]` $\to$ **Column Tools > Sort by Column > `MonthNumberOfYear`**.
     * Click `Dim_Date[CalendarQuarterName]` $\to$ **Column Tools > Sort by Column > `CalendarQuarter`**.
     * Click `Dim_Course[CourseLevel]` $\to$ **Column Tools > Sort by Column > `CourseKey`** (or numeric level).

4. **Mark as Official Date Table**:
   * Right-click **`Dim_Date`** in the Data pane $\to$ select **Mark as Date Table**.
   * Date column: select **`FullDate`** $\to$ click **OK**.
   * *Why*: This disables Power BI's hidden internal auto-date/time hierarchies, saving substantial file size and enabling optimal DAX Time Intelligence execution.

---

Click **Home > Close & Apply** in Power Query Editor to commit all 6 Conformed Dimensions and 4 Galaxy Fact Tables to the tabular model!

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

### Problem 4: Upskilling Velocity, Training ROI ($\Delta P$) & Talent Flight Risk

In modern human capital management, executive leaders look beyond vanity metrics (e.g. total training hours). They demand quantifiable evidence of **Upskilling ROI**, **Competency Gain ($\Delta P$)**, and **Retention of Certified Talent**:

```dax
// 1. Total Certification Investment (EGP)
// Works seamlessly with SQL Server [Cost_EGP] or flat CSV [CertificationCost_EGP]
Total Training Investment EGP = 
IF(
    ISINSCOPE('Fact_TrainingCompletions'[Cost_EGP]),
    SUM('Fact_TrainingCompletions'[Cost_EGP]),
    SUM('Fact_TrainingCompletions'[Cost_EGP])
)

// 2. Total Completed Attempts & Unique Certified Talent
Total Course Completions = 
CALCULATE(
    COUNTROWS('Fact_TrainingCompletions'),
    'Fact_TrainingCompletions'[IsPassed] = 1
)

Certified Employee Count = 
CALCULATE(
    DISTINCTCOUNT('Fact_TrainingCompletions'[EmployeeKey]),
    'Fact_TrainingCompletions'[IsPassed] = 1
)

// 3. First-Time & Overall Examination Pass Rate %
Overall Examination Pass Rate Pct = 
DIVIDE(
    [Total Course Completions],
    COUNTROWS('Fact_TrainingCompletions'),
    0
)

// 4. Average Assessment Score
Average Examination Score = 
AVERAGE('Fact_TrainingCompletions'[Score])

// 5. Upskilling Performance Spread (Delta P: Certified vs Non-Certified Rating)
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

Performance Velocity Delta = 
[Avg Certified Performance Rating] - [Avg NonCertified Performance Rating]

// 6. Cost Per Performance Rating Point Gained (EGP)
Training Cost Per Rating Point Gain EGP = 
VAR Spread = [Performance Velocity Delta]
VAR TotalCost = [Total Training Investment EGP]
RETURN
    IF(Spread > 0, DIVIDE(TotalCost, Spread * [Certified Employee Count], BLANK()), BLANK())

// 7. Upskilling Monetary ROI % (Phillips ROI Model)
// Assumes each 1.0 rating point gain yields a conservative 5% annual productivity boost on base salary
Upskilling Monetary ROI Pct = 
VAR Spread = [Performance Velocity Delta]
VAR CertifiedPayroll = 
    CALCULATE(
        SUM('Fact_WorkforceSnapshot'[BaseSalary]) * 12,
        'Fact_WorkforceSnapshot'[EmployeeKey] IN VALUES('Fact_TrainingCompletions'[EmployeeKey])
    )
VAR EstimatedProductivityGain = CertifiedPayroll * (Spread * 0.05)
VAR TotalCost = [Total Training Investment EGP]
RETURN
    IF(TotalCost > 0, DIVIDE(EstimatedProductivityGain - TotalCost, TotalCost, 0), BLANK())

// 8. Flight Risk of Certified High Performers (Compensation Lag Diagnostic)
// Flags employees who achieved top certification scores (>=4.0 rating) but remain in Junior (<10K) salary bands
Certified Flight Risk Count = 
VAR CertifiedKeys = 
    CALCULATETABLE(
        VALUES('Fact_TrainingCompletions'[EmployeeKey]),
        'Fact_TrainingCompletions'[IsPassed] = 1
    )
RETURN
    CALCULATE(
        DISTINCTCOUNT('Dim_Employee'[EmployeeKey]),
        'Dim_Employee'[EmployeeKey] IN CertifiedKeys,
        'Dim_Employee'[SalaryBand] IN {"Entry (< 5K)", "Junior (5K–10K)"},
        'Dim_Employee'[PerformanceTier] IN {"⭐ Exceptional (Top Talent)", "🔵 High Performer"}
    )

// 9. Expired Compliance Certifications Warning Count
// Flags compliance certificates older than 12 months (365 days) that violate audit standards
Expired Compliance Certifications Count = 
VAR CutoffDate = TODAY() - 365
RETURN
    CALCULATE(
        COUNTROWS('Fact_TrainingCompletions'),
        'Dim_Course'[SkillDomain] = "Compliance",
        'Fact_TrainingCompletions'[CompletionDate] < CutoffDate,
        'Fact_TrainingCompletions'[IsPassed] = 1
    )
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

### Problem 8: Client Delivery Efficiency, Scope Overruns & Bench Cost Bleed

Offshore software consultancies sustain profitability through **high billable talent utilization** and **disciplined scope control**. When engineers sit unallocated on the "bench", their base salary represents pure operational cost bleed. When milestone deliveries experience scope overruns ($ActualHours > PlannedHours$), project profit margins collapse.

```dax
// 1. Total Billable Hours Delivered
Total Billable Hours = 
SUM('Fact_ProjectTasks'[ActualHours])

// 2. Total Contracted Planned Hours
Total Planned Hours = 
SUM('Fact_ProjectTasks'[PlannedHours])

// 3. Net Scope Overrun Hours
Scope Overrun Hours = 
VAR Overrun = [Total Billable Hours] - [Total Planned Hours]
RETURN
    IF(Overrun > 0, Overrun, 0)

// 4. Scope Overrun Rate % (Threshold: Alert when > 15%)
Scope Overrun Rate Pct = 
DIVIDE([Scope Overrun Hours], [Total Planned Hours], 0)

// 5. Delayed Milestone Delivery Rate %
Delayed Milestone Delivery Rate Pct = 
VAR DelayedTasks = CALCULATE(COUNTROWS('Fact_ProjectTasks'), 'Fact_ProjectTasks'[IsDeliveryDelayed] = TRUE())
VAR TotalTasks = COUNTROWS('Fact_ProjectTasks')
RETURN
    DIVIDE(DelayedTasks, TotalTasks, 0)

// 6. Average Client Satisfaction Score (CSAT 1.0 - 5.0)
Average Client CSAT = 
AVERAGE('Fact_ProjectTasks'[ClientSatisfactionRating])

// 7. Total Billed Client Revenue (USD)
Total Billed Revenue USD = 
SUM('Fact_ProjectTasks'[TotalBilling_USD])

// 8. Total Billed Client Revenue Converted to EGP
Total Billed Revenue EGP = 
VAR USD_SpotRate = 
    CALCULATE(
        MAX('Dim_CurrencyRates'[RateToEGP]),
        'Dim_CurrencyRates'[CurrencyCode] = "USD"
    )
RETURN
    [Total Billed Revenue USD] * COALESCE(USD_SpotRate, 48.85)

// 9. Engineering Talent Billable Utilization Rate %
// Standard consulting monthly capacity: 160 hours per active software engineer
Billable Talent Utilization Pct = 
VAR ActiveSoftwareEngineers = 
    CALCULATE(
        COUNTROWS('Dim_Employee'),
        'Dim_Employee'[Department] = "Software Engineering" || 'Dim_Employee'[Department] = "Data & AI",
        'Dim_Employee'[IsActive] = TRUE()
    )
VAR AvailableCapacityHours = ActiveSoftwareEngineers * 160
RETURN
    DIVIDE([Total Billable Hours], AvailableCapacityHours, 0)

// 10. Bench Talent Headcount (Active Technical Staff with Zero Billable Hours in Selected Period)
Bench Talent Headcount = 
CALCULATE(
    COUNTROWS('Dim_Employee'),
    'Dim_Employee'[Department] IN {"Software Engineering", "Data & AI", "Cloud Architecture", "DevOps & SRE"},
    'Dim_Employee'[IsActive] = TRUE(),
    FILTER(
        'Dim_Employee',
        CALCULATE(COUNTROWS('Fact_ProjectTasks')) = 0
    )
)

// 11. Monthly Bench Payroll Cost Bleed (EGP)
Monthly Bench Cost Bleed EGP = 
CALCULATE(
    SUM('Dim_Employee'[الراتب الأساسي]),
    'Dim_Employee'[Department] IN {"Software Engineering", "Data & AI", "Cloud Architecture", "DevOps & SRE"},
    'Dim_Employee'[IsActive] = TRUE(),
    FILTER(
        'Dim_Employee',
        CALCULATE(COUNTROWS('Fact_ProjectTasks')) = 0
    )
)
```

---

### Problem 9: Global Multi-Currency FX Realization & Offshore Margin Arbitrage

Nexora Tech Solutions negotiates client contracts in international currencies (**USD, EUR, GBP, SAR, AED**) while settling operating payroll and domestic overhead in **EGP**. This measure suite provides dynamic multi-currency reporting, allowing executives to toggle reporting currency or evaluate currency devaluation impacts.

```dax
// 1. Currently Selected Reporting Currency from Slicer
Selected Reporting Currency = 
SELECTEDVALUE('Dim_CurrencyRates'[CurrencyCode], "USD")

// 2. Dynamic Revenue Converted to Selected Slicer Currency
Dynamic Revenue Selected Currency = 
VAR TargetCurrency = [Selected Reporting Currency]
VAR TargetRateToEGP = 
    CALCULATE(
        MAX('Dim_CurrencyRates'[RateToEGP]),
        'Dim_CurrencyRates'[CurrencyCode] = TargetCurrency
    )
VAR RevenueInEGP = [Total Billed Revenue EGP]
RETURN
    DIVIDE(RevenueInEGP, TargetRateToEGP, [Total Billed Revenue USD])

// 3. Effective Hourly Client Margin (USD)
// Assumes domestic engineer hourly cost = (Monthly Salary / 160) / USD Exchange Rate
Effective Hourly Client Margin USD = 
VAR AvgEngineerSalaryEGP = AVERAGE('Dim_Employee'[الراتب الأساسي])
VAR USD_Rate = CALCULATE(MAX('Dim_CurrencyRates'[RateToEGP]), 'Dim_CurrencyRates'[CurrencyCode] = "USD")
VAR HourlyCostUSD = DIVIDE(AvgEngineerSalaryEGP, 160 * USD_Rate, 0)
VAR AvgBillableRateUSD = AVERAGE('Fact_ProjectTasks'[BillableHourlyRate_USD])
RETURN
    AvgBillableRateUSD - HourlyCostUSD

// 4. Offshore Multiplier (Revenue USD to Payroll Cost Ratio)
Offshore Revenue to Cost Multiplier = 
VAR MonthlyPayrollUSD = DIVIDE([Actual Monthly Payroll EGP], 48.85, 0)
RETURN
    DIVIDE([Total Billed Revenue USD], MonthlyPayrollUSD, 0)
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

### Step 5.6: Building Report Page 5: "Client Delivery & Bench Utilization Hub" via GUI

To manage Nexora Tech Solutions' offshore client contracts, billable engineering allocation, and project profitability, Page 5 provides executive visibility across client deliverables and talent bench overhead.

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ PAGE 5: CLIENT DELIVERY & BENCH UTILIZATION HUB (1920 x 1080)                                         │
├───────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [NAV] │ [ $1.84M Billed Rev ] [ 82.4% Utilization ] [ 7.2% Overrun ] [ 4.72 CSAT ] [ 42 On Bench ]   │
│       ├───────────────────────────────────────────────┬───────────────────────────────────────────────┤
│       │ Visual 1: Client Account Delivery Matrix      │ Visual 2: Engineering Efficiency Scatter      │
│       │ (Client, Project, Hours, Overrun Data Bars)   │ (X: Billable Hours, Y: Hourly Rate USD)       │
│       ├───────────────────────────────────────────────┼───────────────────────────────────────────────┤
│       │ Visual 3: Global Revenue by Client Country    │ Visual 4: Overdue Milestone Alert Monitor     │
│       │ (Clustered Bar: UAE, KSA, UK, US, Germany)    │ (Delayed Tasks, Assigned Dev, Overrun Hours)  │
└───────┴───────────────────────────────────────────────┴───────────────────────────────────────────────┘
```

#### 1. Page Configuration:
1. Click **`+`** to create a new page $\to$ rename to **`Client_Delivery_Hub`**.
2. Format report page $\to$ **Canvas background**: Color: `#0B0F19`, Transparency: `0%`.
3. Add Page Title: Text box $\to$ `NEXORA TECH SOLUTIONS · CLIENT DELIVERY & BENCH UTILIZATION` (Font: Segoe UI Semibold, Size: 18pt, Color: `#F9FAFB`).

#### 2. Top KPI Hero Ribbon (New Card Visual):
1. In the **Visualizations** pane, select **Card (new)**.
2. Position: X: `230 px`, Y: `80 px`, Width: `1650 px`, Height: `130 px`.
3. Drag the following measures into the **Data** well:
   * `[Total Billed Revenue USD]` $\to$ Display units: **Auto**, Format: `$#,##0`. Reference label: `[Total Billed Revenue EGP]`.
   * `[Billable Talent Utilization Pct]` $\to$ Format: `0.0%`. Callout value color: `#10B981` (Emerald).
   * `[Scope Overrun Rate Pct]` $\to$ Format: `0.0%`. Callout value color: `#F59E0B` (Amber).
   * `[Average Client CSAT]` $\to$ Format: `0.00 / 5.00`. Callout value color: `#6366F1` (Indigo).
   * `[Bench Talent Headcount]` $\to$ Reference label: `[Monthly Bench Cost Bleed EGP]`.
4. Format visual $\to$ **Cards**: Background: `#111827`, Shape: Rounded rectangle (Radius `10 px`), Border: `#1F2937` (`1 px`).

#### 3. Visual 1: Client Account Delivery Matrix:
1. Insert **Matrix visual** $\to$ Position: X: `230 px`, Y: `230 px`, Width: `810 px`, Height: `400 px`.
2. **Rows**: `Fact_ProjectTasks[ClientName]`, `Fact_ProjectTasks[ProjectName]`.
3. **Values**: `[Total Planned Hours]`, `[Total Billable Hours]`, `[Scope Overrun Rate Pct]`, `[Total Billed Revenue USD]`, `[Average Client CSAT]`.
4. Format visual $\to$ **Cell elements**:
   * Turn on **Data bars** for `[Scope Overrun Rate Pct]`: Positive bar color: `#EF4444` (Red), Axis color: `#374151`.
   * Turn on **Icons** for `[Average Client CSAT]`: Star rating thresholds (Red $< 3.5$, Yellow $3.5–4.2$, Green $\ge 4.3$).

#### 4. Visual 2: Engineering Efficiency & Rate Scatter Plot:
1. Insert **Scatter chart** $\to$ Position: X: `1060 px`, Y: `230 px`, Width: `820 px`, Height: `400 px`.
2. **X Axis**: `Fact_ProjectTasks[ActualHours]` (Summarize: Don't summarize).
3. **Y Axis**: `Fact_ProjectTasks[BillableHourlyRate_USD]`.
4. **Size**: `Fact_ProjectTasks[TotalBilling_USD]`.
5. **Legend**: `Fact_ProjectTasks[SkillDomain]`.
6. **Tooltips**: `Fact_ProjectTasks[TaskTitle]`, `Fact_ProjectTasks[ComplexityTier]`, `[Average Client CSAT]`.
7. Add reference lines:
   * Constant X line: `50 Hours` (Standard task sprint budget).
   * Constant Y line: `$80/hr` (Blended target offshore billable rate).

#### 5. Visual 3: Global Revenue by Client Country & Currency:
1. Insert **Clustered bar chart** $\to$ Position: X: `230 px`, Y: `650 px`, Width: `810 px`, Height: `380 px`.
2. **Y Axis**: `Fact_ProjectTasks[ClientCountry]`.
3. **X Axis**: `[Total Billed Revenue USD]`.
4. **Legend**: `Fact_ProjectTasks[BillingModel]` (Fixed-Price Milestone vs Time & Materials).
5. Colors: Fixed-Price (`#3B82F6` Electric Blue), T&M (`#10B981` Emerald Green).

#### 6. Visual 4: Overdue Milestone & Scope Overrun Alert Monitor:
1. Insert **Table visual** $\to$ Position: X: `1060 px`, Y: `650 px`, Width: `820 px`, Height: `380 px`.
2. Columns: `Fact_ProjectTasks[TaskID]`, `Fact_ProjectTasks[TaskTitle]`, `Fact_ProjectTasks[ProjectName]`, `Dim_Employee[FullName]`, `Fact_ProjectTasks[DeliveryDeadline]`, `[Scope Overrun Hours]`.
3. Visual filter: `Fact_ProjectTasks[IsDeliveryDelayed] = True` OR `Fact_ProjectTasks[IsHoursOverrun] = True`.
4. Style: Alternating rows `#1F2937` / `#111827`, Header font bold `#F9FAFB`.

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

- [x] **Diagnose Operational Friction**: Formulate hypotheses on Wage Inversion, Grain Collisions, Ghost Workers, Bench Cost Bleed, and Attrition Survivorship before modeling.
- [x] **Power Query Editor GUI**: Use visual clickpaths to ingest raw CSVs, extract conformed dimensions via Reference queries, impute clock-outs, unpivot wide FP&A budgets, ingest client project tasks (`Fact_ProjectTasks`), and load central bank FX spot rates (`Dim_CurrencyRates`).
- [x] **Production M Script for `Dim_Date`**: Deploy the full enterprise calendar with dynamic dataset date harvesting, Egyptian workweek rules, and relative offsets.
- [x] **Kimball Galaxy Schema (Constellation)**: Enforce 6 conformed dimensions (`Dim_Employee`, `Dim_Department`, `Dim_Branch`, `Dim_Date`, `Dim_Course`, `Dim_CurrencyRates`) filtering 5 galaxy fact tables (`Fact_WorkforceSnapshot`, `Fact_DailyAttendance`, `Fact_DepartmentBudget`, `Fact_TrainingCompletions`, `Fact_ProjectTasks`).
- [x] **Semantic Model Engineering (TMDL)**: Implement Calculation Groups, Field Parameters, RLS/OLS, in-memory `Table.Buffer()` dimension caching, and Incremental Refresh policies.
- [x] **VertiPaq Memory Optimization**: Eliminate Auto Date/Time, split DateTime into Date and Time, hide surrogate keys, and enforce column sorting.
- [x] **Advanced DAX Formulas**: Deploy 9 analytical diagnostic solutions covering salary compression, ghost workers, upskilling ROI, branch space stress, client delivery scope overruns, bench cost bleed, and multi-currency FX arbitrage.
- [x] **Kimball & Enterprise Best Practices**: Single-direction filter relationships, semi-additive snapshots, metadata row counts, and VertiPaq column splitting.
- [x] **Web App UX Design**: Build a 1920x1080 canvas across 5 modern pages (Workforce Overview, Attendance & Space Stress, FP&A Budget Variance, L&D Talent Velocity, Client Delivery & Bench Hub) with persistent sidebars, New Card visuals, wage inversion quadrant scatter plots, and 360° employee dossiers.


