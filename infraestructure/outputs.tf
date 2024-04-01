output "mi_instancia_public_ip" {
  value = module.compute.instance_public_ip
}

output "mi_bucket_url" {
  value = module.storage.bucket_url
}