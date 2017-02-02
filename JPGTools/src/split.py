#-*- coding: cp936 -*-
from PIL import Image, ImageDraw
    
def equal_split(i,num):
    """
    i: the width or height
    num: number of splits
    """
   
    if  i%num == 0:        
        return range(0, i + 1, i/num)
    else:
        reg = range(0, i, i//num)
        reg.reverse()
        result = [ i - ( i//num )* x - x if x < i%num else reg[x] for x in range(len(reg))]
        #result = [x + i%num - reg.index(x) if reg.index(x) < i%num else x for x in reg]
        result.reverse()
        return result
    
def pixel_split(i, num):
    """
    i: the width or height
    num: number of pixels per split
    """
    ini_result = range(0, i, num)
    if i not in ini_result: ini_result.append(i)
    return ini_result
    
def split(im, rows, cols, line_color, isPx, isPy, out_dir = None):
    """
    图片分割效果
    out_dir = None when preview
    isPx: using pixels in X axis
    isPy: using pixels in Y axis
    """
    im = im.convert('RGBA')
    w, h = im.size
   
    ew = pixel_split(w, rows) if isPx else equal_split(w, rows)
    eh = pixel_split(h, cols) if isPy else equal_split(h, cols)
    #ew, eh = equal_split(w, rows), equal_split(h, cols)
    if out_dir:
        for y in xrange ((len(eh)-1) if isPy else cols):
            for x in xrange((len(ew)-1) if isPx else rows):
                im.crop((ew[x],eh[y],ew[x+1],eh[y+1])).save( out_dir + r'_%s%s.png' % (x,y))
        return None
    else: 
        draw = ImageDraw.Draw(im, 'RGBA')
        if isPy:
            for y in eh[1:-1]: draw.line((0, y, w, y), fill = line_color)
        else:
            for y in xrange (1, cols):
                draw.line((0, eh[y], w, eh[y]), fill = line_color)
        if isPx:
            for x in ew[1:-1]: draw.line((x, 0, x, h), fill = line_color)
        else:
            for x in xrange(1, rows):
                draw.line((ew[x], 0, ew[x], h), fill = line_color)

        del draw
        return im

if __name__ == '__main__':    
    print equal_split(349, 50)
    print pixel_split(349, 50)

