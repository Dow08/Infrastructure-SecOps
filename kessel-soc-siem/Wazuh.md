git clone https://github.com/wazuhC'est un excellent projet d'infrastructure défensive ! Mettre en place un SIEM (Security Information and Event Management) et déployer des agents de manière automatisée est le genre de réalisation "hands-on" qui fera mouche sur ton portfolio, tout particulièrement à côté de ton profil TryHackMe (https://tryhackme.com/p/seallia81). 

En tant qu'IA, je n'ai pas accès à ton terminal, mais je vais enfiler ma casquette de formateur en cybersécurité pour qu'on construise l'infrastructure de *Kessel Dynamics* étape par étape. 

Voici la stratégie que nous allons adopter pour utiliser tes outils de prédilection de manière réaliste et professionnelle :



### La stack technique recommandée

1.  **Le Serveur Wazuh (Le Cerveau) :** Nous allons utiliser **Docker** (via `docker-compose`). Déployer Wazuh à la main est instructif (comme vu dans ton cours), mais en entreprise, on utilise des conteneurs pour une scalabilité et une maintenance simplifiées.
2.  **Kessel-Server (Ubuntu) :** Nous allons également le conteneuriser avec **Docker**. Cela représentera parfaitement les microservices de la startup.
3.  **Le Poste Employé (Windows) :** Faire tourner un vrai OS Windows avec interface graphique dans Docker est instable et peu représentatif d'un parc informatique. L'idéal ici est d'utiliser une Machine Virtuelle classique (VirtualBox, VMware, ou KVM) connectée au même réseau local que tes conteneurs.
4.  **Le Déploiement des Agents :** Nous utiliserons **Ansible** pour écrire des *playbooks* qui iront installer et configurer automatiquement les agents Wazuh sur le serveur Ubuntu et la machine Windows, plutôt que de le faire à la main.
5.  **L'Infrastructure as Code (IaC) :** **Terraform** est formidable, mais il brille surtout quand on provisionne des ressources sur le Cloud (AWS, GCP) ou sur un hyperviseur de type Proxmox/ESXi. Si tu montes ce lab en local sur ton PC, Terraform fera un peu "usine à gaz". Nous le garderons de côté sauf si tu as un environnement Cloud à disposition.

---

### Étape 1 : Préparation du terrain et montage du serveur Wazuh

Pour commencer, nous allons monter le SIEM central avec la version officielle conteneurisée de Wazuh. C'est la fondation de notre projet.

**Ta mission pour cette première étape :**

