import sys
import os

import pandas as pd

from PIL import Image

# Création du dataset
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(sys.path)

# Ouvrir les labels
labels = pd.read_csv("sku110k/annotations/annotations_train.csv")

print(labels.columns)

# Ouvrir chaque image
for i in range(5) : 
    pass
    # rec first bb
    # labels[labels]
    # im = Image(f"sku110k/image/train_{i}")


# cropper un objet dedans et laisser une marge comprise entre 20 et 200 pixels aléatoire

# Formater pour yolo

# enregistrer l'image dans le dossier datasets/sku110k-close/images/

# enregistrer le txt dans le dossier datasets/sku110k-close/labels/


# entrainement à partir du modèle drazcat-AI




