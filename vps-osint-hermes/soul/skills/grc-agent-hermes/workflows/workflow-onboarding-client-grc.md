# Workflow - Onboarding d'un client GRC

**Objectif** : Démarrer une mission de conseil GRC chez un nouveau client de manière structurée, en posant les bases d'une relation de confiance et d'un cadrage clair.
**Durée typique** : 2 à 4 semaines (du premier contact à la première vraie production de valeur).
**Public cible** : Consultant GRC en mission chez un client (ESN/MSSP, freelance, audit).

---

## Quand utiliser ce workflow

- Nouveau client signé après commercial.
- Reprise d'une mission GRC d'un confrère ou d'un cabinet précédent.
- Démarrage d'un programme transverse (mise en conformité, certification).
- Première intervention chez un client existant sur un nouveau périmètre.

---

## Phase 0 - Pré-engagement (avant signature)

### Étape 0.1 - Qualification commerciale

Questions à poser **avant** la signature pour cadrer correctement :

| Question | Pourquoi |
|---|---|
| Quel est le déclencheur de la demande ? (incident, audit, certification, client...) | Comprendre l'urgence et la motivation réelle |
| Quel sponsor exécutif ? | Sans sponsor Direction, l'échec est probable |
| Quel budget alloué ? | Cadrer le périmètre proportionnellement |
| Quel niveau de maturité actuel ? | Estimer le delta à combler |
| Quelle équipe interne en face ? | Calibrer la charge consultant vs interne |
| Y a-t-il une cible précise (certification, conformité, échéance) ? | Définir la définition du "fait" |

### Étape 0.2 - Devis et contractualisation

