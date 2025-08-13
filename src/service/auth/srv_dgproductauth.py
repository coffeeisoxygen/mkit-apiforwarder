from typing import Protocol, runtime_checkable

from src.custom.cst_exceptions import ProductAuthError, ProductNotFoundError
from src.domain.digipos.sch_digipos import DGProductInDB
from src.mlogg import logger


@runtime_checkable
class DigiposProductProvider(Protocol):
    def get_product_by_id(self, productid: str) -> DGProductInDB | None: ...


class DigiposProductAuthService:
    """Layanan otentikasi produk Digipos: cek provider, status aktif, dan modul."""

    def __init__(self, product_manager: DigiposProductProvider):
        self.product_manager = product_manager

    def authenticate_and_check(self, productid: str, provider: str) -> DGProductInDB:
        """Autentikasi produk, cek provider, status aktif, dan modul."""
        with logger.contextualize(productid=productid, op="digipos_product_auth"):
            logger.info("Mulai autentikasi produk Digipos")

            product_db = self._get_active_product(productid)

            if product_db.provider != provider:
                logger.error(f"Provider mismatch: {product_db.provider} != {provider}")
                raise ProductAuthError(
                    "Provider tidak sesuai",
                    context={"productid": productid, "provider": provider},
                )

            if not product_db.list_modules or len(product_db.list_modules) == 0:
                logger.error("Produk tidak memiliki modul aktif")
                raise ProductAuthError(
                    "Produk tidak memiliki modul aktif",
                    context={"productid": productid},
                )

            logger.info("Autentikasi produk Digipos sukses")
            return product_db

    def _get_active_product(self, productid: str) -> DGProductInDB:
        """Ambil produk dari DB + cek aktif."""
        product = self.product_manager.get_product_by_id(productid)
        if not product:
            raise ProductNotFoundError(
                f"Product ID '{productid}' not found", context={"productid": productid}
            )
        if not product.is_active:
            raise ProductAuthError(
                "Produk tidak aktif", context={"productid": productid}
            )
        return product
