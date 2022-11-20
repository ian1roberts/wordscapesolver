"""Test the solveit module."""
import pytest
from pathlib import Path
from uuid import uuid4
from click.testing import CliRunner
from wordscapesolver.cli.solveit import solveit

testfile_path = Path(__file__)


@pytest.mark.parametrize("test_img, idx, nlines", [("img01.png", "01", 35)])
def test_read_image_files_ok_solveit(test_img, idx, nlines):
    "Test able to process 13 images in test data input."

    def _get_expected_output(xname, typex=True):
        if typex:
            fname = f"expected_im{xname}.txt"
            test_expected = testfile_path.parent / "output" / fname
        else:
            test_expected = xname
        with open(test_expected, "r") as expected_in:
            exp_out = [line.rstrip() for line in expected_in.readlines()]
        return exp_out

    tmp_fout = f"temp_{uuid4()}.txt"
    runner = CliRunner()
    test_img = testfile_path.parent / "input" / test_img
    tmp_fout = testfile_path.parent / tmp_fout
    test_img = str(test_img.resolve())
    tmp_fout = str(tmp_fout.resolve())
    runner.invoke(solveit, [test_img, tmp_fout], catch_exceptions=False)
    # assert result.exit_code == 0
    observed = _get_expected_output(tmp_fout, typex=False)
    expected = _get_expected_output(idx, typex=True)
    # Path(tmp_fout).unlink()

    for idx01, (cur_obs, cur_expt) in enumerate(zip(observed, expected)):
        assert cur_obs == cur_expt
    assert idx01 == nlines
