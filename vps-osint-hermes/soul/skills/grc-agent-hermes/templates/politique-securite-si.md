# Politique de Sécurité du Système d'Information (PSSI)

**Référence** : PSSI-[NomOrga]-v[X.Y]
**Date d'approbation** : [JJ/MM/AAAA]
**Approuvée par** : [Direction Générale / Comité Exécutif]
**Prochaine revue** : [JJ/MM/AAAA]
**Owner** : [RSSI / CISO]
**Classification** : Interne

---

## 1. Engagement de la Direction

La Direction de [Nom de l'organisation] reconnaît que l'information est un actif essentiel et que sa sécurité conditionne la continuité de nos activités, la confiance de nos clients, partenaires et collaborateurs, ainsi que le respect de nos obligations légales et réglementaires.

À ce titre, la Direction :
- **Établit, approuve et soutient** la présente Politique de Sécurité du Système d'Information
- **Alloue les ressources nécessaires** (humaines, techniques, financières) à sa mise en œuvre
- **S'engage à amélioration continue** du Système de Management de la Sécurité de l'Information (SMSI)
- **Communique** l'importance de la sécurité à l'ensemble du personnel et parties prenantes
- **Tient les dirigeants pour responsables** de la mise en œuvre dans leur périmètre (conforme NIS2 art. 20 si applicable)

## 2. Objet et périmètre

### 2.1 Objet
La présente PSSI définit le cadre de référence en matière de sécurité de l'information pour [Nom de l'organisation]. Elle constitue le document fondateur du SMSI et la référence à laquelle se rattachent toutes les politiques, procédures et standards de sécurité dérivés.

### 2.2 Périmètre
Cette politique s'applique à :
- L'ensemble des entités, sites et filiales : [à préciser]
- L'ensemble du personnel : salariés, intérimaires, stagiaires, alternants, consultants
- Les prestataires et fournisseurs ayant accès aux systèmes d'information
- Tous les actifs informationnels : données, applications, systèmes, infrastructures, locaux

### 2.3 Hors périmètre
[Le cas échéant, préciser explicitement les exclusions]

## 3. Référentiels et conformité

La présente PSSI s'appuie sur :
- **ISO/IEC 27001:2022** — Système de Management de la Sécurité de l'Information
- **ISO/IEC 27002:2022** — Code de bonnes pratiques
- **NIST Cybersecurity Framework 2.0**
- Le **RGPD** (Règlement UE 2016/679)
- La **directive NIS2** (UE 2022/2555) — *si entité concernée*
- Le **règlement DORA** (UE 2022/2554) — *si entité concernée*
- Les exigences contractuelles applicables

## 4. Principes fondamentaux

### 4.1 Triade CIA — Confidentialité, Intégrité, Disponibilité
Toute information est protégée selon trois propriétés indissociables :
- **Confidentialité** : accessible uniquement aux personnes autorisées
- **Intégrité** : exacte et complète
- **Disponibilité** : accessible quand nécessaire aux personnes autorisées

### 4.2 Approche par les risques
La sécurité est pilotée par une analyse des risques régulière (méthodologie EBIOS Risk Manager ou ISO 27005). Les mesures déployées sont proportionnées aux enjeux et au niveau de risque accepté.

### 4.3 Principe du moindre privilège
Chaque utilisateur et système ne dispose que des droits strictement nécessaires à l'exécution de ses missions.

### 4.4 Défense en profondeur
La sécurité repose sur la superposition de mesures organisationnelles, techniques et physiques. Aucune mesure unique ne constitue à elle seule une protection suffisante.

### 4.5 Sécurité dès la conception (Security by Design)
La sécurité est intégrée dès les phases amont des projets et systèmes, et non en superposition après coup.

### 4.6 Conformité légale et réglementaire
Le respect des lois et règlements applicables est une exigence absolue, non négociable.

## 5. Organisation et rôles

### 5.1 Comité de Pilotage Sécurité
Présidé par [Direction Générale / DSI], comprend [RSSI, DPO, Risk Manager, représentants métiers]. Se réunit a minima trimestriellement.

Missions :
- Valider les orientations stratégiques
- Arbitrer les risques majeurs
- Valider les investissements sécurité significatifs
- Suivre les indicateurs

### 5.2 Responsable de la Sécurité des Systèmes d'Information (RSSI)
- Élabore et fait évoluer la PSSI
- Coordonne la mise en œuvre des mesures
- Pilote l'analyse des risques
- Supervise les contrôles et audits internes
- Anime la sensibilisation
- Coordonne la réponse aux incidents

### 5.3 Délégué à la Protection des Données (DPO)
- Veille à la conformité RGPD
- Tient le registre des traitements
- Conseille sur les AIPD
- Point de contact CNIL et personnes concernées

### 5.4 DSI / Production
- Met en œuvre les mesures techniques
- Assure la disponibilité et la fiabilité des systèmes
- Applique les politiques d'administration

### 5.5 Propriétaires d'actifs
Chaque actif (application, base de données, processus) a un propriétaire métier nommément désigné, responsable de :
- La classification de l'actif
- La définition des règles d'accès
- L'arbitrage des risques résiduels

### 5.6 Utilisateurs
Tout utilisateur :
- Lit, signe et respecte la Charte d'Utilisation des Systèmes d'Information
- Signale immédiatement tout incident ou suspicion d'incident
- Suit les formations et sensibilisations obligatoires

