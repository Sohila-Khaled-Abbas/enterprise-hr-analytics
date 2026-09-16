# =============================================================================
# Enterprise HR Analytics - Terraform Root Configuration (IaC)
# Provisions: Azure Resource Group, Azure SQL DWH, ADLS Gen2 Data Lake
# =============================================================================

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.90.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Unique suffix for globally unique resources
resource "random_string" "suffix" {
  length  = 6
  special = false
  upper   = false
}

# Resource Group
resource "azurerm_resource_group" "rg" {
  name     = "${var.resource_group_name}-${var.environment}"
  location = var.location

  tags = {
    Environment = var.environment
    Project     = "Enterprise-HR-Analytics"
    ManagedBy   = "Terraform"
  }
}

# Database Module
module "database" {
  source              = "./modules/database"
  server_name         = "sql-enterprise-hr-${var.environment}-${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  admin_username      = var.sql_admin_username
  admin_password      = var.sql_admin_password
  database_name       = "EnterpriseHR_DWH"
  sku_name            = var.database_sku
}

# Storage Module (ADLS Gen2)
module "storage" {
  source                   = "./modules/storage"
  storage_account_name     = "stenterprisehr${var.environment}${random_string.suffix.result}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = var.storage_account_tier
  account_replication_type = var.storage_account_replication
}
