"""Console script for freesurfer_stats."""
import json
import sys

import click

from freesurfer_statistics.cortical_stats import CorticalStats
from freesurfer_statistics.subcortical_stats import SubCorticalStats


@click.command()
@click.option(
    "-i",
    "--input-file",
    type=click.Path(exists=True),
    required=True,
    help="Path to the Freesurfer .stats file.",
)
@click.option(
    "-o",
    "--output-file",
    type=click.Path(exists=False),
    required=False,
    help="Path to the output .csv file.",
)
@click.option(
    "-om",
    "--output_metadata",
    type=click.Path(exists=False),
    required=False,
    help="Path to the output metadata .json file.",
)
@click.option(
    "-wb",
    "--whole_brain",
    type=click.Path(exists=False),
    required=False,
    help="Path to the output whole brain measurements' .csv file.",
)
@click.option(
    "-subcort",
    "--is_subcortex",
    is_flag=True,
    default=False,
    help="Whether the stats file is for the subcortical structures.",
)
def main(
    input_file: str,
    output_file: str = None,
    output_metadata: str = None,
    whole_brain: str = None,
    is_subcortex: bool = False,
):
    """Console script for freesurfer_stats."""
    output_file = output_file or input_file.replace(".stats", ".csv")
    if is_subcortex:
        stats = SubCorticalStats(input_file)
    else:
        stats = CorticalStats(input_file)
    stats.structural_measurements.to_csv(output_file)
    if output_metadata:
        output_metadata = output_metadata or input_file.replace(".stats", ".json")
        with open(output_metadata, "w") as f:
            json.dump(stats.headers, f)
    if whole_brain:
        whole_brain = whole_brain or input_file.replace(".stats", "_wholebrain.csv")
        stats.whole_brain_measurements.to_csv(whole_brain)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
