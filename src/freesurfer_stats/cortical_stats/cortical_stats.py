import datetime
import typing
from pathlib import Path
from typing import TextIO
from typing import Union

from freesurfer_stats.freesurfer_stats import FreesurferStats


class CorticalStats(FreesurferStats):
    # Headers structure
    HEADERS_END = "Measure"

    def __init__(self, stats_file: Union[Path, str]) -> None:
        super().__init__(stats_file)

    # def _read_headers(self, stream: TextIO) -> None:
    #     headers = {}
    #     while True:
    #         line = self._read_header_line(stream)
    #         if line.startswith(self.HEADERS_END):
    #             break
    #         if line:
    #             attr_name, attr_value_str = line.split(" ", maxsplit=1)
    #             attr_value_str = attr_value_str.lstrip()
    #             if attr_name in ["cvs_version", "mrisurf.c-cvs_version"]:
    #                 attr_value = typing.cast(
    #                     typing.Union[str, datetime.datetime],
    #                     attr_value_str.strip("$").rstrip(),
    #                 )
    #             elif attr_name == "CreationTime":
    #                 attr_dt = datetime.datetime.strptime(
    #                     attr_value_str, "%Y/%m/%d-%H:%M:%S-%Z"
    #                 )
    #                 if attr_dt.tzinfo is None:
    #                     assert attr_value_str.endswith("-GMT")
    #                     attr_dt = attr_dt.replace(tzinfo=datetime.timezone.utc)
    #                 attr_value = attr_dt
    #             elif attr_name == "AnnotationFileTimeStamp":
    #                 attr_value = datetime.datetime.strptime(
    #                     attr_value_str, "%Y/%m/%d %H:%M:%S"
    #                 )
    #             else:
    #                 attr_value = attr_value_str
    #             headers[attr_name] = attr_value
    #     return headers
