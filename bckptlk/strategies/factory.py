"""
    Factory for creating strategy
"""


from .base import BaseStrategy
from .copy import CopyStrategy
from .tar import TarStrategy
from .types import StrategyType


class StrategyFactory:
    """
    Builds strategy from args for you
    """

    # Mapping to strategy
    STRATEGIES: dict[StrategyType, type[BaseStrategy]] = {
        StrategyType.COPY: CopyStrategy,
        StrategyType.TAR: TarStrategy,
    }

    @staticmethod
    def build(strategy: StrategyType, config, target, path) -> BaseStrategy | None:
        """
        Return strategy or None if strategy does not exists
        """
        if cls := StrategyFactory.STRATEGIES.get(strategy, None):
            return cls(config=config, target=target, path=path)
