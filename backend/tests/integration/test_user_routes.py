import pytest
from fastapi.testclient import TestClient


def test_create_and_list_users(client):
    response = client.post(
        "/users/", json={"nome": "Alice", "email": "alice@email.com", "idade": 25}
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "nome": "Alice",
        "email": "alice@email.com",
        "idade": 25,
    }
    assert client.get("/users/").json() == [response.json()]


def test_user_persists_after_api_client_restart(client, db):
    created = client.post(
        "/users/",
        json={
            "nome": "Persisted",
            "email": "persisted@email.com",
            "idade": 25,
        },
    )
    user_id = created.json()["id"]

    client.close()

    with TestClient(client.app) as restarted_client:
        response = restarted_client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["email"] == "persisted@email.com"


def test_read_update_and_delete_user(client):
    user = client.post(
        "/users/", json={"nome": "Bob", "email": "bob@email.com", "idade": 30}
    ).json()

    response = client.get(f"/users/{user['id']}")
    assert response.status_code == 200

    response = client.put(
        f"/users/{user['id']}",
        json={"nome": "Bob Updated", "email": "bob.new@email.com", "idade": 31},
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "Bob Updated"

    assert client.delete(f"/users/{user['id']}").status_code == 204
    assert client.get(f"/users/{user['id']}").status_code == 404


def test_reject_duplicate_email(client):
    payload = {"nome": "Alice", "email": "same@email.com", "idade": 25}
    client.post("/users/", json=payload)

    response = client.post(
        "/users/", json={"nome": "Bob", "email": "same@email.com", "idade": 30}
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Email já cadastrado"}


def test_patch_user(client):
    user = client.post(
        "/users/", json={"nome": "Carol", "email": "carol@email.com", "idade": 28}
    ).json()

    response = client.patch(
        f"/users/{user['id']}",
        json={"nome": "Carol Updated", "idade": 29},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": user["id"],
        "nome": "Carol Updated",
        "email": "carol@email.com",
        "idade": 29,
    }


def test_patch_user_rejects_duplicate_email(client):
    client.post(
        "/users/", json={"nome": "Alice", "email": "alice@email.com", "idade": 25}
    )
    user = client.post(
        "/users/", json={"nome": "Bob", "email": "bob@email.com", "idade": 30}
    ).json()

    response = client.patch(f"/users/{user['id']}", json={"email": "alice@email.com"})

    assert response.status_code == 400
    assert response.json() == {"detail": "Email já cadastrado"}


@pytest.mark.parametrize(
    "method, path",
    [
        ("get", "/users/999"),
        ("put", "/users/999"),
        ("patch", "/users/999"),
        ("delete", "/users/999"),
    ],
)
def test_missing_user_returns_not_found(client, method, path):
    payload = {"nome": "Ghost", "email": "ghost@email.com", "idade": 99}
    response = (
        getattr(client, method)(path, json=payload)
        if method in {"put", "patch"}
        else getattr(client, method)(path)
    )

    assert response.status_code == 404
