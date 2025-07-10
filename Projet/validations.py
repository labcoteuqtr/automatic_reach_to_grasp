import os
from datetime import datetime
from tkinter import *
from tkinter import filedialog, messagebox

# verifie que le numero de l'essai est bien un nombre
def est_un_nombre(nombre):
    if nombre == "":
        return False
    if nombre.isdigit():
        val = int(nombre)
        return val
    return True

# cree le dossier dans lequel sera enregistré la video sans l'aborescence
def choisir_dossier(entry_widget, id_souris, date_enregistrement):
    # dossier par defaut
    dossier = os.path.join(os.path.expanduser("~"))
    os.makedirs(dossier, exist_ok=True)

    # format de la date : 2025-12-31
    date = date_enregistrement.get() if date_enregistrement.get() else datetime.now().strftime("%Y-%m-%d")

    nom_fichier = f"souris-{id_souris.get()}_{date}.avi"

    chemin_fichier = os.path.join(dossier, nom_fichier)

    entry_widget.delete(0, "end")
    entry_widget.insert(0, chemin_fichier)


# cree le dossier dans lequel sera enregistré la video avec l'aborescence
def creer_dossier(entry_widget, id_souris, date_enregistrement):
    # dossier_utilisateur = os.path.expanduser("~")  # represente le dossier principal de l'utilisateur : C://nanka//..//.
    dossier_utilisateur = filedialog.askdirectory(title="Choisir le dossier principal")
    if not dossier_utilisateur:
        return

    souris_id = id_souris.get().strip()
    date = date_enregistrement.get_date().strftime("%Y-%m-%d")  # retourne un objet date

    # construction de l'aborescence des fichiers
    dossier_souris = os.path.join(dossier_utilisateur, f"souris_id-{souris_id}")
    dossier_date = os.path.join(dossier_souris, date)
    os.makedirs(dossier_date, exist_ok=True)

    #nom_video = f"souris-{souris_id}_essai-{numero}_{date}"
    #chemin_video = os.path.join(dossier_date, nom_video)

    nom_fichier = f"souris-{souris_id}_{date}.mp4"
    chemin_video = os.path.join(dossier_date, nom_fichier)

    entry_widget.delete(0, "end")
    entry_widget.insert(0, chemin_video)


# lancer l'enregistrement de la video en ouvrant spinview
def lancer_enregistrement(id_souris, date_enregistrement):
    # chemin_video = entry_lien_enregistrement.get()
    champs =[
        (id_souris.get().strip(), "Veuillez entrer l'ID de la souris."),
        #(numero_essai.get().strip(), "Veuillez entrer le numero de l'essaie."),
        (date_enregistrement.get().strip(), "Veuillez entrer le date de l'enregistrement.")
    ]

    for valeur, message in champs:
        if not valeur:
            messagebox.showwarning("Champ manquant", message)
            return

    try:
        # ouvrir spinview
        chemin_spinview = r"C:\Program Files\FLIR Systems\Spinnaker\bin64\vs2015\SpinView_WPF_v140.exe"
        os.startfile(chemin_spinview)

    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de lancer SpinView :\n{e}")


# construire le dossier ou sera enregistré les videos
def construire_chemin_video(dossier_base, id_souris, numero_essai, date_enregistrement):
    """
    Construit le chemin complet de la vidéo principale :
    dossier_base/souris_id-xx/yyyy-mm-dd/souris-xx_yyyy-mm-dd.mp4
    """
    date_str = date_enregistrement.strftime("%Y-%m-%d")
    dossier_souris = os.path.join(dossier_base, f"souris_id-{id_souris}")
    dossier_date = os.path.join(dossier_souris, date_str)

    os.makedirs(dossier_date, exist_ok=True)

    nom_fichier = f"souris-{id_souris}_essai-{numero_essai}_{date_str}.mp4"
    chemin_video = os.path.join(dossier_date, nom_fichier)

    return chemin_video


