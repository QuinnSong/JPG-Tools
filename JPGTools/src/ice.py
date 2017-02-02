#-*- coding: cp936 -*-

from PIL import Image

def ice(image):
    '''
    @效果：冰冻
    @param image: instance of Image
    @return: instance of Image
    '''    
    if image.mode != "RGBA":
        image.convert("RGBA")
        
    width, height = image.size
    pix = image.load()
    
    for w in xrange(width):
        for h in xrange(height):
            try:
                r, g, b, a = pix[w, h]                
                pix[w, h] = min(255, int(abs(r - g - b) * 3 / 2)), \
                            min(255, int(abs(g - b - r) * 3 / 2)), \
                            min(255, int(abs(b - r - g) * 3 / 2)), \
                            a
            except TypeError:
                pass            
    return image