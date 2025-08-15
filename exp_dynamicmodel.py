"""experimenting validating transaction requests mode."""

from pydantic import BaseModel


class TrxRequest(BaseModel):
    memberid: str
    dest: str
    product: str
    trxid: str


class TrxWithSign(TrxRequest):
    sign: str


class TrxPinPass(TrxRequest):
    pin: str
    password: str


def detect_and_parse(payload: dict):
    """Auto detect payload type and parse to correct model."""
    if "sign" in payload:
        return TrxWithSign(**payload)
    elif "pin" in payload and "password" in payload:
        return TrxPinPass(**payload)
    else:
        raise ValueError("Payload harus mengandung sign atau pin+password")


def main():
    # Contoh payload sign
    payload_sign = {
        "memberid": "123",
        "dest": "456",
        "product": "789",
        "trxid": "abc",
        "sign": "signature",
    }
    # Contoh payload pin/pass
    payload_pinpass = {
        "memberid": "321",
        "dest": "654",
        "product": "987",
        "trxid": "def",
        "pin": "1234",
        "password": "passw0rd",
    }
    # Contoh payload basic (harus error)
    payload_basic = {"memberid": "111", "dest": "222", "product": "333", "trxid": "xyz"}

    for payload in [payload_sign, payload_pinpass, payload_basic]:
        try:
            model = detect_and_parse(payload)
            print(model.__class__.__name__, model.model_dump_json())
        except ValueError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
