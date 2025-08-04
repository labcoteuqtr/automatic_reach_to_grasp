import time
import streamlit as st
import pandas as pd
import tempfile
from extraire_features import extraire_features
from model_utils import charger_modele, predire  # fonctions de prédiction

st.set_page_config(page_title="Classifier", page_icon=" ")
st.title("Classification des vidéos : Succès ou Échec")

col1, col2 = st.columns(2)

with col1:
    st.header("Fichiers CSV")
    uploaded_files = st.file_uploader(
        "Sélectionnez les fichiers DLC (.csv)", accept_multiple_files=True, type=["csv"]
    )

with col2:
    st.header("Actions")
    lancer_classification = st.button("Lancer la classification")

if lancer_classification and uploaded_files:
    progress_bar_text = "Traitement en cours. Merci de patienter..."
    progress_bar = st.progress(0, text=progress_bar_text)

    # Charger le modèle
    model = charger_modele()

    resultats = []
    total_files = len(uploaded_files)

    for i, uploaded_file in enumerate(uploaded_files):
        # Enregistrer le fichier temporairement
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        # Extraire les features
        features = extraire_features(tmp_path)

        # Affichage debug
        print(f"Fichier analysé : {uploaded_file.name}")
        print("Shape des features :", features.shape)
        print("Aperçu des features :", features)

        # Vérification des features
        if features.shape[1] == 0:
            print(f"Aucun feature extrait depuis {uploaded_file.name}")
            prediction = None
            classification = "Erreur : pas de données"
            proba = None
        else:
            # Prédiction
            prediction = predire(model, features)
            proba = model.predict_proba(features)

            print("Prediction brute :", prediction)
            print("Proba :", proba)

            classification = "Succès" if prediction == 1 else "Échec"

        # Extraire le nom de la vidéo d'origine
        nom_csv = uploaded_file.name
        nom_video = nom_csv.split("DLC")[0]

        # Ajouter aux résultats
        resultats.append({
            "Vidéo": nom_video,
            "Fichier CSV": nom_csv,
            "Classification": classification
        })

        progress_bar.progress(int((i + 1) / total_files * 100), text=progress_bar_text)

    time.sleep(1)
    progress_bar.empty()

    # Affichage final
    df_resultats = pd.DataFrame(resultats)
    st.success("Classification terminée ")
    st.dataframe(df_resultats)

    # Option de téléchargement
    csv_export = df_resultats.to_csv(index=False).encode('utf-8')
    st.download_button("Télécharger les résultats", data=csv_export, file_name="resultats_classification.csv", mime='text/csv')

elif lancer_classification:
    st.warning("Veuillez d'abord téléverser des fichiers CSV.")
