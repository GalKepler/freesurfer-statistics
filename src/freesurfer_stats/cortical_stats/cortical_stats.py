from pathlib import Path
from typing import Union

import pandas as pd

from freesurfer_stats.cortical_stats.format import SpecialHeaders
from freesurfer_stats.freesurfer_stats import FreesurferStats


class CorticalStats(FreesurferStats):
    #: Headers structure
    HEADERS_END = "Measure"

    #: Special headers
    SPECIAL_HEADERS = SpecialHeaders

    def __init__(self, stats_file: Union[Path, str]) -> None:
        super().__init__(stats_file)

    def parse_whole_brain_measurements(
        self,
    ) -> pd.DataFrame:
        """
        Parse whole brain measurements from Freesurfer's .stats file.

        Returns
        -------
        pd.DataFrame
            Whole brain measurements.
        """
        data = pd.DataFrame(columns=["index", "description", "unit", "value"])
        for i, line in enumerate(self._get_wholebrain_measures()):
            _, col, description, val, unit = [
                j.strip() for j in line.split(",")
            ]
            data.loc[i, ["index", "description", "unit"]] = [
                col,
                description,
                unit,
            ]
            data.loc[i, "value"] = float(val)
        return data

    def _get_wholebrain_measures(self) -> list:
        """
        Read stats file's measures

        Returns
        -------
        list
            A list of the measures from the stats file.
        """
        measures = []
        lines = self.stream.readlines()
        for line in lines:
            try:
                line = self._read_header_line(line)
            except AssertionError:
                break
            if line.startswith(self.HEADERS_END):
                measures.append(line.replace(self.HEADERS_END, "").strip())
        return measures

    @property
    def whole_brain_measurements(self) -> pd.DataFrame:
        """
        Get whole brain measurements.

        Returns
        -------
        pd.DataFrame
            Whole brain measurements.
        """
        return self.parse_whole_brain_measurements()
