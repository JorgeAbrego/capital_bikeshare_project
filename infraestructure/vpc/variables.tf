variable "vpc_network_name" {
  type = string
}

variable "firewall_name" {
  type = string
}

variable "source_ranges" {
  description = "IP range allowed to access VPC"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}