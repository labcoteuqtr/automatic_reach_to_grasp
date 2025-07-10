from tkinter import *
from fenetre_principale import FenetrePrincipale


# lancer la fenetre principale
if __name__ == "__main__":
    root = Tk()
    app = FenetrePrincipale(root)
    root.protocol("WM_DELETE_WINDOW", app.fermer_application)
    root.mainloop()
