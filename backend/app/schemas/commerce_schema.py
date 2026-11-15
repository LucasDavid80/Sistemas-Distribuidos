from pydantic import BaseModel, ConfigDict, Field


class BalanceDeposit(BaseModel):
    amount: float = Field(gt=0)


class ProductCreate(BaseModel):
    nome: str
    descricao: str = ""
    preco: float = Field(gt=0)
    estoque: int = Field(ge=0)


class Product(ProductCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    seller_id: int


class ProductPatch(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    preco: float | None = Field(default=None, gt=0)
    estoque: int | None = Field(default=None, ge=0)


class PurchaseCreate(BaseModel):
    product_id: int
    quantidade: int = Field(gt=0)


class Purchase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client_id: int
    product_id: int
    quantidade: int
    total: float
