"""
code de la page

"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import plotly.express as px
import json
import os
from tools import *

def affiche():
    

    from pathlib import Path

    # --------------------------------------------------
    # ⚙️ Configuration de la page
    # --------------------------------------------------
    st.set_page_config(page_title="Sunburst enrichi - Gironde", layout="wide")
    st.title("Datavisualisation de la base des ventes immobilières au sein de la Gironde")
    tab1, tab2 = st.tabs(["📚 Visualisation globale de la base", "🔎 Exploration détaillée"])

    # --------------------------------------------------
    # 📥 Chargement et préparation des données
    # --------------------------------------------------

    def load_main_data(path):
        df = pd.read_csv(path, low_memory=False)
        df = df.dropna(subset=["code_commune_1", "type_bien", "nombre_pieces_principales_1", "DPE_1"])
        df["code_commune_1"] = df["code_commune_1"].astype(str).str.zfill(5)

        # Normalisation types et valeurs numériques
        df["valeur_fonciere_1"] = df["valeur_fonciere_1"].astype(str).str.replace(",", ".", regex=False)
        df["valeur_fonciere_1"] = pd.to_numeric(df["valeur_fonciere_1"], errors="coerce").fillna(0.0)
        df["surface_terrain_1"] = pd.to_numeric(df["surface_terrain_1"], errors="coerce").fillna(0.0)

        # Catégorisation : présence de terrain
        df["presence_terrain"] = np.where(df["surface_terrain_1"] > 0, "Avec terrain", "Sans terrain")

        # Types de locaux explicites
        df["code_type_local_1"] = df["code_type_local_1"].replace({
            1.0: "Maisons",
            2.0: "Appartements"
        }).fillna("Autre")

        # Normalisation DPE
        df["DPE_1"] = df["DPE_1"].astype(str).str.upper().replace({"NAN": "Non renseigné"})

        return df


    df_main = load_main_data("data/Cyrielle/df_ok_nan_adresse_POItot.csv")


    # --------------------------------------------------
    # 🧮 Agrégation des données (option 1 : count size)
    # --------------------------------------------------
    group_cols = [
        "nom_commune_1",
        "code_commune_1",
        "code_type_local_1",
        "presence_terrain",
        "nombre_pieces_principales_1",
        "DPE_1"
    ]

    df_sunburst = (
        df_main.groupby(group_cols, dropna=False)
        .agg(
            nb_mutations=("id_mutation", "size"),  # ✅ chaque ligne = 1 mutation
            valeur_totale=("valeur_fonciere_1", "sum")
        )
        .reset_index()
    )

    df_sunburst["nb_mutations"] = df_sunburst["nb_mutations"].astype(int)
    df_sunburst["DPE_label"] = "DPE : " + df_sunburst["DPE_1"].astype(str)
    df_sunburst["Pieces_label"] = "Pièces : " + df_sunburst["nombre_pieces_principales_1"].astype(str)

  
    # --------------------------------------------------
    # 🌇 Sunburst Bordeaux vs Autres communes
    # --------------------------------------------------

    with tab1:
        col1, col2 = st.columns(2)

        palette_bdx = ["#5E0B15", "#8B1E3F", "#A93C6E", "#C76D99", "#E89BB8", "#F2C4D3"]
        palette_autres = ["#003049", "#126782", "#468FAF", "#7FB3C8", "#A9CFE0", "#D1E7F0"]
        palette_sel = ["#14532D", "#1E6F3F", "#278C54", "#4FAE73", "#7FC896", "#A8E0B7"]

        with col1:
            df_bordeaux = df_sunburst[df_sunburst["code_commune_1"] == "33063"]
            if not df_bordeaux.empty:
                fig_bdx = px.sunburst(
                    df_bordeaux,
                    path=[
                        "nom_commune_1",
                        "code_type_local_1",
                        "presence_terrain",
                        "Pieces_label",
                        "DPE_1"
                    ],
                    values="nb_mutations",
                    color="code_type_local_1",
                    color_discrete_sequence=palette_bdx,
                    title="🏙️ Bordeaux — Nombre de mutations",
                    width=500,
                    height=500,
                    hover_data={
                        "nb_mutations": True,
                        "valeur_totale": False,
                        "code_type_local_1": False,
                        "presence_terrain": False,
                        "Pieces_label": False,
                        "DPE_label": False
                    }                
                )
                fig_bdx.update_layout(height=700)
                st.plotly_chart(fig_bdx, use_container_width=True)
            else:
                st.warning("Aucune donnée trouvée pour Bordeaux (33063).")

        with col2:
            df_autres = df_sunburst[df_sunburst["code_commune_1"] != "33063"]
            if not df_autres.empty:
                fig_autres = px.sunburst(
                    df_autres,
                    path=["code_type_local_1", "presence_terrain", "Pieces_label", "DPE_1"],
                    values="nb_mutations",
                    color="code_type_local_1",
                    color_discrete_sequence=palette_autres,
                    title="🌍 Autres communes — Répartition des mutations",
                    width=500,
                    height=500,
                    hover_data={
                        "nb_mutations": True,
                        "valeur_totale": False,
                        "code_type_local_1": False,
                        "presence_terrain": False,
                        "Pieces_label": False,
                        "DPE_label": False
                    }                      
                )
                fig_autres.update_layout(height=700)
                st.plotly_chart(fig_autres, use_container_width=True)
            else:
                st.warning("Aucune donnée disponible pour les autres communes.")


        # --------------------------------------------------
        # 🧭 Sélecteur : Sunburst par commune
        # --------------------------------------------------
        st.markdown("---")
        st.subheader("🔍 Visualisation par commune")

        communes = sorted(df_sunburst["nom_commune_1"].dropna().unique())
        commune_sel = st.selectbox("Choisir une commune :", communes, index=0)

        df_commune = df_sunburst[df_sunburst["nom_commune_1"] == commune_sel]

        if df_commune.empty:
            st.warning("Aucune donnée disponible pour cette commune.")
        else:
            fig_commune = px.sunburst(
                df_commune,
                path=[
                    "nom_commune_1",
                    "code_type_local_1",
                    "presence_terrain",
                    "Pieces_label",
                    "DPE_1"
                ],
                values="nb_mutations",
                color="code_type_local_1",
                color_discrete_sequence=palette_sel,
                title=f"Structure des ventes à {commune_sel}",
                width=800,
                height=700,
                    hover_data={
                        "nb_mutations": True,
                        "valeur_totale": False,
                        "code_type_local_1": False,
                        "presence_terrain": False,
                        "Pieces_label": False,
                        "DPE_label": False
                    }                  
            )
            st.plotly_chart(fig_commune, use_container_width=True)
        
    
    with tab2:
    
        # ================================
        # --- Page 2 : Illustrations
        # ================================
        def page2_visualisations():

            # Chargement des données
            df = pd.read_csv("data/Cyrielle/df_ok_nan_adresse_POItot.csv", index_col=0)
            df = df.drop(columns=["Unnamed: 0"], errors="ignore")

            tab1, tab2 = st.tabs(["📊 Visualisations principales", "🗺️ Cartes et analyses géographiques"])

            # ============================================================
            # --- TAB 1 : VISUALISATIONS PRINCIPALES
            # ============================================================
            with tab1:
                st.header("📈 Distribution et caractéristiques des ventes")


                col1, col2 = st.columns(2)
                # Histogramme
                with col1:
                    st.subheader("Distribution des valeurs foncières")
                    fig1, ax1 = plt.subplots(figsize=(5, 3))
                    sns.histplot(df['valeur_fonciere_1'], bins=100, kde=True, ax=ax1)
                    
                    # Titres et labels plus petits
                    ax1.set_title("Distribution des valeurs foncières", fontsize=8)
                    ax1.set_xlabel("Valeur foncière (€)", fontsize=6)
                    ax1.set_ylabel("Nombre de ventes", fontsize=6)
                    
                    # Taille des ticks (graduations)
                    ax1.tick_params(axis='x', labelsize=6)
                    ax1.tick_params(axis='y', labelsize=6)
                    fig1.tight_layout()
                    st.pyplot(fig1)

                with col2:                

                # Histogramme coloré par type de bien
                    st.subheader("Distribution des prix selon le type de bien")
                    if "type_bien" in df.columns:
                        fig3, ax3 = plt.subplots(figsize=(5, 3))
                        sns.histplot(
                            data=df,
                            x="valeur_fonciere_1",
                            bins=50,
                            hue="type_bien",
                            palette={"Maison": "orange", "Appartement": "blue"},
                            ax=ax3
                        )
                        ax3.set_title("Distribution des prix selon le type de bien", fontsize=8)
                        ax3.set_xlabel("Valeur foncière (€)", fontsize=6)
                        ax3.set_ylabel("Nombre de transactions", fontsize=6)
                        ax3.tick_params(axis='x', labelsize=6)
                        ax3.tick_params(axis='y', labelsize=6)
                        ax3.get_legend().remove()

                        import matplotlib.patches as mpatches
                        legendes = [
                            mpatches.Patch(color="orange", label="Maisons"),
                            mpatches.Patch(color="blue", label="Appartements")
                        ]
                        ax3.legend(
                            handles=legendes,
                            title="Type de bien immobilier",
                            title_fontsize=6,
                            fontsize=5,
                            loc="upper right",
                            frameon=False
                        )

                        fig3.tight_layout()
                        st.pyplot(fig3)
                    st.divider()

                col1, col2 = st.columns(2)
                # Boxplot par type de bien 
                with col1:                   
                    st.subheader("Valeur foncière par type de bien")

                    # On définit une palette cohérente avec les autres graphiques
                    palette = {"Maison": "orange", "Appartement": "blue"}

                    # On s'assure que les valeurs sont bien écrites comme attendu
                    df_plot = df.copy()
                    df_plot["type_bien"] = df_plot["type_bien"].str.strip().str.capitalize()

                    fig2, ax2 = plt.subplots(figsize=(5, 3))
                    sns.boxplot(
                        data=df_plot,
                        y="type_bien",
                        x="valeur_fonciere_1",
                        hue="type_bien",          # 👈 pour colorer selon le type de bien
                        palette=palette,          # 👈 couleurs cohérentes
                        dodge=False,              # 👈 un seul box par catégorie
                        ax=ax2
                    )

                    # Nettoyage et ajustement
                    ax2.set_title("Valeur foncière par type de bien", fontsize=8)
                    ax2.set_ylabel("Type de bien", fontsize=6)
                    ax2.set_xlabel("Valeur foncière (€)", fontsize=6)
                    ax2.tick_params(axis='x', labelsize=6)
                    ax2.tick_params(axis='y', labelsize=6)

                    fig2.tight_layout()
                    st.pyplot(fig2)

                col1, col2 = st.columns(2)

                # Répartition DPE
                with col1:
                    st.subheader("Répartition des transactions par classe DPE et GES")
                    dpe_counts = df["DPE_1"].value_counts().reindex(list("ABCDEFG"))
                    fig4, ax4 = plt.subplots(figsize=(6, 4))
                    dpe_counts.plot(kind="bar", color="skyblue", edgecolor="black", ax=ax4)
                    ax4.set_xlabel("Classe DPE")
                    ax4.set_ylabel("Nombre de transactions")
                    ax4.set_title("Répartition des transactions par classe DPE")
                    st.pyplot(fig4)

                # Répartition GES
                with col2:
                    st.subheader("")
                    ges_counts = df["GES_1"].value_counts().reindex(list("ABCDEFG"))
                    fig5, ax5 = plt.subplots(figsize=(6, 4))
                    ges_counts.plot(kind="bar", color="lightcoral", edgecolor="black", ax=ax5)
                    ax5.set_xlabel("Classe GES")
                    ax5.set_ylabel("Nombre de transactions")
                    ax5.set_title("Répartition des transactions par classe GES")
                    st.pyplot(fig5)

                # Boxplots DPE et GES
                st.subheader("Valeur foncière selon DPE et GES")
                col1, col2 = st.columns(2)

                with col1:
                    fig6, ax6 = plt.subplots(figsize=(6, 4))
                    sns.boxplot(x="DPE_1", y="valeur_fonciere_1", data=df,
                                order=list("ABCDEFG"), palette="Blues", ax=ax6)
                    ax6.set_title("Valeur foncière par classe DPE")
                    st.pyplot(fig6)

                with col2:
                    fig7, ax7 = plt.subplots(figsize=(6, 4))
                    sns.boxplot(x="GES_1", y="valeur_fonciere_1", data=df,
                                order=list("ABCDEFG"), palette="Reds", ax=ax7)
                    ax7.set_title("Valeur foncière par classe GES")
                    st.pyplot(fig7)


                col1, col2 = st.columns(2)

                with col1:
                    # Tableau croisé DPE / GES
                    st.subheader("Croisement des classes DPE et GES")
                    table_dpe_ges = pd.crosstab(df["DPE_1"], df["GES_1"]).reindex(index=list("ABCDEFG"), columns=list("ABCDEFG"))
                    fig8, ax8 = plt.subplots(figsize=(8, 6))
                    sns.heatmap(table_dpe_ges, annot=True, fmt="d", cmap="YlGnBu", ax=ax8)
                    ax8.set_title("Croisement des classes DPE et GES")
                    st.pyplot(fig8)

                    st.divider()


                col1, col2 = st.columns(2)

                with col1:
                    # POI Heatmap
                    st.subheader("Accessibilité des biens par catégorie et distance")
                    categories = {
                        "Santé": ["Médecins généralistes", "Paramédical", "Spécialistes – Médical", "Établissements et services de santé"],
                        "Éducation": ["Écoles, collèges, lycées", "Enseignement supérieur", "Formation continue"],
                        "Commerces": ["Commerces alimentaires", "Grandes surfaces", "Station-service"],
                        "Transports": ["Transports en commun", "Trains et autres transports", "Aéroport"],
                        "Loisirs": ["Parcs", "Sports, loisirs et culture", "Tourisme", "Patrimoine"],
                        "Services publics": ["Mairie", "Police et Gendarmerie", "Déchetterie", "Services funéraires"]
                    }

                    res = []
                    for cat, poi_list in categories.items():
                        for dist in ["50m", "500m", "2km", "10km"]:
                            cols = [f"{poi}_moins_{dist}" for poi in poi_list if f"{poi}_moins_{dist}" in df.columns]
                            if cols:
                                nb = (df[cols].sum(axis=1) > 0).sum()
                                res.append([cat, dist, nb])

                    if res:
                        heatmap_df = pd.DataFrame(res, columns=["Categorie", "Distance", "Nb_biens"])
                        pivot = heatmap_df.pivot(index="Categorie", columns="Distance", values="Nb_biens")

                        fig9, ax9 = plt.subplots(figsize=(6, 4))
                        sns.heatmap(pivot, annot=True, fmt="d", cmap="YlGnBu", ax=ax9)
                        ax9.set_title("Accessibilité des biens par catégorie de services et distances")
                        st.pyplot(fig9)

            # ============================================================
            # --- TAB 2 : CARTES
            # ============================================================
            with tab2:
                st.header("🗺️ Cartographie des ventes immobilières")

                # Carte interactive des ventes
                st.subheader("Localisation des ventes et valeur foncière")
                fig_map = px.scatter_mapbox(
                    df,
                    lat="latitude_1",
                    lon="longitude_1",
                    color="valeur_fonciere_1",
                    size="surface_reelle_bati_1",
                    hover_name="adresse_complete_1",
                    color_continuous_scale=px.colors.sequential.Viridis,
                    zoom=9,
                    mapbox_style="open-street-map",
                    title="Localisation des biens et valeur foncière"
                )
                st.plotly_chart(fig_map, use_container_width=True)

                # --- Choropleth Gironde
                st.subheader("Nombre de ventes immobilières par commune")
                shapefile_path = os.path.join(
                    "..", "..", "data", "staging", "shapefiles", "communes_gironde.shp"
                )

                if os.path.exists(shapefile_path):
                    gironde = gpd.read_file(shapefile_path)
                    if gironde.crs.to_epsg() != 4326:
                        gironde = gironde.to_crs(epsg=4326)

                    gironde["INSEE_COM"] = gironde["INSEE_COM"].astype(str)
                    ventes_par_commune = (
                        df["code_commune_1"].astype(str).value_counts().reset_index()
                    )
                    ventes_par_commune.columns = ["code_commune_1", "nb_ventes"]
                    gironde = gironde.merge(
                        ventes_par_commune,
                        left_on="INSEE_COM",
                        right_on="code_commune_1",
                        how="left"
                    )
                    gironde["nb_ventes"] = gironde["nb_ventes"].fillna(0)
                    gironde["nb_ventes_log"] = np.log1p(gironde["nb_ventes"])

                    geojson_gironde = json.loads(gironde.to_json())
                    ticks = [0, 10, 100, 1000, 5000]
                    tickvals = np.log1p(ticks)
                    ticktext = [str(v) for v in ticks]

                    fig_choro = px.choropleth_mapbox(
                        gironde,
                        geojson=geojson_gironde,
                        locations="INSEE_COM",
                        color="nb_ventes_log",
                        hover_name="NOM",
                        hover_data={"nb_ventes": True, "nb_ventes_log": False},
                        color_continuous_scale="Oranges",
                        mapbox_style="carto-positron",
                        zoom=8,
                        center={"lat": 44.84, "lon": -0.58},
                        height=1200,
                        title="Nombre de ventes immobilières par commune"
                    )
                    fig_choro.update_coloraxes(
                        colorbar_tickvals=tickvals,
                        colorbar_ticktext=ticktext,
                        colorbar_title="Nb ventes"
                    )

                    fig_choro.update_layout(
                        height=1200,  # 👈 hauteur forcée
                        margin=dict(l=0, r=0, t=30, b=0)
                    )

                    st.plotly_chart(fig_choro, use_container_width=True, height=1200)

                # --- Top 20 communes
                st.subheader("Top 20 des communes avec le plus de ventes")
                col1, col2 = st.columns([2, 1])

                with col1:
                    top_communes = df["nom_commune_1"].value_counts().head(20)
                    fig10, ax10 = plt.subplots(figsize=(10, 5))
                    sns.barplot(
                        x=top_communes.values,
                        y=top_communes.index,
                        ax=ax10,
                        palette=sns.color_palette("viridis", n_colors=len(top_communes))  # 👈 une couleur par barre
                    )
                    ax10.set_title("Top 20 des communes avec le plus de transactions")
                    ax10.set_xlabel("Nombre de transactions")
                    ax10.set_ylabel("Commune")
                    st.pyplot(fig10)


        # --- Appel principal
        st.set_page_config(page_title="Exploration et Cartographie", layout="wide")
        page2_visualisations()

    
        # # --------------------------------------------------
        # # 🧩 Chargement des données
        # # --------------------------------------------------
        # @st.cache_data
        # def load_main_data(path):
        #     df = pd.read_csv(path, low_memory=False)
        #     df = df.dropna(subset=["code_commune_1", "type_bien"])
        #     df["code_commune_1"] = df["code_commune_1"].astype(str).str.zfill(5)
        #     return df

        # @st.cache_data
        # def load_dvf_data(folder_path):
        #     """Charge et concatène les fichiers dvf2020.csv à dvf2024.csv pour la Gironde (INSEE_COM commençant par '33')."""
        #     dfs = []
        #     for year in range(2020, 2025):
        #         file_path = Path(folder_path) / ("dvf" + str(year) + ".csv")
        #         if file_path.exists():
        #             df_y = pd.read_csv(file_path, low_memory=False)
        #             # Vérification de la présence du code INSEE
        #             if "INSEE_COM" in df_y.columns:
        #                 df_y["INSEE_COM"] = df_y["INSEE_COM"].astype(str).str.zfill(5)
        #                 # Filtre sur la Gironde (codes commençant par 33)
        #                 df_y = df_y[df_y["INSEE_COM"].str.startswith("33")]
        #             else:
        #                 st.warning("⚠️ Colonne INSEE_COM absente dans " + str(file_path))
        #                 continue

        #         # Ajout de l’année si absente
        #             if "Annee" not in df_y.columns:
        #                 df_y["Annee"] = year
        #             dfs.append(df_y)
        #         else:
        #             st.warning("❌ Fichier introuvable : " + str(file_path))

        #     if len(dfs) == 0:
        #         st.warning("⚠️ Aucun fichier DVF trouvé dans le dossier : " + str(folder_path))
        #         return pd.DataFrame()

        #     # Concaténation sans moyenne
        #     df_all = pd.concat(dfs, ignore_index=True)
        #     return df_all

        # # Chargement effectif
        # df_main = load_main_data("data/Cyrielle/df_ok_nan_adresse_POItot.csv")
        # df_dvf = load_dvf_data("data/Cyrielle")

        # print("Type de df_main :", type(df_main))
        # print("Type de df_dvf :", type(df_dvf))

        # # --------------------------------------------------
        # # 🔄 Fusion DVF + base principale via codes INSEE
        # # --------------------------------------------------
        # df_merge = pd.merge(
        #         df_main,
        #         df_dvf,
        #         left_on="code_commune_1",
        #         right_on="INSEE_COM",
        #         how="left")

        # # Normalisation des champs
        # df_merge["type_bien"] = df_merge["type_bien"].fillna("Inconnu")
        # df_merge["DPE_1"] = df_merge["DPE_1"].fillna("NC")
        # df_merge["GES_1"] = df_merge["GES_1"].fillna("NC")

        # # Agrégation
        # df_sunburst = (
        #     df_merge.groupby(["Annee", "INSEE_COM", "type_bien", "DPE_1", "GES_1"], as_index=False)
        #     .agg({
        #         "Nb_mutations": "count",
        #         "PrixMoyen": "mean",
        #         "Prixm2Moyen": "mean",
        #         "dens_pop": "mean"
        #     })
        # )

        # annees_dispo = sorted(df_sunburst["Annee"].dropna().unique())
        # annee_sel = st.selectbox("🗓️ Sélectionnez une année pour les statiustiques de vente :", annees_dispo)
        # df_year = df_sunburst[df_sunburst["Annee"] == annee_sel]

        # fig = px.sunburst(
        #     df_year,
        #     path=["INSEE_COM", "type_bien", "DPE_1", "GES_1"],
        #     values="Nb_mutations",
        #     color="Prixm2Moyen",
        #     color_continuous_scale="YlGnBu",
        #     hover_data={
        #         "dens_pop": True,
        #         "PrixMoyen": ":,.0f",
        #         "Prixm2Moyen": ":,.0f",
        #         "Nb_mutations": ":,.0f",
        #         "Annee": True
        #     },
        #     title="🌞 Répartition des transactions par commune, type de bien, DPE et GES - " + str(annee_sel)
        # )

        # fig.update_layout(
        #     margin=dict(t=60, l=0, r=0, b=0),
        #     coloraxis_colorbar=dict(title="Prix moyen au m² (€)"),
        # )
        # st.plotly_chart(fig, use_container_width=True)



        # # --------------------------------------------------
        # # 🎛️ Paramètres utilisateur
        # # --------------------------------------------------
        # st.sidebar.header("🧭 Paramètres du graphique")

        # metric = st.sidebar.selectbox(
        #     "Valeur à représenter :",
        #     ["Nombre de ventes", "Valeur foncière totale"]
        # )

        # levels = st.sidebar.multiselect(
        #     "Choisis les niveaux hiérarchiques du sunburst :",
        #     options=[
        #         "nom_commune_1",
        #         "type_bien",
        #         "type_dpe_1",
        #         "periode_construction_dpe_1",
        #         "type_energie_chauffage_1"
        #     ],
        #     default=["nom_commune_1", "type_bien", "type_dpe_1"]
        # )

        # # --------------------------------------------------
        # # 📊 Agrégation pour le sunburst
        # # --------------------------------------------------
        # if len(levels) >= 1:
        #     df_plot = df_merged.copy()
        #     df_plot[levels] = df_plot[levels].fillna("Non spécifié")

        #     if metric == "Valeur foncière totale":
        #         df_agg = df_plot.groupby(levels, as_index=False).agg({
        #             "valeur_fonciere_1": "sum",
        #             "dens_pop": "mean",
        #             "PrixMoyen": "mean",
        #             "Prixm2Moyen": "mean"
        #         })
        #         value_col = "valeur_fonciere_1"
        #     else:
        #         df_agg = df_plot.groupby(levels, as_index=False).agg({
        #             "id_mutation": "count",
        #             "dens_pop": "mean",
        #             "PrixMoyen": "mean",
        #             "Prixm2Moyen": "mean"
        #         })
        #         df_agg.rename(columns={"id_mutation": "Nombre de ventes"}, inplace=True)
        #         value_col = "Nombre de ventes"

        #     # --------------------------------------------------
        #     # 🌞 Sunburst enrichi
        #     # --------------------------------------------------
        #     fig = px.sunburst(
        #         df_agg,
        #         path=levels,
        #         values=value_col,
        #         color=levels[0],
        #         color_discrete_sequence=px.colors.qualitative.Set3,
        #         hover_data={
        #             value_col: ":,.0f",
        #             "dens_pop": ":,.0f",
        #             "PrixMoyen": ":,.0f",
        #             "Prixm2Moyen": ":,.0f"
        #         },
        #         title="Répartition selon " + " → ".join(levels)
        #     )

        #     fig.update_traces(
        #         textinfo="label+percent parent",
        #         hovertemplate=(
        #             "<b>%{label}</b><br>" +
        #             metric + " : %{customdata[0]:,.0f}<br>" +
        #             "Densité pop. : %{customdata[1]:,.0f}<br>" +
        #             "Prix moyen : %{customdata[2]:,.0f} €<br>" +
        #             "Prix/m² moyen : %{customdata[3]:,.0f} €<br>" +
        #             "<extra></extra>"
        #         )
        #     )

        #     st.plotly_chart(fig, use_container_width=True)

        # else:
        #     st.warning("⚠️ Sélectionne au moins un niveau hiérarchique pour afficher le graphique.")


    # def affiche():
    #     st.write("coucou")