"""Test the solveit module using supplied images and known output
supplied in the test data directory."""
import pytest
from pathlib import Path
from click.testing import CliRunner
from wordscapesolver.cli.solveit import solveit

testfile_path = Path(__file__)


@pytest.mark.parametrize(
    "test_img, idx, nlines",
    [
        ("img01.png", "01", 35),
        ("img02.png", "02", 30),
        ("img03.png", "03", 32),
        ("img04.png", "04", 33),
        ("img05.png", "05", 31),
        ("img06.png", "06", 41),
        ("img07.png", "07", 32),
        ("img08.png", "08", 37),
        ("img09.png", "09", 44),
        ("img10.png", "10", 36),
        ("img11.png", "11", 25),
        ("img12.png", "12", 48),
        ("img13.png", "13", 30),
    ],
)
def test_read_image_files_ok_solveit(test_img, idx, nlines):
    "Test able to process 13 images in test data input."

    def _get_expected_output(xname):
        "Load supplied list of known outcomes for each image."
        fname = f"expected_im{xname}.txt"
        test_expected = testfile_path.parent / "output" / fname
        with open(test_expected, "r") as expected_in:
            exp_out = [line.rstrip() for line in expected_in.readlines()]
        return exp_out

    runner = CliRunner()
    test_img = testfile_path.parent / "input" / test_img
    test_img = str(test_img.resolve())

    # This innvocation is equivalent processes a single image and displays output to stdout
    # >> python -m wordscapesolver.cli.solveit --task run .\tests\input\img13.png -
    result = runner.invoke(solveit, [test_img, "-"], catch_exceptions=False)

    # click runner executes command and returns cleanly
    assert result.exit_code == 0

    observed = list(result.output.split("\n"))
    expected = _get_expected_output(idx)

    for idx01, (cur_obs, cur_expt) in enumerate(zip(observed, expected)):
        # Result is line by line identical with expected outcome
        assert cur_obs == cur_expt

    # Confirm expected number of results identified
    assert idx01 == nlines
