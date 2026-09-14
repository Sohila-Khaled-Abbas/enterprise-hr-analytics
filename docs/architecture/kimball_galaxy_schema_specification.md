# 🌌 Technical Architecture: Kimball Galaxy Schema (Fact Constellation)
### Enterprise Data Warehouse · Conformed Dimensions · Multi-Grain Fact Tables · VertiPaq Optimization
**Organization**: Nexora Tech Solutions (Software House & L&D Academy Enterprise)

---

## 1. Architectural Overview & Design Philosophy

In modern enterprise data platforms, business processes rarely operate at a single uniform grain. An offshore software engineering house requires simultaneous analytics across:
1. **Workforce Payroll & Retention**: Monthly periodic snapshot grain (1 row / active employee / month).
2. **Physical Turnstile Telemetry**: Daily high-frequency IoT grain (1 row / employee / access day).
3. **FP&A Financial Allocations**: Quarterly cost-center quota grain (1 row / department / branch / quarter).
4. **L&D Academy Certifications**: Transactional milestone grain (1 row / certification exam attempt).
5. **Client Software Delivery**: Milestone task grain (1 row / client milestone deliverable).

Attempting to force these disparate grains into a single Star Schema produces severe **fan traps**, Cartesian products, and metric distortion (e.g., repeating quarterly budgets for every daily turnstile swipe multiplies financial totals by thousands of times).

To resolve this, Nexora Tech Solutions implements a **Kimball Galaxy Schema (Fact Constellation)** featuring **6 Shared Conformed Dimensions** filtering **5 Specialized Fact Tables** with strict single-direction filter propagation:

<div align="center">
  <a href="../assets/enterprise_galaxy_architecture.svg">
    <img src="../assets/enterprise_galaxy_architecture.png" alt="Nexora Tech Solutions Enterprise Galaxy Schema Architecture" width="100%"/>
  </a>
  <p><i>Figure 1: Kimball Galaxy Schema (Fact Constellation) featuring 6 Conformed Dimensions and 5 Specialized Analytical Fact Tables. <a href="../assets/enterprise_galaxy_architecture.svg">[View Vector SVG]</a></i></p>
</div>

---

## 2. Shared Conformed Dimensions (The Single Version of Truth)

Conformed dimensions represent standardized corporate entities shared across all business processes. Each conformed dimension uses an integer **Surrogate Key (PK)** to insulate the analytical warehouse from operational source system volatility.

### 2.1 `Dim_Employee` (Central Hub · SCD Type 2)
- **Business Purpose**: Single master catalog of all 7,000 technology employees, maintaining temporal historical fidelity (SCD Type 2).
- **Primary Source**: `data/raw/employees_data_7000.txt` (Arabic localized master feed).
- **In-Memory Caching**: Buffered in Power Query RAM via `Table.Buffer()` to accelerate merges across fact tables by $>300\%$.

| Column Name | Data Type | Key Type | Description & Business Rules |
| :--- | :--- | :--- | :--- |
| `EmployeeKey` | `INT` | Surrogate PK | Integer surrogate key (1 to 7,000+). |
| `EmployeeID` | `VARCHAR(20)` | Business Key | Natural employee identifier (`EMP-10001` through `EMP-17000`). |
| `FullName` | `NVARCHAR(150)` | Attribute | Authentic Arabic localized employee name. |
| `Age` | `INT` | Attribute | Chronological age in years. |
| `Gender` | `VARCHAR(10)` | Attribute | Biological gender (`ذكر` / `أنثى`). |
| `MaritalStatus` | `VARCHAR(20)` | Attribute | Marital status (`أعزب` / `متزوج`). |
| `JobRole` | `VARCHAR(100)` | Attribute | Professional engineering title (e.g. Senior Data Engineer, Cloud Architect). |
| `ContractType` | `VARCHAR(50)` | Attribute | Contractual working arrangement (`دوام كامل` / `هجين` / `عن بعد`). |
| `BaseSalary_EGP` | `DECIMAL(12,2)`| Attribute | Monthly base operational payroll in Egyptian Pounds. |
| `HireDate` | `DATE` | Temporal | Official corporate onboarding date. |
| `TenureYears` | `DECIMAL(5,2)` | Metric | Exact service tenure calculated as `(SnapshotDate - HireDate) / 365.25`. |
| `TenureMonths` | `INT` | Metric | Integer months of active tenure. |
| `SalaryBand` | `VARCHAR(20)` | Attribute | Categorical compensation tier (`Band 1` through `Band 5`). |
| `PerformanceTier`| `VARCHAR(30)` | Attribute | Annual appraisal performance category. |
| `FlightRiskIndex`| `VARCHAR(20)` | Diagnostic | Retention risk assessment based on market salary compression. |
| `EffectiveDate` | `DATE` | SCD2 Meta | Start date of dimensional record validity. |
| `ExpiryDate` | `DATE` | SCD2 Meta | End date of record validity (`9999-12-31` for current records). |
| `IsCurrent` | `BIT` | SCD2 Meta | Boolean flag (`1` for active valid row, `0` for superseded history). |

