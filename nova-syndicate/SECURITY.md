# Politique de sécurité — Nova Syndicate

> Document de référence pour la gestion sécurisée du code et de l'infrastructure de ce projet.

---

## Périmètre

Ce repo contient le code Infrastructure-as-Code (Terraform + Ansible) et les livrables documentaires du projet Nova Syndicate. Toute vulnérabilité dans :

- Les playbooks Ansible
- Le code Terraform
- Les scripts d'automatisation Python / Bash
- Les configurations exposées (PHP du site BricoPro, configs Suricata, etc.)
- Les pipelines CI/CD GitHub Actions

...est concernée par cette politique.

---

## Reporting d'une vulnérabilité

### Comment reporter ?

Si vous identifiez une faille de sécurité dans ce projet, **ne créez PAS d'issue publique**. Contactez directement le mainteneur :

- **Email** : `security@nova-syndicate.local` *(adresse fictive du projet)*
- **GitHub Security Advisory** : utilisez la fonctionnalité native de GitHub :
  → Onglet **Security** > **Report a vulnerability**

### Ce qu'il faut inclure

1. **Type de vulnérabilité** (XSS, SQLi, RCE, auth bypass, etc.)
2. **Fichier(s) concerné(s)** et numéro de ligne si possible
3. **Procédure de reproduction** (PoC court)
4. **Impact estimé** (CVSS si vous savez le calculer)
5. **Suggestion de correctif** *(facultatif)*

### Délais de réponse

| Phase | Délai engagé |
|-------|--------------|
| Accusé de réception | 48h |
| Triage et reproduction | 7 jours |
| Correctif déployé (selon sévérité) | Critique : 7j · High : 30j · Medium/Low : 90j |
| Publication advisory + crédit | Après déploiement du patch |

---

## Pratiques de sécurité dans ce projet

### Pipeline CI/CD (GitHub Actions)

Chaque commit est automatiquement scanné par :

- **Trivy** — Vulnérabilités OS, dépendances, secrets, misconfigurations
- **Checkov** — Best practices Infrastructure-as-Code (Terraform, Ansible)
- **Ansible-lint** — Conformité aux bonnes pratiques Ansible
- **Gitleaks** — Détection de secrets dans l'historique Git
- **Dependabot** — Mise à jour automatique des dépendances vulnérables

Les findings remontent dans l'onglet **Security** de ce repo.

### Hardening infrastructure déployée

- **Pare-feu OPNsense** — Deny All by Default sur tous les flux inter-VLAN
- **IDS Suricata** — 5 865 règles ET Open + détection temps réel + corrélation Wazuh
- **SIEM Wazuh** — Logs centralisés, MITRE ATT&CK mapping, audits CIS Debian Benchmark
- **Fail2ban** — Bantime progressif (1h → 24h) sur tentatives SSH
- **Kernel hardening sysctl** — Anti-spoofing, anti-redirect, SYN cookies, ignore broadcast
- **SSH hardening** — `MaxAuthTries 3`, `LoginGraceTime 30s`, `X11Forwarding no`, `PermitEmptyPasswords no`
- **Auto-updates** unattended-upgrades (security uniquement)

### Conformité multi-référentiels

- **ISO 27001** — Management de la sécurité
- **ISO 22301 / 27031** — Continuité d'activité
- **ANSSI** — Guide d'hygiène informatique
- **NIST SP 800-53** — Contrôles sécurité
- **NIST SP 800-207** — Zero Trust
- **MITRE ATT&CK** — Mapping des techniques d'attaque (Wazuh)
- **OWASP Top 10** — Sécurité applicative
- **RGPD** — Données personnelles
- **PCI-DSS** — Paiement en ligne (anticipé)

---

## Versions supportées

Ce projet étant un PoC académique, **seule la branche `main` est supportée**. Aucun backport n'est prévu sur des forks ou branches dérivées.

| Version | Supportée |
|---------|-----------|
| `main` (HEAD) | ✅ |
| Autres branches / forks | ❌ |

---

## Crédits et coordination

Les vulnérabilités déclarées de manière responsable sont créditées dans le CHANGELOG et / ou dans une Security Advisory publique après publication du patch.

Ce repo s'inscrit dans une démarche **DevSecOps** : security shifted left, intégré dès la conception et la CI/CD, et non comme une couche additionnelle.

---

*Politique inspirée de [SLSA Framework](https://slsa.dev/), [NIST SSDF](https://csrc.nist.gov/Projects/ssdf), et [OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/).*

*Dernière mise à jour : mercredi 13/05/2026.*
