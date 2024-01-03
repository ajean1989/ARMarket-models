import pytest
import io

from PIL import Image

@pytest.fixture(scope="module")
def annotation():
    annotation = [
        {
                "label" : "Object",
                "label_int" : 0,
                "bounding box" : [0.11212, 0.11, 0.4564, 0.4546]
          },
          {
                "label" : "bla",
                "label_int" : 2,
                "bounding box" : [0.11, 0.11, 0.45, 0.45]
          }
    ]

    return annotation

@pytest.fixture(scope="module")
def binary_annotation():
    annotation = b'[{"label" : "Object","label_int" : 0,"bounding box" : [0.11212, 0.11, 0.4564, 0.4546]},{"label" : "bla","label_int" : 2,"bounding box" : [0.11, 0.11, 0.45, 0.45]}]'
    return annotation

@pytest.fixture(scope="module")
def binary_img():
    img = Image.open("app/tests/sample/img_1.png")
    imgbyte = io.BytesIO()
    img.save(imgbyte, format="png")
    imgbyte = imgbyte.getvalue()
    return imgbyte

@pytest.fixture(scope="module")
def binary_metadata():
    metadata = b'{"dataset_id" : 0, "dataset_extraction" : "ARM", "pretreatment" : False, "data_augmentation" : False, "test" : True}'
    return metadata
