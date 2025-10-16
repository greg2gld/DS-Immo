"""
code de la page

"""

import streamlit as st
from tools import *

def affiche():
    st.title("affiche un titre") 
    st.header("affiche un deuxième titre") 
    st.subheader("affiche un troisième titre")
    st.markdown("affiche du texte au format markdown")
    
    st.code("affiche du code")
    
    st.latex(r"""latex=\frac{1}{2}""")

       
    st.text("affichage de texte")
    st.write("affiche du texte ou du code (équivalent à print sur un notebook)") 
    
    df = pd.DataFrame({"col1": np.array([1, 2, 3, 4]),
                      "col2": np.array([10, 20, 30, 40])
                      })

    st.markdown("""Afficher un lien :                
                - [Données DVF](https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/)
                - [Base permanente des équipements](https://www.insee.fr/fr/statistiques/2011101)
                """)

    st.markdown("__affiche un dataframe :__")
    st.dataframe(df) # affiche un dataframe
    # Remarque : Il faut encadrer le code classique concernant un dataframe avec cette commande. 
    # Par exemple, si le code de base est df.head(), nous écrivons st.dataframe(df.head()) pour obtenir 
    # l'affichage sur Streamlit.*
    
    st.markdown("__affiche un tableau :__")
    st.table(df)

    st.image(os.path.join("images", "Image Gironde intro.png"),
             width =200,
             caption="une image")
    #"affiche une image (cette fonction prend en argument un np.array à 3 dimensions)"

    st.write(plt.plot(df))

    st.button # crée un bouton
    if st.checkbox("checkbox label"): # crée un bouton à cocher pour obtenir l'affichage
        st.write("checkbox cochée")
    else: 
        st.write("checkbox non cochée")

    st.selectbox("Quel est votre choix?" , ("Premier choix", "Second choix", "Troisième choix")) 
    # crée une boite avec différentes options pour obtenir l'affichage sélectionné

    st.radio("Faites votre choix", ("Premier choix", "Second choix","Troisième choix"))

    st.slider("Slider", 1, 7) # crée un curseur de défilement permettant de sélectionner une valeur numérique parmi une plage donnée
    
    st.select_slider("Choisir un jour de la semaine", 
                     options=["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"])
    # crée un curseur de défilement permettant de sélectionner une valeur non-numérique parmi une plage donnée

    st.text_input("Insérez votre texte")
    st.number_input("Choisissez votre nombre")
    st.date_input("Choisissez une date")
    st.file_uploader("Importer votre fichier")

    st.area_chart(df)

    st.line_chart(df)

    st.bar_chart(df)

    # st.bokeh_chart(df)

    st.markdown("__Afficher un graphique matplotlib.pyplot ou un graphique seaborn__")
    fig = plt.figure()
    sns.countplot(x=[1, 1, 2, 3, 3, 3])
    st.pyplot(fig)

    

    # Afficher un graphique plotly
    # st.plotly_chart(figure)

    # Afficher une carte
    # st.map(df)

    # Garder en mémoire une valeur avec la mémoire cache
    # st.cache_data

    # # Sauvegarder un modèle entraîné clf et l’importer dans streamlit avec Joblib
    # import joblib
    # joblib.dump(clf, “model”)
    # joblib.load(“model”)

    # # Sauvegarder un modèle entraîné clf et l’importer dans streamlit avec Pickle
    # import pickle
    # pickle.dump(clf, open(“model”, “wb”))
    # joblib.load(open(“model”, “wb”))

    
