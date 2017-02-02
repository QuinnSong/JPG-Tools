#-*- coding: cp936 -*-

import math
from PIL import Image

def wave(image, degree = 16):
    '''
    @效果：波浪，对图像进行波浪特效处理
    @param image: instance of Image
    @param degree: 表示波浪的大小[0, 32] 
    @return: instance of Image
    '''
    
    degree = min(max(0, degree), 32)
    
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    
    width, height = image.size    
    pix = image.load()
    
    dst_image = Image.new("RGBA", (width, height))
    dst_pix = dst_image.load()
    
    pi2 = math.pi * 2
    
    for w in xrange(width):
        for h in xrange(height):
            x = int(degree * math.sin(pi2 * h / 128.0)) + w
            y = int(degree * math.cos(pi2 * w / 128.0)) + h
            
            x = min(max(x, 0), width - 1)
            y = min(max(y, 0), height - 1)
            
            dst_pix[w, h] = pix[x, y]
    
    return dst_image