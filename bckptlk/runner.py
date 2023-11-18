"""
    Runner of the backup
"""
from logging import getLogger

from config import Config, ConfigTarget
from formatting import format_target_with_variables
from strategies.factory import StrategyFactory

logger = getLogger(__name__)


def run_strategy(target: ConfigTarget, config: Config) -> int:
    """
    Runs given strategy from config
    """
    backup_to = format_target_with_variables(target)
    strategy = StrategyFactory.build(target.strategy, config, target, backup_to)
    size = strategy.execute()

    if config.verbose:
        logger.info(f"Created new backup with size {size} bytes!")

    return size
