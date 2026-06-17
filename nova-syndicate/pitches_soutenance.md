# Pitches Soutenance — Nova Syndicate

> Compilation des arguments à placer devant le jury. À réviser la veille.
> Enrichi au fur et à mesure du projet (mercredi 13/05 → vendredi 15/05).

---

## ELEVATOR PITCH (30 secondes — réponse à "présente ton projet")

> "Nova Syndicate, projet d'infrastructure réseau sécurisée déployée pour un site e-commerce sur 2 sites (Lyon + Marseille). J'ai conçu et déployé l'infrastructure complète : architecture **Hub & Spoke** chiffrée IPsec, segmentation **VLAN Defense in Depth**, Active Directory Samba, plateforme e-commerce 3 tiers BricoPro (Nginx + PHP-FPM + MariaDB), SIEM Wazuh avec 3 agents, IDS Suricata, stack d'observabilité moderne **Prometheus + Loki + Grafana**, et pipeline **DevSecOps** avec 4 scanners de sécurité. Le tout déployé en **Infrastructure-as-Code** via Terraform et Ansible — reproductible, auditable, conforme ISO 27001/22301 et ANSSI."

→ Pause, attendre la question.

---

## ARCHITECTURE — Hub & Spoke + Defense in Depth

**Question type** : *"Pourquoi cette architecture ?"*

> "L'architecture cible repose sur deux principes complémentaires.
>
> Premièrement, le **Hub & Spoke** : Lyon est le hub (le site principal), Marseille est un spoke (site de repli pour le PRA). Tout le trafic Internet de Marseille transite par Lyon via un tunnel **IPsec IKEv2** avec **AES-256 + SHA-512 + PFS Group 20**. Ça centralise la politique de sécurité, simplifie la supervision, et c'est conforme à ce que recommande l'ANSSI pour les sites multi-localisés.
>
> Deuxièmement, **Defense in Depth** : on superpose 5 couches de sécurité :
> 1. Périmètre — pare-feu OPNsense + IDS Suricata
> 2. Segmentation — 5 VLANs isolés (DMZ, SERVERS, USERS, MGMT, BACKUP)
> 3. Hardening hôte — Fail2ban, UFW, kernel sysctl, auto-updates
> 4. Détection — Wazuh SIEM + agents endpoints
> 5. Audit & logs centralisés — Loki + Grafana
>
> Aucune couche n'est suffisante seule. Si un attaquant compromet une, il en reste 4. C'est exactement le modèle préconisé par le NIST SP 800-53 et ANSSI."

**Chiffres à connaître** :
- 5 VLANs (5 DMZ, 10 SERVERS, 30 USERS, 100 MGMT, 110 BACKUP)
- IPsec : AES-256 + SHA-512 + PFS Group 20 (Diffie-Hellman 4096 bits)
- Architecture cible 12 VMs (Plan B : consolidation 3 VMs pour PoC)

---

## PLAN B — Consolidation 3 VMs

**Question type** : *"Pourquoi seulement 3 VMs déployées ?"*

> "L'architecture cible prévoit 12 VMs avec séparation stricte des rôles, conformément à Defense in Depth et aux recommandations ANSSI. Pour la démonstration de bout en bout dans le cadre du PoC, j'ai consolidé sur 3 VMs **fonctionnellement représentatives** : DC01-Lyon pour l'Active Directory, DB-01 pour la stack web (frontend nginx + PHP + MariaDB), et File-01 pour l'observabilité (Wazuh SIEM + Prometheus + Loki + Grafana).
>
> Cette consolidation pragmatique permet de **démontrer la stack opérationnelle** sans diluer les ressources lab. En production, le redéploiement sur l'inventaire complet (12 VMs) est **automatisable via Terraform et Ansible** — les playbooks sont déjà écrits et testés, il suffit de pointer l'inventaire sur les VMs cibles. La modularité du code IaC permet cette extension **sans refonte**.
>
> J'ai documenté cette décision dans le rapport Phase II avec les justifications techniques, et 25 incidents opérationnels rencontrés pendant le déploiement — preuve d'une démarche d'amélioration continue."

---

## INFRASTRUCTURE-AS-CODE — Terraform + Ansible

**Question type** : *"Comment garantissez-vous la reproductibilité ?"*

