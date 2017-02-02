# -*- coding: utf-8 -*- 
import numpy  as np
from PIL import Image, ImageStat
def avg_image (im):
    """ Return average r,g,b for image"""
    return [int(x) for x in ImageStat.Stat(im).mean]
def mosaic (im, x0, y0, x1, y1, mosaic_size = 8):
    """
    马赛克效果
    mosaic_size：块大小
    x0, y0, x1, y1： 矩形坐标
    """
    w, h = mosaic_size, mosaic_size # the size of mosaic
    im = im.convert("RGBA")
    im_array = np.array(im, dtype=np.uint8)
    #calculate the total pieces in both x and y directions
    width, height = abs(x1-x0)/w, abs(y1-y0)/h
    a = [(x,y) for x in xrange(width) for y in xrange(height)]

    for x, y in a:
        bbox = (x0 + w * x, y0 + w*y, x0 + w * (x + 1), y0 + w* (y + 1))
        bbox_resize = im.crop(bbox ).resize(((x1-x0)/mosaic_size, (y1-y0)/mosaic_size), Image.ANTIALIAS)
        im_array[y0 + h * y: y0 + h * (y + 1), x0 + w * x: x0 + w *(x +1)] = bbox_resize.getpixel((x, y)) #avg_image(im.crop(bbox ))
    im = Image.fromarray(im_array)
    return im

#mosaic(im, 100, 100, 300, 300, 8)