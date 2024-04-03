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

variable "network" {
  description = "El nombre del VPC para asociar con la instancia"
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

variable "private_ssh_key_path" {
  description = "La ruta al archivo de la llave pública SSH"
  type        = string
}

variable "target_bucket" {
  description = "La ruta al archivo de la llave pública SSH"
  type        = string
}
