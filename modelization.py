import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from sklearn.neighbors import BallTree
import requests
import streamlit as st
from encode import *


csv = pd.read_csv(f"./data/dvf2024.csv")
csv = csv.rename(columns={
    "PrixMoyen": "prix_moyen",
    "Prixm2Moyen": "prix_m2_moyen",
    "SurfaceMoy": "surface_moyenne"
})


all_cols = ['surface_reelle_bati_1', 'nombre_pieces_principales_1', 'surface_terrain_2', 'periode_construction_dpe_1', 'MED', 'Action sociale pour enfants en bas-âge_moins_10km', "Autres services d'action sociale_moins_10km", 'Aéroport_moins_10km', 'Commerces alimentaires_moins_10km', 'Déchetterie_moins_10km', 'Enseignement supérieur_moins_10km', 'Formation continue_moins_10km', 'Grandes surfaces_moins_10km', 'Hébergement et restauration étudiants_moins_10km', 'Mairie_moins_10km', 'Médecins généralistes_moins_10km', 'Paramédical_moins_10km', 'Parcs_moins_10km', 'Patrimoine_moins_10km', 'Police et Gendarmerie_moins_10km', 'Services funéraires_moins_10km', 'Sports, loisirs et culture_moins_10km', 'Spécialistes – Médical_moins_10km', 'Station-service_moins_10km', 'Tourisme_moins_10km', 'Trains et autres transports_moins_10km', 'Transports en commun_moins_10km', 'Écoles, collèges, lycées_moins_10km', 'Établissements et services de santé_moins_10km', 'dens_pop', 'DPE_1', 'GES_1', 'terrain_1', 'appartement', 'maison', 'prix_moyen', 'prix_m2_moyen', 'surface_moyenne', 'surface_par_piece', 'prix_theorique', 'comparaison_marche', 'prix_m2', 'travaux', 'premium', 'delinquence_bin_ml', 'Action sociale pour enfants en bas-âge_pp_bin_ml', 'Paramédical_pp_bin_ml', 'Sports, loisirs et culture_pp_bin_ml', "Autres services d'action sociale_pp_bin_ml", 'Hébergement et restauration étudiants_pp_bin_ml', 'Commerces alimentaires_pp_bin_ml', 'Station-service_pp_bin_ml', 'Écoles, collèges, lycées_pp_bin_ml', 'Enseignement supérieur_pp_bin_ml', 'Établissements et services de santé_pp_bin_ml', 'Médecins généralistes_pp_bin_ml', 'Spécialistes – Médical_pp_bin_ml', 'Formation continue_pp_bin_ml', 'Grandes surfaces_pp_bin_ml', 'Aéroport_pp_bin_ml', 'Trains et autres transports_pp_bin_ml', 'Services funéraires_pp_bin_ml', 'Police et Gendarmerie_pp_bin_ml', 'Mairie_pp_bin_ml', 'Déchetterie_pp_bin_ml', 'Tourisme_pp_bin_ml', 'Parcs_pp_bin_ml', 'Transports en commun_pp_bin_ml', 'surface_terrain_1_bin_ml', 'nb_equipements_proches_bin_ml', 'code_nature_culture_1_AB', 'code_nature_culture_1_AG', 'code_nature_culture_1_Aucun', 'code_nature_culture_1_J', 'code_nature_culture_1_L', 'code_nature_culture_1_P', 'code_nature_culture_1_S', 'code_nature_culture_1_T', 'code_nature_culture_speciale_1_ALLEE', 'code_nature_culture_speciale_1_Aucun', 'code_nature_culture_speciale_1_CAMP', 'code_nature_culture_speciale_1_IMM', 'code_nature_culture_speciale_1_PACAG', 'code_nature_culture_speciale_1_POTAG', 'code_nature_culture_speciale_2_ACACI', 'code_nature_culture_speciale_2_AIRE', 'code_nature_culture_speciale_2_ALLEE', 'code_nature_culture_speciale_2_AULN', 'code_nature_culture_speciale_2_Aucun', 'code_nature_culture_speciale_2_CAMP', 'code_nature_culture_speciale_2_CANAL', 'code_nature_culture_speciale_2_CHEM', 'code_nature_culture_speciale_2_CHENE', 'code_nature_culture_speciale_2_FRICH', 'code_nature_culture_speciale_2_IMM', 'code_nature_culture_speciale_2_MARAI', 'code_nature_culture_speciale_2_PACAG', 'code_nature_culture_speciale_2_PAFEU', 'code_nature_culture_speciale_2_PATUR', 'code_nature_culture_speciale_2_PIN', 'code_nature_culture_speciale_2_POTAG', 'code_nature_culture_speciale_2_SABLE', 'code_nature_culture_speciale_2_VAOC', 'code_nature_culture_2_AB', 'code_nature_culture_2_AG', 'code_nature_culture_2_Aucun', 'code_nature_culture_2_B', 'code_nature_culture_2_BF', 'code_nature_culture_2_BR', 'code_nature_culture_2_BT', 'code_nature_culture_2_CA', 'code_nature_culture_2_E', 'code_nature_culture_2_J', 'code_nature_culture_2_L', 'code_nature_culture_2_P', 'code_nature_culture_2_PA', 'code_nature_culture_2_PC', 'code_nature_culture_2_S', 'code_nature_culture_2_T', 'code_nature_culture_2_VI', 'type_energie_chauffage_1_bois', 'type_energie_chauffage_1_charbon', 'type_energie_chauffage_1_electricite', 'type_energie_chauffage_1_fioul', 'type_energie_chauffage_1_gaz', 'type_energie_chauffage_1_gpl/butane/propane', 'type_energie_chauffage_1_reseau de chaleur', 'type_energie_chauffage_1_solaire', 'type_vitrage_1_brique de verre ou polycarbonate', 'type_vitrage_1_double vitrage', 'type_vitrage_1_simple vitrage', 'type_vitrage_1_survitrage', 'type_vitrage_1_triple vitrage']

