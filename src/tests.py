from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


TEST_DATA = {"data": "test_data", "lifetime": 10}
TEST_DATA2 = {"data": "test_data2", "lifetime": 10}

TEST_RESPONSE = {"data": "test_data"}
TEST_RESPONSE2 = {"data": "test_data2"}


def test_push_blob():
    response = client.post("/abc123", json=TEST_DATA)

    assert response.status_code == 200
    assert response.json() == {"id": "abc123"}


def test_push_auto_handle_blob():
    response = client.post("/abc123", json=TEST_DATA)

    assert response.status_code == 200
    assert response.json() != {"id": "auto"}
    assert len(response.json()["id"]) == 6


def test_get_blob():
    response = client.post("/abc123", json=TEST_DATA)
    response = client.get("/abc123")

    assert response.status_code == 200
    assert response.json() == TEST_RESPONSE


def test_overwrite_attempt_behaviour():
    response = client.post("/abc123", json=TEST_DATA)
    response = client.get("/abc123")

    assert response.status_code == 200
    assert response.json() == TEST_RESPONSE

    response = client.post("/abc123", json=TEST_DATA2)
    response = client.get("/abc123")

    assert response.status_code == 200
    assert response.json() == TEST_RESPONSE2


def test_get_invalid_blob():
    response = client.get("/123fakes")
    assert response.status_code == 404
