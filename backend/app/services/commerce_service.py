from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.product import Product as ProductModel
from app.models.purchase import Purchase as PurchaseModel
from app.repositories.product_repository import ProductRepository
from app.repositories.purchase_repository import PurchaseRepository
from app.repositories.user_repository import UserRepository
from app.schemas.commerce_schema import ProductCreate, ProductPatch


def create_product(db: Session, data: ProductCreate, seller_id: int) -> ProductModel:
    product = ProductModel(seller_id=seller_id, **data.model_dump())
    ProductRepository(db).add(product)
    db.commit()
    db.refresh(product)
    return product


def list_products(db: Session) -> list[ProductModel]:
    return ProductRepository(db).list()


def get_product(db: Session, product_id: int) -> ProductModel | None:
    return ProductRepository(db).get(product_id)


def update_product(
    db: Session, product_id: int, data: ProductPatch
) -> ProductModel | None:
    repository = ProductRepository(db)
    product = repository.get(product_id)
    if product is None:
        return None

    for field, value in data.model_dump(exclude_none=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> bool:
    repository = ProductRepository(db)
    product = repository.get(product_id)
    if product is None:
        return False

    repository.delete(product)
    db.commit()
    return True


def purchase_product(
    db: Session, product_id: int, client_id: int, quantity: int
) -> PurchaseModel | None:
    product = ProductRepository(db).get(product_id)
    client = UserRepository(db).get(client_id)
    if product is None or client is None:
        return None
    if product.estoque < quantity:
        raise ValueError("Estoque insuficiente")

    total = product.preco * quantity
    if client.saldo < total:
        raise ValueError("Saldo insuficiente")

    product.estoque -= quantity
    client.saldo -= total
    purchase = PurchaseModel(
        client_id=client_id,
        product_id=product_id,
        quantidade=quantity,
        total=Decimal(str(total)),
    )
    PurchaseRepository(db).add(purchase)
    db.commit()
    db.refresh(purchase)
    return purchase


def list_purchases(db: Session) -> list[PurchaseModel]:
    return PurchaseRepository(db).list()


def list_purchases_by_client(db: Session, client_id: int) -> list[PurchaseModel]:
    return PurchaseRepository(db).list_by_client(client_id)
