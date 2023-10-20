"""
    COPY strategy implementation
"""
from shutil import copytree

from .base import BaseStrategy
from .utils import get_directory_size


class CopyStrategy(BaseStrategy):
    """
    COPY strategy implementation that copies file or directory to another one
    """

    def execute(self) -> int:
        """
        Creates copy and returns it size
        """
        try:
            copytree(
                self.target.path_from, self.path, dirs_exist_ok=self.target.overwrite
            )
        except FileExistsError:
            if self.config.verbose:
                print("Skipping target, as already exists and overwrite is disabled")
            return 0
        return get_directory_size(self.path)
