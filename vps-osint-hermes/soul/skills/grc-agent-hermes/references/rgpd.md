# RGPD — Règlement (UE) 2016/679 — Référence opérationnelle

## Pourquoi le RGPD

Applicable depuis le **25 mai 2018**. C'est le cadre référence mondial pour la protection des données personnelles. Toute organisation traitant des données personnelles d'**Européens** est concernée, même hors UE.

En France, l'autorité de contrôle est la **CNIL**.

## Concepts fondamentaux

### Données personnelles
Toute information se rapportant à une personne physique **identifiée ou identifiable**. Inclut :
- Identifiants directs : nom, email, téléphone
- Identifiants indirects : IP, cookie ID, identifiant device
- Données sensibles (art. 9) : santé, opinions politiques, religion, orientation sexuelle, biométrie

### Traitement
Toute opération sur des données personnelles : collecte, enregistrement, stockage, modification, transmission, suppression.

### Acteurs
- **Responsable de traitement** : décide des finalités et moyens
- **Sous-traitant** : traite pour le compte du responsable (cloud, SaaS, prestataire)
- **Personne concernée** : la personne dont les données sont traitées
- **DPO** (Délégué à la Protection des Données) : obligatoire si secteur public, traitement à grande échelle, ou données sensibles

## Les 6 principes (Article 5)

1. **Licéité, loyauté, transparence** — base légale + information claire
2. **Limitation des finalités** — utilisée uniquement pour la finalité annoncée
3. **Minimisation** — collecter uniquement ce qui est nécessaire
4. **Exactitude** — données à jour, mécanisme de correction
5. **Limitation de la conservation** — durée définie et justifiée
6. **Intégrité et confidentialité** — sécurité technique et organisationnelle

Le **principe d'accountability** (responsabilité) — Art. 24 — impose de **démontrer** la conformité, pas juste la déclarer.

## Les 6 bases légales (Article 6)

Tout traitement doit reposer sur **au moins une** :

| Base légale | Quand l'utiliser |
|-------------|------------------|
| Consentement | Marketing, cookies non strictement nécessaires |
| Contrat | Exécution contrat avec la personne |
| Obligation légale | Comptabilité, RH, fiscal |
| Intérêts vitaux | Urgence vitale (santé) |
| Mission d'intérêt public | Administration publique |
| Intérêts légitimes | Sécurité, prévention fraude, B2B prospection limitée |

**Erreur classique** : choisir "consentement" alors que "contrat" ou "intérêts légitimes" s'applique. Ça oblige inutilement à gérer le retrait du consentement.

## Le registre des traitements (Article 30) — OBLIGATOIRE

Obligatoire sauf exception (moins de 250 salariés ET pas de risque élevé ET pas de données sensibles ET pas occasionnel).

En pratique : **toujours en faire un**.

### Contenu minimum (responsable de traitement)
- Identité du responsable + DPO si désigné
- Finalités du traitement
- Catégories de personnes concernées
- Catégories de données
- Catégories de destinataires
- Transferts hors UE (et garanties)
- Durées de conservation
- Description des mesures de sécurité

### Contenu (sous-traitant)
- Identité du sous-traitant + DPO
- Catégories de traitements effectués par client
- Transferts hors UE
- Mesures de sécurité

Format libre : Excel, base de données, outil dédié. La CNIL fournit un modèle.

## L'AIPD / DPIA (Article 35)

**Analyse d'Impact relative à la Protection des Données** = obligatoire si le traitement présente un **risque élevé** pour les droits et libertés.

### Quand est-elle obligatoire ?

Liste CNIL (R2-1.0 du 22/11/2019) — cas typiques :
- Évaluation systématique et grande échelle de personnes (scoring, profilage)
- Traitement à grande échelle de données sensibles
- Surveillance systématique d'une zone publique
- Croisement de jeux de données importants
- Données concernant personnes vulnérables (enfants, salariés, patients)
- Usage de nouvelles technologies (IA, biométrie, IoT)
- Transferts hors UE de données sensibles à grande échelle
- Empêcher accès à un service ou contrat

### Contenu d'une AIPD
1. Description systématique du traitement
2. Évaluation de la nécessité et proportionnalité
3. Identification et évaluation des risques pour les droits et libertés
4. Mesures pour atténuer ces risques

**Si après AIPD le risque résiduel reste élevé** → consultation préalable obligatoire de la CNIL (art. 36).

## Droits des personnes (Articles 12-22)

| Droit | Délai max | Particularités |
|-------|-----------|----------------|
| Information (art. 13-14) | À la collecte | Mention CNIL obligatoire |
| Accès (art. 15) | 1 mois | Extensible 2 mois si complexe |
| Rectification (art. 16) | 1 mois | |
| Effacement (art. 17) | 1 mois | "Droit à l'oubli" — sauf obligation légale |
| Limitation (art. 18) | 1 mois | |
| Portabilité (art. 20) | 1 mois | Format structuré, lisible machine |
| Opposition (art. 21) | 1 mois | Si intérêts légitimes/marketing |
| Décision automatisée (art. 22) | Variable | Profilage à grande échelle |

