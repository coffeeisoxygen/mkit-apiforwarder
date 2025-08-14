import pytest
from src.schemas.sch_trxdigipos import DigiposMarkup, DigiposTrxModel, ProductEnum


def test_digipos_trxmodel_valid_product():
    valid_product = list(ProductEnum._value2member_map_.keys())[0]
    data = {
        "moduleid": "mod123",
        "product": valid_product,
        "memberid": "member1",
        "dest": "destination1",
        "username": "user1",
        "password": "pass1",
    }
    model = DigiposTrxModel(**data)
    assert model.product == valid_product.upper()


def test_digipos_trxmodel_invalid_product():
    data = {
        "moduleid": "mod123",
        "product": "invalid_product",
        "memberid": "member1",
        "dest": "destination1",
        "username": "user1",
        "password": "pass1",
    }
    with pytest.raises(ValueError, match="Invalid product: invalid_product"):
        DigiposTrxModel(**data)


def test_digipos_trxmodel_default_markup():
    valid_product = list(ProductEnum._value2member_map_.keys())[0]
    data = {"markup": None}
    model = DigiposMarkup(**data)
    assert model.markup == 0


def test_digipos_trxmodel_markup_types():
    valid_product = list(ProductEnum._value2member_map_.keys())[0]
    for markup in [None, 0, "10", 20]:
        data = {"markup": markup}
        model = DigiposMarkup(**data)
        expected = int(markup) if markup is not None else 0
        assert model.markup == expected
