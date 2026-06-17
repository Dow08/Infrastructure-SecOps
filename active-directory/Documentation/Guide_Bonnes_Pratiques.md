# Standards de Sécurité AD

Principes appliqués sur l'infrastructure pour limiter la surface d'attaque et bloquer les mouvements latéraux.

## 1. Modèle en Tiers (Tiering)
Ségrégation stricte des privilèges d'administration pour bloquer le Pass-The-Hash :
* **Tier 0 :** Contrôleurs de domaine. Les Enterprise/Domain Admins ne se connectent jamais sur des machines Tier 1 ou Tier 2.
* **Tier 1 :** Serveurs de fichiers, BDD, applicatifs.
* **Tier 2 :** Postes de travail utilisateurs.

## 2. Moindre Privilège (PoLP)
* Les utilisateurs standards n'ont pas les droits d'administrateur local sur leur poste.
* Les comptes de l'OU `Comptes_De_Service` utilisent exclusivement le droit "Log on as a service" et n'ont pas d'accès interactif (Deny log on locally).

## 3. Hygiène GPO
* Une GPO = Une fonction (ex: `SEC-Block-CMD`).
* Application au plus proche de la cible (liaison sur les OUs métier, pas à la racine du domaine sauf nécessité absolue).
* Aucune modification des permissions directes sur les conteneurs par défaut (`CN=Users`, `CN=Computers`).

## 4. Intégrité de l'annuaire
Activation systématique de la protection contre la suppression accidentelle sur toutes les OUs, groupes et comptes de service.