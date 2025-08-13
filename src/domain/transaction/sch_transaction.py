"""schemas transaksi global all provider."""

from pydantic import BaseModel


class TrxBaseModel(BaseModel):
    memberid: str
    dest: str
    product: str
    pin: str | None = None
    password: str | None = None
    sign: str | None = None
    refid: str | None = None


# NOTE : Tidak defining Rule Config , agar Subclass overide masing masing.


class DigiposTrxModel(TrxBaseModel):
    moduleid: str


class IsimpleTrxModel(TrxBaseModel):
    moduleid: str
