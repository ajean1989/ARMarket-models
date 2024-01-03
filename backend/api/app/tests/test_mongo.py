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
