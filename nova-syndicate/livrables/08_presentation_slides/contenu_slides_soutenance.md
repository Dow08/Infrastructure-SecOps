# Slides Soutenance — Nova Syndicate

> 13 slides + demo live = 15 minutes
> Structure : Intro slides (3 min) → Demo live navigateur (6 min) → Retour slides (6 min)

---

## SLIDE 1 — Page de garde

**Afficher :**

```
Nova Syndicate
Projet d'Infrastructure Réseau Sécurisée

[Ton prénom / nom]
RNCP Niveau 6 — Administrateur d'Infrastructures Sécurisées
Jedha Bootcamp — Mai 2026
```

**Notes orales (30s) :**
> "Bonjour, je vais vous présenter Nova Syndicate, un projet d'infrastructure réseau sécurisée déployée pour un site e-commerce. Je vais d'abord vous montrer l'architecture, puis on passera en démo live, et je terminerai par la sécurité, la conformité et l'étude économique."

---

## SLIDE 2 — Contexte du projet

**Afficher :**

```
CONTEXTE

Nova Syndicate opère BricoPro, un site e-commerce
déployé sur 2 sites : Lyon (principal) + Marseille (PRA)

Objectifs :
  - Infrastructure réseau complète et sécurisée
  - Segmentation VLAN + pare-feu périmétrique
  - Active Directory + SIEM + IDS
  - Monitoring temps réel
  - Stack applicative 3-tiers
  - Le tout en Infrastructure-as-Code (reproductible)

Conformité : ISO 27001 | ISO 22301 | ANSSI | NIST | MITRE ATT&CK
```

**Notes orales (1 min) :**
> "Nova Syndicate opère BricoPro, une plateforme e-commerce, sur deux sites : Lyon en site principal et Marseille en site de repli pour le Plan de Reprise d'Activité. L'objectif est de concevoir, déployer et sécuriser l'intégralité de l'infrastructure réseau — du pare-feu jusqu'au monitoring en temps réel — en restant conforme aux référentiels normatifs ISO 27001, ANSSI et NIST."

---

## SLIDE 3 — Architecture cible

**Afficher :**

```
ARCHITECTURE — Hub & Spoke + Defense in Depth

                    Internet
                       |
              OPNsense Lyon
              + Suricata IDS
                       |
     ┌────────┬────────┼────────┬────────┐
     DMZ     USERS   SERVERS   MGMT   BACKUP
    VLAN5   VLAN30   VLAN10  VLAN100  VLAN110
     |                 |        |
  Web/Proxy     DC01, Wazuh  Bastion
  Honeypot      DB-01, Files   SSH

          ← IPsec AES-256 / SHA-512 →

              Marseille (PRA)
              RODC + Users
```

```
Architecture cible : 12 VMs
PoC fonctionnel : 3 VMs consolidées (DC01 + DB-01 + File-01)
Redéploiement automatisable via Terraform + Ansible
```

**Notes orales (1 min 30) :**
> "L'architecture repose sur deux principes. Le Hub and Spoke : Lyon est le hub, tout le trafic de Marseille transite par Lyon via un tunnel IPsec IKEv2 chiffré AES-256 avec SHA-512. Et la Defense in Depth : 5 couches de sécurité superposées — pare-feu périmétrique, segmentation en 5 VLANs isolés, hardening de chaque hôte, détection via le SIEM Wazuh et l'IDS Suricata, et enfin audit avec les logs centralisés.
>
> L'architecture cible prévoit 12 VMs. Pour le PoC, j'ai consolidé sur 3 VMs fonctionnellement représentatives. Le redéploiement complet est automatisable via Terraform et Ansible — les playbooks sont écrits et testés."

---

## SLIDE 4 — Stack technique

**Afficher :**

```
STACK TECHNIQUE

Infrastructure-as-Code         Sécurité — SIEM & IDS
  Terraform (Proxmox)            Wazuh 4.7 (3 agents)
  Ansible (10 playbooks)         Suricata (5 865 règles ET Open)
  Git (versioning)               Fail2ban + UFW + sysctl

Hyperviseur & Réseau           Observabilité — LGTM
  Proxmox VE 9.1.1               Prometheus (métriques 30j)
  OPNsense (pare-feu)            Loki (logs centralisés)
  IPsec IKEv2                    Grafana (5 dashboards)

Services                       DevSecOps — CI/CD
  Samba 4 (AD nova.local)        Trivy + Checkov + Gitleaks
  MariaDB + Nginx + PHP-FPM      Ansible-lint + Dependabot
  BricoPro (22 produits)          GitHub Advanced Security
```

