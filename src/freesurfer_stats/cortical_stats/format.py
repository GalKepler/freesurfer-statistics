from datetime import datetime
from enum import Enum


def parse_date(date_str: str) -> datetime:
    """
    Parse a date string from a Freesurfer .stats file.
    """
    return datetime.strptime(date_str, "%Y/%m/%d-%H:%M:%S-%Z")


class SpecialHeaders(Enum):
    Table = "title"
    CreationTime = parse_date
    AnnotationFileTimeStamp = parse_date
