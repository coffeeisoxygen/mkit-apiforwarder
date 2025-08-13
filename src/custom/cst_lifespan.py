from contextlib import asynccontextmanager

from src.mlogg import logger
from src.service.srv_data import DataService

data_service = DataService()


@asynccontextmanager
async def app_lifespan(app):  # noqa: ANN001, D103, RUF029
    try:
        data_service.start()
    except Exception as e:
        logger.error(f"Error starting DataService: {e}")
    app.state.data_service = data_service  # bisa akses member_repo dari sini
    yield
    try:
        data_service.stop()
    except Exception as e:
        logger.error(f"Error stopping DataService: {e}")
