# ============================================================
# OPNsense-Lyon — Firewall principal
# 5 interfaces : WAN(vmbr0) + LAN Lyon(vmbr1) + MGMT(vmbr2)
#                + Quarantaine(vmbr4) + Collecte Wazuh(vmbr5)
# Installation manuelle depuis ISO — pas de cloud-init
# ============================================================
resource "proxmox_virtual_environment_vm" "opnsense_lyon" {
  name      = "OPNsense-Lyon"
  node_name = var.proxmox_node
  vm_id     = 100
  started   = false

  cpu {
    cores = 2
  }

  memory {
    dedicated = 2048
  }

  cdrom {
    file_id = "local:iso/OPNsense-26.1.6-vga-amd64.img"
  }

  disk {
    datastore_id = "local-lvm"
    file_format  = "raw"
    interface    = "virtio0"
    size         = 20
  }

  network_device { bridge = "vmbr0" } # WAN
  network_device { bridge = "vmbr1" } # LAN Lyon (trunk VLAN)
  network_device { bridge = "vmbr2" } # MGMT Bastion
  network_device { bridge = "vmbr4" } # Quarantaine
  network_device { bridge = "vmbr5" } # Collecte Wazuh
}

# ============================================================
# OPNsense-Marseille — Firewall site distant
# 2 interfaces : WAN(vmbr0) + LAN Marseille(vmbr3)
# Hub & Spoke : tout le trafic internet passe par Lyon via IPsec
# ============================================================
resource "proxmox_virtual_environment_vm" "opnsense_marseille" {
  name      = "OPNsense-Marseille"
  node_name = var.proxmox_node
  vm_id     = 101
  started   = false

  cpu {
    cores = 2
  }

  memory {
    dedicated = 1024
  }

  cdrom {
    file_id = "local:iso/OPNsense-26.1.6-vga-amd64.img"
  }

  disk {
    datastore_id = "local-lvm"
    file_format  = "raw"
    interface    = "virtio0"
    size         = 10
  }

  network_device { bridge = "vmbr0" } # WAN
  network_device { bridge = "vmbr3" } # LAN Marseille (trunk VLAN)
}

# ============================================================
# GROUPE DMZ — VLAN 5 (172.16.5.0/24) sur vmbr1
# Zone exposée : Proxy, Web, Honeypot
# Pas de route vers SERVERS — isolation stricte
# ============================================================
resource "proxmox_virtual_environment_vm" "proxy_01" {
  name      = "Proxy-01"
  node_name = var.proxmox_node
  vm_id     = 103
  started   = false
  clone {
    vm_id = 9000
  }

  cpu {
    cores = 1
  }

  memory {
    dedicated = 1024
  }

  disk {
    datastore_id = "local-lvm"
    interface    = "scsi0"
    size         = 20
  }

  network_device {
    bridge  = "vmbr1"
    vlan_id = 5
  }

  initialization {
    ip_config {
      ipv4 {
        address = "172.16.5.10/24"
        gateway = "172.16.5.1"
      }
    }
    user_account {
      username = "root"
      password = var.vm_password
    }
  }
}

resource "proxmox_virtual_environment_vm" "web_01" {
  name      = "Web-01"
  node_name = var.proxmox_node
  vm_id     = 104
  started   = false
  clone {
    vm_id = 9000
  }

  cpu {
    cores = 1
  }

  memory {
    dedicated = 1024
  }

  disk {
    datastore_id = "local-lvm"
    interface    = "scsi0"
    size         = 20
  }

  network_device {
    bridge  = "vmbr1"
    vlan_id = 5
  }

  initialization {
    ip_config {
      ipv4 {
        address = "172.16.5.30/24"
        gateway = "172.16.5.1"
      }
    }
    user_account {
      username = "root"
      password = var.vm_password
    }
  }
}

resource "proxmox_virtual_environment_vm" "honeypot_01" {
  name      = "Honeypot-01"
  node_name = var.proxmox_node
  vm_id     = 105
  started   = false
  clone {
    vm_id = 9000
  }

  cpu {
    cores = 1
  }

  memory {
    dedicated = 512
  }

  disk {
    datastore_id = "local-lvm"
    interface    = "scsi0"
    size         = 10
  }

  network_device {
    bridge  = "vmbr1"
    vlan_id = 5
  }

  initialization {
    ip_config {
      ipv4 {
        address = "172.16.5.40/24"
        gateway = "172.16.5.1"
      }
    }
    user_account {
      username = "root"
      password = var.vm_password
    }
  }
}

# ============================================================
# GROUPE SERVERS — VLAN 10 (172.16.10.0/24) sur vmbr1
# DC01 = cœur AD/DNS, Wazuh = SIEM double interface
# DB, File, Backup — accès restreint depuis DMZ interdit
# ============================================================
resource "proxmox_virtual_environment_vm" "dc01_lyon" {
  name      = "DC01-Lyon"
  node_name = var.proxmox_node
  vm_id     = 102
  started   = false
  clone {
    vm_id = 9000
  }

  cpu {
    cores = 2
  }

  memory {
    dedicated = 2048
  }

  disk {
    datastore_id = "local-lvm"
    interface    = "scsi0"
    size         = 30
  }

  network_device {
    bridge  = "vmbr1"
    vlan_id = 10
  }

  initialization {
    ip_config {
      ipv4 {
        address = "172.16.10.10/24"
        gateway = "172.16.10.1"
      }
    }
    user_account {
      username = "root"
      password = var.vm_password
    }
  }
}

