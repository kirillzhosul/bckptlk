import json
import os
from dataclasses import dataclass, field
from enum import Enum

CONFIG_PATH = os.getenv("BCKPTLK_CONFIG_PATH", "./config.json")


class BackupStrategy(Enum):
    COPY = "copy"
    TAR = "tar"


@dataclass
class ConfigTarget:
    id: int
    path_from: str
    path_to: str
    strategy: BackupStrategy = field(default=BackupStrategy.COPY)
    overwrite: bool = False

    def __post_init__(self):
        self.strategy = BackupStrategy(self.strategy)


@dataclass
class Config:
    targets: list[ConfigTarget]


def read_config(path: str = CONFIG_PATH) -> Config:
    try:
        with open(path, "r") as f:
            config = Config(
                targets=[
                    ConfigTarget(id=id_, **kwargs)
                    for id_, kwargs in enumerate(json.load(f).get("targets", []))
                ]
            )
    except (json.JSONDecodeError, FileNotFoundError, OSError, TypeError) as e:
        print("\tUnable to load/decode config!")
        print("\tError:", repr(e))
        exit(1)
    return config
