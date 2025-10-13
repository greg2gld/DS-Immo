"""
code de la page

"""

import streamlit as st
from tools import *

def affiche():
    st.write("### Introduction")
    st.write("hello je suis la page 0")

    # --- Animation d'en-tête principale ---
    safe_lottie_path(os.path.join("images", "r6BoDuSSqg.json"), height=500)

    # with st.echo():
    #     st_lottie(json.load("images\\r6BoDuSSqg.json"))