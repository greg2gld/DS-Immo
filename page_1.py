"""
code de la page

"""
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from tools import *
import pydeck as pdk
from pathlib import Path

# ---------------------------------------------------------------------
# 🔧 CONSTANTES GLOBALES
# ---------------------------------------------------------------------

BASES_NON_RETENUES = pd.DataFrame({
    "Base": [
        "DVF non géolocalisé",
        "DVF enrichi avec OpenData",
        "DV3F",
        "Chiffres détaillés du logement",
        "Données cadastrales",
        "Sitadel",
        "DPE depuis juillet 2021",
        "Chômage par département",
        "Type d'emploi par commune",
        "Population",
        "Base Tous salariés",
        "Chiffres détaillés du tourisme",
        "Géorisques",
        "RAMSESE",
        "DATA Tourisme",
        "Offre de transport - Gironde",
        "Offres de covoiturage en Gironde"
    ],
    "Description": [
        "Version brute des données DVF, sans géocodage",
        "DVF avec d'autres jeux en open data",
        "Base interne à l'administration, non libre d'accès",
        "Données sur les logements (surface, pièces...)",
        "Parcelles cadastrales : géométrie, surface, identifiants",
        "Permis de construire par commune",
        "Performance énergétique (DPE)",
        "Taux de chômage localisés 2024",
        "Professions par commune",
        "Population 2022 par commune",
        "Statistiques sur les salariés",
        "Capacité d'accueil touristique 2020",
        "Risques naturels et technologiques",
        "Établissements scolaires",
        "Points d'intérêt touristiques",
        "Réseau de transport interurbain",
        "Aires de covoiturage"
    ],
    "Raison non retenue": [
        "Version jugée trop peu structurée pour un projet spatial",
        "Absence de précision sur les retraitements",
        "Base pas libre d'accès",
        "Non pertinente pour le modèle ML",
        "Données trop lourdes pour usage actuel",
        "Périmètre non nécessaire à l’étude",
        "Trop récente / incomplète",
        "Granularité trop large (département)",
        "Incohérence spatiale avec DVF",
        "Pas assez de variation spatiale",
        "Données économiques trop générales",
        "Non directement liées aux prix",
        "Risque de doublons / bruit spatial",
        "Usage éducatif, pas pertinent ici",
        "Sources trop hétérogènes",
        "Peu d’impact sur prix immobilier",
        "Données trop ponctuelles"
    ]
})

BASES_RETENUES = pd.DataFrame({
    "Base": [
        "DVF géolocalisé",
        "BDNB",
        "FiLoSoFi",
        "Densité de population",
        "Délinquance",
        "Transports",
        "BPE",
        "OpenStreetMap",
        "Contours IRIS",
        "Indicateurs immobiliers"
    ],
    "Description": [
        "Transactions immobilières (2020–2024)",
        "Base de données nationale des bâtiments",
        "Revenus et indicateurs économiques par IRIS",
        "Densité de population historique (1968–2021)",
        "Statistiques de la délinquance",
        "Arrêts et lignes de transport",
        "Base Permanente des Équipements",
        "Points d’intérêts collaboratifs (POI)",
        "Géométries des IRIS (coordonnées GPS)",
        "Caractéristiques du marché immobilier (2013–2024)"
    ]
})

DATA_PATHS = {
    "DVF géolocalisé (transactions)": "data/Cyrielle/33_all.csv",
    "BDNB (bâtiments)": "data/Cyrielle/batiment_groupe_dpe_representatif_logement.csv",
    "FiLoSoFi (revenus)": "data/Cyrielle/BASE_TD_FILO_IRIS_2021_DEC.csv",
    "Densité de population": "data/Cyrielle/densite pop FR par commune 2021.csv",
    "Délinquance": "data/Cyrielle/delinquence.csv",
    "Transports": "data/Cyrielle/gtfs-stops-france-export-2024-02-01.csv",
    "BPE": "data/Cyrielle/bpe2023_gironde.csv",
    "OpenStreetMap": "data/Cyrielle/OSM_POI.csv",
    "Statistiques ventes": "data/Cyrielle/indicateurs.csv"
}

