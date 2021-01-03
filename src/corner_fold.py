# -*- coding: cp936 -*-

from PIL import Image

def EdgeFold(image, edge, white_percent, pos = u'右边'):
        """
        折角效果
        edge: the percentage of the edge out of width
        image: PIL Image object
        """
        image = image.convert("RGBA")
        edge = image.size[0] * edge / 100
        im = im_trans (image, edge, pos)
        
        taskMapper = { u'右边': img_fold_right, u'左边': img_fold_left }
        im = taskMapper[pos](im, edge, per = white_percent / 100.0)
        return im

   
def LeftTrans(x, y, sq_corner, w):
        if  x < sq_corner and y < sq_corner:
                return sq_corner - y - 1, sq_corner - x - 1
        else:
                return  x, y 

def RightTrans( x, y, sq_corner, w):
        
        if x < w - sq_corner  or y >= sq_corner:
            return  x, y
        else:
            return y + w - sq_corner, x - (w - sq_corner)
        
def numFix (d):
    return d * (0<=d<=255) + 0 * (d < 0) + 255 * (d > 255)
        
def img_fold_left (im, edge = 30, per = 0.2):
    pixels = im.load()
    rw, gw, bw = (255, 255, 255)
    w, h = im.size
    
    for x in range(edge + int(edge * 0.02)):
        for y in range( edge + int(edge * 0.02)):
            r,g,b,a = pixels[x, y]
            
            if x < edge - 1  and y < edge - 1:
                if x  < edge - y - 2:
                    pixels[x, y] = 255,255,255, 0
                elif x  <= edge - y:
                    left = im.getpixel((0, y))
                    pixel = numFix(218- (edge - y -x) * 50)
                    pixels[x, y] =  pixel, pixel, pixel, 255 * a
                    #pixels[x, y] = 182,182,182, 255
                else:   
                    pixels[x, y] =  int(r * (1-per) + rw * per), \
                    int(g * (1-per) + gw * per), \
                    int(b * (1-per) + bw * per), \
                    a
            else:
                if y > edge: a2 = pixels[w - 1, y][3] / 255
                elif x < w - edge: a2 = pixels[x, 0][3] / 255
                if a2 != 0: 
                        pixels[x, y] = 190, 190, 190, numFix(255 - (min(x, y) - edge) * 70)
            
    return im

def img_fold_right (im, edge = 30, per = 0.2): # per is weight for white
    pixels = im.load()
    rw, gw, bw = (255, 255, 255)
    w, h = im.size
    for x in range(w - edge - int(edge * 0.02), w) :
        for y in range( edge + int(edge * 0.02)):
            r,g,b,a = pixels[x, y]
            
            if x > w - edge - 1  and y < edge - 1:
                if x  > w - (edge - y) + 2:
                    pixels[x, y] = 255,255,255, 0
                elif x  >= w - (edge - y):
                    #left = im.getpixel((w, y))
                    pixel = numFix(218- (edge - y -(w -x)) * 70)
                    pixels[x, y] =  pixel, pixel,pixel, numFix(255 -70 * (x -w + (edge-y))) * a
                    #pixels[x, y] = 182,182,182, 255
                else:                    
                    pixels[x, y] =  int(r * (1-per) + rw * per), \
                    int(g * (1-per) + gw * per), \
                    int(b * (1-per) + bw * per), \
                    a
            else:
                if y > edge: a2 = pixels[w - 1, y][3] / 255
                elif x < w - edge: a2 = pixels[x, 0][3] / 255
                else: a2 = 0
                if a2 != 0: 
                        pixels[x, y] = 190, 190, 190,  numFix(255 - (min((w -x), y) - edge) * 70)
        
    return im

def im_trans (im, edge, pos = u'右边'):
        w,h = im.size
        pixels = im.load()
        
        for y in range(edge):
                if pos == u'左边':                
                    for x in range(edge):
                        if x  > edge - y:
                            x1, y1 = LeftTrans(x, y, edge, w)
                            r, g, b, a = pixels[x1, y1]
                            if a != 0:
                               pixels[x, y] = pixels[x1, y1]  
                else:
                    for x in range(w-edge, w):
                        if w - x > edge - y:                            
                            x1, y1 = RightTrans(x, y, edge, w)
                            r, g, b, a = pixels[x1, y1]
                            if a != 0:
                               pixels[x, y] = pixels[x1, y1]                        

        return im