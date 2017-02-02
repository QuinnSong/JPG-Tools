# -*- coding: cp936 -*-

from PIL import Image

def Fade(im, pos = 70, mode = u"淡出", color = (255, 0, 0, 0)):
    """
    渐变效果    
    """
    
    im = im.convert("RGBA")
    w,h = im.size
    pixels = im.load()
    pos = pos * w / 100
    
    if mode == u"淡出":
        for y in range (h):
            for x in range (pos, w):
                factor = float(x - pos) / (w - pos)
                pixels[x, y] = tuple([int(x1  * (1 - factor) + y1 * factor) for x1, y1 in zip(pixels[x,y], color)])
       
    else: # direction == u"上下":
        for y in range (h):
            for x in range (0, pos):
                factor = float(x) / pos
                pixels[x, y] = tuple([int(x1  * (1 - factor) + y1 * factor) for y1, x1 in zip(pixels[x,y], color)])
    return im