"""
Domain Data Models and Entities.
Strongly-typed Pydantic representations for conformed dimensions and core facts.
"""

from __future__ import annotations

from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class DepartmentEntity(BaseModel):
    """Department and Cost Center entity."""
    department_key: int = Field(alias="DepartmentKey")
    department_id: str = Field(alias="DepartmentID")
    department_name: str = Field(alias="DepartmentName")
    division: str = Field(default="Corporate Services", alias="Division")
    cost_center_code: Optional[str] = Field(default=None, alias="CostCenterCode")


class BranchEntity(BaseModel):
    """Branch office geographical entity."""
    branch_key: int = Field(alias="BranchKey")
    branch_id: str = Field(alias="BranchID")
    branch_name: str = Field(alias="BranchName")
    canonical_name: str = Field(alias="CanonicalName")
    region: str = Field(alias="Region")
    city: str = Field(alias="City")
    capacity: int = Field(default=0, alias="Capacity")


class CourseEntity(BaseModel):
    """L&D training course entity."""
    course_key: int = Field(alias="CourseKey")
    course_id: str = Field(alias="CourseID")
    course_name: str = Field(alias="CourseName")
    skill_domain: str = Field(alias="SkillDomain")
    target_competency: Optional[str] = Field(default=None, alias="TargetCompetency")
    estimated_hours: float = Field(default=0.0, alias="EstimatedHours")


class CurrencyRateEntity(BaseModel):
    """Multi-currency exchange rate entity."""
    currency_key: int = Field(alias="CurrencyKey")
    currency_code: str = Field(alias="CurrencyCode")
    currency_name: str = Field(alias="CurrencyName")
    exchange_rate_to_egp: float = Field(alias="ExchangeRateToEGP")
    effective_date: str = Field(alias="EffectiveDate")
    is_active: bool = Field(default=True, alias="IsActive")


class EmployeeEntity(BaseModel):
    """Slowly Changing Dimension Type 2 Employee Entity."""
    employee_key: int = Field(alias="EmployeeKey")
    employee_id: str = Field(alias="EmployeeID")
    full_name: str = Field(alias="FullName")
    age: Optional[int] = Field(default=None, alias="Age")
    gender: Optional[str] = Field(default=None, alias="Gender")
    job_role: str = Field(alias="JobRole")
    department_key: int = Field(alias="DepartmentKey")
    branch_key: int = Field(alias="BranchKey")
    hire_date: str = Field(alias="HireDate")
    base_salary: float = Field(alias="BaseSalary")
    currency: str = Field(default="EGP", alias="Currency")
    contract_type: str = Field(alias="ContractType")
    marital_status: Optional[str] = Field(default=None, alias="MaritalStatus")
    email: Optional[str] = Field(default=None, alias="Email")
    effective_date: str = Field(alias="EffectiveDate")
    expiry_date: str = Field(default="9999-12-31", alias="ExpiryDate")
    is_current: bool = Field(default=True, alias="IsCurrent")


class ProjectTaskEntity(BaseModel):
    """Software House billable project task delivery entity."""
    task_id: str = Field(alias="TaskID")
    project_id: str = Field(alias="ProjectID")
    project_name: str = Field(alias="ProjectName")
    client_name: str = Field(alias="ClientName")
    task_name: str = Field(alias="TaskName")
    assigned_employee_id: str = Field(alias="AssignedEmployeeID")
    start_date: str = Field(alias="StartDate")
    due_date: str = Field(alias="DueDate")
    completion_date: Optional[str] = Field(default=None, alias="CompletionDate")
    task_status: str = Field(alias="TaskStatus")
    estimated_hours: float = Field(alias="EstimatedHours")
    actual_hours: float = Field(alias="ActualHours")
    hourly_rate_usd: float = Field(alias="HourlyRateUSD")
    total_cost_usd: float = Field(alias="TotalCostUSD")
    currency_code: str = Field(default="USD", alias="CurrencyCode")
    is_overdue: bool = Field(default=False, alias="IsOverdue")
    overrun_hours: float = Field(default=0.0, alias="OverrunHours")
