"""
code de la page

"""

from tools import *

print(__name__)

def affiche():
    st.title("Exploration")
    st.markdown("""
    Projet proposé par l'équipe, donc :
                
                ➡️ Sans données fournies par DataScientest 
                ➡️ Long travail de recherche / exploration des données opensource
                ➡️ Pour retenir celles nous semblant pertinentes
                """)
    st.header("1. La base principale")
    st.subheader("Le fichier DVF géolocalisé (2020–2024)")
    st.markdown("""
                Il contient:
                - L’ensemble des biens pour lesquels une transactions immobilières a été réalisées :
                    - En France 
                    - entre 2020 et 2024
                - Des informations géographiques précises (coordonnées GPS) des biens
                - Un ensemble de caratéristiques des biens (type, surface, nombre de pièces...)
                """)
    
    st.header("2. Les données périphériques")
    st.markdown("""
                
                
                Le DVF a été enrichi avec les données open source suivantes :
                """)
                
    # tableau
    data = {'Catégorie': ['Caract. du bien',
                'Économique / Sociale',
                'Économique / Sociale',
                'Économique / Sociale',
                'Économique / Sociale',
                'Géographique',
                'Géographique',
                'Géographique',
                'Géographique'],
            'Nom': ['BDNB',
                'IRIS',
                'FiLoSoFi',
                'Densité de population',
                'Délinquance',
                'Transports',
                'BPE',
                'OpenStreetMap',
                'Contours IRIS'],
            'Description': ['Base de données nationale des bâtiments. Niveau : batiment. Date : 2024-10',
                "Ilots Regroupés pour l'Information Statistique. Données économiques sur la population au sein d'une zones géographique (IRIS)\nNiveau: IRIS\nDate : 2021-12\n\nUsage technique afin de pouvoir exploiter la source FiLoSoFi dont le niveau le plus fin est le découpage IRIS",
                'Fichier localisé social et fiscal\nNiveau: IRIS\nDate: 2021',
                'Ce fichier contient la densité de population historique par commune de 1968 à 2021 \nNiveau: Commune\nDate: 2021',
                'Statistiques de la délinquance enregistrées par la police et la gendarmerie nationales\nNiveau: commune, département\nDate: 2024',
                'Arrêts de transport en France\nNiveau: coordonnées géo\nDate: 2024-02',
                'Base Permanente des Équipements\nNiveau: coordonnées géo\nDate: 2023',
                "Base collaborative des points d'intérêts\nNiveau: coordonnées géo\nDate: 2024-09",
                'Fichier technique contenant la géométrie des IRIS (coord GPS)\nNiveau: IRIS / coordonnées gép\nDate: 2024'],
                'Utilisation': ['DPE, année de construction, classe émission GES...',
                'Revenu médian, taux de pauvreté et taux de chômage',
                'Compléter le fichier IRIS sur des données manquantes',
                'Densité de population',
                'différents indicateurs de délinquance',
                '',
                "Lister les équipements autour d'un bien",
                'Lister les POI autour du bien',
                'Lier les données au niveau IRIS avec des données au niveau coordonnées GPS provenant des autres sources.'],
            'Source': ['[Data Gouv](https://www.data.gouv.fr/fr/datasets/base-de-donnees-nationale-des-batiments/)',
                '[INSEE](https://www.insee.fr/fr/statistiques/fichier/8229323/BASE_TD_FILO_IRIS_2021_DEC_CSV.zip)',
                '[INSEE](https://www.insee.fr/fr/statistiques/8229323)',
                '[Observatoire des territoires](https://www.observatoire-des-territoires.gouv.fr/densite-de-population)',
                '[Data Gouv](https://www.data.gouv.fr/fr/datasets/r/17a807b1-8c4b-4c6d-afdd-8c62f26fd2c5)',
                '[Transports Data Gouv](https://transport.data.gouv.fr/resources/81333)',
                '[INSEE](https://www.insee.fr/fr/statistiques/8217537)',
                '[Data Gouv](https://www.data.gouv.fr/fr/datasets/points-dinterets-openstreetmap/)',
                '[Géoservices](https://geoservices.ign.fr/contoursiris)'],
            }
    tableau = pd.DataFrame(data)
    tableau = tableau.replace("\n", ". ", regex=True)
    # Afficher le tableau en Markdown 
    st.write(tableau.to_markdown(index=False), unsafe_allow_html=False)

    # affiche les champs et description des datasets
    st.subheader("Datasets, champs et descriptions")
    df = csv_to_df(os.path.join(PATH_DATA, "presentation_data_retenus.csv"), sep=";")
    # st.dataframe(df.head())
    l_choix = df['Dataset'].unique()             
    selection = st.selectbox("Choisir un DataSet :" , l_choix)
    st.write("Nombre de champs : ", df.shape[0])
    st.dataframe(df[df['Dataset'] == selection][['Libellé des variables', 'Descriptif des variables']])
    

