# Workflow - Mise en conformité NIS2

**Objectif** : Conduire une organisation de l'identification de son obligation NIS2 jusqu'à la conformité opérationnelle.
**Durée typique** : 6 à 12 mois selon le niveau de maturité initial.
**Référentiels** : Directive UE 2022/2555 (NIS2), Loi française REVOSCYB du 30/10/2024, transpositions nationales.

---

## Quand utiliser ce workflow

- Organisation soupçonnée d'entrer dans le périmètre NIS2 (vérification).
- Notification reçue d'une autorité (ANSSI ou homologue européen).
- Demande client / partenaire pour démontrer la conformité.
- Mise en conformité volontaire dans une logique de mise à niveau cyber.

---

## Phase 0 - Qualification de l'éligibilité (1-2 semaines)

### Étape 0.1 - Vérifier l'appartenance au périmètre

L'organisation est concernée par NIS2 si elle remplit cumulativement :

1. **Secteur d'activité** : Annexe I (entités essentielles) ou Annexe II (entités importantes) de la directive.
   - Annexe I (10 secteurs essentiels) : énergie, transport, banque, infrastructure marché financier, santé, eau potable, eaux usées, infrastructure numérique, gestion services TIC B2B, administration publique, espace.
   - Annexe II (8 secteurs importants) : services postaux, gestion des déchets, fabrication produits chimiques, denrées alimentaires, fabrication, fournisseurs numériques, recherche.

2. **Seuil de taille** :
   - Moyennes entreprises : 50 à 249 salariés ou CA 10 à 50 M€ ou total bilan 10 à 43 M€.
   - Grandes entreprises : ≥ 250 salariés ou CA > 50 M€ ou total bilan > 43 M€.

3. **Exceptions** : certaines entités sont concernées **quelle que soit leur taille** (DNS, registres TLD, services de confiance qualifiés, opérateurs de services essentiels désignés...).

### Étape 0.2 - Classification entité essentielle / importante

| Type | Sanctions max | Exigences |
|---|---|---|
| **Entité essentielle (EE)** | 10 M€ ou 2% du CA mondial | Supervision proactive |
| **Entité importante (EI)** | 7 M€ ou 1,4% du CA mondial | Supervision réactive (après incident/plainte) |

**Output Phase 0** :
- Position claire : concerné / non concerné.
- Classification EE ou EI.
- Identification de l'autorité compétente (ANSSI en France).

---

## Phase 1 - Gap Analysis (4-6 semaines)

### Étape 1.1 - Évaluer l'existant vs les 16 mesures de l'Article 21

Article 21 NIS2 - 10 catégories de mesures techniques, opérationnelles et organisationnelles "tous risques" :

| # | Mesure NIS2 art. 21 | Mapping ISO 27001 Annexe A |
|---|---|---|
| a | Politiques d'analyse de risque + sécurité SI | A.5.1, clause 6.1 |
| b | Gestion des incidents | A.5.24 à A.5.28 |
| c | Continuité d'activité (sauvegarde, reprise, gestion de crise) | A.5.29, A.5.30, A.8.13, A.8.14 |
| d | Sécurité chaîne d'approvisionnement | A.5.19, A.5.20, A.5.21, A.5.22, A.5.23 |
| e | Sécurité acquisition, développement, maintenance SI (vulnérabilités) | A.8.8, A.8.25 à A.8.30 |
| f | Politiques et procédures d'évaluation de l'efficacité des mesures | Clause 9.1 + A.5.36 |
| g | Hygiène cyber de base + formation | A.6.3 |
| h | Politiques et procédures de chiffrement | A.8.24 |
| i | Sécurité des ressources humaines, politique de contrôle d'accès, gestion des actifs | A.5.9 à A.5.18, A.6.1 à A.6.8 |
| j | Authentification multifactorielle (MFA), communications sécurisées vocales/vidéo, communications d'urgence sécurisées | A.5.17, A.8.5 |

Note : les "16 mesures" couramment évoquées proviennent du détail des 10 catégories ci-dessus, parfois découpées différemment dans les transpositions nationales.

**Outils** : `scripts/gap_analysis_iso27001.py` pour évaluer l'existant + matrice de mapping spécifique NIS2.

### Étape 1.2 - Évaluer la gouvernance (Article 20)

**Article 20 NIS2 - Responsabilité des organes de direction** :
- Les organes de direction doivent **approuver** les mesures de gestion des risques cyber.
- Ils doivent **superviser** leur mise en œuvre.
- Ils sont **responsables** en cas de non-conformité (responsabilité personnelle possible selon transposition nationale).
- Ils doivent **suivre une formation cyber régulière** et **assurer** la formation de leurs employés.

