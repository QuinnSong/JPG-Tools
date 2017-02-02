#-*- coding: cp936 -*-
import math
from PIL import Image

def lighting(image, power = 20, center=None):
    """
    @效果：灯光
    @param power: 光照强度
    @param center: 光源坐标(x, y)，默认在图片中心
    """
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    
    width, height = image.size
    
    if center is None:
        center = width / 2, height / 2
        
    radius = int(math.sqrt(center[0] ** 2 + center[1] ** 2)) # 半径
    
    pix = image.load()
    
    for w in xrange(width):
        for h in xrange(height):
            # 当前像素点到光源中心距离
            distance = int(math.sqrt((w - center[0]) ** 2 + (h - center[1]) ** 2))
            
            if distance < radius:
                brightness = power * (radius - distance) / radius
                # 光亮值和到光源中心的距离成反比
                #
                r, g, b, a = pix[w, h]
                r = min(r + brightness, 255)
                g = min(g + brightness, 255)
                b = min(b + brightness, 255)
                pix[w, h] = r, g, b, a
                #pix[w,h]= tuple([min(i + brightness, 255) for i in pix[w,h]])
               
    return image