# Administration-d-active-directory
# Active Directory Lab : Architecture, Sécurité & Audit

Bienvenue sur mon labo Active Directory. J'ai monté ce projet de A à Z pour m'entraîner sur des cas concrets de déploiement, d'automatisation et de sécurisation en environnement multi-domaines.

L'objectif est d'avoir une infrastructure réaliste (Red/Blue Team) pour tester des vecteurs de compromission et configurer les mécanismes de détection (SOC) appropriés. Ce labo s'inscrit dans la continuité de mes entraînements pratiques sur [TryHackMe](https://tryhackme.com/p/seallia81).

## 🏗️ Topologie de l'infrastructure
Simulation d'un réseau d'entreprise avec un domaine racine et deux sous-domaines (gestion de 30 collaborateurs sur 10 départements).

* **Forêt :** `Dow01.local`
  * **Tier 0 (Root) :** `Dow01.local` (IT central, Enterprise Admins)
  * **Child 1 :** `Paris.Dow01.local` (Opérations France)
  * **Child 2 :** `London.Dow01.local` (Opérations Internationales)

## ⚙️ Automatisation (PowerShell)
Toute la structure logique (OUs, groupes de sécurité AGDLP, provisioning des comptes) est générée via script pour garantir la standardisation et la scalabilité.
* [Voir le script de déploiement](Scripts/01_Deploy_AD_Infrastructure.ps1)

## ⚔️ Tests Offensifs (Red Team)
**Privilege Escalation physique (Bypass Admin Local)**
* **Vecteur :** Boot sur ISO d'installation.
* **Exploitation :** Remplacement de `utilman.exe` par `cmd.exe` (Shift+F10).
* **Impact :** Shell `NT AUTHORITY\SYSTEM` sur l'écran de verrouillage, permettant la compromission du compte Administrateur local/domaine.

## 🛡️ Durcissement (Blue Team)
**Stratégies de Groupe (GPO)**
* Blocage de l'invite de commandes (`cmd.exe`) pour les utilisateurs standards.
* Désactivation du traitement silencieux des scripts `.bat` et `.cmd` pour mitiger les attaques par phishing/pièces jointes malveillantes.

## 👁️ Audit et Détection
**Configuration de la `Default Domain Controllers Policy`**
Activation des logs critiques pour la détection d'intrusions :
* **Event ID 4624 / 4625 :** Suivi des connexions (succès/échecs) pour identifier le brute-force ou les mouvements latéraux.
* **Event ID 4720 :** Alertes sur la création de comptes (détection de persistance/backdoors).
