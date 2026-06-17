🛡️ Kessel Dynamics : Infrastructure SOC & SIEM avec Wazuh
Ce projet présente la mise en place d'une infrastructure de monitoring de sécurité (SIEM) pour la startup fintech Kessel Dynamics. L'objectif est de sécuriser un environnement de microservices conteneurisés en déployant une solution de détection et de réponse centralisée.
<img width="1891" height="800" alt="image" src="https://github.com/user-attachments/assets/970958b1-bad7-47c8-8b1b-d5bb9055e1a2" />

📋 Scénario
Kessel Dynamics doit répondre aux exigences de conformité SOC2 et ISO 27001. En tant qu'ingénieur cybersécurité junior, j'ai déployé une infrastructure de base pour surveiller :

Les tentatives d'accès non autorisées (Brute Force SSH).

La conformité des configurations système (SCA).

La détection d'anomalies et de rootkits (Rootcheck).

🛠️ Stack Technique
SIEM : Wazuh (Indexer, Server, Dashboard) déployé via Docker Compose.

Automatisation : Ansible pour le déploiement industriel des agents.

Cibles : Serveurs Ubuntu 22.04 (conteneurs Docker).

Outils : WSL2, Docker Desktop, PowerShell.

🚀 Réalisations
1. Déploiement de l'Infrastructure Wazuh
Mise en place d'une stack Wazuh complète en mode "Single Node" utilisant Docker.

Génération de certificats SSL internes pour sécuriser les flux entre les composants.

Configuration de l'interface Dashboard pour la visualisation en temps réel.

2. Automatisation avec Ansible
Utilisation d'un Playbook Ansible pour automatiser l'installation des agents sur le parc serveur.

Utilisation du connecteur docker d'Ansible pour configurer les conteneurs sans SSH.

Configuration dynamique pour pointer vers host.docker.internal comme Manager.

3. Ingénierie de Détection & Troubleshooting
Configuration de log personnalisée : Modification du fichier ossec.conf pour surveiller /var/log/auth.log sur des images Ubuntu minimalistes.

Simulation d'attaque : Scripting d'une attaque par force brute SSH en Bash pour valider les capacités de corrélation de Wazuh.
"for i in {1..15}; do echo "$(date '+%b %e %H:%M:%S') kessel-server sshd[$(($RANDOM%10000))]: Failed password for root from 1.2.3.4 port $(($RANDOM%60000)) ssh2" >> /var/log/auth.log; done"

Analyse de logs : Identification et gestion de faux positifs (alertes Rootcheck sur les fichiers système Docker).

📊 Preuves de Concept (PoC)
Détection de Force Brute SSH
Wazuh a corrélé plusieurs tentatives d'échec de connexion pour déclencher une alerte de niveau 5 (Authentication failed) puis de niveau supérieur lors de l'attaque massive.

<img width="1908" height="880" alt="Capture d&#39;écran 2026-05-02 181719" src="https://github.com/user-attachments/assets/68aabf96-db0d-4d94-8d33-2d285ca90ed8" />


Audit de Configuration (SCA)
Dès le déploiement, l'agent a audité le serveur par rapport au benchmark CIS Ubuntu Linux.

