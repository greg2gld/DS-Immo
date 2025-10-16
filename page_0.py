"""
code de la page

"""

import streamlit as st
from tools import *

@st.cache_data

def affiche():
    st.title("Prix de l'immobilier en Gironde")
     

    # --- Animation d'en-tête principale ---
    # safe_lottie_path(os.path.join("images", "maison animee.json"), height=500)

    # Affichage vertical en 4 colonnes
    col1, col2 = st.columns(2)

    with col1:
        st.image(os.path.join("images", "Image Gironde intro.png"), width =200)
        

    with col2:
        st.markdown("""                    
                    **Objectif :** 
                    Construire un modèle de prédiction performant capable d’estimer le prix d’un bien en fonction de ses caractéristiques (surface, localisation, type de bien, etc.) et de son environnement.
                    """)
        
    st.header("Introduction")


    st.markdown("""
            **Raison d'être du projet :**
                
            ...

            **Pourquoi la Gironde ?**
            
            ...

            """)
    
    