@st.cache_resource
def try_load_model(path: str):
    p = Path(path)
    if not p.exists():
        st.error(f"Modèle introuvable : `{p}`")
        return None
    try:
        return joblib.load(p)
    except Exception as e:
        st.exception(e)
        st.error("Impossible de charger le modèle. Vérifie le format (joblib/pickle) et les dépendances.")
        return None

immo_bundle = try_load_model("./data/immo_bundle.pkl")
print(immo_bundle)

## Constantes
TARGET = "valeur_fonciere_1"
# Binning
NB_BINS_POI = 5
NB_BINS_DELINQUENCE = 12
COL_BINS_DELINQUENCE = ["delinquence"]
NB_BINS_SURFACE = 24
COL_BINS_SURFACE = ["surface_terrain_1"]

# Outliers combinés
COMBINED_OUTLIERS_COLS = ["surface_reelle_bati_1"]
COMBINED_OUTLIERS_FLAGS = ("travaux", "premium")
COMBINED_OUTLIERS_QUANTILES = (0.25, 0.75)
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
# Feature selection
NB_FEATURES = 50

df_delinquence = pd.read_csv("./data/delinquence.csv")
def base_delinquence(df5_final):
    df_delinquence['nombre_final'] = df_delinquence['nombre'].fillna(df_delinquence['complement_info_nombre'])
    df_delinquence['taux_pour_mille_final'] = df_delinquence['taux_pour_mille'].fillna(df_delinquence['complement_info_taux'])
    df_delinquence['taux_pour_mille_final'] = df_delinquence['taux_pour_mille_final'].astype(str).str.replace(',', '.').astype(float)

    # === Nettoyage des noms d’indicateurs (remplacement des caractères spéciaux)
    remplacement_indicateurs = {
        'Vols de véhicules': 'Vols de vehicules',
        'Vols dans les véhicules': 'Vols dans les vehicules',
        "Vols d'accessoires sur véhicules": "Vols d accessoires sur vehicules",
        'Destructions et dégradations volontaires': 'Destructions et degradations volontaires',
        'Usage de stupéfiants': 'Usage de stupefiants',
        'Usage de stupéfiants (AFD)': 'Usage de stupefiants (AFD)',
        'Trafic de stupéfiants': 'Trafic de stupefiants',
        'Escroqueries': 'Escroqueries'
    }
    df_delinquence['indicateur'] = df_delinquence['indicateur'].replace(remplacement_indicateurs)
    df_delinquence['CODGEO_2024'] = df_delinquence['CODGEO_2024'].astype(str)

    # === Pivot : transforme les lignes d’indicateur en colonnes
    df_pivot = df_delinquence.pivot_table(
        index='CODGEO_2024',
        columns='indicateur',
        values='taux_pour_mille_final',
        aggfunc='first'  # Si doublons (peu probable), garde la première valeur
    )
    # Fusion avec le dvf final

    df5_final = df5_final.merge(
        df_pivot,
        how="left",
        left_on="code_commune_1",
        right_on="CODGEO_2024",
    )
    return df5_final

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
    "Verrains à bâtir": "AB",
    "Verrains d’agrément": "AG",
    "Vois": "B",
    "Vutaies feuillues": "BF",
    "Vutaies mixtes": "BM",
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

