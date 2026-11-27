from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class UserRole(StrEnum):
    CLIENT = "client"
    SELLER = "seller"
    ADMIN = "admin"


class UserBase(BaseModel):
    nome: str
    email: str
    idade: int


class UserCreate(UserBase):
    role: UserRole = UserRole.CLIENT


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: UserRole = UserRole.CLIENT
    saldo: float = 0


class UserPatch(BaseModel):
    nome: str | None = None
    email: str | None = None
    idade: int | None = None
    role: UserRole | None = None
