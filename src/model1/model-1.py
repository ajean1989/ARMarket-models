
import re
import os
# import numpy as np
# from pprint import pprint
# import matplotlib.pyplot as plt

from PIL import Image
from ultralytics import YOLO
import cv2
from pytube import YouTube
from pyzbar.pyzbar import decode

# sys.path.append('../../../')
# print(sys.path)

# Yolo v5

import torch

# Model
# model2 = torch.hub.load("ultralytics/yolov5", 'custom', 'checkpoints/yolov5_unkown2.pt')  # or yolov5n - yolov5x6, custom



# Yolo V8 Tracker 

# Yolo V8
# model0 = YOLO('checkpoints/220923_yolov8_drazcat-ai-hf.pt') 
model1 = YOLO('checkpoints/yolov8x.pt') 


models = [model1]

test = "video"

code = {}

for model in models :

    if test == 'image':
    ## image
        
        results = model("data/pestobig.png")

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        im = Image.fromarray(annotated_frame[..., ::-1])  # RGB PIL image
        im.show()

        image = Image.open("data/pesto.png")

        res_barcode = decode(image)
        print(res_barcode)

        exit()



    if re.search("^video", test) :

        if re.search("YT$", test) :
            # Open the YT file
            video_path = "https://www.youtube.com/watch?v=2ib3_TBZGkU"

            yt = YouTube(video_path)
            stream = yt.streams.get_highest_resolution()

            minute_to_go = 1
            sec_to_go = 54
            fps = 25
            time_to_go = minute_to_go*(60*fps)+sec_to_go*fps
            frames = 10

            cap = cv2.VideoCapture(stream.url)
            print(cap)
            if not cap.isOpened():
                print ("File Cannot be Opened")

        else :
            ## Open video
            video_link = "data/video_test_2.mp4"

            cap = cv2.VideoCapture(video_link)

        frame_count = 0
        # Loop through the video frames
        while cap.isOpened():


            # Read a frame from the video
            success, frame = cap.read()

            # if frame_count > time_to_go :
            if frame_count%30 == 0 :

                if success:
                    # Run YOLOv8 inference on the frame
                    results = model.track(frame, persist=True, classes = 39)

                    # Visualize the results on the frame
                    annotated_frame = results[0].plot()

                    im = Image.fromarray(annotated_frame[..., ::-1])  # RGB PIL image
                    im.show()

                    

                    # Display the annotated frame

                    # res = input("continue any or 'q' for quit : ")
                    # if res == "q" :
                    #     break

                    for r in results :
                        if len(r.boxes.xyxy) == 0 :
                            break
                        # enreistrer l'image dans temps
                        im.save(f"img_{frame_count}.png")

                        print(r.boxes.xyxy[0])
                        for i in range(len(r.boxes.xyxy)) :
                            [x1,y1,x2,y2] = r.boxes.xyxy[i].cpu().numpy()
                            print('---')
                            print(r.boxes.cls)
                            print('---')
                            print("id = ", r.boxes.id.int().cpu().tolist())
                            ids = r.boxes.id.int().cpu().tolist()

                            print('---')
                            
                            # Faire une detection sur les images temp si code barre
                            cropped_image = im.crop((x1,y1,x2,y2))
                            cropped_image.show()

                            res_barcode = decode(cropped_image)
                            print("bar code : ",res_barcode)
                            if len(res_barcode) != 0 :
                                for id in ids :
                                    code[id] = res_barcode[0]["data"]

                        if len(res_barcode) > 0 : 
                            # Si code barre, repérer l'ID de la bb sur lequel il se trouve
                            pass

                else:
                    # Break the loop if the end of the video is reached
                    break

            frame_count += 1

        cap.release()
        cv2.destroyAllWindows()

temp = os.listdir(os.path.join("datasets","bottle_dataset","temp"))
if len(code.keys()) != 0 : 
    for img in temp:    

        results = model(img, classes = 39)  
        # Création du dataset
                        
        for r in results :
            if len(r.boxes.xyxy) == 0 :
                break
            # enreistrer l'image dans temps
            im.save(f"img_{frame_count}.png")
            print(r.boxes.xyxy[0])
            for i in range(len(r.boxes.xyxy)) :
                [x1,y1,x2,y2] = r.boxes.xyxy[i].cpu().numpy()
                print('---')
                print(r.boxes.cls)
                print('---')
                print("id = ", r.boxes.id.int().cpu().tolist)
                print('---')
                
                # Faire une detection sur les images temp si code barre
                cropped_image = im.crop((x1,y1,x2,y2))
                cropped_image.sho
                res_barcode = decode(cropped_image)
                print("bar code : ",res_barcode)
            if len(res_barcode) > 0 : 
                # Si code barre, repérer l'ID de la bb sur lequel il se trouve
                pass

else :
    # Supprimer les fichiers du dossier temp
    for img in temp:  
        os.remove(os.path.join(temp,img))


                    # Conserver les images où le trouve l'ID et traitement pour transformer en dataset au format yolo xyxy, xywh, wywyn, wywhn
                






# Conserver



