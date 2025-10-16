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
        st.markdown("### pres projet")
        
    st.header("Introduction")


    st.text("""
            hello
            """)
    
    # def generate_random_value(x): 
    #     return random.uniform(0, x) 
    # a = generate_random_value(10) 
    # b = generate_random_value(20) 

    # st.write(a)
    # st.write(b)
