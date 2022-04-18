from datetime import datetime
from enum import Enum


def parse_date(date_str: str, format: str) -> datetime:
    """
    Parse a date string from a Freesurfer .stats file.
    """
    return datetime.strptime(date_str, format)


SpecialHeaders = dict(
    Table={"func": "title"},
    CreationTime={
        "func": parse_date,
        "kwargs": {"format": "%Y/%m/%d-%H:%M:%S-%Z"},
    },
    AnnotationFileTimeStamp={
        "func": parse_date,
        "kwargs": {"format": "%Y/%m/%d %H:%M:%S"},
    },
)
