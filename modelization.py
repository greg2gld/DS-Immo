import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from sklearn.neighbors import BallTree
import requests
import streamlit as st
from encode import *

@st.cache_resource
def try_load_model(path: str):
    p = Path(path)
    if not p.exists():
        st.error("Modèle introuvable : `{}`".format(p))
        return None
    try:
        return joblib.load(p)
    except Exception as e:
        st.exception(e)
        st.error("Impossible de charger le modèle. Vérifie le format (joblib/pickle) et les dépendances.")
        return None

@st.cache_data
def init_dvf():
    csv = pd.read_csv("./data/Cyrielle/dvf2024.csv")
    csv = csv.rename(columns={
        "PrixMoyen": "prix_moyen",
        "Prixm2Moyen": "prix_m2_moyen",
        "SurfaceMoy": "surface_moyenne"
    })
    return csv

# Binning
NB_BINS_POI = 5
NB_BINS_SURFACE = 24
COL_BINS_SURFACE = ["surface_terrain_1"]

# Encoding
ENCODING_PARAMETERS = {
    "ordinal_variables" : [
        'DPE_1', 
        'GES_1',
        'periode_construction_dpe_1'
    ],
    "ordinal_categories" : {
        'periode_construction_dpe_1' : [
            "avant 1948",
            "1948-1974",
            "1975-1977",
            "1978-1982",
            "1983-1988",
            "1989-2000",
            "2001-2005",
            "2006-2012",
            "2013-2021",
            "après 2021"
        ]
    },
    "one_hot_variables" : [
        'code_type_local_1', 
        'code_type_local_2', 
        'code_nature_culture_1', 
        'code_nature_culture_speciale_1',
        'code_nature_culture_speciale_2',
        'code_nature_culture_2', 
        'type_energie_chauffage_1', 
        'type_vitrage_1',
    ],
    "target_variables": [
        'code_commune_1'
    ]
}

df_etablissements = pd.read_csv("./data/categorie_bpe.csv", index_col=0)
df_etablissements[['lat_rad', 'lon_rad']] = np.radians(df_etablissements[['LATITUDE', 'LONGITUDE']])

categorie_bpe_test = df_etablissements.dropna(subset=['LATITUDE'])
filosofi = pd.read_csv("./data/cc_filosofi_2021_COM.csv", sep = ";", dtype = str)

allowed_cats = [
    'Action sociale pour enfants en bas-âge',
    'Aéroport',
    'Commerces alimentaires',
    'Déchetterie',
    'Grandes surfaces',
    'Hébergement et restauration étudiants',
    'Mairie',
    'Médecins généralistes',
    'Paramédical',
    'Parcs',
    'Services funéraires',
    'Sports, loisirs et culture',
    'Spécialistes – Médical',
    'Station-service',
    'Tourisme',
    'Transports en commun',
    'Établissements et services de santé'
]

allowed_cats_pp = [
    'Sports, loisirs et culture',
    'Commerces alimentaires', 
    'Aéroport',
    'Trains et autres transports', 
    'Mairie',
    'Déchetterie'
]

codes_nature_culture = {
    "Aucun": 0,
    "Landes": "L",
    "Landes boisées": "LB",
    "Prés": "P",
    "Pâtures": "PA",
    "Pacages": "PC",
    "Prés d’embouche": "PE",
    "Herbages": "PH",
    "Prés plantes": "PP",
    "Sols": "S",
    "Terres": "T",
    "Terres plantées": "TP",
    "Vergers": "VE",
    "Vignes": "VI",
    "Terrains à bâtir": "AB",
    "Terrains d’agrément": "AG",
    "Bois": "B",
    "Futaies feuillues": "BF",
    "Futaies mixtes": "BM",
    "Roseraies": "BO",
    "Peupleraies": "BP",
    "Futaies résineuses": "BR",
    "Taillis sous futaie": "BS",
    "Taillis simples": "BT",
    "Carrières": "CA",
    "Chemin de fer": "CH",
    "Eaux": "E",
    "Jardins":"J"
}

