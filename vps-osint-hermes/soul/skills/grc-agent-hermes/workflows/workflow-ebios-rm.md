# Workflow - Analyse de risque EBIOS Risk Manager (ANSSI)

**Objectif** : Conduire une analyse de risque cyber selon la méthode officielle EBIOS RM.
**Durée typique** : 6 à 10 semaines selon la taille du périmètre.
**Référentiels** : Guide EBIOS RM v1.5 (ANSSI 2018, actualisé), ISO/IEC 27005:2022.

---

## Quand utiliser EBIOS RM

- Analyse de risque initiale pour un SMSI ISO 27001 (clause 6.1.2).
- Analyse de risque sur un nouveau projet critique (homologation RGS, ANSSI).
- Cyber due diligence avant un M&A ou un partenariat critique.
- Mise à jour cyclique (annuelle ou bi-annuelle).
- Préparation au TLPT DORA (vise les sources de risque les plus crédibles).

**EBIOS RM vs autres méthodes** :
- Très adapté aux contextes français/européens (ANSSI, NIS2).
- Approche scénarisée (acteurs réels, modes opératoires concrets) plus parlante que des matrices statiques.
- Pertinent quand on veut prioriser sur les **risques réellement crédibles**, pas tout l'univers du risque.

---

## Vue d'ensemble - 5 ateliers

| # | Atelier | Durée typique | Sortie principale |
|---|---|---|---|
| 1 | Cadrage et socle de sécurité | 1-2 jours | Périmètre, missions, valeurs métier, biens supports, événements redoutés |
| 2 | Sources de risque | 1-2 jours | Liste des sources de risque pertinentes |
| 3 | Scénarios stratégiques | 2-3 jours | Chemins d'attaque haut niveau acteur → bien |
| 4 | Scénarios opérationnels | 3-5 jours | Modes opératoires détaillés (MITRE ATT&CK) |
| 5 | Traitement du risque | 2-3 jours | Plan de traitement, risques résiduels, validation Direction |

**Important** : entre chaque atelier, prévoir 5-10 jours de consolidation et de validation par les sponsors.

---

## Atelier 1 - Cadrage et socle de sécurité

### Objectif

Comprendre l'organisation, son métier, ses enjeux, son périmètre. Cartographier les biens essentiels (informations, processus métier) et les biens supports (systèmes techniques).

### Étape 1.1 - Définir le périmètre

- Périmètre métier : quels processus, quelles activités ?
- Périmètre technique : quels systèmes, quelles applications, quelles infrastructures ?
- Périmètre géographique : sites, pays.
- Périmètre organisationnel : entités, filiales.
- Périmètre temporel : situation actuelle, ou cible projetée à T+12 mois ?

### Étape 1.2 - Identifier les missions et valeurs métier

| Mission | Description | Criticité |
|---|---|---|
| Ex : Production fromages | Transformation lait → produits finis | Critique |
| Ex : Logistique livraison | Distribution réseau GMS | Élevée |

| Valeur métier | Description | Propriétaire |
|---|---|---|
| Ex : Procédés de fabrication | Savoir-faire industriel, recettes | Direction R&D |
| Ex : Données clients B2B | Base CRM, conditions commerciales | Direction commerciale |

### Étape 1.3 - Cartographier les biens supports

| Bien support | Type | Soutient quelle(s) valeur(s) métier ? | Localisation |
|---|---|---|---|
| ERP SAP | Application | Production, Achats, Compta | Datacenter Paris |
| Active Directory | Infrastructure | Toutes | Datacenter Paris + Lille |
| Plateforme e-commerce | Application | Vente B2C | Cloud AWS eu-west-3 |
| Postes de travail | Infrastructure | Toutes | Mobile (télétravail) |
| Sous-traitant paie | Tiers | RH | Externe (Cegedim) |

### Étape 1.4 - Identifier les événements redoutés

Pour chaque valeur métier, lister ce qu'on ne veut **vraiment pas** voir arriver, et évaluer la gravité.

| Valeur métier | Événement redouté | Type (CIA + traçabilité) | Gravité (1-4) | Impacts business |
|---|---|---|---|---|
| Procédés fabrication | Vol des recettes | Confidentialité | 4 | Perte avantage concurrentiel, espionnage |
| Production | Arrêt usine > 48h | Disponibilité | 4 | Pertes 200k€/jour, ruptures clients |
| Données clients | Fuite massive PII | Confidentialité | 3 | Sanction CNIL, image, clients perdus |
| Compta | Falsification | Intégrité | 3 | Risque pénal, refonte annexe comptable |

### Étape 1.5 - Établir le socle de sécurité

Le "socle de sécurité" = ce qui est en place aujourd'hui. Sert de base à l'évaluation de la vraisemblance.

Référentiels typiques utilisés :
- Politique de Sécurité existante (PSSI),
- Mesures ISO 27001 Annexe A déjà déployées,
- Guides ANSSI (40 mesures essentielles, recommandations sectorielles),
- Référentiels sectoriels (PCI-DSS, HDS, RGS, NIS2...).

