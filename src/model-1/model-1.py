import sys 

import numpy as np
import matplotlib.pyplot as plt

from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
from PIL import Image

# Charger une image à partir d'un fichier
pil_image = Image.open("C:\\Users\\Adrien\\Desktop\\synchro\\github\\ARMarket\\models\\data\\img_test.jpg")
image = np.array(pil_image)

sys.path.append("c:\\Python\\Python311\\venv\\ARMarket_models\\models")
print(sys.path)

sam = sam_model_registry["vit_h"](checkpoint="C:\\Users\\Adrien\\Desktop\\synchro\\github\\ARMarket\\models\\checkpoints\\sam_vit_h.pth")
mask_generator = SamAutomaticMaskGenerator(sam)
masks = mask_generator.generate(image)

print(len(masks))
print(masks[0].keys())



def show_anns(anns):
    if len(anns) == 0:
        return
    sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)
    ax = plt.gca()
    ax.set_autoscale_on(False)

    img = np.ones((sorted_anns[0]['segmentation'].shape[0], sorted_anns[0]['segmentation'].shape[1], 4))
    img[:,:,3] = 0
    for ann in sorted_anns:
        m = ann['segmentation']
        color_mask = np.concatenate([np.random.random(3), [0.35]])
        img[m] = color_mask
    ax.imshow(img)




plt.figure(figsize=(20,20))
plt.imshow(image)
show_anns(masks)
plt.axis('off')
plt.show() 

