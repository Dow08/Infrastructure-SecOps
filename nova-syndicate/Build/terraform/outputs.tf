# ============================================================
# Outputs — IPs exportées pour l'inventory Ansible
# Après terraform apply, ces valeurs alimentent ansible/inventory.ini
# ============================================================

output "dc01_lyon_ip" { value = "172.16.10.10" }
output "wazuh_01_ip" { value = "172.16.10.20" }
output "db_01_ip" { value = "172.16.10.30" }
output "file_01_ip" { value = "172.16.10.40" }
output "proxy_01_ip" { value = "172.16.5.10" }
output "web_01_ip" { value = "172.16.5.30" }
output "honeypot_01_ip" { value = "172.16.5.40" }
output "bastion_01_ip" { value = "172.16.100.20" }
output "backup_01_ip" { value = "172.16.110.10" }
output "dns_marseille_ip" { value = "172.16.50.10" }