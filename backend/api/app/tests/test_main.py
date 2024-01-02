from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_add_frame(binary_annotation):
    file1 = {'image': open('app/tests/sample/img_1.png', 'rb')}

    response = client.post("/dataset/frame/", files=file1, content=binary_annotation)
    assert response.status_code == 200


    file = {'upload-file': open('app/tests/sample/test.txt', 'rb')}
    response = client.post("/dataset/frame/", files=file)
    assert response.status_code == 405