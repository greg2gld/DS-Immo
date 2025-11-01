from tools import *
from modelization import *
from encode import *

import streamlit as st
from datetime import date, time, datetime
import pandas as pd
import plotly.express as px
from PIL import Image

def affiche():
    st.title("Modélisation")

    st.write("""
    Cette page retrace l’ensemble du processus d’entraînement et d’optimisation du modèle prédictif.
    """)

    # -------- 1. Encodage --------
    st.header("1️⃣ Encodage des variables")

    st.write("Nous avons utilisé un mix d'encoding : Ordinal, One-Hot et Target Encoding...")

    # -------- 2. Normalisation --------
    st.header("2️⃣ Choix du scaler")

    st.write("""
    Trois scalers testés : **StandardScaler**, **MinMaxScaler**, **RobustScaler**.  
    Le **StandardScaler** a été retenu — pas de gain significatif avec les autres.
    """)

    # -------- 3. Modèles testés --------
    st.header("3️⃣ Sélection du modèle de base")

    image = Image.open("data/Cyrielle/resultats_lazyregressor.png")
    st.image(image, caption="Résultats LazyPredict – Comparaison des modèles")

    st.success("✅ LGBMRegressor retenu")

    # -------- 4. Optimisations --------
    st.header("4️⃣ Optimisation du modèle")

    st.header("📈 Évolution des performances du modèle")

    data = {
        "Types de modèles": [
            "Modèle de base",
            "Modèle appartements uniquement",
            "Modèle maisons uniquement",
            "Modèle Introduction variables simplifiées et variables tranchées",
            "Modèle avec variables premium et travaux",
            "Meta-modèle",
            "Meta-modèle avec hyperparamètres optimisés",
            "Meta-modèle avec hyperparamètres optimisés et feature selection",
            "Meta-modèle avec hyperparamètres optimisés, feature selection et clustering"
        ],
        "R² train": [0.8651, 0.8493, 0.8492, 0.8918, 0.8919, 0.8856, 0.9098, 0.9045, 0.9064],
        "MAPE train": [17.26, 13.76, 18.04, 15.79, 15.81, 16.04, 14.61, 14.98, 14.81],
        "R² test": [0.8271, 0.7873, 0.7741, 0.8405, 0.8413, 0.8413, 0.8428, 0.8429, 0.8438],
        "MAPE test": [18.58, 15.44, 20.97, 17.27, 17.24, 17.23, 16.97, 17.04, 17.03]
    }

    df = pd.DataFrame(data)
    # Convertir R² en %
    df["R² train (%)"] = df["R² train"] * 100
    df["R² test (%)"] = df["R² test"] * 100

    st.subheader("✅ Comparaison des scores R² (%)")
    fig_r2 = px.line(
        df,
        x="Types de modèles",
        y=["R² train (%)", "R² test (%)"],
        markers=True,
        title="Évolution du R² (%)"
    )
    fig_r2.update_layout(xaxis_title="Modèles", yaxis_title="R² (%)", xaxis_tickangle=-25)
    st.plotly_chart(fig_r2, use_container_width=True)

    st.subheader("✅ Comparaison des erreurs MAPE (%)")
    fig_mape = px.line(
        df,
        x="Types de modèles",
        y=["MAPE train", "MAPE test"],
        markers=True,
        title="Évolution du MAPE (%)"
    )
    fig_mape.update_layout(xaxis_title="Modèles", yaxis_title="Erreur MAPE (%)", xaxis_tickangle=-25)
    st.plotly_chart(fig_mape, use_container_width=True)

    # Affichage tableau
    with st.expander("📊 Voir les données brutes"):
        st.dataframe(df)

    st.info("""
    Optimisations effectuées :
    - Feature engineering
    - Variables simplifiées & tranchées
    - Stacking (LGBM + CatBoost + Ridge)
    - Hyperparamètres optimisés
    - Feature selection (SelectKBest)
    - Clustering HDBSCAN pour outliers
    """)

    # -------- 5. Conclusion --------
    st.header("🎯 Modèle final retenu")

    st.success("""
    Meta-modèle final avec :
    - 50 variables
    - R² test ≈ 84.38 %
    - MAPE ≈ 17.03 %
    """)

    st.header("📄 Choix de présentation de plusieurs modèles dans l'onglet Simulation")

    st.info("""
    Pour les simulations avec des biens réels mais aussi avec les données présentes dans X_train et X_test, nous avons fait le choix de vous présenter 4 modèles distincts :

    - **Modèle Global** : Modèle retenu  
    - **Modèle Maison** : Modèle retenu appliqué aux seules maisons  
    - **Modèle Appartements** : Modèle retenu appliqué aux seuls appartements  
    - **Modèle Max** : Modèle présentant les meilleurs résultats avec un clustering générant une suppression de la moitié du dataset
    """)

    st.header("📈 Performances globale de ces modèles")

    data = {
        "Types de modèles": [
            "Modèle Global",
            "Modèle Maisons",
            "Modèle Appartements",
            "Modèle Max"
        ],
        "R² train (en %)": [90.64,],
        "MAPE train (en %)": [14.81,],
        "R² test (en %)": [84.38,],
        "MAPE test (en %)": [17.03,]
    }

    df = pd.DataFrame(data)
 
    # Affichage tableau
    with st.expander("📊 Voir les performances de ces différents modèles"):
        st.dataframe(df)