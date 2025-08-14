"""module untuk konstanta digipos."""

from src.utils.enumloader import get_enum, load_enums_from_yaml

enums = load_enums_from_yaml("config/digipos/products.yaml")
PackageProductEnum = get_enum(enums, "PackageProductEnums")
PaymentEnum = get_enum(enums, "PaymentEnums")
