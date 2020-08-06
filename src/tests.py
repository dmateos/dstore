from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

TEST_KEY = "/abc123"
TEST_KEY_FAKE = "/abcfake"
TEST_KEY_AUTO = "/auto"
TEST_DATA = {"data": "test_data", "lifetime": 10}
TEST_DATA2 = {"data": "test_data2", "lifetime": 10}

TEST_RESPONSE = {"data": "test_data"}
TEST_RESPONSE2 = {"data": "test_data2"}


def test_push_blob():
    response = client.post(TEST_KEY, json=TEST_DATA)

    assert response.status_code == 200
    assert response.json() == {"id": TEST_KEY[1:]}


def test_push_auto_handle_blob():
    response = client.post(TEST_KEY_AUTO, json=TEST_DATA)

    assert response.status_code == 200
    assert len(response.json()["id"]) == 6


def test_get_blob():
    response = client.post(TEST_KEY, json=TEST_DATA)
    response = client.get(TEST_KEY)

    assert response.status_code == 200
    assert response.json() == TEST_RESPONSE


def test_overwrite_attempt_behaviour():
    response = client.post(TEST_KEY, json=TEST_DATA)
    response = client.get(TEST_KEY)

    assert response.status_code == 200
    assert response.json() == TEST_RESPONSE

    response = client.post(TEST_KEY, json=TEST_DATA2)
    response = client.get(TEST_KEY)

    assert response.status_code == 200
    assert response.json() == TEST_RESPONSE2


def test_get_invalid_blob():
    response = client.get(TEST_KEY_FAKE)
    assert response.status_code == 404
