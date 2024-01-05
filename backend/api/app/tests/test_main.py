from fastapi.testclient import TestClient

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
