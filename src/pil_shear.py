from PIL import Image
from math import sin, cos, tan, radians

def Shear (im, x_angle, y_angle):
    w, h = im.size
    top_angle = 90 - y_angle + x_angle

    a = 1 -  (sin(radians(y_angle))/ sin(radians(top_angle))) * sin(radians(x_angle))
    b = - tan(radians(x_angle))/ sin(radians(top_angle)) *  sin(radians(x_angle)) - tan(radians(x_angle))
    c =  h * tan(radians(x_angle)) /sin(radians(top_angle)) * sin(radians(x_angle)) + h * tan(radians(x_angle))
    d = 1 + (sin(radians(y_angle))/ sin(radians(top_angle))) * cos(radians(x_angle))
    e = tan(radians(x_angle))/ sin(radians(top_angle)) * cos(radians(x_angle))
    f =   h * tan(radians(x_angle)) /sin(radians(top_angle)) * cos(radians(x_angle))
    data = (a,b,c,d,e, f)
    
    size = (w + int(h * tan(radians(x_angle))), h + int(w * tan(radians(y_angle))))

    w, h = im.size
    size = im.size #(w + 30, h + 50)
    IM = im.transform(size, Image.AFFINE, data, resample = Image.BICUBIC )
    IM.show()
im = Image.open("n:\\desktop\\pp_fold_right.png")
Shear(im, 15, 0)