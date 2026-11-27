from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.purchase import Purchase


class PurchaseRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, purchase: Purchase) -> Purchase:
        self.session.add(purchase)
        self.session.flush()
        return purchase

    def get(self, purchase_id: int) -> Purchase | None:
        return self.session.get(Purchase, purchase_id)

    def list(self) -> list[Purchase]:
        statement = select(Purchase).order_by(Purchase.id)
        return list(self.session.scalars(statement))

    def list_by_client(self, client_id: int) -> list[Purchase]:
        statement = (
            select(Purchase)
            .where(Purchase.client_id == client_id)
            .order_by(Purchase.id)
        )
        return list(self.session.scalars(statement))
