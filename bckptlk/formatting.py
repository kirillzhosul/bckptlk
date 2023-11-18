"""
    Formmatting target names
"""
import datetime
import pathlib
import uuid

from config import ConfigTarget


def format_target_with_variables(target: ConfigTarget) -> pathlib.Path:
    """
    Format target path with variables for formatter.
    """
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
