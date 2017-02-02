#-*- coding: cp936 -*-
# Modified based on Phatch

#---PIL modules import
from PIL import Image, ImageChops, ImageFilter, ImageEnhance, ImageOps

def has_transparency(image):
    """Checks if the image has transparency.
    The image has an alpha band or a P mode with transparency.

    :param image: the image to check
    :type image: PIL image object
    :returns: True or False
    :rtype: boolean
    """
    return (image.mode == 'P' and 'transparency' in image.info) or\
            has_alpha(image)
        
def has_alpha(image):
    """Checks if the image has an alpha band.
    i.e. the image mode is either RGBA or LA.
    The transparency in the P mode doesn't count as an alpha band

    :param image: the image to check
    :type image: PIL image object
    :returns: True or False
    :rtype: boolean
    """
    return image.mode.endswith('A')

def put_alpha(image, alpha):
    """Copies the given band to the alpha layer of the given image.

    :param image: input image
    :type image: PIL image object
    :param alpha: the alpha band to copy
    :type alpha: single band image object
    """
    if image.mode in ['CMYK', 'YCbCr', 'P']:
        image = image.convert('RGBA')
    elif image.mode in ['1', 'F']:
        image = image.convert('RGBA')
    image.putalpha(alpha)

def remove_alpha(image):
    """Returns a copy of the image after removing the alpha band or
    transparency

    :param image: input image
    :type image: PIL image object
    :returns: the input image after removing the alpha band or transparency
    :rtype: PIL image object
    """
    if image.mode == 'RGBA':
        return image.convert('RGB')
    if image.mode == 'LA':
        return image.convert('L')
    if image.mode == 'P' and 'transparency' in image.info:
        img = image.convert('RGB')
        del img.info['transparency']
        return img
    return image

def get_alpha(image):
    """Gets the image alpha band. Can handles P mode images with transpareny.
    Returns a band with all values set to 255 if no alpha band exists.

    :param image: input image
    :type image: PIL image object
    :returns: alpha as a band
    :rtype: single band image object
    """
    if has_alpha(image):
        return image.split()[-1]
    if image.mode == 'P' and 'transparency' in image.info:
        return image.convert('RGBA').split()[-1]
    # No alpha layer, create one.
    return Image.new('L', image.size, 255)

def fill_background_color(image, color):
    """Fills given image with background color.

    :param image: source image
    :type image: pil.Image
    :param color: background color
    :type color: tuple of int
    :returns: filled image
    :rtype: pil.Image
    """
    if image.mode == 'LA':
        image = image.convert('RGBA')
    elif image.mode != 'RGBA' and\
        not (image.mode == 'P' and 'transparency' in image.info):
        return image
    if len(color) == 4 and color[-1] != 255:
        mode = 'RGBA'
    else:
        mode = 'RGB'
    back = Image.new(mode, image.size, color)
    if (image.mode == 'P' and mode == 'RGBA'):
        image = image.convert('RGBA')
    if has_alpha(image):
        paste(back, image, mask=image)
    elif image.mode == 'P':
        palette = image.getpalette()
        index = image.info['transparency']
        palette[index * 3: index * 3 + 3] = color[:3]
        image.putpalette(palette)
        del image.info['transparency']
        back = image
    else:
        paste(back, image)
    return back

