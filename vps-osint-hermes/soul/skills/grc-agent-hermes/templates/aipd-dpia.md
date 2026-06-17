# Analyse d'Impact relative à la Protection des Données (AIPD / DPIA)

**Référentiel** : RGPD article 35, méthode CNIL PIA, ISO/IEC 29134
**Document** : [À remplir]
**Version** : 1.0
**Date** : [JJ/MM/AAAA]
**Responsable de traitement** : [Nom organisation]
**DPO** : [Nom + contact]

---

## 1. Pourquoi cette AIPD est obligatoire

L'AIPD est obligatoire lorsque le traitement est **susceptible d'engendrer un risque élevé** pour les droits et libertés des personnes (art. 35 RGPD).

Cocher les critères CNIL qui s'appliquent (2 critères = AIPD obligatoire) :

- [ ] Évaluation/scoring (profilage)
- [ ] Décision automatique avec effet juridique
- [ ] Surveillance systématique
- [ ] Données sensibles ou à caractère hautement personnel
- [ ] Données à grande échelle
- [ ] Croisement de jeux de données
- [ ] Personnes vulnérables (mineurs, salariés, patients...)
- [ ] Usage innovant ou nouveau (IA, biométrie, IoT...)
- [ ] Exclusion d'un droit/contrat/service

**Conclusion** : AIPD [obligatoire / recommandée / non requise]

---

## 2. Description du traitement

### 2.1 Finalités

Décrire précisément l'objectif. Pas de "amélioration de la qualité de service" flou.
Exemple : *Détecter automatiquement les transactions bancaires frauduleuses pour bloquer le paiement avant débit.*

### 2.2 Périmètre

| Élément | Description |
|---|---|
| Catégories de personnes | Clients, prospects, salariés, mineurs... |
| Catégories de données | Identité, contact, financier, localisation, biométrie... |
| Données sensibles (art. 9) | Oui/Non - Lesquelles |
| Volume estimé | Nombre de personnes concernées |
| Durée du traitement | Permanent / ponctuel |
| Zones géographiques | UE, hors UE (préciser pays) |

### 2.3 Acteurs

| Rôle | Identité | Responsabilité |
|---|---|---|
| Responsable de traitement | [Org] | Décide finalités/moyens |
| Sous-traitants | [Prestataires] | Voir contrat art. 28 |
| Destinataires | [Liste] | Internes / externes |
| DPO | [Nom] | Conseil et contrôle |

### 2.4 Données et flux

Schéma du flux de données : collecte → stockage → traitement → transmission → archivage → suppression.
Joindre un diagramme.

### 2.5 Supports et durées de conservation

| Donnée | Support | Localisation | Durée active | Durée archivage | Justification |
|---|---|---|---|---|---|
| Ex : Email client | CRM Salesforce | UE (Irlande) | 3 ans après dernier contact | 2 ans intermédiaire | Prescription commerciale |

---

## 3. Conformité aux principes fondamentaux

### 3.1 Finalité (art. 5.1.b)

Finalité **déterminée, explicite, légitime**. Pas de réutilisation incompatible.

- Description : ...
- Mesures pour empêcher détournement : ...

### 3.2 Base légale (art. 6)

| Finalité | Base légale art. 6 | Justification |
|---|---|---|
| Ex : Gestion contrat | Contrat (6.1.b) | Exécution mesures précontractuelles |
| Ex : Prospection email | Intérêt légitime (6.1.f) | Test mise en balance fait |
| Ex : Cookies analytics | Consentement (6.1.a) | Bandeau CNIL |

Pour données sensibles : exception art. 9.2 applicable = ...

### 3.3 Minimisation (art. 5.1.c)

Seules les données **strictement nécessaires** sont collectées.
- Données collectées : ...
- Données écartées (et pourquoi) : ...

### 3.4 Qualité / exactitude (art. 5.1.d)

Mesures pour garantir l'exactitude : auto-déclaration utilisateur, vérification source officielle, mise à jour périodique...

### 3.5 Durées de conservation (art. 5.1.e)

Durées définies + suppression / anonymisation automatique en fin de cycle. Voir tableau §2.5.

### 3.6 Information des personnes (art. 12-14)

- Mention informative au moment de la collecte : Oui / Non
- Politique de confidentialité publiée : URL
- Information complète : identité RT, finalités, base légale, destinataires, durées, droits, recours CNIL, transferts...

### 3.7 Exercice des droits (art. 15-22)

| Droit | Procédure d'exercice | Délai cible |
|---|---|---|
| Accès | Formulaire web + DPO | 1 mois |
| Rectification | Espace client | 1 mois |
| Effacement | DPO + ticket interne | 1 mois |
| Limitation | DPO | 1 mois |
| Portabilité | Export JSON | 1 mois |
| Opposition | Lien désabonnement + DPO | 1 mois |
| Décision automatique | DPO | 1 mois |

### 3.8 Sous-traitance (art. 28)

| Sous-traitant | Service | Contrat art. 28 signé | Pays | Garanties |
|---|---|---|---|---|
| Ex : AWS | Hébergement | Oui | UE (Francfort) | SCC + chiffrement |

### 3.9 Transferts hors UE (art. 44-49)

