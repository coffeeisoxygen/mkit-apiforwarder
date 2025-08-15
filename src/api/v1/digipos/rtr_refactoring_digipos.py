from enum import StrEnum
from typing import Annotated

from fastapi import APIRouter, Query
from src.schemas.digipos.trx_paketdata import DigiposReqListPaketData

router = APIRouter()


class DigiposServiceEnum(StrEnum):
    paket_data = "paket_data"
    pulsa = "pulsa"


@router.get("/list")
def get_products(paketdata: Annotated[DigiposReqListPaketData, Query(...)]):
    # Mocked response for product listing
    return {
        "products": [{"id": "1", "name": "Paket Data"}, {"id": "2", "name": "Pulsa"}]
    }
