"""Router for Digipos product-related operations/ all services."""

from fastapi import APIRouter, Query

from src.dependencies.dep_data import (
    DepDigiposRepo,
    DepDigiProductAuthService,
    DepModuleAuthService,
)

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
    productid: str = Query(..., description="Product ID"),
    moduleid: str = Query(..., description="Module ID"),
):
    """Validate active Digipos product and module for provider digipos."""
    product = product_auth_service.authenticate_and_check(productid, "digipos")
    module = module_auth_service.authenticate_and_check_provider(moduleid, "digipos")
    return {
        "message": "Product and module are valid and active for provider digipos",
        "product": product.model_dump(),
        "module": module.model_dump(),
    }
