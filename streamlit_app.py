
import streamlit as st
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
import time
import os
import json

# lister les pages ici
import page_0
import page_1
import page_2

# on peut mettre des emoji avec win+;

from streamlit_lottie import st_lottie




st.title("Estimation prix de l'immobilier 😍")
st.sidebar.title("Sommaire")
pages=["Introduction", "Exploration", "DataVizualization", "Modélisation"]
page=st.sidebar.radio("Aller vers", pages)


# mettre dans un module séparé pour l'appeler des autres pages

# --- Animation Loader depuis fichiers locaux ---
def load_lottiefile(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

def safe_lottie_path(filepath, height=200):
    anim = load_lottiefile(filepath)
    if anim:
        st_lottie(anim, height=height)
    else:
        st.warning(f"❌ Animation '{filepath}' introuvable.")



# --- Animation d'en-tête principale ---
safe_lottie_path(os.path.join("images", "r6BoDuSSqg.json"), height=500)

# with st.echo():
#     st_lottie(json.load("images\\r6BoDuSSqg.json"))


if page == pages[0] : 
  page_0.affiche()

if page == pages[1] : 
  page_1.affiche()

if page == pages[2] : 
  page_2.affiche()
