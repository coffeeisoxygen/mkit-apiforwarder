"""Member Data Services.

Pure utility functions for member data operations:
- Duplicate checking
- YAML loading and validation
"""

from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from mlogg import logger
from src.custom.cst_exceptions import FileLoaderError
from src.domain.module.sch_module import ModuleInDB


def check_duplicate_moduleids(modules_data: list[dict]) -> list[str]:
    """Check for duplicate moduleids, return list of duplicates."""
    seen_ids = set()
    duplicates = []

    for module in modules_data:
        moduleid = module.get("moduleid")
        if moduleid in seen_ids:
            duplicates.append(moduleid)
        else:
            seen_ids.add(moduleid)

    return duplicates


def load_and_validate_yaml(yaml_path: Path) -> list[ModuleInDB]:
    """Load YAML file and validate each module with Pydantic.

    Pure function that handles complete YAML loading pipeline:
    - File existence check
    - YAML parsing
    - Structure validation
    - Duplicate checking
    - Pydantic validation

    Args:
        yaml_path: Path to YAML file to load

    Returns:
        List of validated MemberInDB objects

    Raises:
        FileNotFoundError: If YAML file doesn't exist
        ValueError: If YAML structure is invalid or duplicates found
        ValidationError: If Pydantic validation fails
    """
    with logger.contextualize(path=yaml_path, operation="load_yaml"):
        # Check file existence
        if not yaml_path.exists():
            logger.error("YAML file not found")
            raise FileNotFoundError(f"YAML file not found: {yaml_path}")

        # Load YAML
        try:
            with yaml_path.open("r", encoding="utf-8") as f:
                data: Any = yaml.safe_load(f)
        except yaml.YAMLError as e:
            logger.error("Failed to parse YAML file", error=str(e))
            raise FileLoaderError("Failed to parse YAML file") from e

        # Validate structure
        if not isinstance(data, dict) or "modules" not in data:
            raise ValueError("YAML must contain 'modules' key")

        modules_list = data["modules"]
        if not isinstance(modules_list, list):
            raise TypeError("'modules' must be a list")

        # Check for duplicates BEFORE Pydantic validation
        duplicates = check_duplicate_moduleids(modules_list)
        if duplicates:
            logger.error("Duplicate memberids found", duplicates=duplicates)
            raise ValueError(f"Duplicate memberids found: {duplicates}")

        # Validate each module with Pydantic
        validated_modules: list[ModuleInDB] = []
        for i, item in enumerate(modules_list):
            try:
                validated_modules.append(ModuleInDB(**item))
            except ValidationError as e:
                logger.error(
                    "Module validation failed", index=i, item=item, error=str(e)
                )
                raise ValueError(f"Module validation failed at index {i}: {e}") from e

        if not validated_modules:
            logger.warning("No valid modules found in YAML file")

        logger.info(
            "Successfully loaded and validated modules", count=len(validated_modules)
        )
        return validated_modules
