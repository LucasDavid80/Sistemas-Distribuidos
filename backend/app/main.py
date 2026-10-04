from fastapi import FastAPI

from app.api.routes.cliente_routes import clientes_db as _clientes_db
from app.api.routes.cliente_routes import router as clientes_router
from app.api.routes.commerce_routes import (
    admin_router,
    client_router,
    product_router,
    purchase_router,
)
from app.api.routes.user_routes import router as users_router

clientes_db = _clientes_db

app = FastAPI(title="Sistema de Compra e Venda")
app.include_router(users_router)
app.include_router(clientes_router)
app.include_router(client_router)
app.include_router(product_router)
app.include_router(purchase_router)
app.include_router(admin_router)


@app.get("/")
def home():
    return {"message": "Bem-vindo ao Sistema de Clientes"}
