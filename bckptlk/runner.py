import datetime
import os
import pathlib
import shutil
import uuid

from config import Config, ConfigTarget
from strategies.factory import StrategyFactory


def _try_clean(config: Config, target: ConfigTarget) -> None:
    if target.clean_limit == 0:
        return
    content = os.listdir(target.path_to)
    if len(content) < target.clean_limit:
        return
    if config.verbose:
        print("Removing old backups...")
    legacy_content = content[: 1 + len(content) - target.clean_limit]
    for raw_path in legacy_content:
        path = pathlib.Path(target.path_to, raw_path)
        (os.remove if os.path.isfile(path) else shutil.rmtree)(path)


def _prepare(target: ConfigTarget) -> None:
    os.makedirs(pathlib.Path(target.path_to), exist_ok=True)


def _format_path_with_name(target: ConfigTarget) -> pathlib.Path:
    now = datetime.datetime.now()
    return pathlib.Path(
        target.path_to,
        target.name.format(
            **{
                "uuid": uuid.uuid4(),
                "m": now.month,
                "d": now.day,
                "y": now.year,
                "H": now.hour,
                "M": now.minute,
                "S": now.second,
            }
        ),
    )


def run_strategy(target: ConfigTarget, config: Config) -> None:
    backup_to = _format_path_with_name(target)
    _prepare(target)
    _try_clean(config, target)
    strategy = StrategyFactory.build(target.strategy, config, target, backup_to)
    size = strategy.execute()

    if config.verbose:
        print("Created new backup with size", size, "bytes!")
