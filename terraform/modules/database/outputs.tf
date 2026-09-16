output "server_fqdn" {
  value = azurerm_mssql_server.sql_server.fully_qualified_domain_name
}

output "server_id" {
  value = azurerm_mssql_server.sql_server.id
}

output "database_name" {
  value = azurerm_mssql_database.dwh.name
}

output "database_id" {
  value = azurerm_mssql_database.dwh.id
}
