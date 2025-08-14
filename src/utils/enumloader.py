from enum import Enum, EnumMeta
from typing import cast

import yaml


def create_enum_from_dict(enum_name: str, enum_members: dict) -> EnumMeta:
    """Dynamically creates an Enum class from a dictionary."""
    return cast(EnumMeta, Enum(enum_name, enum_members))


def load_enums_from_yaml(filepath: str) -> dict[str, EnumMeta]:
    """Loads enum definitions from a YAML file and creates Enum classes."""
    with open(filepath, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    enums = {}
    # Support nested 'enums' key as in products.yaml
    enum_section = data.get("enums", data)
    for enum_name, members in enum_section.items():
        enums[enum_name] = create_enum_from_dict(enum_name, members)
    return enums


def get_enum(enum_dict: dict[str, EnumMeta], name: str) -> EnumMeta:
    """Get Enum class by name from loaded enums."""
    return enum_dict[name]