**Notes orales (45s) :**
> "Côté stack : Terraform pour le provisionnement, Ansible pour la configuration — 10 playbooks idempotents. Proxmox comme hyperviseur, OPNsense en pare-feu. Samba 4 pour l'Active Directory, MariaDB et Nginx pour le site BricoPro. Wazuh comme SIEM avec 3 agents, Suricata en IDS réseau. Prometheus, Loki et Grafana pour l'observabilité. Et un pipeline DevSecOps avec 4 scanners de sécurité automatiques à chaque commit. On va voir tout ça en démo."

---

## SLIDE 5 — Transition démo live

**Afficher :**

```
DEMO LIVE

  1. GitHub — Repo vitrine + CI/CD
  2. BricoPro — Site e-commerce 3-tiers
  3. Wazuh — SIEM + MITRE ATT&CK
  4. Grafana — Métriques + Logs temps réel
  5. Prometheus — Alerting (8 règles)
  6. Suricata — IDS réseau (5 865 règles)
  7. Terminal — Samba AD + Ansible
```

**Notes orales (15s) :**
> "Je bascule sur la démo. On va traverser 7 écrans en 5 minutes."

→ **BASCULER SUR CHROME — suivre le script_demo_live.md (minutes 1 à 6)**

---

*[DEMO LIVE — 5-6 minutes — pas de slides, on est sur Chrome]*

*Voir script_demo_live.md pour le déroulé exact*

---

## SLIDE 6 — Infrastructure-as-Code

**Afficher :**

```
INFRASTRUCTURE-AS-CODE

Terraform                          Ansible
  Provisionnement déclaratif         Configuration idempotente
  12 VMs + 6 bridges + 5 VLANs      10 playbooks
  State versionné sur Git            Master playbook site.yml

Redéploiement complet en 30-45 min :

  $ terraform apply          → VMs créées
  $ bash quickstart.sh all   → Services configurés

Bénéfices :
  Reproductibilité — clone + apply = infra identique
  Auditabilité — chaque changement tracé dans Git
  Résilience — crash = redéploiement automatique
  DR — Marseille redéployable en une commande
```

**Notes orales (1 min 30) :**
> "L'Infrastructure-as-Code repose sur la séparation Terraform pour le provisionnement et Ansible pour la configuration. Terraform crée les 12 VMs, les bridges, les VLANs sur Proxmox. Ansible configure les services : fail2ban, Samba AD, MariaDB, Nginx, Wazuh, Prometheus, Loki, Grafana. Le tout en une seule commande via quickstart.sh. Un nouvel ingénieur clone le repo, lance deux commandes, il a l'infra identique en 45 minutes. C'est aussi notre stratégie de Disaster Recovery : si Lyon tombe, on redéploie Marseille avec le même code."

---

## SLIDE 7 — DevSecOps

**Afficher :**

```
DEVSECOPS — Security Shifted Left

Pipeline CI/CD automatique à chaque commit :

  Trivy ............. CVE + secrets + misconfigs IaC → SARIF
  Checkov ........... Audit IaC (CIS / NIST 800-53)
  Gitleaks .......... Secrets dans l'historique Git
  Ansible-lint ...... Best practices playbooks

+ Dependabot         Mises à jour auto dépendances
+ Secret scanning    Bloque les secrets AVANT le push
+ Code scanning      Résultats dans GitHub Security tab

Code quality : yamllint | markdownlint | ShellCheck | terraform fmt

Conforme : SLSA Framework + NIST SSDF
```

**Notes orales (1 min) :**
> "La sécurité ne s'arrête pas au runtime. On a appliqué le principe Shift Left : 4 scanners automatiques tournent en CI/CD à chaque commit. Trivy pour les CVE et misconfigurations, Checkov pour l'audit IaC mappé sur CIS et NIST, Gitleaks pour détecter des secrets dans l'historique Git, et Ansible-lint pour les bonnes pratiques. Côté repo, le Push Protection de GitHub bloque tout commit contenant un secret avant même qu'il n'atteigne l'historique. C'est conforme au SLSA framework."

