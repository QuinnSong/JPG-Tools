#-*- coding: cp936 -*-

from PIL import Image, ImageOps, ImageStat
from border import border, OPTIONS
import random, os
import cPickle as p
from shadow import drop_shadow
from border import border
from glob import glob
import operator

PIC_LIST = ['.JPG', '.JPEG', '.BMP', '.TIF', 'TIFF', '.GIF', '.PNG']

def mosaic (bgimg, path, n, scale, iteration):
    """
    bgimg: background image, large enough
    """
    # 0. mosaic needs a large image as background
    im_bg = Image.open(bgimg)
    # 2. get a dict for path
    try:
        with open('dic.txt', 'r') as f: dic = p.load(f)
    except:
        dic = tile_dict(path)
        with open('dic.txt', 'wb') as f: p.dump(dic, f)
        
    # 3. thumbnail the big image to compare (n for zoom out; scale for zoom in)
    bg_scale_size = im_bg.size[0] * scale, im_bg.size[1] * scale
    im_chao = Image.new ("RGB", bg_scale_size, 'white')
    tile_size = thumb_background(im_bg, n)
    #print "total tiles: ", tile_size
    #print "total iteration", iteration
    for i in xrange(iteration):
        print i + 1
        # 4. get a list of small images
        im_tiles = get_image_list(im_bg, dic)
        # 5. paste in chaos style
        #print "generate final image"
        #print "im_tiles", im_tiles
        #print "tile_size", tile_size
        im_chao = paste_chaos(im_chao, im_tiles, tile_size )
    return im_chao
        
def find_similiar(lst, dic):
    """ return the top 10 filenames from the dic, which have close RGB values as lst"""
    #print dic
    similiar_map = {}
    for k, v in dic.items():
        similiar_map[reduce(operator.add, map(lambda (a,b): (a-b)**2, zip(lst, v)))] = k
    #map(lambda (k,v): similiar_map[reduce(operator.add, map(lambda a,b: (a-b)**2, zip(lst, v)))] = k, dic.items())
    return sorted(similiar_map.items(), key = lambda x : x[0])[:10]

def get_image_list (im, dic):
    """
    receive a thumbnail image and a dict of images for mosaic, return filenames list as tiles
    """
    im.thumbnail((im.size[0]/10, im.size[1]/10), Image.ANTIALIAS)
    lst = im.getdata()
    print len(lst), "len lst"
    #tiles = []
    tiles = [find_similiar(i, dic)[random.randrange(len(dic) -1)][1] for i in lst]
    return tiles
    
def thumb_background (im, scale):
    """
    thumbnail background image size
    """
    newsize = im.size[0]/scale, im.size[1]/scale
    im.thumbnail(newsize, Image.ANTIALIAS)
    return im.size
    
def avg_img (im):
    """
    # return average R, G, B for Image object
    """
    im = im.convert("RGB")
    color_vector = [int(x) for x in ImageStat.Stat(im).mean]
    return color_vector
    
def tile_dict (path):
    """
    #Return list of average RGB for images in path as dict.
    """
    img_dict = {}
    jpglist = glob(os.path.join(path, "*.jpg"))
    filenames = [ f for f in jpglist if os.path.splitext(f)[1].upper() in PIC_LIST]
    for image in filenames:
        try: im = Image.open(image)
        except: continue
        img_dict [ image ] = avg_image (im)
    return img_dict

def avg_image (im):
    """ Return average r,g,b for image"""
    return [int(x) for x in ImageStat.Stat(im).mean]

def rotate_image (image, degree):
    """ expand to show all"""
    image = image.convert('RGBA')
    return image.rotate(degree, expand = 1)

def paste_chaos(image, tiles, size, shadow_offset = (5, 5)):
    """
    size for thumbnail size which is how many titles per line and row
    """
    if len(tiles) > 0:
        len_tiles = range(len(tiles))
        random.shuffle(len_tiles)
        tile_size = (image.size[0]/size[0], image.size[1]/size[1])
        print len_tiles
        #print tile_size, "size tile"
        for i in len_tiles:
            print i, "i"
            im = Image.open(tiles[i])
            degree = random.randint(-20, 20)
            try:
                im = border(im, OPTIONS[0], border_width = 5, color= (189,189,189), opacity = 80)
                im_shadow = drop_shadow(im, horizontal_offset = 10, vertical_offset = 10)
                im_rotate = rotate_image(im_shadow, degree)
                im_rotate.thumbnail(size, Image.ANTIALIAS)
                
                x = i % size[0] * tile_size[0] + random.randrange(-tile_size[0] / 2, tile_size[0] / 2)
                y = i % size[0] * tile_size[1] + random.randrange(-tile_size[1] / 2, tile_size[1] / 2)
                x, y = sorted( [0, x, abs(size[0] - tile_size[0])])[1], sorted( [0, x, abs(size[1] - tile_size[1])])[1]
                
                image.paste(im_rotate, (x, y), im_rotate)
            except: continue
    return image

bgimg =  r"D:\windows\Desktop\20140630\20140921 src\20140910 src\PIC\Beautiful-Wallpapers-14.jpg"
path = r"D:\windows\Desktop\20140630\20140921 src\20140910 src\PIC"
m_im = mosaic (bgimg, path, 15, 1, 2)
m_im.save("d:\\\windows\\desktop\\final.jpg")
    