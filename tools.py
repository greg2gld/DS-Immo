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
import random
import geopandas as gpd
import plotly.express as px

# constantes
PATH_DATA = os.path.join(".", "data")
PATH_IMAGES = os.path.join(".", "images")


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

# mise en cache des fichiers chargés
# pour éviter qu'ils se rechargent dès qu'on clique qque part
@st.cache_data
def csv_to_df(filepath, sep=",", index_col = None, col_to_ignore=[]):
    print(time.strftime('%Y_%m_%d %H:%M:%S'),
          "chargement : ", filepath)
    df = pd.read_csv(filepath,
                     sep=sep,
                     index_col = index_col)
    df = df.drop(columns = col_to_ignore)
    print(time.strftime('%Y_%m_%d %H:%M:%S'), 
          "chargement terminé")
    return df

@st.cache_data
def load_shape(filepath):
    # Charger shapefile
    print(time.strftime('%Y_%m_%d %H:%M:%S'),
          "chargement : ", filepath)
    region = gpd.read_file(filepath)

    # IMPORTANT : Reprojeter en WGS84 (longitude/latitude) si ce n'est pas déjà fait
    if region.crs.to_epsg() != 4326:
        region = region.to_crs(epsg=4326)

    # Créer une colonne 'nom_affiche' pour l'info-bulle
    region["nom_affiche"] = region["NOM"]

    print(time.strftime('%Y_%m_%d %H:%M:%S'), 
          "chargement terminé")
    # Convertir en GeoJSON exploitable
    return json.loads(region.to_json())


@st.cache_data
def preprocessing_df(df):
    # GDG: basé sur mes Notebooks, 
    # à compléter avec la dernière version

    print(time.strftime('%Y_%m_%d %H:%M:%S'),
          "Prepocessing...")
    # suppression de qques colonnes inutiles
    # col_to_ignore = ['Unnamed: 0', 
    #                 # 'index', je garde pour le lien avec POI pp
    #                 'id_mutation', 
    #                 # 'date_mutation_1', je garde !
    #                 'adresse_complete_1', 'nom_commune_1', 'id_parcelle_1', 
    #                 'types_biens_1', #type_bien (fait doublon avec code_type_local_1), 
    #                 'type_dpe_1',
    #                 # 'code_iris' je garde !
    #                 ]
    # col_to_ignore = [c for c in col_to_ignore if c in df.columns]
    # df = df.drop(columns = col_to_ignore)

    df2 = df.copy()

    # revue des types
    df2['code_type_local_1'] = df2['code_type_local_1'].astype('int')
    df2['code_type_local_2'] = df2['code_type_local_2'].astype('int')
    df2['code_iris'] = df2['code_iris'].astype('int')

    # qques recodages

    # code_type_local_1 devient maison (1= maison, 0= appart)
    df2['maison'] = df2['code_type_local_1'].replace(2, 0)
    df2.head()

    # code_type_local_2 devient dependance (0= sans, 1= avec)
    df2['dependance'] = df2['code_type_local_2'].replace(3, 1)

    # presence terrain
    # df2['terrain'] = df2['surface_terrain_1'].apply(lambda x: 1 if x>0 else 0)
    dftemp = df2['surface_terrain_1'] + df2['surface_terrain_2']
    df2['terrain'] = dftemp.apply(lambda x: 1 if x>0 else 0)

    # date_mutation_1 est splitée en année, mois
    df2['year'] = df2['date_mutation_1'].apply(lambda x: x[:4]).astype('int')
    df2['month'] = df2['date_mutation_1'].apply(lambda x: x[5:7]).astype('int')

    # suppression des colonnes maintenant inutiles
    col_toremove = ['type_bien', 'a_bien_2',
                    # 'code_nature_culture_1', 'code_nature_culture_speciale_1', 'code_nature_culture_2', 'code_nature_culture_speciale_2',
                    'code_type_local_1', 'code_type_local_2',
                    'date_mutation_1',
                    ]
    df2 = df2.drop(col_toremove, axis=1)

    # calcul prix au m² (bati uniquement, terrain ignoré):
    df2['val_bat_m2'] = df2['valeur_fonciere_1'] /  df2['surface_reelle_bati_1']
    df2['val_bat_m2'] = df2['val_bat_m2'].round()
    df2[['valeur_fonciere_1', 'surface_reelle_bati_1', 'val_bat_m2']].head()

    print(time.strftime('%Y_%m_%d %H:%M:%S'),
          "Fin du prepocessing...")
    
    return df2


import os
import zipfile
import requests
import streamlit as st

DATA_DIR = "./data/Cyrielle"
ZIP_URL = "https://www.meetmygeek.fr/DS-immo/data.zip"   # <--- your zip url
ZIP_PATH = "./data/data.zip"

# Cache to avoid re-running extraction unnecessarily
@st.cache_resource
def download_and_extract():
      if os.path.exists("{}/poi.csv".format(DATA_DIR)) and os.listdir(DATA_DIR):
        print("Datasets trouvés")
        return

      with st.spinner(f"Téléchargement des datasets..."):
            os.makedirs(DATA_DIR, exist_ok=True)

      # Download only if zip doesn't exist
      if not os.path.isfile(ZIP_PATH):
            print("zip manquant, téléchargement des fichiers")
            response = requests.get(ZIP_URL)
            with open(ZIP_PATH, "wb") as f:
                  f.write(response.content)
      # Extract
      with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
            zip_ref.extractall(DATA_DIR)