---

## SLIDE 8 — Sécurité en profondeur

**Afficher :**

```
DEFENSE IN DEPTH — 5 couches

  1. Périmètre      OPNsense + Suricata IDS (5 865 règles)
  2. Segmentation    5 VLANs isolés + Deny All by Default
  3. Hardening       Fail2ban + UFW + kernel sysctl + auto-updates
  4. Détection       Wazuh SIEM (570 events/24h, MITRE ATT&CK)
  5. Audit           Loki + Grafana (8 310 lignes/heure)

+ Pipeline DevSecOps (sécurité dès le code)

Corrélation N1 (réseau) + N2 (host) :
  Suricata alerte → syslog → Wazuh corrèle avec FIM/auth
  = pattern SOC opérationnel
```

**Notes orales (1 min) :**
> "On superpose 5 couches de défense. Si un attaquant passe le pare-feu, il tombe sur la segmentation VLAN. S'il pivote, le hardening le ralentit. S'il agit, Wazuh le détecte via les agents endpoints et Suricata le détecte côté réseau. Et tout est tracé dans les logs centralisés. La corrélation entre Suricata en couche réseau et Wazuh en couche host, c'est le pattern classique d'un SOC. En ajoutant le pipeline DevSecOps, la sécurité couvre aussi le code source — c'est du end-to-end."

---

## SLIDE 9 — PCA/PRA + Conformité

**Afficher :**

```
CONTINUITÉ D'ACTIVITÉ                CONFORMITÉ

PCA (ISO 22301)                      ISO 27001 — Sécurité IT
  BIA sur 11 services                ISO 22301 — Continuité
  RTO/RPO définis par service        ISO 27031 — Préparation TIC
  17 risques cotés                   ANSSI — Hygiène + DiD
                                     NIST 800-53 — Contrôles
PRA (ISO 27031)                      NIST 800-207 — Zero Trust
  5 scénarios de sinistre            MITRE ATT&CK — Détections
  Politique sauvegarde 3-2-1         OWASP Top 10 — Web
  5 procédures de restauration       RGPD — Données personnelles
  Marseille = site de repli          PCI-DSS — Paiement (anticipé)
```

**Notes orales (1 min) :**
> "On a documenté un PCA et un PRA complets conformes ISO 22301. Le PCA identifie 17 risques cotés sur une matrice de criticité avec des RTO et RPO définis pour chaque service. Le PRA couvre 5 scénarios de sinistre : crash hyperviseur, corruption de données, ransomware, indisponibilité du site Lyon, erreur humaine. Politique de sauvegarde 3-2-1. Et Marseille sert de site de repli avec un RODC prévu pour la continuité AD.
>
> Le projet s'inscrit dans un cadre normatif large : ISO 27001, ANSSI, NIST, MITRE ATT&CK, OWASP et RGPD."

---

## SLIDE 10 — Étude économique

**Afficher :**

```
ÉTUDE ÉCONOMIQUE — TCO sur 3 ans

Solution                          TCO 3 ans    Souveraineté
A — Propriétaire (VMware+MS)     173 042 €    Faible
B — Open-source on-premise        38 730 €    Forte        ← RETENUE
C — Cloud public (AWS/Azure)      95 200 €    Moyenne

Économie : -78% vs propriétaire (134 k€ sur 3 ans)

Avantages solution retenue :
  Souveraineté française
  Zéro vendor lock-in
  Compétences marché disponibles (Linux/Proxmox)
  Réversibilité totale
```

**Notes orales (1 min) :**
> "On a fait une étude comparative 3 solutions sur 3 ans. La solution propriétaire VMware plus Microsoft coûte 173 000 euros. Le cloud public revient à 95 000. Notre solution open-source on-premise à 38 730 euros — soit 78% d'économie par rapport au propriétaire. Au-delà du coût, c'est la souveraineté qui prime : les données restent sur une infrastructure contrôlée, zéro vendor lock-in, et les compétences Linux/Proxmox sont largement disponibles sur le marché."

---

## SLIDE 11 — Retour d'expérience

**Afficher :**

