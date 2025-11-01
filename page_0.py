"""
code de la page

"""

import streamlit as st
from tools import *



def affiche():
    st.title("Prédiction des prix immobiliers en Gironde")
     

    # Affichage vertical en 4 colonnes
    col1, col2 = st.columns(2)

    with col1:
        st.image(os.path.join("images", "Image Gironde intro.png"), width =300, )
        

    with col2:
        st.header("🎯Objectif :")
        st.markdown("""                    
**Construire un modèle de prédiction de prix de biens immobiliers.**
                    
Notamment, à partir de :
- Ses caractéristiques : 
    - Type de bien (appartement, maison, avec ou sans terrain...)
    - Surface, nombe de pièces, DPE...
    - Localisation géographique
    - ...
- Son environnement :
    - Proximité des transports, commerces, écoles, ...
    - Statistiques économiques et sociales de sa commune
    - ...
                    """)
        
    st.header("Introduction")
    # **Raison d'être du projet :**

    st.markdown("""
**Raison d'être du projet :**
- **Sujet populaire** : en France 18 millions de ménages propriétaires
- Prix **complexes et dynamiques**, dépendants de multiples facteurs
- Etre en mesure d'**objectiver** le prix via des données **factuelles** 
- Aller plus loin que le simple surface * prix/m² du quartier pour tendre vers une valeur **intrinsèque**
- Détecter des éventuelles **anomalies de marché**
                
Et aussi... mettre en pratique nos connaissances en Data Science et manipuler plein de données intéressantes !
...

**🌍Pourquoi la Gironde ?**

- Besoin de réduire le périmètre : s'adapter à nos ressources (temps humain et machines)
- Région vaste et variée, présentant un bon échantillon du territoire 
    - Aussi bien géographique (villes, zones rurales, bord de mer)
    - Que socio-économique
- Attractivité de certaines zones et bonne dynamique des prix
 
De plus, un des membres de l'équipe habite sur place, ce qui nous a permis de vérifier certaines infos et d'être dans le concret !


            """)
    st.header("Présentation")
    # **Raison d'être du projet :**

    st.markdown("""
- **Exploration :** les données que nous avons retenues
- **Preprocessing et Feature engineering :** l'exploitation des données et leurs transformations
- **Datavisualisation :** une vue d'ensemble de notre dataset
- **Modélisation :** les modèles étudiés et leurs résultats
- **Simulation :** un simulateur permettant de retrouver les résultats obtenus sur notre base mais également un simulateur pour les nouveaux biens
- **Conclusion :** ce que nous avons appris et comment aller plus loin

""")

    
