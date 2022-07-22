"""Main module."""
import re
from pathlib import Path
from typing import Callable, Union

import pandas as pd

from freesurfer_statistics.utils import UNITS_CONVERTER, validate_stats_file


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
    INDEX_COLUMN = "ColHeader"
    COLUMNS_CONVERTER = {"StructName": "Region"}

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
        return pd.read_csv(
            self.path,
            header=None,
            names=self.table_columns[self.INDEX_COLUMN].replace(self.COLUMNS_CONVERTER),
            delim_whitespace=True,
            comment="#",
        )

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
        for line in self.lines:
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
        for line in self.lines:
            line = self._read_header_line(line)
            if line.startswith(self.HEADERS_END):
                break
            if line:
                headers.append(line)
        return headers

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

    def _read_lines(self) -> list:
        """
        Read the stats file's lines.

        Returns
        -------
        list
            A list of the lines from the stats file.
        """
        stream = self.path.open("r")
        lines = stream.readlines()
        stream.close()
        return lines

    @property
    def lines(self) -> list:
        """
        Get the lines contained in the stats file.

        Returns
        -------
        list
            The lines contained in the stats file.
        """
        return self._read_lines()

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

    @property
    def structural_measurements(self) -> pd.DataFrame:
        """
        Get the structural measurements from the stats file.

        Returns
        -------
        pd.DataFrame
            Measurements from the stats file.
        """
        return self.get_structural_measurements()
