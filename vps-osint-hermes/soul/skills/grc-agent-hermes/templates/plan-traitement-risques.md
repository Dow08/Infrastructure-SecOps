# Plan de Traitement des Risques

**Référence** : PTR-[NomOrga]-v[X.Y]
**Périmètre SMSI** : [à définir]
**Date** : [JJ/MM/AAAA]
**Owner** : RSSI
**Approbation** : Comité de Pilotage Sécurité du [date]

---

## 1. Objet

Le présent document décrit le plan de traitement des risques de sécurité de l'information identifiés lors de l'analyse de risques [méthodologie : EBIOS RM / ISO 27005] menée le [date]. Il constitue le livrable obligatoire de la clause 6.1.3 de l'ISO 27001:2022.

## 2. Critères d'acceptation du risque

| Niveau | Score | Décision |
|--------|------:|----------|
| Faible | 1-3 | Acceptable — surveillance |
| Modéré | 4-6 | Traitement souhaité — sous 12 mois |
| Élevé | 8-9 | Traitement obligatoire — sous 6 mois |
| Critique | 12-16 | Traitement immédiat — sous 3 mois |

## 3. Stratégie de traitement (par risque)

| Stratégie | Quand l'utiliser |
|-----------|------------------|
| **Réduire** | Risque inacceptable mais traitable techniquement/organisationnellement |
| **Accepter** | Coût des mesures > impact estimé, ou risque résiduel acceptable |
| **Transférer** | Assurance cyber, sous-traitance contractualisée |
| **Refuser** | Arrêt de l'activité génératrice du risque |

## 4. Tableau de traitement

| ID | Risque | Niveau initial | Stratégie | Mesures | Mapping ISO Annexe A | Owner | Échéance | Coût estimé | Niveau résiduel cible | Indicateur de suivi |
|----|--------|----------------|-----------|---------|----------------------|-------|----------|-------------|----------------------|---------------------|
| R-001 | Compromission compte privilégié via phishing | Critique (12) | Réduire | Déploiement PAM + MFA conditionnel renforcé + phishing simulations trimestrielles | A.8.2, A.8.5, A.6.3 | RSSI | 2026-06-30 | 85 k€ | Modéré (6) | % comptes priv. sous PAM, taux clic phishing test |
| R-002 | Ransomware via piece jointe | Critique (12) | Réduire | EDR + sandbox email + sauvegardes immutables 3-2-1-1-0 | A.8.7, A.8.13, A.8.16 | DSI | 2026-09-30 | 120 k€ | Modéré (6) | Couverture EDR, RPO/RTO réels, MTTD/MTTR |
| R-003 | Exfiltration via SaaS shadow IT | Critique (12) | Réduire | Cartographie SaaS + CASB + politique d'usage cloud | A.5.23, A.8.12, A.5.10 | RSSI + DSI | 2026-12-31 | 60 k€ | Modéré (6) | Nb SaaS approuvés, alertes DLP/CASB |
| R-004 | Notification incident RGPD > 72h | Modéré (6) | Réduire | Procédure formelle + exercice annuel | A.5.24-26 | DPO | 2026-04-30 | 5 k€ | Faible (2) | Temps réel de notification lors exercice |
| R-005 | Indispo datacenter > 24h | Modéré (4) | Réduire | Tests PRA biannuels + amélioration RTO | A.5.30, A.8.14 | DSI | 2026-06-30 | 30 k€ | Faible (2) | Résultat tests PRA, RTO mesuré |
| R-006 | Défaillance prestataire critique | Élevé (8) | Réduire + Transférer | Stratégie de sortie formalisée + clauses NIS2/DORA + audit annuel + assurance cyber | A.5.19-22 | Achats + RSSI | 2026-12-31 | 25 k€ + 15 k€/an | Modéré (6) | % prestataires critiques avec stratégie de sortie |
| R-007 | Zero-day application web exposée | Élevé (8) | Réduire | WAF avancé + bug bounty + SLA patch 7j critiques | A.8.8, A.8.20 | DevSecOps | 2026-09-30 | 70 k€ | Modéré (6) | Temps moyen de patch CVSS critique |
| R-008 | Sanction CNIL traitement sans base légale | Modéré (6) | Réduire | Audit base légale + refonte CMP + DPIA marketing | RGPD art. 6, 35 | DPO + Marketing | 2026-06-30 | 20 k€ | Faible (2) | Taux de conformité cookies (audit annuel) |
| R-009 | Compromission supply chain logicielle | Élevé (8) | Réduire | SCA (Trivy/Snyk) + SBOM + signature artefacts | A.8.28, A.5.21 | DevSecOps | 2026-09-30 | 40 k€ | Modéré (6) | % builds avec SBOM, nb CVE critiques laissés |
| R-010 | Perte connaissance départ admin clé | Modéré (9) | Réduire | Plan de succession + documentation + binôme | A.6.5, A.5.37 | DSI + RH | 2026-06-30 | 10 k€ (interne) | Faible (4) | % runbooks à jour, % postes critiques avec backup |

