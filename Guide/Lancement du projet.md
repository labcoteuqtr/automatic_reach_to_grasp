# Étapes d'utilisation
## A - Générer les caractéristiques (features_dataset.csv)
1. Lancer l'application Streamlit 
* en saisissant la commande plus bas 
``` bash
    streamlit run extraire_features.py
```
Cela ouvrira une interface web dans ton navigateur.

2. Importer les fichiers CSV DeepLabCut
Dans l'interface, clique sur "Parcourir les fichiers" ou glisse-dépose plusieurs fichiers .csv issus de DeepLabCut (ex. : *_filtered.csv)
**Remarques :** 
- Les fichiers doivent contenir au moins 150 frames pour être pris en compte
- Le système nettoiera les données en supprimant les coordonnées dont le likelihood est inférieur à 0.9, et interpolera les données manquantes

3. Télécharger les données extraites
Une fois l’extraction terminée :
Les données apparaissent dans un tableau dans l’interface
On peut cliquer sur "Télécharger features_dataset.csv" pour récupérer le fichier
Ce fichier est prêt à être utilisé pour l'entraînement d'un modèle de classification (entrainer_classifier.py)


## B - Entrainer le modèle
1. Lancer l'application Streamlit 
* en saisissant la commande plus bas 
``` bash
    streamlit run entrainer_classifier.py
```
Cela ouvrira une interface web dans ton navigateur.

2. Importer le fichier CSV "features_dataset.csv"

3. Cliquer sur "Entrainer le modèle"
Ce script va 
- Charge features_dataset.csv
- Sépare les données en train/test
- Entraîne un modèle RandomForest
- Affiche les scores, une matrice de confusion et les résultats de validation croisée

4. L'entrainement du modèle est lancé et le fichier "modele_random_forest.pkl" est téléchargé automatiquement