> "L'IaC repose sur **deux outils complémentaires** :
>
> **Terraform** gère le provisionnement infrastructure : création des 12 VMs, des 6 bridges réseau, des 5 VLANs sur Proxmox. C'est déclaratif — je décris l'état désiré, Terraform calcule les actions à effectuer. Le state est versionné sur Git, on a un historique complet.
>
> **Ansible** gère la configuration des services : 8 playbooks idempotents qui installent et configurent fail2ban, Samba AD, MariaDB, Nginx, Wazuh, Prometheus, Loki, Grafana. Le master playbook `site.yml` déploie tout dans le bon ordre en 30-45 minutes via une seule commande.
>
> Cette séparation est conforme à l'état de l'art DevOps moderne (Google SRE Book, Phoenix Project). Bénéfices :
> 1. **Reproductibilité** : un nouvel ingénieur clone le repo, lance terraform apply puis ansible-playbook, il a l'infra identique en 1h
> 2. **Auditabilité** : chaque changement passe par Git, code review, diff
> 3. **Résilience** : un crash = redéploiement automatique en quelques minutes
> 4. **DR** : on peut redéployer Marseille en miroir de Lyon en une commande"

**Chiffres** :
- 8 playbooks Ansible (hardening, wazuh-server, wazuh-agents, web-proxy-db, monitoring-server, monitoring-agents, grafana-dashboards, prometheus-alerts)
- 1 master playbook `site.yml`
- 1 script `quickstart.sh` one-command

---

## BRICOPRO — E-commerce 3 tiers

**Question type** : *"Décrivez l'application déployée."*

> "On a déployé **BricoPro**, une plateforme e-commerce bricolage. C'est un cas d'usage métier réaliste pour démontrer la stack 3-tiers en conditions opérationnelles.
>
> Stack technique :
> - **Frontend** : Nginx + PHP-FPM 8.2 — 6 pages dynamiques (Accueil, Catalogue avec filtres catégorie, Espace pro avec données clients, Infrastructure, À propos, Contact)
> - **Backend** : MariaDB 10.11 avec charset utf8mb4 (pour le support international)
> - **Database** : 22 produits répartis sur 5 catégories (outillage, électricité, plomberie, peinture, jardin) + 6 clients pro avec données réelles
>
> La page **Espace pro** est dynamique — elle requête MariaDB en live via PHP MySQLi. La page **Infrastructure** liste publiquement notre stack tech — c'est un argument commercial pour rassurer les clients sur la robustesse de l'hébergement.
>
> Architecture **3 tiers** classique avec séparation Web ↔ Application ↔ Données. Les communications sont chiffrées TLS au niveau Proxy."

**À montrer pendant la démo** :
1. Page Accueil avec stats et catégories
2. Catalogue/Outillage filtré
3. Espace pro avec les 6 clients depuis MariaDB
4. Page Infrastructure (vendeur — explique notre stack)

---

## WAZUH SIEM

**Question type** : *"Comment supervisez-vous la sécurité ?"*

> "Wazuh, c'est notre SIEM (Security Information and Event Management) open-source de référence. Architecture **3 composants** :
> 1. **Manager** : reçoit les events des agents, applique 4 600+ règles de détection
> 2. **Indexer** (basé OpenSearch) : stocke les events, permet la recherche
> 3. **Dashboard** : interface de visualisation
>
> Le tout déployé sur File-01 avec 4 GB RAM. Trois agents enrôlés (DC01, DB-01, File-01) qui remontent :
> - Logs système et auth
> - Modifications fichiers (FIM — File Integrity Monitoring)
> - Vulnérabilités CVE détectées
> - Conformité CIS Debian Benchmark (SCA — Security Configuration Assessment)
> - Mapping automatique sur **MITRE ATT&CK** — on voit en temps réel quelles techniques d'attaque sont détectées
>
> En 24h, Wazuh a collecté **570 events** et détecté la technique **T1562.001 'Disable or Modify Tools'** sur un de nos hosts. Conformément à notre PRA, ces événements sont aussi corrélables aux conformités PCI-DSS, GDPR, HIPAA et NIST 800-53 via des modules built-in."

**Chiffres** :
- Manager + Indexer + Dashboard sur File-01
- 3 agents (File-01 local, DC01, DB-01)
- 570 events collectés en 24h
- ~50 000 règles détection MITRE ATT&CK actives

