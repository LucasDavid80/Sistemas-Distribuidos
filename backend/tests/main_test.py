import pytest
from fastapi.testclient import TestClient
from app.main import app, clientes_db

# Fixture criando o client e garantindo banco vazio antes de cada teste
@pytest.fixture
def client():
    # Limpa o banco de dados e reseta o contador de ID antes do teste rodar
    clientes_db.clear()
    from app import main
    main.contador_id = 1
    
    return TestClient(app)

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bem-vindo ao Sistema de Clientes"}

# Teste de criação com Parametrização
@pytest.mark.parametrize("nome, email, idade", [
    ("Alice", "alice@email.com", 25),
    ("Bob", "bob@email.com", 30),
    ("Charlie", "charlie@email.com", 35),
])
def test_criar_cliente_sucesso(client, nome, email, idade):
    response = client.post("/clientes/", json={
        "nome": nome,
        "email": email,
        "idade": idade
    })
    assert response.status_code == 201
    dados = response.json()
    assert dados["nome"] == nome
    assert dados["email"] == email
    assert "id" in dados

# Teste Listar clientes
def test_listar_clientes(client):
    client.post("/clientes/", json={"nome": "Dave", "email": "dave@email.com", "idade": 40})
    response = client.get("/clientes/")
    assert response.status_code == 200
    dados = response.json()
    assert len(dados) == 1
    assert dados[0]["nome"] == "Dave"

# Teste Cenário de Erro: Cliente Inexistente (404)
def test_buscar_cliente_inexistente(client):
    response = client.get("/clientes/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Cliente não encontrado"}

# Teste Cenário de Erro: Email Duplicado (400)
def test_criar_cliente_email_duplicado(client):
    cliente_data = {"nome": "Eve", "email": "eve@email.com", "idade": 28}
    client.post("/clientes/", json=cliente_data) # Primeiro vai com sucesso
    
    response = client.post("/clientes/", json=cliente_data) # Segundo deve falhar
    assert response.status_code == 400
    assert response.json() == {"detail": "Email já cadastrado"}

# Teste Deletar cliente
def test_deletar_cliente(client):
    resposta_post = client.post("/clientes/", json={"nome": "Frank", "email": "frank@email.com", "idade": 50})
    id_cliente = resposta_post.json()["id"]
    
    resposta_delete = client.delete(f"/clientes/{id_cliente}")
    assert resposta_delete.status_code == 204
    
    resposta_get = client.get(f"/clientes/{id_cliente}")
    assert resposta_get.status_code == 404
