from pathlib import Path
from typing import Union

from freesurfer_statistics.freesurfer_stats import FreesurferStats
from freesurfer_statistics.subcortical_stats.format import SpecialHeaders


class SubCorticalStats(FreesurferStats):
    #: Headers structure
    HEADERS_END = "TableCol"

    #: Special headers
    SPECIAL_HEADERS = SpecialHeaders

    def __init__(self, stats_file: Union[Path, str]) -> None:
        super().__init__(stats_file)
