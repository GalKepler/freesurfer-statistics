from freesurfer_stats.utils import parse_date


def add_header(value: str) -> str:
    """
    Add a header to the value.

    Parameters
    ----------
    value : str
        The value to add the header to.

    Returns
    -------
    str
        The value with the header added.
    """
    return "Table " + value


SpecialHeaders = dict(
    Table={"key": "title", "func": add_header},
    CreationTime={
        "func": parse_date,
        "kwargs": {"format": "%Y/%m/%d-%H:%M:%S-%Z"},
    },
    AnnotationFileTimeStamp={
        "func": parse_date,
        "kwargs": {"format": "%Y/%m/%d %H:%M:%S"},
    },
)
