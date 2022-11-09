#! /usr/bin/bash

# stop on first error
set -e

# print all executed commands to screen
set -x

python -m wordscapesolver.cli.solveit --task run "$@" -

# prevent window closing
pause
