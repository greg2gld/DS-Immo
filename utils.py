import numpy as np
import pandas as pd
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.ensemble import RandomForestClassifier

def scale_severity(series, method="zscore", clip_quantiles=(0.01, 0.99)):
    """
    Calcule un score continu de gravité dans [0,1] (puis [0,100] possible),
    selon la méthode choisie.
    - zscore : recentre-réduit puis applique CDF ~ N(0,1) pour ramener dans [0,1]
    - minmax : (x - min) / (max - min) avec rognage quantile pour robustesse
    """
    s = series.astype(float).copy()
    if clip_quantiles:
        lo, hi = s.quantile(clip_quantiles[0]), s.quantile(clip_quantiles[1])
        s = s.clip(lo, hi)

    if method == "zscore":
        mu, sigma = s.mean(), s.std(ddof=0) or 1.0
        z = (s - mu) / sigma
        # approx CDF normale via erf
        sev = 0.5 * (1 + (z / np.sqrt(2)).apply(lambda v: erf_safe(v)))
        return sev.clip(0, 1)
    elif method == "minmax":
        mn, mx = s.min(), s.max()
        if mx == mn:
            return pd.Series(0.0, index=s.index)
        return ((s - mn) / (mx - mn)).clip(0, 1)
    else:
        raise ValueError("method doit valoir 'zscore' ou 'minmax'")

def erf_safe(x):
    x = float(x)
    sign = 1 if x >= 0 else -1
    x = abs(x)
    a1,a2,a3,a4,a5,p = 0.254829592,-0.284496736,1.421413741,-1.453152027,1.061405429,0.3275911
    t = 1.0/(1.0+p*x)
    y = 1.0 - (((((a5*t+a4)*t)+a3)*t+a2)*t+a1)*t*np.exp(-x*x)
    return sign*y

def multi_column_severity(df, cols, by=None, method="zscore", weights=None, to_100=True):
    """
    Agrège plusieurs colonnes (ex: différents types de délits) en un score unique.
    - Normalise chaque colonne (par groupe si 'by') puis somme pondérée.
    """
    if weights is None:
        weights = {c: 1.0 for c in cols}
    # normaliser les poids
    wsum = sum(weights.values())
    weights = {c: w / wsum for c, w in weights.items()}

    parts = []
    for c in cols:
        if by is None:
            sev_c = scale_severity(df[c], method=method)
        else:
            sev_c = df.groupby(by, group_keys=False).apply(
                lambda g: scale_severity(g[c], method=method)
            )
        parts.append(weights[c] * sev_c)

    sev = sum(parts)
    return (sev * 100).round(2) if to_100 else sev


def make_bins(X_train, X_test, cols, n_bins, encode="ordinal", strategy="quantile", suffix="_bin_ml", drop=True):
    enc = KBinsDiscretizer(n_bins=n_bins, encode=encode, strategy=strategy)    
    for col in cols:
        if col in X_train.columns:
            enc.fit(X_train[[col]])
            X_train[col + suffix] = enc.transform(X_train[[col]]).astype(int)
            X_test[col + suffix] = enc.transform(X_test[[col]]).astype(int)
    if drop:
        X_train = X_train.drop(columns=cols)
        X_test = X_test.drop(columns=cols)
    return X_train, X_test


def delinquence_bins(df):
    delits = {
        "Autres coups et blessures volontaires" : 2,
        "Cambriolages de logement" : 1,
        "Coups et blessures volontaires" : 2,
        "Coups et blessures volontaires intrafamiliaux" : 2,
        "Destructions et degradations volontaires" : 1,
        "Escroqueries" : 1,
        "Trafic de stupefiants" : 3,
        "Usage de stupefiants" : 1,
        "Usage de stupefiants (AFD)" : 1,
        "Violences sexuelles" : 2,
        "Vols avec armes" : 3,
        "Vols d accessoires sur vehicules" : 2,
        "Vols dans les vehicules" : 2,
        "Vols de vehicules" : 2,
        "Vols sans violence contre des personnes" : 2,
        "Vols violents sans arme" : 2
    }
    cols=list(delits.keys())
    df["delinquence"] = multi_column_severity(
        df, 
        cols=cols,
        method="zscore",
        weights=delits,
        to_100=True
    )
    return df.drop(cols, axis=1)

