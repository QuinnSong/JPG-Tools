#-*- coding: cp936 -*-
import numpy as np
from PIL import Image

def slice_gone (im, point1, point2, horizontal):
    """
    切除再拼接
    """

    im = im.convert("RGBA")
    w,h = im.size
    im_array = np.array(im)
    list_im = np.delete(im_array, np.r_[point1:point2], int(horizontal))
    
    # return that beautiful picture
    return Image.fromarray( list_im)
    # http://stackoverflow.com/questions/14078818/efficiently-remove-rows-columns-of-numpy-image-array
