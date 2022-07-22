from freesurfer_statistics.utils import parse_date

SpecialHeaders = dict(
    GCATimeStamp={
        "func": parse_date,
        "kwargs": {"format": "%Y/%m/%d %H:%M:%S"},
    },
    SegVolFileTimeStamp={
        "func": parse_date,
        "kwargs": {"format": "%Y/%m/%d %H:%M:%S"},
    },
    Only={"key": "comments"},
)