## 6. Domaines de la sécurité (référence Annexe A ISO 27001:2022)

### 6.1 Contrôles organisationnels
- Politiques documentées, approuvées, communiquées, révisées
- Inventaire et classification des actifs informationnels
- Gestion des accès selon le moindre privilège
- Sécurité dans les relations fournisseurs (clauses contractuelles, audits)
- Gestion des incidents avec notification dans les délais légaux (CNIL, ANSSI selon cas)
- Continuité d'activité testée annuellement
- Veille réglementaire et conformité

### 6.2 Sécurité des ressources humaines
- Vérifications avant embauche pour postes sensibles
- Clauses de confidentialité dans les contrats
- Programme de sensibilisation annuel obligatoire
- Procédures formelles de départ
- Régime disciplinaire en cas de manquement

### 6.3 Sécurité physique
- Périmètres de sécurité, contrôle d'accès aux locaux
- Protection des équipements (UPS, climatisation, surveillance)
- Procédure d'effacement sécurisé des supports

### 6.4 Sécurité technologique
- Authentification forte (MFA) pour tous les accès distants et privilégiés
- Chiffrement des données sensibles au repos et en transit
- Gestion des vulnérabilités avec SLA de patch selon criticité
- Journalisation et surveillance 24/7
- Sauvegardes régulières et testées
- Sécurité du développement (SDLC, SAST, DAST, revue de code)
- Sécurité du cloud (politique cloud, classification SaaS)

## 7. Gestion des risques

### 7.1 Méthodologie
[EBIOS Risk Manager / ISO 27005 / méthode interne]

### 7.2 Critères d'acceptation des risques
Niveau de risque tolérable défini par la Direction :
- Risques **faibles** : acceptés par le propriétaire de l'actif
- Risques **modérés** : revus par le RSSI et le propriétaire métier
- Risques **élevés** : décision du Comité de Pilotage Sécurité
- Risques **critiques** : décision de la Direction Générale

### 7.3 Fréquence
- Revue complète : annuelle
- Mise à jour : à chaque changement significatif

## 8. Gestion des incidents

### 8.1 Définition
Tout événement non planifié pouvant porter atteinte à la confidentialité, intégrité ou disponibilité des informations ou des systèmes.

### 8.2 Signalement
Tout incident ou suspicion doit être signalé immédiatement via [canal de signalement défini].

### 8.3 Notification réglementaire
- **CNIL** : sous 72h si violation de données personnelles susceptible d'engendrer un risque
- **ANSSI / CSIRT national** : sous 24h pour incident significatif (si soumis NIS2)
- **Autorité financière** : sous 4h (si soumis DORA)

### 8.4 Cycle
Identification → Confinement → Éradication → Restauration → Retour d'expérience formalisé.

## 9. Continuité d'activité

L'organisation maintient un Plan de Continuité d'Activité (PCA) et un Plan de Reprise d'Activité (PRA) :
- Mis à jour annuellement
- Testés au moins une fois par an
- Incluant scénarios cyber (notamment ransomware)
- Intégrant la gestion de crise (cellule de crise, communication)

## 10. Conformité et contrôle

### 10.1 Conformité légale
Veille réglementaire continue. Mise à jour des dispositifs selon les évolutions législatives.

### 10.2 Audits
- **Audits internes** : annuels minimum, couvrant tout le périmètre par cycle de 3 ans
- **Audits externes** : selon exigences clients, certification, réglementation
- **Revue de Direction** : annuelle minimum

### 10.3 Sanctions
Tout manquement à la PSSI ou aux politiques dérivées expose le contrevenant à des sanctions définies dans le règlement intérieur, sans préjudice des poursuites légales applicables.

## 11. Documentation associée

| Document | Référence |
|----------|-----------|
| Charte d'utilisation des SI | CHARTE-[orga]-v[X] |
| Politique de gestion des accès | POL-ACCES-v[X] |
| Politique de classification | POL-CLASS-v[X] |
| Politique cryptographique | POL-CRYPTO-v[X] |
| Politique cloud | POL-CLOUD-v[X] |
| Plan de gestion des incidents | PLAN-IR-v[X] |
| Plan de continuité d'activité | PCA-v[X] |
| Politique fournisseurs | POL-FOURN-v[X] |
| Registre des traitements RGPD | REG-RGPD-v[X] |
| Déclaration d'applicabilité (SoA) | SOA-v[X] |

## 12. Revue et amélioration

Cette PSSI est :
- **Revue annuellement** par le Comité de Pilotage Sécurité
- **Mise à jour** en cas de changement majeur (évolution business, réglementaire, technologique)
- **Communiquée** à l'ensemble des parties prenantes après chaque révision

---

## Annexes

### Annexe 1 — Glossaire
[Définir les termes clés : SMSI, RSSI, DPO, OIV/OSE, CNIL, ANSSI, etc.]

### Annexe 2 — Historique des versions

| Version | Date | Auteur | Modifications |
|---------|------|--------|---------------|
| 1.0 | [date] | [RSSI] | Création |
| 1.1 | [date] | [RSSI] | Mise à jour [...] |

### Annexe 3 — Signatures

**Approbation Direction Générale**
Nom : ___________________________ Date : ___________ Signature : _______________

**RSSI**
Nom : ___________________________ Date : ___________ Signature : _______________

**DPO** (si applicable)
Nom : ___________________________ Date : ___________ Signature : _______________
