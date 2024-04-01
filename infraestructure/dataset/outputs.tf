output "dataset_id" {
  value       = google_bigquery_dataset.bg_dataset.id
  description = "El ID del dataset de BigQuery creado."
}