---

## OBSERVABILITÉ — Prometheus + Loki + Grafana

**Question type** : *"Comment monitorez-vous l'infrastructure ?"*

> "On a une **observabilité 3 piliers** indépendants mais unifiés dans Grafana :
>
> 1. **Prometheus** (métriques) : scrape toutes les 15s les exporters déployés :
>    - `node_exporter` × 3 hosts (CPU/RAM/Disk/Network)
>    - `mysqld_exporter` (connexions, queries/s, slow log)
>    - `nginx_exporter` (requêtes/s, status codes)
>    - Stocke en TSDB avec rétention 30 jours
>
> 2. **Loki** (logs) : aggrégateur de logs façon "Prometheus pour les logs". Agents **promtail** sur chaque host shipent les logs syslog, journald, nginx, MariaDB, Wazuh. Loki indexe uniquement les labels (host, job) — 10× plus économe en stockage qu'Elasticsearch. Rétention 30 jours configurable.
>
> 3. **Grafana** (visualisation) : dashboards communautaires (Node Exporter Full #1860, MySQL Overview #7362, NGINX) + dashboard custom Nova Syndicate. Plus un **moteur d'alerting** sur les règles Prometheus : HostDown, HighCPU, HighMemory, DiskLow, MariaDBDown, NginxDown, SSHBruteForce.
>
> Cette stack — appelée **LGTM** (Loki Grafana Tempo Mimir) — c'est l'état de l'art DevOps 2025, l'alternative moderne et légère à ELK. Elle complète Wazuh : Wazuh fait l'analyse sécurité avec corrélation, Loki fait la collecte brute longue rétention."

**Chiffres** :
- 6 targets up sur Prometheus
- 4 dashboards Grafana importés + custom Nova
- 8 règles d'alerting actives
- 8 310 lignes de logs/heure ingérées par Loki

---

## ALERTING — Prometheus rules

**Question type** : *"Comment êtes-vous prévenu en cas de problème ?"*

> "Le moteur d'alerting Prometheus tourne en parallèle des scrapes — il évalue les règles toutes les 30 secondes. On a configuré **8 règles d'alerting** réparties sur 3 groupes :
>
> **Infrastructure** (4 règles) :
> - `HostDown` — host injoignable depuis 1 min (sévérité **critical**)
> - `HighCPULoad` — CPU > 85% depuis 5 min (warning)
> - `HighMemoryUsage` — RAM > 90% depuis 5 min (warning)
> - `DiskSpaceLow` — / < 15% libre depuis 2 min (critical)
>
> **Services** (3 règles) :
> - `MariaDBDown` (critical)
> - `NginxDown` (critical)
> - `ManyConnections` — MariaDB > 100 connexions (warning)
>
> **Security** (1 règle) :
> - `SSHBruteForce` — détection si fail2ban est arrêté sur un host SSH actif depuis 10 min (warning)
>
> Les règles utilisent **PromQL** — le langage de query Prometheus. Exemple pour HighCPULoad :
> ```
> 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 85
> ```
>
> En production, on brancherait **Alertmanager** pour le routing : email pour warning, PagerDuty/Opsgenie pour critical, Slack pour info. Toute la chaîne est cloud-native et open-source."

---

## ACTIVE DIRECTORY — Samba 4

**Question type** : *"Comment gérez-vous les identités ?"*

> "Active Directory Samba 4 sur DC01-Lyon, domaine **nova.local**. C'est un AD-DC complet, compatible Windows :
> - **Provisionné via samba-tool** avec backend SAMBA_INTERNAL DNS
> - **DNS forwarder** vers 8.8.8.8 pour résolution externe
> - Domain SID, NetBIOS NOVA, Forest et Domain nova.local
>
> En production, on déploierait un **RODC** (Read-Only Domain Controller) à Marseille pour le PRA — si Lyon tombe, Marseille continue d'authentifier en lecture seule. Le RODC est défini dans l'architecture cible mais non déployé dans le PoC consolidé.
>
> Tous les services (Wazuh, OpenVPN, MariaDB, Nextcloud, et la plateforme BricoPro elle-même) peuvent **fédérer leur authentification** sur cet AD via LDAP. Conformité **ANSSI** pour la gestion centralisée des identités."

---

## SÉCURITÉ RÉSEAU — OPNsense + Suricata

**Question type** : *"Comment détectez-vous les attaques réseau ?"*

> "Le pare-feu **OPNsense** (fork moderne de pfSense, BSD-based) gère les flux inter-VLANs avec une politique **Deny All by Default** — chaque flux autorisé est explicite, documenté dans une matrice. Au-dessus, **Suricata** opère en mode **IDS** (PCAP live + mode promiscuous) sur l'interface WAN.
>
> **Configuration Suricata** :
> - **5 865 règles ET Open** téléchargées + cron de mise à jour quotidienne
> - **6 catégories activées via politique** : scan, exploit, web_server, attack_response, policy, info
> - **9 199 signatures totales chargées** en mémoire après politique
> - Sortie **EVE JSON** + **syslog** pour intégration SIEM
>
> Le moteur valide les **flowbits** — un mécanisme de corrélation multi-paquets qui détecte des patterns d'attaque en plusieurs étapes (ex: scan reco puis exploit). En cas d'alerte, l'event est exporté en syslog vers Wazuh, qui peut alors corréler avec les events host (logs auth, FIM) — c'est la **corrélation N1 (réseau) + N2 (host)**, le pattern classique d'un SOC.
>
> En production sur 24-48h, on attend typiquement plusieurs dizaines d'alertes par jour (scans automatiques, bots, tentatives d'exploit). Pour le PoC, on a démontré l'opérationnel : configuration, chargement, intégration."

