from geo_app import crud
from fastapi.testclient import TestClient

from main import *


client = TestClient(app)


def count_rows():
    num = crud.count()
    print(num)
    return num


def create_item_without_test():
    num1 = count_rows()
    num2 = num1 + 1
    response = client.post(
        "/json/",
        json={"gfield": f"{num2}"},
    )
    return response


def test_create_item():
    num1 = count_rows()
    res = create_item_without_test()
    assert res.status_code == 201
    num2 = count_rows()
    assert res.json() == num2
    assert num2 - num1 == 1


def test_get_one():
    NUM = count_rows()
    if not NUM:
        create_item_without_test()
        NUM = 1
    response = client.get(f"/get-json/{NUM}")
    assert response.status_code == 200
    assert response.json()['gfield'] == json.dumps({"gfield": f"{NUM}"})


def test_get_many():
    NUM = count_rows()
    if NUM < 2:
        create_item_without_test()
        create_item_without_test()
        NUM = count_rows()
    skip = NUM - 1
    response = client.get(f"/geolist/?skip={skip}&limit=1")
    assert response.status_code == 200
    assert response.json()[0]['gfield'] == json.dumps({"gfield": f"{NUM}"})


def test_get_not_existing():
    NUM = count_rows() + 1
    response = client.get(f"/get-json/{NUM}")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Item not found'}


def test_delete_last():
    NUM = count_rows()
    if NUM == 0:
        create_item_without_test()
        NUM = 1
    response = client.delete(f"/delete/{NUM}")
    assert response.status_code == 204
    NUM2 = count_rows()
    assert NUM - NUM2 == 1



# class TestCrud:
#     def test_01(self):
#         # Arrange
#         create("a", 1)
#         # Act

#         # Assert
#         assert d["a"] == 1


# test_create_item()

# test_read()