# =============================================================================
# Enterprise HR Analytics - Terraform Input Variables
# =============================================================================

variable "environment" {
  type        = string
  description = "Target deployment environment (development, staging, production)"
  default     = "production"
}

variable "location" {
  type        = string
  description = "Azure primary region for data services"
  default     = "northeurope"
}

variable "resource_group_name" {
  type        = string
  description = "Name of the parent resource group"
  default     = "rg-enterprise-hr-analytics"
}

variable "sql_admin_username" {
  type        = string
  description = "Administrator username for Azure SQL DWH Server"
  default     = "sqladmin"
}

variable "sql_admin_password" {
  type        = string
  description = "Administrator password for Azure SQL DWH Server"
  sensitive   = true
}

variable "database_sku" {
  type        = string
  description = "Performance SKU for Azure SQL Database"
  default     = "GP_Gen5_2"
}

variable "storage_account_tier" {
  type        = string
  description = "Storage account performance tier"
  default     = "Standard"
}

variable "storage_account_replication" {
  type        = string
  description = "Storage redundancy level"
  default     = "LRS"
}