direct_copy = [
    "nombre_pieces_principales_1",
    "surface_reelle_bati_1",
    "periode_construction_dpe_1",
    "DPE_1",
    "GES_1",
    "type_energie_chauffage_1",
    "surface_terrain_1",
    "surface_terrain_2",
    "code_nature_culture_1",
    "code_nature_culture_2"
]

def clean_columns(df):
    df.columns = (
        df.columns.astype(str)
        .str.replace(r'[^A-Za-z0-9_]+', '_', regex=True)
        .str.strip('_')
    )
    return df

def geocode_ban(address: str, limit: int = 1):
    url = "https://api-adresse.data.gouv.fr/search/"
    params = {"q": address, "limit": limit}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    feats = data.get("features", [])
    if not feats:
        return None
    best = feats[0]["geometry"]["coordinates"]
    lon, lat = best
    return [[lat, lon]]

def compter_etablissements_proches(adresse, etab_lat_col='LATITUDE', etab_lon_col='LONGITUDE', cat_col='CATEGORIE', distances_km=[10]):
    latlon = geocode_ban(adresse)
    coord_logement = np.radians(latlon)[0]
    coords_etabs = np.radians(df_etablissements[[etab_lat_col, etab_lon_col]].values)
    tree = BallTree(coords_etabs, metric='haversine')
    radius_rads = [d / 6371 for d in distances_km]
    logement_result = {}
    
    for rad, d_km in zip(radius_rads, distances_km):
        indices = tree.query_radius([coord_logement], r=rad, return_distance=False)[0]
        if len(indices) > 0:
            cat_counts = df_etablissements.iloc[indices][cat_col].value_counts()
            for cat, count in cat_counts.items():
                if cat in allowed_cats:
                    if d_km < 1:
                        key = "{}_moins_{}m".format(cat, int(d_km * 1000))
                    else:
                        key = "{}_moins_{}km".format(cat, int(d_km))
                    logement_result[key] = count
                if cat in allowed_cats_pp:
                    df_cat = df_etablissements[df_etablissements['CATEGORIE'] == cat]
                    tree = BallTree(df_cat[['lat_rad', 'lon_rad']], metric='haversine')
                    dist, ind = tree.query([coord_logement], k=1)
                    dist_km = dist.flatten() * 6371
                    logement_result[cat + "_pp"] = float(dist_km[0])
    return logement_result

def cmp(a, b):
    return int((a > b)) - int((a < b))

def prixmoy(INSEE, X, csv):
    csv = csv[csv["INSEE_COM"].astype(str) == INSEE]
    X = X | csv[["prix_moyen","prix_m2_moyen"]].to_dict(orient="records")[0]
    X["prix_theorique"] = X["surface_reelle_bati_1"] * X["prix_m2_moyen"]
    X["comparaison_marche"] = cmp(X["prix_theorique"], X["prix_moyen"])
    return X

