


# nos modules
from tools import *



# on peut mettre des emoji avec win+;

st.title("Estimation prix de l'immobilier 😍")
st.sidebar.title("Sommaire")
pages=["Introduction", "Exploration", "DataVizualization", "Modélisation"]
page=st.sidebar.radio("Aller vers", pages)

# lister les pages ici
import page_0 # Introduction
import page_1 # Exploration
import page_2 # DataVizualization
import page_3 # Modélisation

# appel de chaque page
if page == pages[0] : 
  page_0.affiche()

if page == pages[1] : 
  page_1.affiche()

if page == pages[2] : 
  page_2.affiche()
