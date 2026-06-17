# 🎬 Script Démo Live — Soutenance Nova Syndicate

> Plan minute-par-minute de la démo. À répéter au moins 2 fois avant le jour J.
> Cible : **5-6 minutes** de démo (sur 15 min de présentation totale).

---

## ⚙️ PRÉPARATION (à faire AVANT d'entrer en salle)

### A. Démarrer les VMs essentielles (sur Proxmox)
```bash
for vm in 100 101 102 107 108 109; do qm start $vm 2>/dev/null; done

# Recréer le bridge VLAN host (non-persistant)
ip link add link vmbr1 name vmbr1.10 type vlan id 10 2>/dev/null
ip addr add 10.1.10.254/24 dev vmbr1.10 2>/dev/null
ip link set vmbr1.10 up
bridge vlan add vid 10 dev vmbr1 self 2>/dev/null

# Vérifier tout up
sleep 30
bash /root/check_status.sh
```

### B. Lancer les 2 tunnels SSH depuis ton PC (PowerShell ou Git Bash)

**Tunnel 1 — Web BricoPro + Grafana + Prometheus + Loki + Wazuh** (tout-en-un) :
```powershell
ssh -i C:\Users\Dow\.ssh\bastion_key `
    -L 8080:10.1.10.30:80 `
    -L 9090:10.1.10.40:9090 `
    -L 3000:10.1.10.40:3000 `
    -L 3100:10.1.10.40:3100 `
    -L 8443:10.1.10.40:443 `
    root@192.168.1.165
```

→ Laisse cette fenêtre OUVERTE pendant toute la démo.

### C. Pré-ouvrir tes onglets Chrome (dans l'ordre, gauche → droite)

1. `https://github.com/Dow08/Projet_Nova_syndicate_Jedha` — GitHub vitrine
2. `http://localhost:8080` — **BricoPro Accueil**
3. `http://localhost:8080/catalogue.php?cat=outillage` — **Catalogue outillage**
4. `http://localhost:8080/clients.php` — **Espace pro (DB live)**
5. `http://localhost:8080/infrastructure.php` — **Infrastructure (vendeur)**
6. `https://localhost:8443` — **Wazuh dashboard** (login déjà fait : `admin` / `*gyoqx?S2Nst.gKQigw+RaWB4163b5KR`)
7. `http://localhost:3000` — **Grafana** (login `admin/admin`)
8. `http://localhost:9090/targets` — **Prometheus Targets**
9. `http://localhost:9090/alerts` — **Prometheus Alerts**
10. `https://192.168.1.166` — **OPNsense Suricata**

### D. Pré-ouvrir 2 terminals

**Terminal 1** : SSH sur DC01 (pour Samba demo)
```bash
ssh -i /root/.ssh/bastion_key novaadmin@10.1.10.10
```

**Terminal 2** : Proxmox shell pour Ansible / nmap
```bash
# Déjà dans /root/nova-ansible
```

---

## 🎬 SCRIPT MINUTE PAR MINUTE

### Minute 1 — Vitrine GitHub + page accueil BricoPro

**[ONGLET 1 — GitHub]**

🗣️ *« Voici le repo GitHub du projet — c'est la sauvegarde et la vitrine. Vous y trouvez les 10 livrables documentaires, les playbooks Ansible, et le README qui résume l'architecture. Tout est versionné, auditable, conforme aux pratiques GitOps. »*

➜ Scroll rapide le README pour montrer les badges et la table de stack.

**[ONGLET 2 — BricoPro Accueil]**

🗣️ *« On bascule sur la plateforme e-commerce déployée : BricoPro, opérée par Nova Syndicate. Stack 3 tiers : Nginx + PHP-FPM en frontend, MariaDB en backend, le tout sur DB-01 dans le VLAN SERVERS. »*

➜ Montre la page : titre, catégories, produits populaires.

### Minute 2 — Catalogue dynamique + DB live

**[ONGLET 3 — Catalogue Outillage]**

🗣️ *« Le catalogue est dynamique — chaque produit affiché vient d'une requête PHP sur MariaDB. Filtre par catégorie, gestion stock (en stock / limité / rupture), prix HT formatés. »*

**[ONGLET 4 — Espace pro]**

🗣️ *« La page Espace pro est l'exemple parfait du 3-tiers : PHP requête MariaDB en live et affiche les 6 clients pro enregistrés. C'est la base sur laquelle on construit l'authentification AD ensuite. »*

➜ Pointe sur la note en bas : « Source : novalab.clients · auth Samba AD nova.local ».

### Minute 3 — Wazuh SIEM

**[ONGLET 6 — Wazuh dashboard]**

🗣️ *« Wazuh est notre SIEM open-source — manager + indexer + dashboard. Sur la page d'accueil, on voit la matrice MITRE ATT&CK et le nombre d'agents connectés. »*

➜ Click **Modules** → **Security events** → tu vois "570 events / Top MITRE / Top 5 agents".

🗣️ *« 570 events collectés en 24h. La technique T1562.001 'Disable or Modify Tools' a été détectée. Les 3 agents — DC01, DB-01 et File-01 — remontent tous. »*

➜ Click sur **Agents** dans le menu → montre les 3 agents Active avec leur IP et OS.

🗣️ *« Coverage 100%. En cas d'incident, on peut drill-down sur chaque agent pour voir les events, FIM, SCA — c'est notre N2 de défense. »*

### Minute 4 — Observabilité Prometheus + Loki + Grafana

**[ONGLET 7 — Grafana Dashboards]**

🗣️ *« En complément du SIEM, on a la stack LGTM : Loki, Grafana, Tempo, Mimir — l'alternative moderne à ELK. »*

