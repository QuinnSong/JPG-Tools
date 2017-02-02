#-*- coding: cp936 -*-
#Thanks to: 用 Python 處理泛黃的老照片 
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
