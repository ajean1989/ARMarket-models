
import re
import os
import time
import logging

from random import randint
import pandas as pd

from PIL import Image
from ultralytics import YOLO
import cv2
from pyzbar.pyzbar import decode

class automatic_dataset :

    log = logging.getLogger("log-auto")
    log.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    file_handler = logging.FileHandler("app.log")
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    log.addHandler(console_handler)   
    log.addHandler(file_handler)   

    def __init__(self,mode,weight,input) :
        self.mode = mode
        self.weight = weight
        self.input = f"data/{input}"
        self.model = YOLO(f"checkpoints/{self.weight}") 
        self.tracker = "tracker/custom_botsort.yaml"
        self.detected = pd.DataFrame(columns=["name","id","bbxyxy","bbxywhn","code"])
        self.path_temp = os.path.join("src","model-1","datasets","bottle_dataset","temp")
        self.path_dataset = os.path.join("src","model-1","datasets","bottle_dataset","dataset")

    def __call__(self, vizualize= False, max_frame = -1):
        if self.mode == 'test':
            self.reset()
        self.detection(vizualize, max_frame)
        self.code()


    def reset(self) :
        temp = os.listdir(self.path_temp)
        for img in temp: 
            os.remove(os.path.join(self.path_temp,img))
        dataset = os.listdir(self.path_dataset)
        for img in dataset: 
            os.remove(os.path.join(self.path_dataset,img))
        logging.info("mode test activé : Tous les fichiers temp et dataset supprimés")
    
    def detection(self, vizualize= False, max_frame = -1, log=log) :

        frame_count, detection_count, id_count = 0, 0, 0

        cap = cv2.VideoCapture(self.input)

        while cap.isOpened():

            # Read a frame from the video
            success, frame = cap.read()
            # if frame_count%5 == 0 :
            if success:

                # Run YOLOv8 inference on the frame
                results = self.model.track(frame, persist=True, classes = [39,41] , conf=0.1, tracker=self.tracker)
                result = results[0]

                # Visualize the results on the frame befor detect id
                # annotated_frame = results[0].plot()

                for r in result :
                    detection_count += 1
                    if r.boxes.id != None :
                        id_count += 1
                        print("x1, y1, x2, y2, id , conf, cls = ", r.boxes.data.tolist())
                        print('---')
                        print("id = ", r.boxes.id.int().cpu().tolist())
                        print('---')
                        print("class = ", r.boxes.cls)
                        print('---')
                    else : 
                        continue
                    
                    if vizualize == True :
                        # Visualize the results on the frame when id
                        annotated_frame = results[0].plot()
                        im = Image.fromarray(annotated_frame[..., ::-1])  # RGB PIL image
                        im.show()

                    # enregistrer l'image dans temp : nom = timestamp+randint(1024)
                    name = f"img_{str(int(time.time()))}_{randint(0,1023)}.png"
                    path = os.path.join(self.path_temp,name)
                    Image.fromarray(frame[:,:,::-1]).save(path,'PNG')

                    # !!!! une ligne par id !!!
                    # garder une trace (dict["nom","id","bb","code"]) du nom des fichiers + ID + bb enregristrer pour ajouter le label par la suite ou effacer
                    id = r.boxes.id.int().cpu().tolist()[0]
                    bbxyxy = r.boxes.xyxy[0].cpu().numpy() #[x1,y1,x2,y2]
                    bbxywhn = r.boxes.xywhn[0].cpu().numpy() #[x1,y1,x2,y2]

                    self.detected.loc[len(self.detected)] = [name, id, bbxyxy, bbxywhn, 0]
                    
            else:
                # Break the loop if the end of the video is reached
                break

            frame_count += 1
            if frame_count != -1 and frame_count == max_frame:
                break

        cap.release()
        cv2.destroyAllWindows()

        log.info(f"{frame_count} image(s) analysed")
        log.info(f"{detection_count} detected object(s)")
        log.info(f"{id_count} id(s) affected")
        log.info(f"different(s( object(s) detected)) : {id}")


    ## Faire une detection code sur les images temp, sur bb

    def code(self, log=log) :
        for index, value in self.detected.iterrows():
            # ouvrir image
            image = Image.open(os.path.join(self.path_temp,value["name"]))
            
            # cropper avec bb 
            img_crop = image.crop(tuple(value["bbxyxy"]))

            #détection code 
            # img_crop.show()
            res_barcode = decode(img_crop)
            if len(res_barcode) != 0 :
                # propagation code à detected
                # img_crop.show()
                self.detected["code"].loc[self.detected["id"]==value["id"]] = res_barcode[0].data
                log.info(f"code detetcted : {res_barcode[0].data}")


        # Transformer le dict en fichier text d'annotation yolo
        code_detected = self.detected[self.detected["code"] != 0]
        names = set(code_detected["name"])
        for name in names :
            data = code_detected[code_detected["name"]==name]
            with open(os.path.join(self.path_temp,f"{name[:-4]}.txt"), "w") as txt:
                for index, value in data.iterrows():
                    txt.write(str(value["code"])[2:-1] + " " + str(value["bbxywhn"][0]) + " " + str(value["bbxywhn"][1]) + " " + str(value["bbxywhn"][2]) + " " + str(value["bbxywhn"][3]) + "\n")

        # Transférer de temp à dataset
        temp = os.listdir(self.path_temp)
        file_count = 0
        for name in temp:   
            if name[-3:] == "txt" :
                os.replace(os.path.join(self.path_temp,f"{name[:-4]}.txt") , os.path.join(self.path_dataset,f"{name[:-4]}.txt"))
                os.replace(os.path.join(self.path_temp,f"{name[:-4]}.png") , os.path.join(self.path_dataset,f"{name[:-4]}.png"))
                file_count += 1
        log.info(f"{file_count} file(s) transfered from temp to dataset")


        # Supprimer temp
        temp = os.listdir(self.path_temp)
        for img in temp: 
            os.remove(self.path_temp,img)

        return log.info(f"temp files deleted.")
    
    

if __name__ == "__main__":
    create = automatic_dataset("test", "yolov8x", "multiple_bottles_3.mp4")
    create()