INIT_MAP = {
    "DVF géolocalisé (transactions)": False,
    "BDNB (bâtiments)": True,
    "FiLoSoFi (revenus)": True,
    "Densité de population": True,
    "Délinquance": False,
    "Transports": True,
    "BPE": True,
    "OpenStreetMap": True,
    "Statistiques ventes": False
}

# ---------------------------------------------------------------------
# 🧩 FONCTIONS UTILITAIRES
# ---------------------------------------------------------------------
def make_arrow_compatible(df: pd.DataFrame) -> pd.DataFrame:
    # Convert columns that PyArrow can't handle
    for col in df.columns:
        if df[col].dtype == 'object':
            # Try to convert to string to avoid serialization errors
            df[col] = df[col].astype(str)
        elif pd.api.types.is_categorical_dtype(df[col]):
            df[col] = df[col].astype(str)
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            # Remove timezone info if present
            df[col] = pd.to_datetime(df[col]).dt.tz_localize(None)
    return df

# @st.cache_data
def load_csv_auto(path, encoding="utf-8", nrows=None, init_map=True):
    """Charge un CSV en détectant automatiquement le séparateur."""
    if "path" in st.session_state and path != st.session_state["path"]:
        print('path changed, resetting map')
        if "m" in st.session_state:
            del st.session_state["m"]
    st.session_state["path"] = path

    if path == DATA_PATHS["OpenStreetMap"]:
        df = pd.read_csv(path, delimiter = "\t", on_bad_lines='warn', index_col='@id')
        df = df[
                (df["@lat"].between(42.72, 46.80)) &
                (df["@lon"].between(-1.79, 1.45))
            ]
    elif path == DATA_PATHS["Transports"]:
        df = pd.read_csv(path, usecols=["stop_lat", "stop_lon"], dtype=float)
    else:
        with open(path, 'r', encoding=encoding) as f:
            sample = f.read(4096)
            # Détection du séparateur dominant
            if '\t' in sample:
                sep = '\t'
            elif sample.count(';') > sample.count(','):
                sep = ';'
            else:
                sep = ','
        df = pd.read_csv(
            path,
            sep=sep,
            encoding=encoding,
            low_memory=False,
            na_values=["", " ", "None", "none", "NULL", "null", "NaN", "nan"],
            keep_default_na=True,
            nrows=nrows
        )

    df = make_arrow_compatible(df)
    
    possible_lat_cols = ["latitude", "lat", "y", "coord_y", "stop_lat", "LATITUDE"]
    possible_lon_cols = ["longitude", "lon", "x", "coord_x", "stop_lon", "LONGITUDE"]
    lat_col = next((col for col in possible_lat_cols if col in df.columns), None)
    lon_col = next((col for col in possible_lon_cols if col in df.columns), None)

    if init_map:
        if lat_col and lon_col:
            df_valid = df.dropna(subset=[lat_col, lon_col]).copy()
            df_valid[lat_col] = pd.to_numeric(df_valid[lat_col], errors="coerce")
            df_valid[lon_col] = pd.to_numeric(df_valid[lon_col], errors="coerce")
            if "m" not in st.session_state:
                lat_mean = df_valid[lat_col].mean()
                lon_mean = df_valid[lon_col].mean()
                m = folium.Map(location=[lat_mean, lon_mean], zoom_start=9)
                for _, row in df_valid.sample(min(500, len(df_valid))).iterrows():
                    folium.CircleMarker(
                        [row[lat_col], row[lon_col]],
                        radius=4, color="blue", fill=True, fill_opacity=0.6
                    ).add_to(m)
                st.session_state["m"] = m
    return df, lat_col, lon_col


