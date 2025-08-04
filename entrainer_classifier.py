import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

st.set_page_config(page_title="Entraînement du modèle", layout="centered")
st.title("Entraînement du modèle de classification")

# 1. Chargement du fichier CSV
uploaded_file = st.file_uploader("Téléverser le fichier `features_dataset.csv` :", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.write("Colonnes du DataFrame :", df.columns.tolist())

    # Extraire le label
    def extraire_label(nom_fichier):
        nom_fichier = str(nom_fichier).lower()
        if "succès" in nom_fichier:
            return "succès"
        elif "échec" in nom_fichier:
            return "échec"
        else:
            return "inconnu"

    df["label"] = df["fichier"].apply(extraire_label)
    df = df[df["label"].isin(["succès", "échec"])]

    # Supprimer doublons (sauf 'fichier')
    cols_a_considerer = df.columns.difference(["fichier"])
    df = df.drop_duplicates(subset=cols_a_considerer)

    st.success(f"{len(df)} lignes chargées avec labels valides et doublons supprimés.")
    st.dataframe(df.head())

    if st.button("Entraîner le modèle"):
        try:
            # Sélectionner uniquement les colonnes features numériques
            feature_cols = [col for col in df.columns if col.startswith('f') and col != 'fichier']
            st.write(f"Colonnes features utilisées : {feature_cols}")

            X = df[feature_cols].astype(float)  # forcer conversion float si besoin
            y = df["label"]

            # Split stratifié train/test
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )

            # 5. Entraînement RandomForest
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)

            st.subheader("Rapport de classification")
            st.text(classification_report(y_test, y_pred, zero_division=0))

            st.subheader("Matrice de confusion")
            fig, ax = plt.subplots(figsize=(5, 3))
            sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues', ax=ax)
            plt.xlabel('Prédiction')
            plt.ylabel('Réel')
            st.pyplot(fig)

            # 6. Validation croisée (5 folds)
            st.subheader("📈 Validation croisée (5 folds)")
            scores = cross_val_score(RandomForestClassifier(random_state=42), X, y, cv=5)
            st.write(f"**Scores individuels** : {scores}")
            st.write(f"**Score moyen** : {scores.mean():.2f}")

            # 7. Accuracy sur train et test
            train_acc = accuracy_score(y_train, model.predict(X_train))
            test_acc = accuracy_score(y_test, y_pred)
            st.metric("Accuracy sur les données d'entraînement", f"{train_acc:.2f}")
            st.metric("Accuracy sur les données test", f"{test_acc:.2f}")

            # 8. Sauvegarde du modèle
            joblib.dump(model, "modele_random_forest.pkl")
            st.success("Modèle sauvegardé dans le fichier `modele_random_forest.pkl`")

        except Exception as e:
            st.error(f"Une erreur est survenue : {e}")

else:
    st.info("Veuillez téléverser un fichier `features_dataset.csv` généré par l'extraction.")
