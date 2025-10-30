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

# --- En-tête
st.set_page_config(page_title="Préprocessing et Feature Engineering", layout="wide")

# --- Fonction principale
def affiche():

    st.title("⚙️ Preprocessing et Feature Engineering")

    # ============================================================
    # 🧹 1. Retraitement initial
    # ============================================================
    st.markdown("## 🔍 1. Retraitement initial")

    with st.container():
        st.markdown("### 🏠 **Base DVF géolocalisée**")

        st.info('''
     * Conversion des données dans les types attendus
     * Suppression des lignes inexploitables
     * Restrictions du périmètre d'étude aux seules ventes
     * Renseignement des valeurs manquantes des types de locaux
     * Création de variables pour étudier les ventes comportant de multiples biens ou parcelles
     * Périmètre restreint aux transactions comportant au maximum 2 lignes (1 bien immobilier et 1 annexe dans la même commune)                        
     * Conservation des lignes relatives aux ventes :
         * d'appartements
         * de maisons
         * de locaux commerciaux, industriels ou assimilés

     ➡️ Résultat : 84 613 observations conservées.

     * Traitement des valeurs manquantes (suppression ou recherche de la donnée notamment en termes de géolocalisation (Geocoding par API))
    
     ➡️ Résultat : Aucune valeur manquante à l'issue des retraitements

     * Traitement des valeurs extrêmes ou aberrantes

        ✅ **Aucune valeur manquante** à l’issue des retraitements.
        ''')

    # --- Autres bases
    with st.container():
        st.markdown("### 🧾 **Autres bases complémentaires**")

        st.markdown("**BDNB, Filosofi, IRIS, Délinquance, Densité, Indicateurs immobiliers**")
        st.info("""
        - Conversion des données dans les types attendus
        - Traitement éventuel des valeurs manquantes
        - Pré-sélection de variables pertinentes
        """)

        st.markdown("**BPE, OpenStreetMap, Transports**")
        st.info("""
        - CConversion des données dans les types attendus
        - Restriction du périmètre géographique à la **Gironde**  
        - Fusion des différentes sources dans une base unique  
        - Suppression des doublons  
        - Création de **catégories agrégées** pour réduire la dimensionnalité
        """)

    # ============================================================
    # 🧬 2. Constitution de la base finale
    # ============================================================
    st.markdown("## 🧬 2. Constitution de la base finale")

    st.success('''
        * Rapprochement de toutes les bases précédemment citées
        * Traitement des valeurs manquantes lors du croisement des bases
        * Suppression de certaines variables
        * Calcul du nombre de points d'intérêt par catégorie avec 4 groupes de distance (50 mètres, 500 mètres, 2 et 10 kilomètres)
        * Détermination de la distance du point d'intérêt le plus proche pour chaque catégorie
        * Évolution des variables (une fois les premières simulations lancées) :
            * Création de nouvelles variables plus faciles à interpréter
            * Découpage de variables en tranches pour faciliter l'exploitation des résultats par le modèle''')  