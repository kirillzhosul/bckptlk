import datetime
import os
import pathlib
import shutil
import tarfile
import uuid

from config import BackupStrategy, ConfigTarget


def as_tar(target: ConfigTarget, backup_to: str) -> None:
    if target.overwrite and os.path.exists(backup_to):
        os.remove(backup_to)
    with tarfile.open(backup_to, "w:gz") as tar:
        tar.add(target.path_from, arcname=os.path.basename(backup_to))


def as_copy(target: ConfigTarget, backup_to: str) -> None:
    try:
        shutil.copytree(target.path_from, backup_to, dirs_exist_ok=target.overwrite)
    except FileExistsError:
        print("[skipped due to exists and no overwrite enabled]")


def run_strategy(target) -> None:
    now = datetime.datetime.now()
    backup_to = target.path_to.format(
        **{"uuid": uuid.uuid4(), "m": now.month, "d": now.day, "y": now.year}
    )
    os.makedirs(pathlib.Path(backup_to).parent, exist_ok=True)
    if target.strategy == BackupStrategy.COPY:
        as_copy(target, backup_to)
    if target.strategy == BackupStrategy.TAR:
        as_tar(target, backup_to)
