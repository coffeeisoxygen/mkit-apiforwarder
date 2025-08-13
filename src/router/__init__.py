from src.router.rtr_debug import router as member_router
from src.router.rtr_digipos import router as digipos_router


def register_routes(app):  # noqa: ANN001
    """Register application routes.

    This function registers all application routes with the given FastAPI app instance.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    app.include_router(member_router, tags=["debug"])
    app.include_router(digipos_router, tags=["digipos"])
