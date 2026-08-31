from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Olá, Sistemas Distribuídos!"}


def test_hello_lucas():
    response = client.get("/lucas")
    assert response.status_code == 200
    assert response.json() == {"message": "Olá, Lucas!"}
