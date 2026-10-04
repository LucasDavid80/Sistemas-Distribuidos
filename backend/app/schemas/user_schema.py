from pydantic import BaseModel


class UserBase(BaseModel):
    nome: str
    email: str
    idade: int


class User(UserBase):
    id: int