**Output Atelier 1** :
- Périmètre validé.
- Cartographie missions / valeurs métier / biens supports.
- Liste des événements redoutés avec gravité.
- Socle de sécurité documenté.

---

## Atelier 2 - Sources de risque

### Objectif

Identifier les acteurs (humains, organisés ou non, voire non-humains) qui peuvent générer une menace, et caractériser leurs objectifs.

### Étape 2.1 - Lister les sources de risque pertinentes

Typologie ANSSI :

| Catégorie | Exemples | Objectifs typiques |
|---|---|---|
| États / agences étatiques | APT chinois, russes, nord-coréens | Espionnage, sabotage géopolitique |
| Cybercriminels organisés | Conti, LockBit, Black Basta, FIN7 | Lucratif (ransomware, fraude) |
| Hacktivistes | Anonymous, groupes politiques | Idéologique, atteinte image |
| Cybercriminels opportunistes | Script kiddies, ransomware-as-a-service | Lucratif facile |
| Concurrents | Espionnage industriel | Avantage compétitif |
| Insiders malveillants | Salarié, prestataire, partenaire | Vengeance, lucratif, idéologique |
| Insiders accidentels | Erreur humaine | Pas d'intention |
| Forces de la nature | Incendie, inondation, séisme | Aucune |

### Étape 2.2 - Pour chaque source, évaluer

| Source | Pertinence (1-4) | Motivation | Ressources | Justification |
|---|---|---|---|---|
| APT État sponsorisé | 2 | Espionnage R&D | Très élevées | Industrie stratégique |
| Cybercriminels (ransomware) | 4 | Lucratif | Élevées | Vague de ransomware sur secteur |
| Insider malveillant | 2 | Vengeance | Moyennes | Turnover élevé |
| Concurrent direct | 2 | Espionnage | Moyennes | Marché concurrentiel |

### Étape 2.3 - Identifier les couples Source de Risque / Objectif Visé (SR/OV)

| SR | OV (sur quelle valeur métier) |
|---|---|
| Cybercriminels ransomware | Production - arrêt usine |
| APT État | Procédés fabrication - vol recettes |
| Insider malveillant | Données clients - fuite |
| Cybercriminels phishing | Compta - fraude virement |

**Output Atelier 2** : Liste finale des SR/OV pertinents (typiquement 4 à 10 couples).

---

## Atelier 3 - Scénarios stratégiques

### Objectif

Pour chaque SR/OV, décrire **à haut niveau** comment l'attaquant pourrait atteindre son objectif (chemins d'attaque stratégiques).

### Étape 3.1 - Cartographier l'écosystème

Identifier les **parties prenantes** internes et externes qui peuvent être un point d'entrée :
- Salariés,
- Prestataires sur site,
- Fournisseurs (IT, métier),
- Partenaires (commerciaux, logistiques),
- Clients,
- Banques,
- Régulateurs,
- Filiales / maison-mère.

