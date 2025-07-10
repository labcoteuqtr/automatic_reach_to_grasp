# Guide d'installation du module "PySpin"
Ce module ne possède pas de commande pip pour l'installation directe.
Une installation manuelle est nécessaire.

1- Créer un environnement virtuel
```bash
    python -m venv .venv
```

2- Activer l'environnement virtuel
````bash
  . .\.venv\Scripts\Activate.ps1
````

3- Configurer PyCharm avec le nouvel environnement
- Aller dans File > Settings > Project: Souris > Python Interpreter
- Cliquer sur Paramètres (⚙)️ > Add Interpreter...
- Choisir : Existing environment
- Sélectionner C:\Souris\.venv\Scripts\python.exe
- Cliquer surr OK

4- Cliquer sur "Install requirements" en haut de l'editeur de code

5- Télécharger le fichier ".whl" correspondant à la version de python et de spinnaker.
Dans notre cas, il s'agit de "Spinnaker SDK 3.2.0.62 for Windows (May 31, 2024) version python 3.10"

6- Extraire les fichiers du dossier zip téléchargé

7- Installer le fichier ".whl" qui se trouve dans le dossier extrait avec la commande
````bash
  pip install C:\chemin-vers-le-fichier\spinnaker_python-3.2.0.62-cp310-cp310-win_amd64.whl
````

8- Pour vérifier que l'installation a bien été effectué, saisir la commande
````bash
python -c "import PySpin; print('PySpin est installé correctement !')
````

