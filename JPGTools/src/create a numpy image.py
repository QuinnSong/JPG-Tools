np_array =  np.empty( (w,h), np.uint32)
np_array.shape = h, w
np_array[:,:] = 0xFF0000FF #self.colorToHex(color_new)
self.cur_im = Image.frombuffer('RGBA', (w,h), np_array, 'raw', 'RGBA', 0, 1)

def colorToHex (self, color):
    r,g,b,a = color
    return eval('0x' + hex(a)[2:].zfill(2) + hex(b)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(r)[2:].zfill(2))