# -*- coding: cp936 -*-

from PIL import Image
import numpy as np
from np_pil import colorToHex

def Replace(im_array, color_old, color_new, flag = "=", color_old_max = None ):
    """
    颜色替换: return Image array    
    """
    r_old,g_old,b_old,a_old = color_old    
    r,g,b,a = im_array[:,:,0], im_array[:,:,1], im_array[:,:,2], im_array[:,:,3]
    if flag == u'>': mask = (r > r_old) & (g > g_old) & (b > b_old) & (a >= a_old)
    elif flag == u'=': mask = (r == r_old) & (g == g_old) & (b == b_old) & (a == a_old)
    elif flag == u'≠': mask = np.not_equal(r, r_old) & np.not_equal(g, g_old) & np.not_equal(b, b_old) # & np.not_equal(a, a_old) // ignore this channel
    elif flag == u'<': mask = (r < r_old) & (g < g_old) & (b < b_old) & (a <= a_old)
    else:
        r_old_max,g_old_max,b_old_max,a_old_max = color_old_max
        mask = np.logical_and(r > r_old, r < r_old_max) & np.logical_and(g > g_old, g < g_old_max) & np.logical_and(b > b_old, b < b_old_max) & np.logical_and(a >= a_old, a <= a_old_max)
    im_array[:,:,:4][mask] = color_new
    return im_array