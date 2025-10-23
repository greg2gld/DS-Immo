"""
code de la page

"""
from tools import *
from modelization import *
from encode import *

import streamlit as st
from datetime import date, time, datetime

def affiche():
    st.title("Modélisation")
    tab_immo, tab_compare  = st.tabs(["Prédiction immobilière", "Comparatif Modèles immobiliers"])

    with tab_immo:
        st.header("Prédiction du prix d’un bien immobilier en Gironde")
        with st.form("immo_form"):
            st.subheader("Localisation")
            col_numero, col_rue, col_insee = st.columns([0.1,0.7,0.2])
            with col_numero:
                numero = st.text_input("N°", key="adresse_num")
            with col_rue:
                rue = st.text_input("Nom et type de voie", key="adresse_voie", placeholder="Rue de.., Avenue de...")
            with col_insee:
                code_insee = st.selectbox(
                    "Code INSEE", 
                    ['33001', '33002', '33003', '33004', '33005', '33006', '33007', '33008', '33009', '33010', '33011', '33012', '33013', '33014', '33015', '33017', '33018', '33019', '33021', '33022', '33023', '33024', '33025', '33026', '33027', '33028', '33029', '33030', '33032', '33033', '33034', '33035', '33036', '33037', '33038', '33039', '33040', '33042', '33043', '33044', '33045', '33046', '33047', '33048', '33049', '33050', '33051', '33052', '33054', '33055', '33056', '33057', '33058', '33060', '33061', '33062', '33063', '33065', '33067', '33068', '33069', '33070', '33071', '33072', '33073', '33075', '33076', '33077', '33078', '33079', '33080', '33081', '33082', '33083', '33084', '33085', '33086', '33087', '33088', '33089', '33090', '33093', '33094', '33095', '33096', '33097', '33098', '33099', '33100', '33101', '33102', '33104', '33105', '33106', '33108', '33109', '33111', '33112', '33113', '33114', '33115', '33116', '33117', '33118', '33119', '33120', '33121', '33122', '33123', '33124', '33125', '33126', '33127', '33128', '33129', '33130', '33131', '33132', '33134', '33135', '33136', '33137', '33138', '33139', '33140', '33141', '33142', '33143', '33144', '33145', '33146', '33147', '33148', '33149', '33150', '33151', '33152', '33153', '33154', '33157', '33158', '33159', '33160', '33161', '33162', '33163', '33164', '33165', '33166', '33167', '33168', '33169', '33170', '33171', '33172', '33173', '33174', '33175', '33176', '33177', '33178', '33179', '33181', '33182', '33183', '33184', '33185', '33186', '33187', '33188', '33189', '33190', '33191', '33192', '33193', '33194', '33195', '33196', '33197', '33198', '33199', '33200', '33201', '33202', '33203', '33204', '33205', '33206', '33207', '33208', '33209', '33210', '33211', '33212', '33213', '33214', '33215', '33216', '33218', '33219', '33220', '33221', '33222', '33223', '33225', '33226', '33227', '33228', '33229', '33230', '33232', '33233', '33234', '33235', '33236', '33237', '33238', '33239', '33240', '33241', '33242', '33243', '33244', '33245', '33246', '33248', '33249', '33250', '33251', '33252', '33253', '33254', '33255', '33256', '33257', '33258', '33259', '33260', '33261', '33262', '33263', '33264', '33266', '33268', '33269', '33270', '33271', '33272', '33273', '33274', '33275', '33276', '33279', '33280', '33281', '33282', '33283', '33284', '33285', '33287', '33288', '33289', '33290', '33293', '33294', '33296', '33297', '33298', '33299', '33300', '33301', '33302', '33303', '33304', '33305', '33306', '33307', '33308', '33309', '33310', '33311', '33312', '33314', '33315', '33316', '33317', '33318', '33319', '33320', '33321', '33322', '33323', '33324', '33325', '33326', '33327', '33328', '33329', '33330', '33331', '33332', '33333', '33334', '33335', '33336', '33337', '33339', '33341', '33342', '33343', '33344', '33345', '33346', '33347', '33348', '33349', '33350', '33351', '33352', '33353', '33354', '33355', '33356', '33357', '33358', '33360', '33361', '33362', '33363', '33364', '33366', '33367', '33369', '33370', '33372', '33373', '33374', '33375', '33376', '33377', '33378', '33379', '33380', '33381', '33382', '33383', '33384', '33385', '33386', '33387', '33388', '33389', '33390', '33391', '33392', '33393', '33394', '33395', '33396', '33397', '33399', '33400', '33401', '33402', '33404', '33405', '33406', '33407', '33408', '33411', '33412', '33413', '33414', '33415', '33416', '33417', '33418', '33421', '33422', '33423', '33424', '33425', '33426', '33427', '33428', '33429', '33431', '33432', '33433', '33434', '33435', '33436', '33437', '33438', '33439', '33441', '33442', '33443', '33444', '33445', '33447', '33448', '33449', '33450', '33451', '33452', '33453', '33454', '33456', '33457', '33458', '33459', '33460', '33461', '33462', '33463', '33464', '33465', '33466', '33467', '33468', '33470', '33471', '33472', '33473', '33474', '33476', '33477', '33478', '33480', '33481', '33482', '33483', '33484', '33485', '33486', '33487', '33488', '33489', '33490', '33491', '33492', '33493', '33494', '33496', '33498', '33499', '33500', '33501', '33502', '33503', '33504', '33505', '33506', '33507', '33508', '33509', '33511', '33512', '33513', '33514', '33515', '33516', '33517', '33518', '33519', '33520', '33521', '33522', '33523', '33524', '33525', '33527', '33528', '33529', '33530', '33531', '33532', '33533', '33534', '33535', '33536', '33537', '33538', '33539', '33540', '33541', '33542', '33543', '33544', '33545', '33546', '33547', '33548', '33549', '33550', '33551', '33552', '33553', '33554', '33555'], 
                    key="adresse_insee",
                    index=0
                )

            st.subheader("Caractéristiques du bien")
            col_type, col_nbpieces, col_surface = st.columns([0.4,0.3,0.3])
            with col_type:
                type_bien = st.radio("Type de bien", key="type_bien", options=["Appartement", "Maison"], horizontal=True)
            with col_nbpieces:
                nombre_pieces_principales_1 = st.number_input("Nombre de pièces", key="nombre_pieces_principales_1", min_value=0, value=3, step=1)
            with col_surface:
                surface_reelle_bati_1 = st.number_input("Surface du bien (m²)", key="surface_reelle_bati_1", min_value=0.0, value=60.0, step=0.5)

            st.subheader("Caractéristiques énergétiques")
            # DPE / GES (catégories A–G typiquement)
            c3, c4 = st.columns(2)
            with c3:
                periode_construction_dpe_1 = st.selectbox(
                    "Periode de construction",  
                    ["avant 1948","1948-1974","1975-1977","1978-1982","1983-1988","1989-2000","2001-2005","2006-2012","2013-2021","après 2021"],
                    key="periode_construction_dpe_1",
                    index=0
                )
                DPE_1 = st.selectbox("Diagnostic de performance énergétique", list("ABCDEFG"), key="DPE_1")

            with c4:
                GES_1 = st.selectbox("Gaz à effet de serre", list("ABCDEFG"), key="GES_1")
                type_energie_chauffage_1 = st.selectbox("Type de chauffage", ['gaz', 'electricite', 'reseau de chaleur', 'bois', 'fioul',
        'gpl/butane/propane', 'solaire', 'charbon'], key="type_energie_chauffage_1")
                
            st.subheader("Caractéristiques du terrain")
            
            col_surface_1, col_surface_2 = st.columns(2)
            
            with col_surface_1:
                surface_terrain_1 = st.number_input("Surface terrain principal", key="surface_terrain_1", min_value=0.0, value=0.0, step=1.0)
                surface_terrain_2 = st.number_input("Surface autre terrains", key="surface_terrain_2", min_value=0.0, value=0.0, step=1.0)
            with col_surface_2:
                code_nature_culture_1 = st.selectbox("Nature terrain principal", codes_nature_culture.keys(), key="code_nature_culture_1")
                code_nature_culture_2 = st.selectbox("Nature autres terrains", codes_nature_culture.keys(), key="code_nature_culture_2")

            model_type = st.selectbox("Type de modèle (Global, entraîné sur des maisons uniquement ou sur des appartements uniquement)", ["global", "appartements", "maisons"], key="model_type", index=0)
            submitted = st.form_submit_button("Prédire")
    with tab_compare:
        st.header("Comparatif de modèles immobiliers")
        data = [
            {'GES_1': 'A', 'FormSubmitter:immo_form-Prédire': True, 'periode_construction_dpe_1': 'avant 1948', 'type_bien': 'Appartement', 'type_energie_chauffage_1': 'gaz', 'code_nature_culture_2': 'Aucun', 'nombre_pieces_principales_1': 3, 'surface_terrain_1': 0.0, 'adresse_insee': '33001', 'surface_reelle_bati_1': 60.0, 'DPE_1': 'A', 'surface_terrain_2': 0.0, 'adresse_num': '18', 'adresse_voie': 'Avenue de Foncastel', 'code_nature_culture_1': 'Aucun'},
            {'GES_1': 'A', 'FormSubmitter:immo_form-Prédire': True, 'periode_construction_dpe_1': 'avant 1948', 'type_bien': 'Appartement', 'type_energie_chauffage_1': 'gaz', 'code_nature_culture_2': 'Aucun', 'nombre_pieces_principales_1': 3, 'surface_terrain_1': 0.0, 'adresse_insee': '33001', 'surface_reelle_bati_1': 60.0, 'DPE_1': 'A', 'surface_terrain_2': 0.0, 'adresse_num': '18', 'adresse_voie': 'Avenue de Foncastel', 'code_nature_culture_1': 'Aucun'},
            {'GES_1': 'A', 'FormSubmitter:immo_form-Prédire': True, 'periode_construction_dpe_1': 'avant 1948', 'type_bien': 'Appartement', 'type_energie_chauffage_1': 'gaz', 'code_nature_culture_2': 'Aucun', 'nombre_pieces_principales_1': 3, 'surface_terrain_1': 0.0, 'adresse_insee': '33001', 'surface_reelle_bati_1': 60.0, 'DPE_1': 'A', 'surface_terrain_2': 0.0, 'adresse_num': '18', 'adresse_voie': 'Avenue de Foncastel', 'code_nature_culture_1': 'Aucun'},
            {'GES_1': 'A', 'FormSubmitter:immo_form-Prédire': True, 'periode_construction_dpe_1': 'avant 1948', 'type_bien': 'Appartement', 'type_energie_chauffage_1': 'gaz', 'code_nature_culture_2': 'Aucun', 'nombre_pieces_principales_1': 3, 'surface_terrain_1': 0.0, 'adresse_insee': '33001', 'surface_reelle_bati_1': 60.0, 'DPE_1': 'A', 'surface_terrain_2': 0.0, 'adresse_num': '18', 'adresse_voie': 'Avenue de Foncastel', 'code_nature_culture_1': 'Aucun'},
            {'GES_1': 'A', 'FormSubmitter:immo_form-Prédire': True, 'periode_construction_dpe_1': 'avant 1948', 'type_bien': 'Appartement', 'type_energie_chauffage_1': 'gaz', 'code_nature_culture_2': 'Aucun', 'nombre_pieces_principales_1': 3, 'surface_terrain_1': 0.0, 'adresse_insee': '33001', 'surface_reelle_bati_1': 60.0, 'DPE_1': 'A', 'surface_terrain_2': 0.0, 'adresse_num': '18', 'adresse_voie': 'Avenue de Foncastel', 'code_nature_culture_1': 'Aucun'}
        ]

        for item in data:
            st.table({
                "Modèle global" : f"Prix estimé à {prepare_data(item, "global"):,.0f}€",
                "Modèle entraîné uniquement sur les maisons" : f"Prix estimé à {prepare_data(item, "maisons"):,.0f}€",
                "Modèle entrainé uniquement sur les appartements" : f"Prix estimé à {prepare_data(item, "appartements"):,.0f}€"
            })
 
    # Déclenchement
    if submitted:
        prix = prepare_data(st.session_state)
        st.success(f"Le bien est estimé à {prix:,.0f}€ avec le modele {st.session_state["model_type"]}")