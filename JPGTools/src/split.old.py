#-*- coding: cp936 -*-
from PIL import Image, ImageDraw

def equal_split(i, num):
    if num == 1: return [0, i]
    else:
        jump = [j for j in xrange(1, i) if len([a for a in xrange(0, i, j)]) == num][0]
        result = [r for r in xrange(0, j, jump)]
        result.append(i)
        return result
def split(im, rows, cols, line_color, out_dir = None):
    """
    图片分割效果
    out_dir = None when preview
    """
    im = im.convert('RGBA')
    w, h = im.size
   
    ew, eh = equal_split(w, rows), equal_split(h, cols)
    if out_dir:
        for y in xrange (cols):
            for x in xrange(rows):
                im.crop((ew[x],eh[y],ew[x+1],eh[y+1])).save( out_dir + r'_%s%s.png' % (x,y))
        return None
    else: 
        draw = ImageDraw.Draw(im, 'RGBA')
        for y in xrange (1, cols):
            draw.line((0, eh[y], w, eh[y]), fill = line_color)
        for x in xrange(1, rows):
            draw.line((ew[x], 0, ew[x], h), fill = line_color)

        del draw
        return im    
