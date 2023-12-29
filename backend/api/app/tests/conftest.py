import pytest
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
def img():
    img = Image.open("app/tests/sample/img_1703050572_775.png")
    return img