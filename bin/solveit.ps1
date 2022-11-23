function solveit ($input_dir, $output_dir) {
    $py_module = "wordscapesolver.cli.solveit"
    & python -m $py_module $input_dir $output_dir
}
