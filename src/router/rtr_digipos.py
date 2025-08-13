"""Router for Digipos product-related operations/ all services."""

from fastapi import APIRouter, Query

from src.dependencies.dep_data import (
    DepDigiposRepo,
    DepDigiProductAuthService,
    DepMemberAuthService,
    DepModuleAuthService,
)
from src.service.auth.srv_memberauth import MemberTrxRequestModel

router = APIRouter()


@router.get("/digipos/products")
def get_digipos_products(digipos_repo: DepDigiposRepo):
    """Get all Digipos products."""
    products = [p.model_dump() for p in digipos_repo.get_all_products()]
    return {"products": products}


@router.get("/digipos/products/{product_id}")
def get_digipos_product_by_id(product_id: str, digipos_repo: DepDigiposRepo):
    """Get Digipos product by ID."""
    product = digipos_repo.get_product_by_id(product_id)
    if not product:
        return {"error": "Product not found"}
    return product.model_dump()


@router.get("/digipos/products/{product_id}/active")
def is_digipos_product_active(product_id: str, digipos_repo: DepDigiposRepo):
    """Check if Digipos product is active."""
    is_active = digipos_repo.is_product_active(product_id)
    return {"productid": product_id, "is_active": is_active}


@router.get("/digipos/trx")
def digipos_trx(
    product_auth_service: DepDigiProductAuthService,
    module_auth_service: DepModuleAuthService,
    member_auth_service: DepMemberAuthService,
    productid: str = Query(..., description="Product ID"),
    moduleid: str = Query(..., description="Module ID"),
    memberid: str = Query(..., description="Member ID"),
    dest: str = Query(..., description="Destination"),
    product: str = Query(..., description="Product"),
    pin: str | None = Query(None, description="PIN"),
    password: str | None = Query(None, description="Password"),
    sign: str | None = Query(None, description="Signature"),
    refid: str | None = Query(None, description="Reference ID"),
):
    """Validate active Digipos product, module, and member for provider digipos."""
    product_obj = product_auth_service.authenticate_and_check(productid, "digipos")
    module_obj = module_auth_service.authenticate_and_check_provider(
        moduleid, "digipos"
    )
    member_req = MemberTrxRequestModel(
        memberid=memberid,
        dest=dest,
        product=product,
        pin=pin,
        password=password,
        sign=sign,
        refid=refid,
    )
    member_obj = member_auth_service.authenticate_and_verify(member_req)
    return {
        "message": "Product, module, and member are valid and active for provider digipos",
        "product": product_obj.model_dump(),
        "module": module_obj.model_dump(),
        "member": member_obj.model_dump(),
    }
