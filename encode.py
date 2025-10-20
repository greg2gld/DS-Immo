import pandas as pd
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder, TargetEncoder, LabelEncoder

def fit_one_hot(df_source, vars):
    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False, dtype="int")
    encoder.fit(df_source[vars])
    return encoder

def transform_one_hot(encoder, df_source, vars):
    df = df_source.copy()
    encoded = encoder.transform(df[vars])
    encoded_columns = encoder.get_feature_names_out(vars)
    df_encoded = pd.DataFrame(encoded, columns=encoded_columns, index=df.index)
    df = df.drop(columns=vars).join(df_encoded)
    return df

def fit_ordinal(df_source, vars, categories):
    encoder = OrdinalEncoder(categories=categories)
    encoder.fit(df_source[vars])
    return encoder

def transform_ordinal(encoder, df_source, vars):
    df = df_source.copy()
    df[vars] = encoder.transform(df[vars])
    return df

def fit_target(df_source, df_target, vars):
    encoder = TargetEncoder()
    encoder.fit(df_source[vars], df_target)
    return encoder

def transform_target(encoder, df_source, vars):
    df = df_source.copy()
    df[vars] = encoder.transform(df[vars])
    return df

def encode(X_train, X_test, y_train, encoding_parameters, fallback_on_target=True):
    X_train_encoded = X_train.copy()
    X_test_encoded = X_test.copy()
    encoders = {}
    # Encoding des variables Ordinales
    ordinal_variables = [col for col in encoding_parameters["ordinal_variables"] if col in X_train.columns]
    if len(ordinal_variables):
        categories = []
        for variable in ordinal_variables:
            if variable in encoding_parameters["ordinal_categories"]:
                categories.append(encoding_parameters["ordinal_categories"][variable])
            else:
                categories.append(sorted(X_train['DPE_1'].unique(), reverse= True))
        ordinal_encoder = fit_ordinal(X_train, ordinal_variables, categories)
        X_train_encoded = transform_ordinal(ordinal_encoder, X_train_encoded, ordinal_variables)
        X_test_encoded = transform_ordinal(ordinal_encoder, X_test_encoded, ordinal_variables)
        encoders["ordinal_encoder"] = ordinal_encoder

    # Encoding One Hot
    one_hot_variables = [col for col in encoding_parameters["one_hot_variables"] if col in X_train.columns]
    if len(one_hot_variables):
        one_hot_encoder = fit_one_hot(X_train_encoded, one_hot_variables)
        X_train_encoded = transform_one_hot(one_hot_encoder, X_train_encoded, one_hot_variables)
        X_test_encoded = transform_one_hot(one_hot_encoder, X_test_encoded, one_hot_variables)
        encoders["one-hot_encoder"] = one_hot_encoder

    # Encoding des variables Target
    target_variables = [col for col in encoding_parameters["target_variables"] if col in X_train.columns]
    
    if fallback_on_target:
        cat_cols = X_train_encoded.select_dtypes(include=["object", "category"]).columns.tolist()
        cat_cols_filtered = [col for col in cat_cols if col not in one_hot_variables]
        cat_cols_filtered = [col for col in cat_cols_filtered if col not in ordinal_variables]
        target_variables = target_variables + cat_cols_filtered

    if len(target_variables):
        target_encoder = fit_target(X_train_encoded, y_train, target_variables)
        X_train_encoded = transform_target(target_encoder, X_train_encoded, target_variables)
        X_test_encoded = transform_target(target_encoder, X_test_encoded, target_variables)
        encoders["target_encoder"] = target_encoder
    
    return X_train_encoded, X_test_encoded, encoders 
