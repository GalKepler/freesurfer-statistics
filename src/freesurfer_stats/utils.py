from datetime import datetime


def parse_date(date_str: str, format: str) -> datetime:
    """
    Parse a date string from a Freesurfer .stats file.
    """
    return datetime.strptime(date_str, format)


UNITS_CONVERTER = {"NA": str, "unitless": float, "mm": float, "MR": float}
