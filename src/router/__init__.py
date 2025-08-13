from src.router.rtr_member import router as member_router


def register_routes(app):
    app.include_router(member_router)
