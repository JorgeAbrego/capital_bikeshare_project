resource "google_compute_instance" "default" {
  name         = var.instance_name
  machine_type = var.machine_type
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = var.image
    }
  }

  network_interface {
    network = var.network
    access_config {}
  }

  metadata = {
    ssh-keys = "${var.ssh_user}:${file(var.public_ssh_key_path)}",
    VAR_1 = var.target_bucket,
    VAR_2 = "capitalbike_dw"    
  }

  #metadata_startup_script = file("${path.module}/setup-docker.sh")

  connection {
        type        = "ssh"
        user        = var.ssh_user
        private_key = file(var.private_ssh_key_path)
        host        = google_compute_instance.default.network_interface[0].access_config[0].nat_ip
      }
      
  provisioner "file" {
        source      = "../deployment/"
        destination = "/home/${var.ssh_user}"
      }

  provisioner "file" {
        source      = "../keys"
        destination = "/home/${var.ssh_user}/.gcp"
      }

  provisioner "remote-exec" {
        inline = [
          "chmod 777 ./install-docker.sh",
          "./install-docker.sh"
          ]
      }
}
