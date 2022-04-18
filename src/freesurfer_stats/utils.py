from datetime import datetime


def parse_date(date_str: str, format: str) -> datetime:
    """
    Parse a date string from a Freesurfer .stats file.
    """
    return datetime.strptime(date_str, format)