def generate_layer(image_size, mark, method,
        horizontal_offset, vertical_offset,
        horizontal_justification, vertical_justification,
        orientation, opacity):
    """Generate new layer for backgrounds or watermarks on which a given
    image ``mark`` can be positioned, scaled or repeated.

    :param image_size: size of the reference image
    :type image_size: tuple of int
    :param mark: image mark
    :type mark: pil.Image
    :param method: ``'Tile'``, ``'Scale'``, ``'By Offset'``
    :type method: string
    :param horizontal_offset: horizontal offset
    :type horizontal_offset: int
    :param vertical_offset: vertical offset
    :type vertical_offset: int
    :param horizontal_justification: ``'Left'``, ``'Middle'``, ``'Right'``
    :type horizontal_justification: string
    :param vertical_justification: ``'Top'``, ``'Middle'``, ``'Bottom'``
    :type vertical_justification: string
    :param orientation: mark orientation (e.g. ``'ROTATE_270'``)
    :type orientation: string
    :param opacity: opacity within ``[0, 1]``
    :type opacity: float
    :returns: generated layer
    :rtype: pil.Image

    .. see also:: :func:`reduce_opacity`
    """

    mark = convert_safe_mode(open_image(mark))
    opacity /= 100.0
    mark = reduce_opacity(mark, opacity)
    layer = Image.new('RGBA', image_size, (0, 0, 0, 0))
    if method == u'平铺':
        for y in range(0, image_size[1], mark.size[1]):
            for x in range(0, image_size[0], mark.size[0]):
                paste(layer, mark, (x, y))
    elif method == u'比例':
        # scale, but preserve the aspect ratio
        ratio = min(float(image_size[0]) / mark.size[0],
            float(image_size[1]) / mark.size[1])
        w = int(mark.size[0] * ratio)
        h = int(mark.size[1] * ratio)
        mark = mark.resize((w, h))
        paste(layer, mark, ((image_size[0] - w) / 2,
            (image_size[1] - h) / 2))
    elif method == u'偏移':
        location = calculate_location(
            horizontal_offset, vertical_offset,
            horizontal_justification, vertical_justification,
            image_size, mark.size)
        #if orientation:
        #    orientation_value = getattr(Image, orientation)
        #    mark = mark.transpose(orientation_value)
        paste(layer, mark, location, force=True)
    else:
        raise ValueError('Unknown method "%s" for generate_layer.' % method)
    return layer

def open_image(uri):
    """Open local files or remote files over http.

    :param uri: image location
    :type uri: string
    :returns: image
    :rtype: pil.Image
    """
    #if system.is_www_file(uri):
    #    try:
    #        return WWW_CACHE[uri]
    #    except KeyError:
    #        f = urlopen(uri)
    #        im = WWW_CACHE[uri] = open_image_data(f.read())
    #        return im
    if uri[:7] == 'file://':
        uri = uri[7:]
    return Image.open(uri)

def calculate_location(horizontal_offset, vertical_offset,
        horizontal_justification, vertical_justification,
        canvas_size, image_size):
    """Calculate location based on offset and justification. Offsets
    can be positive and negative.

    :param horizontal_offset: horizontal offset
    :type horizontal_offset: int
    :param vertical_offset: vertical offset
    :type vertical_offset: int
    :param horizontal_justification: ``'Left'``, ``'Middle'``, ``'Right'``
    :type horizontal_justification: string
    :param vertical_justification: ``'Top'``, ``'Middle'``, ``'Bottom'``
    :type vertical_justification: string
    :param canvas_size: size of the total canvas
    :type canvas_size: tuple of int
    :param image_size: size of the image/text which needs to be placed
    :type image_size: tuple of int
    :returns: location
    :rtype: tuple of int

    .. see also:: :func:`generate layer`

    >>> calculate_location(50, 50, 'Left', 'Middle', (100,100), (10,10))
    (50, 45)
    """
    canvas_width, canvas_height = canvas_size
    image_width, image_height = image_size

    # check offsets
    if horizontal_offset < 0:
        horizontal_offset += canvas_width
    if vertical_offset < 0:
        vertical_offset += canvas_height

    # check justifications
    if horizontal_justification == u'左':
        horizontal_delta = 0
    elif horizontal_justification == u'中':
        horizontal_delta = -image_width / 2
    elif horizontal_justification == u'右':
        horizontal_delta = -image_width

    if vertical_justification == u'上':
        vertical_delta = 0
    elif vertical_justification == u'中':
        vertical_delta = -image_height / 2
    elif vertical_justification == u'下':
        vertical_delta = -image_height

    return horizontal_offset + horizontal_delta, \
        vertical_offset + vertical_delta

