import datetime
import os
import pathlib
import shutil
import tarfile
import uuid

from config import BackupStrategy, Config, ConfigTarget


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
    path = pathlib.Path(
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
    return path


def get_size(path="."):
    t = 0
    for p, _, fn in os.walk(path):
        for f in fn:
            fp = os.path.join(p, f)

            if not os.path.islink(fp):
                t += os.path.getsize(fp)
    return t


def as_tar(target: ConfigTarget, backup_to: pathlib.Path) -> int:
    if target.overwrite and os.path.exists(backup_to):
        os.remove(backup_to)
    with tarfile.open(backup_to, "w:gz") as tar:
        tar.add(target.path_from, arcname=os.path.basename(backup_to))
    return os.path.getsize(backup_to)


def as_copy(config: Config, target: ConfigTarget, backup_to: pathlib.Path) -> int:
    try:
        shutil.copytree(target.path_from, backup_to, dirs_exist_ok=target.overwrite)
    except FileExistsError:
        if config.verbose:
            print("[skipped due to exists and no overwrite enabled]")
        return 0
    return get_size(backup_to)


def run_strategy(target: ConfigTarget, config: Config) -> None:
    backup_to = _format_path_with_name(target)
    _prepare(target)
    _try_clean(config, target)
    if target.strategy == BackupStrategy.COPY:
        size = as_copy(config, target, backup_to)
    if target.strategy == BackupStrategy.TAR:
        size = as_tar(target, backup_to)
    if config.verbose:
        print("Created new backup with size", size, "bytes!")