def geocode_ban(address: str, limit: int = 1):
    url = "https://api-adresse.data.gouv.fr/search/"
    params = {"q": address, "limit": limit}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    feats = data.get("features", [])
    if not feats:
        return None
    # BAN renvoie [lon, lat]
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
                    key = f"{cat}_moins_{int(d_km * 1000)}m" if d_km < 1 else f"{cat}_moins_{int(d_km)}km"
                    logement_result[key] = count
                if cat in allowed_cats_pp:
                    df_cat = df_etablissements[df_etablissements['CATEGORIE'] == cat]
                    # Construire le BallTree
                    tree = BallTree(df_cat[['lat_rad', 'lon_rad']], metric='haversine')
                    # Recherche du plus proche voisin
                    dist, ind = tree.query([coord_logement], k=1)
                    dist_km = dist.flatten() * 6371
                    # Conversion en km
                    logement_result[cat + "_pp"] = float(dist_km[0])  # Rayon terrestre en km                    
    return logement_result

def cmp(a, b):
    return int((a > b)) - int((a < b))

def prixmoy(INSEE, X, csv):
    csv = csv[csv["INSEE_COM"] == INSEE]
    X = X | csv[["prix_moyen","prix_m2_moyen"]].to_dict(orient="records")[0]
    X["prix_theorique"] = X["surface_reelle_bati_1"] * X["prix_m2_moyen"]
    X["comparaison_marche"] = cmp(X["prix_theorique"], X["prix_moyen"])
    X["prix_m2"] = X["prix_theorique"] / X["surface_reelle_bati_1"]
    return X

