# Fonctionnement de Fenetre_Principale
Ce document explique le but et le fonctionnement des méthodes du Fichier fenetre_principale.py

### 3- fermer_application(self)
#### But : 
Fermer proprement l'application 
#### Fonctionnement :
- Demande confirmation à l'utilisateur.
- Libère les ressources : trigger_recorder (caméra) et video_writer (écriture vidéo).
- Ferme la fenêtre (destroy()).

---

### 4- demarrer_cameraTrigger(self)
#### But : 
Démarrer l'enregistrement vidéo.
#### Fonctionnement :
- Récupère les valeurs des champs utilisateur (ID souris, date, dossier, durée, FPS, etc.).
- Valide les champs.
- Construit le chemin de sauvegarde (via construire_chemin_video()).
- Lance un thread avec lancer_capture_thread pour éviter de bloquer l’interface.
- Met à jour l'interface (status, désactive bouton, etc.).

---

### 5- lancer_capture_thread(...)
#### But : 
Gérer la capture vidéo dans un thread (séparé de l’interface graphique).
#### Fonctionnement :
- Appelle la fonction lancer_camera (du module CameraTrigger) avec tous les paramètres.
- Gère le retour (succès ou erreur) via des fenêtres messagebox et met à jour l'UI.
- Remet les boutons dans leur état initial après l’enregistrement.

---

### 6- lancer_apercu_camera(self)
#### But : 
Afficher un aperçu de la caméra (avant enregistrement).
#### Fonctionnement :
- Appelle afficher_apercu_camera() du module CameraTrigger, avec les dimensions choisies par l'utilisateur.
- Gère les erreurs d'entrée utilisateur (longueur/largeur invalides).

---

### 7- arreter_enregistrement(self)
#### But : 
Arrêter l'enregistrement vidéo en cours.
#### Fonctionnement :
- Change l’état de l’attribut arret_enregistrement à True, ce qui signalera au thread de capture de s’arrêter.
- Met à jour le label de statut.

---

### 8- __init__(self, fenetre=None)
#### But : 
Construire toute l’interface graphique.
#### Fonctionnement :
- Crée la fenêtre principale avec ses LabelFrame, Label, Entry, Button, etc.
- Lie les fonctions aux boutons.
- Initialise les champs (StringVar, Spinbox, etc.).
- Gère aussi l'événement de fermeture (croix rouge) pour appeler fermer_application

---

### 9- construire_chemin_video(dossier_base, id_souris, date_enregistrement)
#### But : 
Générer dynamiquement un chemin de sauvegarde vidéo.
#### Fonctionnement :
- Crée un dossier hiérarchisé : ```[dossier-parent]/[souris_id-<id>]/[yyyy-mm-dd]/.```
- Génère un nom de fichier horodaté ```souris-<id>_date.mp4.```
- Crée les dossiers si nécessaire (os.makedirs(..., exist_ok=True)).
- Retourne le chemin complet vers le fichier .mp4