```
RETOUR D'EXPÉRIENCE

25 incidents techniques documentés
  Symptôme → Cause racine → Fix → Apprentissage

Exemples :
  Mismatch Wazuh agent/manager → pinning version + apt hold
  TCG vs KVM (nested virt) → désactivation Hyper-V → x10 perfs
  MariaDB latin1 vs UTF-8 → migration utf8mb4
  Bridge VLAN non-persistant → procédure documentée
  Cloud-init sshkeys → workaround mount disk

Preuve d'une démarche opérationnelle réelle,
pas d'un projet théorique.
```

**Notes orales (45s) :**
> "Pendant le déploiement, j'ai documenté 25 incidents techniques avec pour chacun le symptôme observé, la cause racine, le fix appliqué et l'apprentissage. Ce n'est pas du théorique — c'est une infrastructure éprouvée. Ces incidents et leur résolution sont la preuve d'une démarche d'amélioration continue."

---

## SLIDE 12 — Conclusion

**Afficher :**

```
CONCLUSION

Infrastructure opérationnelle :
  Architecture Hub & Spoke + Defense in Depth
  Stack complète : AD, Web, SIEM, IDS, Monitoring, DevSecOps
  Reproductible en 45 min via IaC (Terraform + Ansible)

10 livrables produits :
  3 rapports de phase + PCA/PRA + Veille EN
  Scripts + Playbooks + Pentest + CAPEX/OPEX
  Gestion projet Notion + cette présentation

Chiffres clés :
  5 VLANs | 8 playbooks | 25 incidents documentés
  570 events Wazuh/24h | 8 règles alerting | 4 scanners CI/CD
  38 730 € TCO 3 ans (-78% vs propriétaire)
```

**Notes orales (45s) :**
> "Pour conclure : l'infrastructure est opérationnelle, sécurisée sur 5 couches, reproductible en 45 minutes via Infrastructure-as-Code, et conforme aux principaux référentiels normatifs. Les 10 livrables sont produits. Le pipeline DevSecOps garantit la sécurité du code source en continu. Et l'étude économique démontre un TCO de 38 730 euros sur 3 ans avec 78% d'économie par rapport à une solution propriétaire. Je suis prêt pour vos questions."

---

## SLIDE 13 — Q&A

**Afficher :**

```
QUESTIONS ?

[Ton nom]
github.com/Dow08/Projet_Nova_syndicate_Jedha
```

---

## TIMING RECAP

| Slide | Durée | Temps cumulé |
|-------|-------|-------------|
| 1 — Page de garde | 0:30 | 0:30 |
| 2 — Contexte | 1:00 | 1:30 |
| 3 — Architecture | 1:30 | 3:00 |
| 4 — Stack technique | 0:45 | 3:45 |
| 5 — Transition démo | 0:15 | 4:00 |
| DEMO LIVE (Chrome) | 5:30 | 9:30 |
| 6 — IaC | 1:30 | 11:00 |
| 7 — DevSecOps | 1:00 | 12:00 |
| 8 — Sécurité DiD | 1:00 | 13:00 |
| 9 — PCA/PRA + Conformité | 1:00 | 14:00 |
| 10 — CAPEX/OPEX | 1:00 | 15:00 |
| 11 — Retour d'expérience | (si temps) | — |
| 12 — Conclusion | 0:45 | 15:45 |
| 13 — Q&A | variable | — |

**Total slides : ~10 min | Demo live : ~5-6 min | Total : ~15 min**

Slides 11 (Retour d'expérience) est un buffer — si tu es en avance tu le places, sinon tu passes directement à la conclusion.

---

## CONSEILS DE PRÉSENTATION

- **Slide 3 (Architecture)** : c'est la slide la plus importante. Prends le temps de l'expliquer calmement, pointe les éléments avec ta main/laser.
- **Demo live** : si quelque chose foire, dis "la latence est due au mode lab" et bascule sur les screenshots dans Documents/POC_Screen/.
- **CAPEX/OPEX** : mémorise le chiffre 78% et 38 730 euros. Le jury adore les chiffres.
- **Ne lis pas les slides** : elles sont un support visuel, pas un script. Regarde le jury.
- **Rythme** : parle lentement sur l'architecture et la sécurité, plus vite sur le CAPEX.

---

*Dernière maj : mercredi 14/05/2026*
