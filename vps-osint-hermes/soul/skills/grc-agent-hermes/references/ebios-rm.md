# EBIOS Risk Manager (EBIOS RM) — Référence opérationnelle

## Pourquoi EBIOS RM

EBIOS Risk Manager est la **méthode d'analyse de risques cyber officielle de l'ANSSI** (mise à jour 2018). Elle est :
- Compatible ISO 27005 et ISO 31000
- Reconnue dans les marchés publics français et OIV/OSE
- Conçue pour produire un **dialogue stratégique** entre DSI, Direction, métier — pas juste un tableur

**Différence clé avec ISO 27005 / FAIR** : EBIOS RM se concentre sur les **scénarios stratégiques** (qui attaque, pourquoi, comment) avant les scénarios opérationnels (par quels chemins). C'est une approche **par sources de risque et objectifs visés**, pas par vulnérabilités.

## Structure : 5 ateliers

```
Atelier 1 — Cadrage et socle de sécurité
        ↓
Atelier 2 — Sources de risque
        ↓
Atelier 3 — Scénarios stratégiques
        ↓
Atelier 4 — Scénarios opérationnels
        ↓
Atelier 5 — Traitement du risque
```

Les ateliers sont **séquentiels** mais peuvent itérer. Ne saute jamais un atelier.

## Atelier 1 — Cadrage et socle de sécurité

**Objectif** : Définir le périmètre, identifier les valeurs métier, les biens supports, le socle de sécurité existant.

### Livrables
- Périmètre de l'étude (entités, sites, processus métiers inclus/exclus)
- Liste des **valeurs métier** (activités, processus, informations critiques)
- Liste des **biens supports** (applications, serveurs, réseaux, locaux, personnes)
- Liste des **événements redoutés** par valeur métier (avec niveau de gravité)
- Socle de sécurité existant (référentiel et écarts connus)
- Parties prenantes (internes, externes)

### Méthode
1. Atelier de 2h avec Direction + métiers + DSI
2. Cartographier les valeurs métier (max 8-10)
3. Pour chaque valeur métier : "Que craint-on qu'il arrive ?" = événement redouté
4. Coter la gravité de chaque ER sur échelle 1-4 :
   - 1 Mineure
   - 2 Significative
   - 3 Grave
   - 4 Critique

### Exemple
**Valeur métier** : Continuité du service de paiement en ligne
**Biens supports** : Site e-commerce, API paiement, base clients, datacenter primaire
**Événements redoutés** :
- Indisponibilité du service > 4h (Gravité 3)
- Détournement de paiements (Gravité 4)
- Fuite données clients (Gravité 4)

## Atelier 2 — Sources de risque

**Objectif** : Identifier qui pourrait attaquer et pour quel objectif.

### Concepts
- **Source de risque (SR)** : qui (ex. cybercriminels, État, concurrent, hacktiviste, employé malveillant)
- **Objectif visé (OV)** : pourquoi (ex. gain financier, espionnage, déstabilisation, sabotage)

### Méthode
1. Brainstorming des couples SR/OV
2. Pour chaque couple : pertinence (faible / moyenne / forte / critique)
3. Retenir les couples **pertinents** pour la suite

### Sources de risque typiques (2025)
| Source | Motivation | Profil |
|--------|------------|--------|
| Cybercriminel organisé | Gain financier (ransomware, extorsion) | Ressources élevées, sophistiqué |
| État (APT) | Espionnage économique ou politique | Ressources illimitées |
| Concurrent | Espionnage industriel | Variable |
| Hacktiviste | Idéologique, image | Faible à moyen |
| Insider malveillant | Vengeance, gain personnel | Accès interne |
| Insider négligent | Erreur, méconnaissance | Non malveillant mais à risque |
| Prestataire compromis | Supply chain | Variable |

## Atelier 3 — Scénarios stratégiques

**Objectif** : Imaginer **comment** une source de risque pourrait atteindre son objectif.

### Concepts
- **Scénario stratégique** : narratif de haut niveau "SR → cherche à atteindre OV → en passant par parties prenantes → impactant valeur métier → causant ER"
- **Chemin d'attaque stratégique** : enchaînement de parties prenantes à compromettre

