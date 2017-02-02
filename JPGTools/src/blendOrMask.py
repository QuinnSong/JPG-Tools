# -*- coding: cp936 -*-

from PIL import Image, ImageChops
from shadow import paste

def AddMask(im, mask, color = (255,255,255,255)):
    """
    图片蒙版（mask)效果
    背景色缺省是白色
    """
    
    im = im.convert("RGBA")
    background = Image.new('RGBA', im.size, color)
    
    # convert mask mode and resize it
    mask = mask.convert('L')
    mask = mask.resize(im.size, Image.ANTIALIAS)   
    paste(im, background, (0, 0), ImageChops.invert(mask))
    
    return im

def blend(im, im2, alpha = 0.5):
    """
    图片混合效果
    If the alpha is 0.0, a copy of the first image is returned. If the alpha is 1.0, a copy of the second image is returned.
    Both images must have the same size and mode.
    """
    if im2.size != im.size:
        im2 = im2.resize(im.size, Image.ANTIALIAS)
    im, im2 = [image.convert('RGBA') for image in [im, im2] ]   
    return Image.blend(im, im2, alpha)

if __name__ == '__main__':
    im = Image.open('water.jpg')
    #mask = Image.open(r'D:\windows\Desktop\Folder keep\FSViewer50\Mask\mask76.jpg')
    #im = AddMask(im, mask)
    im2 = Image.open('edge2-5.png')
    im = blend(im, im2, 0.2)
    im.show()
    
 
