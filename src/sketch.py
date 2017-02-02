#-*- coding: cp936 -*-

#以下是素描滤镜的主函数
from PIL import Image

def  sketch(image, threshold = 15):
    """
    素描
    image: Image instance
    param threshold： between 0 and 100
    """
    width, height = image.size
    img = image.convert("L")
    pix = img.load() # get pixel matrix
    
    for w in xrange(width -1):
        for h in xrange(height -1):            
            src = pix[w, h]
            dst = pix[w+1, h+1]
            diff = abs(src - dst)
            if diff >= threshold: pix[w,h] = 0
            else: pix[w,h] = 255

    return img
