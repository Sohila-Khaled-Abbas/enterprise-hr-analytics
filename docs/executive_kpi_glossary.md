# Enterprise Executive KPI & Operational Metric Glossary

This document establishes the official corporate KPI dictionary and mathematical diagnostic formulations for the **Enterprise Human Capital, Software House & Operational Analytics Platform**.

---

## 1. Executive Workforce & Talent Analytics

### 1.1 Active Headcount
- **Definition**: The total number of unique, fully engaged employees in the organization during the reporting cutoff period.
- **Mathematical Formula**:
  $$\text{Active Headcount} = \sum [\text{EmploymentStatus} = \text{'Active'}]$$
- **Target Threshold**: Stable headcount aligned with approved FP&A budget limits ($\pm 3\%$).

### 1.2 Salary Compression Ratio & Flag
- **Definition**: Identifies experienced engineering talent whose current base salary is near or below newer junior/intermediate cohorts within the same job role, signaling retention risk.
- **Mathematical Formula**:
  $$\text{Compression Ratio} = \frac{\text{BaseSalary}}{\text{RoleMedianSalary}} \quad \text{where} \quad \text{TenureYears} \ge 3.0 \land \text{CompaRatio} \le 0.95$$
- **Target Threshold**: $< 5.0\%$ of tenured staff compressed.

### 1.3 Flight Risk Index (FRI)
- **Definition**: Composite predictive heuristic scoring the likelihood of voluntary resignation based on tenure, performance tier, compression flag, and commute distance.
- **Mathematical Formula**:
  $$\text{FRI} = (0.35 \times \text{IsCompressed}) + (0.30 \times \text{LowCompa}) + (0.20 \times \text{HighPerformance}) + (0.15 \times \text{TenureStagnation})$$
- **Target Threshold**: Executive review triggered for all personnel scoring $\text{FRI} \ge 0.70$.

---

## 2. Daily IoT Attendance & Remote Compliance

### 2.1 Missing Clock-Out Rate (Forgotten Swipes)
- **Definition**: Percentage of daily physical or virtual shifts where the employee badged in but failed to swipe out at the end of the shift.
- **Mathematical Formula**:
  $$\text{Missing Clock-Out Rate} = \frac{\sum [\text{IsMissingClockOut} = 1]}{\text{Total Attendance Swipes}} \times 100\%$$
- **Remediation**: Heuristic median imputation (+8.0 hours from check-in time).
- **Target Threshold**: $< 3.0\%$.

### 2.2 Remote Work Adherence Violation Rate
- **Definition**: Percentage of contracted on-site personnel logging remote sessions exceeding allowable corporate policy limits (>40% monthly remote).
- **Mathematical Formula**:
  $$\text{Remote Policy Violation Rate} = \frac{\sum [\text{ContractType} = \text{'On-Site'} \land \text{ActualWorkMode} = \text{'Remote'}]}{\text{Total On-Site Shifts}} \times 100\%$$
- **Target Threshold**: $< 5.0\%$.

---

## 3. FP&A Budget & Financial Variance

### 3.1 Budget Variance (OPEX Headcount Expenditure)
- **Definition**: Net difference between approved quarterly departmental payroll budget and actual workforce payroll liability.
- **Mathematical Formula**:
  $$\text{Budget Variance (EGP)} = \text{AllocatedBudget}_{\text{EGP}} - \text{TotalPayrollLiability}_{\text{EGP}}$$
- **Interpretation**: Positive variance indicates budget surplus; negative variance indicates operational deficit.

### 3.2 Headcount Quota Burn Rate %
- **Definition**: Percentage of budgeted talent acquisition capacity utilized.
- **Mathematical Formula**:
  $$\text{Burn Rate \%} = \frac{\text{Actual Payroll (EGP)}}{\text{Allocated Budget (EGP)}} \times 100\%$$
- **Target Threshold**: $95.0\% \le \text{Burn Rate} \le 100.0\%$.

---

## 4. L&D Tech Academy & Talent Development ROI

### 4.1 Certification Pass Rate %
- **Definition**: Proportion of exam attempts meeting or exceeding the minimum passing grade (score $\ge 70$).
- **Mathematical Formula**:
  $$\text{Pass Rate \%} = \frac{\sum [\text{Score} \ge 70]}{\text{Total Exam Attempts}} \times 100\%$$
- **Target Threshold**: $\ge 85.0\%$.

### 4.2 Cost Per Certified Engineer (EGP)
- **Definition**: Average training expenditure required to produce one fully certified engineer in a specific domain (Tech, Leadership, Compliance).
- **Mathematical Formula**:
  $$\text{Cost Per Certified Engineer} = \frac{\sum \text{Tuition Investment (EGP)}}{\sum \text{Passed Certifications}}$$
- **Target Benchmark**: Tech: $\le 15,000 \text{ EGP}$; Leadership: $\le 20,000 \text{ EGP}$.

---

## 5. Software House Client Delivery & Profitability

### 5.1 Project Schedule Overrun %
- **Definition**: Percentage by which actual engineering hours exceeded the contractually scoped effort.
- **Mathematical Formula**:
  $$\text{Overrun \%} = \frac{\sum \text{ActualHours} - \sum \text{PlannedHours}}{\sum \text{PlannedHours}} \times 100\%$$
- **Target Threshold**: $< 10.0\%$ project overrun.

### 5.2 Delivery On-Time Rate %
- **Definition**: Percentage of client deliverables and milestones completed on or before contractual deadlines.
- **Mathematical Formula**:
  $$\text{On-Time Delivery \%} = \left( 1 - \frac{\sum [\text{IsDeliveryDelayed} = 1]}{\text{Total Tasks}} \right) \times 100\%$$
- **Target Threshold**: $\ge 92.0\%$.

### 5.3 Blended Effective Hourly Billing Rate (USD)
- **Definition**: Total billable revenue generated divided by the total consultant effort booked.
- **Mathematical Formula**:
  $$\text{Effective Hourly Rate} = \frac{\sum \text{TotalBilling\_USD}}{\sum \text{ActualHours}}$$
- **Target Benchmark**: Senior/Principal: $\$85 - \$120/\text{hr}$; Mid-level: $\$50 - \$75/\text{hr}$.

### 5.4 Net Project Contribution Margin
- **Definition**: Gross consulting billing minus dedicated consultant payroll and overhead expense.
- **Mathematical Formula**:
  $$\text{Margin \%} = \frac{\text{TotalBilling\_EGP} - \text{TotalConsultantPayroll\_EGP}}{\text{TotalBilling\_EGP}} \times 100\%$$
- **Target Threshold**: $\ge 45.0\%$ gross margin.