def prepare_data(data):
    X = {}
    for key in direct_copy:
        X[key] = data[key]
    X["terrain_1"] = 1 if (X["surface_terrain_1"] > 0 or X["surface_terrain_2"] > 0) else 0
    X["code_nature_culture_1"] = codes_nature_culture[data["code_nature_culture_1"]]
    X["appartement"] = 1 if data["type_bien"] == "Appartement" else 0
    X["maison"] = 1 if data["type_bien"] == "Maison" else 0
    adresse = f"{data["adresse_num"]} {data["adresse_voie"]} {data["adresse_insee"]}"
    X = X | compter_etablissements_proches(adresse)

    X = prixmoy(data["adresse_insee"], X, csv)
    X['surface_par_piece'] = X['surface_reelle_bati_1'] / X['nombre_pieces_principales_1']

    nb_equipements_proches = 0
    for equip in [
        "Mairie_moins_10km",
        "Commerces alimentaires_moins_10km",
        "Tourisme_moins_10km",
        "Déchetterie_moins_10km",
        "Grandes surfaces_moins_10km"
    ]:  
        nb_equipements_proches = nb_equipements_proches + X[equip]

    X["nb_equipements_proches"] = nb_equipements_proches
    X["type_vitrage_1"] = "survitrage"
    X["code_nature_culture_speciale_1"] = "POTAG"
    X["code_nature_culture_speciale_2"] = "POTAG"

    X["MED"] = float(list(filosofi[filosofi["CODGEO"] == data["adresse_insee"]]["MED21"])[0])
    X["code_commune_1"] = data["adresse_insee"]
    df = pd.DataFrame([X])
    from utils import make_bins

    df = df.drop(columns=["code_commune_1"])
    
    COL_BINS_POI = [c for c in df.columns if c.endswith("_pp")]

    df, nope = make_bins(df, df, COL_BINS_POI, NB_BINS_POI)
    df, nope = make_bins(df, df, COL_BINS_SURFACE, NB_BINS_SURFACE, strategy="uniform", encode="ordinal")
    df, nope = make_bins(df, df, ["nb_equipements_proches"], NB_BINS_SURFACE, strategy="uniform", encode="ordinal")

    price_data = csv["prix_m2_moyen"].describe(percentiles=(0.20,0.80))
    df["travaux"] = df["prix_m2"] <= price_data["20%"]
    df["premium"] = df["prix_m2"] >= price_data["80%"]

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


    cols = [c for c in all_cols if c not in list(df.columns)]

    for col in cols:
        df[col] = 0

    df = df[all_cols]
    
    print(list(df.columns))

    df = pd.DataFrame(immo_bundle["scaler"].transform(df), columns = df.columns, index = df.index)
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

    def clean_columns(df):
        df.columns = (
            df.columns.astype(str)
            .str.replace(r'[^A-Za-z0-9_]+', '_', regex=True)
            .str.strip('_')                                 
        )
        return df

    df = clean_columns(df)

    cols = ['surface_reelle_bati_1', 'nombre_pieces_principales_1', 'surface_terrain_2', 'periode_construction_dpe_1', 'MED', 'Action_sociale_pour_enfants_en_bas_ge_moins_10km', 'A_roport_moins_10km', 'Commerces_alimentaires_moins_10km', 'D_chetterie_moins_10km', 'Grandes_surfaces_moins_10km', 'H_bergement_et_restauration_tudiants_moins_10km', 'Mairie_moins_10km', 'M_decins_g_n_ralistes_moins_10km', 'Param_dical_moins_10km', 'Parcs_moins_10km', 'Services_fun_raires_moins_10km', 'Sports_loisirs_et_culture_moins_10km', 'Sp_cialistes_M_dical_moins_10km', 'Station_service_moins_10km', 'Tourisme_moins_10km', 'Transports_en_commun_moins_10km', 'tablissements_et_services_de_sant__moins_10km', 'DPE_1', 'GES_1', 'terrain_1', 'appartement', 'maison', 'prix_moyen', 'prix_m2_moyen', 'surface_par_piece', 'prix_theorique', 'comparaison_marche', 'prix_m2', 'travaux', 'premium', 'Sports_loisirs_et_culture_pp_bin_ml', 'Commerces_alimentaires_pp_bin_ml', 'A_roport_pp_bin_ml', 'Trains_et_autres_transports_pp_bin_ml', 'Mairie_pp_bin_ml', 'D_chetterie_pp_bin_ml', 'surface_terrain_1_bin_ml', 'nb_equipements_proches_bin_ml', 'code_nature_culture_1_Aucun', 'code_nature_culture_1_S', 'code_nature_culture_2_Aucun', 'code_nature_culture_2_S', 'type_energie_chauffage_1_electricite', 'type_energie_chauffage_1_gaz', 'type_energie_chauffage_1_reseau_de_chaleur']
    df = df[cols]
    model = immo_bundle["model"]
    preds =  model.predict(df)
    
    st.success(f"Le bien est estimé à {preds[0]:,.0f}€")
    