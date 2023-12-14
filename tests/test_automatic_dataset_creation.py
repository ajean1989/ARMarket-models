import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print(sys.path)
from src.model1.automatic_dataset_creation import automatic_dataset
from src.model1.backend.mongo.mongo import Mongo

import pytest

auto = automatic_dataset("yolov8x", "multiple_bottles_3.mp4", test=True)

def test_reset():
    # Test que les fichiers des dossiers temps et dataset sont bien effacés

    # Test que la bdd est bien reset

    ## Insertion en bdd
    mongo_test = Mongo()
    new_document = {"nom": "John", "âge": 30}
    result = mongo_test.dataset_test_collection.insert_one(new_document)
    docs = mongo_test.dataset_test_collection.find({})
    count = 0
    for doc in docs :
        count += 1
    assert count > 0 

    ## reset
    auto.reset()
    docs = mongo_test.dataset_test_collection.find({})
    count = 0
    for doc in docs :
        count += 1
    assert count == 0 