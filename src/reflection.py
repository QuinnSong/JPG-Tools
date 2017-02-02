# Modified based on Phatch

#---PIL modules import
from round import paste
from shadow import has_transparency, has_alpha
from PIL import Image, ImageColor, ImageFilter
#
#def HTMLColorToRGB(colorstring):
#    """ convert #RRGGBB to an (R, G, B) tuple """
#    colorstring = colorstring.strip()
#    if colorstring[0] == '#':
#        colorstring = colorstring[1:]
#    if len(colorstring) != 6:
#        raise ValueError("input #%s is not in #RRGGBB format" % colorstring)
#    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
#    r, g, b = [int(n, 16) for n in (r, g, b)]
#    return (r, g, b)
#
#
#def HTMLColorToRGBA(colorstring, opacity):
#    r, g, b = HTMLColorToRGB(colorstring)
#    return (r, g, b, opacity)

REFLECT_ID = 'reflect_w%s_h%s_o%s'


def gradient_vector(size, opacity, cache):
    id = REFLECT_ID % (1, size, opacity)
    try:
        return cache[id]
    except KeyError:
        pass
    opacity = float(opacity)
    grad = Image.new('L', (1, size))
    data = [int(opacity * x / size) for x in range(size, 0, -1)]
    grad.putdata(data)
    cache[id] = grad
    return grad


def gradient_mask(size, opacity, cache):
    id = REFLECT_ID % (size[0], size[1], opacity)
    try:
        return cache[id]
    except KeyError:
        pass
    #gradient vector
    vector = gradient_vector(size[1], opacity, cache)
    #scale vector
    grad = cache[id] = vector.resize(size, Image.LINEAR)
    return grad


def reflect(image, depth, opacity, background_color, background_opacity,
        scale_method, gap=0, scale_reflection=False,
        blur_reflection=False, cache=None):
    if has_transparency(image):
        image = image.convert('RGBA')
    else:
        image = image.convert('RGB')
    if cache is None:
        cache = {}
    opacity = (255 * opacity) / 100
    background_opacity = (255 * background_opacity) / 100
    scale_method = getattr(Image, scale_method)
    r,g,b = background_color
    if background_opacity == 255:
        mode = 'RGB'
        color = (r, g, b)
    else:
        mode = 'RGBA'        
        color = (r, g, b, background_opacity)
        #color = HTMLColorToRGBA(background_color, background_opacity)
    width, height = image.size
    depth = min(height, depth)
    #make reflection
    if has_alpha(image) and background_opacity > 0:
        reflection = Image.new(mode, image.size, color)
        paste(reflection, image, (0, 0), image)
    else:
        reflection = image
    reflection = reflection.transpose(Image.FLIP_TOP_BOTTOM)
    if scale_reflection:
        reflection = reflection.resize((width, depth), scale_method)
    else:
        reflection = reflection.crop((0, 0, width, depth))
    if blur_reflection:
        reflection = reflection.filter(ImageFilter.BLUR)
    mask = gradient_mask((width, depth), opacity, cache)
    #composite
    total_size = (width, height + gap + depth)
    total = Image.new(mode, total_size, color)
    paste(total, image, (0, 0), image)
    paste(total, reflection, (0, height + gap), mask)
    return total