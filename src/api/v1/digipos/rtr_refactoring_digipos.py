from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

router = APIRouter()


# ----- Base & Variant Models -----
class TrxRequest(BaseModel):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "memberid": "123",
                    "dest": "456",
                    "product": "789",
                    "trxid": "abc",
                    "sign": "signature",
                },
                {
                    "memberid": "321",
                    "dest": "654",
                    "product": "987",
                    "trxid": "def",
                    "pin": "1234",
                    "password": "passw0rd",
                },
            ]
        }
    }
    memberid: str = Field(..., description="ID member yang akan bertransaksi")
    dest: str = Field(..., description="Tujuan transaksi")
    product: str = Field(..., description="Produk yang akan di-transaksikan")
    trxid: str | None = Field(None, description="ID transaksi dari member")


class TrxWithSign(TrxRequest):
    sign: str = Field(..., description="Signature verifikasi transaksi")


class TrxPinPass(TrxRequest):
    pin: str = Field(..., description="PIN verifikasi transaksi")
    password: str = Field(..., description="Password verifikasi transaksi")


# ----- Detector -----
def detect_and_parse(payload: dict) -> TrxWithSign | TrxPinPass:
    if payload.get("sign"):
        return TrxWithSign(**payload)
    elif "pin" in payload and "password" in payload:
        return TrxPinPass(**payload)
    else:
        raise ValueError("Payload harus mengandung 'sign' atau 'pin'+'password'")


# ----- Dependency untuk ambil payload -----
async def get_trx_payload(request: Request):
    # Bisa handle GET & POST
    if request.method == "POST":
        raw_data = await request.json()
    else:
        raw_data = dict(request.query_params)

    try:
        return detect_and_parse(raw_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ----- Router -----
@router.get("/trx", response_model=TrxRequest)
@router.post("/trx", response_model=TrxRequest)
async def handle_trx(payload: TrxRequest = Depends(get_trx_payload)):
    return payload
