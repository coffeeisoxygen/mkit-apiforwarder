from pydantic import BaseModel, Field


class RequiredParams(BaseModel):
    username: str
    to: str
    up_harga: str | int
    trxid: str | int | None = None
    category: str
    payment_method: str
    kolom: str


class Product(BaseModel):
    productid: str
    name: str
    provider: str
    type: str
    is_active: bool
    api_path: str
    method: str
    mark_json: int = Field(alias="json")
    required_params: RequiredParams
    optional_params: dict[str, str | int] | None = None
    list_modules: list[str]  # moduleid saja


class DigiposConfig(BaseModel):
    products: list[Product]