Points à clarifier dans le contrat :
- Périmètre détaillé (ce qui est inclus / exclu).
- Livrables précis (avec format et critères d'acceptation).
- Modalités d'intervention (présentiel, distantiel, mix).
- Accès au SI client (comptes, VPN, badges).
- Confidentialité et propriété intellectuelle.
- Conditions de modification de scope.
- Responsabilité civile professionnelle.

---

## Phase 1 - Kick-off et découverte (Semaine 1)

### Étape 1.1 - Réunion de lancement (jour 1)

Participants : sponsor exécutif, client opérationnel, équipe consultant.

Ordre du jour :
1. Présentation des équipes.
2. Rappel des objectifs et du planning.
3. Validation du périmètre.
4. Identification des risques projet (résistance interne, charge, dépendances).
5. Définition de la gouvernance projet (comité, cadence, reporting).
6. Modalités d'accès aux ressources et personnes clés.

**Output** : Compte-rendu de kick-off + plan d'action S1-S2 signé.

### Étape 1.2 - Cartographie initiale

Premier diagnostic à mener sur :

**Organisation** :
- Organigramme général + équipe IT/sécurité.
- Existence et identité du RSSI, DPO, DSI.
- Existence et fréquence des comités de pilotage cyber.
- Sponsor exécutif identifié et engagé ?

**Référentiels existants** :
- Documents disponibles (PSSI, SoA, registre risques, procédures...).
- Référentiels actuellement suivis (ISO, NIST, CIS, sectoriels...).
- Audits récents et leurs conclusions.

**Réglementations applicables** :
- RGPD : oui systématiquement.
- NIS2 : oui si entité essentielle / importante (cf. workflow dédié).
- DORA : oui si secteur financier.
- Sectoriels : HDS, PCI-DSS, RGS, IEC 62443, ISO 13485, etc.

**Périmètre technique** :
- Nombre approximatif d'utilisateurs, de sites, de serveurs.
- Cloud / on-premise / hybride.
- Volume de données personnelles traitées.
- Fournisseurs TIC critiques.

**Output** : Note de découverte (5-10 pages) avec premier diagnostic.

### Étape 1.3 - Entretiens prioritaires (jours 2-5)

Liste type des 8 à 10 entretiens d'1h chacun, dans la première semaine :

1. **Sponsor exécutif** : enjeux business, attentes, contraintes politiques.
2. **RSSI** : maturité actuelle, projets en cours, points de douleur.
3. **DPO** : périmètre RGPD, sujets sensibles, registre.
4. **DSI** : architecture, exploitation, équipes.
5. **Lead Sécurité / Architecte** : technique, outils, dette.
6. **RH** : sensibilisation, charte, formation.
7. **Achats** : fournisseurs critiques, contrats, supply chain.
8. **Juridique** : contrats, contentieux, veille réglementaire.
9. **Direction métier (1-2)** : priorités business, dépendance IT.
10. **Audit / Risk** : maturité ERM, articulation cyber/risque global.

**Méthode** : entretiens semi-directifs, prise de notes structurée par thème, validation à chaud du compte-rendu.

---

## Phase 2 - Cadrage approfondi (Semaine 2)

### Étape 2.1 - Choisir le ou les référentiels structurants

Décision à prendre avec le client :

| Si l'objectif est... | Référentiel recommandé |
|---|---|
| Certification ISO 27001 | ISO 27001:2022 |
| Conformité NIS2 | ISO 27001 (couvre 80%) + spécificités NIS2 |
| Conformité DORA | ISO 27001 + spécificités DORA (TLPT, registre information) |
| Maturité progressive | NIST CSF 2.0 (échelle Tier 1-4) |
| Privacy / RGPD avancé | ISO 27701 + méthode CNIL PIA |
| Quantification financière | FAIR + référentiel principal |
| Multi-conformité (US + EU) | NIST CSF + ISO 27001 + mapping SOC 2 |

### Étape 2.2 - Définir la feuille de route

3 horizons :
- **Court terme (0-3 mois)** : actions de gain rapide (quick wins), pose des fondations.
- **Moyen terme (3-9 mois)** : déploiement des chantiers structurants.
- **Long terme (9-18 mois)** : maturité, certification, optimisation.

Pour chaque chantier :
- Objectif (mesurable).
- Owner client.
- Coût estimé.
- Charge consultant.
- Échéance cible.
- Dépendances.
- Critère de succès.

**Output** : Feuille de route consolidée validée en Comité.

### Étape 2.3 - Définir la gouvernance du programme

| Rythme | Format | Participants | Objet |
|---|---|---|---|
| Hebdomadaire | Stand-up 30 min | Consultant + client opérationnel | Avancement, blocages |
| Bi-hebdomadaire | Point chantier 1h | Consultant + leads | Détails techniques |
| Mensuel | Comité de pilotage 1h30 | Consultant + RSSI + sponsor | Reporting, décisions |
| Trimestriel | Comité de direction 2h | Tous + Direction | Stratégie, budget, escalade |

### Étape 2.4 - Définir les indicateurs

Indicateurs à reporter dès le démarrage :
- Avancement du plan d'action (%).
- Maturité par domaine (échelle 0-5).
- Risques projet ouverts et leur statut.
- Charges consommées vs budget.
- Top 3 risques en cours.

---

## Phase 3 - Premiers livrables (Semaines 3-4)

### Étape 3.1 - Quick wins (à livrer sous 3 semaines)

L'objectif est de démontrer rapidement la valeur du consultant. Quick wins typiques :

- **Cartographie des risques** sommaire (10-20 risques principaux).
- **Gap analysis** synthétique vs référentiel cible (top 10 écarts).
- **Plan d'action 0-3 mois** chiffré et priorisé.
- **Matrice RACI** des rôles et responsabilités GRC.
- **Modèles de documents** (PSSI, procédures incident, registre RGPD) adaptés au client.
- **Présentation Direction** synthétique (1 slide diagnostic, 1 slide plan).

### Étape 3.2 - Première restitution

Au plus tard 4 semaines après le démarrage, présenter devant la Direction :
- Diagnostic synthétique (état des lieux factuel).
- Risques majeurs identifiés.
- Plan d'action proposé.
- Demandes d'arbitrage (budget, priorisation, ressources).

Cette restitution est **structurante** : c'est elle qui valide la suite du programme. Sa qualité conditionne souvent la prolongation de la mission.

---

## Phase 4 - Run de la mission (au-delà)

### Pratiques recommandées

- **Versionning systématique** : tout livrable est daté et versionné.
- **Single source of truth** : un seul espace partagé (SharePoint, Confluence) pour tous les documents.
- **Pas de surprise** : les blocages remontent immédiatement au sponsor, pas attendu au point mensuel.
- **Transfert de compétences** : le consultant n'est pas là pour rester. Documenter, former, faire faire.
- **Indépendance** : ne jamais dépendre d'un seul interlocuteur côté client (risque si départ).

### Signaux d'alerte

- Sponsor exécutif absent des comités → escalade urgente.
- Refus d'accès à certains documents ou personnes → cadrage à reprendre.
- Décisions reportées de mois en mois → repointer sur le contrat et les engagements.
- Demandes croissantes hors scope → avenant ou redéfinition formelle.
- Changement de RSSI ou DSI en cours de mission → reprise du cadrage avec le nouveau.

---

## Phase 5 - Clôture et transfert (fin de mission)

### Étape 5.1 - Livrables de clôture

- Rapport final consolidé.
- Documentation à jour (PSSI, SoA, registre risques, procédures).
- Plan d'action restant à exécuter (avec dates et owners).
- Indicateurs de suivi en mode "run".
- RETEX de mission (côté client et côté consultant).

### Étape 5.2 - Réunion de clôture

- Présentation des résultats vs objectifs initiaux.
- Présentation du plan post-mission.
- Recueil du feedback client.
- Identification d'éventuelles suites (audit annuel, certification, accompagnement run).

### Étape 5.3 - Continuité

Proposer un format de continuité adapté :
- Maintien d'un mandat de RSSI à temps partagé.
- Audit annuel.
- Coaching ponctuel du RSSI interne.
- Veille réglementaire trimestrielle.
- Accompagnement spot (incident, audit externe).

---

## Outils et templates à mobiliser

| Étape | Document |
|---|---|
| Découverte | Note de découverte + entretiens |
| Cadrage | Matrice RACI (`templates/matrice-raci-grc.md`) |
| Diagnostic ISO | Gap analysis (`scripts/gap_analysis_iso27001.py`) |
| Diagnostic NIST | Maturité (`scripts/scoring_maturite_nist_csf.py`) |
| Risques | Registre (`templates/registre-risques.csv`) |
| Politique | PSSI (`templates/politique-securite-si.md`) |
| Plan traitement | (`templates/plan-traitement-risques.md`) |
| RGPD | Registre (`templates/registre-traitements-rgpd.csv`), AIPD (`templates/aipd-dpia.md`) |
| Suivi | Tableau de bord (`templates/tableau-bord-kpi-kri.md`) |
| Audit | Rapport (`templates/rapport-audit-interne.md`) |
| Continuité | PCA/PRA (`templates/plan-continuite-pca.md`) |
| Quantification | FAIR (`scripts/calcul_fair.py`) |

---

## Conseils pour Hermes

1. **Le sponsor exécutif est le facteur de succès numéro 1**. Sans lui, refuser la mission ou la cadrer comme "diagnostic ponctuel" plutôt que programme structurant.
2. **La première restitution conditionne tout**. Y mettre la qualité maximale, faire valider la veille auprès des opérationnels pour éviter les mauvaises surprises.
3. **Ne pas livrer trop vite des "documents génériques"**. Un consultant qui livre une PSSI copiée-collée sans contexte client perd sa crédibilité en 48h.
4. **Documenter les décisions**. Les arbitrages Direction doivent être tracés (qui, quand, quoi). Protège le consultant et clarifie les responsabilités.
5. **Gérer son énergie**. Une mission GRC est marathonienne (6-18 mois). Pas de sprint épuisant en S1-S2 sans avoir évalué l'endurance nécessaire.
6. **Adopter une posture pédagogique avec la Direction**. La majorité des DG n'ont pas un background cyber. Vulgariser, illustrer avec des cas concrets, quantifier les enjeux financiers (FAIR).
7. **Documenter en continu pour le RETEX**. Ce qui marche / ne marche pas chez ce client est de l'or pour les missions suivantes.

---

## Conseils business pour Dow (cibles ESN/MSSP locales)

Pour un consultant junior GRC se positionnant sur des comptes type AVA6, Inforsud, ESN Aveyron-Toulouse :

1. **Vendre par le FAIRE, pas par les certifications**. Démontrer la capacité à livrer un gap analysis, un registre, une AIPD opérationnelle - pas réciter la norme.
2. **PoC court avant signature**. Proposer une analyse gratuite ou à coût symbolique (2-3 jours) pour démontrer la valeur. Conversion : 30-40% sur les bons profils.
3. **Outillage = différenciation**. Arriver avec des scripts (gap analysis, FAIR), templates et automatisations crée un effet "wow" qui sort du discours.
4. **Cibler les PME 50-250 personnes éligibles NIS2 entité importante**. Elles ont l'obligation, peu de ressources internes, mais un budget mobilisable.
5. **Référencer des cas concrets**. Stage Meet Voice + projets perso = portfolio. Mettre en avant les livrables (pas les certifications en cours).
6. **Tarification** : pour un junior expérimenté en consulting GRC, viser 600-800 €/jour en sous-traitance ESN, 350-450 €/jour brut en interne ESN. Au-delà : assumer un statut indépendant après 2-3 ans de track record.
