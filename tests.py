from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_push_blob():
    response = client.post(
        "/", json={"handle": "abc123", "data": "test_data", "lifetime": 10}
    )

    assert response.status_code == 200
    assert response.json() == {"id": "abc123"}


def test_get_blob():
    response = client.post(
        "/", json={"handle": "abc123", "data": "test_data", "lifetime": 10}
    )

    response = client.get("/abc123")

    assert response.status_code == 200
    assert response.json() == {"data": "test_data"}