resource "proxmox_virtual_environment_vm" "wazuh_01" {
  name      = "Wazuh-01"
  node_name = var.proxmox_node
  vm_id     = 106
  started   = false
  clone {
    vm_id = 9000
  }

  cpu {
    cores = 2
  }

  memory {
    dedicated = 4096
  }

  disk {
    datastore_id = "local-lvm"
    interface    = "scsi0"
    size         = 50
  }

  # eth0 : management SERVERS
  network_device {
    bridge  = "vmbr1"
    vlan_id = 10
  }

  # eth1 : collecte logs DMZ + Quarantaine (bridge dédié)
  network_device {
    bridge = "vmbr5"
  }

  initialization {
    ip_config {
      ipv4 {
        address = "172.16.10.20/24"
        gateway = "172.16.10.1"
      }
    }
    user_account {
      username = "root"
      password = var.vm_password
    }
  }
}

resource "proxmox_virtual_environment_vm" "db_01" {
  name      = "DB-01"
  node_name = var.proxmox_node
  vm_id     = 107
  started   = false
  clone {
    vm_id = 9000
  }

  cpu {
    cores = 1
  }

  memory {
    dedicated = 1024
  }

  disk {
    datastore_id = "local-lvm"
    interface    = "scsi0"
    size         = 20
  }

  network_device {
    bridge  = "vmbr1"
    vlan_id = 10
  }

  initialization {
    ip_config {
      ipv4 {
        address = "172.16.10.30/24"
        gateway = "172.16.10.1"
      }
    }
    user_account {
      username = "root"
      password = var.vm_password
    }
  }
}

resource "proxmox_virtual_environment_vm" "file_01" {
  name      = "File-01"
  node_name = var.proxmox_node
  vm_id     = 108
  started   = false
  clone {
    vm_id = 9000
  }

  cpu {
    cores = 1
  }

  memory {
    dedicated = 1024
  }

  disk {
    datastore_id = "local-lvm"
    interface    = "scsi0"
    size         = 30
  }

  network_device {
    bridge  = "vmbr1"
    vlan_id = 10
  }

  initialization {
    ip_config {
      ipv4 {
        address = "172.16.10.40/24"
        gateway = "172.16.10.1"
      }
    }
    user_account {
      username = "root"
      password = var.vm_password
    }
  }
}

resource "proxmox_virtual_environment_vm" "backup_01" {
  name      = "Backup-01"
  node_name = var.proxmox_node
  vm_id     = 110
  started   = false
  clone {
    vm_id = 9000
  }

  cpu {
    cores = 1
  }

  memory {
    dedicated = 1024
  }

  disk {
    datastore_id = "local-lvm"
    interface    = "scsi0"
    size         = 50
  }

  network_device {
    bridge  = "vmbr1"
    vlan_id = 110
  }

  initialization {
    ip_config {
      ipv4 {
        address = "172.16.110.10/24"
        gateway = "172.16.110.1"
      }
    }
    user_account {
      username = "root"
      password = var.vm_password
    }
  }
}

# ============================================================
# BASTION-01 — Bridge physiquement isolé vmbr2
# Accès uniquement via VPN → OPNsense → vmbr2
# Si vmbr1 compromis, Bastion inaccessible (L2 séparé)
# ============================================================
resource "proxmox_virtual_environment_vm" "bastion_01" {
  name      = "Bastion-01"
  node_name = var.proxmox_node
  vm_id     = 109
  started   = false
  clone {
    vm_id = 9000
  }

  cpu {
    cores = 1
  }

  memory {
    dedicated = 512
  }

  disk {
    datastore_id = "local-lvm"
    interface    = "scsi0"
    size         = 10
  }

  network_device {
    bridge = "vmbr2" # MGMT isolé — pas de VLAN tag
  }

  initialization {
    ip_config {
      ipv4 {
        address = "172.16.100.20/24"
        gateway = "172.16.100.1"
      }
    }
    user_account {
      username = "root"
      password = var.vm_password
    }
  }
}

# ============================================================
# DNS-Marseille — Cache bind9 (pas de RODC Samba4)
# Tunnel UP : forward vers DC01-Lyon (172.16.10.10)
# Tunnel DOWN : sert le cache TTL — sessions Kerberos actives tiennent
# ============================================================
resource "proxmox_virtual_environment_vm" "dns_marseille" {
  name      = "DNS-Marseille"
  node_name = var.proxmox_node
  vm_id     = 111
  started   = false
  clone {
    vm_id = 9000
  }

  cpu {
    cores = 1
  }

  memory {
    dedicated = 1024
  }

  disk {
    datastore_id = "local-lvm"
    interface    = "scsi0"
    size         = 10
  }

  network_device {
    bridge  = "vmbr3"
    vlan_id = 50
  }

  initialization {
    ip_config {
      ipv4 {
        address = "172.16.50.10/24"
        gateway = "172.16.50.1"
      }
    }
    user_account {
      username = "root"
      password = var.vm_password
    }
  }
}
