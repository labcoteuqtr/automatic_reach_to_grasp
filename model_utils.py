import joblib
import numpy as np

def charger_modele(path="modele_random_forest.pkl"):
    return joblib.load(path)

def predire(model, features):
    if isinstance(features, list):
        features = np.array(features).reshape(1, -1)
    elif hasattr(features, "values"):  # DataFrame
        features = features.values.reshape(1, -1)

    # verifie que les features ne sont pas vides
    if features.shape[1] == 0:
        print("Aucun feature extrait, prédiction impossible.")
        return "Erreur: Pas de données"

    return model.predict(features)[0]