Cette exigence est nouvelle, structurante et souvent sous-estimée. À évaluer :
- Existe-t-il un Comité de pilotage cyber avec présence Direction ?
- Les dirigeants ont-ils suivi une formation cyber dans les 12 derniers mois ?
- Existe-t-il un PV signé Direction validant la stratégie cyber ?

### Étape 1.3 - Évaluer le dispositif de notification

**Obligation de notification multi-temps** :

| Délai | Action | Destinataire |
|---|---|---|
| 24 heures | **Alerte précoce** (early warning) - notification initiale | CSIRT + autorité compétente (ANSSI) |
| 72 heures | **Notification d'incident** complète | CSIRT + autorité compétente |
| 1 mois | **Rapport final** | CSIRT + autorité compétente |
| À la demande | **Rapports intermédiaires** | CSIRT + autorité compétente |

À évaluer :
- Procédure de qualification d'un "incident significatif" existe-t-elle ?
- Astreinte 24/7 capable d'envoyer une alerte sous 24h ?
- Procédure RETEX produisant un rapport final structuré ?

### Étape 1.4 - Cartographier les écarts

**Output Phase 1** :
- Rapport de gap analysis NIS2 (matrice "exigence vs existant vs écart").
- Score de conformité initial (typiquement 30-60% pour une PME sans démarche préalable).
- Top 10 écarts critiques.

---

## Phase 2 - Plan de mise en conformité (2-3 semaines)

### Étape 2.1 - Prioriser les actions

Approche en 3 vagues :

**Vague 1 (3 mois) - Fondations** :
- Désignation RSSI (formel, fiche de poste, lettre de mission).
- Politique de sécurité signée par la Direction.
- Procédure d'incident + cellule de crise opérationnelle (sans laquelle la notification 24h est impossible).
- MFA sur accès distants et comptes privilégiés.
- Sauvegardes immuables testées.
- Formation cyber des dirigeants (au minimum 1 session).

**Vague 2 (6 mois) - Gestion des risques** :
- Analyse de risque EBIOS RM ou équivalent.
- Registre des actifs + classification.
- Plan de traitement des risques.
- Gestion des vulnérabilités (scan + patch SLA).
- Sécurité chaîne d'approvisionnement (clauses contractuelles, tiering fournisseurs).
- Plan de continuité PCA/PRA testé.

**Vague 3 (12 mois) - Maturité** :
- SOC ou MSSP opérationnel (détection 24/7).
- Tests de pénétration annuels.
- Tableau de bord KPI/KRI.
- Audit interne SMSI.
- Certification ISO 27001 (option, couvre 80% des exigences NIS2).

### Étape 2.2 - Budget et ressources

Estimation typique pour une PME 100-250 personnes sans démarche préalable :
- **Investissement initial** : 150 à 400 k€ (selon outils choisis).
- **Run annuel** : 150 à 350 k€ (RSSI + outils + MSSP).
- **Équipe** : RSSI dédié (1 ETP) + DPO (existant ou externalisé) + ressources opérationnelles DSI.

### Étape 2.3 - Plan d'action détaillé

| Action | Vague | Owner | Coût | Échéance | Indicateur |
|---|---|---|---|---|---|
| Désignation RSSI | 1 | DG | 80 k€/an | M+1 | Lettre mission signée |
| PSSI signée | 1 | RSSI | 0 | M+2 | PSSI publiée |
| Procédure incidents | 1 | RSSI | 5 k€ | M+3 | Procédure + 1 exercice |
| MFA généralisé | 1 | DSI | 30 k€ | M+3 | 95% comptes |
| Backup immuable | 1 | DSI | 40 k€ | M+3 | Test restauration OK |
| Formation Direction | 1 | RH | 5 k€ | M+3 | 100% dirigeants |
| EBIOS RM | 2 | RSSI | 25 k€ | M+6 | Analyse validée |
| Registre actifs | 2 | DSI | 15 k€ | M+6 | 100% actifs critiques |
| Vulnérabilités | 2 | DSI | 25 k€/an | M+6 | Scanner + SLA |
| Supply chain | 2 | Achats | 10 k€ | M+6 | Top 20 fournisseurs |
| PCA testé | 2 | RSSI+DSI | 50 k€ | M+8 | Test annuel OK |
| MSSP SOC | 3 | RSSI | 80 k€/an | M+12 | Détection 24/7 |
| Audit interne | 3 | RSSI | 15 k€ | M+12 | Rapport |

---

## Phase 3 - Exécution (6-12 mois)

