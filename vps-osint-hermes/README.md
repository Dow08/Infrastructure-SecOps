# Pack de Réplication & Configuration du VPS

Ce dépôt contient l'ensemble complet et automatisé permettant de répliquer, sauvegarder et redéployer l'intégralité de l'environnement de ton VPS en quelques clics. Il est organisé de manière totalement indépendante (VPS_Jarod_AI_et_OSINT) afin d'éviter tout mélange de configurations avec tes autres projets.

## Présentation de l'Architecture

L'environnement du VPS repose sur un système Ubuntu 24.04 servant trois points d'accès principaux via un proxy inverse Nginx sécurisé par SSL (Let's Encrypt) et une authentification de base (Basic Auth) :

1. **crfdow08.tech** (Hub Principal) - Portail web statique hébergé dans `/var/www/hub`.
2. **hermes.crfdow08.tech** (Hermes Agent & Workspace) - Serveur d'API Python s'exécutant sur l'hôte en tant que service systemd, couplé à l'interface utilisateur web basée sur Node/Vite (port 3000).
3. **shadowbroker.crfdow08.tech** (Pile Shadowbroker) - Application microservices s'exécutant entièrement dans des conteneurs Docker via Docker Compose.

---

## Structure du Dépôt

```
VPS_Jarod_AI_et_OSINT/
├── README.md                 # Cette documentation
├── setup.sh                  # Script principal d'installation automatisée
├── backup-restore.sh         # Utilitaire de sauvegarde et de restauration des données actives
├── backup-soul.sh            # Script planifié pour la sauvegarde hebdomadaire de l'âme
├── soul-shield.py            # Script d'analyse de sécurité et de censure des secrets
├── nginx/
│   └── cyberstation.template # Modèle de blocs serveurs Nginx avec variables de domaines
├── systemd/                  # Définitions des unités de services Systemd
│   ├── hermes-gateway.service.template
│   ├── hermes-dashboard.service.template
│   └── hermes-ui.service.template
└── soul/                     # Dossier créé automatiquement contenant les sauvegardes de l'âme
```

---

## Guide de Déploiement en un Clic (Nouveau VPS)

Lors du déploiement sur un serveur Ubuntu 24.04 entièrement vierge, exécute ces commandes pour recréer exactement le même environnement :

### Étape 1 : Cloner ce dépôt de réplication
Connecte-toi en tant que root sur ton nouveau VPS et clone ce dépôt :
```bash
git clone https://github.com/Dow08/VPS_Jarod_AI_et_OSINT.git /root/VPS_Jarod_AI_et_OSINT
```

### Étape 2 : Lancer l'installateur
Accède au dossier, rends les scripts exécutables et lance l'installation :
```bash
cd /root/VPS_Jarod_AI_et_OSINT
chmod +x setup.sh backup-restore.sh backup-soul.sh soul-shield.py
./setup.sh
```

Pendant son exécution, le script va :
- Installer toutes les dépendances système requises (Nginx, Docker, Node.js, pnpm, Python 3.11, etc.).
- Cloner automatiquement les dépôts nécessaires (/root/hermes-workspace, /root/Shadowbroker) ainsi que ton projet GRC indépendant (/workspace).
- Enregistrer et activer les services systemd.
- Configurer le proxy inverse Nginx avec tes noms de domaines et sécuriser les accès par authentification Basic Auth.
- Créer des modèles de fichiers d'environnement `.env` vides à remplir.

### Étape 3 : Remplir les clés secrètes
Configure tes clés d'API et variables d'environnement sur ton nouveau serveur :
1. **Secrets de l'Agent Hermes :** `/root/.hermes/.env` (Remplis tes clés `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, etc.).
2. **Secrets de l'interface Hermes :** `/root/hermes-workspace/.env` (Définis ton `HERMES_PASSWORD` pour la connexion).
3. **Secrets de Shadowbroker :** `/root/Shadowbroker/.env` (Clés d'API et paramètres de l'opérateur).

Après avoir configuré tes clés, redémarre les services :
```bash
systemctl restart hermes-gateway hermes-dashboard hermes-ui
cd /root/Shadowbroker && docker compose restart
```

### Étape 4 : Obtenir les certificats SSL (HTTPS)
Exécute simplement le configurateur interactif Certbot pour générer et lier tes certificats Let's Encrypt :
```bash
certbot --nginx -d crfdow08.tech -d www.crfdow08.tech -d hermes.crfdow08.tech -d www.hermes.crfdow08.tech -d shadowbroker.crfdow08.tech -d www.shadowbroker.crfdow08.tech
```

---

## Sauvegarde & Restauration des Données Actives

La réplication du système est dissociée de la sauvegarde des données d'usage. Pour sauvegarder ton état de données actif (historiques de discussions, compétences personnalisées, mémoires d'apprentissage et bases de données Shadowbroker), utilise l'utilitaire `backup-restore.sh`.

### Effectuer une sauvegarde depuis le VPS actif :
Exécute cette commande pour créer une archive de sauvegarde compressée :
```bash
/root/VPS_Jarod_AI_et_OSINT/backup-restore.sh backup
```
L'archive contiendra :
- Tous les fichiers de configuration système Nginx et d'authentification Basic Auth.
- Tous les fichiers `.env` secrets.
- La base de données SQLite active d'Hermes (`~/.hermes/state.db`), les compétences personnalisées (`~/.hermes/skills`) et les mémoires.
- Les fichiers HTML du portail web statique (`/var/www/hub/`).
- Une copie de sauvegarde à chaud du volume Docker `shadowbroker_backend_data` de Shadowbroker.

L'archive finale sera stockée dans `/root/vps-backups/vps_state_backup_AAAAMMJJ_HHMMSS.tar.gz`. Tu pourras la télécharger en toute sécurité depuis ton VPS.

### Restaurer sur un nouveau VPS :
Pour restaurer tes données et configurations sur un VPS fraîchement installé avec `setup.sh`, transfère l'archive sur le nouveau VPS et exécute :
```bash
/root/VPS_Jarod_AI_et_OSINT/backup-restore.sh restore /chemin/vers/l_archive.tar.gz
```
Le script s'occupera d'arrêter proprement les services, de restaurer l'intégralité des bases de données, des volumes Docker et des configurations, puis de relancer l'environnement de manière totalement transparente et sans aucune perte.
