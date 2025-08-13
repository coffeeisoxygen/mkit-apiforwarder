from src.domain.digipos.rep_digipos import DigiposProductRepository
from src.domain.module.rep_module import ModuleRepository
from src.domain.transaction.sch_transaction import DigiposTrxModel
from src.mlogg import logger


class DigiposQueryBuilder:
    def __init__(
        self, product_repo: DigiposProductRepository, module_repo: ModuleRepository
    ):
        self.product_repo = product_repo
        self.module_repo = module_repo

    def _map_param(self, value, module, request):
        if isinstance(value, str):
            if value.startswith("modules."):
                return getattr(module, value.split(".", 1)[1])
            elif value.startswith("request."):
                return getattr(request, value.split(".", 1)[1])
            else:
                return value
        else:
            return value

    def build(self, trx: DigiposTrxModel) -> dict:
        product = self.product_repo.get_product_by_id(trx.product)
        module = self.module_repo.get_module_by_id(trx.moduleid)
        params = {}

        logger.info(
            f"Building query for trx_id={getattr(trx, 'id', None)}, product_id={getattr(trx, 'product', None)}, module_id={getattr(trx, 'moduleid', None)}"
        )

        # Helper to process params
        def process_params(param_dict):
            for k, v in param_dict.items():
                params[k] = self._map_param(v, module, trx)

        if product:
            if (
                hasattr(product, "required_params")
                and isinstance(product.required_params, dict)
                and product.required_params
            ):
                process_params(product.required_params)
            if (
                hasattr(product, "optional_params")
                and isinstance(product.optional_params, dict)
                and product.optional_params
            ):
                process_params(product.optional_params)

        url = (
            f"{module.base_url}{product.api_path}"
            if module
            and hasattr(module, "base_url")
            and product
            and hasattr(product, "api_path")
            else ""
        )
        method = getattr(product, "method", None) if product else None
        result = {"method": method, "url": url, "params": params}
        logger.info(f"Built query: {result}")
        return result
