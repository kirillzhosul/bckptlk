"""
    CLI runner
"""

from logging import DEBUG, basicConfig, getLogger

from config import read_config
from runner import run_strategy

basicConfig(level=DEBUG, format="[%(asctime)s] %(levelname)s:%(name)s - %(message)s")
logger = getLogger(__name__)


def main() -> None:
    config = read_config()
    size = 0
    for target in config.targets:
        if config.verbose:
            logger.info(
                f"Backuping target {target.id} with strategy: {target.strategy}"
            )
        size += run_strategy(target, config)

    if config.verbose:
        logger.info(f"Finished all targets with overall size {size} bytes!")


if __name__ == "__main__":
    main()
