from typing import TYPE_CHECKING

from sqlalchemy import Enum, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.schemas.user_schema import UserRole

if TYPE_CHECKING:
    from app.models.product import Product
    from app.models.purchase import Purchase


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True)
    idade: Mapped[int] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            name="user_role",
            values_callable=lambda enum: [member.value for member in enum],
        ),
        nullable=False,
        default=UserRole.CLIENT,
    )
    saldo: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)

    products: Mapped[list["Product"]] = relationship(back_populates="seller")
    purchases: Mapped[list["Purchase"]] = relationship(back_populates="client")
