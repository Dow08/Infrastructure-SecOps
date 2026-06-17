# Workflow - Audit ISO 27001 (interne ou pré-certification)

**Objectif** : Conduire un audit ISO 27001:2022 de bout en bout, de la planification à la restitution.
**Durée typique** : 4 à 6 semaines selon la taille du périmètre.
**Référentiels** : ISO 27001:2022 (clause 9.2), ISO 19011:2018 (lignes directrices audit), ISO/IEC 27007.

---

## Quand utiliser ce workflow

- Audit interne annuel obligatoire (clause 9.2 ISO 27001).
- Audit blanc avant certification externe (gap analysis approfondi).
- Audit de surveillance (organisme certificateur, support).
- Audit fournisseur dans le cadre de la chaîne d'approvisionnement.
- Mandat de consultant externe sur la maturité GRC.

---

## Phase 1 - Préparation (Semaine 1)

### Étape 1.1 - Cadrer la mission

**Objectifs** :
- Définir le périmètre exact (entités, sites, processus, systèmes).
- Identifier le commanditaire et la chaîne décisionnelle.
- Convenir du référentiel : ISO 27001:2022 seul, ou + ISO 27017 (Cloud), 27018 (PII Cloud), 27701 (Privacy).
- Fixer les dates clés et le rendu final.

**Output** : Lettre de mission signée, plan d'audit.

**Outils** : `templates/matrice-raci-grc.md` pour clarifier les rôles.

### Étape 1.2 - Collecter la documentation

Documents à demander à l'audité (J-15 avant le terrain) :
- Politique de Sécurité (PSSI),
- Déclaration d'Applicabilité (SoA),
- Plan de traitement des risques,
- Registre des risques,
- Procédures opérationnelles,
- Comptes-rendus des 12 derniers mois du comité SMSI,
- Indicateurs / tableaux de bord,
- Inventaire des actifs,
- Rapport d'audit interne précédent + plan d'action,
- Rapport de revue de Direction.

**Output** : Dossier documentaire complet, premier diagnostic des manques.

### Étape 1.3 - Construire le programme d'audit

Construire un planning détaillé avec :
- Liste des entretiens (qui, quand, durée, sujets),
- Liste des observations physiques (sites, datacenter),
- Liste des échantillons à tester (habilitations, logs, configurations),
- Planning de restitution intermédiaire et finale.

**Output** : Programme d'audit envoyé à l'audité J-7 minimum.

---

## Phase 2 - Exécution (Semaines 2-4)

### Étape 2.1 - Réunion d'ouverture

- Présenter l'équipe d'auditeurs et la méthodologie.
- Confirmer le périmètre, le planning, la confidentialité.
- Rappeler que les constats sont factuels et fondés sur preuves.
- Désigner le point de contact pour la production de preuves.

### Étape 2.2 - Audit des clauses 4 à 10 (système management)

Pour chaque clause, mener un entretien semi-directif avec le responsable + revue documentaire :

| Clause | Personne à rencontrer | Questions clés |
|---|---|---|
| 4 - Contexte | RSSI / Direction | Enjeux, parties intéressées, périmètre |
| 5 - Leadership | Direction | Engagement, ressources, politique |
| 6 - Planification | RSSI | Méthode risques, traitement, objectifs |
| 7 - Support | RSSI + RH | Compétences, sensibilisation, documentation |
| 8 - Fonctionnement | RSSI + DSI | Procédures opérationnelles, changement |
| 9 - Évaluation | RSSI + Audit | KPI, audit interne, revue Direction |
| 10 - Amélioration | RSSI | Non-conformités, actions correctives |

**Méthode** : pour chaque exigence, demander "comment faites-vous concrètement ?" puis "montrez-moi la preuve".

### Étape 2.3 - Audit des contrôles Annexe A

Sur les 93 contrôles, échantillonner intelligemment :
- 100% des contrôles déclarés "Applicables et implémentés" sur le SoA (vérification).
- Focus particulier sur les **11 nouveaux contrôles 2022** (A.5.7, A.5.23, A.5.30, A.7.4, A.8.9 à A.8.12, A.8.16, A.8.23, A.8.28).
- Tests d'efficacité par sondage (pas seulement la conformité documentaire).

Exemples de tests :
- A.5.15 Contrôle d'accès → extraire 10 utilisateurs aléatoires, vérifier que leurs droits correspondent à leur poste.
- A.8.8 Vulnérabilités → demander le dernier rapport de scan + traçage de remédiation.
- A.8.13 Sauvegardes → assister à un test de restauration d'un échantillon.
- A.8.15 Logs → vérifier la couverture des sources critiques et la conservation.
- A.5.30 PCA TIC → demander la date et le rapport du dernier test PRA.

**Outils** : `scripts/gap_analysis_iso27001.py` pour automatiser la consolidation des constats.

### Étape 2.4 - Observations physiques et techniques

- Visite physique des sites sensibles (datacenter, bureaux RH, archives).
- Vérification des badges, alarmes, vidéosurveillance.
- Test "écrans verrouillés" en heure de pointe.
- Vérification "bureau dégagé" en fin de journée.
- Vérification de la gestion des déchets sensibles (papier, supports).

### Étape 2.5 - Documenter chaque constat

