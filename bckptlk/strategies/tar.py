"""
    TAR strategy implementation
"""

import tarfile
from os import remove
from os.path import basename, exists, getsize

from .base import BaseStrategy


class TarStrategy(BaseStrategy):
    """
    TAR strategy implementation that makes backup as `tar` archive type file
    """

    def execute(self) -> int:
        """
        Creates TAR file and returns it size
        """

        super(TarStrategy, self).execute()

        # Remove legacy file if should overwrite
        if exists(self.path):
            if self.target.overwrite:
                remove(self.path)
            elif self.config.verbose:
                self.logger.info(
                    "Skipping target, as already exists and overwrite is disabled"
                )
                return -1

        compression = self.target.additional.get("compression", "gz")
        mode = f"w:{compression}"
        archname = basename(self.path)
        recursive = True
        if not exists(self.target.path_from):
            self.logger.warn(f"{self.target.path_from} does not exist, skipped!")
            return 0

        with tarfile.open(name=self.path, mode=mode) as tar:
            tar.add(self.target.path_from, arcname=archname, recursive=recursive)

        return getsize(self.path)
