# =============================================================================
# Database Module: Azure SQL Server and EnterpriseHR_DWH Database
# =============================================================================

resource "azurerm_mssql_server" "sql_server" {
  name                         = var.server_name
  resource_group_name          = var.resource_group_name
  location                     = var.location
  version                      = "12.0"
  administrator_login          = var.admin_username
  administrator_login_password = var.admin_password
  minimum_tls_version          = "1.2"

  tags = {
    Project     = "Enterprise-HR-Analytics"
    ManagedBy   = "Terraform"
  }
}

resource "azurerm_mssql_database" "dwh" {
  name           = var.database_name
  server_id      = azurerm_mssql_server.sql_server.id
  collation      = "SQL_Latin1_General_CP1_CI_AS"
  sku_name       = var.sku_name
  max_size_gb    = 100
  zone_redundant = false

  tags = {
    Project   = "Enterprise-HR-Analytics"
    ManagedBy = "Terraform"
  }
}

# Allow Azure services to access server
resource "azurerm_mssql_firewall_rule" "allow_azure_services" {
  name             = "AllowAzureServices"
  server_id        = azurerm_mssql_server.sql_server.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}
