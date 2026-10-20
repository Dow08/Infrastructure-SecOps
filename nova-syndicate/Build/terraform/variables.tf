# ============================================================
# Variables — AUCUN secret en valeur par défaut.
# Les valeurs sensibles viennent de terraform.tfvars (ignoré par git)
# ou des variables d'environnement TF_VAR_proxmox_api_token / TF_VAR_vm_password.
# Voir terraform.tfvars.example.
# ============================================================

variable "proxmox_endpoint" {
  description = "URL de l'API Proxmox (ex : https://192.168.1.165:8006/)"
  type        = string
  default     = "https://192.168.1.165:8006/"
}

variable "proxmox_node" {
  description = "Nom du nœud Proxmox cible"
  type        = string
  default     = "pve"
}

variable "proxmox_api_token" {
  description = "Token API Proxmox au format user@realm!tokenid=uuid — jamais en dur dans le code"
  type        = string
  sensitive   = true
}

variable "vm_password" {
  description = "Mot de passe root injecté par cloud-init dans les VMs Debian — jamais en dur dans le code"
  type        = string
  sensitive   = true
}
