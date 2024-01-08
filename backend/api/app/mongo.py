from pymongo import MongoClient
from bson.objectid import ObjectId
from PIL import Image
import bson

import io
import logging
import datetime
import random
import re
import json
import shutil
import sys

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


    def img_to_byte(self, img):
        """ Convertion d'une image PIL en BYTES """
        imgbyte = io.BytesIO()
        img.save(imgbyte, format="png")
        image_file_size = imgbyte.tell()
        imgbyte = imgbyte.getvalue()

        return [imgbyte, image_file_size]
    

    
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
       

    def set_img(self,img : bytes, annotation : bytes, dataset_id : list, dataset_extraction : str, pretreatment : bool, data_augmentation: bool, test : bool):
        """ 
        post /dataset/frame
        Enregistre les images qui on eu une détection et les métadonnées :
        "date" : "[date JJMMYYYY] Date de l'insertion du document",
        "id" : "[int] Id de l'image / collection",
        "img" : "[bin] Image",
        "name" : "[str] Nom de l'image format [from(dataset)_rand(10).jpg]",
        "size" : "[int] Taille de l'image en Mo",
        "pre-treatment" : "[bool] Si l'image a été pré-traitée",
        "data_augmentation" : "[bool] Si l'image est issue d'une data augmentation",
        "dataset" : "[list] Liste des datasets auquel l'image appartient",
        "training_data" :
            [
                {
                    "label" : "[str] Label associé à l'image",
                    "label_int" : "[int] Label associé à l'image sous forme d'integer unique avec table de correspondance dans label.json",
                    "bounding box" : "[list] Liste des bounding box au format xywhn"
                },
                {
                    "label" : "[str] Label associé à l'image",
                    "label_int" : "[int] Label associé à l'image sous forme d'integer unique avec table de correspondance dans label.json",
                    "bounding box" : "[list] Liste des bounding box au format xywhn"
                }
            ]
        """

        # Création du document
        new_document = {}

        # "date" : "[date YYYYMMDD] Date de l'insertion du document"
        new_document["date"] = datetime.datetime.today().strftime('%Y-%m-%d')

        # "id" : "[int] Id de l'image / collection"
        # Créé automatiquement "_id"

        # "img" : "[bin] Image"
        #imgbyte = self.img_to_byte(img)
        new_document["img"] = img
        # "size" : "[int] Taille de l'image en Mo"
        new_document["size"] = sys.getsizeof(img)

        # "name" : "[str] Nom de l'image format [from(dataset d'extraction)_rand(10).jpg]"
        new_document["name"] = f"{dataset_extraction}_{random.random()*(10**10)}"


        # "pre-treatment" : "[bool] Si l'image a été pré-traitée",
        new_document["pre_treatment"] = pretreatment

        # "data_augmentation" : "[bool] Si l'image est issue d'une data augmentation",
        new_document["data_augmentation"] = data_augmentation

        # "dataset" : "[list] Liste des datasets auquel l'image appartient"
        new_document["dataset"] = dataset_id

        # "training_data" : list de dict contenant label, label int, bb de chaque détection de l'image
        # input est un une list contenant un json pré formaté avant l'envoie à l'API pour correspondre au format attendu par yolo. 
        annotation = annotation.decode("utf-8")
        annotation = json.loads(annotation)
        
        new_document["training_data"] = annotation

        
        # Insertion en base
        if test :
            self.dataset_test_collection.insert_one(new_document)
            self.log.info(f"API : frame set in dataset_test collection- dataset_id : {dataset_id}")
        else : 
            self.dataset_collection.insert_one(new_document)
            self.log.info(f"API : frame set in dataset collection - dataset_id : {dataset_id}")

    def update_frame(self, id : str, query : dict, test: bool):
        """
        Met à jour une frame via son id.
        query = "key premier niveau" : value
        "key premier niveau = date, img, name, size, pre-trement, data_aumentation, dataset, training_data.
        """

        if test :
            self.dataset_test_collection.update_one(
                {"_id" : ObjectId(id)},
                {"$set" : query}
            )
            self.dataset_test_collection.update_one(
                {"_id" :  ObjectId(id)},
                {"$set" : {"update_date" : datetime.datetime.today().strftime('%Y-%m-%d')}}
            )
            self.log.info(f"API : frame {id} updated in dataset_test collection with {query}")
        else : 
            self.dataset_test_collection.update_one(
                {"_id" :  ObjectId(id)},
                {"$set" : query}
            )
            self.dataset_test_collection.update_one(
                {"_id" :  ObjectId(id)},
                {"$set" : {"update_date" : datetime.datetime.today().strftime('%Y-%m-%d')}}
                )
            self.log.info(f"API : frame {id} updated in dataset collection with {query}")


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


