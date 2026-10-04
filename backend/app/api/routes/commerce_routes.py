from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.core.permissions import current_user, require_role
from app.schemas.commerce_schema import (
    BalanceDeposit,
    Product,
    ProductCreate,
    ProductPatch,
    Purchase,
    PurchaseCreate,
)
from app.schemas.user_schema import User, UserRole
from app.services import commerce_service, user_service

product_router = APIRouter(prefix="/products", tags=["products"])
client_router = APIRouter(prefix="/clients", tags=["clients"])
purchase_router = APIRouter(prefix="/purchases", tags=["purchases"])
admin_router = APIRouter(prefix="/admin", tags=["admin"])


CurrentUser = Annotated[User, Depends(current_user)]


@product_router.post("/", response_model=Product, status_code=201)
def create_product(data: ProductCreate, user: CurrentUser) -> Product:
    require_role(user, UserRole.SELLER, UserRole.ADMIN)
    return commerce_service.create_product(data, user.id)


@product_router.get("/", response_model=list[Product])
def list_products() -> list[Product]:
    return list(commerce_service.products_db.values())


@product_router.get("/{product_id}", response_model=Product)
def get_product(product_id: int) -> Product:
    product = commerce_service.products_db.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product


@product_router.patch("/{product_id}", response_model=Product)
def update_product(product_id: int, data: ProductPatch, user: CurrentUser) -> Product:
    product = get_product(product_id)
    require_role(user, UserRole.SELLER, UserRole.ADMIN)
    if user.role != UserRole.ADMIN and product.seller_id != user.id:
        raise HTTPException(status_code=403, detail="Produto pertence a outro vendedor")
    return commerce_service.update_product(product_id, data)


@product_router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, user: CurrentUser) -> None:
    product = get_product(product_id)
    require_role(user, UserRole.SELLER, UserRole.ADMIN)
    if user.role != UserRole.ADMIN and product.seller_id != user.id:
        raise HTTPException(status_code=403, detail="Produto pertence a outro vendedor")
    del commerce_service.products_db[product_id]


@client_router.post("/{client_id}/balance", response_model=User)
def deposit_balance(
    client_id: int,
    data: BalanceDeposit,
    user: CurrentUser,
) -> User:
    require_role(user, UserRole.CLIENT, UserRole.ADMIN)
    if user.role != UserRole.ADMIN and user.id != client_id:
        raise HTTPException(status_code=403, detail="Cliente não autorizado")
    updated = user_service.add_balance(client_id, data.amount)
    if updated is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return updated


@purchase_router.post("/", response_model=Purchase, status_code=201)
def create_purchase(data: PurchaseCreate, user: CurrentUser) -> Purchase:
    require_role(user, UserRole.CLIENT)
    try:
        purchase = commerce_service.purchase_product(
            data.product_id, user.id, data.quantidade
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    if purchase is None:
        raise HTTPException(status_code=404, detail="Produto ou cliente não encontrado")
    return purchase


@purchase_router.get("/mine", response_model=list[Purchase])
def list_my_purchases(user: CurrentUser) -> list[Purchase]:
    require_role(user, UserRole.CLIENT, UserRole.ADMIN)
    return [p for p in commerce_service.purchases_db.values() if p.client_id == user.id]


@admin_router.get("/users", response_model=list[User])
def list_all_users(user: CurrentUser) -> list[User]:
    require_role(user, UserRole.ADMIN)
    return user_service.list_users()


@admin_router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, user: CurrentUser) -> None:
    require_role(user, UserRole.ADMIN)
    if not user_service.delete_user(user_id):
        raise HTTPException(status_code=404, detail="Usuário não encontrado")


@admin_router.get("/purchases", response_model=list[Purchase])
def list_all_purchases(user: CurrentUser) -> list[Purchase]:
    require_role(user, UserRole.ADMIN)
    return list(commerce_service.purchases_db.values())
