#-*- coding: cp936 -*-

import math
from PIL import Image

def spherize(image):
    '''
    @Ч�������棬��ͼ�����������Ч����(������)
    @param image: instance of Image
    @return: instance of Image
    '''
    
    width, height = image.size
    
    mid_x = width / 2
    mid_y = height / 2 # modified
    max_mid_xy = max(mid_x, mid_y)
    
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    pix = image.load()
    
    dst_image = Image.new("RGBA", (width, height))
    dst_pix = dst_image.load()
    
    for w in xrange(width):
        for h in xrange(height):
            offset_x = w - mid_x
            offset_y = h - mid_y
            
            radian = math.atan2(offset_y, offset_x) # �Ƕȣ�ʹ��math.atan2(y, x)��
            # ���ﲻ�������İ뾶
            radius = (offset_x ** 2 + offset_y ** 2) / max_mid_xy
            
            x = int(radius * math.cos(radian)) + mid_x
            y = int(radius * math.sin(radian)) + mid_y
            
            x = min(max(x, 0), width - 1)
            y = min(max(y, 0), height - 1)
            
            dst_pix[w, h] = pix[x, y]
            
    return dst_image