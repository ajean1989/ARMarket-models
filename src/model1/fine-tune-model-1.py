import sys
import os

import pandas as pd
import numpy as np

from PIL import Image

# Création du dataset
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(sys.path)

# Ouvrir les labels
labels = pd.read_csv("sku110k/annotations/annotations_train.csv", names = ["name","x1","y1","x2","y2","class","width","height"])

print(labels.columns)
print(labels.head())

# Ouvrir chaque image
for i in range(2) : 
    # rec first bb
    rows = labels[labels["name"]==f"train_{i}.jpg"]
    # intégrer objet scrappé pour meilleure res
    
    
    # im_crop = im_crop.rotate(np.random.randint(-45,45))
    
    # Superposer les deux images

    # Insertion du crop au milieu (avec un peu de random) de l'image originale avec un peu de rotation
    # width, eight = im.size
    # width_insertion = int(width/2 + 0.1*(np.random.randint(-100,100)/100)*width)
    # eight_insertion = int(eight/2 + 0.1*(np.random.randint(-100,100)/100)*eight)

    # im_crop = im_crop.resize((int(width/2), int(eight/2)))
    # im.paste(im_crop, (width_insertion,eight_insertion))

    # im.show()



# cropper un objet dedans et laisser une marge comprise entre 20 et 200 pixels aléatoire

# Formater pour yolo

# enregistrer l'image dans le dossier datasets/sku110k-close/images/

# enregistrer le txt dans le dossier datasets/sku110k-close/labels/


# entrainement à partir du modèle drazcat-AI




