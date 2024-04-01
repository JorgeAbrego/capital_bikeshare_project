variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  type    = string
  default = "capitalbike_dw"
}

variable "location" {
  description = "Location of BigQuery Dataset"
  type    = string
  default = "US"
}