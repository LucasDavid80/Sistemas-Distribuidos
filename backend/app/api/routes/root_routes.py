from fastapi import APIRouter

router = APIRouter(tags=["root"])


@router.get("/")
def home():
    return {"message": "Bem-vindo ao Sistema de Clientes"}


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
