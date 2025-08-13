"""Member Repository.

Repository pattern for member data management:
- Constructor injection with optional file path
- Delegates loading tasks to pure functions in srv_memberdata
- Public interface for data access
- Error handling with fallback behavior
- Integration with FileWatcher via reload callback
"""

from pathlib import Path

from src.domain.module.sch_module import ModuleInDB
from src.mlogg import logger
from src.service.dto.srv_dtoloader import GenericYamlLoader


class ModuleRepository:
    """Repository for module data with fallback behavior and clean interface."""

    def __init__(self, file_path: Path | str | None = None):
        """Initialize ModuleRepository with optional file path.

        Args:
            file_path: Path to modules.yaml file. If None, uses default data/modules.yaml
        """
        if file_path is None:
            file_path = Path("data/modules.yaml")

        self.file_path = Path(file_path)

        self.loader = GenericYamlLoader("modules", "moduleid", ModuleInDB, logger)
        self._modules: list[ModuleInDB] = []
        self._modules_dict: dict[str, ModuleInDB] = {}

        logger.info("Initializing ModuleRepository", path=self.file_path)
        self.reload()

    def _load_data_from_file(self) -> list[ModuleInDB]:
        """Load data using GenericYamlLoader.

        Returns:
            List of validated ModuleInDB objects or empty list if file is empty.

        Raises:
            FileNotFoundError: If YAML file doesn't exist
            ValueError: If YAML structure is invalid or duplicates found
            ValidationError: If Pydantic validation fails
        """
        return self.loader.load_and_validate(self.file_path)

    def reload(self) -> None:
        """Reload all data from file and update internal state.

        Uses fallback behavior - if reload fails, keeps existing data and logs error.
        This ensures the repository remains functional even if file becomes temporarily invalid.
        """
        logger.info("Starting ModuleRepository reload")
        try:
            new_modules = self._load_data_from_file()

            # Update both list and dict storage
            self._modules = new_modules
            self._modules_dict = {m.moduleid: m for m in new_modules}

            logger.info(
                "ModuleRepository reload completed successfully", count=len(new_modules)
            )

        except FileNotFoundError as e:
            # Only fallback if we already have data loaded, else propagate
            if not self._modules:
                logger.error(
                    "Module data file not found during initial load",
                    error=str(e),
                    path=str(self.file_path),
                )
                raise
            logger.error(
                "Failed to reload module data, keeping existing data",
                error=str(e),
                current_count=len(self._modules),
            )
        except Exception as e:
            # Fallback behavior - keep existing data on reload failure
            logger.error(
                "Failed to reload module data, keeping existing data",
                error=str(e),
                current_count=len(self._modules),
            )
            # Don't re-raise - this allows the repository to continue functioning

    def get_module_by_id(self, moduleid: str) -> ModuleInDB | None:
        """Get module by ID with O(1) lookup."""
        module = self._modules_dict.get(moduleid)
        if module:
            logger.debug("Module found", moduleid=moduleid)
        else:
            logger.debug("Module not found", moduleid=moduleid)
        return module

    def get_all_modules(self) -> list[ModuleInDB]:
        """Get all modules as a copy of the internal list."""
        return self._modules.copy()

    def get_module_count(self) -> int:
        """Get total number of modules."""
        return len(self._modules)

    def is_module_active(self, moduleid: str) -> bool:
        """Quick check if module exists and is active."""
        module = self.get_module_by_id(moduleid)
        return module is not None and module.is_active

    def get_module_ids(self) -> list[str]:
        """Get all module IDs."""
        return list(self._modules_dict.keys())

    def get_module_by_provider(self, provider: str) -> list[ModuleInDB]:
        """Get all modules by provider."""
        return [module for module in self._modules if module.provider == provider]

    def has_module(self, moduleid: str) -> bool:
        """Check if module exists."""
        return moduleid in self._modules_dict

    def clear_data(self) -> None:
        """Clear all stored data (useful for testing)."""
        self._modules.clear()
        self._modules_dict.clear()
        logger.info("Module data cleared from repository")
