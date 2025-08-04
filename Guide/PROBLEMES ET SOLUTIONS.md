# Fichier de résolution des problèmes
Ce document présente les erreurs rencontrées lors de l’utilisation du script `entrainer_classifier.py`, ainsi que les solutions appliquées.

## Erreur 1 : Unresolved reference 
- **Contexte** : Survenue lors de l'exécution du script `entrainer_classifier.py`.
- **Cause** : Les différents packages ne sont pas installés dans l'environnement virtuel actif.
- **Solution** : Procéder à l'installation des différents packages en exécutant la commande :
```` bash
    pip install -r requirements.txt
````
Ou alors procéder à l'installation manuelle et individuelle de chaque package en effectuant un clic droit sur
le nom du package en question et cliquer sur "Install package"






