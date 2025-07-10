from tkinter import *
from tkinter import messagebox
from validations import *
from tkcalendar import DateEntry
from CameraTrigger import lancer_camera, afficher_apercu_camera
import threading
import os
import time

class FenetrePrincipale(Frame):
    def fermer_application(self):
        reponse = messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter ?")
        if reponse:
            print("Fermeture sécurisée de l'application.")
            try:
                if hasattr(self, "trigger_recorder") and self.trigger_recorder:
                    self.trigger_recorder.fermer()
                if hasattr(self, "video_writer") and self.video_writer:
                    self.video_writer.release()
            except Exception as e:
                print(f"Erreur pendant la fermeture : {e}")
            self.master.destroy()

    def demarrer_cameraTrigger(self):
        id_souris = self.value_souris_id.get().strip()
        date_enregistrement = self.entry_date_enregistrement.get_date()
        chemin_ou_dossier = self.entry_lien_enregistrement.get().strip()

        if not id_souris or not date_enregistrement or not chemin_ou_dossier:
            messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs.")
            return

        try:
            if chemin_ou_dossier.endswith(".mp4"):
                chemin_video = chemin_ou_dossier
            else:
                chemin_video = construire_chemin_video(chemin_ou_dossier, id_souris, date_enregistrement)

            print("CHEMIN FINAL :", chemin_video)

            duree = int(self.value_duree.get())
            frame_rate = int(self.value_frame_rate.get())
            longueur = int(self.value_longueur.get())
            largeur = int(self.value_largeur.get())

            FACTEUR_RALENTI = 1
            frame_rate_lecture = frame_rate / FACTEUR_RALENTI

            nb_images = frame_rate * duree
            duree_lue = nb_images / frame_rate_lecture
            print(f"[DEBUG] Frame rate enregistrement : {frame_rate} FPS")
            print(f"[DEBUG] Frame rate lecture       : {frame_rate_lecture:.2f} FPS")
            print(f"[DEBUG] Durée réelle             : {duree} s")
            print(f"[DEBUG] Durée vidéo ralentie     : {duree_lue:.2f} s")

        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de construire le chemin vidéo :\n{e} ")
            return

        self.bouton_enregistrer.config(state=DISABLED)
        self.label_status.config(text="Enregistrement en cours...")
        self.bouton_arreter.config(state=NORMAL)
        self.arret_enregistrement = False

        thread = threading.Thread(
            target=self.lancer_capture_thread,
            args=(id_souris, date_enregistrement, chemin_video, duree, frame_rate, frame_rate_lecture, longueur, largeur),
            daemon=True
        )
        thread.start()

    def lancer_capture_thread(self, id_souris, date_enregistrement, chemin_video, duree, frame_rate, frame_rate_lecture, longueur, largeur):
        try:
            self.enregistrement_en_cours = True
            success, self.trigger_recorder, self.video_writer = lancer_camera(
                id_souris,
                date_enregistrement.strftime("%Y-%m-%d"),
                chemin_video,
                duree,
                frame_rate,
                frame_rate_lecture,
                longueur,
                largeur,
                arret_condition=lambda: self.arret_enregistrement
            )
            if success:
                self.fenetre.after(0, lambda: messagebox.showinfo("Succès", "L'enregistrement a démarré avec succès."))
            else:
                self.fenetre.after(0, lambda: messagebox.showerror("Erreur", "Lancement échoué."))
        except Exception as e:
            self.fenetre.after(0, lambda: messagebox.showerror("Erreur", f"Échec de l'enregistrement :\n{e}"))
        finally:
            self.enregistrement_en_cours = False
            self.fenetre.after(0, lambda: self.bouton_enregistrer.config(state=NORMAL))
            self.fenetre.after(0, lambda: self.label_status.config(text="Prêt"))

    def lancer_apercu_camera(self):
        try:
            longueur = int(self.value_longueur.get())
            largeur = int(self.value_largeur.get())
            afficher_apercu_camera(longueur=longueur, largeur=largeur)
        except ValueError:
            messagebox.showerror("Erreur", "Longueur ou largeur invalide pour l'aperçu.")

    def arreter_enregistrement(self):
        if self.enregistrement_en_cours:
            self.arret_enregistrement = True
            self.label_status.config(text="Arrêt en cours...")

    def __init__(self, fenetre=None):
        super().__init__(fenetre)
        self.fenetre = fenetre
        self.trigger_recorder = None
        self.video_writer = None
        self.fenetre.protocol("WM_DELETE_WINDOW", self.fermer_application)
        self.enregistrement_en_cours = False
        self.fenetre.geometry("800x600")
        self.fenetre.title("Enregistrement des vidéos de souris")
        self.pack(fill=BOTH, expand=True)
        self.arret_enregistrement = False

        label = Label(self.fenetre, text="Enregistrement des vidéos de souris")
        label.pack()

        self.frame1 = LabelFrame(self, borderwidth=2, relief=SUNKEN, text="Nom de la vidéo")
        self.frame1.pack(padx=10, pady=10, fill=X)

        Label(self.frame1, text="ID souris").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.value_souris_id = StringVar()
        Entry(self.frame1, textvariable=self.value_souris_id, width=30).grid(row=0, column=1, padx=5, pady=5)

        vcmd = self.register(est_un_nombre)

        Label(self.frame1, text="Date de l'enregistrement").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_date_enregistrement = DateEntry(
            self.frame1,
            width=27,
            borderwidth=2,
            background="darkblue",
            foreground="white",
            date_pattern='yyyy-mm-dd'
        )
        self.entry_date_enregistrement.grid(row=2, column=1, padx=5, pady=5)

        self.frame2 = LabelFrame(self, borderwidth=2, relief=SUNKEN, text="Lien d'enregistrement de la vidéo")
        self.frame2.pack(padx=10, pady=10, fill=X)

        Label(self.frame2, text="Lien de la vidéo").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_lien_enregistrement = Entry(self.frame2, width=50)
        self.entry_lien_enregistrement.grid(row=0, column=1, padx=5, pady=5)

        Button(
            self.frame2,
            text="Choisir le dossier principal",
            command=lambda: creer_dossier(
                self.entry_lien_enregistrement,
                self.value_souris_id,
                self.entry_date_enregistrement
            )
        ).grid(row=0, column=2, padx=5, pady=5)

        self.frame4 = LabelFrame(self, borderwidth=2, relief=SUNKEN, text="Paramètre de la caméra")
        self.frame4.pack(padx=10, pady=10, fill=X)

        Label(self.frame4, text="Durée de l'enregistrement en secondes").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.value_duree = StringVar(value="600")
        Spinbox(self.frame4, from_=1, to=1200, textvariable=self.value_duree, width=28,
                validate='key', validatecommand=(vcmd, '%P')).grid(row=1, column=1, padx=5, pady=5)

        Label(self.frame4, text="Nombre de frames").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.value_frame_rate = StringVar(value="150")
        Spinbox(self.frame4, from_=1, to=1200, textvariable=self.value_frame_rate, width=28,
                validate='key', validatecommand=(vcmd, '%P')).grid(row=2, column=1, padx=5, pady=5)

        Label(self.frame4, text="Longueur").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.value_longueur = StringVar(value="500")
        Spinbox(self.frame4, from_=1, to=1200, textvariable=self.value_longueur, width=28,
                validate='key', validatecommand=(vcmd, '%P')).grid(row=3, column=1, padx=5, pady=5)

        Label(self.frame4, text="Largeur").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.value_largeur = StringVar(value="300")
        Spinbox(self.frame4, from_=1, to=1200, textvariable=self.value_largeur, width=28,
                validate='key', validatecommand=(vcmd, '%P')).grid(row=4, column=1, padx=5, pady=5)

        self.frame3 = LabelFrame(self, borderwidth=2)
        self.frame3.pack(pady=20)

        Button(
            self.frame3,
            text="Aperçu caméra",
            command=self.lancer_apercu_camera,
            bg="blue",
            fg="white",
            padx=10,
            pady=5
        ).pack(pady=5)

        self.bouton_enregistrer = Button(
            self.frame3,
            text="Lancer l'enregistrement",
            command=self.demarrer_cameraTrigger,
            bg="green",
            fg="white",
            padx=10,
            pady=5
        )
        self.bouton_enregistrer.pack()

        self.bouton_arreter = Button(
            self.frame3,
            text="Arrêter l'enregistrement",
            command=self.arreter_enregistrement,
            bg="red",
            fg="white",
            padx=10,
            pady=5,
            state=DISABLED
        )
        self.bouton_arreter.pack()

        self.label_status = Label(self.frame3, text="Prêt")
        self.label_status.pack(pady=5)


def construire_chemin_video(dossier_base, id_souris, date_enregistrement):
    date_str = date_enregistrement.strftime("%Y-%m-%d")
    timestamp = time.strftime("%H-%M-%S")
    dossier_souris = os.path.join(dossier_base, f"souris_id-{id_souris}", date_str)
    os.makedirs(dossier_souris, exist_ok=True)
    nom_fichier = f"souris-{id_souris}_{date_str}_{timestamp}.mp4"
    chemin_video = os.path.join(dossier_souris, nom_fichier)
    return chemin_video
