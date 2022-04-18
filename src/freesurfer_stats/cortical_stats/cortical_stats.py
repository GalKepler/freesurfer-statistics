from enum import Enum
from pathlib import Path
from typing import Callable
from typing import Union

from freesurfer_stats.cortical_stats.format import SpecialHeaders
from freesurfer_stats.freesurfer_stats import FreesurferStats


class CorticalStats(FreesurferStats):
    #: Headers structure
    HEADERS_END = "Measure"

    #: Special headers
    SPECIAL_HEADERS = SpecialHeaders

    def __init__(self, stats_file: Union[Path, str]) -> None:
        super().__init__(stats_file)

    def _read_headers(self, special_headers: Enum = None) -> dict:
        """
        Parses the headers found in Freesurfer's .stats file.

        Returns
        -------
        dict
            A dictionary with headers' titles as keys and their
            corresponding parsed values.
        """
        special_headers = special_headers or self.SPECIAL_HEADERS
        headers = {}
        for line in self._get_headers():
            header, value = line.split(" ", maxsplit=1)
            if header in special_headers:
                parser = special_headers[header]
                func = parser["func"]
                if isinstance(func, Callable):
                    kwargs = parser.get("kwargs", {})
                    value = func(value, **kwargs)
                elif isinstance(func, str):
                    value = func
            headers[header] = value
        return headers

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
