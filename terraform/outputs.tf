# =============================================================================
# Enterprise HR Analytics - Terraform Outputs
# =============================================================================

output "resource_group_name" {
  description = "Provisioned resource group name"
  value       = azurerm_resource_group.rg.name
}

output "sql_server_fqdn" {
  description = "Fully qualified domain name of Azure SQL Server"
  value       = module.database.server_fqdn
}

output "database_name" {
  description = "Enterprise HR DWH Database name"
  value       = module.database.database_name
}

output "storage_account_name" {
  description = "Azure Data Lake Storage Gen2 account name"
  value       = module.storage.storage_account_name
}

output "raw_data_container" {
  description = "Raw landing data lake container"
  value       = module.storage.raw_container_name
}

output "processed_data_container" {
  description = "Processed curated data lake container"
  value       = module.storage.processed_container_name
}

output "odbc_connection_string_template" {
  description = "Template ODBC connection string for applications and Power BI"
  value       = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=${module.database.server_fqdn};DATABASE=${module.database.database_name};UID=${var.sql_admin_username};PWD=***;TrustServerCertificate=no;"
  sensitive   = false
}
