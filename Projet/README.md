# Enregistreur_Videos
Ceci est un outil python avec interface graphique permettant d'enregistrer des vidéos et des données d'expérience

## Prérequis
- Système d'exploitation Windows
- Python 3.10
- pip installé
- Une caméra compatible. Dans notre cas, il s'agit de la caméra FLIR Blackfly
- Un système arduino branché

## Installation
1- Clone du dépôt Git
Dans git bash, saisir dans le dossier où l'on veut sauvegarder le code, la commande :
``` bash
 git clone https://github.com/NankNgSa/Enregistreur-videos-souris.git
 cd Enregistreur_Videos
```
2- Création de l'environnement virtuel (optionnel mais recommandé)
``` bash
  python -m venv .venv
  . .\.venv\Scripts\Activate.ps1
```

3- Installation des dépendances
``` bash
 pip install -r requirements.txt
```

## Lancement
1- S'assurer que SpinView est installé à cet emplacement :
- C:\Program Files\FLIR Systems\Spinnaker\bin64\vs2015\SpinView_WPF_v140.exe

2- Lancer le programme
Se placer dans le dossier du code puis lancer la commande :
``` bash
 python Souris/main.py
```









