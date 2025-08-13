"""Application lifespan event handler for FastAPI.

Setup loguru logging and handle startup/shutdown events using lifespan context.
"""

import pathlib
from contextlib import asynccontextmanager

from mlogg import init_logging
from mlogg import logger as lifespan_logger
from src.config import DEVELOPMENT_ENV_FILE, get_settings
from src.domain.member.rep_member import MemberRepository
from src.service.watcher.srv_watcher import FileWatcher

settings = get_settings(_env_file=DEVELOPMENT_ENV_FILE)
init_logging(settings.app_env)
# Get paths from settings
data_path = get_settings().data_path
member_file_path: pathlib.Path = data_path / "members.yaml"

# initialize repository
member_repo = MemberRepository(file_path=member_file_path)

# Create watchers with proper file paths and callbacks
member_watcher = FileWatcher(file_path=member_file_path, callback=member_repo.reload)

settings = get_settings()
lifespan_logger = lifespan_logger.bind(app_env=settings.app_env)


@asynccontextmanager
async def app_lifespan(app):  # noqa: ANN001
    """Lifespan context for FastAPI app: setup logging and log events."""
    lifespan_logger.info("FastAPI application startup initiated")
    app.state.member_repo = member_repo
    lifespan_logger.info("Member repository initialized and registered to app state")

    lifespan_logger.info("Starting file watchers for data monitoring")
    member_watcher.start()
    app.state.member_watcher = member_watcher
    lifespan_logger.info("All file watchers started and registered to app state")
    lifespan_logger.info("FastAPI application startup completed successfully")

    try:
        yield
    finally:
        lifespan_logger.info("FastAPI application shutdown initiated")
        lifespan_logger.info("Stopping file watchers")
        member_watcher.stop()
        lifespan_logger.info("File watchers cleanup completed")
        lifespan_logger.info("FastAPI application shutdown completed")
