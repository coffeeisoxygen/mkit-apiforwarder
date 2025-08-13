from typing import Annotated

from fastapi import APIRouter, Query

from src.dependencies.dep_data import (
    DepDigiposRepo,
    DepDigiProductAuthService,
    DepMemberAuthService,
    DepModuleAuthService,
)
from src.domain.transaction.sch_transaction import DigiposTrxModel

router = APIRouter()


@router.get("/digipos/products")
def get_digipos_products(digipos_repo: DepDigiposRepo):
    products = [p.model_dump() for p in digipos_repo.get_all_products()]
    return {"products": products}


@router.get("/digipos/products/{product_id}")
def get_digipos_product_by_id(product_id: str, digipos_repo: DepDigiposRepo):
    product = digipos_repo.get_product_by_id(product_id)
    if not product:
        return {"error": "Product not found"}
    return product.model_dump()


@router.get("/digipos/products/{product_id}/active")
def is_digipos_product_active(product_id: str, digipos_repo: DepDigiposRepo):
    is_active = digipos_repo.is_product_active(product_id)
    return {"productid": product_id, "is_active": is_active}


@router.get("/digipos/trx")
def digipos_trx(
    trx_query: Annotated[DigiposTrxModel, Query()],
    product_auth_service: DepDigiProductAuthService,
    module_auth_service: DepModuleAuthService,
    member_auth_service: DepMemberAuthService,
):
    member_obj = member_auth_service.authenticate_and_verify(trx_query)
    product_obj = product_auth_service.authenticate_and_check(
        trx_query.product, "digipos"
    )
    module_obj = module_auth_service.authenticate_and_check_provider(
        trx_query.moduleid, "digipos"
    )
    return {
        "message": "Product, module, and member are valid and active for provider digipos",
        "product": product_obj.model_dump(),
        "module": module_obj.model_dump(),
        "member": member_obj.model_dump(),
    }
