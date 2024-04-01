resource "google_bigquery_dataset" "bg_dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}