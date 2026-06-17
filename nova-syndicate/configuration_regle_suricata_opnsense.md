# Configuration Optimisée de Suricata pour OPNsense

Ce document détaille la sélection de règles préconisée pour une installation Suricata sur OPNsense. L'objectif est d'assurer une protection robuste tout en minimisant l'impact sur les ressources CPU et en limitant les faux positifs.

---

## 1. Flux de Réputation (Blocklists IP)
Ces règles sont basées sur des listes d'adresses IP connues pour être malveillantes. Elles sont peu gourmandes en ressources et très efficaces.

### `et/botcc` & `et/botcc.portgrouped`
* **Fonction :** Détection des serveurs de "Command & Control" (C2).
* **Pourquoi :** Si un appareil de votre réseau est infecté par un botnet, il tentera de contacter son "maître". Cette règle bloque cette communication, rendant le malware inopérant.

### `et/ciarmy`
* **Fonction :** Liste d'IP identifiées par la communauté comme étant "agressives".
* **Pourquoi :** Bloque les adresses IP qui scannent activement Internet à la recherche de failles. C'est une première ligne de défense contre les attaques opportunistes.

### `et/compromised`
* **Fonction :** Identifie les serveurs légitimes qui ont été piratés.
* **Pourquoi :** Un site web sain peut être compromis pour héberger des malwares. Cette règle vous empêche de vous y connecter le temps de l'infection.

### `et/drop` (Spamhaus)
* **Fonction :** "Don't Route Or Peer".
* **Pourquoi :** Bloque les réseaux entiers détournés par des cybercriminels (spam, botnets, serveurs de phishing).

### `et/dshield`
* **Fonction :** Liste des 20 sous-réseaux les plus actifs en termes d'attaques.
* **Pourquoi :** Protection proactive contre les infrastructures d'attaque les plus persistantes du moment.

---

## 2. Sécurité Réseau et Prévention d'Intrusion
Ces règles analysent le contenu des paquets pour détecter des comportements de piratage.

### `et/emerging-attack_response`
* **Fonction :** Détection de la réponse à une attaque.
* **Pourquoi :** Cette règle surveille si un de vos serveurs envoie des données typiques d'une fuite d'informations (ex: sortie d'un shell distant). C'est crucial pour savoir si une intrusion a réussi.

### `et/emerging-exploit`
* **Fonction :** Signatures contre les vulnérabilités logicielles connues (CVE).
* **Pourquoi :** Bloque les tentatives d'utilisation de failles dans vos applications ou systèmes d'exploitation avant même qu'ils ne soient mis à jour.

### `et/emerging-shellcode`
* **Fonction :** Détection de code binaire malveillant dans le flux réseau.
* **Pourquoi :** Les pirates injectent souvent du "shellcode" pour prendre le contrôle d'une machine. Cette règle repère ces motifs spécifiques.

### `et/emerging-worm`
* **Fonction :** Blocage de la propagation des vers informatiques.
* **Pourquoi :** Empêche une infection de se propager automatiquement d'une machine à une autre sur votre réseau local.

### `et/threatview_CS_c2`
* **Fonction :** Détection spécifique de l'outil Cobalt Strike.
* **Pourquoi :** Cobalt Strike est l'outil favori des groupes de ransomware. Bloquer ses balises (beacons) est une priorité absolue.

---

## 3. Protection de la Navigation (Endpoints)
Règles destinées à protéger les utilisateurs lors de leur navigation quotidienne.

### `et/emerging-adware_pup`
* **Fonction :** Logiciels publicitaires et programmes potentiellement indésirables.
* **Pourquoi :** Nettoie votre navigation en bloquant les trackers agressifs et les installeurs de logiciels douteux.

### `et/emerging-coinminer`
* **Fonction :** Détection du minage de crypto-monnaie non autorisé.
* **Pourquoi :** Empêche les sites web ou malwares d'utiliser la puissance de votre CPU pour miner de la crypto-monnaie à votre insu.

### `et/emerging-phishing`
* **Fonction :** URLs et domaines de phishing.
* **Pourquoi :** Bloque l'accès aux faux sites (banques, messageries) conçus pour voler vos identifiants.

---

## Recommandations de Mise en Œuvre

1.  **Mode IDS d'abord :** Laissez Suricata en mode détection uniquement pendant 48h pour observer les alertes.
2.  **Passage en IPS :** Une fois les faux positifs identifiés et exclus, activez le mode IPS pour que Suricata bloque réellement le trafic.
3.  **Hardware Offloading :** Assurez-vous de désactiver le LRO et le TSO dans les paramètres d'interface d'OPNsense si vous utilisez le mode IPS, sinon Suricata ne pourra pas analyser correctement les paquets.


cron suricata : 

une mise à jour quotidienne (par exemple à 01h15 du matin, quand le réseau est peu sollicité) :

Minutes : 15

Heures : 1

Jours du mois : * (Tous)

Mois : * (Tous)

Jours de la semaine : * (Tous)

Commande : Recherchez et sélectionnez "Intrusion Detection: Rule Update".

Description : Donnez un nom clair, par exemple Mise à jour auto Suricata.

Update : OPNsense va chercher les nouvelles signatures chez Emerging Threats (les règles qu'on a choisies ensemble).

Reload : Il demande à Suricata de charger ces nouvelles règles en mémoire pour qu'elles soient actives immédiatement.

C'est parfait, une fois que c'est fait, votre firewall se mettra à jour tout seul toutes les nuits à 01h15 !