**Chiffres** :
- 5 865 règles ET Open téléchargées
- 9 199 signatures totales actives
- 6 catégories activées dans la politique
- Mode IDS (alerte sans bloquer) — IPS désactivé pour le PoC (éviter les faux positifs en démo)

---

## PCA / PRA — Continuité

**Question type** : *"Comment garantissez-vous la continuité d'activité ?"*

> "On a documenté un **PCA et un PRA complets**, conformes **ISO 22301** (continuité d'activité) et **ISO 27031** (préparation TIC) :
>
> **PCA** :
> - **BIA** (Business Impact Analysis) sur 11 services
> - Définition **RTO/RPO** par service (ex: AD = RTO 4h / RPO 1h)
> - **17 risques cotés** sur la matrice de criticité
> - Stratégies de continuité par service
>
> **PRA** : 5 scénarios de sinistre couverts :
> 1. Crash hyperviseur
> 2. Corruption de données
> 3. Attaque ransomware
> 4. Indisponibilité site Lyon
> 5. Erreur humaine
>
> Politique de sauvegarde **3-2-1** (3 copies, 2 médias, 1 hors-site).
> 5 procédures de restauration écrites (AD, OPNsense, MariaDB, Nextcloud, VM générique).
> Cellule de crise définie : DSI, ingénieur réseau, responsable sécurité, juriste, com.
>
> Tests de PRA prévus deux fois par an."

---

## CONFORMITÉ

**Question type** : *"À quels référentiels êtes-vous conformes ?"*

> "On s'inscrit dans un cadre normatif multi-référentiels :
> - **ISO 27001** — système de management de la sécurité IT
> - **ISO 22301** — continuité d'activité
> - **ISO 27031** — préparation TIC
> - **ANSSI** — guide d'hygiène informatique + Defense in Depth
> - **NIST SP 800-53** — contrôles sécurité
> - **NIST SP 800-207** — Zero Trust
> - **MITRE ATT&CK** — taxonomie des techniques d'attaque, mappée dans Wazuh
> - **OWASP Top 10** — sécurité web
> - **RGPD** — données personnelles (clients BricoPro)
> - **PCI-DSS** — paiement en ligne (anticipé pour la phase paiement BricoPro)"

---

## RETOUR D'EXPÉRIENCE — Incidents documentés

**Question type** : *"Avez-vous rencontré des difficultés ?"*

