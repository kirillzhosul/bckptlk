"""
    Base type for all strategies
"""
from abc import ABC, abstractmethod
from pathlib import Path

from config import Config, ConfigTarget


class BaseStrategy(ABC):
    """
    Base abstract class for strategies
    """

    config: Config
    target: ConfigTarget
    path: Path

    def __init__(self, config: Config, target: ConfigTarget, path: Path):
        self.config = config
        self.target = target
        self.path = path

    @abstractmethod
    def execute(self) -> int:
        """
        Run strategy and return size of total backup size
        """
        ...