def show_styled_df(df, max_col_px=380):
    """
    Affiche un DataFrame stylé avec une colonne 'N°' (index + 1),
    sans afficher l'index natif de pandas.
    """
    # On crée une colonne 'N°' à partir de l'index + 1
    df_display = df.reset_index(drop=True).copy()
    df_display.insert(0, "N°", range(1, len(df_display) + 1))

    # Style du tableau
    styler = df_display.style.set_table_styles([
        {"selector": "th", "props": [("text-align", "left"), ("padding", "6px 8px")]},
        {"selector": "td", "props": [
            ("white-space", "normal"),
            ("word-wrap", "break-word"),
            ("max-width", f"{max_col_px}px"),
            ("padding", "6px 8px"),
            ("vertical-align", "top")
        ]},
        {"selector": "thead th:first-child", "props": [("text-align", "center")]},
        {"selector": "tbody td:first-child", "props": [("text-align", "center"), ("font-weight", "600")]}
    ])

    # Affichage Streamlit sans l’index
    st.markdown(styler.hide(axis="index").to_html(), unsafe_allow_html=True)

# PAGE PRINCIPALE
def affiche():
    st.title("Exploration des données")
 
    tab1, tab2 = st.tabs(["📚 Synthèse des bases", "🔎 Exploration des bases retenues"])

    # Onglet 1 : Synthèse
    with tab1:
        st.markdown("""
        Projet proposé par l'équipe :

        ➡️ Sans données fournies par DataScientest  
        ➡️ Recherche et exploration de données open source  
        ➡️ Sélection finale : ~20 fichiers
        """)
        
        st.header("Méthodologie")
        st.image(os.path.join("images", "Diag1.png"))

        st.subheader("✅ Bases retenues dans la modélisation")
        show_styled_df(BASES_RETENUES)
        # show_styled_df(BASES_RETENUES.reset_index(drop=True).rename_axis("N°").rename(index=lambda x: x + 1))

        st.subheader("❌ Bases non retenues dans la modélisation")
        show_styled_df(BASES_NON_RETENUES)
        # show_styled_df(BASES_NON_RETENUES.reset_index(drop=True).rename_axis("N°").rename(index=lambda x: x + 1))


   # --- SECTION 2 : EXPLORATION INTERACTIVE ---

    with tab2:
        selected_name = st.selectbox("📂 Choisir une base :", list(DATA_PATHS.keys()))
        path = DATA_PATHS[selected_name]
        
        with st.spinner(f"Chargement de {selected_name}..."):
            df, lat_col, lon_col = load_csv_auto(path, init_map=INIT_MAP[selected_name])

        st.success(f"{selected_name} chargée ({df.shape[0]:,} lignes × {df.shape[1]} colonnes)")
        st.write("### Aperçu des données")

        df = df.replace({
            None: pd.NA,
            "None": pd.NA,
            "none": pd.NA,
            "NaN": pd.NA,
            "nan": pd.NA,
            "": pd.NA
        })

        # df_display = df.fillna({col: "" for col in df.select_dtypes(include="object").columns})
        df_display = df.fillna("")
        st.dataframe(df_display.head(10), hide_index=True)

        # --- Sous-onglets
        t1, t2, t3, t4 = st.tabs([
            "📊 Statistiques descriptives",
            "🕳️ Valeurs manquantes",
            "🔍 Filtrage par commune",
            "🗺️ Mini-carte",
        ])

        # --- Statistiques descriptives
        with t1:
            # Statistiques descriptives (toutes colonnes)
            df_describe = df.describe(include="all").fillna("")

            #Suppression des lignes non pertinentes pour les variables non numériques
            df_describe = df_describe.drop(index=["top", "unique", "freq"], errors="ignore")

            # Transposition pour lecture plus intuitive
            st.dataframe(df_describe.T, use_container_width=True)


        # --- Valeurs manquantes
        with t2:
            missing = df.isna().sum()
            missing = missing[missing > 0].sort_values(ascending=False)
            if missing.empty:
                st.success("✅ Aucune valeur manquante détectée.")
            else:
                df_missing = pd.DataFrame({
                    "Colonnes": missing.index,
                    "Valeurs manquantes": missing.values,
                    "% du total": (missing / len(df) * 100).round(2)
                })
                st.dataframe(df_missing, hide_index=True)
                fig = px.bar(
                    df_missing,
                    x="Colonnes", y="% du total",
                    title="Taux de valeurs manquantes",
                    labels={"% du total": "% de valeurs manquantes"},
                    template="plotly_white"
                )
                st.plotly_chart(fig, use_container_width=True)

        # --- Filtrage par commune
        with t3:
            possible_cols = ["commune", "nom_commune", "libelle_commune", "code_commune",
                            "codgeo", "CODGEO_2024", "libgeo", "code_insee", "INSEE_COM"]
            geo_cols = [col for col in possible_cols if col in df.columns]

            if geo_cols:
                col_geo = st.selectbox("Choisir la colonne géographique :", geo_cols)
                valeurs = sorted(df[col_geo].dropna().unique())
                if len(valeurs) > 2000:
                    recherche = st.text_input(f"Rechercher une valeur dans '{col_geo}' :")
                    if recherche:
                        subset = df[df[col_geo].astype(str).str.contains(recherche, case=False, na=False)]
                        st.dataframe(subset.head(20), hide_index=True)
                    else:
                        st.info("Saisissez une valeur pour filtrer.")
                else:
                    valeur = st.selectbox(f"Choisir une valeur dans '{col_geo}' :", valeurs)
                    st.dataframe(df[df[col_geo] == valeur].head(20), hide_index=True)
            else:
                st.info("Aucune colonne géographique détectée.")

        # --- Mini-carte

        with t4:

            # Cas : Statistiques ventes
            if selected_name == "Statistiques ventes":
                commune_cols = [c for c in ["INSEE_COM", "code_insee", "codgeo"] if c in df.columns]
                if not commune_cols:
                    st.warning("Aucune colonne géographique trouvée.")
                    st.stop()
                col_commune = commune_cols[0]
                df[col_commune] = df[col_commune].astype(str).str.zfill(5)

                # Filtre année
                if "Annee" in df.columns:
                    annees = sorted(df["Annee"].dropna().unique())
                    annee_sel = st.selectbox("📅 Choisir une année :", annees)
                    df = df[df["Annee"] == annee_sel]

                labels_vars = {
                    "Nb_mutations": "Nombre de mutations",
                    "NbMaisons": "Maisons vendues",
                    "NbApparts": "Appartements vendus",
                    "propmaison": "Proportion de maisons",
                    "propappart": "Proportion d'appartements",
                    "PrixMoyen": "Prix moyen (€)",
                    "Prixm2Moyen": "Prix moyen au m² (€)",
                    "SurfaceMoy": "Surface moyenne (m²)"
                }

                variables = [c for c in labels_vars.keys() if c in df.columns]
                label_sel = st.selectbox("📊 Variable :", [labels_vars[c] for c in variables])
                variable = {v: k for k, v in labels_vars.items()}[label_sel]

                palette = st.selectbox("🎨 Choisir une palette :", ["YlGnBu", "YlOrRd", "PuBu", "BuPu", "RdPu"])

                geojson_path = "data/Cyrielle/communes-33-gironde.geojson"
                with open(geojson_path, encoding="utf-8") as f:
                    geojson_data = json.load(f)

                m = folium.Map(location=[44.8, -0.6], zoom_start=8, tiles="cartodb positron")
                folium.Choropleth(
                    geo_data=geojson_data,
                    data=df,
                    columns=[col_commune, variable],
                    key_on="feature.properties.code",
                    fill_color=palette,
                    fill_opacity=0.8,
                    line_opacity=0.3,
                    nan_fill_color="lightgrey",
                    legend_name=label_sel
                ).add_to(m)

                # Fusion des valeurs pour afficher la variable également
                df_tooltip = df[[col_commune, variable]].set_index(col_commune).to_dict()[variable]
                for feature in geojson_data["features"]:
                    code = feature["properties"]["code"]
                    value = df_tooltip.get(code)
                    if value is not None and not pd.isna(value):
                        feature["properties"]["Valeur"] = round(value, 2)
                    else:
                        feature["properties"]["Valeur"] = "NA"

                folium.GeoJson(
                    geojson_data,
                    style_function=lambda feature: {
                        "fillOpacity": 0,
                        "color": "transparent",
                        "weight": 0
                    },
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=["nom", "code", "Valeur"],
                        aliases=["Commune :", "Code INSEE :", f"{label_sel} :"],
                        localize=True,
                        sticky=True,
                        labels=True,
                        style=("background-color: white; color: #333; "
                            "font-size: 12px; padding: 5px; border-radius: 4px;")
                    )
                ).add_to(m)

                st_folium(m, width=850, height=600)

            # Cas : Délinquance
            elif selected_name == "Délinquance":

                commune_cols = [c for c in ["code_insee", "codgeo", "INSEE_COM", "CODGEO_2024"] if c in df.columns]
                if not commune_cols:
                    st.warning("Aucune colonne de code commune trouvée.")
                    st.stop()
                col_commune = commune_cols[0]
                df[col_commune] = df[col_commune].astype(str).str.zfill(5)

                # Filtre indicateur
                if "indicateur" in df.columns:
                    indicateurs = sorted(df["indicateur"].dropna().unique())
                    indicateur_sel = st.selectbox("🧩 Choisir un indicateur :", indicateurs)
                    df = df[df["indicateur"] == indicateur_sel]

                # Filtre unité
                unite_col = "unite_de_compte" if "unite_de_compte" in df.columns else "unité_de_compte"
                if unite_col in df.columns:
                    unites = sorted(df[unite_col].dropna().unique())
                    unite_sel = st.selectbox("⚖️ Unité de compte :", unites)
                    df = df[df[unite_col] == unite_sel]

                # Filtre type d'information
                indicateurs_possibles = ["nombre", "taux_pour_mille", "complement_info_nombre", "complement_info_taux"]
                indicateurs_existants = [v for v in indicateurs_possibles if v in df.columns]

                if not indicateurs_existants:
                    st.warning("Aucune colonne exploitable trouvée (nombre / taux...).")
                    st.stop()

                label_sel = st.selectbox("📊 Choisir la variable :", indicateurs_existants)
                variable = label_sel

                # Conversion en numérique
                df[variable] = df[variable].astype(str).str.replace(",", ".", regex=False)
                df[variable] = pd.to_numeric(df[variable], errors="coerce")

                if df[variable].notna().sum() == 0:
                    st.warning(f"Aucune donnée disponible pour la combinaison : {indicateur_sel} × {unite_sel}.")
                    st.stop()

                palette = st.selectbox("🎨 Choisir une palette :", ["YlOrRd", "PuBu", "BuPu", "RdPu", "YlGnBu"])

                geojson_path = "data/Cyrielle/communes-33-gironde.geojson"
                with open(geojson_path, encoding="utf-8") as f:
                    geojson_data = json.load(f)

                m = folium.Map(location=[44.8, -0.6], zoom_start=8, tiles="cartodb positron")
                folium.Choropleth(
                    geo_data=geojson_data,
                    data=df,
                    columns=[col_commune, variable],
                    key_on="feature.properties.code",
                    fill_color=palette,
                    fill_opacity=0.8,
                    line_opacity=0.3,
                    nan_fill_color="lightgrey",
                    legend_name=f"{variable} ({unite_sel})"
                ).add_to(m)

            # --- Ajout de la couche GeoJson avec infobulle ---
                df_tooltip = df[[col_commune, variable]].set_index(col_commune).to_dict()[variable]
                for feature in geojson_data["features"]:
                    code = feature["properties"]["code"]
                    value = df_tooltip.get(code)
                    if value is not None and not pd.isna(value):
                        feature["properties"]["Valeur"] = round(value, 2)
                    else:
                        feature["properties"]["Valeur"] = "NA"

                folium.GeoJson(
                    geojson_data,
                    style_function=lambda feature: {
                        "fillOpacity": 0,
                        "color": "transparent",
                        "weight": 0
                    },
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=["nom", "code", "Valeur"],
                        aliases=["Commune :", "Code INSEE :", f"{label_sel} :"],
                        localize=True,
                        sticky=True,
                        labels=True,
                        style=("background-color: white; color: #333; "
                            "font-size: 12px; padding: 5px; border-radius: 4px;")
                    )
                ).add_to(m)

                # --- Affichage ---

                st_folium(m, width=850, height=600)
                st.caption("🟣 Les zones grisées indiquent des données manquantes (NA).")


            
            # Cas : DVF géolocalisé
            elif selected_name == "DVF géolocalisé (transactions)":

                # --- Nettoyage des coordonnées
                df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
                df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
                df = df.dropna(subset=["latitude", "longitude"])

                # --- Nettoyage des colonnes clés
                df["valeur_fonciere"] = pd.to_numeric(df["valeur_fonciere"], errors="coerce")
                df["surface_reelle_bati"] = pd.to_numeric(df["surface_reelle_bati"], errors="coerce")
                df["nombre_pieces_principales"] = pd.to_numeric(df["nombre_pieces_principales"], errors="coerce")


                # Carte choroplèthe - Nb ventes par commune
                st.subheader("🧭 Nombre de ventes par commune (Gironde)")

                geojson_path = "data/Cyrielle/communes-33-gironde.geojson"

                if os.path.exists(geojson_path):
                    with open(geojson_path, "r", encoding="utf-8") as f:
                        geojson_gironde = json.load(f)

                    # Vérifie le bon champ d'identifiant (ex: "code" ou "id")
                    # Ici on suppose que le champ INSEE est dans "code"
                    ventes_par_commune = (
                        df["code_commune"].astype(str).value_counts().reset_index()
                    )
                    ventes_par_commune.columns = ["code_commune", "nb_ventes"]

                    fig_choro = px.choropleth_mapbox(
                        ventes_par_commune,
                        geojson=geojson_gironde,
                        locations="code_commune",
                        featureidkey="properties.code",  # ⚠️ adapte ce champ selon ton geojson !
                        color="nb_ventes",
                        color_continuous_scale="Oranges",
                        mapbox_style="carto-positron",
                        zoom=8,
                        center={"lat": 44.84, "lon": -0.58},
                        hover_data=["nb_ventes"],
                        title="Nombre de ventes immobilières par commune (filtrées)"
                    )
                    fig_choro.update_layout(
                        height=800,
                        margin=dict(l=0, r=0, t=30, b=0)
                    )

                    st.plotly_chart(fig_choro, use_container_width=True)


            # Cas : Densité de la population
            elif selected_name == "Densité de population":

                geojson_path = "data/Cyrielle/communes-33-gironde.geojson"
                data_path = "data/Cyrielle/densite pop FR par commune 2021.csv"

                # --- Vérification de la présence des fichiers
                if not os.path.exists(geojson_path):
                    st.warning("Fichier GeoJSON introuvable.")
                    st.stop()

                if not os.path.exists(data_path):
                    st.warning("Fichier de données de population introuvable.")
                    st.stop()

                # --- Lecture des fichiers
                with open(geojson_path, "r", encoding="utf-8") as f:
                    geojson_gironde = json.load(f)

                df_pop = pd.read_csv(data_path, dtype={"code_commune": str})

                # Vérifie la présence des colonnes attendues
                colonnes_attendues = {"codgeo", "dens_pop"}
                if not colonnes_attendues.issubset(df_pop.columns):
                    st.error(f"Le fichier CSV doit contenir les colonnes : {colonnes_attendues}")
                    st.stop()

                # --- Choix de la palette
                palettes = {
                    "Oranges": "Oranges",
                    "Viridis": "Viridis",
                    "Plasma": "Plasma",
                    "Cividis": "Cividis",
                    "Blues": "Blues",
                    "Greens": "Greens",
                    "RdBu": "RdBu",
                    "YlGnBu": "YlGnBu",
                    "Inferno": "Inferno",
                }
                palette_choisie = st.selectbox(
                    "🎨 Choisir une palette de couleurs",
                    list(palettes.keys()),
                    index=1
                )

                # --- Construction de la carte
                fig_densite = px.choropleth_mapbox(
                    df_pop,
                    geojson=geojson_gironde,
                    locations="codgeo",
                    featureidkey="properties.code", 
                    color="dens_pop",
                    color_continuous_scale=palettes[palette_choisie],
                    mapbox_style="carto-positron",
                    zoom=8,
                    center={"lat": 44.84, "lon": -0.58},
                    hover_data={
                        "dens_pop": ":.1f"
                    },
                    title=f"Densité de la population par commune (palette : {palette_choisie})"
                )

                fig_densite.update_layout(
                    height=800,
                    margin=dict(l=0, r=0, t=30, b=0)
                )

                st.plotly_chart(fig_densite, use_container_width=True)

            # Cas : Transports — Carte des arrêts
            elif selected_name == "Transports":
                if not os.path.exists(DATA_PATHS[selected_name]):
                    st.warning("❌ Fichier des arrêts de transport introuvable.")
                    st.stop()

                df_arrets = df.copy()
                df_arrets = df_arrets[
                    (df_arrets["stop_lat"].between(42.72, 46.80)) &
                    (df_arrets["stop_lon"].between(-1.79, 1.45))
                ]


                # Carte centrée sur Bordeaux pour éviter écran noir
                view_state = pdk.ViewState(
                    latitude=44.84,
                    longitude=-0.58,
                    zoom=7,
                    pitch=0
                )

                # ScatterLayer (points)
                layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=df_arrets,
                    get_position='[stop_lon, stop_lat]',
                    get_radius=80, 
                    radius_min_pixels=3, 
                    radius_max_pixels=30, 
                    pickable=False
                )

                r = pdk.Deck(
                    layers=[layer],
                    initial_view_state=view_state,
                    map_provider="carto", 
                    map_style="light"    
                )

                st.pydeck_chart(r)
                st.success(f"✅ {len(df_arrets):,} arrêts transport affichés en Nouvelle-Aquitaine")
           
            elif selected_name == "OpenStreetMap":

                # Carte centrée sur Bordeaux pour éviter écran noir
                view_state = pdk.ViewState(
                    latitude=44.84,
                    longitude=-0.58,
                    zoom=7,
                    pitch=0
                )

                # ScatterLayer (points)
                layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=df,
                    get_position='[@lon, @lat]',
                    get_radius=80, 
                    radius_min_pixels=3, 
                    radius_max_pixels=30, 
                    pickable=False
                )

                r = pdk.Deck(
                    layers=[layer],
                    initial_view_state=view_state,
                    map_provider="carto", 
                    map_style="light"    
                )

                st.pydeck_chart(r)
                st.success(f"✅ {len(df):,} points d'intérêt affichés en Nouvelle-Aquitaine")
             
            elif lat_col and lon_col:
                if "m" in st.session_state:
                    st_folium(st.session_state["m"], width=850, height=600)
            else:
                st.info("Aucune carte disponible pour cette base.")