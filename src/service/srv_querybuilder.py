import uuid

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
        """Map value based on prefix or return literal."""
        if isinstance(value, str):
            if value.startswith("modules."):
                return getattr(module, value.split(".", 1)[1])
            elif value.startswith("request."):
                attr = value.split(".", 1)[1]
                # generate trxid if requested and None
                if attr == "trxid" and getattr(request, "trxid", None) is None:
                    return str(uuid.uuid4())
                return getattr(request, attr)
            else:
                return value
        else:
            return value

    def build(self, trx: DigiposTrxModel) -> dict:
        product = self.product_repo.get_product_by_id(trx.product)
        module = self.module_repo.get_module_by_id(trx.moduleid)
        params = {}

        logger.info(
            f"Building query for trx_id={getattr(trx, 'trxid', None)}, "
            f"product_id={getattr(trx, 'product', None)}, "
            f"module_id={getattr(trx, 'moduleid', None)}"
        )

        def process_params(param_dict):
            for k, v in param_dict.items():
                mapped = self._map_param(v, module, trx)
                if mapped is not None:
                    params[k] = mapped

        if product:
            if hasattr(product, "required_params") and product.required_params:
                # convert required_params (DGReqParams) ke dict
                process_params(product.required_params.model_dump())
            if hasattr(product, "optional_params") and product.optional_params:
                process_params(product.optional_params)

        url = f"{module.base_url}{product.api_path}" if module and product else ""
        method = getattr(product, "method", None) if product else None

        result = {"method": method, "url": url, "params": params}
        logger.info(f"Built query: {result}")
        return result
