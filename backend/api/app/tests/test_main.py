from fastapi.testclient import TestClient
from bson.objectid import ObjectId

import json

from app.main import app
from app.mongo import Mongo

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_add_frame(binary_annotation, binary_metadata):
    # Ajout d'un frame
    mongo = Mongo()
    mongo.reset_db(test=True)
    img = open("app/tests/sample/img_1.png","rb")
    files = [('files', img),("files", binary_annotation), ("files" , binary_metadata)]
    response = client.post("/dataset/frame/", files=files)

    assert response.status_code == 200

    # Image n'est pas un jpg, png, etc. 
    mongo.reset_db(test=True)
    img = open("app/tests/sample/test.txt","rb")
    files = [('files', img),("files", binary_annotation), ("files" , binary_metadata)]
    response = client.post("/dataset/frame/", files=files)

    assert response.status_code == 405

    # Array n'a pas 3 éléments
    mongo.reset_db(test=True)
    img = open("app/tests/sample/img_1.png","rb")
    files = [('files', img),("files", binary_annotation)]
    response = client.post("/dataset/frame/", files=files)

    assert response.status_code == 405
    assert response.json() == {"error": "array must have 3 binaries elements"}

def test_update_frame(binary_annotation, binary_metadata):
    # Ajout d'un frame
    mongo = Mongo()
    mongo.reset_db(test=True)
    img = open("app/tests/sample/img_1.png","rb")
    files = [('files', img),("files", binary_annotation), ("files" , binary_metadata)]


    response = client.post("/dataset/frame/", files=files)
    assert response.status_code == 200

    res = mongo.dataset_test_collection.find_one({})
    assert res["data_augmentation"] == False 

    # Modification de data_augmentation
    id_init = (res["_id"]) 
    id = str(res["_id"]) 
    pp = ObjectId(id)
    assert id_init == pp 

    update = {
        "id" : id,
        "query" : {"data_augmentation" : True},
        "test" : True
    }

    response = client.put("/dataset/frame/", json=update)
    assert response.status_code == 200

    res_updated = mongo.dataset_test_collection.find_one({"_id": id_init})
    assert res_updated["data_augmentation"] == True 

    # Multi modification

    update = {
        "id" : id,
        "query" : {"data_augmentation" : True,
                   "pre_treatment" : True},
        "test" : True
    }

    response = client.put("/dataset/frame/", json=update)
    assert response.status_code == 200

    res_updated = mongo.dataset_test_collection.find_one({"_id": id_init})
    assert res_updated["data_augmentation"] == True 
    assert res_updated["pre_treatment"] == True 


    # Cas où le champ de query n'existe pas

    update = {
        "id" : id,
        "query" : {"data_augment" : True},
        "test" : True
    }

    response = client.put("/dataset/frame/", json=update)
    assert response.status_code == 405
