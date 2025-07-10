import os.path
import time
from datetime import datetime
from tkinter import messagebox

from validations import construire_chemin_video
from videoTrigger import VideoTriggerRecorder

import PySpin
import cv2
import serial
import io

# constantes de configuration camera
WIDTH = 640  # largeur
HEIGHT = 600  # longueur
OFFSET_X = 620
OFFSET_Y = 316
PIXEL_FORMAT = "Mono8"
BINNING_H = 1
BINNING_V = 1
GAMMA_ENABLED = True
GAMMA_VALUE = 0.8

# Constantes d'acquisition
EXPOSURE = 3500.0        # µs
GAIN = 10.0              # dB
FRAME_RATE = 30.0         # Hz
FRAME_RATE_RALENTI = 1
DURATION = 300             # durée de l'enregistrement en secondes

# communication arduino
COM_PORT = 'COM3'
BAUD_RATE = 9600

# fichier video
FILENAME_ROOT = 'mouse_'


def afficher_apercu_camera(longueur=640, largeur=480):
    print("Ouverture de la caméra pour aperçu...")
    system = PySpin.System.GetInstance()
    cam_list = system.GetCameras()

    if cam_list.GetSize() == 0:
        print("Aucune caméra détectée.")
        messagebox.showwarning("Caméra", "Aucune caméra détectée.")
        return

    cam = cam_list[0]
    cam.Init()
    configurer_camera(cam, longueur, largeur)

    cam.BeginAcquisition()
    print("Appuyez sur 'q' ou fermez la fenêtre pour arrêter l'aperçu.")

    window_name = 'Apercu - Camera FLIR'

    while True:
        image_result = cam.GetNextImage(1000)

        if image_result.IsIncomplete():
            print("Image incomplète.")
            image_result.Release()
            continue

        img_data = image_result.GetNDArray()
        img_bgr = cv2.cvtColor(img_data, cv2.COLOR_GRAY2BGR) if len(img_data.shape) == 2 else img_data

        cv2.imshow(window_name, img_bgr)
        image_result.Release()

        # verifie si 'q' est pressé ou si la fenetre a ete fermee
        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break

    cam.EndAcquisition()
    cam.DeInit()
    del cam
    cam_list.Clear()
    system.ReleaseInstance()
    cv2.destroyAllWindows()
    print("Aperçu fermé.")


def configurer_camera(cam, longueur, largeur):
    nodemap = cam.GetNodeMap()

    # largeur et hauteur
    width_node = PySpin.CIntegerPtr(nodemap.GetNode("Width"))
    height_node = PySpin.CIntegerPtr(nodemap.GetNode("Height"))
    if PySpin.IsWritable(width_node):
        width_node.SetValue(min(width_node.GetMax(), longueur))
    if PySpin.IsWritable(height_node):
        height_node.SetValue(min(height_node.GetMax(), largeur))

    # offsets
    offset_x = PySpin.CIntegerPtr(nodemap.GetNode("OffsetX"))
    offset_y = PySpin.CIntegerPtr(nodemap.GetNode("OffsetY"))
    if PySpin.IsWritable(offset_x):
        offset_x.SetValue(OFFSET_X)
    if PySpin.IsWritable(offset_y):
        offset_y.SetValue(OFFSET_Y)

    # pixel
    pixel_format = PySpin.CEnumerationPtr(nodemap.GetNode("PixelFormat"))
    if PySpin.IsWritable(pixel_format):
        fmt_entry = pixel_format.GetEntryByName(PIXEL_FORMAT)
        if PySpin.IsAvailable(fmt_entry) and PySpin.IsReadable(fmt_entry):
            pixel_format.SetIntValue(fmt_entry.GetValue())

    # binning
    bin_h = PySpin.CIntegerPtr(nodemap.GetNode("BinningHorizontal"))
    bin_v = PySpin.CIntegerPtr(nodemap.GetNode("BinningVertical"))
    if PySpin.IsWritable(bin_h):
        bin_h.SetValue(BINNING_H)
    if PySpin.IsWritable(bin_v):
        bin_v.SetValue(BINNING_V)

    # gamma
    gamma_enable = PySpin.CBooleanPtr(nodemap.GetNode("GammaEnable"))
    gamma = PySpin.CFloatPtr(nodemap.GetNode("Gamma"))
    if PySpin.IsWritable(gamma_enable):
        gamma_enable.SetValue(GAMMA_ENABLED)
    if PySpin.IsWritable(gamma):
        gamma.SetValue(GAMMA_VALUE)

    print(f"Caméra configurée à {WIDTH}x{HEIGHT}, Offset ({OFFSET_X},{OFFSET_Y}), {PIXEL_FORMAT}, Gamma {GAMMA_VALUE}")


