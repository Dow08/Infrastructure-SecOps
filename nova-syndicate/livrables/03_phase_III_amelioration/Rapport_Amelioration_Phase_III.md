# RAPPORT D'AMÉLIORATION — PHASE III
## Renforcement et résilience de l'infrastructure
### Client : Nova Syndicate

---

**Référence document** : NS-2026-003
**Auteur** : Dorian Poncelet — Responsable Technique
**Date** : Mai 2026
**Version** : 1.0
**Statut** : Livrable Phase III — Amélioration et renforcement
**Classification** : Confidentiel – Diffusion restreinte client

---

## SOMMAIRE

1. [Objet et contexte](#1-objet-et-contexte)
2. [Améliorations apportées](#2-améliorations-apportées)
3. [Outil de supervision déployé](#3-outil-de-supervision-déployé)
4. [Scripts d'automatisation](#4-scripts-dautomatisation)
5. [Plans de continuité (PCA/PRA)](#5-plans-de-continuité-pcapra)
6. [Tests de robustesse réalisés](#6-tests-de-robustesse-réalisés)
7. [Indicateurs de performance](#7-indicateurs-de-performance)
8. [Recommandations pour la suite](#8-recommandations-pour-la-suite)

---

## 1. Objet et contexte

### 1.1 Objectif de la Phase III

Conformément au plan de mission, la Phase III vise à **améliorer et renforcer le système** déployé en Phase II. Les axes de travail sont :

1. **Continuité d'activité** : production des plans PCA et PRA.
2. **Supervision** : mise en place d'un outil de monitoring temps réel.
3. **Automatisation** : production d'au moins un script d'automatisation.
4. **Résilience** : tests de robustesse et validation des procédures.

Ces ajouts accroissent la **résilience**, la **visibilité** et l'**efficacité** opérationnelle du système.

### 1.2 Méthodologie d'évaluation

Pour chaque amélioration, nous documentons :
- Le **problème adressé** (issu du retour d'expérience Phase II).
- La **solution implémentée**.
- Les **bénéfices attendus** et **indicateurs**.
- Les **tests** réalisés.

---

## 2. Améliorations apportées

### 2.1 Synthèse des améliorations

| Domaine | Avant Phase III | Après Phase III |
|---------|-----------------|-----------------|
| Supervision | Aucune | Wazuh SIEM avec 9 agents + dashboard temps réel |
| Sauvegardes | Aucune procédure formalisée | Backup automatique 6 services + rétention 30 jours + chiffrement GPG |
| Détection intrusions | Aucune | Suricata IDS sur OPNsense + intégration Wazuh |
| Protection brute force | Aucune | Fail2ban sur Bastion, Web-01, Mail-01 |
| Continuité documentée | Aucune | PCA + PRA + matrice 17 risques + procédures restauration |
| Création users AD | Manuelle (~5 min/user) | Script Python batch (5 min pour 85 users) |
| Surveillance disque | Aucune | Script `disk_alert.sh` avec alerting email |
| Honeypot | Aucun | Cowrie + intégration Wazuh (option bonus) |

### 2.2 Détail des ajouts

#### Ajout #1 — Système de supervision Wazuh
Cf. chapitre 3.

#### Ajout #2 — Scripts d'automatisation
Cf. chapitre 4.

#### Ajout #3 — Plans de continuité
Cf. chapitre 5 (document séparé : `PCA_PRA_Nova_Syndicate.md`).

#### Ajout #4 — Détection des intrusions
Activation de **Suricata** sur l'interface WAN d'OPNsense Lyon avec :
- **Ruleset Emerging Threats Open** (~30 000 règles à jour).
- **Mode IDS** (alerting only, pas de blocage actif).
- **Forward des alertes** vers Wazuh via syslog.

#### Ajout #5 — Protection brute force
Déploiement de **Fail2ban** sur les hôtes exposés :
- **Bastion-01** : protection SSH (banni après 5 échecs en 10 min, durée 1h).
- **Web-01 + Proxy-01** : protection HTTP/HTTPS (anti-scan).
- **Mail-01** : protection SMTP AUTH (anti-brute force).

Les bans génèrent un log local + un événement Wazuh.

---

## 3. Outil de supervision déployé

### 3.1 Choix justifié

**Wazuh 4.x** a été retenu (étude détaillée dans le rapport de veille technologique). Les principaux atouts :
- Convergence SIEM + EDR dans un seul outil.
- Coût licence nul (open-source GPL2).
- 5 000+ règles MITRE ATT&CK pré-construites.
- Dashboard intégré (OpenSearch).
- Communauté active, releases régulières.

### 3.2 Architecture de déploiement

- **Wazuh-01** : 4 GB RAM, 2 vCPUs, 50 GB disque.
- Composants installés : Manager + Indexer + Dashboard (single-server).
- **Double interface réseau** :
  - `eth0` (10.1.10.20, vmbr1 VLAN 10) : management + collecte SERVERS.
  - `eth1` (10.0.5.20, vmbr5) : collecte DMZ + Quarantaine (séparation physique des flux).

### 3.3 Agents déployés

| Hôte | Rôle | Type d'événements collectés |
|------|------|-------------------------------|
| DC01-Lyon | Authentification AD | Logs Samba, événements sécurité Windows-like |
| Proxy-01 | Reverse proxy | Logs Nginx (access + error) |
| Web-01 | Site web | Logs Apache, logs PHP |
| DB-01 | Base MariaDB | Logs MariaDB, requêtes lentes |
| File-01 | Nextcloud | Logs Nextcloud, FIM `/var/lib/nextcloud/data` |
| Mail-01 | Messagerie | Logs Postfix, Dovecot, authentifications |
| Backup-01 | Sauvegardes | Résultats des backups, intégrité fichiers |
| Bastion-01 | SSH jump | Logs SSHD, Fail2ban |
| Honeypot-01 | Leurre (bonus) | Tout — capteur de threat intel |

Total : **9 agents** dans la flotte initiale.

### 3.4 Règles et alertes activées

| Catégorie | Règles | Source |
|-----------|--------|--------|
| MITRE ATT&CK | 5 200+ | Wazuh ruleset officiel |
| PCI DSS | 230 | Wazuh Compliance |
| GDPR | 120 | Wazuh Compliance |
| Suricata enrichi | 30 000+ | Emerging Threats Open |
| FIM (intégrité) | Personnalisée | /etc/, /var/lib/nextcloud/data, configs sensibles |

### 3.5 Notifications

- **Email** : alertes haut niveau (severity > 10) vers `it-alerts@nova.local` (envoi via Mail-01).
- **Dashboard** : visualisation temps réel + historique.

### 3.6 Conformité SLA

Le SIEM permet de mesurer :
- **Disponibilité des services** (via heartbeat agents).
- **Temps de détection** d'un événement de sécurité (Mean Time To Detect, MTTD).
- **Conformité réglementaire** (rapports auto pour GDPR, PCI DSS).

---

## 4. Scripts d'automatisation

### 4.1 Inventaire des scripts livrés

| # | Script | Cible | Rôle |
|---|--------|-------|------|
| 1 | `01_create_ad_users.py` | DC01-Lyon | Création batch utilisateurs AD depuis CSV |
| 2 | `02_disk_alert.sh` | Toutes VMs | Surveillance disque + alerte email |
| 3 | `03_backup_orchestrator.sh` | Backup-01 | Orchestration sauvegardes quotidiennes |

### 4.2 Script #1 — Création utilisateurs AD

**Problème adressé** : la création manuelle de 85 utilisateurs prendrait ~5 min/user soit environ 7 heures de travail, avec risque d'erreurs (typos, oublis de groupes, OU incorrectes).

**Solution** : script Python idempotent qui :
- Lit un CSV (`username,firstname,lastname,email,department,manager,site`).
- Génère un mot de passe cryptographiquement sûr (`secrets`) de 16 caractères.
- Crée le compte via `samba-tool user create`.
- Place le compte dans la bonne OU selon le département.
- Ajoute le compte au bon groupe.
- Force le changement de mot de passe à la première connexion.
- Trace toutes les actions dans `/var/log/nova/create_users.log`.
- Sauve les mots de passe initiaux dans un fichier chiffrable.

**Mode dry-run** disponible pour simulation avant exécution réelle.

**Bénéfice mesuré** : 85 utilisateurs créés en **< 5 minutes** contre ~7 heures en manuel (gain ~98 %).

### 4.3 Script #2 — Alerte disque

**Problème adressé** : risque R-13 du PCA/PRA (disque plein sur VM hôte Proxmox). Une saturation disque sur DC01 ou DB-01 entraînerait une indisponibilité critique non détectée immédiatement.

**Solution** : script Bash en cron toutes les 10 minutes qui :
- Vérifie l'occupation de chaque partition montée.
- Émet une alerte au seuil **80 %** (warning) ou **90 %** (critical).
- Envoie un email à `it-alerts@nova.local` avec détail des plus gros dossiers.
- Forwarde l'événement vers Wazuh via `logger`/syslog.
- Implémente un **anti-spam** (cooldown 1h entre 2 alertes pour la même partition).

**Bénéfice attendu** : détection préventive 6-24 h avant saturation effective.

### 4.4 Script #3 — Orchestration des sauvegardes

**Problème adressé** : conformité à la politique 3-2-1 du PCA. Avant ce script : aucune sauvegarde automatisée → risque majeur de perte de données.

**Solution** : script Bash exécuté quotidiennement à 1h du matin sur Backup-01 qui :
- Sauvegarde **6 services** : Active Directory, MariaDB, Nextcloud, Mail, OPNsense (Lyon + Marseille), VMs Proxmox.
- **Chiffre** chaque archive en GPG asymétrique (clé publique pré-importée).
- Génère un **checksum SHA-256** pour vérification d'intégrité.
- Applique la **rétention 30 jours** automatique.
- Envoie un **rapport email** de succès/échec.
- Forwarde les événements vers Wazuh.

**Bénéfice** : automatisation complète d'une tâche critique. Conformité PCA garantie. Capacité de restauration en < 4 h.

### 4.5 Documentation et qualité

Chaque script présente :
- **En-tête** : objectif, auteur, date, version, référence.
- **Configuration** centralisée en haut de fichier.
- **Fonctions** documentées (docstrings Python ou commentaires Bash).
- **Logs** structurés avec niveau (info / warning / error).
- **Codes de retour** standards (0 OK, 1 erreur config, 2 erreur exécution).
- **Idempotence** : relance possible sans effet de bord.

---

## 5. Plans de continuité (PCA/PRA)

Document complet livré séparément : `04_pca_pra/PCA_PRA_Nova_Syndicate.md`.

### 5.1 Points marquants du PCA

- **Cellule de continuité** définie (5 rôles).
- **17 risques opérationnels** identifiés et cotés (matrice probabilité × impact).
- **11 services critiques** cartographiés avec RTO + RPO.
- **Procédures d'activation** détaillées (étape par étape).
- **Plan de tests** trimestriel + annuel.

### 5.2 Points marquants du PRA

- **5 scénarios de sinistre** documentés avec procédure de reprise.
- **Politique de sauvegarde 3-2-1** implémentée.
- **5 procédures de restauration** détaillées (AD, OPNsense, MariaDB, Nextcloud, VM générique).
- **Organisation de la cellule de crise** formalisée.
- **Calendrier de tests annuel** planifié.

### 5.3 Conformité ISO 22301 et ISO 27031

Les deux documents s'inscrivent dans les référentiels :
- **ISO 22301** (continuité d'activité) — exigences couvertes : contexte, leadership, planification, support, fonctionnement, évaluation, amélioration.
- **ISO 27031** (continuité IT) — alignement sur les recommandations.
- **ANSSI** — alignement sur le guide d'hygiène informatique.

---

## 6. Tests de robustesse réalisés

### 6.1 Tests fonctionnels

| Test | Procédure | Résultat |
|------|-----------|----------|
| Authentification AD depuis Marseille | Login Kerberos cross-site via IPsec | ✅ OK |
| Ping cross-site IPsec | Bastion (172.16.100.20) → DNS-Marseille (10.0.2.10) | ✅ OK (latence ~8ms) |
| Accès Nextcloud authentifié AD | Login navigateur avec compte AD | ✅ OK |
| Site web public via Proxy | https://web-01 via Proxy-01 | ✅ OK |
| Mail SMTP/IMAP | Envoi/réception entre comptes locaux | ✅ OK |
| Webmail Roundcube | Connexion + lecture mails | ✅ OK |
| SSH bastion depuis Internet | `ssh -p 2222 novaadmin@WAN` | ✅ OK |

### 6.2 Tests de sécurité (preuves de blocage)

| Test | Procédure | Résultat attendu | Résultat obtenu |
|------|-----------|-------------------|------------------|
| DMZ → Internet | `ping 8.8.8.8` depuis Web-01 | **BLOQUÉ** | ✅ TIMEOUT |
| USERS → SERVERS direct | `ssh dc01` depuis USERS (sans bastion) | **REFUSÉ** | ✅ Connection refused |
| Quarantaine → tout | ping depuis vmbr4 | **BLOQUÉ** | ✅ TIMEOUT |
| Brute force SSH | `hydra` depuis Internet sur 2222 | **DÉTECTÉ** | ✅ Alerte Wazuh + ban Fail2ban |
| Scan Nmap | `nmap -sV WAN_IP` | **DÉTECTÉ** | ✅ Alerte Suricata |
| Tentative login échouée AD | Mauvais mot de passe répétitif | **LOG + ALERTE** | ✅ Visible dashboard Wazuh |

### 6.3 Tests de continuité (PCA)

| Test | Scénario | Résultat |
|------|----------|----------|
| Coupure tunnel IPsec | Arrêt OPNsense Marseille 5 min | DNS Marseille bind9 sert le cache → OK |
| Restauration backup MariaDB | Suppression DB + restauration depuis dump | RTO 12 min mesuré (cible 4h) ✅ |
| Restauration config OPNsense | Reset à neuf + import XML | RTO 25 min mesuré (cible 30 min) ✅ |
| Snapshot rollback Proxmox | Rollback DC01 vers snapshot précédent | RTO < 5 min ✅ |

---

## 7. Indicateurs de performance

### 7.1 KPI techniques

| Indicateur | Valeur mesurée | Cible |
|------------|-----------------|-------|
| Disponibilité globale infrastructure | 99,7 % | 99,5 % ✅ |
| Latence IPsec Lyon-Marseille | 8 ms (moyenne 0% loss) | < 50 ms ✅ |
| Temps de détection alerte Wazuh | < 30 s | < 2 min ✅ |
| Temps moyen restauration VM (vzdump) | 12 min | < 4 h ✅ |
| Couverture agents Wazuh | 9/9 (100 %) | 100 % ✅ |
| Volume logs Wazuh / jour | ~150 MB | — |
| Backups quotidiens réussis | 6/6 services | 6/6 ✅ |
| Incidents techniques durant build | 12 (tous résolus) | — |

### 7.2 KPI processus

| Indicateur | Valeur |
|------------|--------|
| Documentation produite | 10 livrables (~150 pages cumulées) |
| Scripts d'automatisation livrés | 3 (création users, monitoring disque, backups) |
| POC captures écran | 25 numérotées et légendées |
| Procédures opérationnelles | 8 documentées (PCA + PRA + exploitation) |
| Risques identifiés et cotés | 17 |
| Tests fonctionnels validés | 13/13 |
| Tests de blocage validés | 6/6 |

---

## 8. Recommandations pour la suite

### 8.1 Améliorations à court terme (3 mois)

1. **Externaliser une copie de sauvegarde hors-site** (OVH Cloud Storage ou Scaleway Object Storage, ~5 €/mois pour 100 GB).
2. **Activer MFA sur OpenVPN** (Google Authenticator ou TOTP via plugin OPNsense).
3. **Migrer SSH Bastion en authentification par clé uniquement** (désactiver password).
4. **Mettre en place certificats Let's Encrypt** sur Proxy-01 (remplacer auto-signé).
5. **Activer Suricata en mode IPS** (blocage actif) après période d'observation IDS.

### 8.2 Améliorations à moyen terme (6-12 mois)

1. **Mettre en place un DC secondaire** (Samba 4 second DC ou Windows Server) pour vraie continuité AD.
2. **Liaison Internet directe à Marseille** + split-tunneling (libère Marseille de la dépendance Lyon).
3. **Migrer vers OpenVPN profils utilisateurs individuels** (révocation granulaire).
4. **Mettre en place un PKI interne** pour certificats utilisateurs (auth forte).
5. **Tests de pénétration externes annuels** par cabinet certifié.

### 8.3 Améliorations stratégiques (12-24 mois)

1. **Migration progressive vers Kubernetes** pour les services applicatifs (Web, DB, Nextcloud).
2. **Intégration de l'authentification SAML/OIDC** (SSO inter-applications).
3. **Mise en place d'un SOC managé** (ou externalisation Wazuh à un MSSP).
4. **Plan de transformation cloud hybride** (workloads de pointe sur AWS/Azure).
5. **Certification ISO 27001** de l'organisation.

---

## CONCLUSION

La Phase III a permis de transformer une infrastructure simplement fonctionnelle (Phase II) en une infrastructure **résiliente, observable et automatisée**. Les trois ajouts majeurs (supervision Wazuh, scripts d'automatisation, plans PCA/PRA) constituent les fondations d'une **gouvernance IT mature** pour Nova Syndicate.

Le client dispose désormais de :
- Une **visibilité temps réel** sur l'état de son infrastructure.
- Des **procédures formalisées** de continuité et reprise.
- Une **automatisation** des tâches critiques répétitives.
- Une **documentation exhaustive** transmise à l'équipe interne.

Les **bénéfices mesurés** par rapport à la situation initiale :
- Réduction du temps de détection des incidents : de **plusieurs jours à temps réel**.
- Réduction du temps de provisioning de comptes : de **7 heures à 5 minutes** (gain 98 %).
- Conformité acquise aux principes ANSSI d'hygiène informatique.
- TCO 3 ans maintenu à **14 700 €** contre 132 920 € en solution propriétaire (-89 %).

L'infrastructure est prête à supporter la **croissance prévue de +30 %/an** sans refonte d'architecture.

---

**Document arrêté à la version 1.0** — Mai 2026

*Ce document clôt la Phase III du projet de modernisation Nova Syndicate.*
