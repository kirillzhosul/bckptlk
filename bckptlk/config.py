import json
import os
import pathlib
from dataclasses import dataclass, field
from logging import getLogger

from strategies.types import StrategyType

CONFIG_PATH = os.getenv("BCKPTLK_CONFIG_PATH", "./config.json")

logger = getLogger(__name__)


@dataclass
class ConfigTarget:
    id: int
    path_from: pathlib.Path
    name: str
    path_to: pathlib.Path
    strategy: StrategyType = field(default=StrategyType.COPY)
    clean_limit: int = 0
    overwrite: bool = False
    additional: dict = field(default=dict)

    def __post_init__(self):
        self.strategy = StrategyType(self.strategy)
        self.path_to = pathlib.Path(self.path_to)
        self.path_from = pathlib.Path(self.path_from)


@dataclass
class Config:
    targets: list[ConfigTarget]
    verbose: bool = True


def read_config(path: str = CONFIG_PATH) -> Config:
    try:
        with open(path, "r") as f:
            raw = json.load(f)
            config = Config(
                verbose=raw.get("verbose", True),
                targets=[
                    ConfigTarget(id=id_, **kwargs)
                    for id_, kwargs in enumerate(raw.get("targets", []))
                ],
            )
    except (json.JSONDecodeError, OSError, TypeError) as e:
        logger.error("Unable to load/decode config!", exc_info=e)
        exit(1)
    return config
