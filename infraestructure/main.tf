module "vpc" {
  source = "./vpc"

  vpc_network_name = var.vpc_network_name
  firewall_name = var.firewall_name
}

module "dataset" {
  source = "./dataset"

  location = var.location
}

module "storage" {
  source = "./storage"
  
  datalake_bucket_name = var.datalake_bucket_name
  location = var.location
}

module "compute" {
  source = "./compute"

  instance_name = var.instance_name
  machine_type  = var.machine_type
  zone          = var.zone
  image         = var.image
  network       = module.vpc.vpc_id
  ssh_user      = var.ssh_user
  public_ssh_key_path = var.public_ssh_key_path
  private_ssh_key_path = var.private_ssh_key_path
  target_bucket = var.datalake_bucket_name
}