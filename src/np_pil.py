# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image
"""
Conversions between numpy and pil image
"""

def colorToHex (color):
    r,g,b,a = color
    return eval('0x' + hex(a)[2:].zfill(2) + hex(b)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(r)[2:].zfill(2))
def hexToColor (hex_str):
    return int(hex_str[2:], 16), int(hex_str[4:], 16), int(hex_str[6:], 16)
def npToPil (np_array):
    return Image.fromarray(np_array, mode = "RGBA")
def pilToNp (pil_im):
    pil_im = pil_im.convert("RGBA")
    return np.array(pil_im, dtype=np.uint8)
def newPil (w, h, fill): # using numpy
    np_array =  np.empty( (w,h), np.uint32)
    np_array.shape = h, w
    np_array.fill(colorToHex(fill))
    return Image.frombuffer('RGBA', (w,h), np_array, 'raw', 'RGBA', 0, 1)