from pathlib import Path
from typing import Any

from src.config import get_settings
from src.domain.member.rep_member import MemberRepository
from src.domain.module.rep_module import ModuleRepository
from src.mlogg import logger
from src.service.watcher.srv_watcher import FileWatcher


class DataService:
    """Service to manage data repositories and file watchers.

    Easily extensible for new repositories and watchers.
    """

    def __init__(self) -> None:
        self.data_path = Path(get_settings().data_path)
        self.repos: dict[str, Any] = {}
        self.watchers: dict[str, FileWatcher] = {}
        self._init_repositories()
        self._init_watchers()

    def _init_repositories(self) -> None:
        """Initialize all repositories."""
        self.repos["member"] = MemberRepository(self.data_path / "members.yaml")
        logger.info("MemberRepository initialized")
        self.repos["module"] = ModuleRepository(self.data_path / "modules.yaml")
        logger.info("ModuleRepository initialized")
        # Add more repositories here as needed

    def _init_watchers(self) -> None:
        """Initialize all file watchers."""
        self.watchers["member"] = FileWatcher(
            self.data_path / "members.yaml", self.repos["member"].reload
        )
        logger.info(
            "Member FileWatcher initialized", path=str(self.data_path / "members.yaml")
        )
        self.watchers["module"] = FileWatcher(
            self.data_path / "modules.yaml", self.repos["module"].reload
        )
        logger.info(
            "Module FileWatcher initialized", path=str(self.data_path / "modules.yaml")
        )
        # Add more watchers here as needed

    def start(self) -> None:
        """Start all watchers."""
        for name, watcher in self.watchers.items():
            try:
                watcher.start()
                logger.info(f"{name.capitalize()} watcher started")
            except Exception as e:
                logger.error(f"Failed to start {name} watcher", error=str(e))

    def stop(self) -> None:
        """Stop all watchers."""
        for name, watcher in self.watchers.items():
            try:
                watcher.stop()
                logger.info(f"{name.capitalize()} watcher stopped")
            except Exception as e:
                logger.error(f"Failed to stop {name} watcher", error=str(e))

    @property
    def member_repo(self) -> MemberRepository:
        return self.repos["member"]

    @property
    def module_repo(self) -> ModuleRepository:
        return self.repos["module"]
