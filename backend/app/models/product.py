from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.purchase import Purchase
    from app.models.user import User


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("preco > 0", name="ck_products_preco_positive"),
        CheckConstraint("estoque >= 0", name="ck_products_estoque_nonnegative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    descricao: Mapped[str] = mapped_column(String(1000), nullable=False, default="")
    preco: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    estoque: Mapped[int] = mapped_column(nullable=False)
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    seller: Mapped["User"] = relationship(back_populates="products")
    purchases: Mapped[list["Purchase"]] = relationship(back_populates="product")
