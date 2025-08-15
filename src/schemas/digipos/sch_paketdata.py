r"""schema untuk transaksi paket data digipos.

documentasi asli:
    - list product : http://10.0.0.3:10003/list_paket?username=[username]&to=[tujuan]&category=[category]&payment_method=LINKAJA&json=1

NOTE : Validasi Category
NOTE: [category] harus diisi dengan kategori yang valid
NOTE: [trxid] dan [up_harga] bersifat opsional

    - harga per id product : http://10.0.0.3:10003/paket?username=[username]&pin=[pin]&payment_method=LINKAJA&category=[category]&to=[tujuan]&productId=[productId]&check=1

    - beli product : http://10.0.0.3:10003/paket?username=[username]&pin=[pin]&payment_method=LINKAJA&category=[category]&to=[tujuan]&productId=[productId]

"""

from pydantic import field_validator
from sch_trxbase import TrxWithMemberAuth

from src.schemas.digipos.constants import PaketDataEnum


class DigiposReqBase(TrxWithMemberAuth):
    """Base class for Digipos requests.

    validator dsini overide product di base class TrxWithMemberAuth
    """

    @field_validator("category", mode="before")
    @classmethod
    def validate_category(cls, value: str) -> str:
        """Validate the category field.

        This validator checks if the provided category is valid according to the
        PaketDataEnum.

        Args:
            value (str): The category to validate.

        Raises:
            ValueError: If the category is invalid.

        Returns:
            str: The validated category.
        """
        value_upper = value.upper()
        if value_upper not in PaketDataEnum._value2member_map_:
            raise ValueError(f"Invalid category: {value}")
        return value_upper


class DigiposReqListPaketData(DigiposReqBase):
    """Request model for Digipos Paket Data transactions.

    untuk melakukan pengecekan Elligible Paket untuk nomor tersebut.
    """
