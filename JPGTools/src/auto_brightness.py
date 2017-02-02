from PIL import Image, ImageStat, ImageEnhance
import math, sys, os

# For images being compared
BRIGHTNESS_DIFF = 1.1

def brightness( im ):
    """ Evaluate brightness of a image"""
    stat = ImageStat.Stat(im.convert("RGB"))
    r,g,b = stat.rms
    return math.sqrt(0.241*(r**2) + 0.691 *(g**2) + 0.068*(b**2))

def equalize(im, target_br):
    """ Adjust brightness of source image to meet the target """
    source_br = brightness(im)
    bright = ImageEnhance.Brightness(im)
    
    if source_br > target_br: step = -0.001
    else: step = 0.001
    
    return adjust (im, target_br, step)

def adjust (im, target_br, step):
    """ The loop to adjust brightness """
    f = 1
    
    while abs(brightness(im) - target_br) > BRIGHTNESS_DIFF:
        diff_tuple = (im, abs(brightness(im) - target_br))
        bright = ImageEnhance.Brightness(im)
        f += step        
        im =  bright.enhance(f)
        if diff_tuple[1] >= abs(brightness(im) - target_br):
            diff_tuple = im, abs(brightness(im) - target_br)
        else: break
    return im
#
#if __name__ == '__main__':
#    target_img = sys.argv[1]
#    src_img = sys.argv[2]
#    target = Image.open(sys.argv[1])
#    im = Image.open(sys.argv[2])
#    target_bright = brightness(target)
#    im = equalize(im, target_bright)
#    src_auto = os.path.splitext(src_img)[0] + '_auto' + os.path.splitext(src_img)[1]
#    im.save(src_auto)
