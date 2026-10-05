from fastapi import APIRouter

router = APIRouter(tags=["root"])


@router.get("/")
def home():
    return {"message": "Bem-vindo ao Sistema de Clientes"}
