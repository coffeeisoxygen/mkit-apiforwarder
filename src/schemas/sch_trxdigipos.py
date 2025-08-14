"""class untuk bertransaksi digipos.

inherit dari base model, TrxRequestBase, dan untuk response transaksi juga menggunakan TrxResponseBase.
"""

from pydantic import Field

from src.schemas.sch_trxbase import TrxAuthFields, TrxBaseModel


class DigiposTrxModel(TrxBaseModel, TrxAuthFields):
    """Model untuk transaksi Digipos."""

    moduleid: str = Field(..., description="ID modul Account transaksi Digipos")
    markup: str | int | None = Field(
        0, description="Markup harga untuk transaksi Digipos, default 0"
    )