Toute organisation doit avoir un **processus documenté** pour traiter ces demandes.

## Sécurité (Article 32)

Mesures techniques et organisationnelles "appropriées" :
- Pseudonymisation et chiffrement
- Confidentialité, intégrité, disponibilité, résilience
- Capacité à rétablir disponibilité en cas d'incident
- Procédure de test et évaluation régulière

ISO 27001 + Annexe A couvre largement ces exigences.

## Notification de violation (Articles 33-34)

### À la CNIL (art. 33)
Dans **72h** après en avoir pris connaissance, si la violation est susceptible d'engendrer un risque pour les droits/libertés.

Contenu : nature, catégories et nombre approximatif de personnes affectées, conséquences probables, mesures prises.

### Aux personnes concernées (art. 34)
Sans délai injustifié si risque **élevé** pour les droits/libertés. Sauf si mesures techniques (chiffrement) rendent les données inintelligibles.

**Toujours documenter** toute violation, même non notifiable, dans un registre interne.

## Transferts hors UE (Articles 44-49)

Possibles si :
- Pays "adéquat" (décision Commission UE) — ex. Royaume-Uni, Suisse, Canada (partiel)
- Clauses Contractuelles Types (SCC) — modèles UE 2021
- Règles d'Entreprise Contraignantes (BCR)
- Certifications, codes de conduite (rares)
- Dérogations exceptionnelles (art. 49)

**Cas USA** : après l'invalidation du Privacy Shield (Schrems II 2020), le nouveau **Data Privacy Framework** (2023) est de nouveau valide, mais sous contestation. Surveiller la jurisprudence.

## Sanctions (Article 83)

Deux paliers :
| Type d'infraction | Sanction maximale |
|-------------------|-------------------|
| Manquements généraux (art. 83.4) | **10M€ ou 2% CA mondial** |
| Manquements majeurs (art. 83.5) — droits personnes, principes, transferts | **20M€ ou 4% CA mondial** |

(Le plus élevé des deux.)

En France, la CNIL peut aussi :
- Mises en demeure publiques
- Astreintes journalières
- Suspension du traitement

## Cookies et traceurs (ePrivacy + RGPD)

Régime spécifique français (CNIL — lignes directrices 2020) :
- Bannière conforme : refus aussi facile qu'accepter
- Cookies de mesure d'audience anonyme exemptés sous conditions
- Durée maximale du consentement : 13 mois (ou plus court justifié)
- Cookies tiers (publicité) toujours soumis à consentement explicite

## DPO — Obligation et rôle (Articles 37-39)

### Quand est-il obligatoire ?
- Autorité ou organisme public
- Suivi régulier et systématique à grande échelle (réseaux sociaux, traçage)
- Traitement à grande échelle de données sensibles (santé, biométrie)

### Indépendance
Le DPO :
- N'est **pas** soumis à instructions sur l'exercice de ses missions
- Rapporte directement au plus haut niveau hiérarchique
- Ne peut être sanctionné pour l'exercice de ses missions
- Doit pouvoir refuser des conflits d'intérêts (typiquement : DSI = NON, RH = NON, RSSI = à discuter)

## Pièges à éviter / signaler

1. **Pas de registre** alors que >250 salariés — sanction directe
2. **Base légale "consentement" non vérifiable** — exigé qu'il soit "libre, spécifique, éclairé, univoque"
3. **Pas de DPIA** sur un traitement à risque élevé — sanction si incident
4. **Sous-traitants sans contrat art. 28** — toute relation avec un SaaS/cloud doit être contractualisée
5. **Transferts hors UE non encadrés** — particulièrement vers USA (jurisprudence Schrems II)
6. **Conservation indéfinie** — toute donnée doit avoir une durée de vie
7. **Information opaque** — la mention RGPD doit être claire, accessible, en français

## Documents minimums RGPD pour une PME

1. Registre des traitements (responsable + sous-traitant si applicable)
2. Politique de confidentialité publique
3. Mentions d'information au moment de la collecte
4. Procédure de gestion des demandes de droits
5. Procédure de gestion des violations de données
6. Contrats avec sous-traitants (clauses art. 28)
7. AIPD pour traitements à risque
8. Cookies banner + politique cookies
9. Charte RGPD interne (sensibilisation)

## Mapping RGPD / ISO 27001

- RGPD = quoi protéger (données personnelles, droits)
- ISO 27001 = comment protéger (système de management)
- ISO 27701 = extension RGPD spécifique (PIMS - Privacy Information Management System)

L'ISO 27701 est la **norme de référence pour démontrer la conformité RGPD**. Elle étend ISO 27001 avec des contrôles spécifiques.
