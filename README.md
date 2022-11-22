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
set the path to Tesseract in the configuration file (default config is in ./etc/config.ini)

    C:\Program Files\Tesseract-OCR\tesseract

The path currently set is the default installation path for Windows

    (png2txt) github clone https://github.com/ian1roberts/wordscapesolver.git
    (png2txt) cd wordscapesolver
    (png2txt) pip install -r requirements.txt
    (png2txt) pip install -e .

Testing installation
```
  (png2txt) tox . 
```

## Workflow as follows:
1. Take screenshot of puzzle board (on iPhone press volume up and powerswitch simultaneously)
2. Share screenshot to your images input directory in the package install (I've been using OneDrive to transfer images)
3. Run wordscapesolver.py to compute playable words

## Example session
> sample images are in the test directory

This example runs wordscapesolver on the 13 test images in the tests directory,
and writes the output in a file `found.txt`
Progress is displayed in on screen log messages

    python -m wordscapesolver.cli.solevit --task run --no-move tests/input found.txt

````(png2txt) wordscapesolver> python -m wordscapesolver.cli.solveit --task run --force --no-move .\tests\input\ found.txt
INFO:__main__:wordscapesolver.cli.solveit --task run found.txt .\tests\input\
INFO:__main__:Reading input from .\tests\input\ and writing output to found.txt
INFO:__main__:Working on ... img01.png
INFO:__main__:Processed img01.png --> BESLOU
INFO:__main__:  3 letter words ...      7
INFO:__main__:  4 letter words ...      11
INFO:__main__:  5 letter words ...      5
INFO:__main__:  6 letter words ...      1
INFO:__main__:  Longest words ... BLOUSE
INFO:__main__:Done img01.png    24 words found.
````
... etc etc

````INFO:__main__:Working on ... img13.png
INFO:__main__:Processed img13.png --> ADYRAWW
INFO:__main__:  3 letter words ...      9
INFO:__main__:  4 letter words ...      7
INFO:__main__:  5 letter words ...      1
INFO:__main__:  7 letter words ...      1
INFO:__main__:  Longest words ... WAYWARD
INFO:__main__:Done img13.png    18 words found.
````
View all the found words in the output file `found.txt`
    
    cat found.txt # just the last example
    
````
 ================================================================================

img13.png
ADYRAWW

3 letter words
        DAY
        DRY
        RAW
        RAY
        WAD
        WAR
        WAY
        WRY
        YAW

4 letter words
        AWAY
        AWRY
        DRAW
        DRAY
        WARD
        WARY
        YARD

5 letter words
        AWARD

7 letter words
        WAYWARD

================================================================================
````

## Command line
````
Usage: python -m wordscapesolver.cli.solveit [OPTIONS] [XINPUT] [XOUTPUT]

  Given an input directory, iterate over PNG screenshots and process WordScape
  puzzles. User may also supply a single image file.
  Words are sent to standard out (-) or `output` file

  python -m wordscapesolver.cli.solveit --move --force --task run [input
  directory or single file] [output file or stdout]

Options:
  --task [run|debug]        run normally or in debug mode. Debug displays
                            letter detection images, click close to continue.
  --force / --no-force      Force overwrite of output text.
  --logfile / --no-logfile  Save a session log.
  --move / --no-move        Move processed images to an output directory.
  --config TEXT             Filepath to configuration file (default
                            /etc/config.ini
  --help                    Show this message and exit.
````

## Configuration
There are a few parameters you can set in the ./etc/config.ini file, as shown

    # Configurations for wordscapesolver
    [IMAGE]
    # imageparse.py configs
    # path to system install of tesseract executable
    TESSERACT_PATH = C:\Program Files\Tesseract-OCR\tesseract
    # Padding space to add around images
    PAD = 5
    # Optimal size in pixels of images for OCR
    OPTSIZE = 25
    # Tesseract inline configuration command
    CUSTOM_CONFIG = -l eng --oem 3 --psm 10 -c tessedit_char_whitelist="1il:|ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    [DICTIONARY]
    # Filepath to dictionary, by default use one in /etc
    DICT = DEFAULT

You may supply alternative dictionary files to the DEFAULT one supplied in `./etc/british-english.txt` just give the full path to the word file.

## Developers
Install the developer environment with
    
    pip install -r dev-requirements.txt

* Developed with Python3.9.6
* Tests with pytest
* Automation with tox

Get started with 
``` tox . ```