### Méthode
1. Pour chaque couple SR/OV retenu, construire 1 à 3 scénarios stratégiques
2. Identifier les **parties prenantes critiques** (fournisseurs, prestataires, partenaires)
3. Coter la **gravité** (issue de l'ER ciblé) et la **vraisemblance** stratégique (V1 à V4)

### Exemple
**Scénario stratégique** : Un groupe cybercriminel cible le site e-commerce via son prestataire de paiement (partie prenante), en exploitant une vulnérabilité de leur API, pour exfiltrer la base clients (événement redouté : fuite données). Gravité 4, Vraisemblance V3.

## Atelier 4 — Scénarios opérationnels

**Objectif** : Détailler **techniquement** comment l'attaque se déroulerait, étape par étape, sur les biens supports.

### Concepts
- **Scénario opérationnel** : suite d'**actions élémentaires** (kill chain, ATT&CK)
- **Vraisemblance opérationnelle** : probabilité de réussite de la chaîne

### Méthode
1. Pour chaque scénario stratégique pertinent, détailler la kill chain
2. Référencer **MITRE ATT&CK** ou une autre matrice (techniques, tactiques)
3. Coter la vraisemblance opérationnelle (V1 à V4)
4. La vraisemblance finale du scénario = combinaison stratégique × opérationnel

### Exemple (suite)
1. **Reconnaissance** : OSINT sur le prestataire de paiement
2. **Initial access** : Phishing ciblé sur un dev du prestataire (T1566 ATT&CK)
3. **Credential access** : Vol de token API
4. **Lateral movement** : Accès à l'API de production
5. **Exfiltration** : Téléchargement BDD clients via API légitime
6. **Impact** : Mise en vente sur darknet, demande de rançon

## Atelier 5 — Traitement du risque

**Objectif** : Décider quoi faire de chaque risque.

### Concepts
- **Risque inhérent** : niveau avant mesures
- **Mesures de traitement** : nouvelles mesures ou renforcements
- **Risque résiduel** : niveau après mesures
- **Plan d'amélioration continue (PACS)** : roadmap de mise en œuvre

### Options de traitement
| Option | Quand l'utiliser |
|--------|------------------|
| Réduire | Quand le risque est inacceptable mais traitable |
| Accepter (assumer) | Quand le coût des mesures > impact estimé |
| Refuser (éviter) | Arrêter l'activité génératrice de risque |
| Transférer (partager) | Assurance cyber, sous-traitance contractualisée |

### Livrables finaux
- Matrice des risques (gravité × vraisemblance, avant/après)
- Plan d'amélioration continue de la sécurité (PACS) avec :
  - Mesures
  - Owners
  - Échéances
  - Coût estimé
  - Indicateurs de suivi
- Note de validation par la Direction

## Format de sortie recommandé

EBIOS RM produit beaucoup de tableaux. Voici les principaux à livrer :

| Atelier | Tableau de sortie |
|---------|-------------------|
| A1 | Valeurs métier × Événements redoutés × Gravité |
| A2 | Couples SR/OV avec pertinence |
| A3 | Scénarios stratégiques avec gravité × vraisemblance |
| A4 | Scénarios opérationnels avec kill chain et vraisemblance |
| A5 | Plan de traitement (mesures, owners, échéances, résiduel) |

## Erreurs classiques

1. **Sauter l'Atelier 1** : sans cadrage, l'analyse est hors-sol
2. **Confondre source de risque et menace technique** : la SR est qui, pas comment
3. **Trop de scénarios** : limiter à 6-10 scénarios stratégiques majeurs
4. **Pas de cotation** : sans gravité ni vraisemblance, pas de hiérarchisation
5. **Plan de traitement sans owner** : risque immédiat de non-exécution
6. **Ne pas itérer** : EBIOS doit être révisé au minimum annuellement

## Outils complémentaires

- **MITRE ATT&CK** : pour structurer les scénarios opérationnels
- **Outil ANSSI Egerie/Risk Manager** : pour les missions de grande taille
- **Excel/CSV** : suffisant pour les missions <500 actifs

## Mapping ISO 27005 ↔ EBIOS RM

| ISO 27005 | EBIOS RM |
|-----------|----------|
| Établissement du contexte | Atelier 1 |
| Identification des risques | Ateliers 2-3-4 |
| Estimation des risques | Cotations gravité × vraisemblance |
| Évaluation des risques | Hiérarchisation |
| Traitement des risques | Atelier 5 |
| Acceptation des risques | Validation Direction |
| Communication | Tout au long |
| Surveillance/Réexamen | Cycle annuel |

EBIOS RM = ISO 27005 + dimension stratégique narrative + ancrage français/ANSSI.
