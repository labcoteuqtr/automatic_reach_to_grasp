# Fichier de résolution des problèmes
Ce document présente les erreurs rencontrées lors de l’utilisation du script `CameraRoll.py`, ainsi que les solutions appliquées.

## Erreur 1 : ModuleNotFoundError: No module named 'PySpin'
- **Contexte** : Survenue lors de l'exécution du script `cameraTrigger.py`.
- **Cause** : Le module `PySpin` n'était pas installé dans l'environnement virtuel actif.
- **Solution** : Consulter le fichier INSTALLATION PYSPIN


## Erreur 2 : A module that was compiled using NumPy 1.x cannot be run in NumPy 2.2.6 as it may crash. 
- **Contexte** : Survenue lors de l'exécution du script `cameraTrigger.py`.
- **Cause** : Les modules compilés contre NumPy 1.x utilisent une interface binaire qui n’est plus complètement compatible avec NumPy 2.x.
- **Solution** : Downgrade NumPy à une version < 2 pour assurer la compatibilité avec les modules compilés :
    ``` bash
    pip install numpy<2
    ```

## Erreur 3 :  ffmpeg/ffprobe not found in path: C:/FLIRcamera/ffmpeg-master-latest-win64-gpl/bin/
- **Contexte** : Survenue lors de l'exécution du script `cameraTrigger.py`.
- **Cause** : Le module skvideo ne trouve pas ffmpeg.exe et ffprobe.exe dans le chemin système ou dans le chemin indiqué (C:/FLIRcamera/ffmpeg-master-latest-win64-gpl/bin/).
- **Solution** :
### Étapes :
1. Ajouter FFmpeg au PATH système dans les variables d'environnement
. Vérifie que les fichiers suivants (ffmpeg.exe, ffprobe.exe) existent dans :
C:\FLIRcamera\ffmpeg-7.1.1-full_build\bin
. Si c'est le cas, ajouter cechemin au PATH système
  Ouvre les Paramètres système avancés.
  Clique sur Variables d’environnement.
  Dans les variables utilisateur ou système, trouve Path, clique sur Modifier, puis ajoute :
``` bash
      C:\FLIRcamera\ffmpeg-master-latest-win64-gpl\bin
 ```
  
ou dans le code, remplacer la ligne
``` bash
        C:\FLIRcamera\ffmpeg-master-latest-win64-gpl\bin
```
par
``` bash
        C:/FLIRcamera/ffmpeg-7.1.1-full_build/bin
```

## Erreur 4: IOError("Serial device not found! Connect the behavioral box to computer")
- **Contexte** : Survenue lors de l'exécution du script `cameraTrigger.py`.
- **Cause** : le script CameraRoll.py ne détecte pas de périphérique série (arduino ou microcontrôleur) connecté à l'ordinateur
- **Solution** : 
1. Vérifier que le périphérique est bien connecté en USB.
  2. Trouver le bon port COM via PowerShell :
     ```powershell
     mode
     ```
     ou dans le **Gestionnaire de périphériques** (section Ports COM).
  3. Modifier le script pour utiliser le bon port :
     ```python
     ser = serial.Serial('COM3', 9600)
     ```
  4. Option avancée : automatiser la détection avec `serial.tools.list_ports`.

## Erreur 5 : cannot find installation of real FFmpeg (which comes with ffprobe)
- **Contexte** : Survenue lors de l'exécution du code
- **Cause** : Le système ne trouve pas une installation valide de FFmpeg
- **Solution** : Le système ne trouve pas une installation valide de FFmpeg
1. Télécharger FFmpeg [https://ffmpeg.org/download.html]()
- Pour Windows : suivez le lien vers Gyan.dev ou BtbN builds.
- Téléchargez l'archive release full (ex. : ffmpeg-release-full.7z ou .zip)
2. Décompresser et installer
Placez ce dossier quelque part accessible, par exemple :
C:\ffmpeg\
3. Ajouter FFmpeg au PATH
Ouvrez le menu Démarrer > tapez "variables d’environnement" et ouvrez l’option "Modifier les variables d’environnement du système"
Dans la section "Variables système" :
Trouvez Path > cliquez sur Modifier
Cliquez sur Nouveau et ajoutez le chemin vers le dossier bin de FFmpeg, par exemple :
   ```bash
     C:\ffmpeg\bin\reste-du-chemin
   ```