def commune_outliers(df, threshold=10):
    ## Suppression communes avec moins de X ventes
    commune_counts = df["code_commune_1"].value_counts()
    # Garder uniquement les communes avec au moins 10 ventes
    communes_a_garder = commune_counts[commune_counts >= threshold].index
    # Filtrer df pour ne garder que ces communes
    df_filtré = df[df["code_commune_1"].isin(communes_a_garder)].copy()
    df = df_filtré
    return df#.drop(columns = ["code_commune_1"])

def _safe_ratio(t: pd.Series, c: pd.Series) -> pd.Series:
    denom = c.replace(0, np.nan)
    r = t / denom
    r = r.replace([np.inf, -np.inf], np.nan)
    return r

def fit_combined_outliers(
    X_train: pd.DataFrame,
    denom: str,
    cols: list[str] | None = None,
    groupby: list[str] | None = None,
    quantiles: tuple[float, float] = (0.25, 0.75),
):
    """Apprend les seuils 'luxe' (indice bas) et 'travaux' (indice haut) sur TRAIN uniquement."""
    df = X_train.copy()

    # Gestion des colonnes à combiner & exclusion de la cible
    if cols is None:
        cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cols = [c for c in cols if c != denom]

    per_col_idx_names = []
    mean_ratio_global = {}
    mean_ratio_by_group = {}

    # calcul err_idx = 100 * mean(t/c) / (t/c)
    for c in cols:
        ratio = _safe_ratio(df[denom], df[c])
        if groupby is None:
            m = ratio.mean(skipna=True)
            mean_ratio_global[c] = m
            err_idx = 100.0 * m / ratio
        else:
            gkey = df[groupby].apply(tuple, axis=1) if isinstance(groupby, list) else df[groupby]
            mean_g = ratio.groupby(gkey).transform("mean")
            mean_ratio_by_group[c] = ratio.groupby(gkey).mean()
            err_idx = 100.0 * mean_g / ratio

        name = f"{c}_err_idx"
        df[name] = err_idx.replace([np.inf, -np.inf], np.nan)
        per_col_idx_names.append(name)

    df["err_idx_min"] = df[per_col_idx_names].min(axis=1, skipna=True)
    df["err_idx_max"] = df[per_col_idx_names].max(axis=1, skipna=True)

    q_low, q_high = quantiles
    threshold_low = np.nanpercentile(df["err_idx_min"], q_low * 100)
    threshold_high = np.nanpercentile(df["err_idx_max"], q_high * 100)

    return {
        "cols" : cols,
        "groupby" : groupby,
        "quantiles" :quantiles,
        "threshold_low" : threshold_low,
        "threshold_high": threshold_high,
        "mean_ratio_global": mean_ratio_global if groupby is None else None,
        "mean_ratio_by_group" : mean_ratio_by_group if groupby is not None else None
    }

def transform_combined_outliers(
    X: pd.DataFrame,
    parameters: dict,
    denom: str = "valeur_fonciere_1",
    flags=("luxe", "travaux"),
    return_intermediate: bool = False,
) -> pd.DataFrame:
    """
    Applique les seuils appris. Utilise y uniquement pour calculer l'indice (diagnostic).
    """
    df = X.copy()

    per_col_idx_names = []
    for c in parameters['cols']:
        ratio = _safe_ratio(df[denom], df[c])
        if parameters['groupby'] is None:
            m = parameters['mean_ratio_global'][c]
            err_idx = 100.0 * m / ratio
        else:
            gkey = df[parameters['groupby']].apply(tuple, axis=1) if isinstance(parameters['groupby'], list) else df[parameters['groupby']]
            # aligner les moyennes apprises; si un groupe est inconnu, fallback global
            mean_g = gkey.map(parameters['mean_ratio_by_group'][c])
            # fallback : moyenne globale sur TRAIN de cette colonne
            fallback = np.nanmean(parameters['mean_ratio_by_group'][c].values)
            mean_g = mean_g.fillna(fallback)
            err_idx = 100.0 * mean_g / ratio

        name = f"{c}_err_idx"
        df[name] = err_idx.replace([np.inf, -np.inf], np.nan)
        per_col_idx_names.append(name)

    df["err_idx_min"] = df[per_col_idx_names].min(axis=1, skipna=True)
    df["err_idx_max"] = df[per_col_idx_names].max(axis=1, skipna=True)

    col_luxe, col_trav = flags
    df[col_luxe] = df["err_idx_min"] < parameters['threshold_low']
    df[col_trav] = df["err_idx_max"] > parameters['threshold_high']
    
    if not return_intermediate:
        drop_cols = [c for c in df.columns if c.endswith("_err_idx")] + ["err_idx_min", "err_idx_max"]
        df = df.drop(columns=drop_cols, errors="ignore")
    else:
        # on ne garde pas la cible par défaut
        df = df.drop(columns=[denom], errors="ignore")

    return df


