import streamlit as st
import time

print(time.strftime('%Y_%m_%d %H:%M:%S'),
      "En cours d'exec...")

# Définir les pages
# pages = st.Page("./pages/")
page1 = st.Page("page_1.py", title="Page 1", icon="📄")
page2 = st.Page("page_2.py", title="Page 2", icon="📄")

# print(pages)

# Créer la navigation (par défaut dans la sidebar)
pg = st.navigation([page1, page2])
# pg = st.navigation(pages)
# pg = st.navigation(pages=pages)

print(pg)

# Exécuter la page sélectionnée
pg.run()