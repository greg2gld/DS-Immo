# import streamlit as st
# import graphviz

# st.title("Preprocessing et feature engineering")

# def affiche():

#     st.subheader("1. 🔍 Retraitement initial")

#     st.markdown('***DVF géolocalisé***')

#     st.markdown('''
                
#     * Suppression des lignes inexploitables
#     * Restrictions du périmètre d'étude aux seules ventes
#     * Renseignement des valeurs manquantes des types de locaux
#     * Création de variables pour étudier les ventes comportant de multiples biens ou parcelles
#     * Périmètre restreint aux transactions comportant au maximum 2 lignes (1 bien immobilier et 1 annexe dans la même commune)                        
#     * Conservation des lignes relatives aux ventes :
#         * d'appartements
#         * de maisons
#         * de locaux commerciaux, industriels ou assimilés

#     ➡️ Résultat : 84 613 observations conservées.

#     * Traitement des valeurs manquantes (suppression ou recherche de la donnée notamment en termes de géolocalisation (Geocoding par API))
    
#     ➡️ Résultat : Aucune valeur manquante à l'issue des retraitements

#     * Traitement des valeurs extrêmes ou aberrantes''')

#     st.markdown('***Autres bases***')

#     st.markdown('**BDNB, Filosofi, IRIS, Délinquance, Densité de population, Indicateurs immobiliers**')
                
#     st.markdown('''
                
#         * Traitement éventuel des valeurs manquantes
#         * Pré-sélection de variables''')

#     st.markdown('**BPE, OpenStreetMap, Transports**')
                
#     st.markdown('''
                
#         * Restriction du périmètre géographique à la Gironde
#         * Création d'une base unique regroupant tous ces éléments
#         * Traitement des doublons
#         * Création de catégories pour limiter le nombre de variables''')    

#     st.subheader("2. 🔬 Consitution de la base finale")

#     st.markdown('''
                
#         * Rapprochement de toutes les bases précédemment citées
#         * Traitement des valeurs manquantes lors du croisement des bases
#         * Suppression de certaines variables
#         * Calcul du nombre de points d'intérêt par catégorie avec 4 groupes de distance (50 mètres, 500 mètres, 2 et 10 kilomètres)
#         * Détermination de la distance du point d'intérêt le plus proche pour chaque catégorie
#         * Évolution des variables (une fois les premières simulations lancées pour améliorer les résultats du modèle) :
#                 * Création de nouvelles variables plus faciles à interpréter
#                 * Découpage de variables en tranches pour faciliter l'exploitation des résultats par le modèle''')  

import streamlit as st
from tools import *

# --- En-tête
st.set_page_config(page_title="Préprocessing et Feature Engineering", layout="wide")

# --- Fonction principale
def affiche():

    st.title("⚙️ Preprocessing et Feature Engineering")
    # st.markdown("#### Comment nous avons nettoyé, transformé et enrichi les données...")

    col01, col02 = st.columns([0.5, 0.5], vertical_alignment='top', )
    with col01:
        st.markdown("## 🗂️ Bases", )
    with col02:
        st.markdown("## 🔨 Travaux effectués")

    col1, col2 = st.columns([0.5, 0.5], vertical_alignment='center')

    with col1:
        
        st.image(os.path.join("images", "Diag1_light2.png"))
        

    with col2:
        # safe_lottie_path(os.path.join(PATH_IMAGES, "Idea_into_Book_Machine.json"), height=200)
        
        # ============================================================
        # 🧹 1. Retraitement initial
        # ============================================================
        
        

        st.markdown("### 1️⃣ Préparation des données et Data Cleaning")

        with st.expander("**💾 Pour toutes les bases:**"):
                            
            st.info('''
* Conversion des types (.dtype)
* Traitement des valeurs manquantes (manuel, ou usage d’API) 
* Suppressions des lignes inexploitables ou doublons
* Pré-sélection de variables pertinentes
* Traitement des valeurs extrêmes ou aberrantes
                    ''')
           
        # --- Autres bases
        with st.expander("**🏡 Spécifiques au DVF:**"):
            
            st.info("""
- Restrictions du périmètre d'étude aux seules ventes
- Création de variables pour étudier les ventes comportant de multiples biens ou parcelles
- Périmètre restreint aux transactions comportant au maximum 2 lignes (1 bien immobilier et 1 annexe dans la même commune)
- Conservation des lignes relatives aux ventes :
    - d'appartements
    - de maisons
    - de locaux commerciaux, industriels ou assimilés

            """)

        with st.expander("**📊 Spécifiques à BPE, OpenStreetMap, Transports**"):
            st.info("""
- Restriction du périmètre géographique: rectangle incluant la Gironde (longitude/latitude)
- Fusion des différentes sources dans une base unique
- Agrégation de features pour réduction de dimension (Urgences + Maternité + Centre de santé + … = Établissements de santé) 144 types -> 24  catégories de POI

            """)

        # ============================================================
        # 🧬 2. Constitution de la base finale
        # ============================================================
        st.markdown("### 2️⃣ Agrégation et enrichissement")



        with st.expander(" **💰 Constitution de la base finale**"):

            st.info("""
- Jointures multiples (codes communes, IRIS, parcelle, bâtiment…)
- Calcul du nombre de points d'intérêt par catégorie avec 4 groupes de distance (50 mètres, 500 mètres, 2 et 10 kilomètres)
- Détermination de la distance du point d'intérêt le plus proche pour chaque catégorie
- Évolution des variables dans le cadre de la modélisation
                        """)