---

### 2.2 `Dim_Date` (Enterprise Calendar)
- **Business Purpose**: Enterprise temporal reference supporting Gregorian, Fiscal, and Egyptian regional workweek calendars.
- **Dynamic Boundary Harvesting**: Automatically bounded by harvesting the minimum and maximum operational dates across all fact tables via Power Query:
  $$\text{StartDate} = \text{Date.StartOfYear}(\text{List.Min}(\text{AllHarvestedDates}))$$
  $$\text{EndDate} = \text{Date.EndOfYear}(\text{List.Max}(\text{AllHarvestedDates}))$$

| Column Name | Data Type | Key Type | Description & Business Rules |
| :--- | :--- | :--- | :--- |
| `DateKey` | `INT` | Surrogate PK | Integer smart key formatted as `YYYYMMDD` (e.g. `20260515`). |
| `FullDate` | `DATE` | Alternate UK | Standard continuous date series. |
| `CalendarYear` | `INT` | Hierarchy | Gregorian calendar year (e.g. `2024`, `2025`, `2026`). |
| `CalendarQuarter` | `INT` | Hierarchy | Quarter number (`1`, `2`, `3`, `4`). |
| `CalendarQuarterName` | `VARCHAR(10)` | Attribute | Formatted quarter label (`Q1`, `Q2`, `Q3`, `Q4`). |
| `MonthNumberOfYear` | `INT` | Hierarchy | Numeric month index (`1` to `12`) used for strict chart sorting. |
| `MonthName` | `VARCHAR(20)` | Attribute | Full month label (`January` through `December`). |
| `DayNumberOfWeek` | `INT` | Hierarchy | Day of week index (`1` = Sunday through `7` = Saturday). |
| `DayNameOfWeek` | `VARCHAR(20)` | Attribute | Name of weekday (`Sunday`, `Monday`, etc.). |
| `IsWeekend` | `BIT` | Regional Flag | **Egyptian Workweek Standard**: `1` if Day is Friday or Saturday, `0` otherwise. |
| `IsWorkingDay` | `BIT` | Regional Flag | Inverted weekend flag accounting for corporate business days. |
| `FiscalYear` | `INT` | Financial | Corporate fiscal year. |
| `FiscalQuarter` | `VARCHAR(10)` | Financial | Corporate fiscal quarter (`FY26-Q1`). |

---

### 2.3 `Dim_Department` (Organizational Divisions)
- **Business Purpose**: Defines the 6 conformed technology and operational business units.

| DepartmentKey | DepartmentID | DepartmentName | Division | Active Tech Focus |
| :---: | :---: | :--- | :--- | :--- |
| **1** | `DEPT-001` | Software Engineering | Tech Solutions | Web, Mobile, Microservices, APIs |
| **2** | `DEPT-002` | Data & AI Engineering | Tech Solutions | Databricks, PySpark, Fabric, GenAI |
| **3** | `DEPT-003` | Cloud Architecture & DevOps | Tech Solutions | AWS, Azure, Kubernetes (CKA), CI/CD |
| **4** | `DEPT-004` | Quality Engineering & Testing | Corporate Services | Automated Cypress, Performance, ISTQB |
| **5** | `DEPT-005` | Enterprise Cybersecurity | Corporate Services | Zero-Trust, SOC2, DevSecOps, Identity |
| **6** | `DEPT-006` | Corporate Operations & Talent | Executive Office | L&D Academy, FP&A, Talent Retention |

---

### 2.4 `Dim_Branch` (Geographic Tech Delivery Hubs)
- **Business Purpose**: Encapsulates 14 localized delivery centers across Egypt, tracking physical office capacity and regional clustering.

