
import re
import os
import time

from random import randint
import pandas as pd

from PIL import Image
from ultralytics import YOLO
import cv2
from pyzbar.pyzbar import decode

# reset for tests
mode ='test'

if mode == "test":
    temp = os.listdir(os.path.join("src","model-1","datasets","bottle_dataset","temp"))
    for img in temp: 
        os.remove(os.path.join("src","model-1","datasets","bottle_dataset","temp",img))
    dataset = os.listdir(os.path.join("src","model-1","datasets","bottle_dataset","dataset"))
    for img in dataset: 
        os.remove(os.path.join("src","model-1","datasets","bottle_dataset","dataset",img))

# var init
model = YOLO('checkpoints/yolov8x.pt') 

video_link = "data/multiple_bottles_3.mp4"

cap = cv2.VideoCapture(video_link)

frame_count = 0

detected = pd.DataFrame(columns=["name","id","bbxyxy","bbxywhn","code"])

while cap.isOpened():

    # Read a frame from the video
    success, frame = cap.read()
    # if frame_count%5 == 0 :
    if success:

        # Run YOLOv8 inference on the frame
        results = model.track(frame, persist=True, classes = [39,41] , conf=0.1, tracker="tracker/custom_botsort.yaml")
        
        # Visualize the results on the frame
        # annotated_frame = results[0].plot()

        for r in results :
            # r = chaque détection au sein d'une frame

            if len(r.boxes.xyxy) == 0 :
                break

            try :
                    print("id = ", r.boxes.id.int().cpu().tolist())
                    print('---')
                    print("class = ", r.boxes.cls)
                    print('---')
            except : 
                continue

            # Visualize the results on the frame
            # annotated_frame = results[0].plot()
            # im = Image.fromarray(annotated_frame[..., ::-1])  # RGB PIL image
            # im.show()

            # enregistrer l'image dans temp : nom = timestamp+randint(1024)
            name = f"img_{str(int(time.time()))}_{randint(0,1023)}.png"
            path = os.path.join("src","model-1","datasets","bottle_dataset","temp",name)
            Image.fromarray(frame[:,:,::-1]).save(path,'PNG')

            # !!!! une ligne par id !!!
            # garder une trace (dict["nom","id","bb","code"]) du nom des fichiers + ID + bb enregristrer pour ajouter le label par la suite ou effacer
            id = r.boxes.id.int().cpu().tolist()[0]
            bbxyxy = r.boxes.xyxy[0].cpu().numpy() #[x1,y1,x2,y2]
            bbxywhn = r.boxes.xywhn[0].cpu().numpy() #[x1,y1,x2,y2]

            detected.loc[len(detected)] = [name, id, bbxyxy, bbxywhn, 0]
            
    else:
        # Break the loop if the end of the video is reached
        break

    frame_count += 1
    # if frame_count == 300:
    #     break

cap.release()
cv2.destroyAllWindows()

## Faire une detection code sur les images temp, sur bb

# ouvrir image
for index, value in detected.iterrows():
    image = Image.open(os.path.join("src","model-1","datasets","bottle_dataset","temp",value["name"]))
    
    # cropper avec bb 
    img_crop = image.crop(tuple(value["bbxyxy"]))

    #détection code 
    # img_crop.show()
    res_barcode = decode(img_crop)
    if len(res_barcode) != 0 :
        # propagation code à detected
        # img_crop.show()
        detected["code"].loc[detected["id"]==value["id"]] = res_barcode[0].data


# Transformer le dict en fichier text d'annotation yolo
code_detected = detected[detected["code"] != 0]
names = set(code_detected["name"])
for name in names :
    data = code_detected[code_detected["name"]==name]
    with open(os.path.join("src","model-1","datasets","bottle_dataset","temp",f"{name[:-4]}.txt"), "w") as txt:
        for index, value in data.iterrows():
            txt.write(str(value["code"])[2:-1] + " " + str(value["bbxywhn"][0]) + " " + str(value["bbxywhn"][1]) + " " + str(value["bbxywhn"][2]) + " " + str(value["bbxywhn"][3]) + "\n")

# Transférer de temp à dataset
temp = os.listdir(os.path.join("src","model-1","datasets","bottle_dataset","temp"))
to_move = []
for name in temp:   
    if name[-3:] == "txt" :
        os.replace(os.path.join("src","model-1","datasets","bottle_dataset","temp",f"{name[:-4]}.txt") , os.path.join("src","model-1","datasets","bottle_dataset","dataset",f"{name[:-4]}.txt"))
        os.replace(os.path.join("src","model-1","datasets","bottle_dataset","temp",f"{name[:-4]}.png") , os.path.join("src","model-1","datasets","bottle_dataset","dataset",f"{name[:-4]}.png"))

# Supprimer temp
temp = os.listdir(os.path.join("src","model-1","datasets","bottle_dataset","temp"))
for img in temp: 
    os.remove(os.path.join("src","model-1","datasets","bottle_dataset","temp",img))