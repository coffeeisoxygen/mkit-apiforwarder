"""class untuk bertransaksi digipos.

inherit dari base model, TrxRequestBase, dan untuk response transaksi juga menggunakan TrxResponseBase.
"""

from pydantic import Field, field_validator

from src.schemas.sch_trxbase import TrxAuthFields, TrxBaseModel
from src.utils.enumloader import get_enum, load_enums_from_yaml

enums = load_enums_from_yaml("config/digipos/products.yaml")
ProductEnum = get_enum(enums, "ProductEnums")
PaymentEnum = get_enum(enums, "PaymentEnums")


class DigiposTrxModel(TrxBaseModel, TrxAuthFields):
    """Model untuk transaksi Digipos."""

    moduleid: str = Field(..., description="ID modul Account transaksi Digipos")
    markup: str | int | None = Field(
        0, description="Markup harga untuk transaksi Digipos, default 0"
    )

    @field_validator("product", mode="before")
    @classmethod
    def validate_product(cls, value: str) -> str:
        value_upper = value.upper() if isinstance(value, str) else value
        if value_upper not in ProductEnum._value2member_map_:
            raise ValueError(f"Invalid product: {value}")
        return value_upper