| BranchKey | BranchID | BranchName | Region | City | Desk Capacity |
| :---: | :---: | :--- | :--- | :--- | :---: |
| **1** | `BR-001` | القاهرة - القرية الذكية | Cairo Tech Hub | 6th of October / Giza | 1,200 |
| **2** | `BR-002` | القاهرة - التجمع الخامس | Cairo Tech Hub | New Cairo | 950 |
| **3** | `BR-003` | القاهرة - المعادي | Greater Cairo | Maadi, Cairo | 800 |
| **4** | `BR-004` | القاهرة - مصر الجديدة | Greater Cairo | Heliopolis, Cairo | 600 |
| **5** | `BR-005` | الجيزة - الدقي | Greater Cairo | Dokki, Giza | 450 |
| **6** | `BR-006` | الجيزة - 6 أكتوبر | Greater Cairo | 6th of October | 500 |
| **7** | `BR-007` | الجيزة - الشيخ زايد | Greater Cairo | Sheikh Zayed | 400 |
| **8** | `BR-008` | الإسكندرية - سموحة | Coastal Hub | Alexandria | 650 |
| **9** | `BR-009` | الإسكندرية - لوران | Coastal Hub | Alexandria | 350 |
| **10** | `BR-010` | الغربية - طنطا | Delta Hub | Tanta | 300 |
| **11** | `BR-011` | الدقهلية - المنصورة | Delta Hub | Mansoura | 300 |
| **12** | `BR-012` | بورسعيد - الشرق | Canal Hub | Port Said | 250 |
| **13** | `BR-013` | دمياط - دمياط الجديدة | Canal Hub | New Damietta | 200 |
| **14** | `BR-014` | أسيوط - أسيوط الجديدة | Upper Egypt Hub | New Assiut | 350 |

---

### 2.5 `Dim_Course` (L&D Academy Certification Catalog)
- **Business Purpose**: Houses the 10 professional technical curriculum offerings across 3 progressive tiers.

| CourseKey | CourseID | CourseName | Skill Domain | Course Level | Accreditation Partner | Duration | Cost (EGP) |
| :---: | :---: | :--- | :--- | :--- | :--- | :---: | :---: |
| **1** | `CRS-101` | Cloud Foundations & Azure | Cloud | Level 1 (Foundational) | Microsoft Learn | 24 hrs | 4,500 |
| **2** | `CRS-102` | Python for Data Analytics | Data & AI | Level 1 (Foundational) | Python Institute | 32 hrs | 5,200 |
| **3** | `CRS-103` | Agile Scrum Practices | Leadership | Level 1 (Foundational) | Scrum.org | 16 hrs | 3,800 |
| **4** | `CRS-201` | AWS Solutions Architect | Cloud | Level 2 (Intermediate) | Amazon Web Services | 48 hrs | 9,500 |
| **5** | `CRS-202` | Databricks PySpark Lakehouse | Data & AI | Level 2 (Intermediate) | Databricks Academy | 60 hrs | 12,500 |
| **6** | `CRS-203` | Docker & GitHub Actions CI/CD | DevOps | Level 2 (Intermediate) | Linux Foundation | 40 hrs | 8,200 |
| **7** | `CRS-204` | Next.js Microservices | Software Eng | Level 2 (Intermediate) | Vercel / Node.js Org | 45 hrs | 8,900 |
| **8** | `CRS-301` | Kubernetes Admin (CKA) | DevOps | Level 3 (Advanced) | CNCF / Cloud Native | 75 hrs | 18,000 |
| **9** | `CRS-302` | Enterprise Fabric Architecture | Data & AI | Level 3 (Advanced) | Microsoft Fabric Alliance| 65 hrs | 16,500 |
| **10**| `CRS-303` | Zero-Trust DevSecOps | Cybersecurity | Level 3 (Advanced) | ISC2 / CISSP Partner | 80 hrs | 22,000 |

---

### 2.6 `Dim_CurrencyRates` (Multi-Currency Foreign Exchange)
- **Business Purpose**: Enables real-time currency conversion between international client invoicing (USD, EUR, GBP, SAR, AED) and domestic operational costs (EGP).

| CurrencyKey | CurrencyCode | CurrencyName | RateToEGP | OneEGPInCurrency | RateType |
| :---: | :---: | :--- | :---: | :---: | :--- |
| **1** | `EGP` | Egyptian Pound | 1.0000 | 1.000000 | Base Operational Currency |
| **2** | `USD` | United States Dollar | 48.8500 | 0.020471 | Central Bank Spot Rate |
| **3** | `EUR` | Euro | 53.2000 | 0.018797 | Central Bank Spot Rate |
| **4** | `GBP` | British Pound | 63.5000 | 0.015748 | Central Bank Spot Rate |
| **5** | `SAR` | Saudi Riyal | 13.0200 | 0.076805 | Regional Pegged Spot |
| **6** | `AED` | UAE Dirham | 13.3000 | 0.075188 | Regional Pegged Spot |

