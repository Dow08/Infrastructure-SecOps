# Tableau de bord GRC - KPI et KRI

**Objectif** : Piloter la performance et l'exposition au risque cyber. Donner à la Direction une vision agrégée, actionnable, mensuelle/trimestrielle.
**Référentiels** : ISO 27001 clause 9.1, ISO 27004 (mesures), NIST CSF 2.0 Govern, DORA art. 13
**Version** : 1.0
**Fréquence de revue** : mensuelle (équipe), trimestrielle (Direction)
**Owner** : RSSI

---

## Différence KPI vs KRI

- **KPI (Key Performance Indicator)** : mesure la **performance** des contrôles (ce qu'on fait bien).
- **KRI (Key Risk Indicator)** : mesure l'**exposition au risque** (ce qui peut nous arriver).

Un tableau de bord équilibré combine les deux. Les KRI permettent d'anticiper, les KPI de piloter.

---

## 1. KPI - Gouvernance SMSI

| KPI | Description | Cible | Seuil rouge | Fréquence | Source | Owner |
|---|---|---|---|---|---|---|
| Taux de réalisation du plan d'action SMSI | Actions clôturées vs planifiées | ≥ 85% | < 70% | Mensuel | GRC tool | RSSI |
| % politiques à jour (revue < 12 mois) | Politiques internes datées | 100% | < 90% | Trimestriel | GED | RSSI |
| Couverture documentaire SMSI | Documents obligatoires ISO 27001 présents | 100% | < 95% | Trimestriel | Checklist ISO | RSSI |
| Comités SMSI tenus vs planifiés | Gouvernance effective | 100% | < 80% | Trimestriel | Calendrier | DG |
| Décisions de revue de Direction exécutées | Engagement Direction | ≥ 90% | < 70% | Semestriel | PV revue | DG |

---

## 2. KPI - Gestion des risques

| KPI | Description | Cible | Seuil rouge | Fréquence | Source | Owner |
|---|---|---|---|---|---|---|
| % risques avec propriétaire désigné | Pas de risque orphelin | 100% | < 95% | Mensuel | Registre risques | RSSI |
| % risques avec mesures de traitement actives | Pas de risque inertie | ≥ 90% | < 80% | Mensuel | Registre risques | RSSI |
| Délai moyen de mise à jour des risques | Risques pas trop anciens | < 90j | > 180j | Trimestriel | Registre risques | RSSI |
| % risques critiques traités dans le SLA | Réactivité | ≥ 95% | < 80% | Trimestriel | Plan traitement | RSSI |
| Réalisation analyse de risques annuelle | Conformité ISO 27001 | 100% | non fait | Annuel | Rapport EBIOS | RSSI |

---

## 3. KPI - Conformité

| KPI | Description | Cible | Seuil rouge | Fréquence | Source | Owner |
|---|---|---|---|---|---|---|
| Taux de conformité Annexe A ISO 27001 | Contrôles "Implémentés" vs applicables | ≥ 90% | < 80% | Trimestriel | SoA | RSSI |
| % traitements RGPD inscrits au registre | Couverture art. 30 | 100% | < 95% | Trimestriel | Registre RGPD | DPO |
| % contrats fournisseurs avec clauses sécurité | Conformité art. 28 RGPD | ≥ 95% | < 80% | Trimestriel | Outil achats | ACH |
| Délai moyen de notification CNIL (incidents) | Respect 72h | < 72h | > 72h | Par incident | Registre violations | DPO |
| Délai moyen de notification NIS2 | Respect 24h alerte précoce | < 24h | > 24h | Par incident | Procédure crise | RSSI |
| % réponses aux demandes RGPD dans le délai 1 mois | Droits personnes | ≥ 95% | < 90% | Mensuel | Outil DSR | DPO |
| % AIPD réalisées sur traitements à risque | Conformité art. 35 | 100% | < 90% | Trimestriel | Registre AIPD | DPO |

---

## 4. KPI - Sécurité technique

| KPI | Description | Cible | Seuil rouge | Fréquence | Source | Owner |
|---|---|---|---|---|---|---|
| % patchs critiques (CVSS ≥ 9) appliqués sous 30j | Gestion vulnérabilités | ≥ 95% | < 85% | Mensuel | Scanner | DSI |
| % patchs élevés (CVSS 7-8.9) appliqués sous 60j | Gestion vulnérabilités | ≥ 90% | < 75% | Mensuel | Scanner | DSI |
| Vulnérabilités critiques ouvertes > 30j | Stock de risque | 0 | > 5 | Mensuel | Scanner | DSI |
| % postes avec EDR actif | Couverture endpoint | 100% | < 98% | Mensuel | EDR | DSI |
| % comptes avec MFA activée | Authentification forte | ≥ 95% | < 85% | Mensuel | IAM | DSI |
| % comptes privilégiés avec PAM | Comptes à haut risque | 100% | < 95% | Mensuel | PAM | DSI |
| Taux de réussite test de restauration | Sauvegardes fonctionnelles | 100% | < 90% | Trimestriel | Outil backup | DSI |
| RPO mesuré vs objectif | Perte de données potentielle | ≤ objectif | > 2x objectif | Mensuel | Outil backup | DSI |

---

## 5. KPI - Détection et réponse

| KPI | Description | Cible | Seuil rouge | Fréquence | Source | Owner |
|---|---|---|---|---|---|---|
| MTTD (Mean Time To Detect) | Détection menace | < 4h | > 24h | Mensuel | SIEM | SOC |
| MTTR (Mean Time To Respond) incident majeur | Réponse | < 1h | > 4h | Par incident | SIEM/SOAR | SOC |
| MTTC (Mean Time To Contain) | Confinement | < 4h | > 24h | Par incident | SIEM/SOAR | SOC |
| MTTRecover (Mean Time To Recover) | Reprise totale | < 24h | > 72h | Par incident | Logs Ops | DSI |
| % alertes SIEM traitées | Pas d'alertes orphelines | ≥ 95% | < 80% | Mensuel | SIEM | SOC |
| Taux de faux positifs | Qualité détection | < 30% | > 60% | Mensuel | SIEM | SOC |
| Couverture des sources de logs critiques | Visibilité | ≥ 95% | < 80% | Trimestriel | SIEM | SOC |

---

## 6. KPI - Ressources humaines / sensibilisation

| KPI | Description | Cible | Seuil rouge | Fréquence | Source | Owner |
|---|---|---|---|---|---|---|
| % personnel formé annuellement | Couverture | 100% | < 90% | Trimestriel | LMS | RH |
| % nouveaux arrivants formés J+30 | Onboarding | 100% | < 90% | Mensuel | LMS | RH |
| Taux de clic phishing simulé | Vigilance utilisateurs | < 10% | > 20% | Trimestriel | Outil phishing | RSSI |
| Taux de signalement phishing | Comportement positif | ≥ 30% | < 10% | Trimestriel | Outil phishing | RSSI |
| Délai de désactivation comptes au départ | Offboarding | < 24h | > 72h | Mensuel | IAM + RH | DSI |

---

## 7. KPI - Tiers / fournisseurs

| KPI | Description | Cible | Seuil rouge | Fréquence | Source | Owner |
|---|---|---|---|---|---|---|
| % fournisseurs critiques évalués sécurité | Maîtrise tiers | 100% | < 90% | Trimestriel | GRC tool | ACH |
| % fournisseurs critiques audités dans l'année | Surveillance continue | ≥ 80% | < 50% | Annuel | Rapports audit | ACH |
| Incidents fournisseurs significatifs | Propagation risque tiers | 0 | > 2 | Annuel | Registre incidents | RSSI |
| % registre information DORA complet | Conformité art. 28.3 DORA | 100% | < 95% | Trimestriel | Outil DORA | RSSI |

---

## 8. KRI - Indicateurs de risque

| KRI | Description | Seuil vert | Seuil orange | Seuil rouge | Source | Owner |
|---|---|---|---|---|---|---|
| Nombre de tentatives d'intrusion bloquées | Pression menace externe | < baseline | × 2 baseline | × 5 baseline | Pare-feu, WAF | SOC |
| Nombre de vulnérabilités critiques ouvertes | Surface d'attaque exposée | < 5 | 5-15 | > 15 | Scanner | DSI |
| Nombre de comptes privilégiés sans MFA | Risque compromission élevé | 0 | 1-5 | > 5 | IAM | DSI |
| Nombre d'incidents de sécurité du mois | Activité hostile | < baseline | × 2 baseline | × 5 baseline | SIEM | SOC |
| Nombre de fuites de données détectées | Exfiltration | 0 | 1-2 | > 2 | DLP, OSINT | RSSI |
| Volume de données sensibles non chiffrées | Exposition | < 5% | 5-15% | > 15% | DLP, classification | RSSI |
| Délai depuis dernier test PCA | Préparation crise | < 6 mois | 6-12 mois | > 12 mois | Plan tests | RSSI |
| Délai depuis dernier audit interne | Indépendance contrôle | < 12 mois | 12-18 mois | > 18 mois | Programme audit | AUD |
| % shadow IT identifié | Périmètre maîtrisé | < 5% | 5-15% | > 15% | CASB | DSI |
| Stress score équipe sécurité (turnover, absent.) | Capacité opérationnelle | < seuil | mod | élevé | RH | DG |
| Exposition financière FAIR (P90 annuel) | Risque financier cyber | < tolérance | proche tolérance | > tolérance | Quantification FAIR | RSSI/FIN |
| % budget cyber consommé vs prévu | Capacité d'action | 60-100% | 40-60% | < 40% | Comptabilité | DG/RSSI |

---

## 9. Tableau de bord exécutif (1 page CODIR)

À présenter en revue trimestrielle, format synthétique.

| Domaine | Indicateur clé | Cible | Mois M | Tendance | Statut |
|---|---|---|---|---|---|
| Gouvernance | Taux plan d'action SMSI | 85% | 82% | ↑ | 🟢 |
| Risques | Risques critiques résiduels | < 3 | 2 | → | 🟢 |
| Conformité | % SoA ISO conforme | 90% | 87% | ↑ | 🟠 |
| Sécurité | Vulnérabilités critiques | < 5 | 3 | ↓ | 🟢 |
| Détection | MTTD moyen | < 4h | 6h | ↓ | 🟠 |
| RH | Phishing - clic | < 10% | 8% | ↓ | 🟢 |
| Tiers | Fournisseurs critiques évalués | 100% | 92% | ↑ | 🟠 |
| Financier | Budget cyber consommé | 60-100% | 65% | → | 🟢 |
| **Score global de maturité (NIST CSF)** | **Tier 3** | **2.8** | **↑** | **🟠** |
| **Exposition financière (FAIR P90)** | **< 5 M€** | **3.2 M€** | **↓** | **🟢** |

Légende statut :
- 🟢 Vert : conforme à la cible
- 🟠 Orange : écart à surveiller, action en cours
- 🔴 Rouge : alerte, action immédiate

---

## 10. Données et automatisation

### Sources possibles

| Catégorie | Outils types |
|---|---|
| SIEM / SOC | Splunk, Sentinel, Elastic, Wazuh, QRadar |
| EDR | CrowdStrike, SentinelOne, Microsoft Defender |
| Vulnérabilités | Qualys, Tenable, Rapid7, OpenVAS |
| IAM / PAM | Okta, Microsoft Entra ID, CyberArk, Delinea |
| GRC | OneTrust, ServiceNow GRC, Drata, Vanta, AuditBoard |
| DLP / CASB | Symantec, Forcepoint, Netskope, Microsoft Purview |
| Sauvegardes | Veeam, Commvault, Rubrik |
| Tickets | Jira, ServiceNow ITSM |
| Phishing | KnowBe4, Cofense, Mantra |
| Quantification | RiskLens, Resilience |

### Architecture cible

```
[Sources données] → [API/connecteurs] → [Datalake/BI] → [Dashboard]
```

- Préférer les outils GRC qui agrègent nativement.
- À défaut, ETL maison via Python/n8n vers Grafana ou Power BI.
- Automatiser ≥ 70% de la collecte → libère le RSSI pour l'analyse.

### Pièges classiques

- Mesurer ce qui est facile à mesurer plutôt que ce qui est important.
- Trop d'indicateurs → noyade. Garder 15-25 max au niveau opérationnel, 8-12 au niveau Direction.
- Indicateurs déconnectés des objectifs business.
- Données peu fiables = décisions peu fiables. Investir dans la qualité de la donnée avant le reporting.
- Pas de revue régulière des seuils → indicateurs deviennent inutiles avec le temps.

---

## 11. Revue et amélioration des indicateurs

| Activité | Fréquence | Owner |
|---|---|---|
| Revue mensuelle KPI/KRI (équipe sécurité) | Mensuel | RSSI |
| Revue trimestrielle au CODIR | Trimestriel | DG + RSSI |
| Recalibrage seuils (vert/orange/rouge) | Annuel | RSSI |
| Ajout/suppression d'indicateurs | Selon besoin | RSSI |
| Benchmark externe (sectoriel) | Annuel | RSSI |

---

## Annexes

- Annexe A : Définitions détaillées et formules de calcul de chaque indicateur
- Annexe B : Procédures de collecte automatique (API, requêtes)
- Annexe C : Modèles de visualisation (Grafana, Power BI)
- Annexe D : Historique des recalibrages de seuils
