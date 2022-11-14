"""Test the solveit module."""
from pathlib import Path
from click.testing import CliRunner
from wordscapesolver.cli.solveit import solveit

testfile_path = Path(__file__)
test_input =  testfile_path.parent / 'input' / "."
test_output = testfile_path.parent / 'output' / "foo.txt"
test_expected = testfile_path.parent / 'output' / "expected_output.txt"
test_input_str = str(test_input.resolve())
test_output_str = str(test_output.resolve())

# get the expected output
with open(test_expected, "r") as expected_in:
    exp_out = [line.rstrip() for line in expected_in.readlines()]

def test_read_image_files_ok_solveit():
    "Test able to process 13 images in test data input."
    runner = CliRunner()
    result = runner.invoke(solveit, [test_input_str, "-"])
    image_files = [f"img{x:02d}.png" for x in range(1, 14)]
    for cur_image in image_files:
        assert cur_image in result.output

def test_all_words_detected_ok_solveit():
    "All the words are found in all 13 images"
    runner = CliRunner()
    result = runner.invoke(solveit, ["--force", test_input_str, "-"])
    observed = list(result.output.split("\n"))
    
    for idx, (cur_obs, cur_expt) in enumerate(zip(observed, exp_out)):
        assert cur_obs == cur_expt

    assert idx == 467