Pour chaque partie prenante, évaluer son **niveau de menace** (probabilité d'être compromis ou d'être un vecteur d'attaque).

### Étape 3.2 - Construire les scénarios stratégiques

Format : SR → chemin d'attaque haut niveau → événement redouté.

**Exemple - Cybercriminels ransomware visant la production** :
```
[Cybercriminels] 
   → Phishing campaign sur salariés ou prestataire IT
   → Compromission compte utilisateur 
   → Élévation privilèges via vulnérabilité non patchée
   → Latéralisation jusqu'à AD
   → Déploiement ransomware sur serveurs production
   → Arrêt usine > 48h
```

**Exemple - APT État vol recettes** :
```
[APT État sponsorisé]
   → Spear phishing ciblé Direction R&D
   → Compromission poste R&D
   → Exfiltration silencieuse documents recettes vers C2
   → Vol propriété industrielle
```

### Étape 3.3 - Évaluer chaque scénario stratégique

| Scénario | Vraisemblance (1-4) | Gravité (héritée) | Niveau de risque |
|---|---|---|---|
| Ransomware production | 4 | 4 | 16 - Critique |
| APT vol recettes | 2 | 4 | 8 - Élevé |
| Insider fuite données clients | 2 | 3 | 6 - Modéré |
| Phishing CFO fraude virement | 3 | 3 | 9 - Élevé |

**Output Atelier 3** : 10 à 20 scénarios stratégiques évalués, hiérarchisés.

---

## Atelier 4 - Scénarios opérationnels

### Objectif

Pour les scénarios stratégiques retenus comme prioritaires, **décomposer** en modes opératoires concrets (étapes techniques de l'attaque) → utiliser MITRE ATT&CK.

### Étape 4.1 - Mapping MITRE ATT&CK

Pour chaque scénario stratégique prioritaire, identifier les **tactiques** et **techniques** ATT&CK utilisées.

Exemple - Ransomware production :

| Phase | Tactique ATT&CK | Technique | Détection actuelle ? |
|---|---|---|---|
| 1 | TA0001 Initial Access | T1566.001 Spearphishing Attachment | Filtre + sensibilisation |
| 2 | TA0002 Execution | T1204.002 User Execution: Malicious File | EDR partiel |
| 3 | TA0003 Persistence | T1547.001 Registry Run Keys | EDR oui |
| 4 | TA0004 Privilege Escalation | T1068 Exploit for Privilege Escalation | Patching SLA non respecté |
| 5 | TA0008 Lateral Movement | T1021.002 SMB/Windows Admin Shares | Segmentation incomplète |
| 6 | TA0007 Discovery | T1083 File and Directory Discovery | UEBA partiel |
| 7 | TA0009 Collection | T1005 Data from Local System | Pas couvert |
| 8 | TA0040 Impact | T1486 Data Encrypted for Impact | EDR détection signatures |

### Étape 4.2 - Identifier les points de rupture

Pour chaque étape, identifier les **points de rupture** où l'attaque pourrait être stoppée par une mesure de sécurité.

### Étape 4.3 - Évaluer la vraisemblance opérationnelle

La vraisemblance opérationnelle dépend de :
- Capacités de l'attaquant (ressources, sophistication).
- Mesures de sécurité en place sur le chemin.
- Probabilité de détection à chaque étape.

**Output Atelier 4** :
- Cartographie ATT&CK pour les top scénarios.
- Points de rupture identifiés.
- Vraisemblance opérationnelle affinée.

---

## Atelier 5 - Traitement du risque

### Objectif

Définir le plan de traitement, valider les risques résiduels avec la Direction.

### Étape 5.1 - Définir la stratégie de traitement pour chaque risque

4 options ISO 27005 / EBIOS RM :
- **Réduire** : déployer des mesures supplémentaires.
- **Accepter** : laisser tel quel (Direction signe).
- **Transférer** : assurance cyber, externalisation.
- **Refuser** : arrêter l'activité génératrice du risque.

### Étape 5.2 - Sélectionner les mesures de sécurité

Pour les risques à réduire :
- Identifier les **points de rupture** prioritaires de l'Atelier 4.
- Sélectionner des contrôles ISO 27001 Annexe A (mapping) ou autres référentiels.
- Évaluer le coût (CAPEX + OPEX) et l'efficacité attendue.
- Calculer le risque résiduel post-mesure.

### Étape 5.3 - Construire le plan de traitement

| Risque | Mesure(s) | Mapping ISO 27001 | Owner | Échéance | Coût | Risque résiduel cible | KPI/KRI |
|---|---|---|---|---|---|---|---|
| Ransomware prod | Backups immuables + tests trim. | A.8.13 | DSI | T+90j | 80 k€ | Élevé → Modéré | RPO mesuré |
| APT vol recettes | DLP + classification + monitoring | A.5.12, A.8.12, A.8.16 | RSSI | T+180j | 120 k€ | Élevé → Modéré | Alertes DLP traitées |

### Étape 5.4 - Validation Direction et acceptation des risques résiduels

Présenter à la Direction :
- Top risques évalués,
- Coût du traitement,
- Risque résiduel attendu,
- Risques **acceptés** (signature explicite Direction).

**Output Atelier 5** :
- Plan de traitement détaillé (`templates/plan-traitement-risques.md`).
- Registre des risques mis à jour (`templates/registre-risques.csv`).
- PV de validation Direction avec acceptation des risques résiduels.

---

## Restitution finale

Document de synthèse (30-50 pages typique) :
1. Résumé exécutif (1 page CODIR).
2. Méthodologie EBIOS RM.
3. Atelier 1 - Cadrage et socle.
4. Atelier 2 - Sources de risque.
5. Atelier 3 - Scénarios stratégiques.
6. Atelier 4 - Scénarios opérationnels.
7. Atelier 5 - Plan de traitement.
8. Risques résiduels acceptés.
9. Annexes (MITRE ATT&CK, mapping ISO, registres).

---

## Conseils pour Hermes

1. **EBIOS RM est consommateur de temps**. Ne pas le proposer pour une PME < 50 personnes ; préférer une analyse simplifiée (Excel + ISO 27005 light).
2. **Impliquer les métiers**. Sans eux, les valeurs métier sont mal identifiées et la gravité mal évaluée.
3. **Sources de risque réalistes**. Inutile de mettre l'APT chinois si on n'a aucun actif stratégique - ça décrédibilise l'analyse.
4. **MITRE ATT&CK n'est pas obligatoire** mais fortement recommandé pour l'Atelier 4 : c'est ce qui rend l'analyse opérationnelle et pas théorique.
5. **Risques résiduels = signature Direction obligatoire**. C'est le point clé qui transfère la responsabilité juridique.
6. **L'analyse n'est pas une fin en soi** : sans plan de traitement actionné, c'est du papier mort.
7. **Cycle de vie** : EBIOS RM doit être révisé annuellement, et systématiquement après un changement majeur (M&A, nouveau service critique, incident).
