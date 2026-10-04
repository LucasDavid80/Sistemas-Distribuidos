from app.schemas.commerce_schema import Product, ProductCreate, ProductPatch, Purchase
from app.services import user_service

products_db: dict[int, Product] = {}
purchases_db: dict[int, Purchase] = {}
next_product_id = 1
next_purchase_id = 1


def create_product(data: ProductCreate, seller_id: int) -> Product:
    global next_product_id
    product = Product(id=next_product_id, seller_id=seller_id, **data.model_dump())
    products_db[next_product_id] = product
    next_product_id += 1
    return product


def update_product(product_id: int, data: ProductPatch) -> Product | None:
    product = products_db.get(product_id)
    if product is None:
        return None
    updated = product.model_copy(update=data.model_dump(exclude_none=True))
    products_db[product_id] = updated
    return updated


def purchase_product(product_id: int, client_id: int, quantity: int) -> Purchase | None:
    global next_purchase_id
    product = products_db.get(product_id)
    client = user_service.get_user(client_id)
    if product is None or client is None:
        return None
    if product.estoque < quantity:
        raise ValueError("Estoque insuficiente")
    total = product.preco * quantity
    if client.saldo < total:
        raise ValueError("Saldo insuficiente")

    products_db[product_id] = product.model_copy(
        update={"estoque": product.estoque - quantity}
    )
    user_service.users_db[client_id] = client.model_copy(
        update={"saldo": client.saldo - total}
    )
    purchase = Purchase(
        id=next_purchase_id,
        client_id=client_id,
        product_id=product_id,
        quantidade=quantity,
        total=total,
    )
    purchases_db[next_purchase_id] = purchase
    next_purchase_id += 1
    return purchase
