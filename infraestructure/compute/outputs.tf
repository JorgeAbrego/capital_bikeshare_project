output "instance_id" {
  value       = google_compute_instance.default.id
  description = "El ID de la instancia de Compute Engine."
}

output "instance_public_ip" {
  value       = google_compute_instance.default.network_interface[0].access_config[0].nat_ip
  description = "La dirección IP pública de la instancia de Compute Engine."
}
