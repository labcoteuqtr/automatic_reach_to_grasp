"""
import streamlit as st
import pandas as pd
import numpy as np

SEUIL_LIKELIHOOD = 0.9
LONGUEUR_MIN = 150  # seuil minimal de frames pour garder la video

def nettoyer_donnees(df):
    df_clean = df.copy()
    for point in df.columns.levels[0]:
        faible = df[(point, 'likelihood')] < SEUIL_LIKELIHOOD
        df_clean.loc[faible, (point, 'x')] = np.nan
        df_clean.loc[faible, (point, 'y')] = np.nan

    df_clean.interpolate(method='linear', inplace=True)
    df_clean.dropna(inplace=True)
    return df_clean

def extraire_features(df):
    # vérifie que df est bien un DataFrame MultiIndex non vide
    if not isinstance(df, pd.DataFrame) or not isinstance(df.columns, pd.MultiIndex) or df.empty:
        return np.array([]).reshape(1, 0)

    features = []
    for point in df.columns.levels[0]:
        try:
            x = df[(point, 'x')].values
            y = df[(point, 'y')].values
        except KeyError:
            continue
        if len(x) < 2:
            continue

        vitesseX = np.diff(x)
        vitesseY = np.diff(y)
        vitesses = np.sqrt(vitesseX ** 2 + vitesseY ** 2)
        acceleration = np.diff(vitesses)

        features.extend([
            np.nanmean(x), np.nanstd(x),
            np.nanmean(y), np.nanstd(y),
            np.nanmean(vitesses), np.nanstd(vitesses),
            np.nanmean(acceleration), np.nanstd(acceleration)
        ])

    if len(features) == 0:
        return np.array([]).reshape(1, 0)

    return np.array(features).reshape(1, -1)

st.title("Extraction de features depuis fichiers CSV DeepLabCut")

uploaded_files = st.file_uploader(
    "Glissez-déposez vos fichiers CSV ici",
    type="csv",
    accept_multiple_files=True
)

if uploaded_files:
    data = []
    noms = []

    for uploaded_file in uploaded_files:
        try:
            df = pd.read_csv(uploaded_file, header=[1, 2], index_col=0)
            df = nettoyer_donnees(df)

            if len(df) < LONGUEUR_MIN:
                # st.warning(f"Fichier {uploaded_file.name} ignoré (trop court: {len(df)} frames)")
                continue

            features = extraire_features(df)
            if features.size > 0:
                data.append(features.flatten())
                noms.append(uploaded_file.name)
            else:
                st.warning(f"Aucune feature extraite pour {uploaded_file.name}")
        except Exception as e:
            st.error(f"Erreur avec {uploaded_file.name} : {e}")

    if data:
        df_final = pd.DataFrame(data)
        df_final.columns = [f"f{i}" for i in range(df_final.shape[1])]
        df_final.insert(0, "fichier", noms)

        st.write("Features extraites :")
        st.dataframe(df_final)

        csv = df_final.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger features_dataset.csv",
            data=csv,
            file_name="features_dataset.csv",
            mime="text/csv"
        )
    else:
        st.info("Aucun fichier valide traité.")
else:
    st.info("Veuillez glisser-déposer au moins un fichier CSV.")
"""

import streamlit as st
import pandas as pd
import numpy as np

SEUIL_LIKELIHOOD = 0.9
LONGUEUR_MIN = 150

def nettoyer_donnees(df):
    df_clean = df.copy()
    for point in df.columns.levels[0]:
        faible = df[(point, 'likelihood')] < SEUIL_LIKELIHOOD
        df_clean.loc[faible, (point, 'x')] = np.nan
        df_clean.loc[faible, (point, 'y')] = np.nan

    df_clean.interpolate(method='linear', inplace=True)
    df_clean.dropna(inplace=True)
    return df_clean

def extraire_features(df):
    if isinstance(df, str):
        try:
            df = pd.read_csv(df, header=[1, 2], index_col=0)
        except Exception as e:
            print(f"Erreur de lecture du fichier : {e}")
            return np.array([]).reshape(1, 0)

    if df.empty or not isinstance(df.columns, pd.MultiIndex):
        print("Fichier vide ou format non compatible.")
        return np.array([]).reshape(1, 0)

    try:
        df_clean = df.fillna(0).astype(float)
        features = df_clean.agg(['mean', 'std'], axis=0).values.flatten()
        return features.reshape(1, -1)
    except Exception as e:
        print(f"Erreur pendant l'extraction des features : {e}")
        return np.array([]).reshape(1, 0)

# === INTERFACE STREAMLIT ===

st.set_page_config(page_title="Extraction de Features", page_icon="")
st.title("Extraction de features depuis fichiers CSV DeepLabCut")

uploaded_files = st.file_uploader(
    "Glissez-déposez vos fichiers CSV ici ",
    type="csv",
    accept_multiple_files=True
)

if uploaded_files:
    data = []
    noms = []

    for uploaded_file in uploaded_files:
        try:
            df = pd.read_csv(uploaded_file, header=[1, 2], index_col=0)

            if df.empty:
                st.warning(f"{uploaded_file.name} est vide.")
                continue

            df = nettoyer_donnees(df)

            if len(df) < LONGUEUR_MIN:
                st.warning(f"{uploaded_file.name} ignoré (trop court : {len(df)} frames)")
                continue

            features = extraire_features(df)
            if features.size > 0:
                data.append(features.flatten())
                noms.append(uploaded_file.name)
            else:
                st.warning(f"Aucune feature extraite pour {uploaded_file.name}")
        except Exception as e:
            st.error(f"Erreur avec {uploaded_file.name} : {e}")

    if data:
        df_final = pd.DataFrame(data)
        df_final.columns = [f"f{i}" for i in range(df_final.shape[1])]
        df_final.insert(0, "fichier", noms)

        st.success(f"{len(df_final)} fichier(s) traité(s) avec succès !")
        st.dataframe(df_final)

        csv = df_final.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger features_dataset.csv",
            data=csv,
            file_name="features_dataset.csv",
            mime="text/csv"
        )
    else:
        st.info("Aucun fichier valide traité.")
else:
    st.info("Veuillez glisser-déposer au moins un fichier CSV.")
