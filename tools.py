"""
mettre ici les modules et fonctions communes à toutes les pages

"""

import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
import os
import json


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

