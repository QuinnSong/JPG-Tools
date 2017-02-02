# -*- coding: cp936 -*- 

from PIL import Image
import numpy as np

def ImgSalon(x_qty, y_qty, im_list, bkcolor, is_column = True, gap = 0, allow_resize = False):
    """
    拼图效果
    im_list: list of all image objects    
    """
    ## resize all images if not same size
    if len(set(map(lambda x: x.size, im_list))) != 1:
        max_shape = tuple([max(j) for j in zip(*[i.size for i in im_list])])
        w, h = max_shape
        if allow_resize:
            # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
            im_list = [ i.resize(max_shape, Image.ANTIALIAS)  for i in im_list ]
        # if x*y more than avaiable pics
        if len(im_list) > 1 and len(im_list) < x_qty * y_qty:
            emp = np.zeros([max_shape[1], max_shape[0], 4], dtype=np.uint8)
            emp[:] = bkcolor
            im_list = im_list + [Image.fromarray(emp)] * (x_qty * y_qty - len(im_list))

    else:
        w,h = set(map(lambda x: x.size, im_list)).pop()
        if len(im_list) > 1 and len(im_list) < x_qty * y_qty:
                emp = np.zeros([h, w, 4], dtype=np.uint8)
                emp[:] = bkcolor
                im_list = im_list + [Image.fromarray(emp)] * (x_qty * y_qty - len(im_list))
            
    
    imgs = im_list[:x_qty * y_qty] if len(im_list) > 1 else im_list * x_qty * y_qty
    if gap == 0 and len(set(map(lambda x: x.size, im_list))) == 1:
            
        # If images are same size, and gap = 0 then no background color is required
        arrs = []
        if is_column:
            for i in range(0, len(imgs), y_qty):
                arrs.append(reduce(lambda x, y: np.vstack((np.asarray(x), np.asarray(y))), imgs[i:i+y_qty]))        
        
            im = reduce(lambda x, y: np.hstack((x, y)), arrs)
        else:
            for i in range(0, len(imgs), x_qty):
                arrs.append(reduce(lambda x, y: np.hstack((np.asarray(x), np.asarray(y))), imgs[i:i+x_qty]))        
        
            im = reduce(lambda x, y: np.vstack((x, y)), arrs)    

    else:
        count = 0
        # create empty background
        im = np.zeros([y_qty * h + (y_qty -1) * gap, x_qty * w + (x_qty -1) * gap, 4], dtype=np.uint8)
        im[:] = bkcolor
        
        if is_column:
            for x in range(x_qty):
                for y in range(y_qty):
                    if count < len(imgs):
                        w1, h1 = imgs[count].size
                        im[y * h + y * gap:y* h + h1 + y * gap, x * w + x * gap:x * w + w1  + x * gap] = np.asarray(imgs[count] )
                        count = count + 1
                    else:   break
        else:
            for y in range(y_qty):
                for x in range(x_qty):            
                    if count < len(imgs):
                        w1, h1 = imgs[count].size
                        im[y * h + y * gap:y* h + h1 + y * gap, x * w + x * gap:x * w + w1 + x * gap] = np.asarray(imgs[count] )
                        count = count + 1
                    else:   break
    return Image.fromarray(im)

if __name__ == '__main__':
    files = [r'D:\windows\Desktop\DS-Operator\2_1.jpg', r'D:\windows\Desktop\DS-Operator\3_2.jpg', r'D:\windows\Desktop\DS-Operator\3_3.jpg',
             r'D:\windows\Desktop\DS-Operator\39_38.jpg', r'D:\windows\Desktop\DS-Operator\40-39.jpg', r'D:\windows\Desktop\DS-Operator\41_40.jpg'
             ]
    print len(files)
    im_list = [Image.open(i) for i in files]
    im = ImgSalon(2, 3, im_list, None, is_column = True)
    im.save(r'D:\windows\Desktop\DS-Operator\final_final.jpg', quality = 95)