variable "storage_account_name" {
  type        = string
  description = "Storage account name (lowercase, alphanumeric, 3-24 chars)"
}

variable "resource_group_name" {
  type        = string
  description = "Parent resource group"
}

variable "location" {
  type        = string
  description = "Azure region"
}

variable "account_tier" {
  type    = string
  default = "Standard"
}

variable "account_replication_type" {
  type    = string
  default = "LRS"
}
