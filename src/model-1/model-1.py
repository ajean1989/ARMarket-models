import sys 

import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt

from segment_anything import SamAutomaticMaskGenerator, sam_model_registry, SamPredictor
from PIL import Image, ImageDraw

sys.path.append('../../../')
print(sys.path)





# SAM

# # Charger une image à partir d'un fichier
# pil_image = Image.open("data/img_test.jpg")
# # pil_image = Image.open("C:\\Users\\Adrien\\Desktop\\synchro\\github\\ARMarket\\models\\data\\img_test.jpg")
# image = np.array(pil_image)

# device = "cpu"

# sam = sam_model_registry["vit_h"](checkpoint="checkpoints/sam_vit_h.pth")
# sam.to(device=device)
# # sam = sam_model_registry["vit_h"](checkpoint="C:\\Users\\Adrien\\Desktop\\synchro\\github\\ARMarket\\models\\checkpoints\\sam_vit_h.pth")

# # Prédiction automatique sur toute l'image
# mask_generator = SamAutomaticMaskGenerator(sam)
# masks = mask_generator.generate(image)

# # prédiction avec un prompt
# # predictor = SamPredictor(sam)
# # predictor.set_image(image)
# # masks, _, _ = predictor.predict()


# print(len(masks))
# print(masks[0].keys())
# pprint(masks)



# def show_anns(anns):
#     if len(anns) == 0:
#         return
#     sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)
#     ax = plt.gca()
#     ax.set_autoscale_on(False)

#     img = np.ones((sorted_anns[0]['segmentation'].shape[0], sorted_anns[0]['segmentation'].shape[1], 4))
#     img[:,:,3] = 0
#     for ann in sorted_anns:
#         m = ann['segmentation']
#         color_mask = np.concatenate([np.random.random(3), [0.35]])
#         img[m] = color_mask
#     ax.imshow(img)


# plt.figure(figsize=(20,20))
# plt.imshow(image)
# show_anns(masks)
# plt.axis('off')
# plt.show() 







# Yolo V8 Tracker 

from ultralytics import YOLO

model = YOLO('checkpoints/yolov8x.pt') 

# results = model(source="https://www.youtube.com/watch?v=_bMyTB-J6FM", stream=True)




# for r in results:
#     print('---')
#     print(r)
#     print('---')

#     name = r.names
#     boxes = r.boxes  # Boxes object for bbox outputs
#     probs = r.probs  # Class probabilities for classification outputs
#     print('name : ', name, "\n boxes !!! : ", boxes.xyxy.cpu().numpy(), "\n box id : ", boxes.id, "\n box cls : ", boxes.cls.cpu().numpy())
#     im_array = r.plot()
#     # Créer un objet ImageDraw pour dessiner sur l'image
#     image_pil = Image.fromarray(im_array[..., ::-1])
#     draw = ImageDraw.Draw(image_pil)

#     # Supposons que vous ayez les résultats YOLO dans un objet "results" contenant les boîtes englobantes
#     # results.boxes contient les boîtes englobantes (bounding boxes) au format [x_min, y_min, x_max, y_max]
#     # results.labels contient les étiquettes de classe des objets détectés

#     for elt, cls in zip(boxes.xyxy.cpu().numpy(),boxes.cls.cpu().numpy()) :
#         if len(elt) > 0 :
#             x_min, y_min, x_max, y_max = elt
#             # Dessiner la boîte englobante
#             draw.rectangle([x_min, y_min, x_max, y_max], outline="red", width=2)
#             # Ajouter une étiquette de classe au-dessus de la boîte
#             draw.text((x_min, y_min), name[cls], fill="red")

#     # Afficher l'image avec les boîtes englobantes
#     image_pil.show()
#     res = input("continue any or 'q' for quit")
#     if res == "q" :
#         break







import cv2
from pytube import YouTube

# Open the video file
video_path = "https://www.youtube.com/watch?v=NG-de6quWkE"

yt = YouTube(video_path)
stream = yt.streams.get_highest_resolution()


cap = cv2.VideoCapture(stream.url)
print(cap)
if not cap.isOpened():
   print ("File Cannot be Opened")

minute_to_go = 4
sec_to_go = 20
fps = 30
time_to_go = minute_to_go*(60*fps)+sec_to_go*fps
frames = 10
frame_count = 0

# Loop through the video frames
while cap.isOpened():

    


    # Read a frame from the video
    success, frame = cap.read()

    print(frame_count)
    print(time_to_go)

    # if frame_count in range(time_to_go, time_to_go+frames)  :
    if frame_count > time_to_go :

        if success:
            # Run YOLOv8 inference on the frame
            results = model(frame)

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            im = Image.fromarray(annotated_frame[..., ::-1])  # RGB PIL image
            im.show()

            # Display the annotated frame
            # cv2.imshow("YOLOv8 Inference", annotated_frame)

            res = input("continue any or 'q' for quit : ")
            if res == "q" :
                break
        
    frame_count += 1


cap.release()
cv2.destroyAllWindows()




# Conserver les images où il y a une bounding box avec la class 'items' avec l'ID du track dans un dossier temp

# Faire une detection sur les images temp si code barre

# Si code barre, repérer s l'ID de la bb sur lequel il se trouve

# Conserver les images où le trouve l'ID et traitement pour transformer en dataset  xyxy, xywh, wywyn, wywhn