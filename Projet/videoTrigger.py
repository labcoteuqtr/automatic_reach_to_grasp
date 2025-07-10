import os
import cv2
import serial
import time
from datetime import datetime
from collections import deque

class VideoTriggerRecorder:
    def __init__(self, cam, dossier_mini_video, frame_rate=5.0, buffer_seconds=3, com_port='COM3', baud_rate=9600):
        self.cam = cam
        self.dossier_mini_video = dossier_mini_video
        self.frame_rate = frame_rate
        self.buffer_size = int(frame_rate * buffer_seconds)
        self.pre_trigger_buffer = deque(maxlen=self.buffer_size)
        self.triggered = False
        self.post_trigger_counter = 0
        self.video_writer = None
        self.width = self.cam.Width.GetValue()
        self.height = self.cam.Height.GetValue()
        self.ser = serial.Serial(com_port, baud_rate, timeout=1)  # ️ ouverture constante
        self.frame_count = 0  # compteur pour le diagnostic
        self.derniere_ligne = ""  # garder en memoire la derniere ligne lu sur la console
        self.derniere_detection = 0
        self.temps_attente = 3  # secondes à attendre entre deux triggers


    def maj(self, frame):
        self.pre_trigger_buffer.append(frame)
        self.frame_count += 1  # <- compteur incrémenté

        if not self.triggered and self.detecter_trigger():
            print("[Déclenchement] Objet détecté par capteur Arduino")
            self.commencer_enregistrer_video(self.dossier_mini_video)
            self.triggered = True
            self.post_trigger_counter = self.buffer_size

        if self.triggered:
            self.video_writer.write(frame)
            self.post_trigger_counter -= 1
            if self.post_trigger_counter <= 0:
                self.arret_enregistrer_video()

    def detecter_trigger(self):
        try:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').strip()
                if line != self.derniere_ligne:
                    print(f"[Arduino dit] {line}") ###
                    self.derniere_ligne = line

                if "ENCENDIDO" in line.upper():
                    maintenant = time.time()
                    if maintenant - self.derniere_detection > self.temps_attente:
                        self.derniere_detection = maintenant
                        return True

                #return "ENCENDIDO" in line.upper()  # remplacer encendio par trigger plutard
            return False
        except Exception as e:
            print(f"[Erreur Arduino] {e}")
            return False

    def commencer_enregistrer_video(self, dossier_mini_video):
        # print(f"[DEBUG] appelé avec self={self} et dossier_mini_video={dossier_mini_video}")
        date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        #dossier = os.path.join("C:/FLIRcamera/Vidéos_Souris", "evenements")
        os.makedirs(dossier_mini_video, exist_ok=True)

        path = os.path.join(dossier_mini_video, f"evenement_{date_str}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter(path, fourcc, self.frame_rate, (self.width, self.height))

        if not self.video_writer.isOpened():
            print(f"[ERREUR] Impossible d'ouvrir le fichier vidéo : {path}")
            self.video_writer = None
            return

        print(f"[INFO] Début enregistrement événement : {path}")

        # Enregistrer les frames précédentes
        for frame in self.pre_trigger_buffer:
            # self.video_writer.write(frame)
            if frame is not None and frame.shape[0] == self.height and frame.shape[1] == self.width:
                self.video_writer.write(frame)
            else:
                print("[AVERTISSEMENT] Frame invalide ignorée.")

    def arret_enregistrer_video(self):
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
            print("[INFO] Fin de l'enregistrement événement")
        self.triggered = False

    def fermer(self):
        if self.video_writer:
            print("[INFO] Fermeture en cours : vidéo principale...")
            self.video_writer.release()
            self.video_writer = None
        if self.ser and self.ser.is_open:
            print("[INFO] Fermeture du port série...")
            self.ser.close()


