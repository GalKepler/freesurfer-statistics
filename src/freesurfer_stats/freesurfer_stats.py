"""Main module."""
import re
from pathlib import Path
from typing import Callable
from typing import Union

import pandas as pd


class FreesurferStats:
    STRUCTURE_MAP = {
        "lh": "left",
        "rh": "right",
        "aseg": "subcortex",
        "subcortex": "subcortex",
    }
    HEMI_PATTERN = re.compile(r"# hemi (lh|rh)")
    SUBCORTEX_PATTERN = re.compile(r"# cmdline mri_segstats *")

    SPECIAL_HEADERS = {}

    def __init__(self, stats_file: Union[Path, str]) -> None:
        self.path = self.validate_stats_file(stats_file)

    def validate_stats_file(self, stats_file: Union[Path, str]) -> Path:
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

    def get_structural_measurements(self) -> pd.DataFrame:
        """
        Get the structural measurements from the stats file.

        Returns
        -------
        pd.DataFrame
            Measurements from the stats file.
        """
        raise NotImplementedError

    def get_whole_brain_measurements(self) -> pd.DataFrame:
        """
        Get the whole-brain measurements from the stats file.

        Returns
        -------
        pd.DataFrame
            Measurements from the stats file.
        """
        raise NotImplementedError

    def query_header(self) -> list:
        """
        Get the headers from the stats file.

        Returns
        -------
        list
            The headers from the stats file.
        """
        raise NotImplementedError

    def query_hemisphere(self):
        """
        Query the hemisphere of the stats file.

        Returns
        -------
        str
            The hemisphere of the stats file.
        """
        for line in self.stream:
            cortical_match = self.HEMI_PATTERN.match(line)
            if cortical_match:
                return self.STRUCTURE_MAP.get(
                    cortical_match.group(1), "unknown"
                )
            subcortical_match = self.SUBCORTEX_PATTERN.match(line)
            if subcortical_match:
                return "subcortex"
        return "unknown"

    def _read_headers(self, special_headers: dict = None) -> dict:
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
            headers[key] = value
        return headers

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
        assert line.startswith("# ")
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
