import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import commerce_service, user_service


@pytest.fixture
def client():
    user_service.users_db.clear()
    user_service.next_id = 1
    commerce_service.products_db.clear()
    commerce_service.purchases_db.clear()
    commerce_service.next_product_id = 1
    commerce_service.next_purchase_id = 1
    return TestClient(app)


def create_user(client, nome, email, role):
    response = client.post(
        "/users/",
        json={
            "nome": nome,
            "email": email,
            "idade": 30,
            "role": role,
        },
    )
    assert response.status_code == 201
    return response.json()


def product_payload():
    return {"nome": "Teclado", "descricao": "Mecânico", "preco": 25, "estoque": 5}


def test_product_crud_and_permissions(client):
    seller = create_user(client, "Vendedor", "seller@email.com", "seller")
    other_seller = create_user(client, "Outro", "other@email.com", "seller")
    client_user = create_user(client, "Cliente", "client@email.com", "client")

    unauthenticated = client.post("/products/", json=product_payload())
    assert unauthenticated.status_code == 401

    forbidden = client.post(
        "/products/",
        json=product_payload(),
        headers={"X-User-Id": str(client_user["id"])},
    )
    assert forbidden.status_code == 403

    created = client.post(
        "/products/",
        json=product_payload(),
        headers={"X-User-Id": str(seller["id"])},
    )
    assert created.status_code == 201
    product = created.json()
    assert product["seller_id"] == seller["id"]

    assert client.get("/products/").json() == [product]
    assert client.get(f"/products/{product['id']}").json() == product
    assert client.get("/products/999").status_code == 404

    updated = client.patch(
        f"/products/{product['id']}",
        json={"estoque": 5},
        headers={"X-User-Id": str(seller["id"])},
    )
    assert updated.status_code == 200
    assert updated.json()["estoque"] == 5

    other_update = client.patch(
        f"/products/{product['id']}",
        json={"estoque": 2},
        headers={"X-User-Id": str(other_seller["id"])},
    )
    assert other_update.status_code == 403

    deleted = client.delete(
        f"/products/{product['id']}",
        headers={"X-User-Id": str(seller["id"])},
    )
    assert deleted.status_code == 204
    assert client.get(f"/products/{product['id']}").status_code == 404


def test_deposit_balance_and_permissions(client):
    client_user = create_user(client, "Cliente", "client@email.com", "client")
    other_client = create_user(client, "Outro", "other@email.com", "client")
    seller = create_user(client, "Vendedor", "seller@email.com", "seller")

    deposited = client.post(
        f"/clients/{client_user['id']}/balance",
        json={"amount": 100},
        headers={"X-User-Id": str(client_user["id"])},
    )
    assert deposited.status_code == 200
    assert deposited.json()["saldo"] == 100

    unauthorized = client.post(
        f"/clients/{other_client['id']}/balance",
        json={"amount": 100},
        headers={"X-User-Id": str(client_user["id"])},
    )
    assert unauthorized.status_code == 403

    role_forbidden = client.post(
        f"/clients/{client_user['id']}/balance",
        json={"amount": 100},
        headers={"X-User-Id": str(seller["id"])},
    )
    assert role_forbidden.status_code == 403

    missing = client.post(
        "/clients/999/balance",
        json={"amount": 100},
        headers={"X-User-Id": str(client_user["id"])},
    )
    assert missing.status_code == 403


def test_purchase_and_purchase_listing(client):
    client_user = create_user(client, "Cliente", "client@email.com", "client")
    seller = create_user(client, "Vendedor", "seller@email.com", "seller")
    admin = create_user(client, "Admin", "admin@email.com", "admin")

    client.post(
        f"/clients/{client_user['id']}/balance",
        json={"amount": 75},
        headers={"X-User-Id": str(client_user["id"])},
    )
    product = client.post(
        "/products/",
        json=product_payload(),
        headers={"X-User-Id": str(seller["id"])},
    ).json()

    purchase = client.post(
        "/purchases/",
        json={"product_id": product["id"], "quantidade": 2},
        headers={"X-User-Id": str(client_user["id"])},
    )
    assert purchase.status_code == 201
    assert purchase.json()["total"] == 50
    assert client.get(
        "/purchases/mine", headers={"X-User-Id": str(client_user["id"])}
    ).json() == [purchase.json()]
    assert client.get(
        "/admin/purchases", headers={"X-User-Id": str(admin["id"])}
    ).json() == [purchase.json()]
    assert (
        client.get("/admin/users", headers={"X-User-Id": str(admin["id"])}).status_code
        == 200
    )

    insufficient_balance = client.post(
        "/purchases/",
        json={"product_id": product["id"], "quantidade": 2},
        headers={"X-User-Id": str(client_user["id"])},
    )
    assert insufficient_balance.status_code == 400
    assert insufficient_balance.json() == {"detail": "Saldo insuficiente"}

    seller_purchase = client.post(
        "/purchases/",
        json={"product_id": product["id"], "quantidade": 1},
        headers={"X-User-Id": str(seller["id"])},
    )
    assert seller_purchase.status_code == 403


def test_admin_delete_user_and_non_admin_forbidden(client):
    admin = create_user(client, "Admin", "admin@email.com", "admin")
    user = create_user(client, "Cliente", "client@email.com", "client")

    forbidden = client.get("/admin/users", headers={"X-User-Id": str(user["id"])})
    assert forbidden.status_code == 403

    deleted = client.delete(
        f"/admin/users/{user['id']}",
        headers={"X-User-Id": str(admin["id"])},
    )
    assert deleted.status_code == 204
    assert client.get(f"/users/{user['id']}").status_code == 404
    assert (
        client.delete(
            "/admin/users/999", headers={"X-User-Id": str(admin["id"])}
        ).status_code
        == 404
    )
