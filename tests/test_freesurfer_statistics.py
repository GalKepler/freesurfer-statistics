from freesurfer_statistics.cli import main


def test_main():
    short_help = main.get_short_help_str()
    assert short_help == "Console script for freesurfer_stats."