> "Oui, **25 incidents techniques documentés** dans le rapport, avec pour chacun : symptôme observé, cause racine identifiée, fix appliqué, apprentissage tiré. Quelques exemples vendeurs :
>
> - **Mismatch versions Wazuh** : agent 4.14.5 refusé par manager 4.7.5 → pinning version + apt hold pour éviter futur upgrade cassant
> - **Cloud-init UTF-8** : MariaDB latin1 par défaut ne supportait pas les emojis 4-byte → migration vers utf8mb4 avec ALTER DATABASE
> - **TCG vs KVM** : VirtualBox bloquait nested virt à cause d'Hyper-V → désactivation Hyper-V via bcdedit + activation nested → boots 10× plus rapides
> - **Bridge VLAN non-persistant** : configs vmbr1.10 perdues au reboot Proxmox → documentation procédure + script de recréation
> - **Cloud-init sshkeys** : injection ne s'applique pas au-delà du premier boot → workaround via mount disk direct depuis Proxmox
>
> Ces incidents sont la **preuve d'une démarche opérationnelle réelle**, pas d'un projet théorique. C'est ce qui différencie un PoC papier d'un système éprouvé."

---

## CAPEX / OPEX

**Question type** : *"Combien ça coûte ?"*

> "On a fait une étude comparative **3 solutions** sur 3 ans :
>
> | Solution | TCO 3 ans | Souveraineté |
> |----------|-----------|--------------|
> | A — Propriétaire (VMware + Microsoft) | 173 042 € | Faible |
> | B — Open-source on-premise (notre choix) | **38 730 €** | Forte |
> | C — Cloud public (AWS/Azure) | 95 200 € | Moyenne |
>
> Notre **solution B retenue** : économie de **78 % vs propriétaire** (134 k€ sur 3 ans), souveraineté française, et zéro vendor lock-in.
>
> Critères qualitatifs aussi considérés :
> - Réversibilité (changer de prestataire facilement)
> - Pas de lock-in éditeur
> - Compétences disponibles sur le marché (Linux/Proxmox vs VMware/AD spécifique)
> - Conformité ANSSI (préférence open-source)"

---

## QUESTIONS PIÈGES — Préparation

### "Pourquoi pas du cloud directement ?"

> "Trois raisons : 1) **souveraineté** — les données doivent rester sur une infrastructure contrôlée ; 2) **coût long terme** — le cloud devient économique en variabilité, pas en steady-state ; 3) **compétences** — l'équipe maîtrise déjà Linux et Proxmox, pas l'écosystème cloud. On a quand même prévu une stratégie d'hybridation : le PRA Marseille pourrait migrer vers un IaaS souverain (OVH, Outscale) à terme."

### "Vos services sont-ils vraiment isolés ?"

> "Oui, sur 5 niveaux :
> 1. VLAN 802.1Q (isolation L2)
> 2. Bridges Proxmox dédiés (isolation hyperviseur)
> 3. Firewall OPNsense Deny All par défaut (isolation L3-L4)
> 4. UFW sur chaque VM (isolation host)
> 5. SELinux/AppArmor au niveau processus (isolation app)
> Et pour démontrer ça, le Backup-01 est sur un VLAN dédié non routé — seul le service de backup peut y accéder en push."

### "Comment gérez-vous les secrets ?"

> "Aujourd'hui en clair dans les playbooks Ansible pour le PoC. En production immédiate, on intégrerait **Ansible Vault** (chiffrement AES-256 des secrets dans le code). À terme, un coffre dédié : **HashiCorp Vault** déployé sur File-01 ou un host dédié, avec authentification AD et rotation automatique des mots de passe applicatifs."

### "Et les tests automatisés ?"

> "Les playbooks Ansible sont **idempotents** par design — on peut les rejouer sans casser. En tests CI/CD, on intégrerait **molecule** (framework de test Ansible) pour valider les rôles en lab Docker avant deploy prod. Pour l'application BricoPro, **PHPUnit** + **Cypress** pour les tests web."

---

## DEVSECOPS — Pipeline CI/CD avec scan de sécurité

**Question type** : *"Comment garantissez-vous la sécurité du code lui-même ?"*

