# ruff : noqa T201
from enum import Enum, StrEnum
from pathlib import Path

import yaml

# Load products dari YAML
config_path = Path().resolve().parent.parent.parent / "config/digipos/products.yaml"
with open(config_path, encoding="utf-8") as f:
    data = yaml.safe_load(f)

products_list = data["products"]


class ProductTypeEnum(StrEnum):
    paketdata = "paketdata"
    pulsa = "pulsa"
    voucher = "voucher"


# ProductEnum (all products)
ProductEnum = Enum("ProductEnum", {p["product"]: p["product"] for p in products_list})
# PaketDataEnum
PaketDataEnum = Enum(
    "PaketDataEnum",
    {
        p["product"]: p["product"]
        for p in products_list
        if p["type"] == ProductTypeEnum.paketdata
    },
)
# Pulsa Enums
PulsaEnum = Enum(
    "PulsaEnum",
    {
        p["product"]: p["product"]
        for p in products_list
        if p["type"] == ProductTypeEnum.pulsa
    },
)

# Voucher Enums
VoucherEnum = Enum(
    "VoucherEnum",
    {
        p["product"]: p["product"]
        for p in products_list
        if p["type"] == ProductTypeEnum.voucher
    },
)

# 3. PaymentEnum (all payment_method dari products, skip None)
payment_methods = {p["payment_method"] for p in products_list if "payment_method" in p}
PaymentEnum = Enum("PaymentEnum", {pm: pm for pm in payment_methods})


def main():
    # Usage example
    print(list(ProductTypeEnum))
    print(list(PaketDataEnum.__members__.values()))
    print(list(PulsaEnum))
    print(list(VoucherEnum))
    print(list(PaymentEnum))


if __name__ == "__main__":
    main()