| Destinataire | Pays | Outil de transfert | Mesures complémentaires |
|---|---|---|---|
| Ex : Sous-traitant US | États-Unis | SCC + DPF | Chiffrement E2E, audit annuel |

---

## 4. Mesures de sécurité (art. 32)

### 4.1 Mesures techniques

| Mesure | Mise en œuvre | Référence |
|---|---|---|
| Chiffrement au repos | AES-256 sur base | ISO A.8.24 |
| Chiffrement en transit | TLS 1.3 | ISO A.8.24 |
| Authentification | MFA pour accès admin | ISO A.5.17, A.8.5 |
| Contrôle d'accès | RBAC + moindre privilège | ISO A.5.15, A.8.3 |
| Journalisation | Logs centralisés 1 an | ISO A.8.15 |
| Sauvegarde | 3-2-1, chiffrée, testée | ISO A.8.13 |
| Anonymisation/pseudonymisation | Hash + sel sur identifiants | RGPD art. 32.1.a |
| Protection contre malware | EDR sur endpoints | ISO A.8.7 |
| Gestion vulnérabilités | Scan mensuel + patch SLA | ISO A.8.8 |
| DLP | Surveillance flux sortants | ISO A.8.12 |

### 4.2 Mesures organisationnelles

| Mesure | Mise en œuvre |
|---|---|
| Politique de sécurité | PSSI v2.0 signée Direction |
| Sensibilisation | Formation annuelle + phishing trimestriel |
| Engagement de confidentialité | Clause contrat + charte signée |
| Habilitations | Revue trimestrielle accès |
| Gestion incidents | Procédure notification 72h CNIL |
| Audit | Audit interne annuel + externe bi-annuel |

---

## 5. Analyse des risques pour les personnes

### 5.1 Méthode

Méthode CNIL : pour chaque événement redouté, évaluer la **gravité** (impact sur la personne) et la **vraisemblance** (probabilité de survenance).

### 5.2 Identification des sources de risques

| Source | Type | Exemple |
|---|---|---|
| Source humaine interne | Malveillant / accidentel | Admin curieux, erreur saisie |
| Source humaine externe | Malveillant / accidentel | Hacker, ingénierie sociale |
| Source non humaine | - | Panne, incendie, virus |

### 5.3 Événements redoutés

| Événement | Impact sur personne | Gravité (1-4) | Vraisemblance (1-4) | Niveau de risque |
|---|---|---|---|---|
| Accès illégitime aux données | Vol identité, atteinte vie privée, discrimination | 3 | 2 | Élevé |
| Modification non désirée | Décision erronée, préjudice | 2 | 2 | Modéré |
| Disparition de données | Impossibilité exercer droits, perte historique | 2 | 1 | Faible |

Échelle gravité : 1=Négligeable, 2=Limité, 3=Important, 4=Maximal
Échelle vraisemblance : 1=Négligeable, 2=Limité, 3=Important, 4=Maximal

### 5.4 Scénarios de menaces

Pour chaque événement redouté, décrire 1-3 scénarios concrets.

**Exemple - Accès illégitime** :
- Scénario 1 : Vol identifiants admin via phishing → exfiltration base clients
- Scénario 2 : Sous-traitant non conforme → fuite données via journaux non protégés
- Scénario 3 : Salarié quittant l'entreprise emporte fichier clients

### 5.5 Traitement des risques

| Risque | Mesure existante | Mesure complémentaire | Risque résiduel | Acceptable ? |
|---|---|---|---|---|
| Accès illégitime | MFA + RBAC | DLP + UEBA | Modéré | Oui |
| Modification | Logs + 4-yeux | Workflow approbation | Faible | Oui |
| Disparition | Backup 3-2-1 | Test restauration trimestriel | Faible | Oui |

---

## 6. Validation et avis

### 6.1 Avis du DPO

**[Favorable / Réservé / Défavorable]**
Commentaires : ...
Recommandations : ...
Signature DPO + date :

### 6.2 Avis des personnes concernées (si pertinent)

Consultation effectuée : Oui / Non
Modalité : enquête, comité utilisateurs, représentants du personnel...
Résultats : ...

### 6.3 Décision du responsable de traitement

**[Traitement autorisé / Conditionné aux mesures complémentaires / Non autorisé]**

Si risque élevé résiduel persiste malgré les mesures → **consultation préalable CNIL obligatoire** (art. 36).

Signature Direction + date :

---

## 7. Plan d'action et suivi

| Action | Owner | Échéance | Statut | Indicateur |
|---|---|---|---|---|
| Déploiement DLP | RSSI | Q3 2026 | En cours | % flux couverts |
| Formation équipe | DPO | T+30j | Planifié | % personnel formé |
| Audit sous-traitant | Achats | T+60j | À lancer | Rapport audit |

**Revue de l'AIPD** : à chaque modification substantielle du traitement, et au minimum tous les 3 ans.

---

## Annexes

- Annexe 1 : Schéma de flux des données
- Annexe 2 : Contrat sous-traitant art. 28
- Annexe 3 : Politique de sécurité applicable
- Annexe 4 : Mention d'information aux personnes
- Annexe 5 : Procédure d'exercice des droits
