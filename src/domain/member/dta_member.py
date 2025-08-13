"""Member Data Services.

Pure utility functions for member data operations:
- Duplicate checking
- YAML loading and validation
"""

from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from src.custom.cst_exceptions import FileLoaderError
from src.domain.member.sch_member import MemberInDB
from src.mlogg import logger


def check_duplicate_memberids(members_data: list[dict]) -> list[str]:
    """Check for duplicate memberids, return list of duplicates."""
    seen_ids = set()
    duplicates = []

    for member in members_data:
        memberid = member.get("memberid")
        if memberid in seen_ids:
            duplicates.append(memberid)
        else:
            seen_ids.add(memberid)

    return duplicates


def load_and_validate_yaml(yaml_path: Path) -> list[MemberInDB]:
    """Load YAML file and validate each member with Pydantic.

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
            logger.error("YAML file not found", path=str(yaml_path))
            raise FileNotFoundError(f"YAML file not found: {yaml_path}")

        # Load YAML
        try:
            with yaml_path.open("r", encoding="utf-8") as f:
                data: Any = yaml.safe_load(f)
            logger.info("YAML file loaded successfully", path=str(yaml_path))
        except yaml.YAMLError as e:
            logger.error("Failed to parse YAML file", error=str(e), path=str(yaml_path))
            raise FileLoaderError("Failed to parse YAML file") from e

        # Validate structure
        if not isinstance(data, dict) or "members" not in data:
            logger.error(
                "YAML structure invalid: missing 'members' key", path=str(yaml_path)
            )
            raise ValueError("YAML must contain 'members' key")

        members_list = data["members"]
        if not isinstance(members_list, list):
            logger.error(
                "YAML structure invalid: 'members' is not a list", path=str(yaml_path)
            )
            raise TypeError("'members' must be a list")

        # Check for duplicates BEFORE Pydantic validation
        duplicates = check_duplicate_memberids(members_list)
        if duplicates:
            logger.error(
                "Duplicate memberids found", duplicates=duplicates, path=str(yaml_path)
            )
            raise ValueError(f"Duplicate memberids found: {duplicates}")

        # Validate each member with Pydantic
        validated_members: list[MemberInDB] = []
        for i, item in enumerate(members_list):
            memberid = item.get("memberid", "<unknown>")
            try:
                validated_member = MemberInDB(**item)
                validated_members.append(validated_member)
                logger.info(
                    "Member validation succeeded",
                    index=i,
                    memberid=memberid,
                )
            except ValidationError as e:
                logger.error(
                    "Member validation failed",
                    index=i,
                    memberid=memberid,
                    item=item,
                    error=str(e),
                )
                raise ValueError(
                    f"Member validation failed at index {i} (memberid={memberid}): {e}"
                ) from e

        if not validated_members:
            logger.warning("No valid members found in YAML file", path=str(yaml_path))
        else:
            logger.info(
                "Successfully loaded and validated members",
                count=len(validated_members),
                path=str(yaml_path),
            )
        return validated_members