import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import cross_val_score, StratifiedKFold

def predictor(
    df, X_test, variable_low, variable_high, target,
    thr_corr_feat=0.30, thr_corr_target=0.20,
    random_state=42, use_proba=True, cv_folds=5
):
    """
    Remplace variable_low / variable_high (booléens) par des prédictions
    de modèles annexes entraînés uniquement sur des features autorisées,
    et affiche leurs scores de validation croisée.
    """
    df = df.copy()
    X_test = X_test.copy()

    # Convertit les booléens en int pour corrélation
    for col in [variable_low, variable_high, target]:
        if col in df.columns and df[col].dtype == bool:
            df[col] = df[col].astype(int)

    # Corrélation sur les colonnes numériques
    num_df = df.select_dtypes(include=[np.number])
    corrs = num_df.corr()

    for col in [target, variable_low, variable_high]:
        if col not in num_df.columns:
            raise ValueError(f"La colonne '{col}' doit être numérique pour la corrélation.")

    target_corr = corrs[target]
    low_corr = corrs[variable_low]
    high_corr = corrs[variable_high]

    cand_cols = [c for c in num_df.columns if c not in {target, variable_low, variable_high}]
    cand_cols_test = set(X_test.columns)

    # Sélection de features
    features_high = [
        c for c in cand_cols
        if abs(high_corr.get(c, 0.0)) > thr_corr_feat and abs(target_corr.get(c, 0.0)) < thr_corr_target
    ]
    features_low = [
        c for c in cand_cols
        if abs(low_corr.get(c, 0.0)) > thr_corr_feat and abs(target_corr.get(c, 0.0)) < thr_corr_target
    ]

    features_high = [c for c in features_high if c in cand_cols_test]
    features_low  = [c for c in features_low  if c in cand_cols_test]

    if len(features_high) == 0 or len(features_low) == 0:
        raise ValueError("Aucune feature sélectionnée — ajuste les seuils de corrélation.")

    # === Entraînement des modèles ===
    model_high = RandomForestClassifier(n_estimators=1000,max_depth=12, random_state=random_state)
    model_low = RandomForestClassifier(n_estimators=1000, max_depth=12, random_state=random_state)

    # Cross-validation pour évaluer la précision
    kf = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=random_state)

    def evaluate(model, X, y):
        acc = cross_val_score(model, X, y, cv=kf, scoring='accuracy').mean()
        f1 = cross_val_score(model, X, y, cv=kf, scoring='f1').mean()
        auc = cross_val_score(model, X, y, cv=kf, scoring='roc_auc').mean()
        return {"accuracy": acc, "f1": f1, "roc_auc": auc}

    metrics_high = evaluate(model_high, df[features_high], df[variable_high])
    metrics_low  = evaluate(model_low, df[features_low], df[variable_low])

    print(f"\n🔹 Performance du classifieur '{variable_high}' :")
    print(f"  - Accuracy : {metrics_high['accuracy']:.3f}")
    print(f"  - F1-score : {metrics_high['f1']:.3f}")
    print(f"  - AUC      : {metrics_high['roc_auc']:.3f}")

    print(f"\n🔹 Performance du classifieur '{variable_low}' :")
    print(f"  - Accuracy : {metrics_low['accuracy']:.3f}")
    print(f"  - F1-score : {metrics_low['f1']:.3f}")
    print(f"  - AUC      : {metrics_low['roc_auc']:.3f}")

    # Fit final (entraînement complet)
    model_high.fit(df[features_high], df[variable_high])
    model_low.fit(df[features_low], df[variable_low])

    # Prépare X_train sans les colonnes originales
    X_train = df.drop(columns=[target, variable_low, variable_high], errors='ignore').copy()
    X_test = X_test.drop(columns=[target, variable_low, variable_high], errors='ignore').copy()
    # Ajoute les prédictions
    if use_proba:
        X_train[variable_low]  = model_low.predict_proba(X_train[features_low])[:, 1].astype(bool)
        X_train[variable_high] = model_high.predict_proba(X_train[features_high])[:, 1].astype(bool)
        X_test[variable_low]   = model_low.predict_proba(X_test[features_low])[:, 1].astype(bool)
        X_test[variable_high]  = model_high.predict_proba(X_test[features_high])[:, 1].astype(bool)
    else:
        X_train[variable_low]  = model_low.predict(X_train[features_low]).astype(bool)
        X_train[variable_high] = model_high.predict(X_train[features_high]).astype(bool)
        X_test[variable_low]   = model_low.predict(X_test[features_low]).astype(bool)
        X_test[variable_high]  = model_high.predict(X_test[features_high]).astype(bool)

    return X_train, X_test, {"luxe": metrics_high, "travaux": metrics_low}


