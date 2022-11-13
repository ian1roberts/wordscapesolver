"""Provides wordscapesolver with image manipulation and OCR functions"""
from math import floor

import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"
CUSTOM_CONFIG = (
    r"""-l eng --oem 3 --psm 10 """
    """-c tessedit_char_whitelist="1il:|ABCDEFGHIJKLMNOPQRSTUVWXYZ" """
)
PAD = 5
OPTSIZE = 25
ALPHA = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def do_contour(cur_contour, img, debug: bool = True) -> chr:
    """For each detected region
    1. Setup segmentation coordinates from contour detection
    2. If h:w ratio fits a letter, and area is big enough process
    3. Segment image by coordinates
    4. Scale segment to area preferred for OCR - default is 25 px + 5 px padding
    5. Invert image for black txt on white background
    6. Call out to pytesseract OCR letter detection

    Args:
        cur_contour (contour): contour coordinates detected from open CV
        img (cv2.Image): Image object
        debug (bool, optional): if debug, display intermediate letter detection images
    """
    x_loc, y_loc, width, height = cv2.boundingRect(cur_contour)
    tpos = -PAD + y_loc
    bpos = y_loc + height + PAD
    rpos = -PAD + x_loc
    lpos = x_loc + width + PAD
    ratio = height / width
    area = cv2.contourArea(cur_contour)
    letter = False
    if ratio > 0.7 and 100 < area < 10000:
        # foreground image
        selection = img[tpos:bpos, rpos:lpos]
        src_height, src_width = selection.shape
        # proportion of 30
        scale_factor = OPTSIZE / src_height
        des_w = floor(src_width * scale_factor)
        des_dim = (des_w, OPTSIZE)
        resized = cv2.resize(selection, des_dim, interpolation=cv2.INTER_AREA)
        segment = cv2.bitwise_not(resized)
        letter = pytesseract.image_to_string(segment, config=CUSTOM_CONFIG)
        letter = letter.strip().upper()
        if letter == "":
            letter = "*"

        if letter in [":", "|", "1", "i", "l"]:
            letter = "I"

        if debug:
            cv2.imshow("segment", segment)
            cv2.waitKey(0)
    return letter


def proc_image(img) -> chr:
    """For each image file, process ready for OCR

    Args:
        img (_type_): _description_
    """
    img = cv2.imread(str(img))
    # manually cropping coords defined by checking an image in Gimp
    im_left, im_top, im_right, im_bottom = (134, 1056, 610, 1540)
    img = img[im_top:im_bottom, im_left:im_right]
    img = cv2.resize(img, None, fx=1.25, fy=1.25, interpolation=cv2.INTER_CUBIC)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    img = cv2.bilateralFilter(img, 9, 75, 75)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    items = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = items[0] if len(items) == 2 else items[1]

    detected = ""
    for cur_contour in contours:
        letter = do_contour(cur_contour, thresh, False)
        if letter:
            detected += letter

    return detected
