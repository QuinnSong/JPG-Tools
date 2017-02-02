from PIL import Image
from math import tan, radians, sin, cos

def Shear(im, x_angle = 45, y_angle = 45, bkcolor = (255,255,255,255)):
    im = im.convert("RGBA")
    pixels = im.load()
    w, h = im.size
    
    top_angle = 90 - y_angle + x_angle
    # calculate x factors in (ax + by + c)
    a = 1
    b =  tan(radians(x_angle))
    c =  - h * tan(radians(x_angle))
    x_factor = sin(radians(y_angle))/(cos(radians(x_angle)) * sin(radians(top_angle)))
    # calculate y factors in (dx + ey + f)
    d = - x_factor
    e =  1 - tan(radians(x_angle)) * x_factor
    f =   h * tan(radians(x_angle))* x_factor
    
    size = (int((w * e - c * e + b * f)/ (a * e - b * d)),
            h + int(w * sin(radians(y_angle))/(cos(radians(x_angle)) * sin(radians(top_angle)))))    
    im_new = Image.new("RGBA", size = size, color = bkcolor)
    pixels_new = im_new.load()
    
    for y in range(size[1]):            
        for x in range(size[0]):
                x_old = int(a * x + b * y + c)
                y_old = int(d * x + e * y + f)
                if x_old in range(w) and y_old in range(h):
                    pixels_new[x, y] = pixels[x_old, y_old]
    return im_new