import logging

import pytest

from .exp_builder import build_query

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# mock module
module = {
    "base_url": "http://10.0.0.3:10003",
    "username": "WIR6289504",
    "pin": "123456",
    "provider": "digipos",
}

# mock products
products = [
    {"product": "DATA", "name": "Check Eligible Paket Digipos"},
    {"product": "VOICE_SMS", "name": "Check Eligible Paket SMS"},
]

# mock default params
default_params = {
    "list_paket": {
        "api_path": "/list_paket",
        "method": "GET",
        "required_params": {
            "username": "WIR6289504",
            "to": None,
            "up_harga": None,
            "trxid": None,
            "payment_method": "LINKAJA",
            "category": "default_category",
        },
        "kolom": [
            "productId",
            "productSubCategory",
            "productName",
            "quota",
            "duration",
            "total_",
        ],
    },
    "paket": {
        "api_path": "/paket",
        "method": "GET",
        "required_params": {
            "username": "WIR6289504",
            "pin": "123456",
            "payment_method": "LINKAJA",
            "category": "default_category",
            "to": None,
            "productId": None,
            "trxid": None,
            "check": None,
        },
    },
}

# -------------------
# Tests
# -------------------


def test_list_paket():
    runtime = {"to": "081295221639", "up_harga": 100, "trxid": "1LIST"}
    product = products[0]  # DATA

    url, params = build_query(module, product, default_params, "list_paket", runtime)
    print("URL:", url)
    print("Params:", params)
    logger.info(f"test_list_paket URL: {url}")
    logger.info(f"test_list_paket Params: {params}")

    assert "category=DATA" in url
    assert "to=081295221639" in url
    assert "up_harga=100" in url
    assert (
        params["kolom"]
        == "productId,productSubCategory,productName,quota,duration,total_"
    )


def test_paket_check():
    runtime = {
        "to": "08123456789",
        "trxid": "TRX123",
        "check": 1,
        "productId": "00017864",
    }
    product = products[0]  # DATA

    url, params = build_query(module, product, default_params, "paket", runtime)
    print("URL:", url)
    print("Params:", params)
    logger.info(f"test_paket_check URL: {url}")
    logger.info(f"test_paket_check Params: {params}")

    assert "category=DATA" in url
    assert params["check"] == 1
    assert params["productId"] == "00017864"


def test_paket_buy():
    runtime = {
        "to": "08123456789",
        "trxid": "TRX456",
        "check": 0,
        "productId": "00017864",
    }
    product = products[0]  # DATA

    url, params = build_query(module, product, default_params, "paket", runtime)
    print("URL:", url)
    print("Params:", params)
    logger.info(f"test_paket_buy URL: {url}")
    logger.info(f"test_paket_buy Params: {params}")

    assert "category=DATA" in url
    assert params["check"] == 0
    assert params["productId"] == "00017864"


def test_missing_productId_raises():
    runtime = {"to": "08123456789", "trxid": "TRX999", "check": 1}
    product = products[0]  # DATA

    logger.info("test_missing_productId_raises started")
    with pytest.raises(ValueError):
        build_query(module, product, default_params, "paket", runtime)
