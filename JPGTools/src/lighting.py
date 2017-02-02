#-*- coding: cp936 -*-
import math
from PIL import Image

def lighting(image, power = 20, center=None):
    """
    @Ч�����ƹ�
    @param power: ����ǿ��
    @param center: ��Դ����(x, y)��Ĭ����ͼƬ����
    """
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    
    width, height = image.size
    
    if center is None:
        center = width / 2, height / 2
        
    radius = int(math.sqrt(center[0] ** 2 + center[1] ** 2)) # �뾶
    
    pix = image.load()
    
    for w in xrange(width):
        for h in xrange(height):
            # ��ǰ���ص㵽��Դ���ľ���
            distance = int(math.sqrt((w - center[0]) ** 2 + (h - center[1]) ** 2))
            
            if distance < radius:
                brightness = power * (radius - distance) / radius
                # ����ֵ�͵���Դ���ĵľ���ɷ���
                #
                r, g, b, a = pix[w, h]
                r = min(r + brightness, 255)
                g = min(g + brightness, 255)
                b = min(b + brightness, 255)
                pix[w, h] = r, g, b, a
                #pix[w,h]= tuple([min(i + brightness, 255) for i in pix[w,h]])
               
    return image