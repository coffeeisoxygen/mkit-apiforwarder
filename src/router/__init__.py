from src.router.rtr_member import router as member_router


def register_routes(app):  # noqa: ANN001
    """Register application routes.

    This function registers all application routes with the given FastAPI app instance.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    app.include_router(member_router, prefix="/members", tags=["members"])