Pour **chaque** constat (positif ou négatif) :
- Contrôle ou clause concernée.
- Constat précis et factuel.
- Preuve(s) collectée(s) ou référencée(s).
- Personne(s) rencontrée(s).
- Niveau : Conforme / Observation / Non-conformité mineure / Non-conformité majeure.
- Risque associé.

**Critères ISO 19011** :
- **Non-conformité majeure (NC)** : absence systémique d'une exigence, ou un constat qui remet en cause l'efficacité du SMSI sur un pan entier.
- **Non-conformité mineure (nc)** : écart ponctuel, isolé, traitable rapidement.
- **Observation / Opportunité d'amélioration (OA)** : pas d'écart mais piste de progrès.

---

## Phase 3 - Synthèse et restitution (Semaine 5-6)

### Étape 3.1 - Analyse croisée

- Consolider les constats par clause / contrôle.
- Identifier les causes racines (souvent récurrentes : gouvernance, ressources, gestion changement).
- Calculer les scores par thème.
- Top 5 ou Top 10 des actions prioritaires.

**Outils** : `templates/rapport-audit-interne.md` à remplir au fil de l'eau.

### Étape 3.2 - Rédiger le rapport

Structure type :
1. Synthèse exécutive (1 page CODIR).
2. Périmètre et méthodologie.
3. Évaluation des clauses 4 à 10.
4. Évaluation des contrôles Annexe A.
5. Détail des non-conformités (avec preuve, cause, action recommandée).
6. Observations et opportunités d'amélioration.
7. Bonnes pratiques relevées.
8. Plan d'action consolidé avec échéances.
9. Conclusion et recommandations stratégiques.

**Pièges à éviter** :
- Ne pas mélanger constats et recommandations dans la même phrase.
- Pas de jugement de valeur. Faits + preuves uniquement.
- Pas de copier-coller de la norme ; expliquer **ce que l'auditeur a vu**.
- Pas de "il faudrait" mais "l'exigence X.Y demande Z, le constat est W, l'action corrective recommandée est V".

### Étape 3.3 - Réunion de restitution intermédiaire

Avec l'audité avant la version finale :
- Présenter les constats provisoires.
- Permettre à l'audité de produire des preuves complémentaires sous 5 jours.
- Ajuster le rapport si nouvelle preuve change un constat.

### Étape 3.4 - Réunion de clôture

Devant la Direction :
- Synthèse exécutive.
- Verdict global de conformité.
- Top actions prioritaires.
- Calendrier de plan d'action et de suivi.

---

## Phase 4 - Suivi post-audit (3 à 12 mois)

### Étape 4.1 - Validation du plan d'action

À J+30 du rapport final, valider que l'audité a élaboré un plan d'action :
- Une ligne par non-conformité,
- Owner identifié,
- Échéance réaliste (NC majeures : 90 jours max, mineures : 90-180 jours),
- Indicateur de clôture.

### Étape 4.2 - Suivi périodique

- Point trimestriel de l'avancement.
- Audit de suivi sur les NC majeures à mi-parcours.
- Clôture formelle de chaque NC sur production de preuve d'efficacité (pas juste de l'action menée).

### Étape 4.3 - Audit de suivi (12 mois)

Préparation de l'audit annuel suivant. Vérifier que les actions correctives ont produit des effets durables, et pas seulement temporaires.

---

## Checklist auditeur ISO 27001

À utiliser en mémo-tampon pendant la mission :

- [ ] Lettre de mission signée
- [ ] Périmètre validé par écrit
- [ ] Documentation collectée et analysée avant le terrain
- [ ] Programme d'audit envoyé à J-7
- [ ] Réunion d'ouverture tenue
- [ ] 100% des clauses 4-10 traitées
- [ ] Échantillon Annexe A couvre les 4 thèmes
- [ ] Focus 11 nouveaux contrôles 2022 fait
- [ ] Observations physiques effectuées
- [ ] Au moins 1 test d'efficacité par contrôle critique
- [ ] Chaque constat appuyé par une preuve
- [ ] Top 5 ou Top 10 actions priorisées
- [ ] Rapport produit dans les 10 jours ouvrés post-terrain
- [ ] Restitution intermédiaire + finale tenues
- [ ] Plan d'action validé à J+30

---

## Sortie attendue du workflow

- Rapport d'audit interne complet (modèle `templates/rapport-audit-interne.md`).
- Plan d'action consolidé.
- Synthèse exécutive (CODIR).
- Mise à jour du registre des non-conformités SMSI.
- Données pour la prochaine revue de Direction.

---

## Conseils pour Hermes

1. **Toujours demander la preuve**. Sans preuve, c'est une observation, pas une conformité.
2. **Le SoA ne suffit pas**. Auditer ce qui est dit "implémenté" sur le SoA est un piège : on trouve souvent l'écart en testant l'efficacité réelle.
3. **L'audit n'est pas un contrôle policier**. Posture senior : pédagogique, factuel, force de proposition.
4. **Cibler les bonnes personnes**. Rencontrer le RSSI suffit rarement ; aller voir le terrain (admins, devs, utilisateurs).
5. **Les nouveaux contrôles 2022 sont peu mûrs**. Threat intel, Cloud, DLP, codage sécurisé : c'est là que se concentrent souvent les écarts.
6. **Ne pas oublier les fournisseurs**. La chaîne d'approvisionnement est le maillon faible le plus fréquent en 2026.