### Étape 3.1 - Gouvernance du programme

- Comité de pilotage mensuel avec Direction.
- Reporting d'avancement standardisé.
- Indicateurs d'avancement et d'efficacité.
- Gestion des risques projet (retard, dépassement, dérive scope).

### Étape 3.2 - Communication et conduite du changement

- Communication régulière interne (intranet, mémo Direction).
- Onboarding des managers sur leurs nouvelles responsabilités.
- Formation cyber étalée sur l'année (par populations : direction, IT, métier, RH, achats).

### Étape 3.3 - Articulation avec autres réglementations

Vérifier les recouvrements pour éviter les doublons :
- **RGPD** : sécurité art. 32, notification 72h CNIL.
- **DORA** : si entité du secteur financier, surcouche supplémentaire (incidents 4h, TLPT...).
- **NIS2 vs ISO 27001** : ISO 27001 couvre ~80% des exigences NIS2.

**Outils** : `references/mapping-crosswalk.md` pour la vue consolidée.

---

## Phase 4 - Démonstration de conformité (continue)

### Étape 4.1 - Documentation à maintenir à jour

NIS2 ne demande pas formellement une "certification" mais l'autorité peut **demander des preuves** à tout moment. Documents minimums :

- Politique de Sécurité signée Direction (datée < 12 mois).
- Cartographie des risques actualisée.
- Plan de traitement des risques.
- Procédures incident, continuité, supply chain.
- Registre des incidents et des notifications.
- Rapports d'audit interne / externe.
- Preuves de formation Direction et personnel.
- Inventaire des actifs critiques.
- Liste des fournisseurs TIC critiques.

### Étape 4.2 - Préparation à un audit / inspection ANSSI

L'ANSSI peut, surtout pour les EE, demander :
- Audits ad hoc en cas d'incident signalé.
- Audits programmés (typiquement tous les 2-3 ans).
- Demandes de preuves sur sollicitation.

Conseil : maintenir un "**dossier de preuves NIS2**" centralisé, mis à jour trimestriellement, prêt à être présenté en moins de 48h.

### Étape 4.3 - Tableau de bord NIS2 récurrent

Indicateurs à reporter mensuellement (RSSI → Direction) :
- % de complétion du plan d'action.
- Délais MTTD / MTTR / MTTC des incidents.
- % de patch critiques dans le SLA.
- Taux de couverture MFA.
- Taux de formation cyber Direction et personnel.
- Nombre d'incidents notifiés à l'ANSSI dans l'année.

**Outils** : `templates/tableau-bord-kpi-kri.md`.

---

## Phase 5 - Maintien en conformité (continue)

### Activités récurrentes

| Activité | Fréquence | Owner |
|---|---|---|
| Revue de Direction SMSI | Annuelle | DG + RSSI |
| Mise à jour analyse de risques | Annuelle | RSSI |
| Test PCA/PRA | Annuelle (au minimum) | DSI + RSSI |
| Audit interne | Annuelle | Audit / RSSI |
| Sensibilisation cyber | Annuelle | RSSI + RH |
| Formation Direction | Annuelle | RH |
| Revue fournisseurs critiques | Annuelle | Achats + RSSI |
| Revue accès | Semestrielle | DSI |
| Scan vulnérabilités | Mensuel | DSI |
| Reporting indicateurs | Mensuel | RSSI |

---

## Conseils pour Hermes

1. **L'Article 20 est sous-estimé**. Beaucoup d'organisations focalisent sur la technique et oublient la formation Direction + leur responsabilité personnelle. À mettre dans les premiers points de l'audit.
2. **24h pour l'alerte précoce** est un délai très court. Sans astreinte 24/7 et procédure rodée, l'organisation est en non-conformité par construction.
3. **NIS2 ne demande pas l'ISO 27001**, mais l'ISO 27001 facilite massivement la conformité NIS2 (80% de couverture).
4. **Supply chain** : c'est le point d'attention 2025-2026. Identifier le Top 20 fournisseurs critiques, leur faire signer un addendum cyber, les auditer.
5. **NIS2 est une obligation de moyens, pas de résultat**. Si l'organisation peut démontrer qu'elle a mis en place les mesures **proportionnées au risque**, elle est conforme même en cas d'incident.
6. **Veiller à l'application nationale** (REVOSCYB en France) : la transposition peut ajouter des exigences locales (délais, autorités, sanctions spécifiques).
7. **Croisement DORA / NIS2 / RGPD** : un même incident peut déclencher 3 notifications avec délais différents. Préparer une procédure unique de qualification multi-réglementaire.
