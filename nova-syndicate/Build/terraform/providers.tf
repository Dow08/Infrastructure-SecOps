terraform {
  required_providers {
    proxmox = {
      source  = "bpg/proxmox"
      version = "~> 0.66"
    }
  }
}

# Pourquoi insecure = true ? Proxmox utilise un certificat SSL auto-signé.
# Sans ça, Terraform refuserait la connexion. En production : certificat valide et insecure = false.
provider "proxmox" {
  endpoint  = var.proxmox_endpoint
  api_token = var.proxmox_api_token
  insecure  = true
}