def lancer_camera(mouse_id, date_str, chemin_video, duree, frame_rate_acquisition, frame_rate_lecture, longueur, largeur, arret_condition=lambda: False):
    system = None
    cam = None
    video_writer = None
    trigger_recorder = None
    try:
        # ajouter le dossier "prise" au dossier contenant la vidéo
        dossier_date = os.path.dirname(chemin_video)
        dossier_mini_video = os.path.join(dossier_date, "prise")
        os.makedirs(dossier_mini_video, exist_ok=True)

        log_path = chemin_video.replace(".mp4", ".txt")
        print(f"VIDÉO ENREGISTRÉE DANS : {chemin_video}")

        # log de ce qui se passe
        with open(log_path, 'w', encoding='utf-8') as log_file:
            #log_file.write(f"Trial: {trial_number}\n")
            log_file.write(f"Mouse ID: {mouse_id}\n")
            log_file.write(f"Date: {date_str}\n")

        #  initialiser camera
        system = PySpin.System.GetInstance()
        cam_list = system.GetCameras()
        if cam_list.GetSize() == 0:
            raise Exception("Aucune caméra FLIR détectée.")
        cam = cam_list[0]
        cam.Init()
        configurer_camera(cam, longueur, largeur)

        # Mode de buffer : éviter blocages si lecture trop lente
        #stream_nodemap = cam.GetTLStreamNodeMap()
        #handling_mode = PySpin.CEnumerationPtr(stream_nodemap.GetNode("StreamBufferHandlingMode"))
        #if PySpin.IsWritable(handling_mode):
            #newest_only = handling_mode.GetEntryByName("NewestOnly")
            #if PySpin.IsAvailable(newest_only) and PySpin.IsReadable(newest_only):
                #handling_mode.SetIntValue(newest_only.GetValue())
                #print("[INFO] Mode de buffer réglé sur 'NewestOnly'")


        # Paramètres manuels
        if PySpin.IsWritable(cam.ExposureAuto):
            cam.ExposureAuto.SetValue(PySpin.ExposureAuto_Off)
        if PySpin.IsWritable(cam.ExposureTime):
            cam.ExposureTime.SetValue(EXPOSURE)
        if PySpin.IsWritable(cam.Gain):
            cam.Gain.SetValue(GAIN)
        if PySpin.IsWritable(cam.AcquisitionFrameRateEnable):
            cam.AcquisitionFrameRateEnable.SetValue(True)
        if PySpin.IsWritable(cam.AcquisitionFrameRate):
            cam.AcquisitionFrameRate.SetValue(frame_rate_acquisition)
        if PySpin.IsWritable(cam.Width):
            cam.Width.SetValue(min(cam.Width.GetMax(), longueur))
        if PySpin.IsWritable(cam.Height):
            cam.Height.SetValue(min(cam.Height.GetMax(), largeur))


        actual_rate = cam.AcquisitionFrameRate.GetValue()
        print(f"[INFO] Frame rate réel appliqué à la caméra : {actual_rate:.2f} FPS")

        # width = cam.Width.GetValue()
        # height = cam.Height.GetValue()

        # VideoWriter pour vidéo finale (lecture)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(chemin_video, fourcc, frame_rate_lecture, (longueur, largeur), isColor=False)  # changer en wight et height

        trigger_recorder = VideoTriggerRecorder(
            cam,
            dossier_mini_video=dossier_mini_video,
            frame_rate=frame_rate_acquisition,
            com_port=COM_PORT,
            baud_rate=BAUD_RATE
        )
        trigger_recorder.commencer_enregistrer_video(dossier_mini_video)
        trigger_recorder.frame_count = 0

        cam.BeginAcquisition()
        print("Début acquisition vidéo...")
        start_time = time.time()

        while time.time() - start_time < duree:
            image_result = cam.GetNextImage(1000)
            if image_result.IsIncomplete():
                print("Image incomplète")
                image_result.Release()
                continue
            if arret_condition():
                print("[INFO] Arrêt manuel de la vidéo")
                break

            img_data = image_result.GetNDArray()

            img_bgr = cv2.cvtColor(img_data, cv2.COLOR_GRAY2BGR) if len(img_data.shape) == 2 else img_data

            #trigger_recorder.maj(img_bgr)  # gerer l'enregistrement des petites videos
            #video_writer.write(img_bgr)
            # Ne pas convertir en couleur pour gagner du temps
            trigger_recorder.frame_count += 1
            video_writer.write(img_data)  # img_data est en niveaux de gris

            image_result.Release()

        cam.EndAcquisition()
        elapsed = time.time() - start_time
        print(f"[INFO] Temps écoulé : {elapsed:.2f} s")
        print(f"[INFO] Frames capturées : {trigger_recorder.frame_count}")
        print(f"[INFO] Frame rate effectif : {trigger_recorder.frame_count / elapsed:.2f} FPS")

        cam.DeInit()
        del cam

        video_writer.release()
        trigger_recorder.fermer()

        print("Vidéo enregistrée :", chemin_video)

        arduino_data = lire_arduino()
        with open(log_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"Arduino data: {arduino_data}\n")

        print("Enregistrement terminé avec succès.")
        return True, trigger_recorder, video_writer

    except Exception as e:
        print(f"Erreur pendant l'acquisition : {e}")
        return False, None, None

    finally:
        if cam is not None:
            try:
                cam.DeInit()
            except:
                pass
        if system is not None:
            system.ReleaseInstance()


# a partir du systeme arduino, recuperer les donnees
def lire_arduino():
    try:
        ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=5)
        ser_io = io.TextIOWrapper(io.BufferedRWPair(ser, ser), encoding='utf-8', errors='replace')
        print("Lecture depuis Arduino...")
        line = ser_io.readline().strip()
        ser.close()
        return line
    except Exception as e:
        print(f"Erreur de lecture Arduino : {e}")
        return "Erreur de lecture"

