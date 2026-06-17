# 05 — Points de Friction & Solutions

---

## 1. Nested Virtualization — Performance

**Problème :** Proxmox dans VMware = KVM dans VMware. Les VMs internes tournent sans accélération hardware native.

**Impact :** Wazuh (4 GB, Java/Elasticsearch) sera lent au démarrage. Dashboard potentiellement laggy.

**Solution :**
- Activer "Virtualize Intel VT-x/EPT" dans les paramètres VMware
- Si trop lent : réduire Wazuh à l'essentiel pour le PoC (pas de dashboard, juste collecte logs)
- Allouer 6 cores CPU à la VM Proxmox dans VMware

---

## 2. OPNsense IPsec — Config partiellement manuelle

**Problème :** La collection `ansibleguy.opnsense` ne couvre pas tout. IPsec et OpenVPN nécessitent une configuration initiale via l'interface web OPNsense.

**Solution :**
- Configurer IPsec manuellement via GUI OPNsense
- Exporter la config en XML (`System > Configuration > Backups`)
- Versionner le XML dans Git
- En cas de recréation de VM = import XML → gain de temps

---

## 3. Terraform provider bpg/proxmox — Maturité

**Problème :** Provider communautaire, possible instabilité sur certaines ressources (cloud-init, VLAN tags).

**Solution :**
- Tester chaque ressource Terraform unitairement
- Ne pas tout appliquer en un seul `terraform apply` lors du premier déploiement
- Garder les configs manuelles de secours pour les ressources problématiques

---

## 4. RODC Samba4 — Non supporté

**Problème :** Samba4 ne supporte pas le mode RODC (Read-Only Domain Controller) de façon stable.

**Solution retenue : Option B — DNS cache bind9 à Marseille**
- bind9 en forward vers DC01-Lyon quand tunnel UP
- bind9 sert le cache quand tunnel DOWN
- Sessions Kerberos actives restent valides (jusqu'à expiration ticket)
- Nouveaux logins AD bloqués si tunnel down (documenté comme limitation PoC)
- **Pour la soutenance :** expliquer qu'en production = DC replica complet (Windows Server)

---

## 5. Double NAT VMware — IPsec cassé

**Problème :** Si VMware est en mode NAT, les deux OPNsense sont derrière le même NAT. L'IPsec entre eux peut poser des problèmes de traversée NAT (NAT-T).

**Solution :**
- VMware **obligatoirement en mode Bridged** pour la carte réseau connectée à vmbr0
- En mode Bridged, les deux OPNsense ont des IPs directement sur le réseau physique
- L'IPsec fonctionne comme un "LAN-to-LAN" dans Proxmox (les deux sur vmbr0)

---

## 6. Ordre de déploiement — Dépendances critiques

**Problème :** Si on déploie les VMs avant OPNsense, elles n'ont pas de gateway et Ansible ne peut pas les atteindre.

**Solution :**
1. OPNsense Lyon en premier (gateway de tout le réseau Lyon)
2. VMs Lyon ensuite (peuvent atteindre internet pour les packages)
3. DC01-Lyon avant tous les autres services (les services dépendent de l'AD)
4. Wazuh avant les agents (les agents ont besoin de l'adresse du manager)
5. OPNsense Marseille + VMs Marseille en dernier

---

## 7. Fallback internet Marseille — Non prévu

**Problème :** Si le tunnel IPsec tombe, Marseille n'a plus internet (tout transite via Lyon).

**Solution pour le PoC :**
- Documenté comme limitation acceptable
- La topologie Hub & Spoke est correcte pour un PoC
- **Pour la soutenance :** mentionner qu'en production = liaison internet directe Marseille + split tunneling (seul le trafic vers Lyon passe via IPsec, internet sort directement)

---

## 8. Honeypot-01 — Isolation dans la DMZ

**Problème :** Honeypot-01 est en DMZ (vmbr1, VLAN 5), sur le même bridge que Proxy-01 et Web-01. Il ne doit pas pouvoir communiquer avec les autres VMs DMZ.

**Solution :**
- Règles OPNsense intra-DMZ : Honeypot-01 ne peut parler qu'à Wazuh (logs)
- Pas d'accès Honeypot → Proxy-01, Honeypot → Web-01
- Si un attaquant entre dans le honeypot = il est en cul-de-sac DMZ + alerté dans Wazuh

---

## 9. Wazuh double interface — Cloud-init

**Problème :** Wazuh-01 a besoin de 2 interfaces réseau (eth0 SERVERS + eth1 collecte vmbr5). La configuration cloud-init de Terraform ne gère qu'une interface par défaut.

**Solution :**
- Terraform crée Wazuh-01 avec 2 interfaces réseau déclarées
- Ansible configure les deux interfaces via /etc/network/interfaces
- Le rôle `network_persist` gère la configuration statique des deux IPs

---

## 10. Samba4 AD — Clavier AZERTY en console

**Rappel :** Le mot de passe AD `Nova@2024!` contient des caractères spéciaux.
Sur clavier AZERTY physique en console QEMU : `@` = AltGr+0, `!` = Maj+!

**Solution :** Utiliser un mot de passe sans caractères spéciaux compliqués pour le PoC.
Proposition : `Nova2024Pass` (lettres + chiffres uniquement pour les consoles)
