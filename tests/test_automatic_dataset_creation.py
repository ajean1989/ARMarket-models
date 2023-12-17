import os 

from backend.automatic_dataset_creation import automatic_dataset


# def test_reset(mongo):
#     auto = automatic_dataset("yolov8x-oiv7", "multiple_bottles_3.mp4", test=True)
#     # Test que les fichiers du dossiers temps sont bien effacés

#     with open (os.path.join("backend","temp","test.txt"), "w") as txt :
#         txt.write("test")

#     assert len(os.listdir(os.path.join("backend","temp"))) > 0
#     # Test que la bdd est bien reset

#     ## Insertion en bdd

#     new_document = {"nom": "John", "âge": 30}
#     result = mongo.dataset_test_collection.insert_one(new_document)
#     docs = mongo.dataset_test_collection.find({})
#     count = 0
#     for doc in docs :
#         count += 1
#     assert count > 0 

#     ## reset
#     auto.reset()
#     docs = mongo.dataset_test_collection.find({})
#     count = 0
#     for doc in docs :
#         count += 1
#     assert count == 0 
#     assert len(os.listdir(os.path.join("backend","temp"))) == 0

def test_detection():
    auto = automatic_dataset("yolov8x-oiv7.pt", "data/sample/multiple_bottles_3.mp4", test=True)
    assert len(os.listdir(os.path.join("backend","temp"))) == 0
    auto.detection(vizualize=True)
    assert len(os.listdir(os.path.join("backend","temp"))) > 0
