from pymongo import MongoClient
from PIL import Image
import io
import logging
import datetime

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from config import *


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

    # test()

    def set_img(self,img, txt_path, dataset = 0, data_augmentation = False, test = True):
        """ Enregistre les images qui on eu une détection et les métadonnées :
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
        new_document["dataset"] = dataset
        new_document["pretreatment"] = self.pretreatment
        new_document["data_augmentation"] = data_augmentation

        # Insertion en base
        if test :
            self.dataset_test_collection.insert_one(new_document)
        else : 
            self.dataset_collection.insert_one(new_document)

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


