"""
    Base type for all strategies
"""
import os
import pathlib
import shutil
from abc import ABC, abstractmethod
from logging import Logger, getLogger
from pathlib import Path

from config import Config, ConfigTarget


class BaseStrategy(ABC):
    """
    Base abstract class for strategies
    """

    config: Config
    target: ConfigTarget
    path: Path
    logger: Logger

    def __init__(self, config: Config, target: ConfigTarget, path: Path) -> None:
        self.config = config
        self.target = target
        self.path = path
        self.logger = getLogger(f"strategy_{target.id}")

    @abstractmethod
    def execute(self) -> int:
        """
        Run strategy and return size of total backup size
        """
        self.prepare()
        self.initial_cleanup()

    def prepare(self) -> None:
        os.makedirs(pathlib.Path(self.target.path_to), exist_ok=True)

    def initial_cleanup(self) -> None:
        if self.target.clean_limit == 0:
            return
        content = os.listdir(self.target.path_to)
        if len(content) < self.target.clean_limit:
            return
        if self.config.verbose:
            self.logger.info("Removing old backups...")
        legacy_content = content[: 1 + len(content) - self.target.clean_limit]
        for raw_path in legacy_content:
            path = pathlib.Path(self.target.path_to, raw_path)
            (os.remove if os.path.isfile(path) else shutil.rmtree)(path)
