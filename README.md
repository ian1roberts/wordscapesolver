# WordScapeSolver

Solves WordScape puzzles using pytesseract and openCV2 libraries
Most of the OCR and image manipulation code reused directly from pytesseract examples.
* [tesseract](https://github.com/tesseract-ocr/tessdoc)
* [pytesseract](https://pypi.org/project/pytesseract/)
* [openCV2](https://pypi.org/project/opencv-python/)
My contributions, mostly tweaking tesseract settings to improve letter detection and providing the wrapper.


## Workflow as follows:
1. Take screenshot of puzzle board (on iPhone press volume up and powerswitch simultaneously)
2. Share screenshot to your images input directory in the package install (I've been using OneDrive to transfer images)
3. Run wordscapesolver.py to compute playable words

## Example session
>> sample images are in the test directory
