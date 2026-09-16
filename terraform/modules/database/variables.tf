variable "server_name" {
  type        = string
  description = "Azure SQL Server name"
}

variable "resource_group_name" {
  type        = string
  description = "Parent resource group"
}

variable "location" {
  type        = string
  description = "Azure region"
}

variable "admin_username" {
  type        = string
  description = "Admin user"
}

variable "admin_password" {
  type        = string
  description = "Admin password"
  sensitive   = true
}

variable "database_name" {
  type        = string
  description = "Database name"
  default     = "EnterpriseHR_DWH"
}

variable "sku_name" {
  type        = string
  description = "Database compute SKU"
  default     = "GP_Gen5_2"
}
