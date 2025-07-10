# Fonctionnement de Fichier validations.py
Ce document explique le but et le fonctionnement des méthodes du Fichier validations.py

### 1- est_un_nombre(nombre)
#### But : 
Vérifie si la valeur entrée est un nombre
#### Fonctionnement :
- Si le champ est vide ("") → retourne False.
- Si la chaîne contient uniquement des chiffres (isdigit()) :
- Elle est convertie en entier.
- Retourne True sinon False

---

### 2- choisir_dossier(...)
#### But : 
Construit un chemin de fichier vidéo simple sans structure hiérarchique de dossiers, et l’affiche dans un champ (entry_widget).
#### Fonctionnement :
- Définit un dossier de base : le répertoire utilisateur (~).
- Formate la date selon YYYY-MM-DD.
- Crée un nom de fichier vidéo au format :
_souris-id_date.avi_
- Construit le chemin complet.
- Efface et insère ce chemin dans le champ d’entrée (Tkinter).

---

### 3- creer_dossier(entry_widget, id_souris, date_enregistrement)
#### But : 
Permet à l’utilisateur de choisir un dossier de base, puis crée une arborescence de sous-dossiers pour enregistrer la vidéo.
#### Fonctionnement :
1. Affiche une boîte de dialogue pour choisir un dossier principal.
2. Récupère :
- L’ID de la souris
- La date (depuis un DateEntry comme tkcalendar)

3. Crée une hiérarchie :
```
dossier_parent/
    souris_id-<id_souris>/
        <date>/ 
            souris-<id_souris>_<date>.mp4
```
4. Écrit le chemin complet dans le champ de saisie (entry_widget).

---

### 4- lancer_enregistrement(id_souris, numero_essai, date_enregistrement)
#### But : 
Génère le chemin complet vers une vidéo d’expérimentation, avec sous-dossiers par souris et date.
#### Fonctionnement :
- Formate la date (YYYY-MM-DD).
- Construit une structure comme :
```
dossier_parent/
    souris_id-<id_souris>/
        <date>/ 
            souris-<id_souris>_<date>.mp4
```
- Crée les dossiers nécessaires (os.makedirs(...)).
- Retourne le chemin complet du fichier vidéo.









