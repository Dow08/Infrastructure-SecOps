# PLAN DE CONTINUITÉ D'ACTIVITÉ (PCA)
# & PLAN DE REPRISE APRÈS SINISTRE (PRA)

## Client : Nova Syndicate

---

**Référence document** : NS-2026-004
**Auteur** : Dorian Poncelet — Responsable Technique
**Date** : Mai 2026
**Version** : 1.0
**Statut** : Livrable Phase III — Continuité et Résilience
**Classification** : Confidentiel – Diffusion restreinte client
**Cadre normatif** : ISO 22301 (Continuité) — ISO 27031 (Reprise IT)

---

## SOMMAIRE

### PARTIE A — PLAN DE CONTINUITÉ D'ACTIVITÉ (PCA)

1. [Objet du PCA](#1-objet-du-pca)
2. [Organisation de la continuité](#2-organisation-de-la-continuité)
3. [Analyse d'impact métier (BIA)](#3-analyse-dimpact-métier-bia)
4. [Matrice des risques](#4-matrice-des-risques)
5. [Stratégies de continuité par service](#5-stratégies-de-continuité-par-service)
6. [Procédures opérationnelles de continuité](#6-procédures-opérationnelles-de-continuité)
7. [Tests et maintenance du PCA](#7-tests-et-maintenance-du-pca)

### PARTIE B — PLAN DE REPRISE APRÈS SINISTRE (PRA)

8. [Objet du PRA](#8-objet-du-pra)
9. [Scénarios de sinistre couverts](#9-scénarios-de-sinistre-couverts)
10. [Stratégie de sauvegarde](#10-stratégie-de-sauvegarde)
11. [Procédures de restauration](#11-procédures-de-restauration)
12. [Organisation de la cellule de crise](#12-organisation-de-la-cellule-de-crise)
13. [Tests de PRA](#13-tests-de-pra)

---

# PARTIE A — PLAN DE CONTINUITÉ D'ACTIVITÉ (PCA)

## 1. Objet du PCA

### 1.1 Définition

Le **Plan de Continuité d'Activité** (PCA) est l'ensemble organisé des procédures, ressources et compétences permettant à Nova Syndicate de **maintenir un niveau de service acceptable** pendant et après un incident perturbant son activité normale.

### 1.2 Périmètre

Le présent PCA couvre :
- L'**infrastructure informatique** déployée dans le cadre de la mission.
- Les **services métiers critiques** identifiés conjointement avec la direction client.
- Les **deux sites** Nova Syndicate (Lyon HQ et Marseille agence).
- Les **accès distants** des 20 commerciaux itinérants.

Hors périmètre :
- La continuité des locaux physiques (gérée par les services généraux).
- La continuité des fournisseurs externes (M365 SaaS, opérateurs télécom).

### 1.3 Objectifs stratégiques

| Objectif | Indicateur cible |
|----------|------------------|
| Maintenir l'activité commerciale en cas d'incident majeur | Disponibilité du portail web > 99,5 % |
| Préserver l'intégrité des données critiques | Aucune perte > 24 h de données métier |
| Garantir la traçabilité réglementaire (médical/aéro/défense) | 100 % des logs SIEM conservés 12 mois |
| Permettre le télétravail des collaborateurs Lyon en cas d'incident site | Capacité VPN remote pour 40 utilisateurs |

---

## 2. Organisation de la continuité

### 2.1 Cellule de continuité

| Rôle | Désignation | Responsabilités |
|------|-------------|-----------------|
| **Directeur de la continuité (DC)** | Direction générale Nova Syndicate | Décision déclenchement PCA / PRA |
| **Responsable IT** | DSI Nova Syndicate (à recruter / interne) | Coordination technique opérationnelle |
| **Référent sécurité** | RSSI ou équivalent | Communication ANSSI / CNIL / clients défense |
| **Référent métier** | Directeurs commerciaux Lyon/Marseille | Priorisation des services à rétablir |
| **Référent communication** | Direction communication | Information clients, fournisseurs, salariés |

### 2.2 Procédure d'alerte

1. **Détection** : alerte Wazuh / appel utilisateur / panne constatée.
2. **Notification immédiate** : SMS + email cellule de continuité (annuaire en annexe).
3. **Évaluation** : qualification de l'incident (mineur / majeur / sinistre).
4. **Déclenchement** : décision du DC sur activation PCA et/ou PRA.
5. **Mise en œuvre** : exécution des procédures par le responsable IT.
6. **Reporting** : compte-rendu horaire pendant la crise, post-mortem ensuite.

### 2.3 Critères de déclenchement

| Niveau | Critères | Action |
|--------|---------|--------|
| **Mineur** | Service indisponible < 1 h, aucune perte donnée | Procédure standard d'exploitation |
| **Majeur** | Service indisponible 1 h – 4 h, perte limitée | Activation partielle PCA |
| **Sinistre** | Indisponibilité > 4 h ou perte données critique | Activation PCA complet + PRA |

---

## 3. Analyse d'impact métier (BIA)

### 3.1 Méthodologie

L'analyse d'impact métier (Business Impact Analysis) évalue pour chaque service :
- Son **RTO** (Recovery Time Objective) : temps maximum tolérable d'interruption.
- Son **RPO** (Recovery Point Objective) : perte maximale de données tolérable.
- Son **impact financier** sur l'activité.
- Son **impact réglementaire** (RGPD, sectoriel).

### 3.2 Cartographie des services critiques

| Service | Composant | Criticité | RTO | RPO | Impact 24h interruption |
|---------|-----------|-----------|-----|-----|--------------------------|
| Active Directory | DC01-Lyon | ★★★ Critique | 2 h | 1 h | Impossible se connecter aux postes |
| Base de données métier | DB-01 | ★★★ Critique | 4 h | 1 h | Catalogue indisponible, ventes bloquées |
| Portail web public | Web-01 + Proxy-01 | ★★ Haute | 4 h | 4 h | Image dégradée, perte CA estimée 5 000 €/jour |
| Partage de fichiers | File-01 (Nextcloud) | ★★★ Critique | 4 h | 4 h | Collaboration interne bloquée |
| Messagerie | Mail-01 | ★★ Haute | 8 h | 1 h | Communication client interrompue |
| Supervision SIEM | Wazuh-01 | ★★ Haute | 8 h | 24 h | Cécité sur incidents sécurité |
| VPN commerciaux | OpenVPN sur OPNsense Lyon | ★★★ Critique | 4 h | N/A (sans état) | 20 commerciaux isolés |
| Tunnel IPsec Lyon-Marseille | OPNsense Lyon + Marseille | ★★ Haute | 4 h | N/A | Marseille perd Internet et AD |
| Sauvegardes | Backup-01 | ★ Modérée | 24 h | N/A | Décalage planning de backup |
| Bastion SSH | Bastion-01 | ★★ Haute | 8 h | N/A | Impossible administrer à distance |
| Honeypot | Honeypot-01 / Cowrie | ★ Modérée | 48 h | N/A | Perte d'un capteur de threat intelligence |

### 3.3 Indicateurs de niveau de service (SLA)

| Service | SLA disponibilité visée | Mesure |
|---------|--------------------------|--------|
| Portail web public | 99,9 % | Sonde externe + Wazuh |
| Active Directory | 99,5 % | Wazuh agent + samba-tool |
| Base de données | 99,5 % | Wazuh agent + script SQL test |
| Partage de fichiers | 99,5 % | Sonde Nextcloud occ status |
| VPN | 99 % | Logs OpenVPN OPNsense |

---

## 4. Matrice des risques

### 4.1 Grille d'évaluation

| Probabilité | Description |
|-------------|-------------|
| P1 — Très faible | < 1 occurrence par 5 ans |
| P2 — Faible | 1 occurrence par 2-5 ans |
| P3 — Moyenne | 1 occurrence par an |
| P4 — Forte | Plusieurs fois par an |
| P5 — Très forte | Plusieurs fois par mois |

| Impact | Description |
|--------|-------------|
| I1 — Mineur | Interruption < 1h, pas de perte donnée |
| I2 — Modéré | Interruption 1-4h, perte donnée < 1h |
| I3 — Majeur | Interruption 4-24h, perte donnée < 24h |
| I4 — Critique | Interruption > 24h ou perte donnée majeure |
| I5 — Catastrophique | Perte définitive ou impact réglementaire majeur |

**Niveau de risque** = Probabilité × Impact

### 4.2 Matrice des risques opérationnels

| ID | Risque | Probabilité | Impact | Niveau | Stratégie | Mitigation |
|----|--------|-------------|--------|--------|-----------|------------|
| R-01 | Panne hardware serveur Proxmox | P3 | I4 | **Élevé** | Réduire | Sauvegarde quotidienne + image OS clonable |
| R-02 | Coupure Internet site Lyon | P3 | I3 | **Élevé** | Accepter | Communication aux utilisateurs, télétravail temporaire |
| R-03 | Coupure tunnel IPsec Lyon-Marseille | P3 | I2 | **Modéré** | Réduire | Cache DNS bind9 à Marseille + Kerberos tickets |
| R-04 | Corruption base de données | P2 | I4 | **Modéré** | Réduire | Backup horaire (mysqldump) + binlog |
| R-05 | Compromission Bastion-01 | P2 | I5 | **Élevé** | Réduire | Fail2ban + clé SSH uniquement + audit Wazuh |
| R-06 | Compromission DC01-Lyon | P2 | I5 | **Élevé** | Réduire | Pas d'exposition Internet + monitoring AD changes |
| R-07 | Brute force OpenVPN | P4 | I3 | **Élevé** | Réduire | Auth AD + Fail2ban + MFA (futur) |
| R-08 | DDoS sur portail web | P3 | I3 | **Élevé** | Réduire | Rate limiting OPNsense + Suricata + CDN externe |
| R-09 | Ransomware sur File-01 (Nextcloud) | P3 | I5 | **Élevé** | Réduire | Backup quotidien isolé + versioning Nextcloud |
| R-10 | Erreur humaine config OPNsense | P4 | I3 | **Élevé** | Réduire | Snapshot config avant chaque modif + export XML versionné |
| R-11 | Sinistre physique site Lyon | P1 | I5 | **Modéré** | Transférer | Assurance + cloud backup externalisé (à mettre en place) |
| R-12 | Erreur humaine suppression user AD | P4 | I2 | **Modéré** | Réduire | Audit log Samba + recyclage 30j AD bin |
| R-13 | Disque plein sur VM hôte Proxmox | P3 | I3 | **Élevé** | Réduire | Script monitoring `disk_alert.sh` + LVM extensible |
| R-14 | Vol matériel (portable commercial) | P3 | I3 | **Élevé** | Réduire | Chiffrement disque + révocation cert VPN |
| R-15 | Mise à jour cassante OS | P3 | I3 | **Élevé** | Réduire | Snapshot avant `apt upgrade` + canary 1 VM avant flotte |
| R-16 | Saturation logs Wazuh | P3 | I2 | **Modéré** | Réduire | Rotation logs + alerte espace disque |
| R-17 | Vulnérabilité zero-day OPNsense | P2 | I4 | **Modéré** | Réduire | Veille sécu + patch < 7 jours |

### 4.3 Cartographie visuelle des risques

```
Impact                                                                
  I5  │   R-11        R-09        R-05/R-06              
  I4  │   R-15        R-04        R-01/R-17              
  I3  │   R-15        R-02/R-13   R-08/R-10/R-14         R-07
  I2  │              R-03        R-16                     R-12
  I1  │              
      └──────────────────────────────────────────────────────
        P1          P2          P3          P4          P5
                              Probabilité
```

---

## 5. Stratégies de continuité par service

### 5.1 Continuité de l'Active Directory

**Scénario** : DC01-Lyon hors service ou tunnel IPsec coupé.

**Réponse à l'incident** :
- Marseille : sessions Kerberos actives restent valides jusqu'à expiration du TGT (généralement 8-10 h).
- Marseille : DNS-Marseille (bind9) sert les résolutions en cache.
- Lyon : si DC01 KO, **aucun nouveau login possible** → activation procédure PRA-AD (restauration depuis Backup-01).

**Limitation acceptée** : pas de DC secondaire en mode RODC (Samba 4 ne le supporte pas pleinement). En cas d'évolution, prévoir Windows Server pour mode RODC complet.

**Mesures d'atténuation** :
- Sauvegarde quotidienne Samba (`samba_backup_online`).
- Snapshot Proxmox de DC01 toutes les 6 heures.
- Procédure de restauration documentée (cf. §11.2).

### 5.2 Continuité du portail web

**Scénario** : Web-01 ou Proxy-01 hors service.

**Réponse à l'incident** :
- Si Web-01 KO : page de maintenance servie par Proxy-01 (fichier statique embarqué).
- Si Proxy-01 KO : fail-over manuel vers Web-01 en exposition directe (procédure documentée).
- Si DB-01 KO : portail en mode dégradé (lecture seule sur cache + retry).

**Mesures d'atténuation** :
- Backup horaire de la base MariaDB (Phase III).
- Snapshot Proxmox quotidien des 2 VMs.
- Configuration nginx versionnée Git.

### 5.3 Continuité du partage de fichiers

**Scénario** : File-01 (Nextcloud) hors service.

**Réponse à l'incident** :
- Versioning Nextcloud natif (rétention 30 jours) → restauration self-service utilisateur.
- Backup nocturne sur Backup-01 (rsync + crypté).
- Procédure de restauration de fichier individuel < 15 min.

**Mesures d'atténuation** :
- Backup quotidien complet vers Backup-01.
- Snapshot Proxmox quotidien.
- Surveillance espace disque (script `disk_alert.sh`).

### 5.4 Continuité de la messagerie

**Scénario** : Mail-01 hors service.

**Réponse à l'incident** :
- Réception : Postfix retry automatique pendant 5 jours côté émetteur externe.
- Émission : impossibilité d'émettre pendant l'indisponibilité (acceptable < 8 h).
- Webmail Roundcube indisponible → utilisation client lourd local (cache local).

**Mesures d'atténuation** :
- Snapshot Proxmox quotidien.
- Backup maildirs (Backup-01).
- Procédure de restauration complète documentée.

### 5.5 Continuité de l'accès distant (VPN commerciaux)

**Scénario** : OPNsense Lyon hors service → 20 commerciaux isolés.

**Réponse à l'incident** :
- Sessions VPN en cours : déconnectées immédiatement.
- Nouvelles connexions : impossibles tant que OPNsense Lyon n'est pas relevé.
- Configuration OPNsense exportée XML → restauration en 30 minutes sur nouvelle VM.

**Mesures d'atténuation** :
- Export XML OPNsense versionné Git après chaque modification (script à automatiser).
- Snapshot Proxmox quotidien.
- Procédure de réinstallation OPNsense documentée (cf. PRA §11.3).

### 5.6 Continuité inter-sites Lyon-Marseille

**Scénario** : tunnel IPsec coupé (panne Internet d'un côté ou config).

**Réponse à l'incident** :
- Marseille : DNS local bind9 sert le cache → tickets Kerberos restent valides.
- Marseille : pas d'Internet (Hub & Spoke) → utilisation 4G/5G backup.
- Lyon : non impacté.

**Limitation acceptée** : Marseille n'a pas de liaison Internet directe. En cas d'évolution, prévoir split-tunneling + liaison ADSL/4G de secours.

---

## 6. Procédures opérationnelles de continuité

### 6.1 Procédure d'activation du PCA

```
ÉTAPE 1 — Évaluation initiale (< 15 min)
  └── Responsable IT évalue : impact, durée estimée, périmètre.

ÉTAPE 2 — Notification cellule (< 30 min)
  └── SMS + email à : DC, RSSI, référents métier.

ÉTAPE 3 — Décision déclenchement (< 1 h)
  └── DC valide ou ajuste le niveau d'activation.

ÉTAPE 4 — Mise en œuvre (< 2 h pour services critiques)
  └── Exécution procédures par responsable IT.
  └── Communication interne (chat / email de masse).

ÉTAPE 5 — Suivi crise (toutes les heures)
  └── Reporting horaire au DC.
  └── Communication client/fournisseur si nécessaire.

ÉTAPE 6 — Retour à la normale
  └── Validation par DC.
  └── Communication de fin de crise.

ÉTAPE 7 — Post-mortem (< 5 jours ouvrés)
  └── Analyse causale.
  └── Mise à jour du PCA si besoin.
```

### 6.2 Tableau de contacts d'urgence

| Rôle | Nom | Téléphone | Email | Disponibilité |
|------|-----|-----------|-------|---------------|
| DC (Direction) | [à compléter] | [à compléter] | [à compléter] | 24/7 |
| Responsable IT | [à compléter] | [à compléter] | [à compléter] | H24 astreinte |
| RSSI | [à compléter] | [à compléter] | [à compléter] | Heures ouvrées + astreinte |
| Hébergeur | Cabinet Mission | — | — | Heures ouvrées |
| Opérateur télécom | [opérateur] | [à compléter] | — | 24/7 |

---

## 7. Tests et maintenance du PCA

### 7.1 Plan de tests

| Test | Fréquence | Type | Responsable |
|------|-----------|------|-------------|
| Test restauration AD | Trimestrielle | Réel (sur VM test) | Responsable IT |
| Test restauration BDD | Trimestrielle | Réel | Responsable IT |
| Test bascule VPN | Semestrielle | Théorique (cellule réunie) | RSSI |
| Test communication crise | Annuelle | Exercice complet | DC |
| Test PRA complet | Annuelle | Exercice complet | DC + IT |

### 7.2 Maintenance documentaire

- **Mise à jour du PCA** : à chaque modification d'architecture (immédiat).
- **Revue complète** : annuelle.
- **Validation** : par le DC avec compte-rendu écrit.
- **Diffusion contrôlée** : version courante seulement accessible à la cellule.

---

# PARTIE B — PLAN DE REPRISE APRÈS SINISTRE (PRA)

## 8. Objet du PRA

### 8.1 Définition

Le **Plan de Reprise après Sinistre** (PRA) est l'ensemble des procédures techniques permettant de **rétablir l'infrastructure informatique** après un sinistre majeur ayant rendu indisponible une partie ou la totalité du système.

### 8.2 Distinction PCA / PRA

| Aspect | PCA | PRA |
|--------|-----|-----|
| Focus | Maintien d'activité pendant l'incident | Reconstruction technique post-incident |
| Horizon | Court terme (heures à jours) | Moyen terme (heures à semaines) |
| Périmètre | Métier + IT | IT principalement |
| Responsable | Direction (DC) | Responsable IT |

---

## 9. Scénarios de sinistre couverts

### 9.1 Scénario S-01 — Panne hardware Proxmox host

**Description** : le serveur physique hébergeant Proxmox tombe en panne (disque, CPU, alimentation).

**Conséquence** : toutes les VMs s'arrêtent simultanément.

**Procédure de reprise** :
1. Diagnostic hardware → remplacement composant (< 24 h chez prestataire local).
2. Remontage Proxmox à partir de l'image système (USB de récupération).
3. Restauration des VMs depuis Backup-01 (export `vzdump` quotidien).
4. Reconfiguration réseau via Terraform / import XML OPNsense.
5. Reprise progressive des services selon ordre de priorité (AD → DB → reste).

**RTO** : 8 heures.
**RPO** : 24 heures (dernière sauvegarde nocturne).

### 9.2 Scénario S-02 — Corruption logique d'une VM

**Description** : une VM ne boote plus suite à une mise à jour ou corruption.

**Procédure de reprise** :
1. Snapshot Proxmox antérieur → rollback (< 5 min).
2. Si pas de snapshot : restauration depuis `vzdump` (15-30 min).
3. Test fonctionnel.
4. Reprise des services.

**RTO** : 1 heure.
**RPO** : variable selon dernière sauvegarde.

### 9.3 Scénario S-03 — Compromission majeure (ransomware)

**Description** : chiffrement malveillant d'une ou plusieurs VMs.

**Procédure de reprise** :
1. **Isolation immédiate** : OPNsense → bloquer la VM compromise (vmbr4 quarantaine).
2. **Notification** : RSSI → CNIL (RGPD) + ANSSI (selon classification données).
3. **Analyse forensique** : capture snapshot RAM + disque pour investigation.
4. **Reconstruction propre** : NE PAS restaurer un backup post-compromission.
5. **Audit complet** : Wazuh logs sur les 30 derniers jours.
6. **Rotation des secrets** : tous mots de passe + clés SSH renouvelés.
7. **Communication client** : si données clients impactées (notification < 72 h RGPD).

**RTO** : 24-72 heures.
**RPO** : variable (dernier backup propre).

### 9.4 Scénario S-04 — Sinistre site Lyon (incendie/inondation)

**Description** : site Lyon complètement inutilisable.

**Procédure de reprise** :
1. Cellule de crise réunie en moins de 4 h.
2. Activation hébergement de secours (cloud externalisé — à mettre en place).
3. Restauration depuis backup distant (hors site).
4. Communication clients (notification commerciale).
5. Reconstruction infrastructure (plusieurs jours).

**RTO** : 48-72 heures (objectif si backup externalisé en place).
**RPO** : 24 heures.

**Mesure d'amélioration recommandée** : externaliser une copie chiffrée des sauvegardes vers un stockage cloud (S3-compatible, hébergement français — OVH, Scaleway).

### 9.5 Scénario S-05 — Erreur humaine destructive

**Description** : suppression accidentelle de données, mauvaise commande, mauvaise configuration.

**Procédure de reprise** :
1. Snapshot ou backup → restauration directe.
2. Procédures variées selon le service impacté.

**RTO** : < 4 heures.

---

## 10. Stratégie de sauvegarde

### 10.1 Politique 3-2-1 (cible)

- **3 copies** des données :
  - 1 copie primaire (VM en production).
  - 1 copie sur Backup-01 (différent VLAN, vmbr1 mais isolé par firewall).
  - 1 copie hors site (à mettre en place — cloud OVH par exemple).
- **2 supports différents** : disques VM + backup distant.
- **1 copie hors site** : externalisation cloud chiffrée (recommandation à valider).

### 10.2 Plan de sauvegarde détaillé

| Donnée | Outil | Fréquence | Rétention | Cible | Chiffrement |
|--------|-------|-----------|-----------|-------|-------------|
| Base MariaDB | `mysqldump` + binlog | Horaire (binlog) + Quotidien (dump) | 30 jours | Backup-01 | AES-256 (gpg) |
| Active Directory Samba | `samba_backup_online` | Quotidien (3h) | 30 jours | Backup-01 | AES-256 |
| File-01 (Nextcloud data) | `rsync --delete-after` | Quotidien (2h) | 30 jours | Backup-01 | AES-256 |
| Mail-01 (Maildirs) | `rsync` | Quotidien (3h) | 30 jours | Backup-01 | AES-256 |
| Config OPNsense (XML) | Export GUI + Git push | Manuel + après modif | Illimité | Git + Backup-01 | TLS Git |
| Snapshots Proxmox | `vzdump` PVE | Quotidien (1h) | 7 jours | Local-lvm + Backup-01 | AES-256 |
| Logs Wazuh | rotation logrotate | Quotidien | 12 mois | Backup-01 | AES-256 |

### 10.3 Configuration cron Backup-01

Voir script `06_scripts_automation/backup_orchestrator.sh` pour orchestration complète.

Extrait synthétique :
```bash
# /etc/cron.d/nova-backups
0  1  * * *  root  /usr/local/bin/backup_proxmox.sh
0  2  * * *  root  /usr/local/bin/backup_nextcloud.sh
0  3  * * *  root  /usr/local/bin/backup_samba.sh
0  3  * * *  root  /usr/local/bin/backup_mail.sh
0  *  * * *  root  /usr/local/bin/backup_mariadb_binlog.sh
```

### 10.4 Tests de restauration

**Tests trimestriels obligatoires** :
- Restauration d'un fichier Nextcloud aléatoire.
- Restauration d'une table MariaDB.
- Restauration complète d'une VM (sandbox).

**Test annuel** :
- Restauration de l'intégralité de l'infrastructure dans un environnement secondaire.

---

## 11. Procédures de restauration

### 11.1 Procédure générale de restauration d'une VM

```
ÉTAPE 1 — Constat de l'incident
  └── Identification VM impactée + nature panne.

ÉTAPE 2 — Décision de restauration
  └── Snapshot disponible ?
        OUI → ÉTAPE 3a (rollback)
        NON → ÉTAPE 3b (restore vzdump)

ÉTAPE 3a — Rollback snapshot
  └── Proxmox GUI : VM → Snapshots → Rollback
  └── Démarrer VM, vérifier services.

ÉTAPE 3b — Restauration vzdump
  └── ls /var/lib/vz/dump/ → identifier backup le plus récent.
  └── qmrestore /var/lib/vz/dump/<backup>.vma.zst <vmid>
  └── qm start <vmid>
  └── Vérifier services.

ÉTAPE 4 — Tests fonctionnels
  └── Selon nature de la VM (cf. checklist par service).

ÉTAPE 5 — Levée d'alerte
  └── Communication aux utilisateurs.
  └── Mise à jour ticket incident.
```

### 11.2 Procédure restauration Active Directory (DC01-Lyon)

**Cas standard — restauration vzdump récent** :
```bash
# Sur Proxmox host
qm stop 102 --skiplock 1
qmrestore /var/lib/vz/dump/vzdump-qemu-102-<date>.vma.zst 102 --force 1
qm start 102

# Sur DC01-Lyon (après boot)
sudo samba-tool dbcheck --cross-ncs
sudo samba-tool domain info nova.local
sudo systemctl status samba-ad-dc
```

**Cas avancé — restauration depuis backup Samba** :
```bash
# Sur Backup-01
scp /backup/samba/samba-backup-<date>.tar.gz dc01:/tmp/

# Sur DC01-Lyon
sudo systemctl stop samba-ad-dc
cd /var/lib/samba
sudo tar xzf /tmp/samba-backup-<date>.tar.gz
sudo systemctl start samba-ad-dc
sudo samba-tool dbcheck --cross-ncs
```

### 11.3 Procédure restauration OPNsense

**Cas — réinstallation à partir XML config** :
1. Télécharger ISO OPNsense 26.x.
2. Créer nouvelle VM Proxmox identique (CPU, RAM, interfaces).
3. Booter sur ISO, installer OPNsense.
4. Sur OPNsense fresh install : System → Configuration → Backups → Restore → uploader le XML versionné Git.
5. Reboot.
6. Vérifier interfaces, règles, IPsec, NAT.

**Temps total estimé** : 30 minutes.

### 11.4 Procédure restauration MariaDB

```bash
# Sur DB-01

# 1. Stopper MariaDB
sudo systemctl stop mariadb

# 2. Restaurer le dernier dump complet
sudo gunzip < /backup/mysql/full-<date>.sql.gz | mysql -u root -p

# 3. Rejouer les binlogs depuis le dernier dump
mysqlbinlog /backup/mysql/binlog.* | mysql -u root -p

# 4. Démarrer et tester
sudo systemctl start mariadb
mysql -u root -p -e "SHOW DATABASES;"
```

### 11.5 Procédure restauration Nextcloud

```bash
# Sur File-01

# 1. Mode maintenance
sudo -u www-data php /var/www/nextcloud/occ maintenance:mode --on

# 2. Restaurer base
mysql nextcloud < /backup/nextcloud/db-<date>.sql

# 3. Restaurer fichiers
rsync -a /backup/nextcloud/data/ /var/lib/nextcloud/data/
sudo chown -R www-data:www-data /var/lib/nextcloud/data

# 4. Vérifier
sudo -u www-data php /var/www/nextcloud/occ files:scan --all

# 5. Sortir mode maintenance
sudo -u www-data php /var/www/nextcloud/occ maintenance:mode --off
```

---

## 12. Organisation de la cellule de crise

### 12.1 Activation

La cellule de crise est activée par le DC dès qu'un sinistre est qualifié (cf. §2.3).

### 12.2 Composition et rôles

| Membre | Mission pendant la crise |
|--------|--------------------------|
| DC | Pilotage global, décisions majeures, communication externe |
| Responsable IT | Exécution technique des procédures PRA |
| RSSI | Liaison RGPD/CNIL/ANSSI selon nature incident |
| Référent métier | Priorisation services, communication interne |
| Référent communication | Information clients, médias si nécessaire |

### 12.3 Outils de coordination

- Salle de crise dédiée (Lyon, salle de réunion principale).
- Tableau blanc / paperboard pour traçabilité décisions.
- Téléphones (lignes fixes + 2 portables d'astreinte chargés).
- Tablette / laptop avec accès Wazuh + Proxmox + Notion (documentation).

### 12.4 Reporting

- **Compte-rendu horaire** : du responsable IT vers le DC.
- **Communication client** : préparée par RC, validée par DC.
- **Journal de bord** : tenu en direct (timestamp + action + résultat).

---

## 13. Tests de PRA

### 13.1 Plan de tests annuel

| Trimestre | Test | Périmètre |
|-----------|------|-----------|
| Q1 | Restauration AD | DC01-Lyon dans environnement test |
| Q2 | Restauration BDD | DB-01 dans environnement test |
| Q3 | Restauration OPNsense | Réinstall complète depuis XML |
| Q4 | Test PRA complet | Reconstruction infra dans Proxmox secondaire |

### 13.2 Critères de réussite

- Procédure documentée suivie sans modification ad-hoc.
- RTO respecté.
- RPO respecté.
- Services testés fonctionnels (checklists).
- Post-mortem rédigé sous 5 jours ouvrés.

### 13.3 Indicateurs de performance du PRA

- **Taux de succès** des tests trimestriels : cible 100 %.
- **Délai moyen de restauration** : à mesurer sur 1 an de tests.
- **Couverture documentaire** : 100 % des services critiques avec procédure validée.

---

## ANNEXES

### Annexe A — Glossaire

- **BIA** (*Business Impact Analysis*) : Analyse d'impact métier.
- **DC** (*Disaster Controller* / Directeur de Continuité) : Responsable du déclenchement PCA/PRA.
- **PCA** : Plan de Continuité d'Activité.
- **PRA** : Plan de Reprise après Sinistre.
- **RPO** (*Recovery Point Objective*) : Perte de données maximale tolérée.
- **RTO** (*Recovery Time Objective*) : Temps de reprise maximal toléré.
- **SLA** (*Service Level Agreement*) : Engagement de niveau de service.

### Annexe B — Documents de référence

- ISO 22301:2019 – Sécurité et résilience – Systèmes de management de la continuité d'activité.
- ISO 27031:2011 – Lignes directrices pour la préparation des technologies de l'information à la continuité d'activité.
- ANSSI – Guide d'hygiène informatique (2017, mise à jour 2023).
- Référentiel RGPD (CNIL).

### Annexe C — Calendrier de revue

| Action | Fréquence | Prochaine date |
|--------|-----------|----------------|
| Revue PCA/PRA complète | Annuelle | Mai 2027 |
| Mise à jour matrice risques | Semestrielle | Novembre 2026 |
| Mise à jour contacts d'urgence | Trimestrielle | Août 2026 |

---

**Document arrêté à la version 1.0** — Mai 2026

*Document à diffusion contrôlée. Seuls les membres de la cellule de continuité disposent de la version à jour.*
