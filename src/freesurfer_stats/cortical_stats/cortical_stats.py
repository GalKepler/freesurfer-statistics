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

    #: Special measurements
    SPECIAL_WHOLEBRAIN_MEASUREMENTS = {}

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
        for i, line in enumerate(self._get_measures()):
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
