#-*- coding: cp936 -*-

import math
from PIL import Image

def swirl(image, degree = 50):
    '''
    @Ч�������У���ͼ�����������Ч����
    @param image: instance of Image
    @param degree: ��ʾ���еĴ�С[0, 100] 
    @return: instance of Image
    '''
    degree = min(max(0, degree), 100) / 1000.0
    
    if image.mode != "RGBA":
        image = image.convert("RGBA")
        
    width, height = image.size
    pix = image.load()
    
    center = width / 2, height / 2 # �������ĵ����ͼƬ����
    
    dst_image = Image.new("RGBA", (width, height))
    dst_pix = dst_image.load()
    
    for w in xrange(width):
        for h in xrange(height):
            offset_x = w - center[0]
            offset_y = h - center[1]
            
            radian = math.atan2(offset_y, offset_x) # �Ƕȣ�ʹ��math.atan2(y, x)���м���
            radius = math.sqrt(offset_x ** 2 + offset_y ** 2) # �뾶�������ص�����ľ���
            
            # ����ԽԶ����ת�ĽǶȾ�Խ��
            # �½Ƕ�Ϊ���Ƕ� + ���� �� Ȩ��
            x = int(radius * math.cos(radian + radius * degree)) + center[0] 
            y = int(radius * math.sin(radian + radius * degree)) + center[1]
            
            x = min(max(0, x), width - 1)
            y = min(max(0, y), height - 1)
            
            dst_pix[w, h] = pix[x, y]
            
    return dst_image