from src.utils.enumloader import get_enum, load_enums_from_yaml


def test_load_enums_from_yaml():
    enums = load_enums_from_yaml("config/digipos/products.yaml")
    assert "ProductEnums" in enums
    assert "PaymentEnums" in enums
    product_enum = get_enum(enums, "ProductEnums")
    payment_enum = get_enum(enums, "PaymentEnums")
    # Check enum members using getattr for dynamic Enum
    assert product_enum.DATA.value == "DATA"  # type: ignore
    assert product_enum.VOICE_SMS.value == "VOICE_SMS"  # type: ignore
    assert payment_enum.LINKAJA.value == "LINKAJA"  # type: ignore
    assert payment_enum.NGRS.value == "NGRS"  # type: ignore


def test_enum_type():
    enums = load_enums_from_yaml("config/digipos/products.yaml")
    product_enum = get_enum(enums, "ProductEnums")
    assert isinstance(product_enum.DATA, product_enum)  # type: ignore
