from pymongo import MongoClient
from PIL import Image
import io
import logging
import datetime
import random
import re
import shutil

# import sys
# import os
# sys.path.append((os.path.dirname(os.path.abspath(__file__))))
# print(sys.path)

from app.config import *


class Mongo :

    log = logging.getLogger("log-auto")
    log.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    file_handler = logging.FileHandler("app.log")
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    log.addHandler(console_handler)   
    log.addHandler(file_handler)   

    def __init__(self) -> None:
        self.client = MongoClient(f'mongodb://{user_mongo}:{pass_mongo}@{adresse_mongo}:{port_mongo}')
        self.db = self.client.ARMarket
        self.dataset_collection = self.db.dataset
        self.dataset_test_collection = self.db.dataset_test
        self.pretreatment = 1

    def img_to_byte(self, img):
        """ Convertion d'une image PIL en BYTES """
        imgbyte = io.BytesIO()
        img.save(imgbyte, format="png")
        imgbyte = imgbyte.getvalue()
        return imgbyte
    

    
    def byte_to_img(self, imgbyte):
        """ Conversion des BYTES en image PIL"""
        imgbyte_io = io.BytesIO(imgbyte)
        image_pil = Image.open(imgbyte_io)
        return image_pil

    def test(self) : 
        """ Test de la base"""
        img = Image.open("data/img_test.jpg")
        imgbyte = self.img_to_byte(img)

        new_document = {"nom": "John", "âge": imgbyte}
        result = self.dataset_collection.insert_one(new_document)
        print(result)
        input("consulter la database avant d'effacer le test puis press enter")
        query = {"nom": "John"}
        self.dataset_collection.delete_one(query)
        input("vérifier document effacé puis press enter")
        return "test terminé"

    # API


    def get_dataset_id(self, id) : 
        """get /dataset/{id}"""
        # Réquête
        documents = self.dataset_collection.find({"dataset_id" : {"$elemMatch": {"$eq": id}}})

        if len(documents) == 0 :
            # mauvais id
            return False

        # Création d'un dossier structuré
        no_folder = random.randint(100,999)
        for index, doc in enumerate(documents):
            img = self.byte_to_img(doc["img"])
            img.save(f"temp/{no_folder}/{index}.png")
            
            labels = [i for i in doc.keys() if re.search("^label" , i)]
            with open(f"temp/{no_folder}/{index}.txt", "w") as txt :
                for label in labels :
                    txt.write(f"{doc[label]['code']} {doc[label]['bb'][0]} {doc[label]['bb'][1]} {doc[label]['bb'][2]} {doc[label]['bb'][3]} \n")
        # Transformation en zip
        shutil.make_archive(no_folder, 'zip', no_folder)
        self.log.info(f"API : get dataset, dataset_id : {id}")

        return f"temp/{no_folder}.zip"
    
    def delete_dataset_id(self, id) : 
        """delete /dataset/{id}"""
        self.dataset_collection.delete_many({"dataset_id" : {"$elemMatch": {"$eq": id}}})
        self.log.info(f"API : delete dataset, dataset_id : {id}")
       

    def set_img(self,img, txt_path, dataset_id = 0, data_augmentation = False, test = True):
        """ 
        post /dataset/frame
        Enregistre les images qui on eu une détection et les métadonnées :
        Date de la mise en base
        Code + BB
        Nom du dataset : 0 = all
        pré-traitement y a-t-il eu 
        Data augmentation y a-t-il eu
        """

        imgbyte = self.img_to_byte(img)

        # Création du document
        new_document = {}

        new_document["img"] = imgbyte
        new_document["date"] = datetime.datetime.today()


        with open (f"{txt_path}", "r") as txt :
            rows = txt.readlines()
            for index, row in enumerate(rows) :
                words = row.split()
                new_document[f"label_{index}"] = {"code" : words[0], "bb" : [words[1], words[2], words[3], words[4]]}
        new_document["dataset_id"] = [dataset_id]
        new_document["pretreatment"] = self.pretreatment
        new_document["data_augmentation"] = data_augmentation

        # Insertion en base
        if test :
            self.dataset_test_collection.insert_one(new_document)
            self.log.info(f"API : frame set in dataset_test collection- dataset_id : {dataset_id}")
        else : 
            self.dataset_collection.insert_one(new_document)
            self.log.info(f"API : frame set in dataset collection - dataset_id : {dataset_id}")


    def delete_frame(self, id) : 
        """delete /dataset/{id}"""
        doc = self.dataset_collection.find_one({"_id" : {"$elemMatch": {"$eq": id}}})
        self.dataset_collection.delete_one({"_id" : {"$elemMatch": {"$eq": id}}})
        self.log.info(f"API : frame {id} deleted from dataset_id : {doc['dataset_id']}")


    def reset_db(self, test = True):
        """Efface la base de donnée sélectionnée (dataset ou dataset_test)"""

        if test : 
            self.dataset_test_collection.delete_many({})
            logging.info("La collection dataset_test a été vidée de ses documents")

        else : 
            self.dataset_collection.delete_many({})
            logging.info("La collection dataset a été vidée de ses documents")

        

        



if __name__ == "__main__" : 
    Mongo_test = Mongo()
    # Mongo_test.test()
    Mongo_test.reset_db(test=False)