➜ Click **Dashboards** → ouvre **Node Exporter Full**.

🗣️ *« Node Exporter Full — métriques système temps réel pour les 3 hôtes. CPU, RAM, disque, réseau. Refresh 15s. »*

➜ Click **Explore** → datasource **Loki** → query `{job="systemd-journal"}` → Run.

🗣️ *« Et Loki côté logs — on a 8 000 lignes ingérées par heure depuis les 3 hosts. Cherche systemd, nginx, mariadb, wazuh. Toutes les logs centralisées. »*

### Minute 5 — Prometheus alerting + Suricata

**[ONGLET 9 — Prometheus Alerts]**

🗣️ *« 8 règles d'alerting actives : HostDown, HighCPULoad, MariaDBDown, SSHBruteForce, etc. En cas de seuil franchi, en prod on brancherait Alertmanager pour router email / PagerDuty / Slack. »*

**[ONGLET 10 — OPNsense Suricata]**

🗣️ *« Côté réseau, Suricata en mode IDS sur OPNsense Lyon. 5 865 règles ET Open chargées + cron de mise à jour quotidienne. »*

➜ Click **Règles** → montre les milliers de lignes.

### Minute 6 — Live commands terminal

**[TERMINAL 1 — DC01]**
```bash
sudo samba-tool user list
sudo samba-tool domain info 127.0.0.1
```

🗣️ *« AD Samba 4 sur DC01, domaine nova.local — Administrator, Guest, krbtgt. Domaine info : Forest nova.local, NetBIOS NOVA. Production ready. »*

**[TERMINAL 2 — Proxmox]**
```bash
ansible -i /root/nova-ansible/inventory.ini all -m ping
```

🗣️ *« Et pour clôturer, Ansible — le pont entre IaC et configuration management. Un ping confirme la connectivité sur les 3 hosts. Tout est redéployable en une commande avec quickstart.sh. »*

---

## 🎯 SCRIPT EXTENSIBLE (si t'as 7-8 min de démo)

### Bonus 1 — Démo nmap → Wazuh corrélation
```bash
# Depuis Proxmox
nmap -sV -A 192.168.1.166
```
Puis montrer dans Wazuh **Security events** filtrer par "nmap" ou "scan".

### Bonus 2 — Démo PCA/PRA
Ouvre `livrables/04_pca_pra/PCA_PRA_Nova_Syndicate.md` dans le repo GitHub. Montre la matrice 17 risques.

### Bonus 3 — Architecture diagram (Topologie 3D)
Montre le visuel Canva/Gemini que tu auras généré.

---

## 🚨 PLAN B — si quelque chose foire pendant la démo

| Si... | Tu dis et tu fais |
|-------|-------------------|
| **Wazuh ne charge pas** | « Le tunnel SSH a dû dropper, mais voici un screenshot pris avant la soutenance » → ouvre `Documents/POC_Screen/Dashboard Wazuh.png` |
| **Grafana ne répond pas** | Pareil : `POC PROMETHEUS+GRAFANA+LOKI.png` |
| **BricoPro 502** | « DB-01 a dû être rebooté » → ouvre screenshots `SIte vitrine page X.png` |
| **Terminal hang** | Ctrl+C, dis « la latence est due au mode TCG en lab » et continue le pitch |
| **Tunnel SSH coupe** | Relance le tunnel dans une 2e fenêtre PowerShell, en parallèle continue le pitch documentaire |

**Règle d'or** : tu as **35 screenshots POC** dans `Documents/POC_Screen/`. Si tu butes sur la démo live, tu bascules sur les screenshots et tu commentes — le contenu reste vendable.

---

## 🗣️ TRANSITIONS ENTRE SECTIONS

| Transition | Phrase |
|-----------|--------|
| GitHub → BricoPro | « Maintenant je vous montre ce qui tourne réellement » |
| BricoPro → Wazuh | « La question évidente : comment on surveille tout ça ? » |
| Wazuh → Grafana | « Wazuh c'est la sécu, Grafana c'est la performance — les deux complémentaires » |
| Grafana → Suricata | « Ça c'est le host. Au niveau réseau, on a Suricata » |
| Suricata → Terminal | « Tout ça est piloté par Ansible — démo en CLI » |
| Terminal → Conclusion | « Architecture cible 12 VMs, PoC consolidé 3, redéploiement automatisable » |

---

## ⏱️ TIMING TOTAL

- Préparation (avant entrée) : 5 min
- Démo live : **5-6 min**
- Buffer pour questions pendant démo : 1-2 min
- Buffer pour Q&A après : 3-4 min

→ Sur 15 min de présentation totale, garde **8 min pour le slide deck** (contexte, archi, sécurité, conformité, CAPEX/OPEX, conclusion).

---

## 📝 CHECKLIST À COCHER LA VEILLE (jeudi soir)

- [ ] Toutes les VMs essentielles up et stable depuis 1h+
- [ ] Bridge VLAN host Proxmox recréé après reboot
- [ ] Tunnel SSH multi-port testé depuis ton PC
- [ ] Chrome : 10 onglets pré-ouverts et logués
- [ ] 2 terminals pré-ouverts (DC01 + Proxmox)
- [ ] Screenshots `Documents/POC_Screen/` accessibles offline en backup
- [ ] Câble réseau de secours / connexion 4G fallback
- [ ] Charger laptop à 100%, brancher adaptateur secteur en salle
- [ ] Eau à portée de main
- [ ] Cravate / chemise propre 😄

---

*Document à imprimer ou ouvrir sur ton téléphone pendant la soutenance pour ne rien oublier.*
*Dernière maj : mercredi 13/05/2026 aprem.*
