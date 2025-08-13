from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, Query

from src.dependencies.dep_data import (
    DepDigiposRepo,
    DepDigiProductAuthService,
    DepMemberAuthService,
    DepModuleAuthService,
    DepModuleRepo,
)
from src.domain.transaction.sch_transaction import DigiposTrxModel
from src.service.parser.digipos.parser_service import process_category_response
from src.service.srv_querybuilder import DigiposQueryBuilder

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


def get_digipos_query_builder(
    product_repo: DepDigiposRepo,
    module_repo: DepModuleRepo,
) -> DigiposQueryBuilder:
    return DigiposQueryBuilder(product_repo, module_repo)


@router.get("/digipos/trx")
async def digipos_trx(
    trx_query: Annotated[DigiposTrxModel, Query()],
    product_auth_service: DepDigiProductAuthService,
    module_auth_service: DepModuleAuthService,
    member_auth_service: DepMemberAuthService,
    query_builder: DigiposQueryBuilder = Depends(get_digipos_query_builder),
):
    member_obj = member_auth_service.authenticate_and_verify(trx_query)
    product_obj = product_auth_service.authenticate_and_check(
        trx_query.product, "digipos"
    )
    module_obj = module_auth_service.authenticate_and_check_provider(
        trx_query.moduleid, "digipos"
    )
    result = query_builder.build(trx_query)
    # 3. Kirim request ke target API (async)
    async with httpx.AsyncClient(timeout=module_obj.timeout) as client:
        if result["method"].upper() == "GET":
            resp = await client.get(result["url"], params=result["params"])
        else:  # POST / PUT bisa ditambah disini
            resp = await client.post(result["url"], json=result["params"])
    # Get category from query params (result["params"]) for parser
    category = result["params"].get("category")
    parsed = None
    if category:
        parsed = process_category_response(category, resp.text)
    return {
        "message": "Product, module, and member are valid and active for provider digipos",
        "query": result,
        "response": {
            "status_code": resp.status_code,
            "headers": dict(resp.headers),
            "body": resp.json(),
            "parsed": parsed,
        },
    }
