r"""schema untuk transaksi paket data digipos.

documentasi asli:
    - list product : http://10.0.0.3:10003/list_paket?username=[username]&to=[tujuan]&category=[category]&payment_method=LINKAJA&json=1

NOTE : Validasi Category
NOTE: [category] harus diisi dengan kategori yang valid
NOTE: [trxid] dan [up_harga] bersifat opsional

    - harga per id product : http://10.0.0.3:10003/paket?username=[username]&pin=[pin]&payment_method=LINKAJA&category=[category]&to=[tujuan]&productId=[productId]&check=1

    - beli product : http://10.0.0.3:10003/paket?username=[username]&pin=[pin]&payment_method=LINKAJA&category=[category]&to=[tujuan]&productId=[productId]

"""

from pydantic import BaseModel, Field, field_validator

from src.schemas.sch_trxbase import TrxWithMemberAuth


class DigiposOptionalFilterParams(BaseModel):
    subproduct: str | None = Field(
        default="",
        description="Sub-category of the product, biasa nya subproduct hanya alphabet",
        pattern=r"^[A-Za-z]+$",
    )
    duration: int | None = Field(
        default=0, description="Duration for the product, if applicable."
    )


class DigiposOptionalMarkupParams(BaseModel):
    markup: int = Field(
        default=0,
        description="Markup nominal for the product, if applicable.",
    )

    @field_validator("markup")
    @classmethod
    def validate_markup(cls, v: int) -> int:
        # Accept any integer, including negative values
        if not isinstance(v, int):
            raise TypeError("markup must be an integer")
        return v

    # TODO : Add Params Lain Seperti Up harga Min Harga Max harga dan lain lain.


class DigiposReqListPaketData(
    TrxWithMemberAuth, DigiposOptionalFilterParams, DigiposOptionalMarkupParams
):
    """Request model for Digipos Paket Data transactions.

    untuk melakukan pengecekan Elligible Paket untuk nomor tersebut.
    ini hanya parameters opsional
    validasi product akan di lakukan di level service
    """

    pass


class DigiposReqCheckBuyPaket(TrxWithMemberAuth, DigiposOptionalMarkupParams):
    """Request model for Digipos Paket Data purchase transactions.

    untuk melakukan pembelian Paket untuk nomor tersebut.
    ini hanya parameters opsional
    validasi product akan di lakukan di level service
    """

    productid: str = Field(
        description="ID product yg di dapatkan dari list Paket, biasa nya hanya angka",
        pattern=r"^[0-9]+$",
    )
    check: bool = Field(
        default=True,
        description=(
            "Jika ingin melakukan pengecekan ulang harga setelah list, gunakan check=1. "
            "Jika sudah yakin, tidak perlu kirim check atau gunakan check=0. "
            "Nilai 1/True akan melakukan pengecekan harga, nilai 0/False akan melewati pengecekan."
        ),
    )

    @field_validator("check", mode="before")
    @classmethod
    def validate_check(cls, v: int | str | bool) -> bool:
        """Accepts 1/0, True/False, '1'/'0' and converts to boolean."""
        if v in (1, "1", True):
            return True
        if v in (0, "0", False):
            return False
        raise ValueError("check must be 1, 0, True, or False")
