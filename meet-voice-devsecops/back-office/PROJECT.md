# Back Office MeetVoice

## 🎯 Project Vision
Back office d'administration full-stack pour la plateforme de rencontres/réseau social **MeetVoice**. Permet à l'équipe de gérer les comptes utilisateurs, la modération, la facturation (Mollie), le monitoring des serveurs (Prometheus/Grafana via SSH), les bases de données (PostgreSQL + MongoDB), les emails, les newsletters et les VPS Contabo. Le tout accessible via une interface Django sécurisée.

## 🏗️ Architecture & Tech Stack

- **Language** : Python 3.12
- **Framework** : Django 5.2.8
- **Base de données principale** : PostgreSQL (via tunnel SSH → `81.17.103.146:5432`)
- **Base de données articles** : PostgreSQL séparé (via tunnel SSH → `149.102.143.243:5432`)
- **Bases MongoDB** :
  - Gateway (messagerie) → `164.68.109.146:27017`
  - API (social, posts, commentaires) → `164.68.115.49:27017`
  - Événements → `45.84.138.48:27017`
- **Cache/Sessions** : Redis (optionnel) + fallback LocMemCache
- **Monitoring** : Prometheus + Grafana (Docker Compose) via tunnels SSH vers Node Exporter (port 9100)
- **Paiements** : Mollie API (`mollie-api-python`)
- **Cloud/VPS** : Contabo API
- **Email** : IMAP/SMTP via `paramiko` + `aiohttp` + `edge-tts`
- **Storage** : AWS S3 (`boto3`)
- **Social** : LinkedIn OAuth2, Facebook API
- **SSH** : Tunnels persistants maison (paramiko) + terminal interactif
- **IA** : Module `ai_terminal.py` (assistant dans le terminal SSH)
- **Conteneurisation** : Docker + docker-compose
- **Serveur de prod** : Gunicorn (3 workers gthread)

### Carte des serveurs (14 nodes)

| Clé | Rôle | IP | User SSH |
|---|---|---|---|
| frontend | Frontend | 86.48.5.225 | root |
| backend | Backend | 156.67.29.190 | root |
| postgresql | PostgreSQL | 81.17.103.146 | root |
| mongo_messagerie | MongoDB Messagerie | 164.68.109.146 | root |
| mongo_reseaux | MongoDB Réseaux Sociaux | 164.68.115.49 | root |
| mongo_evenement | MongoDB Événement | 45.84.138.48 | root |
| evenement | Événement | 2.58.82.237 | root |
| ia | IA | 185.193.66.99 | root |
| automatisation | Automatisation | 149.102.143.243 | root |
| article | Article | 149.102.138.98 | root |
| reseaux_sociaux | Réseaux Sociaux | 62.171.154.23 | root |
| messagerie | Messagerie | 62.171.162.229 | root |
| websocket | WebSocket | 167.86.82.111 | sulta |
| gateway | Gateway | 89.117.49.9 | root |

## 📂 Structure des modules Django

```
back_office/          # Configuration Django, settings, tunnels SSH auto-démarrage
core/                 # Modèles : PlanAbonnement, Facture, Detail, UserEvent
compte/               # Modèles : Compte (UUID), Photo, Like, Blacklist, Signalement, Abonnement...
content/              # Modèles : PgArticle, ArticleView + db_router vers BDD articles
dashboard/            # Vues (67 routes), helpers : Mollie, IMAP, SSH, AI, newsletter, Contabo, LinkedIn
monitoring/           # Prometheus + Grafana (docker-compose + générateur dynamique)
templates/dashboard/  # 20 templates HTML (base.html + pages)
```

## 🔒 DevSecOps Strategy

- **CI/CD** : ✅ GitHub Actions opérationnel — tests Django + Trivy CVE scan (`.github/workflows/ci.yml`) ; déploiement manuel via Semaphore
- **Trivy Rules** : Bloquer sur CRITICAL et HIGH CVEs ; avertir sur MEDIUM — ✅ configuré
- **Secrets** : Gérés via `python-decouple` + `.env` — ✅ credentials migrés dans `.env` (plus aucun hardcodé dans `settings.py`)
- **Fuzzing Targets** :
  - `dashboard/views.py` → endpoints `pg_table_view`, `mongo_collection_view`, `terminal_exec`, `mailbox_send`
  - `tracking_event` → entrée non-authentifiée JSON
  - `newsletter_generate_image` → génération IA sur input utilisateur

## 🚨 Security Flags (identifiés au scan)