def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity if opacity is
    within ``[0, 1]``.

    :param im: source image
    :type im: pil.Image
    :param opacity: opacity within ``[0, 1]``
    :type opacity: float
    :returns im: image
    :rtype: pil.Image

    >>> im = Image.new('RGBA', (1, 1), (255, 255, 255))
    >>> im = reduce_opacity(im, 0.5)
    >>> im.getpixel((0,0))
    (255, 255, 255, 127)
    """
    if opacity < 0 or opacity > 1:
        return im
    alpha = get_alpha(im)
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    put_alpha(im, alpha)
    return im

def convert_safe_mode(image):
    """Converts image into a processing-safe mode.

    :param image: input image
    :type image: PIL image object
    :returns: the converted image
    :rtype: PIL image object
    """
    if image.mode in ['1', 'F']:
        return image.convert('L')
    if image.mode == 'P' and 'transparency' in image.info:
        img = image.convert('RGBA')
        del img.info['transparency']
        return img
    if image.mode in ['P', 'YCbCr', 'CMYK', 'RGBX']:
        return image.convert('RGB')
    return image

def drop_shadow(image, horizontal_offset=5, vertical_offset=5,
        background_color=(255, 255, 255, 0), shadow_color=0x444444,
        border=8, shadow_blur=3, force_background_color=False, cache=None):
    """Add a gaussian blur drop shadow to an image.

    :param image: The image to overlay on top of the shadow.
    :param type: PIL Image
    :param offset:

        Offset of the shadow from the image as an (x,y) tuple.
        Can be positive or negative.

    :type offset: tuple of integers
    :param background_color: Background color behind the image.
    :param shadow_color: Shadow color (darkness).
    :param border:

        Width of the border around the image.  This must be wide
        enough to account for the blurring of the shadow.

    :param shadow_blur:

        Number of times to apply the filter.  More shadow_blur
        produce a more blurred shadow, but increase processing time.
    """
    if cache is None:
        cache = {}

    if has_transparency(image) and image.mode != 'RGBA':
        # Make sure 'LA' and 'P' with trasparency are handled
        image = image.convert('RGBA')

    #get info
    size = image.size
    mode = image.mode

    back = None

    #assert image is RGBA
    if mode != 'RGBA':
        if mode != 'RGB':
            image = image.convert('RGB')
            mode = 'RGB'
        #create cache id
        id = ''.join([str(x) for x in ['shadow_', size,
            horizontal_offset, vertical_offset, border, shadow_blur,
            background_color, shadow_color]])

        #look up in cache
        if id in cache:
            #retrieve from cache
            back, back_size = cache[id]

    if back is None:
        #size of backdrop
        back_size = (size[0] + abs(horizontal_offset) + 2 * border,
                        size[1] + abs(vertical_offset) + 2 * border)

        #create shadow mask
        if mode == 'RGBA':
            image_mask = get_alpha(image)
            shadow = Image.new('L', back_size, 0)
        else:
            image_mask = Image.new(mode, size, shadow_color)
            shadow = Image.new(mode, back_size, background_color)

        shadow_left = border + max(horizontal_offset, 0)
        shadow_top = border + max(vertical_offset, 0)
        paste(shadow, image_mask, (shadow_left, shadow_top,
                                shadow_left + size[0], shadow_top + size[1]))
        del image_mask  # free up memory

        #blur shadow mask

        #Apply the filter to blur the edges of the shadow.  Since a small
        #kernel is used, the filter must be applied repeatedly to get a decent
        #blur.
        n = 0
        while n < shadow_blur:
            shadow = shadow.filter(ImageFilter.BLUR)
            n += 1

        #create back
        if mode == 'RGBA':
            back = Image.new('RGBA', back_size, shadow_color)
            back.putalpha(shadow)
            del shadow  # free up memory
        else:
            back = shadow
            cache[id] = back, back_size

    #Paste the input image onto the shadow backdrop
    image_left = border - min(horizontal_offset, 0)
    image_top = border - min(vertical_offset, 0)
    if mode == 'RGBA':
        paste(back, image, (image_left, image_top), image)
        if force_background_color:
            mask = get_alpha(back)
            paste(back, Image.new('RGB', back.size, background_color),
                (0, 0), ImageChops.invert(mask))
            back.putalpha(mask)
    else:
        paste(back, image, (image_left, image_top))

    return back

def paste(destination, source, box=(0, 0), mask=None, force=False):
    """"Pastes the source image into the destination image while using an
    alpha channel if available.

    :param destination: destination image
    :type destination:  PIL image object
    :param source: source image
    :type source: PIL image object
    :param box:

        The box argument is either a 2-tuple giving the upper left corner,
        a 4-tuple defining the left, upper, right, and lower pixel coordinate,
        or None (same as (0, 0)). If a 4-tuple is given, the size of the
        pasted image must match the size of the region.

    :type box: tuple
    :param mask: mask or None

    :type mask: bool or PIL image object
    :param force:

        With mask: Force the invert alpha paste or not.

        Without mask:

        - If ``True`` it will overwrite the alpha channel of the destination
          with the alpha channel of the source image. So in that case the
          pixels of the destination layer will be abandonned and replaced
          by exactly the same pictures of the destination image. This is mostly
          what you need if you paste on a transparant canvas.
        - If ``False`` this will use a mask when the image has an alpha
          channel. In this case pixels of the destination image will appear
          through where the source image is transparent.

    :type force: bool
    """
    # Paste on top
    if source == mask:
        if has_alpha(source):
            # invert_alpha = the transparant pixels of the destination
            if has_alpha(destination) and (destination.size == source.size
                    or force):
                invert_alpha = ImageOps.invert(get_alpha(destination))
                if invert_alpha.size != source.size:
                    # if sizes are not the same be careful!
                    # check the results visually
                    if len(box) == 2:
                        w, h = source.size
                        box = (box[0], box[1], box[0] + w, box[1] + h)
                    invert_alpha = invert_alpha.crop(box)
            else:
                invert_alpha = None
            # we don't want composite of the two alpha channels
            source_without_alpha = remove_alpha(source)
            # paste on top of the opaque destination pixels
            destination.paste(source_without_alpha, box, source)
            if invert_alpha != None:
                # the alpha channel is ok now, so save it
                destination_alpha = get_alpha(destination)
                # paste on top of the transparant destination pixels
                # the transparant pixels of the destination should
                # be filled with the color information from the source
                destination.paste(source_without_alpha, box, invert_alpha)
                # restore the correct alpha channel
                destination.putalpha(destination_alpha)
        else:
            destination.paste(source, box)
    elif mask:
        destination.paste(source, box, mask)
    else:
        destination.paste(source, box)
        if force and has_alpha(source):
            destination_alpha = get_alpha(destination)
            source_alpha = get_alpha(source)
            destination_alpha.paste(source_alpha, box)
            destination.putalpha(destination_alpha)
            
def blend(im1, im2, amount, color=None):
    """Blend two images with each other. If the images differ in size
    the color will be used for undefined pixels.

    :param im1: first image
    :type im1: pil.Image
    :param im2: second image
    :type im2: pil.Image
    :param amount: amount of blending
    :type amount: int
    :param color: color of undefined pixels
    :type color: tuple
    :returns: blended image
    :rtype: pil.Image
    """
    im2 = convert_safe_mode(im2)
    if im1.size == im2.size:
        im1 = convert(im1, im2.mode)
    else:
        if color is None:
            expanded = Image.new(im2.mode, im2.size)
        elif im2.mode in ('1', 'L') and type(color) != int:
            expanded = Image.new(im2.mode, im2.size, color[0])
        else:
            expanded = Image.new(im2.mode, im2.size, color)
        im1 = im1.convert(expanded.mode)
        we, he = expanded.size
        wi, hi = im1.size
        paste(expanded, im1, ((we - wi) / 2, (he - hi) / 2),
            im1.convert('RGBA'))
        im1 = expanded
    return Image.blend(im1, im2, amount)
    
def invert(image, amount=100):
    image = convert_safe_mode(image)
    inverted = ImageChops.invert(image)
    if amount < 100:
        inverted = blend(image, inverted, amount / 100.0)
    if has_alpha(image):
        inverted.putalpha(get_alpha(image))
    return inverted

def convert(image, mode, *args, **keyw):
    """Returns a converted copy of an image

    :param image: input image
    :type image: PIL image object
    :param mode: the new mode
    :type mode: string
    :param args: extra options
    :type args: tuple of values
    :param keyw: extra keyword options
    :type keyw: dictionary of options
    :returns: the converted image
    :rtype: PIL image object
    """
    if mode == 'P':
        if image.mode == 'P':
            return image
        if image.mode in ['1', 'F']:
            return image.convert('L').convert(mode, *args, **keyw)
        if image.mode in ['RGBA', 'LA']:
            alpha = get_alpha(image)
            output = image.convert('RGB').convert(
                mode, colors=255, *args, **keyw)
            paste(output,
                255, alpha.point(COLOR_MAP))
            output.info['transparency'] = 255
            return output
        return image.convert('RGB').convert(mode, *args, **keyw)
    if image.mode == 'P' and mode == 'LA':
        # A workaround for a PIL bug.
        # Converting from P to LA directly doesn't work.
        return image.convert('RGBA').convert('LA', *args, **keyw)
    if has_transparency(image) and (not mode in ['RGBA', 'LA']):
        if image.mode == 'P':
            image = image.convert('RGBA')
            del image.info['transparency']
        #image = fill_background_color(image, (255, 255, 255, 255))
        image = image.convert(mode, *args, **keyw)
        return image
    return image.convert(mode, *args, **keyw)