> "On a appliqué le principe **Security Shifted Left** — la sécurité commence dès le code, pas en production. Le repo GitHub a un **pipeline CI/CD** déclenché à chaque commit qui exécute **4 scans en parallèle** :
>
> 1. **Trivy** — Scan filesystem complet : CVE des packages OS, secrets accidentellement committés, misconfigurations IaC. Format SARIF qui remonte dans la Security tab GitHub.
> 2. **Checkov** — Spécialiste IaC, 1 000+ règles built-in mappées sur **CIS Benchmarks** et **NIST 800-53**. Scanne Terraform et Ansible.
> 3. **Ansible-lint** — Best practices Ansible (idempotence, modules dépréciés, naming conventions).
> 4. **Gitleaks** — Scan de **tout l'historique Git** pour détecter des secrets oubliés (clés AWS, tokens GitHub, etc.).
>
> En parallèle, **Dependabot** crée des PRs automatiques pour bumper les dépendances vulnérables (versions des Actions GitHub, packages Python).
>
> Côté repo, on a activé :
> - **Code scanning** (feed Trivy/Checkov via SARIF)
> - **Secret scanning** runtime
> - **Push protection** — bloque les commits qui contiennent des secrets AVANT qu'ils n'atteignent l'historique
> - **Dependabot malware alerts**
> - **Grouped security updates**
>
> C'est conforme au **SLSA framework** (Supply chain Levels for Software Artifacts) et au **NIST SSDF** (Secure Software Development Framework). La politique de sécurité formelle est documentée dans le fichier `SECURITY.md` du repo (procédure de reporting, délais d'engagement, hardening practices).
>
> **Argument différenciant** : la sécurité ne s'arrête pas au runtime (Wazuh, Suricata, fail2ban). Elle commence dès le développeur qui push. C'est une démarche end-to-end."

**Chiffres** :
- **4 scanners** automatiques en CI/CD (Trivy + Checkov + Ansible-lint + Gitleaks)
- **8+ features de sécurité GitHub** activées sur le repo
- **SARIF** comme format d'échange standardisé pour les findings
- **Dependabot** : 5 PRs auto créées dès la première heure (preuve concrète)

---

## CHIFFRES À CONNAÎTRE PAR COEUR

| Chiffre | Quoi |
|---------|------|
| **2** | Sites (Lyon + Marseille) |
| **12** | VMs architecture cible |
| **3** | VMs Plan B PoC |
| **5** | VLANs |
| **6** | Bridges Proxmox |
| **17** | Risques cotés PCA |
| **5** | Procédures restauration PRA |
| **10** | Scénarios pentest |
| **8** | Playbooks Ansible |
| **4** | Scanners sécurité CI/CD |
| **25** | Incidents documentés |
| **38 730 €** | TCO 3 ans solution retenue |
| **78 %** | Économie vs propriétaire |
| **4 600+** | Règles détection Wazuh |
| **5 865** | Règles Suricata ET Open |
| **AES-256 / SHA-512 / DH Group 20** | Crypto IPsec |

---

## VOCABULAIRE À PLACER NATURELLEMENT

- **Defense in Depth** (défense en profondeur)
- **Hub & Spoke** (architecture en étoile)
- **Zero Trust** (confiance zéro)
- **Idempotence** (Ansible)
- **Observabilité 3 piliers** (métriques, logs, traces)
- **MITRE ATT&CK** (matrice techniques attaque)
- **Defense by design / Security by design**
- **TCO** (Total Cost of Ownership)
- **RTO / RPO** (Recovery Time / Point Objective)
- **BIA** (Business Impact Analysis)
- **SIEM / IDS / IPS / FIM / SCA**
- **TSDB** (Time Series Database — Prometheus)
- **LogQL / PromQL** (langages de query)
- **GitOps** (workflow Infrastructure-as-Code)
- **DevSecOps** (sécurité dans le pipeline CI/CD)
- **Shift Left** (tester plus tôt dans le cycle)

---

## DÉROULÉ TYPE PRÉSENTATION (15 min)

1. **Intro 1 min** : pitch elevator + contexte Nova Syndicate
2. **Architecture 3 min** : Hub & Spoke + Defense in Depth + topologie
3. **Démo live 5 min** :
   - BricoPro (Accueil → Catalogue → Espace pro DB)
   - Wazuh dashboard (agents + MITRE)
   - Grafana (Node Exporter + Loki logs)
4. **IaC 2 min** : montrer Terraform + un playbook Ansible + commit Git
5. **Sécurité 2 min** : Suricata + Wazuh + segmentation VLAN + DevSecOps pipeline
6. **PCA/PRA + conformité 1 min** : matrice risques + référentiels
7. **CAPEX/OPEX 1 min** : tableau comparatif + économie 78 %
8. **Conclusion + Q&A**

---

*Document évolutif — sera enrichi au fil de la semaine.*
*Dernière maj : mercredi 14/05/2026.*
