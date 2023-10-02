
import sys 
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



# Yolo V8 Tracker 

# Yolo V8
model = YOLO('checkpoints/220923_yolov8_drazcat-ai-hf.pt') 

## image

# results = model("data/img_test.jpg")

# # Visualize the results on the frame
# annotated_frame = results[0].plot()

# im = Image.fromarray(annotated_frame[..., ::-1])  # RGB PIL image
# im.show()





##  Open the YT file
# video_path = "https://www.youtube.com/watch?v=2ib3_TBZGkU"

# yt = YouTube(video_path)
# stream = yt.streams.get_highest_resolution()

# minute_to_go = 1
# sec_to_go = 54
# fps = 25
# time_to_go = minute_to_go*(60*fps)+sec_to_go*fps
# frames = 10
frame_count = 0


# cap = cv2.VideoCapture(stream.url)
# print(cap)
# if not cap.isOpened():
#    print ("File Cannot be Opened")




## Open video
video_link = "data/video_test.mp4"

cap = cv2.VideoCapture(video_link)

# Loop through the video frames
while cap.isOpened():

    


    # Read a frame from the video
    success, frame = cap.read()

    # print(frame_count)
    # print(time_to_go)

    # if frame_count > time_to_go :
    if frame_count%100 == 0 :

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
                
            # Conserver les images où il y a une bounding box avec la class 'items' avec l'ID du track dans un dossier temp
            for r in results :
                print(r.boxes.xyxy[0])
                [x1,y1,x2,y2] = r.boxes.xyxy[0].cpu().numpy()
                print(x1)
                print('---')
                print(r.boxes.cls)
                print('---')
                
                # Faire une detection sur les images temp si code barre
                cropped_image = im.crop((x1,y1,x2,y2))
                cropped_image.show()

                res_barcode = decode(cropped_image)
                print(res_barcode)

                if len(res_barcode) > 0 : 
                    # Si code barre, repérer l'ID de la bb sur lequel il se trouve
                    pass


            # Conserver les images où le trouve l'ID et traitement pour transformer en dataset au format yolo xyxy, xywh, wywyn, wywhn

    frame_count += 1


cap.release()
cv2.destroyAllWindows()




# Conserver



