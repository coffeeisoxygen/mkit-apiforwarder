from pathlib import Path

from src.domain.digipos.sch_digipos import DGProductInDB  # pastikan model ini ada
from src.mlogg import logger
from src.service.srv_dtoloader import GenericYamlLoader


class DigiposProductRepository:
    """Repository for Digipos products data."""

    def __init__(self, file_path: Path | str | None = None):
        if file_path is None:
            file_path = Path("data/digipos.yaml")
        self.file_path = Path(file_path)
        self.loader = GenericYamlLoader("products", "productid", DGProductInDB, logger)
        self._products: list[DGProductInDB] = []
        self._products_dict: dict[str, DGProductInDB] = {}
        logger.info("Initializing DigiposProductRepository", path=self.file_path)
        self.reload()

    def _load_data_from_file(self) -> list[DGProductInDB]:
        return self.loader.load_and_validate(self.file_path)

    def reload(self) -> None:
        logger.info("Starting DigiposProductRepository reload")
        try:
            products = self._load_data_from_file()
            self._products = products
            self._products_dict = {p.productid: p for p in products}
            logger.info(
                "DigiposProductRepository reload completed successfully",
                count=len(products),
            )
        except Exception as e:
            logger.error("DigiposProductRepository reload failed", error=str(e))
            self._products = []
            self._products_dict = {}

    def get_product_by_id(self, productid: str) -> DGProductInDB | None:
        return self._products_dict.get(productid)

    def get_all_products(self) -> list[DGProductInDB]:
        return self._products

    def get_product_count(self) -> int:
        return len(self._products)

    def is_product_active(self, productid: str) -> bool:
        product = self.get_product_by_id(productid)
        return bool(product and getattr(product, "is_active", False))

    def get_product_ids(self) -> list[str]:
        return list(self._products_dict.keys())

    def has_product(self, productid: str) -> bool:
        return productid in self._products_dict

    def clear_data(self) -> None:
        self._products = []
