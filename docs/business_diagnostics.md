# Enterprise Business Diagnostics Playbook

This playbook outlines the four primary analytical diagnostic frameworks implemented in the **Enterprise Human Capital & Operational Efficiency Diagnostics** platform.

---

## 1. Diagnostic Framework 1: Salary Compression & Flight Risk Analytics

### 1.1 The Business Problem
**Salary Compression** occurs when external market wages for new talent rise faster than internal annual merit increases. Over time, new hires (tenure $\le 1$ year) earn equal to or more than long-tenured top performers (tenure $\ge 3$ years) in the same job role.

**Business Impact**:
* High voluntary turnover among experienced institutional domain experts.
* Demoralization and loss of employee engagement.
* Exponentially higher replacement recruiting and onboarding costs.

### 1.2 Mathematical Formulation & Algorithms

#### Role Salary Percentile
For employee $i$ with salary $S_i$ in job role $R$:
$$\text{Percentile}(S_i, R) = \frac{\sum_{j \in R} \mathbb{I}(S_j < S_i)}{N_R - 1}$$

#### Salary Inversion Index (SII)
$$\text{SII}_i = \frac{\text{BaseSalary}_i}{\text{Median}(\text{BaseSalary}_{\text{NewHires}}, R)}$$
* $\text{SII}_i < 1.0 \implies$ **Salary Inversion**: The employee earns less than the market median of new hires in their role.

#### Flight Risk Priority Severity Score (1–100 Scale)
$$\text{FlightRiskScore}_i = \begin{cases}
\min\left(100, \; 50 \cdot \left(\frac{P_i}{5.0}\right) + 35 \cdot (1 - \text{Percentile}_i) + \min(15, 3 \cdot T_i)\right) & \text{if } \text{SII}_i < 1.0 \land T_i \ge 3.0 \\
25 \cdot (1 - \text{Percentile}_i) + 20 \cdot \left(\frac{P_i}{5.0}\right) & \text{otherwise}
\end{cases}$$
Where:
* $P_i$: Annual Performance Rating (1.00–5.00).
* $T_i$: Tenure in years.
* $\text{Percentile}_i$: Salary percentile in role.

### 1.3 Actionable Mitigation Strategy
* **Severity $\ge 80$ (Critical Flight Risk)**: Immediate off-cycle retention compensation adjustment to at least the 60th percentile of new-hire market rate.
* **Severity 60–79 (High Risk)**: Target for upcoming annual compensation cycle equity re-benchmarking.

---

## 2. Diagnostic Framework 2: Budget Burn Rate & Headcount Variance

### 2.1 The Business Problem
Finance & FP&A plan budgets at the **aggregated quarterly department and branch level**, whereas payroll and employee headcount operate at the **individual employee monthly level**. Fact-to-fact comparisons typically suffer from granularity mismatches and circular dependency errors in BI semantic layers.

### 2.2 Granularity Reconciliation Mechanics
The Galaxy Schema handles this through **Conformed Dimensions** (`Dim_Department`, `Dim_Branch`, `Dim_Date`):

```
Fact_WorkforceSnapshot (Monthly Grain)   Fact_DepartmentBudget (Quarterly Grain)
             │                                        │
             ▼                                        ▼
   [Sum of BaseSalary]                      [Sum of AllocatedBudget / 3]
             │                                        │
             └───────────────────┬────────────────────┘
                                 │
                       [Payroll Burn Rate %]
```

### 2.3 Key Operational Metrics
1. **Headcount Variance**:
   $$\Delta \text{HC} = \text{Actual Active Headcount} - \text{Budgeted Target Headcount}$$
2. **Payroll Burn Rate %**:
   $$\text{BurnRate\%} = \frac{\sum \text{Fact\_WorkforceSnapshot}[\text{BaseSalary}]}{\frac{1}{3} \sum \text{Fact\_DepartmentBudget}[\text{AllocatedSalaryBudget\_EGP}]}$$
   * $\text{BurnRate\%} > 105\% \implies$ Over-budget red alert (overtime or unbudgeted hiring).
   * $\text{BurnRate\%} < 90\% \implies$ Understaffed operational risk (hiring pipeline stagnation).

---

## 3. Diagnostic Framework 3: Workplace Policy Compliance & Ghost Worker Auditing

### 3.1 The Business Problem
Organizations operating under hybrid or onsite policies face operational friction:
1. **Contract Violations**: Employees contracted under `دوام كامل (حضوري)` who log more than 60% remote days, or hybrid employees failing branch desk quotas.
2. **Ghost Workers**: Deceased, resigned, or unmonitored employees who remain active on the payroll system, generating monthly salary disbursements despite producing zero physical turnstile or system badge access.

### 3.2 Detection Algorithms

#### Physical Presence Rate %
$$\text{PresenceRate\%} = \frac{\sum \mathbb{I}(\text{ActualWorkMode} = \text{'On-site'})}{\text{Total Access Days In Period}}$$

#### Policy Breach Classification
$$\text{IsViolation} = \begin{cases}
1 & \text{if Contract} = \text{'دوام كامل (حضوري)'} \land \text{ActualWorkMode} = \text{'Remote'} \\
1 & \text{if Contract} = \text{'هجين'} \land \text{WeeklyOnsiteDays} < 2 \\
0 & \text{otherwise}
\end{cases}$$

#### Ghost Worker Audit Rule
$$\text{GhostWorker} = 1 \iff (\text{EmploymentStatus} = \text{'Active'}) \land (\text{DaysSinceLastBadgeAccess} > 60)$$

### 3.3 Business Recovery Protocol
* **Ghost Worker Alert**: Triggers immediate automated payroll disbursement freeze pending HR physical audit verification.
* **Chronic Remote Breach**: Flags manager review in performance appraisals.

---

## 4. Diagnostic Framework 4: Upskilling ROI & Performance Score Velocity

### 4.1 The Business Problem
Enterprises spend millions on learning and development (L&D) certifications without empirical measurement of whether skill acquisition translates into enhanced operational performance.

### 4.2 Analytical Metrics

#### Performance Score Velocity ($\Delta P$)
Compares performance ratings of certified staff versus uncertified peers controlling for tenure and job role:
$$\Delta P = \bar{P}_{\text{Certified}} - \bar{P}_{\text{Non-Certified}}$$

#### Training Efficiency Index (TEI)
Measures performance rating increment per 10,000 EGP of training investment:
$$\text{TEI} = \frac{\Delta P}{\sum \text{CertificationCost\_EGP} / 10,000}$$

### 4.3 Strategic Application
* Identify high-ROI skill domains (e.g. `Tech` vs `Compliance`) to optimize future L&D budget allocations.
* Track individual employee post-certification velocity to prioritize promotion and succession planning pipelines.
