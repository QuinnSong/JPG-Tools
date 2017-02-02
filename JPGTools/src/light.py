# -*- coding: cp936 -*-

from PIL import Image
import math
   
def edge_blur ( edgeColor, im, radius_in, radius_out, transparent = False ):
    """
    光圈效果
    如果 transparent = False (0) 那么边缘透明
    """
    im = im.convert("RGBA")
    w,h = im.size
    pixels = im.load()
    cx,cy = (w - 1)/2, h/2

    for y in range(h):
        for x in range(w):
            dist = math.sqrt(pow(x - cx, 2) + pow(y -cy, 2))
            if dist > radius_in and dist <= radius_out:                
                pixels[x, y] = tuple([int(((dist - radius_in) * x1 + (radius_out - dist) * y1)/ (radius_out - radius_in)) for x1,y1 in zip(edgeColor, pixels[x, y])])
                
            if dist > radius_out: pixels[x, y] = edgeColor [0], edgeColor[1], edgeColor[2], 255 * (not transparent)
    return im

