import streamlit as st
import pandas as pd
import duckdb
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Analyse de Performance Étudiante",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: rgba(128, 128, 128, 0.1);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }

    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .stMetric {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("📚 Application d'Analyse de Performance Étudiante")
st.markdown("### Interactive Web App avec Streamlit et DuckDB")
st.markdown("---")

# Sidebar for file upload
with st.sidebar:
    st.header("📁 Téléversement de Fichier")
    uploaded_file = st.file_uploader(
        "Téléversez un fichier CSV contenant des données étudiantes",
        type="csv",
        help="Formats acceptés: student_habits_performance.csv ou StudentPerformanceFactors.csv"
    )

    st.markdown("---")
    st.info("""
    **Datasets supportés:**
    - Student Habits vs Performance
    - Student Performance Factors
    """)

if uploaded_file is not None:
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)
# DATA VALIDATION IMPROVEMENT (Member 4 - Testing & Quality)
        if df.empty:
            st.error("⚠️ The uploaded file is empty. Please upload a valid CSV dataset.")
            st.stop()
        
        # Check for required columns based on dataset detection
        required_cols = [score_col, gender_col, study_col]
        if not all(col in df.columns for col in required_cols):
            st.error("⚠️ The CSV structure is incorrect. Missing required data columns.")
            st.stop()
            
        # Store original column names
        original_columns = df.columns.tolist()

        # Determine dataset type and standardize column names
        if 'student_id' in df.columns:
            dataset_type = "habits"
            st.sidebar.success("✅ Dataset: Student Habits vs Performance")

            # Standardize column names for consistency
            score_col = 'exam_score'
            gender_col = 'gender'
            study_col = 'study_hours_per_day'
            attendance_col = 'attendance_percentage'
            sleep_col = 'sleep_hours'
            parent_edu_col = 'parental_education_level'

        elif 'Hours_Studied' in df.columns:
            dataset_type = "factors"
            st.sidebar.success("✅ Dataset: Student Performance Factors")

            # Standardize column names
            score_col = 'Exam_Score'
            gender_col = 'Gender'
            study_col = 'Hours_Studied'
            attendance_col = 'Attendance'
            sleep_col = 'Sleep_Hours'
            parent_edu_col = 'Parental_Education_Level'
        else:
            st.error("⚠️ Format de fichier non reconnu. Veuillez téléverser un dataset valide.")
            st.stop()

        # Display basic info
        st.success(f"✅ Fichier chargé avec succès: **{uploaded_file.name}**")

        # Display data preview in expander
        with st.expander("👀 Aperçu des données (10 premières lignes)"):
            st.dataframe(df.head(10), use_container_width=True)

        # Display dataset statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 Nombre de lignes", f"{len(df):,}")
        with col2:
            st.metric("📋 Nombre de colonnes", len(df.columns))
        with col3:
            st.metric("🎓 Score moyen", f"{df[score_col].mean():.2f}")
        with col4:
            st.metric("📈 Score max", f"{df[score_col].max():.2f}")

        st.markdown("---")

        # Connect to DuckDB (in-memory database)
        con = duckdb.connect(database=':memory:', read_only=False)

        # Create table in DuckDB
        con.execute("CREATE OR REPLACE TABLE student_data AS SELECT * FROM df")

        # === FILTERS SECTION ===
        st.sidebar.header("🔍 Filtres Dynamiques")

        # Gender filter
        if gender_col in df.columns:
            genders = df[gender_col].dropna().unique().tolist()
            selected_genders = st.sidebar.multiselect(
                "Genre",
                options=genders,
                default=genders,
                help="Filtrer par genre des étudiants"
            )
            gender_filter = f"{gender_col} IN ({','.join(repr(g) for g in selected_genders)})" if selected_genders else "1=1"
        else:
            gender_filter = "1=1"

        # Score range filter
        min_score = float(df[score_col].min())
        max_score = float(df[score_col].max())
        score_range = st.sidebar.slider(
            "Plage de scores (Exam Score)",
            min_value=min_score,
            max_value=max_score,
            value=(min_score, max_score),
            help="Filtrer par plage de scores d'examen"
        )
        score_filter = f"{score_col} BETWEEN {score_range[0]} AND {score_range[1]}"

        # Parental Education filter (if available)
        if parent_edu_col in df.columns:
            parent_edu_levels = df[parent_edu_col].dropna().unique().tolist()
            selected_parent_edu = st.sidebar.multiselect(
                "Niveau d'éducation des parents",
                options=parent_edu_levels,
                default=parent_edu_levels,
                help="Filtrer par niveau d'éducation parentale"
            )
            parent_edu_filter = f"{parent_edu_col} IN ({','.join(repr(p) for p in selected_parent_edu)})" if selected_parent_edu else "1=1"
        else:
            parent_edu_filter = "1=1"

        # Study hours filter
        if study_col in df.columns:
            min_study = float(df[study_col].min())
            max_study = float(df[study_col].max())
            study_range = st.sidebar.slider(
                "Heures d'étude",
                min_value=min_study,
                max_value=max_study,
                value=(min_study, max_study),
                help="Filtrer par heures d'étude"
            )
            study_filter = f"{study_col} BETWEEN {study_range[0]} AND {study_range[1]}"
        else:
            study_filter = "1=1"

        # Combine all filters
        full_filter = f"WHERE {gender_filter} AND {score_filter} AND {parent_edu_filter} AND {study_filter}"

        # Get filtered data count
        filtered_count = con.execute(f"SELECT COUNT(*) FROM student_data {full_filter}").fetchone()[0]
        st.sidebar.markdown(f"**Étudiants filtrés:** {filtered_count:,} / {len(df):,}")

        # === KPIs SECTION ===
        st.header("📊 Indicateurs Clés de Performance (KPIs)")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            # KPI 1: Average Exam Score
            avg_score = con.execute(f"SELECT AVG({score_col}) FROM student_data {full_filter}").fetchone()[0]
            st.metric(
                "🎯 Score Moyen d'Examen",
                f"{avg_score:.2f}",
                delta=f"{avg_score - df[score_col].mean():.2f} vs global",
                help="Score moyen d'examen des étudiants filtrés"
            )

        with col2:
            # KPI 2: Success Rate (Score >= 70)
            total_students = con.execute(f"SELECT COUNT(*) FROM student_data {full_filter}").fetchone()[0]
            success_count = con.execute(f"SELECT COUNT(*) FROM student_data {full_filter} AND {score_col} >= 70").fetchone()[0]
            success_rate = (success_count / total_students * 100) if total_students > 0 else 0
            st.metric(
                "✅ Taux de Réussite",
                f"{success_rate:.1f}%",
                help="Pourcentage d'étudiants avec un score >= 70"
            )

        with col3:
            # KPI 3: Average Study Hours
            avg_study = con.execute(f"SELECT AVG({study_col}) FROM student_data {full_filter}").fetchone()[0]
            st.metric(
                "📚 Heures d'Étude Moyennes",
                f"{avg_study:.2f}h",
                help="Nombre moyen d'heures d'étude"
            )

        with col4:
            # KPI 4: Average Attendance
            avg_attendance = con.execute(f"SELECT AVG({attendance_col}) FROM student_data {full_filter}").fetchone()[0]
            st.metric(
                "👥 Taux de Présence Moyen",
                f"{avg_attendance:.1f}%",
                help="Taux de présence moyen des étudiants"
            )

        st.markdown("---")

        # === VISUALIZATIONS SECTION ===
        st.header("📈 Visualisations des Données")

        # Visualization 1: Score Distribution
        st.subheader("1️⃣ Distribution des Scores d'Examen")
        scores_data = con.execute(f"SELECT {score_col} FROM student_data {full_filter}").fetchdf()
        fig1 = px.histogram(
            scores_data,
            x=score_col,
            nbins=30,
            title="Distribution des Scores",
            labels={score_col: "Score d'Examen", "count": "Nombre d'Étudiants"},
            color_discrete_sequence=['#1f77b4']
        )
        fig1.update_layout(
            showlegend=False,
            xaxis_title="Score d'Examen",
            yaxis_title="Nombre d'Étudiants",
            hovermode='x'
        )
        st.plotly_chart(fig1, use_container_width=True)

        # Two columns for side-by-side visualizations
        col1, col2 = st.columns(2)

        with col1:
            # Visualization 2: Study Hours vs Exam Score
            st.subheader("2️⃣ Heures d'Étude vs Score")
            study_score_data = con.execute(
                f"SELECT {study_col}, {score_col} FROM student_data {full_filter}"
            ).fetchdf()
            fig2 = px.scatter(
                study_score_data,
                x=study_col,
                y=score_col,
                title="Corrélation: Heures d'Étude et Score",
                trendline="ols",
                labels={study_col: "Heures d'Étude", score_col: "Score d'Examen"},
                color=score_col,
                color_continuous_scale='Viridis'
            )
            fig2.update_layout(
                xaxis_title="Heures d'Étude",
                yaxis_title="Score d'Examen"
            )
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            # Visualization 3: Performance by Gender
            st.subheader("3️⃣ Performance par Genre")
            gender_perf = con.execute(
                f"""SELECT {gender_col},
                           AVG({score_col}) as avg_score,
                           COUNT(*) as count
                    FROM student_data {full_filter}
                    GROUP BY {gender_col}"""
            ).fetchdf()
            fig3 = px.bar(
                gender_perf,
                x=gender_col,
                y='avg_score',
                title="Score Moyen par Genre",
                labels={gender_col: "Genre", 'avg_score': "Score Moyen"},
                color='avg_score',
                color_continuous_scale='Blues',
                text='avg_score'
            )
            fig3.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig3.update_layout(
                xaxis_title="Genre",
                yaxis_title="Score Moyen"
            )
            st.plotly_chart(fig3, use_container_width=True)

        # Visualization 4: Attendance vs Score
        st.subheader("4️⃣ Taux de Présence vs Score d'Examen")

        # Create attendance bins for better visualization
        attendance_score_query = f"""
            SELECT
                CASE
                    WHEN {attendance_col} < 60 THEN '< 60%'
                    WHEN {attendance_col} < 70 THEN '60-70%'
                    WHEN {attendance_col} < 80 THEN '70-80%'
                    WHEN {attendance_col} < 90 THEN '80-90%'
                    ELSE '90-100%'
                END as attendance_range,
                AVG({score_col}) as avg_score,
                COUNT(*) as count
            FROM student_data {full_filter}
            GROUP BY attendance_range
            ORDER BY attendance_range
        """
        attendance_data = con.execute(attendance_score_query).fetchdf()

        fig4 = px.bar(
            attendance_data,
            x='attendance_range',
            y='avg_score',
            title="Impact de la Présence sur les Scores",
            labels={'attendance_range': "Plage de Présence", 'avg_score': "Score Moyen"},
            color='avg_score',
            color_continuous_scale='Greens',
            text='avg_score'
        )
        fig4.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig4.update_layout(
            xaxis_title="Plage de Taux de Présence",
            yaxis_title="Score Moyen",
            xaxis={'categoryorder': 'array', 'categoryarray': ['< 60%', '60-70%', '70-80%', '80-90%', '90-100%']}
        )
        st.plotly_chart(fig4, use_container_width=True)

        # === ADDITIONAL INSIGHTS ===
        st.markdown("---")
        st.header("🔍 Insights Supplémentaires")

        col1, col2 = st.columns(2)

        with col1:
            # Top performers
            st.subheader("🏆 Top 10 Étudiants")
            if dataset_type == "habits":
                top_students = con.execute(
                    f"""SELECT student_id, {score_col}, {study_col}, {attendance_col}
                        FROM student_data {full_filter}
                        ORDER BY {score_col} DESC
                        LIMIT 10"""
                ).fetchdf()
                st.dataframe(top_students, use_container_width=True)
            else:
                top_students = con.execute(
                    f"""SELECT {score_col}, {study_col}, {attendance_col}
                        FROM student_data {full_filter}
                        ORDER BY {score_col} DESC
                        LIMIT 10"""
                ).fetchdf()
                st.dataframe(top_students, use_container_width=True)

        with col2:
            # Correlation analysis
            st.subheader("📊 Corrélation: Étude et Score")
            correlation_data = con.execute(
                f"SELECT {study_col}, {score_col} FROM student_data {full_filter}"
            ).fetchdf()

            if len(correlation_data) > 1:
                correlation = correlation_data[study_col].corr(correlation_data[score_col])
                st.metric(
                    "Coefficient de Corrélation",
                    f"{correlation:.3f}",
                    help="Corrélation entre heures d'étude et score d'examen (-1 à 1)"
                )

                if correlation > 0.5:
                    st.success("✅ Forte corrélation positive: Plus d'étude = Meilleur score")
                elif correlation > 0.3:
                    st.info("ℹ️ Corrélation modérée positive")
                else:
                    st.warning("⚠️ Corrélation faible")

        # === DETAILED DATA TABLE ===
        st.markdown("---")
        with st.expander("📋 Voir les Données Filtrées Complètes"):
            filtered_data = con.execute(f"SELECT * FROM student_data {full_filter}").fetchdf()
            st.dataframe(filtered_data, use_container_width=True)

            # Download button
            csv = filtered_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="💾 Télécharger les données filtrées (CSV)",
                data=csv,
                file_name=f"student_data_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

        # Close DuckDB connection
        con.close()

    except Exception as e:
        st.error(f"❌ Erreur lors du traitement du fichier: {str(e)}")
        st.exception(e)