## 5. Budget global

| Rubrique | Investissement (CAPEX) | Récurrent (OPEX annuel) |
|----------|------------------------:|-------------------------:|
| Outillage technique | 285 k€ | 65 k€ |
| Conseil et accompagnement | 75 k€ | - |
| Formation et sensibilisation | 20 k€ | 15 k€ |
| Assurance cyber | - | 15 k€ |
| **Total** | **380 k€** | **95 k€** |

## 6. Calendrier de mise en œuvre

```
2026 Q1 : Quick wins — Procédures incident, sensibilisation, audit base légale RGPD
2026 Q2 : Sécurité postes — EDR, MFA renforcé, plan succession
2026 Q3 : Sécurité applicative — WAF avancé, SCA, SAST, bug bounty
2026 Q4 : Cloud et tiers — CASB, cartographie SaaS, clauses fournisseurs
2027 Q1 : Audit interne, premier bilan, ajustements
```

## 7. Risques résiduels acceptés par la Direction

Après mise en œuvre du plan, les risques résiduels suivants restent acceptés par la Direction (validation Comité de Pilotage du [date]) :

| ID | Description risque résiduel | Niveau résiduel | Justification d'acceptation | Date revue |
|----|-----------------------------|----------------:|-----------------------------|------------|
| R-001 | Phishing résiduel sur compte non privilégié | Modéré (6) | Coût d'éradication totale disproportionné, sensibilisation continue suffit | 2027-01-15 |
| R-009 | CVE supply chain découvertes après build | Modéré (6) | Veille active + monitoring runtime acceptable | 2027-01-15 |

## 8. Indicateurs de pilotage (KPI / KRI)

À reporter mensuellement au Comité de Pilotage Sécurité :

| Indicateur | Cible | Seuil d'alerte |
|------------|------:|---------------:|
| % comptes privilégiés sous PAM | 100% | < 90% |
| % couverture EDR | 100% | < 95% |
| Taux clic phishing simulation | < 5% | > 8% |
| Temps moyen de patch CVSS critique | < 7j | > 14j |
| % runbooks postes critiques à jour | 100% | < 80% |
| Temps réel notification RGPD (exercice) | < 48h | > 60h |
| Nb d'incidents de sécurité confirmés | Tendance | + 30% MoM |
| Score maturité NIST CSF | Cible définie | < niveau année N-1 |

## 9. Revue et mise à jour

- **Revue trimestrielle** : avancement du plan, ajustements opérationnels
- **Revue annuelle complète** : analyse de risques refaite, nouveau plan
- **Revue exceptionnelle** : changement majeur (M&A, nouveau site, nouveau cadre réglementaire)

---

**Validation Comité de Pilotage Sécurité**

Date : _______________

| Rôle | Nom | Signature |
|------|-----|-----------|
| Direction Générale | | |
| RSSI | | |
| DSI | | |
| DPO | | |
| Risk Manager | | |
