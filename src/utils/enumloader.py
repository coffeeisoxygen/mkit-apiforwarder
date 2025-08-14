from enum import Enum, EnumMeta
from typing import cast

import yaml


class DynamicDictEnumLoader:
    """Utility for dynamically creating Enum classes from dictionary definitions.

    This is useful for loading enums from configuration files (YAML, JSON, etc),
    especially when enum definitions may change or expand over time.

    Usage:
        # Example: Load products from a YAML file (list of dicts)
        import yaml
        with open('products.yaml', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        products_list = data['products']
        product_enum_dict = {p['product']: p['product'] for p in products_list}
        ProductEnum = DynamicDictEnumLoader.create_enum_from_dict('ProductEnum', product_enum_dict)
        # Now you can use ProductEnum.DATA, ProductEnum.VOICE_SMS, etc.
    """

    @staticmethod
    def create_enum_from_dict(enum_name: str, enum_members: dict) -> EnumMeta:
        """Dynamically creates an Enum class from a dictionary.

        Args:
            enum_name (str): Name of the Enum class.
            enum_members (dict): Dictionary of enum members.

        Returns:
            EnumMeta: The created Enum class.
        """
        return cast(EnumMeta, Enum(enum_name, enum_members))

    @staticmethod
    def load_enums_from_yaml(filepath: str) -> dict[str, EnumMeta]:
        """Loads enum definitions from a YAML file and creates Enum classes.

        Expects a dictionary of enums, not a list.

        Args:
            filepath (str): Path to the YAML file.

        Returns:
            dict[str, EnumMeta]: Dictionary of Enum classes.
        """
        with open(filepath, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        enums = {}
        # Support nested 'enums' key as in products.yaml
        enum_section = data.get("enums", data)
        for enum_name, members in enum_section.items():
            enums[enum_name] = DynamicDictEnumLoader.create_enum_from_dict(
                enum_name, members
            )
        return enums

    @staticmethod
    def get_enum(enum_dict: dict[str, EnumMeta], name: str) -> EnumMeta:
        """Get Enum class by name from loaded enums.

        Args:
            enum_dict (dict[str, EnumMeta]): Dictionary of Enum classes.
            name (str): Name of the Enum class to retrieve.

        Returns:
            EnumMeta: The requested Enum class.
        """
        return enum_dict[name]
