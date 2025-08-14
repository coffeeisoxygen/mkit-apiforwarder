"""class untuk bertransaksi digipos.

inherit dari base model, TrxRequestBase, dan untuk response transaksi juga menggunakan TrxResponseBase.

common issues:
- jika tanpa api ini adalah :
    - exposing credentials : username, pin , password dari akun API
- dengan api ini:
    - trx otomax ke api akan di validasi dengan pin passwod / sign
    - moduleid : credentials akun API yg di simpan di yaml | switch
    - product : equivalen dengan category yg ada di API Digipos
    - subproduct: equivalen dengan productSubCategory
    - support all params actual dari API Digipos ASL.
"""

from pydantic import BaseModel, Field, field_validator

from src.schemas.sch_trxbase import TrxAuthFields, TrxBaseModel
from src.utils.enumloader import get_enum, load_enums_from_yaml

enums = load_enums_from_yaml("config/digipos/products.yaml")
ProductEnum = get_enum(enums, "ProductEnums")
PaymentEnum = get_enum(enums, "PaymentEnums")


class DigiposTrxModel(TrxBaseModel, TrxAuthFields):
    """Model untuk transaksi Digipos.

    moduleid adalah data module digios yg ada di yaml
    ini wajib udah ada.
    """

    moduleid: str = Field(
        ...,
        description="ID modul Account API Digipos, ini equvalen dengan username=<username>",
    )

    @field_validator("product", mode="before")
    @classmethod
    def validate_product(cls, value: str) -> str:
        value_upper = value.upper() if isinstance(value, str) else value
        if value_upper not in ProductEnum._value2member_map_:
            raise ValueError(f"Invalid product: {value}")
        return value_upper


class DigiposMarkup(BaseModel):
    """Model untuk markup transaksi Digipos."""

    markup: str | int | None = Field(
        default=0,
        description="Markup untuk transaksi,ini equivalen dengan up_harga=<markup>",
    )

    @field_validator("markup", mode="before")
    @classmethod
    def validate_markup(cls, value: str | int | None) -> int:
        if value is None:
            return 0
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                return 0
        return value


class DigiposTrxModelList(DigiposTrxModel, DigiposMarkup):
    """Model untuk transaksi check List Paket Eligible.

    endpoint:
        yang akan menggunakan ini adalah /digipos/list?
    """

    subproduct: str | None = Field(
        description="ini equivalen dengan productSubCategory=<subproduct>"
    )
    duration: str | None = Field(description="ini equivalen dengan duration=<duration>")
    pm: str = Field(
        description="Payment method yang di gunakan,equivalen dengan payment_method=<payment_method>"
    )
    col: list[str] | None = Field(
        default=["productId,productSubCategory,productName,quota,duration,total_"],
        description="List kolom yang di gunakan, ini equivalen dengan kolom=productId,productSubCategory,duration, dan lain lain.",
    )
