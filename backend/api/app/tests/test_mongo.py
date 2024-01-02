from app.mongo import Mongo

mongo = Mongo()

def test_set_img(binary_annotation, img):
    mongo.reset_db(test=True)
    annotation = eval(binary_annotation.decode('UTF-8'))
    mongo.set_img(img, annotation, dataset_id =0, dataset_extraction = "ARM", pretreatment = False, data_augmentation = False, test = True)
    res = mongo.dataset_test_collection.find({})
    print(res)
    count = 0
    for doc in res :
        count += 1
    assert count == 1 
