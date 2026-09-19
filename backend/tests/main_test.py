import pytest
from fastapi.testclient import TestClient
from main import app

# Fixture criando o client, conforme exigido na atividade
@pytest.fixture
def client():
    return TestClient(app)

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Olá, Sistemas Distribuídos!"}

def test_hello_lucas(client):
    response = client.get("/lucas")
    assert response.status_code == 200
    assert response.json() == {"message": "Olá, Lucas!"}

# Teste com parametrização para testar múltiplos produtos corretos de uma vez
@pytest.mark.parametrize("produto_id, nome_esperado", [
    (1, "Teclado"),
    (2, "Mouse"),
    (3, "Monitor"),
])
def test_buscar_produto_sucesso(client, produto_id, nome_esperado):
    response = client.get(f"/produtos/{produto_id}")
    assert response.status_code == 200
    assert response.json()["nome"] == nome_esperado

# Teste de cenário de erro: Produto não encontrado (404)
def test_buscar_produto_nao_encontrado(client):
    response = client.get("/produtos/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Produto não encontrado"}

# Teste de cenário de erro: Input inválido (400)
def test_buscar_produto_id_negativo(client):
    response = client.get("/produtos/-5")
    assert response.status_code == 400
    assert response.json() == {"detail": "ID do produto não pode ser negativo"}