def prepare_data(df):
    # Cleanup colonnes
    df = df.drop(columns = ["id_mutation","adresse_complete_1", "index","Unnamed: 0","a_bien_2","nom_commune_1","id_parcelle_1","longitude_1","latitude_1","types_biens_1","type_bien","type_dpe_1","code_iris","lon_rad","lat_rad"], axis = 1)
    df = df.drop(df.filter(like="_moins_50m").columns, axis=1)
    df = df.drop(df.filter(like="_moins_500m").columns, axis=1)
    df = df.drop(df.filter(like="_moins_2km").columns, axis=1)
    df = df.dropna()
    
    # Calcul et bins délinquance
    df = delinquence_bins(df)
   
    df["terrain_1"] = (df["surface_terrain_1"] != 0).astype(int)
   # df["appartement"] = np.where(df["code_type_local_1"] == 2, 1, 0)
    df["maison"] = np.where(df["code_type_local_1"] == 1, 1, 0)
    df = df.drop(columns=["code_type_local_1"], axis=1)
    df = df.drop(columns=["code_type_local_2"], axis=1)
    df = commune_outliers(df)

    df['annee_mutation'] = pd.to_datetime(df['date_mutation_1']).dt.year
    df_liste = []
    for year in [2020, 2021, 2022, 2023, 2024]:
        csv = pd.read_csv(f"dvf{year}.csv")
        # Renomme pour harmoniser avec le df source
        csv = csv.rename(columns={
            "INSEE_COM": "code_commune_1", 
            "Annee": "annee_mutation",
            "PrixMoyen": "prix_moyen",
            "Prixm2Moyen": "prix_m2_moyen",
            "SurfaceMoy": "surface_moyenne"
        })
        csv["annee_mutation"] = int(year)
        df_liste.append(csv[['code_commune_1', 'annee_mutation', 'prix_moyen', 'prix_m2_moyen', 'surface_moyenne']])

    df_prix = pd.concat(df_liste, ignore_index=True)

    df['code_commune_1'] = df['code_commune_1'].astype(str)
    df_prix['code_commune_1'] = df_prix['code_commune_1'].astype(str)
    df = df.merge(df_prix, how="left", on=["code_commune_1", "annee_mutation"])
    df['surface_par_piece'] = df['surface_reelle_bati_1'] / df['nombre_pieces_principales_1'].replace(0, np.nan)

    equipements_vars = [
        "Mairie_moins_10km",
        "Commerces alimentaires_moins_10km",
        "Tourisme_moins_10km",
        "Déchetterie_moins_10km",
        "Grandes surfaces_moins_10km"
    ]

    surface_totale = df["surface_reelle_bati_1"]

    df["nb_equipements_proches"] = df[equipements_vars].sum(axis=1)
    df["prix_theorique"] = (surface_totale) * df["prix_m2_moyen"]
    df["comparaison_marche"] = cmp(df["prix_theorique"], df["prix_moyen"])
    df["prix_m2"] = df["prix_theorique"] / surface_totale
    #df["comparaison_marche_m2"] = cmp(df["prix_m2"], df["prix_m2_moyen"])
    df = df.drop(columns=['code_commune_1', 'date_mutation_1', 'annee_mutation'])
    return df


def cmp(a, b):
    return (a > b).astype(int) - (a < b).astype(int)

def clean_columns(df):
    df.columns = (
        df.columns.astype(str)
        .str.replace(r'[^A-Za-z0-9_]+', '_', regex=True)
        .str.strip('_')                                 
    )
    return df


__all__ = ["fit_combined_outliers", "transform_combined_outliers", "make_bins", "prepare_data", "predictor","commune_outliers","delinquence_bins", "clean_columns"]