---

## 3. Galaxy Fact Constellations (Multi-Grain Fact Tables)

### 3.1 `Fact_WorkforceSnapshot` (Monthly Periodic Snapshot)
- **Grain**: Exactly 1 Row per Active Employee per Monthly Snapshot Date.
- **Foreign Keys**: `EmployeeKey`, `DepartmentKey`, `BranchKey`, `SnapshotDateKey`, `CurrencyKey`.
- **Core Metrics**: `BaseSalary_EGP`, `AnnualPerformanceRating`, `SalaryPercentileInRole`, `TenureMonths`.
- **Diagnostic Flags**: `IsSalaryCompressed` (Veteran flight risk flag when a senior earns less than market entry median).

### 3.2 `Fact_DailyAttendance` (Daily IoT Telemetry)
- **Grain**: Exactly 1 Row per Employee per Badge Access Day.
- **Foreign Keys**: `EmployeeKey`, `BranchKey`, `AccessDateKey`.
- **Core Metrics**: `CheckInTime`, `CheckOutTime`, `DurationHours`, `OvertimeHours`.
- **Diagnostic Flags**: `IsImputedClockOut` (recovered forgotten swipe), `IsTardyArrival` (arrival after 9:15 AM).

### 3.3 `Fact_DepartmentBudget` (Quarterly FP&A Run-Rate)
- **Grain**: Exactly 1 Row per Department per Branch per Fiscal Quarter.
- **Foreign Keys**: `DepartmentKey`, `BranchKey`, `DateKey` (quarter start), `CurrencyKey`.
- **Core Metrics**: `BudgetedHeadcount`, `AllocatedSalaryBudget_EGP`.
- **Multi-Grain Apportionment in DAX**:
  $$\text{Monthly Apportioned Budget} = \text{DIVIDE}(\text{SUM}(\text{Fact\_DepartmentBudget}[\text{AllocatedSalaryBudget\_EGP}]), 3)$$

### 3.4 `Fact_TrainingCompletions` (LMS Certification Attempts)
- **Grain**: Exactly 1 Row per Certification Exam Attempt.
- **Foreign Keys**: `EmployeeKey`, `CourseKey`, `CompletionDateKey`.
- **Core Metrics**: `Score` (0.0 to 100.0), `CertificationCost_EGP`.
- **Diagnostic Attributes**: `IsPassed` ($\text{Score} \ge 70$), `ScoreTier` (Distinction, Proficient, Remediation).

### 3.5 `Fact_ProjectTasks` (Client Software Delivery Milestones)
- **Grain**: Exactly 1 Row per Client Milestone Deliverable.
- **Foreign Keys**: `EmployeeKey`, `ProjectID`, `DateKey` (delivery date), `CurrencyKey`.
- **Core Metrics**: `PlannedHours`, `ActualHours`, `BillableHourlyRate_USD`, `TotalBilling_USD`, `ClientSatisfactionRating`.
- **Diagnostic Flags**: `IsHoursOverrun` (scope creep alert), `IsDeliveryDelayed`.

---

## 4. Relationship Matrix & Filter Propagation Rules

```
                      ┌──────────────────────┐
                      │     Dim_Employee     │
                      └──────────┬───────────┘
         ┌───────────────────────┼───────────────────────┬───────────────────────┐
         ▼ 1 → *                 ▼ 1 → *                 ▼ 1 → *                 ▼ 1 → *
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  Fact_Workforce  │    │   Fact_Daily     │    │  Fact_Training   │    │   Fact_Project   │
│     Snapshot     │    │   Attendance     │    │   Completions    │    │      Tasks       │
└──────────────────┘    └──────────────────┘    └──────────────────┘    └──────────────────┘
```

1. **Single-Direction Filter Propagation (`1 → *`)**: Conformed dimensions strictly filter fact tables. Bi-directional filtering is prohibited to prevent circular dependency ambiguities and visual performance penalties.
2. **Fact-to-Fact Physical Isolation**: Fact tables are never directly joined in the schema layout. Cross-fact intelligence (e.g. Budget vs Actual Payroll, or Billable Utilization vs Turnstile Attendance) is evaluated dynamically via DAX measures.
3. **Surrogate Key Integrity**: Foreign keys in all fact tables reference integer surrogate keys in conformed dimensions, ensuring zero orphaned records across the entire constellation.
4. **VertiPaq Columnar Storage**: All integer keys and categorical flags are strictly typed (`Int64.Type`, `Currency.Type`, `type logical`) to enable VertiPaq dictionary encoding and sub-second rendering.
