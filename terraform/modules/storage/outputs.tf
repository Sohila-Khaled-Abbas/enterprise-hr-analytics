output "storage_account_name" {
  value = azurerm_storage_account.sa.name
}

output "storage_account_id" {
  value = azurerm_storage_account.sa.id
}

output "raw_container_name" {
  value = azurerm_storage_data_lake_gen2_filesystem.raw.name
}

output "processed_container_name" {
  value = azurerm_storage_data_lake_gen2_filesystem.processed.name
}

output "primary_dfs_endpoint" {
  value = azurerm_storage_account.sa.primary_dfs_endpoint
}
