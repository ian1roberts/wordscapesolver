from math import floor

import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
custom_config = r'-l eng --oem 3 --psm 10 -c tessedit_char_whitelist="1il:|ABCDEFGHIJKLMNOPQRSTUVWXYZ" '
pad = 5
optsize = 25
alpha = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def do_contour(c, img, debug=True):
    x, y, w, h = cv2.boundingRect(c)
    tpos = -pad + y
    bpos = y + h + pad
    rpos = -pad + x
    lpos = x + w + pad
    ratio = h/w
    area = cv2.contourArea(c)
    letter = False
    if ratio > 0.7 and 100 < area < 10000:
        # foreground image
        selection = img[tpos: bpos, rpos: lpos]
        src_h, src_w = selection.shape
        # proportion of 30
        sf = (optsize / src_h)
        des_w = floor(src_w * sf)
        des_dim = (des_w, optsize)
        resized = cv2.resize(selection, des_dim, interpolation=cv2.INTER_AREA)
        segment = cv2.bitwise_not(resized)
        letter = pytesseract.image_to_string(segment, config=custom_config)
        letter = letter.strip().upper()
        if letter == "":
            letter = "*"
        
        if letter in [':', '|', '1', 'i', 'l']:
            letter = "I"
            
        if debug:
            cv2.imshow("segment", segment)
            cv2.waitKey(0)
    return(letter)

def procImage(img):
    img = cv2.imread(str(img))
    l, t, r, b = (134, 1056, 610, 1540)
    img = img[t:b, l:r]
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
    for c in contours:
        letter = do_contour(c, thresh, False)
        if letter:
            detected += letter

    return(detected)

