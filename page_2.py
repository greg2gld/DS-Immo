"""
code de la page

"""

from tools import *

def affiche():
    st.title("DataVisualization")
    st.markdown("""
...
                """)
    
    
    st.header("1. Transactions")
    st.subheader("Carte")
    
    # chargement du df
    col_to_ignore = ['Unnamed: 0',                     
                    ]
    df_ok_nan = csv_to_df(os.path.join(PATH_DATA, "df_ok_nan.csv"),
                          sep=",",
                          index_col = "index",
                          col_to_ignore = col_to_ignore)
    
    df_post_prepro = preprocessing_df(df_ok_nan)

    # filtres
    col1, col2, col3 = st.columns(3)

    with col1:
        val_to_display = st.radio("**Donnée à afficher :**", ("nb_transactions", "prix_moyen"))
    with col2:
        type_de_bien = st.radio("**Type de bien :**",
                            ("Tout type", "Maison", "Appartement"))
    with col3:
        presence_terrain = st.radio("**Presence terrain :**",
                             ("Avec et sans", "Oui", "Non"))

    match type_de_bien:
            case "Tout type":
                # on fait rien
                df_filtered = df_post_prepro
            case "Maison":
                df_filtered = df_post_prepro[df_post_prepro['maison'] == 1]
            case "Appartement":
                df_filtered = df_post_prepro[df_post_prepro['maison'] == 0]

    match presence_terrain:         
         case "Avec et sans":
            # on fait rien
            df_filtered = df_filtered
         case "Oui":
              df_filtered = df_filtered[df_filtered['terrain'] == 1]
         case "Non":
              df_filtered = df_filtered[df_filtered['terrain'] == 0]

    col = ['valeur_fonciere_1',
       'code_commune_1',
       'nom_commune_1',
       'types_biens_1'
       ]

    # groupby
    gb = df_filtered[col] \
        .groupby(['code_commune_1', 'nom_commune_1']) \
        .agg(
            nb_transactions=('valeur_fonciere_1', 'count'),
            prix_moyen=('valeur_fonciere_1', 'mean'))  
    
    # st.write(gb)

    # val_to_display = "nb_transactions"
    
    # chargement shp
    geojson_gironde = load_shape(os.path.join(PATH_DATA, "shapefiles", "communes_gironde.shp"))

    # affichage carte
    fig = px.choropleth_map(
        gb,
        geojson=geojson_gironde,
        locations=gb.index.levels[0], # 'code_commune',
        featureidkey="properties.INSEE_COM",
        color=val_to_display,
        hover_name=gb.index.levels[1], #'nom_commune', 
        # labels={'dens_pop':'hab./km²'},
        color_continuous_scale="Oranges",
        range_color=(gb[val_to_display].min(), gb[val_to_display].max()),
        # color_continuous_scale="Viridis",
        # range_color=(0, 12),
        center={"lat": 44.84, "lon": -0.58},
        zoom=8,
        width=1200, height=750
        )

    fig.update_layout(
        title_text=val_to_display,
        title_font_size=22,
        title_x=0.5, 
        # title_y=0,
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        )
    st.plotly_chart(fig)
    # st.pyplot(fig)
    