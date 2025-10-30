"""
code de la page

"""

from tools import *

def affiche():
    # --- Titre principal ---
    st.title("🚀 Conclusion du projet")
    st.markdown("""
    ### Synthèse, apprentissages et perspectives
    ---
    """)

    # --- Introduction dynamique ---
    st.info("💡 *Ce projet nous a permis de mettre à profit notre formation en Data Science sur un sujet concret et populaire : l'immobilier.*")

    st.write("Chaque membre de l’équipe a contribué à construire un modèle de prédiction de la valeur foncière en Gironde, en explorant de nombreuses données open source et en relevant de vrais défis techniques et organisationnels.")

    st.markdown("---")

    # --- Timeline du projet ---
    st.subheader("🧭 Les grandes étapes du projet")
    timeline = {
        "Exploration des données": 40,
        "Nettoyage et préparation": 20,
        "Modélisation": 30,
        "Mise en production": 5,
        "Présentation finale": 5
    }
    fig = px.bar(
        x=list(timeline.keys()),
        y=list(timeline.values()),
        title="Répartition du temps par phase (%)",
        labels={"x": "Phase", "y": "Temps (en %)"}
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Sections avec expanders ---
    with st.expander("📘 Bilan du projet", expanded=True):
        st.markdown("""
        Ce projet nous a permis de **mettre en pratique nos compétences** sur un cas d’usage concret et accessible à tous : le marché immobilier.

        🔹 **Recherche et manipulation de données open data** : un travail conséquent de sélection, de nettoyage et de compréhension.  
        🔹 **Vision multidimensionnelle** du problème : variables géographiques, économiques, sociales, techniques.  
        🔹 **Conscience des limites** : fraîcheur des données, absence de certaines caractéristiques clés (état du bien, subjectivité des acheteurs, etc.).  
        🔹 **Dimension humaine** : la valeur d’un bien reste partiellement subjective, au-delà des modèles statistiques.
        """)

    with st.expander("⚙️ Difficultés rencontrées"):
        st.markdown("""
        Plusieurs difficultés techniques et organisationnelles ont marqué ce projet :
        - 📊 **Choix et recherche des données** : absence de cadre initial, nécessitant beaucoup d’exploration.  
        - 🧩 **Gestion des compétences** : des décalages dans la formation ont parfois ralenti le rythme collectif.  
        - 🔁 **Arrêt des itérations** : difficile de trouver le bon équilibre entre performance et délais.  
        - 🧪 **Usage partiel d’outils MLOps (MLflow)** : suivi des expériences artisanal, comparaisons manuelles.  
        - 👀 **Absence de revue de code systématique** : difficultés à relire ou reprendre certains scripts.  
        - ⚖️ **Compromis MLOps / performance** : choix d’un modèle plus léger, réaliste pour un déploiement.
        """)

    with st.expander("🤝 Gestion du travail"):
        st.markdown("""
        La **collaboration** a permis la réalisation du projet :

        👥 **Répartition des rôles :**
        - Chaque membre a fait de la **recherche de données** open source pour déterminer les sources de données intéressantes.
        - L'**analyse des différentes sources de données** a été partagée entre les différents membres selon le temps disponible poour chacun.  
        - Pour la **modélisation**, chaque membre est parti de ses propres hypothèses (pour éviter de s'influencer et avoir des idées diversifiées)
        - **Rédaction du rapport** à trois mains en fonction des parties traitées par chacun des membres.

        🧭 **Organisation du travail :**
        - Outils communs utilisés : GitHub, Slack, Google Drive + Outils utilisés individuellement
        - Organisation : réunions hebdomadaires, liste de tâches  
        - Difficultés : disponibilité inégale, apprentissage progressif des modules de formation  

        🧠 **Enseignements tirés :**
        - Importance de la **coordination technique et humaine** dans un projet Data Science. 
        - Nécessité de **documenter et partager les expérimentations**.  
        - Mise en place nécessaire de **revues de code systématiques".
        - Recours à **MLFlow**.
        """)

    with st.expander("🌱 Futures évolutions et perspectives"):
        st.markdown("""
        Les perspectives du projet ouvrent de nombreuses voies d’amélioration :

        🔹 **1. Enrichir les données** : intégrer davantage de variables (cadastre, environnement, accessibilité, etc.)  
        🔹 **2. Ajouter des données en temps réel** : via **web scraping** de sites d’agences pour suivre les prix de marché actuels.  
        🔹 **3. Étendre le périmètre** : tester le modèle sur d’autres départements ou régions.  
        🔹 **4. Diversifier les types de biens** : terrains, locaux commerciaux, industriels.  
        🔹 **5. Explorer d’autres approches** : modèles neuronaux, deep learning, ou modèles hiérarchiques spatio-temporels.  

        En résumé, ce projet a posé les **fondations d’un modèle robuste et évolutif**, qui pourrait devenir un outil complet d’aide à la décision pour les acteurs du marché immobilier.
        """)

    # --- Animation finale ---
    st.markdown("---")
    with st.container():
        st.subheader("🎓 En conclusion...")
        text = "Un projet exigeant, formateur et techniquement et humainement enrichissant."
        placeholder = st.empty()
        for i in range(len(text) + 1):
            placeholder.markdown(f"### ✨ {text[:i]}")
            time.sleep(0.03)

        st.success("Merci à DataScientest pour cette aventure 👏")

        st.markdown("""
        Ce projet a été une **expérience complète de mise en œuvre de la Data Science**,  
        depuis la recherche de données jusqu’à la modélisation et la réflexion MLOps.

        Il a permis de **confronter la théorie à la pratique**, de développer une **autonomie technique**,  
        et de mieux comprendre les **exigences réelles d’un projet de machine learning**.
                    
        **L'aventure continue...** 🚀  
        *#MachineLearning #DataScience #Collaboration #MLOps*
        """)
"""
code de la page

"""

from tools import *

def affiche():
    # --- Titre principal ---
    st.title("🚀 Conclusion du projet")
    st.markdown("""
    ### Synthèse, apprentissages et perspectives
    ---
    """)

    # --- Introduction dynamique ---
    st.info("💡 *Ce projet nous a permis de mettre à profit notre formation en Data Science sur un sujet concret et populaire : l'immobilier.*")

    st.write("Chaque membre de l’équipe a contribué à construire un modèle de prédiction de la valeur foncière en Gironde, en explorant de nombreuses données open source et en relevant de vrais défis techniques et organisationnels.")

    st.markdown("---")

    # --- Timeline du projet ---
    st.subheader("🧭 Les grandes étapes du projet")
    timeline = {
        "Exploration des données": 40,
        "Nettoyage et préparation": 20,
        "Modélisation": 30,
        "Mise en production": 5,
        "Présentation finale": 5
    }
    fig = px.bar(
        x=list(timeline.keys()),
        y=list(timeline.values()),
        title="Répartition du temps par phase (%)",
        labels={"x": "Phase", "y": "Temps (en %)"}
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Sections avec expanders ---
    with st.expander("📘 Bilan du projet", expanded=True):
        st.markdown("""
        Ce projet nous a permis de **mettre en pratique nos compétences** sur un cas d’usage concret et accessible à tous : le marché immobilier.

        🔹 **Recherche et manipulation de données open data** : un travail conséquent de sélection, de nettoyage et de compréhension.  
        🔹 **Vision multidimensionnelle** du problème : variables géographiques, économiques, sociales, techniques.  
        🔹 **Conscience des limites** : fraîcheur des données, absence de certaines caractéristiques clés (état du bien, subjectivité des acheteurs, etc.).  
        🔹 **Dimension humaine** : la valeur d’un bien reste partiellement subjective, au-delà des modèles statistiques.
        """)

    with st.expander("⚙️ Difficultés rencontrées"):
        st.markdown("""
        Plusieurs difficultés techniques et organisationnelles ont marqué ce projet :
        - 📊 **Choix et recherche des données** : absence de cadre initial, nécessitant beaucoup d’exploration.  
        - 🧩 **Gestion des compétences** : des décalages dans la formation ont parfois ralenti le rythme collectif.  
        - 🔁 **Arrêt des itérations** : difficile de trouver le bon équilibre entre performance et délais.  
        - 🧪 **Usage partiel d’outils MLOps (MLflow)** : suivi des expériences artisanal, comparaisons manuelles.  
        - 👀 **Absence de revue de code systématique** : difficultés à relire ou reprendre certains scripts.  
        - ⚖️ **Compromis MLOps / performance** : choix d’un modèle plus léger, réaliste pour un déploiement.
        """)

    with st.expander("🤝 Gestion du travail"):
        st.markdown("""
        La **collaboration** a permis la réalisation du projet :

        👥 **Répartition des rôles :**
        - Chaque membre a fait de la **recherche de données** open source pour déterminer les sources de données intéressantes.
        - L'**analyse des différentes sources de données** a été partagée entre les différents membres selon le temps disponible poour chacun.  
        - Pour la **modélisation**, chaque membre est parti de ses propres hypothèses (pour éviter de s'influencer et avoir des idées diversifiées)
        - **Rédaction du rapport** à trois mains en fonction des parties traitées par chacun des membres.

        🧭 **Organisation du travail :**
        - Outils communs utilisés : GitHub, Slack, Google Drive + Outils utilisés individuellement
        - Organisation : réunions hebdomadaires, liste de tâches  
        - Difficultés : disponibilité inégale, apprentissage progressif des modules de formation  

        🧠 **Enseignements tirés :**
        - Importance de la **coordination technique et humaine** dans un projet Data Science. 
        - Nécessité de **documenter et partager les expérimentations**.  
        - Mise en place nécessaire de **revues de code systématiques".
        - Recours à **MLFlow**.
        """)

    with st.expander("🌱 Futures évolutions et perspectives"):
        st.markdown("""
        Les perspectives du projet ouvrent de nombreuses voies d’amélioration :

        🔹 **1. Enrichir les données** : intégrer davantage de variables (cadastre, environnement, accessibilité, etc.)  
        🔹 **2. Ajouter des données en temps réel** : via **web scraping** de sites d’agences pour suivre les prix de marché actuels.  
        🔹 **3. Étendre le périmètre** : tester le modèle sur d’autres départements ou régions.  
        🔹 **4. Diversifier les types de biens** : terrains, locaux commerciaux, industriels.  
        🔹 **5. Explorer d’autres approches** : modèles neuronaux, deep learning, ou modèles hiérarchiques spatio-temporels.  

        En résumé, ce projet a posé les **fondations d’un modèle robuste et évolutif**, qui pourrait devenir un outil complet d’aide à la décision pour les acteurs du marché immobilier.
        """)

    # --- Animation finale ---
    st.markdown("---")
    with st.container():
        st.subheader("🎓 En conclusion...")
        text = "Un projet exigeant, formateur et techniquement et humainement enrichissant."
        placeholder = st.empty()
        for i in range(len(text) + 1):
            placeholder.markdown(f"### ✨ {text[:i]}")
            time.sleep(0.03)

        st.success("Merci à DataScientest pour cette aventure 👏")

        st.markdown("""
        Ce projet a été une **expérience complète de mise en œuvre de la Data Science**, depuis la recherche de données jusqu’à la modélisation et la réflexion MLOps.

        Il a permis de **confronter la théorie à la pratique**, de développer une **autonomie technique** et de mieux comprendre les **exigences réelles d’un projet de machine learning**.
                    
        **L'aventure continue...** 🚀  
        """)