else:
    # Welcome screen when no file is uploaded
    st.markdown("""
    ## 👋 Bienvenue!

    Cette application vous permet d'analyser les données de performance étudiante de manière interactive.

    ### 🎯 Fonctionnalités:
    - 📁 **Téléversement de fichiers CSV**
    - 🗄️ **Stockage et requêtes avec DuckDB**
    - 📊 **4 KPIs principaux** pour suivre la performance
    - 📈 **Visualisations interactives** avec filtres dynamiques
    - 🔍 **Filtres avancés** par genre, score, éducation parentale, etc.

    ### 🚀 Pour commencer:
    1. Utilisez le panneau latéral pour téléverser un fichier CSV
    2. Les données seront automatiquement analysées
    3. Explorez les KPIs et visualisations
    4. Utilisez les filtres pour affiner votre analyse

    ### 📂 Datasets supportés:
    - **Student Habits vs Academic Performance**: Analyse l'impact des habitudes étudiantes
    - **Student Performance Factors**: Analyse multifactorielle de la performance

    ---
    """)

    # Display example data structure
    st.info("""
    **💡 Astuce:** Vous pouvez téléverser les fichiers CSV situés dans le dossier `Dataset/`:
    - `student_habits_performance.csv`
    - `StudentPerformanceFactors.csv`
    """)