| Sévérité | Fichier | Problème | Statut |
|---|---|---|---|
| 🔴 CRITICAL | `back_office/settings.py` | Credentials MongoDB hardcodés (`admin:Ilaaiua18aa45`, `AdminPass123!`, `gateway_password_2025`) | ✅ Corrigé — migrés vers `.env` |
| 🔴 CRITICAL | `back_office/settings.py` | Mot de passe PostgreSQL articles hardcodé (`meetVoice123`) | ✅ Corrigé — migré vers `.env` |
| 🔴 CRITICAL | `monitoring/docker-compose.yml` | Mot de passe Grafana hardcodé (`meetvoice2025`) | ✅ Corrigé — variable env `${GRAFANA_ADMIN_PASSWORD}` |
| 🔴 CRITICAL | `back_office/settings.py` | `SECRET_KEY` Django insecure en fallback hardcodé | ✅ Corrigé — `config('SECRET_KEY')` sans default en prod |
| 🟠 HIGH | `back_office/settings.py` | `AutoAddPolicy()` paramiko (pas de vérification des host keys) | ⚠️ En attente — TASK-002 |
| 🟠 HIGH | `monitoring/docker-compose.yml` | `GF_AUTH_ANONYMOUS_ENABLED=true` → Grafana accessible sans auth | ✅ Corrigé — `false` |
| 🟡 MEDIUM | `back_office/settings.py` | `DEBUG=True` par défaut | ⚠️ À gérer via `.env` (`DEBUG=False` en prod) |
| 🟡 MEDIUM | Multiples IPs exposées dans le code source | IPs dans PROJECT.md uniquement (pas dans code) | ℹ️ Acceptable |

## 📐 Code Rules

- **Naming Conventions** : snake_case Python, templates en kebab (html)
- **Unit Tests** : Présents mais minimaux (`compte/tests.py`, `core/tests.py`, `dashboard/tests.py`, `dashboard/tests_perf.py`)
- **Linting** : Non configuré (à ajouter : `flake8` ou `ruff`)
- **Coverage** : Non mesuré (cible : ≥ 80% sur logique métier)

## 🗺️ Current Roadmap

- Epic 1 : **Sécurisation** — ✅ secrets migrés dans `.env`, Grafana anonyme corrigé ; ⚠️ reste AutoAddPolicy SSH
- Epic 2 : **CI/CD Pipeline** — ✅ GitHub Actions opérationnel (tests Django + Trivy + Docker build) ; déploiement via Semaphore
- Epic 3 : **Monitoring étendu** — compléter `prometheus.yml` avec les 14 serveurs (actuellement seuls 3 sont dans la config statique)
- Epic 4 : **Test Coverage** — écrire des tests unitaires pour les helpers critiques (Mollie, IMAP, Contabo)
- Epic 5 : **Observabilité applicative** — ajouter des métriques Django (django-prometheus ou custom)

## 📋 Backlog (TODO)

- [ ] TASK-002 — Remplacer `AutoAddPolicy()` par vérification des host keys
  - Description: Le tunnel SSH fait confiance aveuglément aux hosts distants (MITM risk)
  - Sécurité: 🟠 HIGH — attaque man-in-the-middle possible
  - Tests: Tests de connexion SSH avec un known_hosts valide

- [ ] TASK-005 — Compléter la config Prometheus avec les 14 serveurs
  - Description: `prometheus.yml` n'a que 3 jobs (pg, mongo_gw, mongo_api) — les 11 autres serveurs ne sont pas scrapés statiquement
  - Tests: Vérifier que tous les jobs apparaissent dans Prometheus targets

- [ ] TASK-006 — Ajouter `ruff` / `flake8` au projet
  - Description: Aucun linter configuré — qualité du code non garantie
  - Tests: `ruff check .` sans erreur

- [ ] TASK-007 — Écrire des tests pour les helpers critiques
  - Description: `mollie_helper.py`, `imap_helper.py`, `contabo.py`, `ssh_terminal.py` sans couverture
  - Fuzzing: `mailbox_send`, `terminal_exec` (inputs utilisateur non-filtrés)
  - Tests: Mock des APIs externes, test des chemins d'erreur

## ✅ Done

- [x] TASK-001 — Déplacer les credentials hardcodés dans `.env`
  - Résultat: `settings.py` migré vers `config()` pour tous les credentials MongoDB, PostgreSQL et Grafana
  - `.env` créé avec toutes les variables ; `.gitignore` mis à jour

- [x] TASK-003 — Désactiver l'accès anonyme Grafana
  - Résultat: `GF_AUTH_ANONYMOUS_ENABLED=false` dans `monitoring/docker-compose.yml`

- [x] TASK-004 — Mettre en place GitHub Actions CI/CD
  - Résultat: `.github/workflows/ci.yml` — 4 jobs : tests Django (settings_ci.py / SQLite), Trivy deps, Trivy image, résumé global
  - `settings_ci.py` créé pour CI sans tunnels SSH ni dépendances externes
  - Déploiement CD : manuel via Semaphore UI (port 3001 sur le monitoring_server)
  - Infrastructure Ansible : self-healing (systemd + cron 4h), certbot TLS, semaphore UI

---
_Dernière mise à jour : 2026-03-27 — CI/CD GitHub Actions + Ansible self-healing opérationnels_
