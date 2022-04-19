"""Main module."""
import re
from pathlib import Path
from typing import Callable
from typing import Union

import pandas as pd

from freesurfer_stats.utils import UNITS_CONVERTER
from freesurfer_stats.utils import validate_stats_file


class FreesurferStats:
    STRUCTURE_MAP = {
        "lh": "left",
        "rh": "right",
        "aseg": "subcortex",
        "subcortex": "subcortex",
    }

    #: Columns format
    COLUMNS_IDENTIFIER = "TableCol"
    COLUMNS_PROPERTIES = ["ColHeader", "FieldName", "Units", "CastedType"]

    #: Data format
    DATA_IDENTIFIER = "ColHeaders"
    INDEX_COLUMN = "FieldName"

    def __init__(self, stats_file: Union[Path, str]) -> None:
        self.path = validate_stats_file(stats_file)

    def get_structural_measurements(self) -> pd.DataFrame:
        """
        Get the structural measurements from the stats file.

        Returns
        -------
        pd.DataFrame
            Measurements from the stats file.
        """
        lines = self._get_data()
        table_columns = self.table_columns
        converters = [
            UNITS_CONVERTER.get(val.split("^")[0])
            for val in table_columns["Units"]
        ]
        data = pd.DataFrame(
            index=table_columns[self.INDEX_COLUMN], columns=range(len(lines))
        )
        for i, line in enumerate(lines):
            data[i] = [
                converter(val)
                for converter, val in zip(converters, line.split())
            ]
        return data

    def query_hemisphere(self):
        """
        Query the hemisphere of the stats file.

        Returns
        -------
        str
            The hemisphere of the stats file.
        """
        hemi = self.headers.get("hemi")
        if hemi:
            return self.STRUCTURE_MAP.get(hemi, "unknown")
        else:
            return "subcortex"

    def _read_table_columns(self):
        """
        Read stats file's table columns

        Returns
        -------
        list
            A list of the table columns from the stats file.
        """
        table_columns = pd.DataFrame(columns=self.COLUMNS_PROPERTIES)
        for line in self._get_table_columns():
            _, i, col, value = [i.strip() for i in line.split(maxsplit=3)]
            table_columns.loc[int(i), col] = value
            if col == "Units":
                table_columns.loc[int(i), "CastedType"] = UNITS_CONVERTER.get(
                    value.split("^")[0]
                ).__name__
        return table_columns

    def _read_headers(self, special_headers: dict = None) -> dict:
        """
        Parses the headers found in Freesurfer's .stats file.

        Parameters
        ----------
        special_headers : dict, optional
            A dictionary with headers' titles as keys and their
            corresponding target keys and parsing methods
            as "key" and "func" keys accordingly. The default is None.

        Returns
        -------
        dict
            _description_
        """
        special_headers = special_headers or self.SPECIAL_HEADERS
        headers = {}
        for line in self._get_headers():
            header, value = line.split(" ", maxsplit=1)
            key = header
            value = value.strip()
            if header in special_headers:
                parser = special_headers[header]
                func = parser.get("func")
                key = parser.get("key")
                if isinstance(func, Callable):
                    kwargs = parser.get("kwargs", {})
                    value = func(value, **kwargs)
                elif isinstance(func, str):
                    value = func
            headers[key or header] = value
        return headers

    def _get_table_columns(self) -> list:
        """
        Read stats file's table columns

        Returns
        -------
        list
            A list of the table columns from the stats file.
        """
        columns = []
        lines = self.stream.readlines()
        for line in lines:
            line = self._read_header_line(line)
            if line.startswith(self.COLUMNS_IDENTIFIER):
                columns.append(line)
        return columns

    def _get_headers(self) -> list:
        """
        Read stats file's headers

        Returns
        -------
        list
            A list of the headers from the stats file.
        """
        headers = []
        lines = self.stream.readlines()
        for line in lines:
            line = self._read_header_line(line)
            if line.startswith(self.HEADERS_END):
                break
            if line:
                headers.append(line)
        return headers

    def _get_data(self) -> list:
        """
        Read stats file's data rows

        Returns
        -------
        list
            A list of rows containing stats file's measurements
        """
        lines = self.stream.readlines()
        for i, line in enumerate(lines):
            line = self._read_header_line(line)
            if line.startswith(self.DATA_IDENTIFIER):
                break
        return lines[i + 1 :]

    @staticmethod
    def _read_header_line(line: str) -> str:
        """
        Read a header line from the stats file.

        Parameters
        ----------
        line : str
            The line to read.

        Returns
        -------
        str
            The header line.
        """
        # assert line.startswith("# ")
        return line[2:].rstrip()

    @property
    def stream(self):
        """
        Get the stats file as a stream.

        Returns
        -------
        io.TextIOWrapper
            The stats file as a stream.
        """
        return self.path.open("r")

    @property
    def hemisphere(self) -> str:
        """
        Get the hemisphere of the stats file.

        Returns
        -------
        str
            The hemisphere of the stats file.
        """
        return self.query_hemisphere()

    @property
    def headers(self) -> dict:
        """
        Get the headers from the stats file.

        Returns
        -------
        dict
            The headers from the stats file.
        """
        return self._read_headers()

    @property
    def table_columns(self) -> pd.DataFrame:
        """
        Get the table columns from the stats file.

        Returns
        -------
        pd.DataFrame
            The table columns from the stats file.
        """
        return self._read_table_columns()
