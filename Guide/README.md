# Classificateur de vidéos comportementales de souris
Ce projet utilise les fichiers générés par DeepLabCut pour classifier automatiquement si une vidéo est un **succès** ou un **échec**, en analysant les mouvements détectés de la souris.

## Structure du projet
```text
Classifier_Souris/
├── fichiers_dlc/ # Contient les fichiers CSV produits par DeepLabCut
│ ├── M134_20150506_v028DLC_...
│ └── ...
├── Annotations.csv # Fichier listant les labels (succès = 0 / échec = 1)
├── entrainer_classifier.py
├── extraire_features.py # Script d'extraction des caractéristiques
├── features_dataset.csv # (généré automatiquement)
├── classer_fichier.py # Script entraînant le modèle et affichant les résultats
├── interface.py
├── main.py
├── Guide
│ ├── README.md
│ ├── Installation.md
│ └── PROBLEMES ET SOLUTIONS.md
├── random_forest_model.pkl
├── requirements.txt
└── .venv/ (optionnel) # Environnement virtuel Python
```

## Installation
1. Cloner le projet ou le placer dans un dossier local.
2. Créer un environnement virtuel
``` bash
  python -m venv .venv
  .venv\Scripts\activate.ps1  # windows
```
3. Installer les dépendances
``` bash
  pip install streamlit pandas numpy scikit-learn matplotlib seaborn
```

## Configurer l'interpréteur avec le nouvel environnement
- Aller dans File > Settings > Project: Souris > Python Interpreter
- Cliquer sur Paramètres (⚙)️ > Add Interpreter...
- Choisir : Existing environment
- Sélectionner C:\Souris\.venv\Scripts\python.exe
- Cliquer surr OK














