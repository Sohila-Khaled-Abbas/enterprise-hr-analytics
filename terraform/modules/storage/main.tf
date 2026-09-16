# =============================================================================
# Storage Module: Azure Data Lake Storage Gen2 Containers (Raw & Processed)
# =============================================================================

resource "azurerm_storage_account" "sa" {
  name                     = var.storage_account_name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = var.account_tier
  account_replication_type = var.account_replication_type
  account_kind             = "StorageV2"
  is_hns_enabled           = true # Enables Hierarchical Namespace (ADLS Gen2)
  min_tls_version          = "TLS1_2"

  tags = {
    Project   = "Enterprise-HR-Analytics"
    ManagedBy = "Terraform"
  }
}

# Raw Zone Container (Bronze)
resource "azurerm_storage_data_lake_gen2_filesystem" "raw" {
  name               = "raw"
  storage_account_id = azurerm_storage_account.sa.id
}

# Processed Zone Container (Silver & Gold)
resource "azurerm_storage_data_lake_gen2_filesystem" "processed" {
  name               = "processed"
  storage_account_id = azurerm_storage_account.sa.id
}
