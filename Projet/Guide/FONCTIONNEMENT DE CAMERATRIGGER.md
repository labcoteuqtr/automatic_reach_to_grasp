# Fonctionnement de Fichier CameraTrigger.py
Ce document explique le but et le fonctionnement des méthodes de Fichier CameraTrigger.py

### 1- afficher_apercu_camera(longueur=640, largeur=480)
#### But : 
Affiche en direct l'image de la caméra dans une fenêtre OpenCV pour prévisualisation.

#### Fonctionnement :
Initialise le système FLIR (PySpin) et récupère la première caméra.
Configure la caméra via configurer_camera(...).
Lance l'acquisition et montre chaque image capturée dans une fenêtre.
Quitte si l'utilisateur appuie sur q ou ferme la fenêtre.

---

### 2- configurer_camera(cam, longueur, largeur)
#### But : 
Applique les paramètres physiques de capture à la caméra.

#### Fonctionnement :
Définit :
- la taille d’image (width, height)
- les offsets (région de la caméra à capturer)
- le format de pixels (ici Mono8 pour N&B)
- les coefficients de binning (compression spatiale)
- l’activation et la valeur du gamma (contraste/éclairage)
- Utilise les API PySpin pour accéder aux nœuds de configuration.

---

### 3- lancer_camera(...)
#### But : 
Lance un enregistrement vidéo longue durée, en parallèle avec l'enregistrement de mini-vidéos déclenchées par Arduino. 

#### Fonctionnement :
1. Préparation :
- Crée les dossiers nécessaires. 
- Crée un fichier .txt de log pour noter l’ID souris et la date.

2. Initialisation caméra :
- Récupère la première caméra disponible.
- Configure les paramètres d’acquisition (exposition, gain, framerate, etc.)

3. Vidéo principale :
- Utilise cv2.VideoWriter pour enregistrer une vidéo principale continue.
- Boucle jusqu'à la durée souhaitée (ou arrêt manuel).
- Enregistre les images dans la vidéo principale et met à jour le compteur de frames.

4. Mini-vidéos :
- Utilise un objet VideoTriggerRecorder (gère déclenchements Arduino).
- Chaque déclenchement démarre l’enregistrement d’une mini-vidéo dans le dossier prise.

5. Fin d'enregistrement :
- Libère les ressources (caméra, vidéo, PySpin).
- Lit les données envoyées par Arduino à la fin via lire_arduino().
- Écrit les données Arduino dans le fichier .txt.

---

### 4- lire_arduino()
#### But : 
Lit une ligne de texte depuis l'Arduino à la fin de l'enregistrement.

#### Fonctionnement :
- Ouvre une connexion série (serial.Serial) sur le port COM.
- Lit une ligne avec timeout de CINQ secondes.
- Ferme la connexion et retourne la chaîne lue.











