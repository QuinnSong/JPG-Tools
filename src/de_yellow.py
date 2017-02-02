#-*- coding: cp936 -*-
#Thanks to: �� Python ̎���S������Ƭ 
#http://weijr-note.blogspot.ca/2012/03/python.html

from PIL import Image, ImageOps

def deYellow(image, method = 0):
    
    if image.mode != "RGB":
        image = image.convert("RGB")
        
    if method == 0:
        return ImageOps.autocontrast(image)
    elif method == 1:
        return ImageOps.equalize(image)
    else:
        return image
