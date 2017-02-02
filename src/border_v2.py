# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image
from np_pil import newPil, pilToNp

def border(image, border_width, color, opacity = 100):
    """
    ±ß¿ò£ºwith same width on all sides
    """
    #create an image with color and opacity using numpy
    w, h = image.size
    color = color[0], color[1], color[2], int(opacity * 255 / 100)
    # create background with above color
    bg_img = newPil(w + border_width * 2 , h + border_width * 2 , fill = color)
    im_array = pilToNp(image)
    bg_img_array = pilToNp(bg_img)
    # move image to center of background
    bg_img_array[border_width : (border_width + h), border_width : (border_width + w)] =  im_array
    return Image.fromarray(bg_img_array)   