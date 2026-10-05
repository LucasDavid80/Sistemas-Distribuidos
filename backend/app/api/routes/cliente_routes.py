from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/clientes", tags=["clientes"])


class ClienteBase(BaseModel):
    nome: str
    email: str
    idade: int


class Cliente(ClienteBase):
    id: int


clientes_db: dict[int, Cliente] = {}
contador_id = 1


@router.post("/", response_model=Cliente, status_code=201)
def criar_cliente(cliente: ClienteBase) -> Cliente:
    if any(existing.email == cliente.email for existing in clientes_db.values()):
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    global contador_id
    contador_id = max(clientes_db, default=0) + 1
    novo_cliente = Cliente(id=contador_id, **cliente.model_dump())
    clientes_db[contador_id] = novo_cliente
    contador_id += 1
    return novo_cliente


@router.get("/", response_model=list[Cliente])
def listar_clientes() -> list[Cliente]:
    return list(clientes_db.values())


@router.get("/{cliente_id}", response_model=Cliente)
def buscar_cliente(cliente_id: int) -> Cliente:
    cliente = clientes_db.get(cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


@router.put("/{cliente_id}", response_model=Cliente)
def atualizar_cliente(cliente_id: int, data: ClienteBase) -> Cliente:
    if cliente_id not in clientes_db:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    if any(
        existing.email == data.email and existing.id != cliente_id
        for existing in clientes_db.values()
    ):
        raise HTTPException(
            status_code=400, detail="Email já cadastrado por outro cliente"
        )
    cliente = Cliente(id=cliente_id, **data.model_dump())
    clientes_db[cliente_id] = cliente
    return cliente


@router.delete("/{cliente_id}", status_code=204)
def deletar_cliente(cliente_id: int) -> None:
    if cliente_id not in clientes_db:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    del clientes_db[cliente_id]
