from pathlib import Path

from config import get_settings
from mlogg import logger
from src.domain.member.rep_member import MemberRepository
from src.service.watcher.srv_watcher import FileWatcher


class DataService:
    """Service to manage data repositories and file watchers."""

    def __init__(self) -> None:
        data_path = Path(get_settings().data_path)
        # Member repository
        self.member_repo = MemberRepository(data_path / "members.yaml")
        logger.info("Initializing DataService for members")
        self.member_watcher = FileWatcher(
            data_path / "members.yaml", self.member_repo.reload
        )
        logger.info(
            "Member watcher initialized", path=self.member_watcher._path_to_watch
        )

        # ======================
        # TODO: Module repository
        # Prepare for future module repository and watcher
        # self.module_repo: ModuleRepository | None = None
        # self.module_watcher: FileWatcher | None = None
        # Uncomment and implement when ready:
        # self.module_repo = ModuleRepository(data_path / "modules.yaml")
        # self.module_watcher = FileWatcher(data_path / "modules.yaml", self.module_repo.reload)

    def start(self) -> None:
        """Start all watchers."""
        try:
            self.member_watcher.start()
            logger.info("Member watcher started")
        except Exception as e:
            logger.error("Failed to start member watcher", error=str(e))
        # Uncomment when module watcher is ready
        # try:
        #     self.module_watcher.start()
        #     logger.info("Module watcher started")
        # except Exception as e:
        #     logger.error("Failed to start module watcher", error=str(e))

    def stop(self) -> None:
        """Stop all watchers."""
        try:
            self.member_watcher.stop()
            logger.info("Member watcher stopped")
        except Exception as e:
            logger.error("Failed to stop member watcher", error=str(e))
        # Uncomment when module watcher is ready
        # try:
        #     self.module_watcher.stop()
        #     logger.info("Module watcher stopped")
        # except Exception as e:
        #     logger.error("Failed to stop module watcher", error=str(e))
