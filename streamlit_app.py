
# import de tous les modules commun
# et notre boite à outils
from tools import *

# import des pages ici
import page_0 # Introduction
import page_1 # Exploration
import page_2 # DataVizualization
import page_3 # Modélisation
import page_4 # Modélisation
import page_st_fct # qques fonctions streamlit 
import page_test1 # qques tests




# juste pour vérifier que le code tourne...
print(time.strftime('%Y_%m_%d %H:%M:%S'),
      "En cours d'exec...")

print(os.getcwd())

st.sidebar.title("Immo Gironde")
st.sidebar.write("🌊  🏄‍♀️  🏖️  🏡  🌲 ")
st.sidebar.header("Sommaire")

pages=["Introduction", "Exploration", "DataVizualization", "Modélisation", "Conclusion", "__st fonctions", "__test1"]
page=st.sidebar.radio("Aller vers", pages)

st.sidebar.markdown("""
                    😀 Membres du projet :
                    ----------------
                    - Cyrielle BARGET
                    - Grégory DE GLADKY
                    - Grégory FILLION
                    
                    Mentor : Yaniv BENICHOU
                    Cohorte : Janvier 2025 - Data Scientist - Format continu
                """)




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
  page_st_fct.affiche()

if page == pages[6] : 
  page_test1.affiche()

# trash



# st.page_link("page_1.py", label="Page 1", icon="1️⃣")
# st.page_link("page_1.py", label="Page 2", icon="2️⃣", disabled=True)
# st.sidebar.page_link("http://www.google.com", label="Google", icon="🌎")
# st.sidebar.page_link(".\\pages\\1_page.py", label="Home", icon="🏠")
# st.sidebar.page_link(r"pages/1_page.py", label="Home", icon="🏠")

# Définir les pages
# page1 = st.Page("page_1.py", title="Page 1", icon="📄")
# page2 = st.Page("page_2.py", title="Page 2", icon="📄")

# # Créer la navigation (par défaut dans la sidebar)
# pg = st.navigation([page1, page2])

# # Exécuter la page sélectionnée
# pg.run()
