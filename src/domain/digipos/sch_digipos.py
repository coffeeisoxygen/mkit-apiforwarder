from pydantic import BaseModel, Field


class DGReqParams(BaseModel):
    username: str
    to: str
    up_harga: str | int
    trxid: str | int | None = None
    category: str
    payment_method: str
    kolom: str


class DGProductInDB(BaseModel):
    productid: str
    name: str
    provider: str
    type: str
    is_active: bool
    api_path: str
    method: str
    mark_json: int = Field(alias="json")
    required_params: DGReqParams
    optional_params: dict[str, str | int] | None = None
    list_modules: list[str]  # moduleid saja


class DgProducList(BaseModel):
    products: list[DGProductInDB]
