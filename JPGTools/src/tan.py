#-*- coding: cp936 -*-

from PIL import Image
#from shadow import has_transparency

def tan(image):
    '''
    @效果：老照片（深褐色）
    @param image: instance of Image
    @return: instance of Image
    '''
    
    if image.mode != "RGBA":
        image = image.convert("RGBA")    
    
    # 获得图片的宽、高
    width, height = image.size

    pix = image.load()

    for w in xrange(width):
        for h in xrange(height):
            cr_p = pix[w, h] # 当前像素点

            R = (25756 * cr_p[0] + 50397 * cr_p[1] + 12386 * cr_p[2]) >> 16
            G = (22872 * cr_p[0] + 44958 * cr_p[1] + 11010 * cr_p[2]) >> 16;
            B = (17826 * cr_p[0] + 34996 * cr_p[1] + 8585 * cr_p[2]) >> 16;

            if R < 0: R = 0
            if R > 255: R = 255

            if G < 0: G = 0
            if G > 255: G = 255

            if B < 0: B = 0
            if B > 255: B = 255

            pix[w, h] = R, G, B, cr_p[3]

    return image