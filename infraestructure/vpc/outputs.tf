output "vpc_id" {
  value       = google_compute_network.vpc_network.id
  description = "El ID del VPC creado."
}

output "firewall_id" {
  value       = google_compute_firewall.firewall.id
  description = "El ID de la regla del firewall creada."
}
