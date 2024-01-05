from app.mongo import Mongo

mongo = Mongo()

def test_set_img(binary_annotation, binary_img):
    mongo.reset_db(test=True)
    annotation = binary_annotation
    mongo.set_img(binary_img, annotation, dataset_id =0, dataset_extraction = "ARM", pretreatment = False, data_augmentation = False, test = True)
    res = mongo.dataset_test_collection.find({})
    print(res)
    count = 0
    for doc in res :
        count += 1
    assert count == 1 



def test_update_frame(binary_annotation, binary_metadata):
    res = mongo.dataset_test_collection.find_one({})
    assert res["data_augmentation"] == False
    id = res["_id"] 
    mongo.update_frame(id=id, query={"data_augmentation" : True}, test=True)
    res_updated = mongo.dataset_test_collection.find_one({"_id": id})
    assert res_updated["data_augmentation"] == True 

