# -*- coding: cp936 -*- 

from PIL import Image
import numpy as np

def ImgSalon(x_qty, y_qty, im_list, bkcolor, is_column = True, gap = 0):
    """
    拼图效果
    im_list: list of all image objects    
    """
    count = 0
    # which is max?
    [w,h] = im_list[0].size
    #im_new = Image.new("RGBA", (x_qty * w + (x_qty -1) * gap, y_qty * h + (y_qty -1) * gap), color = bkcolor)
    # create empty background
    im = np.zeros([y_qty * h + (y_qty -1) * gap, x_qty * w + (x_qty -1) * gap, 4], dtype=np.uint8)
    im[:] = bkcolor
    
    if is_column:
        for x in range(x_qty):
            for y in range(y_qty):
                if len(im_list) == 1:
                    im[y * h + y * gap:y* h + h + y * gap, x * w + x * gap:x * w + w  + x * gap] = np.array( im_list[0] )
                    #im_new.paste(im, (x * w + x * gap, y * h + y * gap, x * w + w  + x * gap, y* h + h + y * gap))
                elif count < len(im_list):
                    _im = im_list[count]
                    print _im.mode
                    w1, h1 = _im.size
                    _im = _im.resize((w,h))
                    im[y * h + y * gap:y* h + h + y * gap, x * w + x * gap:x * w + w  + x * gap] = np.array(_im )
                    count = count + 1
                else:   break
    else:
        for y in range(y_qty):
            for x in range(x_qty):            
                if len(im_list) == 1:
                    im[y * h + y * gap:y* h + h + y * gap, x * w + x * gap:x * w + w  + x * gap] = np.array( im_list[0] )
                    #im_new.paste(im, (x * w + x * gap, y * h + y * gap, x * w + w  + x * gap, y* h + h + y * gap))
                elif count < len(im_list):
                    _im = im_list[count]
                    print _im.mode
                    w1, h1 = _im.size
                    _im = _im.resize((w,h))
                    im[y * h + y * gap:y* h + h + y * gap, x * w + x * gap:x * w + w + x * gap] = np.array( _im )
                    count = count + 1
                else:   break
    return Image.fromarray(im)