def prepare_data(data, bundle_type = "global"):

    csv = init_dvf()
    if "model_type" in data:
        bundle_type = data["model_type"]

    immo_bundle = try_load_model("./data/models/immo_bundle_" + bundle_type + ".pkl")
    X = {}
    for key in direct_copy:
        X[key] = data[key]

    if "adresse_insee" in data:
        X["code_commune_1"] = data["adresse_insee"]
    else:
        X["code_commune_1"] = data["code_commune_1"]
    
    X["code_commune_1"] = str(X["code_commune_1"])

    X["terrain_1"] = 1 if (X["surface_terrain_1"] > 0 or X["surface_terrain_2"] > 0) else 0
    if X["code_nature_culture_1"] in codes_nature_culture:
        X["code_nature_culture_1"] = codes_nature_culture[data["code_nature_culture_1"]]
    
    if "type_bien" in data:
        X["maison"] = 1 if data["type_bien"] == "Maison" else 0
    elif "code_type_local_1" in data:
        X["maison"] = 1 if data["code_type_local_1"] == 1 else 0

    if "adresse_full" not in data:
        adresse = "{} {} {}".format(data["adresse_num"], data["adresse_voie"], X["code_commune_1"])
    else:
        adresse = data["adresse_full"]
    X = X | compter_etablissements_proches(adresse)

    X = prixmoy(X["code_commune_1"], X, csv)
    X['surface_par_piece'] = X['surface_reelle_bati_1'] / X['nombre_pieces_principales_1']

    nb_equipements_proches = 0
    for equip in [
        "Mairie_moins_10km",
        "Commerces alimentaires_moins_10km",
        "Tourisme_moins_10km",
        "Déchetterie_moins_10km",
        "Grandes surfaces_moins_10km"
    ]:  
        if equip in X:
            nb_equipements_proches = nb_equipements_proches + X[equip]
        else:
            nb_equipements_proches = nb_equipements_proches + 0

    X["nb_equipements_proches"] = nb_equipements_proches
    X["type_vitrage_1"] = "survitrage"
    X["code_nature_culture_speciale_1"] = "POTAG"
    X["code_nature_culture_speciale_2"] = "POTAG"

    X["MED"] = float(list(filosofi[filosofi["CODGEO"] == X["code_commune_1"]]["MED21"])[0])

    df = pd.DataFrame([X])
    from utils import make_bins

    df = df.drop(columns=["code_commune_1"])
    
    COL_BINS_POI = [c for c in df.columns if c.endswith("_pp")]

    df, nope = make_bins(df, df, COL_BINS_POI, NB_BINS_POI)
    df, nope = make_bins(df, df, COL_BINS_SURFACE, NB_BINS_SURFACE, strategy="uniform", encode="ordinal")
    df, nope = make_bins(df, df, ["nb_equipements_proches"], NB_BINS_SURFACE, strategy="uniform", encode="ordinal")

    price_data = csv["prix_m2_moyen"].describe(percentiles=(0.20,0.80))
    df["travaux"] = df["prix_m2_moyen"] <= price_data["20%"]
    df["premium"] = df["prix_m2_moyen"] >= price_data["80%"]

    ordinal_variables = [col for col in ENCODING_PARAMETERS["ordinal_variables"] if col in df.columns]
    one_hot_variables = [col for col in ENCODING_PARAMETERS["one_hot_variables"] if col in df.columns]
    df_ohe = pd.get_dummies(df[one_hot_variables])
    df[list(df_ohe.columns)] = df_ohe
    df = df.drop(columns=one_hot_variables)
    df = transform_ordinal(immo_bundle["ordinal_encoder"], df, ordinal_variables)

    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    exlude_cols = one_hot_variables + ordinal_variables
    cols_restantes = [c for c in cat_cols if c not in exlude_cols]

    if len(cols_restantes):
        df = transform_target(immo_bundle["target_encoder"], df, cols_restantes)

    cols = [c for c in immo_bundle["scaler_columns"] if c not in list(df.columns)]

    for col in cols:
        df[col] = 0

    df = df[immo_bundle["scaler_columns"]]
    
    df = pd.DataFrame(immo_bundle["scaler"].transform(df), columns=df.columns, index=df.index)
    df = df.drop(columns=cols)
    df = df.drop(df.filter(like="type_vitrage").columns, axis=1)
    df = df.drop(df.filter(like="POTAG").columns, axis=1)
    
    codes_nature_requis = [
        'code_nature_culture_1_Aucun',
        'code_nature_culture_1_S',
        'code_nature_culture_2_Aucun',
        'code_nature_culture_2_S',
        'type_energie_chauffage_1_electricite',
        'type_energie_chauffage_1_gaz',
        'type_energie_chauffage_1_reseau de chaleur'
    ]
    
    for col in ['type_energie_chauffage_1_bois', 'type_energie_chauffage_1_fioul','type_energie_chauffage_1_gpl/butane/propane', 'type_energie_chauffage_1_solaire', 'type_energie_chauffage_1_charbon']:
        if col in df.columns:
            df = df.drop(columns=[col])
    
    for col in codes_nature_requis:
        if col not in df.columns:
            df[col] = 0

    for col in immo_bundle["features"]:
        if col not in list(df.columns):
            df[col] = 0

    for col in list(df.columns):
        if col not in immo_bundle["features"]:
            df = df.drop(columns=[col])

    df = df[immo_bundle["features"]]
    df = clean_columns(df)
    model = immo_bundle["model"]
    preds = model.predict(df)
    
    return preds[0]