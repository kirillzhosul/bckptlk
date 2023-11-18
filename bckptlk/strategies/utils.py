"""
    Some utils for working with directories and etc
"""

from os import walk
from os.path import getsize, islink, join


def get_directory_size(path=".") -> int:
    """
    Returns directory size in bytes
    """
    t = 0
    for p, _, fn in walk(path):
        for f in fn:
            fp = join(p, f)

            if not islink(fp):
                t += getsize(fp)
    return t