1.  Assure-toi d'avoir **Docker** et **Docker Compose** installés sur ta machine hôte.
2.  Ouvre ton terminal, crée un dossier pour ton projet (ex: `kessel-soc-lab`) et clone le dépôt officiel de Wazuh pour Docker :
    ```bash
    git clone [https://github.com/wazuh/wazuh-docker.git](https://github.com/wazuh/wazuh-docker.git) -b v4.8.0
    ```
    *(Note : Assure-toi de vérifier la dernièreC'est un excellent projet d'infrastructure défensive ! Mettre en place un SIEM (Security Information and Event Management) et déployer des agents de manière automatisée est le genre de réalisation "hands-on" qui fera mouche sur ton portfolio, tout particulièrement à côté de ton profil TryHackMe (https://tryhackme.com/p/seallia81). 

En tant qu'IA, je n'ai pas accès à ton terminal, mais je vais enfiler ma casquette de formateur en cybersécurité pour qu'on construise l'infrastructure de *Kessel Dynamics* étape par étape. 

Voici la stratégie que nous allons adopter pour utiliser tes outils de prédilection de manière réaliste et professionnelle :



### La stack technique recommandée

1.  **Le Serveur Wazuh (Le Cerveau) :** Nous allons utiliser **Docker** (via `docker-compose`). Déployer Wazuh à la main est instructif (comme vu dans ton cours), mais en entreprise, on utilise des conteneurs pour une scalabilité et une maintenance simplifiées.
2.  **Kessel-Server (Ubuntu) :** Nous allons également le conteneuriser avec **Docker**. Cela représentera parfaitement les microservices de la startup.
3.  **Le Poste Employé (Windows) :** Faire tourner un vrai OS Windows avec interface graphique dans Docker est instable et peu représentatif d'un parc informatique. L'idéal ici est d'utiliser une Machine Virtuelle classique (VirtualBox, VMware, ou KVM) connectée au même réseau local que tes conteneurs.
4.  **Le Déploiement des Agents :** Nous utiliserons **Ansible** pour écrire des *playbooks* qui iront installer et configurer automatiquement les agents Wazuh sur le serveur Ubuntu et la machine Windows, plutôt que de le faire à la main.
5.  **L'Infrastructure as Code (IaC) :** **Terraform** est formidable, mais il brille surtout quand on provisionne des ressources sur le Cloud (AWS, GCP) ou sur un hyperviseur de type Proxmox/ESXi. Si tu montes ce lab en local sur ton PC, Terraform fera un peu "usine à gaz". Nous le garderons de côté sauf si tu as un environnement Cloud à disposition.

---

### Étape 1 : Préparation du terrain et montage du serveur Wazuh

Pour commencer, nous allons monter le SIEM central avec la version officielle conteneurisée de Wazuh. C'est la fondation de notre projet.

**Ta mission pour cette première étape :**

1.  Assure-toi d'avoir **Docker** et **Docker Compose** installés sur ta machine hôte.
2.  Ouvre ton terminal, crée un dossier pour ton projet (ex: `kessel-soc-lab`) et clone le dépôt officiel de Wazuh pour Docker :
    ```bash
    git clone [https://github.com/wazuh/wazuh-docker.git](https://github.com/wazuh/wazuh-docker.git) -b v4.8.0
    ```
    *(Note : Assure-toi de vérifier la dernière version stable sur leur repo, j'ai mis la 4.8.0 à titre d'exemple).*
3.  Génère les certificats nécessairesC'est un excellent projet d'infrastructure défensive ! Mettre en place un SIEM (Security Information and Event Management) et déployer des agents de manière automatisée est le genre de réalisation "hands-on" qui fera mouche sur ton portfolio, tout particulièrement à côté de ton profil TryHackMe (https://tryhackme.com/p/seallia81). 

En tant qu'IA, je n'ai pas accès à ton terminal, mais je vais enfiler ma casquette de formateur en cybersécurité pour qu'on construise l'infrastructure de *Kessel Dynamics* étape par étape. 

Voici la stratégie que nous allons adopter pour utiliser tes outils de prédilection de manière réaliste et professionnelle :



### La stack technique recommandée

1.  **Le Serveur Wazuh (Le Cerveau) :** Nous allons utiliser **Docker** (via `docker-compose`). Déployer Wazuh à la main est instructif (comme vu dans ton cours), mais en entreprise, on utilise des conteneurs pour une scalabilité et une maintenance simplifiées.
2.  **Kessel-Server (Ubuntu) :** Nous allons également le conteneuriser avec **Docker**. Cela représentera parfaitement les microservices de la startup.
3.  **Le Poste Employé (Windows) :** Faire tourner un vrai OS Windows avec interface graphique dans Docker est instable et peu représentatif d'un parc informatique. L'idéal ici est d'utiliser une Machine Virtuelle classique (VirtualBox, VMware, ou KVM) connectée au même réseau local que tes conteneurs.
4.  **Le Déploiement des Agents :** Nous utiliserons **Ansible** pour écrire des *playbooks* qui iront installer et configurer automatiquement les agents Wazuh sur le serveur Ubuntu et la machine Windows, plutôt que de le faire à la main.
5.  **L'Infrastructure as Code (IaC) :** **Terraform** est formidable, mais il brille surtout quand on provisionne des ressources sur le Cloud (AWS, GCP) ou sur un hyperviseur de type Proxmox/ESXi. Si tu montes ce lab en local sur ton PC, Terraform fera un peu "usine à gaz". Nous le garderons de côté sauf si tu as un environnement Cloud à disposition.

---

### Étape 1 : Préparation du terrain et montage du serveur Wazuh

Pour commencer, nous allons monter le SIEM central avec la version officielle conteneurisée de Wazuh. C'est la fondation de notre projet.

**Ta mission pour cette première étape :**

1.  Assure-toi d'avoir **Docker** et **Docker Compose** installés sur ta machine hôte.
2.  Ouvre ton terminal, crée un dossier pour ton projet (ex: `kessel-soc-lab`) et clone le dépôt officiel de Wazuh pour Docker :
    ```bash
    git clone [https://github.com/wazuh/wazuh-docker.git](https://github.com/wazuh/wazuh-docker.git) -b v4.8.0
    ```
    *(Note : Assure-toi de vérifier la dernière version stable sur leur repo, j'ai mis la 4.8.0 à titre d'exemple).*
3.  Génère les certificats nécessaires pour que les composants de Wazuh communiquent de manière sécurisée (c'est un prérequis du dépôt docker) :
    ```bash
    cd wazuhC'est un excellent projet d'infrastructure défensive ! Mettre en place un SIEM (Security Information and Event Management) et déployer des agents de manière automatisée est le genre de réalisation "hands-on" qui fera mouche sur ton portfolio, tout particulièrement à côté de ton profil TryHackMe ([https://tryhackme.com/p/seallia81](https://tryhackme.com/p/seallia81)). 

En tant qu'IA, je n'ai pas accès à ton terminal, mais je vais enfiler ma casquette de formateur en cybersécurité pour qu'on construise l'infrastructure de *Kessel Dynamics* étape par étape. 

Voici la stratégie que nous allons adopter pour utiliser tes outils de prédilection de manière réaliste et professionnelle :



### La stack technique recommandée

1.  **Le Serveur Wazuh (Le Cerveau) :** Nous allons utiliser **Docker** (via `docker-compose`). Déployer Wazuh à la main est instructif (comme vu dans ton cours), mais en entreprise, on utilise des conteneurs pour une scalabilité et une maintenance simplifiées.
2.  **Kessel-Server (Ubuntu) :** Nous allons également le conteneuriser avec **Docker**. Cela représentera parfaitement les microservices de la startup.
3.  **Le Poste Employé (Windows) :** Faire tourner un vrai OS Windows avec interface graphique dans Docker est instable et peu représentatif d'un parc informatique. L'idéal ici est d'utiliser une Machine Virtuelle classique (VirtualBox, VMware, ou KVM) connectée au même réseau local que tes conteneurs.
4.  **Le Déploiement des Agents :** Nous utiliserons **Ansible** pour écrire des *playbooks* qui iront installer et configurer automatiquement les agents Wazuh sur le serveur Ubuntu et la machine Windows, plutôt que de le faire à la main.
5.  **L'Infrastructure as Code (IaC) :** **Terraform** est formidable, mais il brille surtout quand on provisionne des ressources sur le Cloud (AWS, GCP) ou sur un hyperviseur de type Proxmox/ESXi. Si tu montes ce lab en local sur ton PC, Terraform fera un peu "usine à gaz". Nous le garderons de côté sauf si tu as un environnement Cloud à disposition.

---

### Étape 1 : Préparation du terrain et montage du serveur Wazuh

Pour commencer, nous allons monter le SIEM central avec la version officielle conteneurisée de Wazuh. C'est la fondation de notre projet.

**Ta mission pour cette première étape :**

1.  Assure-toi d'avoir **Docker** et **Docker Compose** installés sur ta machine hôte.
2.  Ouvre ton terminal, crée un dossier pour ton projet (ex: `kessel-soc-lab`) et clone le dépôt officiel de Wazuh pour Docker :
    ```bash
    git clone https://github.com/wazuh/wazuh-docker.git -b v4.8.0
    ```
    *(Note : Assure-toi de vérifier la dernière version stable sur leur repo, j'ai mis la 4.8.0 à titre d'exemple).*
3.  Génère les certificats nécessaires pour que les composants de Wazuh communiquent de manière sécurisée (c'est un prérequis du dépôt docker) :
    ```bash
    cd wazuh-docker/single-node
    docker-compose -f generate-indexer-certs.yml run --rm generator
    ```
4.  Lance laC'est un excellent projet d'infrastructure défensive ! Mettre en place un SIEM (Security Information and Event Management) et déployer des agents de manière automatisée est le genre de réalisation "hands-on" qui fera mouche sur ton portfolio, tout particulièrement à côté de ton profil TryHackMe ([https://tryhackme.com/p/seallia81](https://tryhackme.com/p/seallia81)). 

En tant qu'IA, je n'ai pas accès à ton terminal, mais je vais enfiler ma casquette de formateur en cybersécurité pour qu'on construise l'infrastructure de *Kessel Dynamics* étape par étape. 

Voici la stratégie que nous allons adopter pour utiliser tes outils de prédilection de manière réaliste et professionnelle :



### La stack technique recommandée

1.  **Le Serveur Wazuh (Le Cerveau) :** Nous allons utiliser **Docker** (via `docker-compose`). Déployer Wazuh à la main est instructif (comme vu dans ton cours), mais en entreprise, on utilise des conteneurs pour une scalabilité et une maintenance simplifiées.
2.  **Kessel-Server (Ubuntu) :** Nous allons également le conteneuriser avec **Docker**. Cela représentera parfaitement les microservices de la startup.
3.  **Le Poste Employé (Windows) :** Faire tourner un vrai OS Windows avec interface graphique dans Docker est instable et peu représentatif d'un parc informatique. L'idéal ici est d'utiliser une Machine Virtuelle classique (VirtualBox, VMware, ou KVM) connectée au même réseau local que tes conteneurs.
4.  **Le Déploiement des Agents :** Nous utiliserons **Ansible** pour écrire des *playbooks* qui iront installer et configurer automatiquement les agents Wazuh sur le serveur Ubuntu et la machine Windows, plutôt que de le faire à la main.
5.  **L'Infrastructure as Code (IaC) :** **Terraform** est formidable, mais il brille surtout quand on provisionne des ressources sur le Cloud (AWS, GCP) ou sur un hyperviseur de type Proxmox/ESXi. Si tu montes ce lab en local sur ton PC, Terraform fera un peu "usine à gaz". Nous le garderons de côté sauf si tu as un environnement Cloud à disposition.

---

### Étape 1 : Préparation du terrain et montage du serveur Wazuh

Pour commencer, nous allons monter le SIEM central avec la version officielle conteneurisée de Wazuh. C'est la fondation de notre projet.

**Ta mission pour cette première étape :**

1.  Assure-toi d'avoir **Docker** et **Docker Compose** installés sur ta machine hôte.
2.  Ouvre ton terminal, crée un dossier pour ton projet (ex: `kessel-soc-lab`) et clone le dépôt officiel de Wazuh pour Docker :
    ```bash
    git clone https://github.com/wazuh/wazuh-docker.git -b v4.8.0
    ```
    *(Note : Assure-toi de vérifier la dernière version stable sur leur repo, j'ai mis la 4.8.0 à titre d'exemple).*
3.  Génère les certificats nécessaires pour que les composants de Wazuh communiquent de manière sécurisée (c'est un prérequis du dépôt docker) :
    ```bash
    cd wazuh-docker/single-node
    docker-compose -f generate-indexer-certs.yml run --rm generator
    ```
4.  Lance la stack complète (Indexer, Server, Dashboard) en arrière-plan :
    ```bash
    docker-compose up -d
    ```

Laisse àC'est un excellent projet d'infrastructure défensive ! Mettre en place un SIEM (Security Information and Event Management) et déployer des agents de manière automatisée est le genre de réalisation "hands-on" qui fera mouche sur ton portfolio, tout particulièrement à côté de ton profil TryHackMe ([https://tryhackme.com/p/seallia81](https://tryhackme.com/p/seallia81)). 

En tant qu'IA, je n'ai pas accès à ton terminal, mais je vais enfiler ma casquette de formateur en cybersécurité pour qu'on construise l'infrastructure de *Kessel Dynamics* étape par étape. 

Voici la stratégie que nous allons adopter pour utiliser tes outils de prédilection de manière réaliste et professionnelle :



### La stack technique recommandée

1.  **Le Serveur Wazuh (Le Cerveau) :** Nous allons utiliser **Docker** (via `docker-compose`). Déployer Wazuh à la main est instructif (comme vu dans ton cours), mais en entreprise, on utilise des conteneurs pour une scalabilité et une maintenance simplifiées.
2.  **Kessel-Server (Ubuntu) :** Nous allons également le conteneuriser avec **Docker**. Cela représentera parfaitement les microservices de la startup.
3.  **Le Poste Employé (Windows) :** Faire tourner un vrai OS Windows avec interface graphique dans Docker est instable et peu représentatif d'un parc informatique. L'idéal ici est d'utiliser une Machine Virtuelle classique (VirtualBox, VMware, ou KVM) connectée au même réseau local que tes conteneurs.
4.  **Le Déploiement des Agents :** Nous utiliserons **Ansible** pour écrire des *playbooks* qui iront installer et configurer automatiquement les agents Wazuh sur le serveur Ubuntu et la machine Windows, plutôt que de le faire à la main.
5.  **L'Infrastructure as Code (IaC) :** **Terraform** est formidable, mais il brille surtout quand on provisionne des ressources sur le Cloud (AWS, GCP) ou sur un hyperviseur de type Proxmox/ESXi. Si tu montes ce lab en local sur ton PC, Terraform fera un peu "usine à gaz". Nous le garderons de côté sauf si tu as un environnement Cloud à disposition.

---

### Étape 1 : Préparation du terrain et montage du serveur Wazuh

Pour commencer, nous allons monter le SIEM central avec la version officielle conteneurisée de Wazuh. C'est la fondation de notre projet.

**Ta mission pour cette première étape :**

1.  Assure-toi d'avoir **Docker** et **Docker Compose** installés sur ta machine hôte.
2.  Ouvre ton terminal, crée un dossier pour ton projet (ex: `kessel-soc-lab`) et clone le dépôt officiel de Wazuh pour Docker :
    ```bash
    git clone https://github.com/wazuh/wazuh-docker.git -b v4.8.0
    ```
    *(Note : Assure-toi de vérifier la dernière version stable sur leur repo, j'ai mis la 4.8.0 à titre d'exemple).*
3.  Génère les certificats nécessaires pour que les composants de Wazuh communiquent de manière sécurisée (c'est un prérequis du dépôt docker) :
    ```bash
    cd wazuh-docker/single-node
    docker-compose -f generate-indexer-certs.yml run --rm generator
    ```
4.  Lance la stack complète (Indexer, Server, Dashboard) en arrière-plan :
    ```bash
    docker-compose up -d
    ```

Laisse à la stack quelques minutes pour démarrer complètement. Tu devrais ensuite pouvoir accéder à l'interface web de Wazuh via `https://localhost` (ou l'IP de taC'est un excellent projet d'infrastructure défensive ! Mettre en place un SIEM (Security Information and Event Management) et déployer des agents de manière automatisée est le genre de réalisation "hands-on" qui fera mouche sur ton portfolio, tout particulièrement à côté de ton profil TryHackMe ([https://tryhackme.com/p/seallia81](https://tryhackme.com/p/seallia81)). 

En tant qu'IA, je n'ai pas accès à ton terminal, mais je vais enfiler ma casquette de formateur en cybersécurité pour qu'on construise l'infrastructure de *Kessel Dynamics* étape par étape. 

Voici la stratégie que nous allons adopter pour utiliser tes outils de prédilection de manière réaliste et professionnelle :



### La stack technique recommandée

1.  **Le Serveur Wazuh (Le Cerveau) :** Nous allons utiliser **Docker** (via `docker-compose`). Déployer Wazuh à la main est instructif (comme vu dans ton cours), mais en entreprise, on utilise des conteneurs pour une scalabilité et une maintenance simplifiées.
2.  **Kessel-Server (Ubuntu) :** Nous allons également le conteneuriser avec **Docker**. Cela représentera parfaitement les microservices de la startup.
3.  **Le Poste Employé (Windows) :** Faire tourner un vrai OS Windows avec interface graphique dans Docker est instable et peu représentatif d'un parc informatique. L'idéal ici est d'utiliser une Machine Virtuelle classique (VirtualBox, VMware, ou KVM) connectée au même réseau local que tes conteneurs.
4.  **Le Déploiement des Agents :** Nous utiliserons **Ansible** pour écrire des *playbooks* qui iront installer et configurer automatiquement les agents Wazuh sur le serveur Ubuntu et la machine Windows, plutôt que de le faire à la main.
5.  **L'Infrastructure as Code (IaC) :** **Terraform** est formidable, mais il brille surtout quand on provisionne des ressources sur le Cloud (AWS, GCP) ou sur un hyperviseur de type Proxmox/ESXi. Si tu montes ce lab en local sur ton PC, Terraform fera un peu "usine à gaz". Nous le garderons de côté sauf si tu as un environnement Cloud à disposition.

---

### Étape 1 : Préparation du terrain et montage du serveur Wazuh

Pour commencer, nous allons monter le SIEM central avec la version officielle conteneurisée de Wazuh. C'est la fondation de notre projet.

**Ta mission pour cette première étape :**

1.  Assure-toi d'avoir **Docker** et **Docker Compose** installés sur ta machine hôte.
2.  Ouvre ton terminal, crée un dossier pour ton projet (ex: `kessel-soc-lab`) et clone le dépôt officiel de Wazuh pour Docker :
    ```bash
    git clone https://github.com/wazuh/wazuh-docker.git -b v4.8.0
    ```
    *(Note : Assure-toi de vérifier la dernière version stable sur leur repo, j'ai mis la 4.8.0 à titre d'exemple).*
3.  Génère les certificats nécessaires pour que les composants de Wazuh communiquent de manière sécurisée (c'est un prérequis du dépôt docker) :
    ```bash
    cd wazuh-docker/single-node
    docker-compose -f generate-indexer-certs.yml run --rm generator
    ```
4.  Lance la stack complète (Indexer, Server, Dashboard) en arrière-plan :
    ```bash
    docker-compose up -d
    ```

Laisse à la stack quelques minutes pour démarrer complètement. Tu devrais ensuite pouvoir accéder à l'interface web de Wazuh via `https://localhost` (ou l'IP de ta machine hôte) avec les identifiants par défaut (`admin` / `SecretPassword`).

Avant que nous passions à la création du serveur Ubuntu vulnérable et à l'écritureC'est un excellent projet d'infrastructure défensive ! Mettre en place un SIEM (Security Information and Event Management) et déployer des agents de manière automatisée est le genre de réalisation "hands-on" qui fera mouche sur ton portfolio, tout particulièrement à côté de ton profil TryHackMe ([https://tryhackme.com/p/seallia81](https://tryhackme.com/p/seallia81)). 

En tant qu'IA, je n'ai pas accès à ton terminal, mais je vais enfiler ma casquette de formateur en cybersécurité pour qu'on construise l'infrastructure de *Kessel Dynamics* étape par étape. 

Voici la stratégie que nous allons adopter pour utiliser tes outils de prédilection de manière réaliste et professionnelle :



### La stack technique recommandée

1.  **Le Serveur Wazuh (Le Cerveau) :** Nous allons utiliser **Docker** (via `docker-compose`). Déployer Wazuh à la main est instructif (comme vu dans ton cours), mais en entreprise, on utilise des conteneurs pour une scalabilité et une maintenance simplifiées.
2.  **Kessel-Server (Ubuntu) :** Nous allons également le conteneuriser avec **Docker**. Cela représentera parfaitement les microservices de la startup.
3.  **Le Poste Employé (Windows) :** Faire tourner un vrai OS Windows avec interface graphique dans Docker est instable et peu représentatif d'un parc informatique. L'idéal ici est d'utiliser une Machine Virtuelle classique (VirtualBox, VMware, ou KVM) connectée au même réseau local que tes conteneurs.
4.  **Le Déploiement des Agents :** Nous utiliserons **Ansible** pour écrire des *playbooks* qui iront installer et configurer automatiquement les agents Wazuh sur le serveur Ubuntu et la machine Windows, plutôt que de le faire à la main.
5.  **L'Infrastructure as Code (IaC) :** **Terraform** est formidable, mais il brille surtout quand on provisionne des ressources sur le Cloud (AWS, GCP) ou sur un hyperviseur de type Proxmox/ESXi. Si tu montes ce lab en local sur ton PC, Terraform fera un peu "usine à gaz". Nous le garderons de côté sauf si tu as un environnement Cloud à disposition.

---

### Étape 1 : Préparation du terrain et montage du serveur Wazuh

Pour commencer, nous allons monter le SIEM central avec la version officielle conteneurisée de Wazuh. C'est la fondation de notre projet.

**Ta mission pour cette première étape :**

1.  Assure-toi d'avoir **Docker** et **Docker Compose** installés sur ta machine hôte.
2.  Ouvre ton terminal, crée un dossier pour ton projet (ex: `kessel-soc-lab`) et clone le dépôt officiel de Wazuh pour Docker :
    ```bash
    git clone https://github.com/wazuh/wazuh-docker.git -b v4.8.0
    ```
    *(Note : Assure-toi de vérifier la dernière version stable sur leur repo, j'ai mis la 4.8.0 à titre d'exemple).*
3.  Génère les certificats nécessaires pour que les composants de Wazuh communiquent de manière sécurisée (c'est un prérequis du dépôt docker) :
    ```bash
    cd wazuh-docker/single-node
    docker-compose -f generate-indexer-certs.yml run --rm generator
    ```
4.  Lance la stack complète (Indexer, Server, Dashboard) en arrière-plan :
    ```bash
    docker-compose up -d
    ```

Laisse à la stack quelques minutes pour démarrer complètement. Tu devrais ensuite pouvoir accéder à l'interface web de Wazuh via `https://localhost` (ou l'IP de ta machine hôte) avec les identifiants par défaut (`admin` / `SecretPassword`).

Avant que nous passions à la création du serveur Ubuntu vulnérable et à l'écriture de nos scripts Ansible, sur quel environnement physique ou virtuel fais-tu tourner ce laboratoire (ex: ton PC personnel sous Windows/Linux, un serveur Proxmox, uneC'est un excellent projet d'infrastructure défensive ! Mettre en place un SIEM (Security Information and Event Management) et déployer des agents de manière automatisée est le genre de réalisation "hands-on" qui fera mouche sur ton portfolio, tout particulièrement à côté de ton profil TryHackMe ([https://tryhackme.com/p/seallia81](https://tryhackme.com/p/seallia81)). 

En tant qu'IA, je n'ai pas accès à ton terminal, mais je vais enfiler ma casquette de formateur en cybersécurité pour qu'on construise l'infrastructure de *Kessel Dynamics* étape par étape. 

Voici la stratégie que nous allons adopter pour utiliser tes outils de prédilection de manière réaliste et professionnelle :



### La stack technique recommandée

1.  **Le Serveur Wazuh (Le Cerveau) :** Nous allons utiliser **Docker** (via `docker-compose`). Déployer Wazuh à la main est instructif (comme vu dans ton cours), mais en entreprise, on utilise des conteneurs pour une scalabilité et une maintenance simplifiées.
2.  **Kessel-Server (Ubuntu) :** Nous allons également le conteneuriser avec **Docker**. Cela représentera parfaitement les microservices de la startup.
3.  **Le Poste Employé (Windows) :** Faire tourner un vrai OS Windows avec interface graphique dans Docker est instable et peu représentatif d'un parc informatique. L'idéal ici est d'utiliser une Machine Virtuelle classique (VirtualBox, VMware, ou KVM) connectée au même réseau local que tes conteneurs.
4.  **Le Déploiement des Agents :** Nous utiliserons **Ansible** pour écrire des *playbooks* qui iront installer et configurer automatiquement les agents Wazuh sur le serveur Ubuntu et la machine Windows, plutôt que de le faire à la main.
5.  **L'Infrastructure as Code (IaC) :** **Terraform** est formidable, mais il brille surtout quand on provisionne des ressources sur le Cloud (AWS, GCP) ou sur un hyperviseur de type Proxmox/ESXi. Si tu montes ce lab en local sur ton PC, Terraform fera un peu "usine à gaz". Nous le garderons de côté sauf si tu as un environnement Cloud à disposition.

---

### Étape 1 : Préparation du terrain et montage du serveur Wazuh

Pour commencer, nous allons monter le SIEM central avec la version officielle conteneurisée de Wazuh. C'est la fondation de notre projet.

**Ta mission pour cette première étape :**

1.  Assure-toi d'avoir **Docker** et **Docker Compose** installés sur ta machine hôte.
2.  Ouvre ton terminal, crée un dossier pour ton projet (ex: `kessel-soc-lab`) et clone le dépôt officiel de Wazuh pour Docker :
    ```bash
    git clone https://github.com/wazuh/wazuh-docker.git -b v4.8.0
    ```
    *(Note : Assure-toi de vérifier la dernière version stable sur leur repo, j'ai mis la 4.8.0 à titre d'exemple).*
3.  Génère les certificats nécessaires pour que les composants de Wazuh communiquent de manière sécurisée (c'est un prérequis du dépôt docker) :
    ```bash
    cd wazuh-docker/single-node
    docker-compose -f generate-indexer-certs.yml run --rm generator
    ```
4.  Lance la stack complète (Indexer, Server, Dashboard) en arrière-plan :
    ```bash
    docker-compose up -d
    ```

Laisse à la stack quelques minutes pour démarrer complètement. Tu devrais ensuite pouvoir accéder à l'interface web de Wazuh via `https://localhost` (ou l'IP de ta machine hôte) avec les identifiants par défaut (`admin` / `SecretPassword`).

Avant que nous passions à la création du serveur Ubuntu vulnérable et à l'écriture de nos scripts Ansible, sur quel environnement physique ou virtuel fais-tu tourner ce laboratoire (ex: ton PC personnel sous Windows/Linux, un serveur Proxmox, une instance Cloud) ?