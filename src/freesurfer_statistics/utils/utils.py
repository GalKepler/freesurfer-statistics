from datetime import datetime
from pathlib import Path
from typing import Union


def parse_date(date_str: str, format: str) -> datetime:
    """
    Parse a date string from a Freesurfer .stats file.
    """
    return datetime.strptime(date_str, format)


UNITS_CONVERTER = {"NA": str, "unitless": float, "mm": float, "MR": float}


def validate_stats_file(stats_file: Union[Path, str]) -> Path:
    """
    Validate the stats file as an existing file Freesurfer .stats file.

    Parameters
    ----------
    stats_file : Union[Path,str]
        The path to the Freesurfer .stats file.

    Raises
    ------
    FileNotFoundError
        If the stats file does not exist.

    Returns
    -------
    Path
        The path to the stats file.
    """
    stats_file = Path(stats_file)
    if not stats_file.exists():
        raise FileNotFoundError(f"{stats_file} does not exist")
    if stats_file.suffix != ".stats":
        raise ValueError(f"{stats_file} is not a Freesurfer .stats file")
    return stats_file
