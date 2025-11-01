"""
code de la page

"""

import streamlit as st
from tools import *

# import des pages ici
import page_0 # Introduction
import page_1 # Exploration
import page_2 # Preprocessing et Feature engineering
import page_3 # DataVisualisation
import page_4 # Modélisation
import page_5 # Simulation
import page_6 # Conclusion



def affiche():
    st.title("Prédiction des prix immobiliers en Gironde")
     

    # Affichage vertical en 4 colonnes
    col1, col2 = st.columns([0.4, 0.6], vertical_alignment='center')

    with col1:
        st.image(os.path.join("images", "Image Gironde intro.png"), width =300, )
        

    with col2:
        st.header("🎯Objectif :")
        # with st.container():

        st.info("**Construire un modèle de prédiction de prix de biens immobiliers !**")

        
        st.markdown("""                    
**A partir de :**
                    """)  
        st.subheader("- Ses caractéristiques :")
#         st.markdown("""
# ### Ses caractéristiques :
#                     """)
        col21, col22 = st.columns([0.2, 0.8], vertical_alignment='center')
        with col22:
            st.markdown("""
- Type de bien (appartement, maison, avec ou sans terrain...)
- Surface, nombe de pièces, DPE...
- Localisation géographique
                        """)
        with col21:
            st.image(os.path.join("images", "maison et arbre.jpg"), width =100, )

        st.markdown("""
### - Son environnement :
                    """)
        col23, col24 = st.columns([0.2, 0.8], vertical_alignment='center')
        with col24:
            st.markdown("""
- Proximité des transports, commerces, écoles, ...
- Statistiques économiques et sociales de sa commune
                    """)
        with col23:
            st.image(os.path.join("images", "2954458-illustration-3d-isometrique-du-quartier-de-ville-avec-maisons-vectoriel.jpg"),
                      width =100, )

        
        # st.image(os.path.join("images", "maison et jardin 3d.png"), width =200, )

        # st.image(os.path.join("images", "maison et arbre.jpg"), width =200, )
        # st.image(os.path.join("images", "quartier banlieue.jpg"), width =200, )
        # st.image(os.path.join("images", "quartier rond.png"), width =200, )
    
    st.divider()
    st.header("🎃 Introduction")
    # **Raison d'être du projet :**

    st.markdown("""
### Raison d'être du projet :""")
    st.info("""
- **Sujet populaire** : en France 18 millions de ménages propriétaires  
- Prix **complexes et dynamiques**, dépendants de multiples facteurs  
- Etre en mesure d'**objectiver** le prix via des données **factuelles**   
- Aller plus loin que le simple surface * prix/m² du quartier pour tendre vers une valeur **intrinsèque**  
- Détecter des éventuelles **anomalies de marché**  
                
Et aussi... mettre en pratique nos connaissances en Data Science et manipuler plein de données intéressantes ! 😍
...
            """)
    
    st.markdown("""
### Pourquoi la Gironde ?""")

    st.info("""
* Besoin de réduire le périmètre : s'adapter à nos ressources (temps humain et machines)  
* Région vaste et variée, présentant un bon échantillon du territoire  
    * Aussi bien géographique (villes, zones rurales, bord de mer)  
    * Que socio-économique  
* Attractivité de certaines zones et bonne dynamique des prix  
 
De plus, un des membres de l'équipe habite sur place, ce qui nous a permis de vérifier certaines infos et d'être dans le concret !


            """)
    st.divider()
    st.header("🎥 Présentation")
    
    st.markdown("""
🔍 **Exploration :** les données que nous avons retenues  
⚙️ **Preprocessing et Feature engineering :** l'exploitation des données et leurs transformations  
📊 **DataVisualisation :** une vue d'ensemble de notre dataset  
📈 **Modélisation :** les modèles étudiés et leurs résultats  
🧮 **Simulation :** un simulateur permettant de retrouver les résultats obtenus sur notre base mais également un simulateur pour les nouveaux biens  
- **Interprétabilité :** l'explication de l'impact de chaque feature pôur les prédictions
🚀 **Conclusion :** ce que nous avons appris et comment aller plus loin  

""")
    # page_1.affiche()
    # st.page_link("page_1.py", label="Exploration")

    # if st.button("🔍 **Exploration :** les données que nous avons retenues"):
    # #     st.write("Why hello there")
    #     page_1.affiche()
    
