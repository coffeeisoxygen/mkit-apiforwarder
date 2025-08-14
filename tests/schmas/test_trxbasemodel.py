import pytest
from pydantic import ValidationError
from src.schemas.sch_trxbase import TrxAuthFields, TrxBaseModel, TrxResponse

# pyright: reportUndefinedVariable=false, reportGeneralTypeIssues=false, reportCallIssue=false


def test_trx_base_model_required_fields():
    # All required fields present
    obj = TrxBaseModel(memberid="123", dest="08123456789", product="pulsa", trxid=None)
    assert obj.memberid == "123"
    assert obj.dest == "08123456789"
    assert obj.product == "pulsa"
    assert obj.trxid is None


def test_trx_base_model_missing_required():
    # Missing required field should raise ValidationError
    with pytest.raises(ValidationError):
        TrxBaseModel(dest="08123456789", product="pulsa")


def test_trx_auth_fields_optional():
    obj = TrxAuthFields(pin="1234", password=None, sign="abc")
    assert obj.pin == "1234"
    assert obj.password is None
    assert obj.sign == "abc"


def test_trx_response_build_method():
    resp = TrxResponse.build(
        refid="trx123",
        status="success",
        dest="08123456789",
        product="pulsa",
        raw_message="OK",
    )
    assert resp.refid == "trx123"
    assert resp.status == "SUCCESS"
    assert resp.dest == "08123456789"
    assert "Transaksi pulsa ke 08123456789 status SUCCESS" in resp.message
    assert resp.raw_message == "OK"


def test_trx_response_build_method_no_raw_message():
    resp = TrxResponse.build(
        refid="trx456", status="failed", dest="08123456789", product="token"
    )
    assert resp.status == "FAILED"
    assert resp.raw_message is None
    assert "output:" in resp.message


def test_trx_response_validation():
    # All required fields present
    resp = TrxResponse(
        refid="trx789",
        status="SUCCESS",
        dest="08123456789",
        message="Transaksi berhasil",
    )
    assert resp.refid == "trx789"
    assert resp.status == "SUCCESS"
    assert resp.dest == "08123456789"
    assert resp.message == "Transaksi berhasil"
    assert resp.raw_message is None

    # Missing required field should raise ValidationError
    with pytest.raises(ValidationError):
        TrxResponse(status="SUCCESS", dest="08123456789", message="OK")
