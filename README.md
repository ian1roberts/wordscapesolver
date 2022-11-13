# WordScapeSolver
Solves WordScape puzzles using pytesseract and openCV2 libraries
Most of the OCR and image manipulation code reused directly from pytesseract examples.
* [tesseract](https://github.com/tesseract-ocr/tessdoc) - OCR application
* [pytesseract](https://pypi.org/project/pytesseract/) - Python API
* [openCV2](https://pypi.org/project/opencv-python/) - Image manipulation

My contributions, mostly tweaking tesseract settings to improve letter detection and providing the wrapper.

# Install
Its recommended to install in a [virtual environment](https://docs.python.org/3/library/venv.html#module-venv)


    python -m venv png2txt
    ./png2txt/Scripts/activate

You must have a fully working installation of Tesseract OCR and
set the path to Tesseract in the `imageparse.py` module Line 7


    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

The path currently set is the default installation path for Windows

    (png2txt) github clone https://github.com/ian1roberts/wordscapesolver.git
    (png2txt) cd wordscapesolver
    (png2txt) pip install -r requirements.txt
    (png2txt) pip install -e .


## Workflow as follows:
1. Take screenshot of puzzle board (on iPhone press volume up and powerswitch simultaneously)
2. Share screenshot to your images input directory in the package install (I've been using OneDrive to transfer images)
3. Run wordscapesolver.py to compute playable words

## Example session
> sample images are in the test directory

This example runs wordscapesolver on the 13 test images in the tests directory,
and writes the output in a file found.txt
Progress is displayed in on screen log messages

    python -m wordscapesolver.cli.solevit --task run --no-move tests/input found.txt

## Command line
````
Usage: python -m wordscapesolver.cli.solveit [OPTIONS] [XINPUT] [XOUTPUT]

  Given an input directory, iterate over PNG screenshots and process WordScape
  puzzles. Words are sent to standard out (-) or `output` file

  python -m wordscapesolver.cli.solveit --move --force --task run [input
  directory] [output file]

Options:
  --task [run|debug]        run normally or in debug mode. Debug displays
                            letter detection images, click close to continue.
  --force / --no-force      Force overwrite of output text.
  --logfile / --no-logfile  Save a session log.
  --move / --no-move        Move processed images to an output directory.
  --help                    Show this message and exit.
````

## Developers
Install the developer environment with
    
    pip install -r dev-requirements.txt

* Developed with Python3.9.6
* Tests with pytest
* CICD with tox



