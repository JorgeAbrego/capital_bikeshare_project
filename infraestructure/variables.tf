variable "credentials" {
  description = "My Credentials"
}

variable "project" {
  description = "Project"
}

variable "region" {
  description = "Region"
}

variable "location" {
  description = "Project Location"
}

variable "datalake_bucket_name" {
  description = "Data Lake bucket name"
}

variable "vpc_network_name" {
  type    = string
}

variable "firewall_name" {
  type = string
}


variable "instance_name" {
  description = "El nombre de la instancia de Compute Engine"
  type        = string
}

variable "machine_type" {
  description = "El tipo de máquina de la instancia"
  type        = string
}

variable "zone" {
  description = "La zona donde se desplegará la instancia"
  type        = string
}

variable "image" {
  description = "La imagen de sistema operativo para la instancia"
  type        = string
}

variable "ssh_user" {
  description = "El nombre de usuario para la configuración SSH"
  type        = string
}

variable "public_ssh_key_path" {
  description = "La ruta al archivo de la llave pública SSH"
  type        = string
}