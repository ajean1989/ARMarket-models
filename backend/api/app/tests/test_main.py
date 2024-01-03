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
    mongo = Mongo()
    mongo.reset_db(test=True)
    img = open("app/tests/sample/img_1.png","rb")
    files = [('image', img),("image", binary_annotation), ("image" , binary_metadata)]


    response = client.post("/dataset/frame/", files=files)
    assert response.status_code == 200

