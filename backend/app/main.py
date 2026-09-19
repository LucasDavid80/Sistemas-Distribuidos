from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI()

# Modelos Pydantic
class ClienteBase(BaseModel):
    nome: str
    email: str
    idade: int

class Cliente(ClienteBase):
    id: int

# Banco de dados em memória
clientes_db: Dict[int, Cliente] = {}
contador_id = 1

@app.get("/")
def home():
    return {"message": "Bem-vindo ao Sistema de Clientes"}

@app.post("/clientes/", response_model=Cliente, status_code=201)
def criar_cliente(cliente: ClienteBase):
    global contador_id
    
    # Validação de e-mail duplicado
    for cl in clientes_db.values():
        if cl.email == cliente.email:
            raise HTTPException(status_code=400, detail="Email já cadastrado")
            
    novo_cliente = Cliente(id=contador_id, **cliente.model_dump())
    clientes_db[contador_id] = novo_cliente
    contador_id += 1
    
    return novo_cliente

@app.get("/clientes/", response_model=List[Cliente])
def listar_clientes():
    return list(clientes_db.values())

@app.get("/clientes/{cliente_id}", response_model=Cliente)
def buscar_cliente(cliente_id: int):
    if cliente_id not in clientes_db:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return clientes_db[cliente_id]

@app.put("/clientes/{cliente_id}", response_model=Cliente)
def atualizar_cliente(cliente_id: int, cliente_atualizado: ClienteBase):
    if cliente_id not in clientes_db:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
    for cl in clientes_db.values():
        if cl.email == cliente_atualizado.email and cl.id != cliente_id:
            raise HTTPException(status_code=400, detail="Email já cadastrado por outro cliente")
            
    cliente = Cliente(id=cliente_id, **cliente_atualizado.model_dump())
    clientes_db[cliente_id] = cliente
    return cliente

@app.delete("/clientes/{cliente_id}", status_code=204)
def deletar_cliente(cliente_id: int):
    if cliente_id not in clientes_db:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    del clientes_db[cliente_id]
    return None
