
# import de tous les modules commun
# et notre boite à outils
from tools import *

# import des pages ici
import page_0 # Introduction
import page_1 # Exploration
import page_2 # Preprocessing et Feature engineering
import page_3 # DataVisualisation
import page_4 # Modélisation
import page_5 # Simulation
import page_6 # SHAP
import page_7 # Conclusion
# import page_st_fct # qques fonctions streamlit

download_and_extract()

st.set_page_config(
    page_title="Prix Immobilier Gironde",
    page_icon="🏡",
    layout="wide",     # ← ICI : mode large
)

# juste pour vérifier que le code tourne...
print(time.strftime('%Y_%m_%d %H:%M:%S'),
      "En cours d'exec...")

st.sidebar.title("Prédire les prix immobiliers en Gironde")
st.sidebar.header("Sommaire")

pages = ["🏠 Introduction", "🔍 Exploration", "⚙️ Preprocessing et Feature engineering", "📊 Datavisualisation", "📈 Modélisation", "🧮 Simulation","Interprétabilité SHAP", "🚀 Conclusion"]
page=st.sidebar.radio("Aller à", pages)

st.sidebar.markdown("""
                    🧑‍🤝‍🧑 Membres du projet :
                    ----------------
                    - Cyrielle BARGET
                    - Grégory DE GLADKY
                    - Grégory FILLION
                    
                    Mentor : Yaniv BENICHOU
                    Cohorte : Janvier 2025 - Data Scientist - Format continu
                """)

st.sidebar.image(os.path.join("images", "Image Gironde intro.png"), width =300, )


# appel de chaque page
if page == pages[0] :
  page_0.affiche()

if page == pages[1] :
  page_1.affiche()

if page == pages[2] :
  page_2.affiche()

if page == pages[3] :
  page_3.affiche()

if page == pages[4] :
  page_4.affiche()

if page == pages[5] :
  page_5.affiche()

if page == pages[6] :
  page_6.affiche()

if page == pages[7] :
  page_7.affiche()
