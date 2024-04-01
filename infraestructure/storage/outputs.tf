output "bucket_url" {
  value       = google_storage_bucket.datalake-bucket.url
  description = "La URL del bucket de Cloud Storage."
}
