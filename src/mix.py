# -*- coding: cp936 -*-

from PIL import Image
import numpy as np

def MixColor(im, factor = 100, color = (0, 255, 255, 0)):
    """
    混色效果    
    """
    im_array = np.array(im.convert("RGBA"))
    im_array =( im_array * (1 - factor/float(100)) + np.ones_like(im_array) * color * (factor/float(100))).astype(np.uint8)
    return Image.fromarray(im_array) 