# -*- coding: cp936 -*-

from PIL import Image
import random

WHITE_FACTOR = 5

def Tear(im, pos = 80, direction = u"左右", isCut = True):
    """
    锯齿边缘
    isCut： cut unused transparent edge
    """
    
    im = im.convert("RGBA")
    w,h = im.size
    pixels = im.load()
    
    if direction == u"左右":
        x = 0
        tmp = None
        Down = False
        x_cut = w
        y_cut = (pos + 5) * h / 100  
        while x < w:
            y_start = pos * h / 100  
            y_factor = random.randint(1,3)
            white_factor = 5
            f = getInt()
            if tmp:
                if f > tmp: Down = False
                else: Down = True
            tmp =f
            for i in range(f):
        
                if Down:
                    data = getdata(f - i)
                else: 
                    data = getdata(i)
                try:
                    for j in range(len(data)):
                        r,g,b,a = pixels[x + i,y_start+ j + y_factor]
            
                        rr,gg,bb = data[j]
                        pixels[x + i, y_start + j + y_factor ] = r + rr, g + gg, b + bb, a
                except: pass
                
                try:
        
                    for j in range(y_start + j + y_factor + 1, h):
                        pixels[x + i,j] = 255,255,255,0
                except: pass
            
            x = x + f
        
    else: # direction == u"上下":
        y = 0
        tmp = None
        Down = False
        y_cut = h
        x_cut = (pos + 5) * w / 100
        while y < h:
            x_start = pos * w / 100
            x_factor = random.randint(1,3)
            white_factor = 5
            f = getInt()
            if tmp:
                if f > tmp: Down = False
                else: Down = True
            tmp =f
            for i in range(f):
        
                if Down:
                    data = getdata(f - i)
                else: 
                    data = getdata(i)
                try:
                    for j in range(len(data)):
                        r,g,b,a = pixels[x_start+ j + x_factor, y + i]
            
                        rr,gg,bb = data[j]
                        pixels[x_start + j + x_factor, y + i ] = r + rr, g + gg, b + bb, a
                except: pass
                
                try:
        
                    for j in range(x_start + j + x_factor + 1, w):
                        pixels[j, y + i] = 255,255,255,0
                except: pass
            
            y = y + f
            
    if not isCut: return im
    else: return im.crop((0, 0, x_cut, y_cut))

def getInt():
    i = random.randint(2, 6)
    return i

def getdata(f):
    data = [(0,0,0)] + [d for d in ((-1,-1,-1),) * 2] + [(-5,-5,-5),(0,0,0)] + [d for d in  ((-4, -2,-3),)* 1 ] + [d for d in  ((-3,-1,-2),)* 1 ] + [d for d in  ((-2,0,-1),)* f ] + \
    [d for d in ((-12,-12,-12),) * WHITE_FACTOR] + [ (-24,-24,-24),(-32,-31,-46),(-17,-20,-37),(-10,-25,-25),(-41,-57,-16) ]
    return data
