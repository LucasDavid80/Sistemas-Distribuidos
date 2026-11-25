from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.cliente_routes import router as clientes_router
from app.api.routes.commerce_routes import (
    admin_router,
    client_router,
    product_router,
    purchase_router,
)
from app.api.routes.root_routes import router as root_router
from app.api.routes.task_routes import project_router, task_router
from app.api.routes.user_routes import router as users_router
from app.core.config import get_settings

app = FastAPI(title="Gerenciador de Tarefas e Projetos - C216")
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "X-User-Id"],
)

app.include_router(users_router)
app.include_router(clientes_router)
app.include_router(client_router)
app.include_router(product_router)
app.include_router(purchase_router)
app.include_router(admin_router)
app.include_router(task_router)
app.include_router(project_router)
app.include_router(root_router)
