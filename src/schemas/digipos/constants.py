from enum import StrEnum
from pathlib import Path
from typing import Any

import yaml


def load_products_yaml(path: Path) -> list[dict[str, Any]]:
    """Load products from a YAML file."""
    try:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data["products"]
    except Exception as e:
        raise RuntimeError(f"Failed to load products YAML: {e}") from e


def create_str_enum(enum_name: str, items: list[str]) -> StrEnum:
    """Create a StrEnum from a list of strings."""
    return StrEnum(enum_name, {item: item for item in items})


def create_str_enum_by_type(
    enum_name: str, products: list[dict[str, Any]], prod_type: str
) -> StrEnum:
    """Create a StrEnum for products of a specific type."""
    items = [p["product"] for p in products if p["type"] == prod_type]
    return create_str_enum(enum_name, items)


def create_payment_str_enum(enum_name: str, products: list[dict[str, Any]]) -> StrEnum:
    """Create a StrEnum for payment methods in products."""
    payment_methods = {p["payment_method"] for p in products if p.get("payment_method")}
    return create_str_enum(enum_name, list(payment_methods))


# Load products dari YAML
config_path = (
    Path(__file__).resolve().parent.parent.parent / "config/digipos/products.yaml"
)
products_list = load_products_yaml(config_path)


class ProductTypeEnum(StrEnum):
    """Product type enumeration."""

    paketdata = "paketdata"
    pulsa = "pulsa"
    voucher = "voucher"


# ProductEnum (all products)
ProductEnum = create_str_enum("ProductEnum", [p["product"] for p in products_list])
# PaketDataEnum
PaketDataEnum = create_str_enum_by_type(
    "PaketDataEnum", products_list, ProductTypeEnum.paketdata
)
# PulsaEnum
PulsaEnum = create_str_enum_by_type("PulsaEnum", products_list, ProductTypeEnum.pulsa)
# VoucherEnum
VoucherEnum = create_str_enum_by_type(
    "VoucherEnum", products_list, ProductTypeEnum.voucher
)
# PaymentEnum
PaymentEnum = create_payment_str_enum("PaymentEnum", products_list)
