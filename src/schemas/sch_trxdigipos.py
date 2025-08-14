"""class untuk bertransaksi digipos.

inherit dari base model, TrxRequestBase, dan untuk response transaksi juga menggunakan TrxResponseBase.

common issues:
- jika tanpa api ini adalah :
    - exposing credentials : username, pin , password dari akun API
- dengan api ini:
    - trx otomax ke api akan di validasi dengan pin passwod / sign
    - moduleid : credentials akun API yg di simpan di yaml | switch
    - product : equivalen dengan category yg ada di API Digipos
    - support all params actual dari API Digipos ASL.
"""

from pydantic import BaseModel, Field, field_validator

from src.schemas.sch_trxbase import TrxBaseModel, TrxMemberAuthModel
from src.utils.enumloader import get_enum, load_enums_from_yaml

enums = load_enums_from_yaml("config/digipos/products.yaml")
PackageProductEnum = get_enum(enums, "PackageProductEnums")
PaymentEnum = get_enum(enums, "PaymentEnums")


class DigiposAuthModel(TrxBaseModel, TrxMemberAuthModel):
    """Model untuk transaksi Digipos.

    moduleid adalah data module digios yg ada di yaml
    ini wajib udah ada.
    model Base ini Support untuk transaksi package(paket) / Pulsa Dan Lain Lain.
    """

    moduleid: str = Field(
        ...,
        description="ID modul Account API Digipos, ini equvalen dengan username=<username>",
    )

    @field_validator("product", mode="before")
    @classmethod
    def validate_product(cls, value: str) -> str:
        value_upper = value.upper() if isinstance(value, str) else value
        if value_upper not in PackageProductEnum._value2member_map_:
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


class DigiposPMLinkAja(BaseModel):
    """Model untuk payment method LinkAja pada transaksi Digipos."""

    pm: str = Field(
        description="Payment method yang di gunakan,equivalen dengan payment_method=<payment_method>"
    )

    @field_validator("pm", mode="before")
    @classmethod
    def validate_payment_method(cls, value: str) -> str:
        value_upper = value.upper() if isinstance(value, str) else value
        if value_upper != "LINKAJA":
            raise ValueError("Payment method must be LINKAJA")
        if value_upper not in PaymentEnum._value2member_map_:
            raise ValueError(f"Invalid payment method: {value}")
        return value_upper


class DigiposPMNgrs(BaseModel):
    """Model untuk payment method Ngrs pada transaksi Digipos."""

    pm: str = Field(
        description="Payment method yang di gunakan,equivalen dengan payment_method=<payment_method>"
    )

    @field_validator("pm", mode="before")
    @classmethod
    def validate_payment_method(cls, value: str) -> str:
        value_upper = value.upper() if isinstance(value, str) else value
        if value_upper != "NGRS":
            raise ValueError("Payment method must be NGRS")
        if value_upper not in PaymentEnum._value2member_map_:
            raise ValueError(f"Invalid payment method: {value}")
        return value_upper


# untuk mode transaksi yg berkaitan dengan Paket Internet dan Enums Products.
class DigiposTrxEligiblePackageList(DigiposAuthModel, DigiposMarkup, DigiposPMLinkAja):
    """Model untuk transaksi check List Paket Eligible untuk nomor user.

    endpoint:
        yang akan menggunakan ini adalah /digipos/list?
    return expected adalah list product2 yang eligible untuk destination
    """

    subproduct: str | None = Field(
        description="optional filter,ini equivalen dengan productSubCategory=<subproduct>"
    )
    duration: str | None = Field(description="ini equivalen dengan duration=<duration>")

    col: list[str] | None = Field(
        default=["productId,productSubCategory,productName,quota,duration,total_"],
        description="List kolom yang di gunakan, ini equivalen dengan kolom=productId,productSubCategory,duration, dan lain lain.",
    )


class DigiposTrxBuyPackage(DigiposAuthModel, DigiposMarkup, DigiposPMLinkAja):
    """Model untuk transaksi beli produk grup package.

    endpoint:
        yang akan menggunakan ini adalah /digipos/buy?
    """

    productid: str = Field(description="ini equivalen dengan productId=<productId>")
    check: str | int = Field(
        description="ini equivalen dengan check=<check>, jika check = 1 maka akan melakukan re validasi harga 1x lagi , jika check = 0 maka ini di anggap langsung membeli."
    )

    @field_validator("check", mode="before")
    @classmethod
    def validate_check(cls, value: str | int) -> int:
        """Validator to ensure check is only 1 or 0."""
        if isinstance(value, str):
            if value not in ("0", "1"):
                raise ValueError("check must be '0' or '1'")
            return int(value)
        if value not in (0, 1):
            raise ValueError("check must be 0 or 1")
        return value
