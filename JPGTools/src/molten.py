#-*- coding: cp936 -*-
from PIL import Image

def molten(image):
    """效果：熔铸"""
    if image.mode != "RGBA": image = image.convert("RGBA")
    
    width, height = image.size
    pix = image.load()
    
    for w in xrange(width):
        for h in xrange(height):
            r, g, b, a = pix[w, h]
            
            pix[w, h] = min(255, int(abs(r * 128 / (g + b + 1)))), \
                        min(255, int(abs(g * 128 / (b + r + 1)))), \
                        min(255, int(abs(b * 128 / (r + g + 1)))), \
                        a
    return image           