from typing import Protocol, runtime_checkable

from src.custom.cst_exceptions import (
    ModuleAuthError,
    ModuleNotFoundError,
)
from src.domain.module.sch_module import ModuleInDB
from src.mlogg import logger


@runtime_checkable
class ModuleProvider(Protocol):
    def get_module_by_id(self, moduleid: str) -> ModuleInDB | None: ...


class ModuleAuthService:
    """Layanan otentikasi module + cek provider."""

    def __init__(self, module_manager: ModuleProvider):
        self.module_manager = module_manager

    def authenticate_and_check_provider(
        self, moduleid: str, provider: str
    ) -> ModuleInDB:
        """Autentikasi module, cek status aktif, dan provider."""
        with logger.contextualize(moduleid=moduleid, op="module_auth"):
            logger.info("Mulai autentikasi module")

            module_db = self._get_active_module(moduleid)

            if module_db.provider != provider:
                logger.error(f"Provider mismatch: {module_db.provider} != {provider}")
                raise ModuleAuthError("Provider tidak sesuai")

            logger.info("Autentikasi module sukses")
            return module_db

    def _get_active_module(self, moduleid: str) -> ModuleInDB:
        """Ambil module dari DB + cek aktif."""
        module = self.module_manager.get_module_by_id(moduleid)
        if not module:
            raise ModuleNotFoundError(f"Module ID '{moduleid}' not found")
        if not module.is_active:
            raise ModuleAuthError("Module tidak aktif")
        return module
