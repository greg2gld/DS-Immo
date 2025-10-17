"""
code de la page

"""

# import streamlit as st
from tools import *

def affiche1():
    


    'Starting a long computation...'

    # Add a placeholder
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        # Update the progress bar with each iteration.
        latest_iteration.text(f'Iteration {i+1}')
        bar.progress(i + 1)
        time.sleep(0.1)

    '...and now we\'re done!'

def affiche2():
    data = {
        "Nom": ["Google", "OpenAI"],
        "Lien": [
            "[Visiter](https://google.com)",
            "[Visiter](https://openai.com)"
        ]
    }

    df = pd.DataFrame(data)

    # Afficher le tableau en Markdown (statique mais propre)
    st.write(df.to_markdown(index=False), unsafe_allow_html=False)
    # print(df.to_markdown(index=False))

def affiche3():
    # ex html

     myhtml = """<table border=".">
        <thead>
        <tr style="height: 35.2px;">
        <th style="height: 35.2px;">
        <p><strong>Cat&eacute;gorie</strong></p>
        </th>
        <th style="height: 35.2px;">
        <p><strong>Nom</strong></p>
        </th>
        <th style="height: 35.2px;">
        <p><strong>Description</strong></p>
        </th>
        <th style="height: 35.2px;">
        <p><strong>Utilisation</strong></p>
        </th>
        <th style="height: 35.2px;">
        <p><strong>Source</strong></p>
        </th>
        </tr>
        </thead>
        <tbody>
        <tr style="height: 84px;">
        <td style="height: 84px;">
        <p><span style="font-weight: 400;">Caract. du bien</span></p>
        </td>
        <td style="height: 84px;">
        <p><strong>BDNB</strong></p>
        </td>
        <td style="height: 84px;">
        <p><span style="font-weight: 400;">Base de donn&eacute;es nationale des b&acirc;timents.</span></p>
        <p><span style="font-weight: 400;">Niveau : batiment</span></p>
        <p><span style="font-weight: 400;">Date : 2024-10</span></p>
        </td>
        <th style="height: 84px;">
        <p><span style="font-weight: 400;">DPE, ann&eacute;e de construction, classe &eacute;mission GES...</span></p>
        </th>
        <td style="height: 84px;">
        <p><a href="https://www.data.gouv.fr/fr/datasets/base-de-donnees-nationale-des-batiments/"><span style="font-weight: 400;">Data Gouv</span></a></p>
        </td>
        </tr>
        <tr style="height: 172px;">
        <td style="height: 172px;">
        <p><span style="font-weight: 400;">&Eacute;conomique / Sociale</span></p>
        </td>
        <td style="height: 172px;">
        <p><strong>IRIS</strong></p>
        </td>
        <td style="height: 172px;">
        <p><span style="font-weight: 400;">Ilots Regroup&eacute;s pour l'Information Statistique</span></p>
        <p><span style="font-weight: 400;">Donn&eacute;es &eacute;conomiques sur la population au sein d'une zones g&eacute;ographique (IRIS)</span></p>
        <p><span style="font-weight: 400;">Niveau: IRIS</span></p>
        <p><span style="font-weight: 400;">Date : 2021-12</span></p>
        <br />
        <p><span style="font-weight: 400;">Usage technique afin de pouvoir exploiter la source FiLoSoFi dont le niveau le plus fin est le d&eacute;coupage IRIS</span></p>
        </td>
        <td style="height: 172px;">
        <p><span style="font-weight: 400;">Revenu m&eacute;dian, taux de pauvret&eacute; et taux de ch&ocirc;mage</span></p>
        </td>
        <td style="height: 172px;">
        <p><a href="https://www.insee.fr/fr/statistiques/fichier/8229323/BASE_TD_FILO_IRIS_2021_DEC_CSV.zip"><span style="font-weight: 400;">INSEE</span></a></p>
        </td>
        </tr>
        <tr style="height: 84px;">
        <td style="height: 84px;">
        <p><span style="font-weight: 400;">&Eacute;conomique / Sociale</span></p>
        </td>
        <td style="height: 84px;">
        <p><strong>FiLoSoFi</strong></p>
        </td>
        <td style="height: 84px;">
        <p><span style="font-weight: 400;">Fichier localis&eacute; social et fiscal</span></p>
        <p><span style="font-weight: 400;">Niveau: IRIS</span></p>
        <p><span style="font-weight: 400;">Date: 2021</span></p>
        </td>
        <td style="height: 84px;">
        <p><span style="font-weight: 400;">Compl&eacute;ter le fichier IRIS sur des donn&eacute;es manquantes</span></p>
        </td>
        <td style="height: 84px;">
        <p><a href="https://www.insee.fr/fr/statistiques/8229323"><span style="font-weight: 400;">INSEE</span></a></p>
        </td>
        </tr>
        <tr style="height: 84px;">
        <td style="height: 84px;">
        <p><span style="font-weight: 400;">&Eacute;conomique / Sociale</span></p>
        </td>
        <td style="height: 84px;">
        <p><strong>Densit&eacute; de population</strong></p>
        </td>
        <td style="height: 84px;">
        <p><span style="font-weight: 400;">Ce fichier contient la densit&eacute; de population historique par commune de 1968 &agrave; 2021&nbsp;</span></p>
        <p><span style="font-weight: 400;">Niveau: Commune</span></p>
        <p><span style="font-weight: 400;">Date: 2021</span></p>
        </td>
        <td style="height: 84px;">
        <p><span style="font-weight: 400;">Densit&eacute; de population</span></p>
        </td>
        <td style="height: 84px;">
        <p><a href="https://www.observatoire-des-territoires.gouv.fr/densite-de-population"><span style="font-weight: 400;">Observatoire des territoires</span></a></p>
        </td>
        </tr>
        <tr style="height: 84px;">
        <td style="height: 84px;">
        <p><span style="font-weight: 400;">&Eacute;conomique / Sociale</span></p>
        </td>
        <td style="height: 84px;">
        <p><strong>D&eacute;linquance</strong></p>
        </td>
        <td style="height: 84px;">
        <p><span style="font-weight: 400;">Statistiques de la d&eacute;linquance enregistr&eacute;es par la police et la gendarmerie nationales</span></p>
        <p><span style="font-weight: 400;">Niveau: commune, d&eacute;partement</span></p>
        <p><span style="font-weight: 400;">Date: 2024</span></p>
        </td>
        <td style="height: 84px;">
        <p><span style="font-weight: 400;">diff&eacute;rents indicateurs de d&eacute;linquance</span></p>
        </td>
        <td style="height: 84px;">
        <p><a href="https://www.data.gouv.fr/fr/datasets/r/17a807b1-8c4b-4c6d-afdd-8c62f26fd2c5"><span style="font-weight: 400;">Data Gouv</span></a></p>
        </td>
        </tr>
        <tr style="height: 84px;">
        <td style="height: 84px;">
        <p><span style="font-weight: 400;">G&eacute;ographique</span></p>
        </td>
        <td style="height: 84px;">
        <p><strong>Transports</strong></p>
        </td>
        <td style="height: 84px;">
        <p><span style="font-weight: 400;">Arr&ecirc;ts de transport en France</span></p>
        <p><span style="font-weight: 400;">Niveau: coordonn&eacute;es g&eacute;o</span></p>
        <p><span style="font-weight: 400;">Date: 2024-02</span></p>
        </td>
        <td style="height: 84px;">&nbsp;</td>
        <td style="height: 84px;">
        <p><a href="https://transport.data.gouv.fr/resources/81333"><span style="font-weight: 400;">Transports Data Gouv</span></a></p>
        </td>
        </tr>
        <tr style="height: 84px;">
        <td style="height: 84px;">
        <p><span style="font-weight: 400;">G&eacute;ographique</span></p>
        </td>
        <td style="height: 84px;">
        <p><strong>BPE</strong></p>
        </td>
        <td style="height: 84px;">
        <p><span style="font-weight: 400;">Base Permanente des &Eacute;quipements</span></p>
        <p><span style="font-weight: 400;">Niveau: coordonn&eacute;es g&eacute;o</span></p>
        <p><span style="font-weight: 400;">Date: 2023</span></p>
        </td>
        <td style="height: 84px;">
        <p><span style="font-weight: 400;">Lister les &eacute;quipements autour d'un bien</span></p>
        </td>
        <td style="height: 84px;">
        <p><a href="https://www.insee.fr/fr/statistiques/8217537"><span style="font-weight: 400;">INSEE</span></a></p>
        </td>
        </tr>
        <tr style="height: 84px;">
        <td style="height: 84px;">
        <p><span style="font-weight: 400;">G&eacute;ographique</span></p>
        </td>
        <td style="height: 84px;">
        <p><strong>OpenStreetMap</strong></p>
        </td>
        <td style="height: 84px;">
        <p><span style="font-weight: 400;">Base collaborative des points d'int&eacute;r&ecirc;ts</span></p>
        <p><span style="font-weight: 400;">Niveau: coordonn&eacute;es g&eacute;o</span></p>
        <p><span style="font-weight: 400;">Date: 2024-09</span></p>
        </td>
        <td style="height: 84px;">
        <p><span style="font-weight: 400;">Lister les POI autour du bien</span></p>
        </td>
        <td style="height: 84px;">
        <p><a href="https://www.data.gouv.fr/fr/datasets/points-dinterets-openstreetmap/"><span style="font-weight: 400;">Data Gouv</span></a></p>
        </td>
        </tr>
        <tr style="height: 84px;">
        <td style="height: 84px;">
        <p><span style="font-weight: 400;">G&eacute;ographique</span></p>
        </td>
        <td style="height: 84px;">
        <p><strong>Contours IRIS</strong></p>
        </td>
        <td style="height: 84px;">
        <p><span style="font-weight: 400;">Fichier technique contenant la g&eacute;om&eacute;trie des IRIS (coord GPS)</span></p>
        <p><span style="font-weight: 400;">Niveau: IRIS / coordonn&eacute;es g&eacute;p</span></p>
        <p><span style="font-weight: 400;">Date: 2024</span></p>
        </td>
        <td style="height: 84px;">
        <p><span style="font-weight: 400;">Lier les donn&eacute;es au niveau IRIS avec des donn&eacute;es au niveau coordonn&eacute;es GPS provenant des autres sources.</span></p>
        </td>
        <td style="height: 84px;">
        <p><a href="https://geoservices.ign.fr/contoursiris"><span style="font-weight: 400;">G&eacute;oservices</span></a></p>
        </td>
        </tr>
        </tbody>
        </table>
        """
     st.write(myhtml, unsafe_allow_html=True)


def affiche():
    # PATH_DATA
    
    df = pd.read_csv(os.path.join(PATH_DATA, "presentation_data_retenus.csv"), sep=";")
                     
    # temp = st.selectbox("Quel est votre choix?" , ("Premier choix", "Second choix", "Troisième choix"))
    # print(temp)
    st.dataframe(df.head())