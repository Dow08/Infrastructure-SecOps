# Architecture Logique et Topologie

## 1. Structure de la Forêt
Relation d'approbation (Trust) bidirectionnelle et transitive entre le domaine parent et les domaines enfants.

* **DC01-PROD (Dow01.local) :** Rôles FSMO de la forêt (Schema Master, Domain Naming Master).
* **DC02-PARIS (Paris.Dow01.local) :** Infrastructure succursale FR.
* **DC03-LONDON (London.Dow01.local) :** Infrastructure succursale UK.

## 2. Unités d'Organisation (OUs)
Structure répliquée sur chaque domaine pour compartimenter les droits et cibler les GPOs :

* `OU=ENTREPRISE`
  * `OU=Direction` (Cibles VIP)
  * `OU=Ressources_Humaines` (Données sensibles / PII)
  * `OU=Finance_Comptabilite` 
  * `OU=Informatique` (Admins locaux / Tier 1 & 2)
  * `OU=Marketing`
  * `OU=Commercial`
  * `OU=Production`
  * `OU=Logistique`
  * `OU=Recherche_Developpement`
  * `OU=Comptes_De_Service` (Isolation stricte pour contrer le Kerberoasting)

## 3. Gestion des accès (Modèle AGDLP)
Application stricte du standard Microsoft pour les permissions NTFS et partages réseau :
1. **A**ccounts : Comptes utilisateurs (ex: `j.dupont`).
2. **G**lobal Groups : Regroupement par fonction métier (ex: `GG-Ressources_Humaines`).
3. **D**omain **L**ocal Groups : Définition de la permission (ex: `GL-Partage-RH-Lecture`).
4. **P**ermissions : Les droits sont assignés uniquement au groupe local.