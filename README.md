# 📚 Projet de Groupe 4 : Application Web Interactive d'Analyse de Performance Étudiante

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![DuckDB](https://img.shields.io/badge/duckdb-latest-yellow.svg)](https://duckdb.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🎯 Objectif du Projet

Ce projet développe une **application web interactive** utilisant **Streamlit** pour l'interface utilisateur et **DuckDB** pour la gestion des données. L'application permet aux utilisateurs de :

- 📁 Téléverser des fichiers CSV contenant des données de performance étudiante
- 🗄️ Stocker et interroger ces données avec DuckDB
- 📊 Visualiser 4 indicateurs clés de performance (KPI) distincts
- 🔍 Filtrer dynamiquement les résultats par genre, score, éducation parentale, et heures d'étude
- 📈 Explorer des visualisations interactives et des insights approfondis

## 📂 Datasets Utilisés

Ce projet analyse deux datasets complémentaires sur la performance étudiante :

### Dataset 1 : Student Habits vs Academic Performance
**Source:** [Kaggle - Student Habits vs Academic Performance](https://www.kaggle.com/datasets/jayaantanaath/student-habits-vs-academic-performance)

**Colonnes principales:**
- `student_id`, `age`, `gender`
- `study_hours_per_day`, `social_media_hours`, `netflix_hours`
- `attendance_percentage`, `sleep_hours`, `diet_quality`
- `exercise_frequency`, `parental_education_level`
- `mental_health_rating`, `extracurricular_participation`
- `exam_score` (variable cible)

**Taille:** ~500 enregistrements

### Dataset 2 : Student Performance Factors
**Source:** [Kaggle - Student Performance Factors](https://www.kaggle.com/datasets/lainguyn123/student-performance-factors)

**Colonnes principales:**
- `Hours_Studied`, `Attendance`, `Parental_Involvement`
- `Access_to_Resources`, `Extracurricular_Activities`
- `Sleep_Hours`, `Previous_Scores`, `Motivation_Level`
- `Internet_Access`, `Tutoring_Sessions`, `Family_Income`
- `Teacher_Quality`, `School_Type`, `Peer_Influence`
- `Physical_Activity`, `Learning_Disabilities`
- `Parental_Education_Level`, `Distance_from_Home`, `Gender`
- `Exam_Score` (variable cible)

**Taille:** ~6,000+ enregistrements

## 🚀 Installation et Exécution

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git

### Installation

1. **Clonez ce dépôt:**
   ```bash
   git clone https://github.com/DnastyGroup/Projet-de-Groupe-4-Cr-ez-une-Application-Web-Interactive-avec-Git-Streamlit-et-DuckDB.git
   cd Projet-de-Groupe-4-Cr-ez-une-Application-Web-Interactive-avec-Git-Streamlit-et-DuckDB
   ```

2. **Créez un environnement virtuel (recommandé):**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Installez les dépendances:**
   ```bash
   pip install -r requirements.txt
   ```

### Exécution

Lancez l'application Streamlit:
```bash
streamlit run app.py
```

L'application sera automatiquement ouverte dans votre navigateur à l'adresse **http://localhost:8501**

## 📊 Fonctionnalités Principales

### 1️⃣ Interface de Téléversement de Fichiers
- Téléversement simple via drag & drop ou sélection de fichier
- Support des fichiers CSV
- Détection automatique du type de dataset
- Prévisualisation des données avec statistiques de base

### 2️⃣ Intégration DuckDB
- Base de données en mémoire pour des performances optimales
- Requêtes SQL optimisées pour l'analyse de données
- Gestion efficace de datasets volumineux
- Transactions sécurisées

**Exemples de requêtes SQL utilisées:**
```sql
-- Calcul du score moyen filtré
SELECT AVG(exam_score) FROM student_data
WHERE gender IN ('Male', 'Female')
AND exam_score BETWEEN 0 AND 100;

-- Analyse par tranche de présence
SELECT
    CASE
        WHEN attendance_percentage < 60 THEN '< 60%'
        WHEN attendance_percentage < 70 THEN '60-70%'
        ELSE '90-100%'
    END as attendance_range,
    AVG(exam_score) as avg_score
FROM student_data
GROUP BY attendance_range;
```

### 3️⃣ Quatre KPIs Distincts

| KPI | Description | Calcul |
|-----|-------------|--------|
| 🎯 **Score Moyen d'Examen** | Performance académique moyenne | `AVG(exam_score)` |
| ✅ **Taux de Réussite** | Pourcentage d'étudiants avec score ≥ 70 | `COUNT(score >= 70) / COUNT(*) * 100` |
| 📚 **Heures d'Étude Moyennes** | Temps moyen consacré aux études | `AVG(study_hours)` |
| 👥 **Taux de Présence Moyen** | Assiduité moyenne des étudiants | `AVG(attendance_percentage)` |

### 4️⃣ Quatre Visualisations Interactives

#### Visualisation 1: Distribution des Scores d'Examen
- **Type:** Histogramme
- **Objectif:** Comprendre la répartition des performances
- **Insights:** Identification des pics de performance et de la normalité de distribution

#### Visualisation 2: Heures d'Étude vs Score
- **Type:** Scatter plot avec ligne de tendance
- **Objectif:** Analyser la corrélation entre temps d'étude et réussite
- **Insights:** Validation de l'impact positif du temps d'étude

#### Visualisation 3: Performance par Genre
- **Type:** Bar chart
- **Objectif:** Comparer les performances entre genres
- **Insights:** Analyse des disparités de performance

#### Visualisation 4: Impact de la Présence sur les Scores
- **Type:** Bar chart groupé
- **Objectif:** Mesurer l'effet de l'assiduité
- **Insights:** Corrélation entre présence et réussite académique

### 5️⃣ Filtres Dynamiques

| Filtre | Type | Description |
|--------|------|-------------|
| **Genre** | Multi-sélection | Filtrer par Male/Female/Other |
| **Plage de Scores** | Slider | Sélection de la plage de scores (0-100) |
| **Éducation Parentale** | Multi-sélection | High School/Bachelor/Master/Postgraduate |
| **Heures d'Étude** | Slider | Filtrage selon le temps d'étude |

### 6️⃣ Fonctionnalités Additionnelles

- **📊 Analyse de Corrélation:** Coefficient de corrélation entre heures d'étude et score
- **🏆 Top 10 Étudiants:** Classement des meilleurs performers
- **💾 Export de Données:** Téléchargement des données filtrées en CSV
- **📈 Insights Automatiques:** Interprétation intelligente des corrélations

## 🏗️ Structure du Projet

```
Projet-de-Groupe-4/
│
├── Dataset/                          # Datasets CSV
│   ├── student_habits_performance.csv
│   └── StudentPerformanceFactors.csv
│
├── app.py                            # Application Streamlit principale
├── requirements.txt                  # Dépendances Python
├── README.md                         # Documentation
│
└── __pycache__/                      # Fichiers Python compilés
```

## 🧪 Phase de Tests et Assurance Qualité (Salimi Mazrag Amina)
J'ai assuré la stabilité et la fiabilité de l'application via une approche de "stress testing" :

- **Tests Logiques Automatisés :** Création du script `test_logic.py` pour valider les calculs de KPIs via DuckDB.
- **Gestion des Erreurs Critiques :** 
    - Implémentation d'une détection préventive des fichiers de 0 octet (`uploaded_file.size`).
    - Capture spécifique de l'exception `pd.errors.EmptyDataError` pour éviter les crashs de l'interface lors du chargement de fichiers corrompus.
- **Validation de Structure :** Vérification dynamique de l'intégrité de la structure CSV avant tout traitement DuckDB.
- **Amélioration UX :** Ajout d'infobulles explicatives sur les KPIs et messages d'erreur clairs en cas de mauvais format de fichier.
- **Workflow Git :** Gestion complète via une branche dédiée (`feature/tests-y-mejoras`) et Pull Requests.


## 📦 Dépendances

```txt
streamlit>=1.28.0          # Framework web interactif
pandas>=2.0.0              # Manipulation de données
duckdb>=0.9.0              # Base de données analytique
plotly>=5.17.0             # Visualisations interactives
numpy>=1.24.0              # Calculs numériques
statsmodels>=0.14.0        # Analyses statistiques et trendlines
```

## 👥 Répartition des Tâches (Équipe de 4)

| Membre | Responsabilité | Tâches Principales |
|--------|----------------|-------------------|
| **Membre 1** | Interface Streamlit | • Configuration de la page<br>• Interface de téléversement<br>• Layout et organisation |
| **Yassine Kamali** | Intégration DuckDB | • Connexion à DuckDB<br>• Création de tables<br>• Requêtes SQL optimisées |
| **Membre 3** | Visualisations & KPIs | • 4 graphiques interactifs<br>• Calcul des KPIs<br>• Design des visualisations |
| **Membre 4** | Filtres & Documentation | • Système de filtres dynamiques<br>• Tests fonctionnels<br>• Documentation (README) |
| **SALIMI MAZRAG AMINA** | Tests & Qualité | • Script de tests automatisés (test_logic.py) <br> • Validation des données et gestion d'erreurs <br> • Amélioration UX et documentation |

## 🧪 Guide d'Utilisation

### Étape 1: Téléverser un Fichier
1. Cliquez sur "Browse files" dans la sidebar
2. Sélectionnez un fichier CSV (student_habits_performance.csv ou StudentPerformanceFactors.csv)
3. Les données sont automatiquement chargées et analysées

### Étape 2: Explorer les KPIs
- Consultez les 4 indicateurs principaux en haut de page
- Comparez avec les valeurs globales (delta)

### Étape 3: Appliquer des Filtres
1. Utilisez la sidebar pour sélectionner vos critères
2. Les visualisations se mettent à jour en temps réel
3. Le compteur d'étudiants filtrés s'affiche en bas de la sidebar

### Étape 4: Analyser les Visualisations
- Explorez les 4 graphiques interactifs
- Survolez les points pour voir les détails
- Zoomez et déplacez-vous dans les graphiques

### Étape 5: Exporter les Données
1. Ouvrez l'expander "Voir les Données Filtrées Complètes"
2. Cliquez sur "Télécharger les données filtrées (CSV)"
3. Le fichier est sauvegardé avec un timestamp

## 🔍 Exemples de Cas d'Usage

### Cas 1: Identifier les Facteurs de Réussite
**Objectif:** Comprendre quels facteurs influencent le plus la réussite académique

**Démarche:**
1. Téléverser le dataset Student Performance Factors
2. Observer la corrélation entre heures d'étude et score
3. Analyser l'impact de la présence sur les performances
4. Comparer les résultats par niveau d'éducation parentale

**Insight Attendu:** Les étudiants avec >5h d'étude/jour et >80% de présence ont un score moyen supérieur de 15 points

### Cas 2: Analyse des Disparités de Genre
**Objectif:** Évaluer s'il existe des différences de performance entre genres

**Démarche:**
1. Utiliser le filtre "Genre" pour sélectionner alternativement Male/Female
2. Comparer les KPIs entre les deux groupes
3. Observer la visualisation "Performance par Genre"

**Insight Attendu:** Identification de potentielles disparités nécessitant des actions correctives

### Cas 3: Optimisation des Heures d'Étude
**Objectif:** Déterminer le nombre optimal d'heures d'étude

**Démarche:**
1. Observer le scatter plot "Heures d'Étude vs Score"
2. Identifier le point d'inflexion où plus d'heures n'améliore plus significativement le score
3. Analyser la ligne de tendance

**Insight Attendu:** Le rendement marginal des heures d'étude diminue après 6-7h/jour

## 🛠️ Technologies Utilisées

| Technologie | Version | Utilisation |
|-------------|---------|-------------|
| **Python** | 3.8+ | Langage principal |
| **Streamlit** | 1.28+ | Framework web interactif |
| **DuckDB** | 0.9+ | Base de données analytique |
| **Pandas** | 2.0+ | Manipulation de données |
| **Plotly** | 5.17+ | Visualisations interactives |
| **NumPy** | 1.24+ | Calculs numériques |

## 📈 Métriques de Qualité du Code

- ✅ Code modulaire et réutilisable
- ✅ Gestion d'erreurs avec try/except
- ✅ Interface utilisateur intuitive
- ✅ Performance optimisée avec DuckDB
- ✅ Documentation inline complète
- ✅ Compatibilité multi-datasets

## 🤝 Contribution

Pour contribuer à ce projet:

1. Fork le repository
2. Créez une branche pour votre feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 Licence

Ce projet est développé dans le cadre d'un projet académique MBA ESG.


---

**Développé par l'Équipe Groupe 4 - MBA ESG**

