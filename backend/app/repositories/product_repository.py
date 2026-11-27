from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product


class ProductRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, product: Product) -> Product:
        self.session.add(product)
        self.session.flush()
        return product

    def get(self, product_id: int) -> Product | None:
        return self.session.get(Product, product_id)

    def list(self) -> list[Product]:
        statement = select(Product).order_by(Product.id)
        return list(self.session.scalars(statement))

    def delete(self, product: Product) -> None:
        self.session.delete(product)
        self.session.flush()
