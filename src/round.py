# -*- coding: utf-8 -*-

# Modified based on Phatch
#---PIL modules import
from PIL import Image, ImageChops, ImageDraw
from shadow import has_alpha, paste
import math

# Declare constants here
ROUNDED = 'Rounded'
CORNER_ID = 'rounded_corner_r%d_f%d'
ROUNDED_POS = (ROUNDED, ROUNDED, ROUNDED, ROUNDED)
ROUNDED_RECTANGLE_ID = 'rounded_rectangle_r%d_f%d_s%s_p%s'


def round_image(image, cache={}, radius = 5, pos=ROUNDED_POS, back_color='#FFFFFF'):
    # 计算圆角半径
    radius = (min(image.size) * radius)/100
    
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    pos = 4 * (ROUNDED, )

    mask = create_rounded_rectangle(image.size, cache, radius, pos)

    paste(image, Image.new('RGB', image.size, back_color), (0, 0),
        ImageChops.invert(mask))
    image.putalpha(mask)
    return image

def create_rounded_rectangle(size=(600, 400), cache={}, radius=100, pos=ROUNDED_POS):
    #rounded_rectangle
    im_x, im_y = size
    rounded_rectangle_id = ROUNDED_RECTANGLE_ID % (radius, 255, size, pos)
    if rounded_rectangle_id in cache:
        return cache[rounded_rectangle_id]
    else:
        #cross
        cross_id = ROUNDED_RECTANGLE_ID % (radius, 255, size, ROUNDED_POS)
        if cross_id in cache:
            cross = cache[cross_id]
        else:
            cross = cache[cross_id] = Image.new('L', size, 0)
            draw = ImageDraw.Draw(cross)
            draw.rectangle((radius, 0, im_x - radius, im_y), fill=255)
            draw.rectangle((0, radius, im_x, im_y - radius), fill=255)
        #corner
        corner_id = CORNER_ID % (radius, 255)
        if corner_id in cache:
            corner = cache[corner_id]
        else:
            corner = cache[corner_id] = create_corner(radius, 4) #255)
        #rounded rectangle
        rectangle = Image.new('L', (radius, radius), 255)
        rounded_rectangle = cross.copy()
        for index, angle in enumerate(pos):
            if angle == ROUNDED:
                element = corner
            else:
                element = rectangle
            if index % 2:
                x = im_x - radius
                element = element.transpose(Image.FLIP_LEFT_RIGHT)
            else:
                x = 0
            if index < 2:
                y = 0
            else:
                y = im_y - radius
                element = element.transpose(Image.FLIP_TOP_BOTTOM)
            paste(rounded_rectangle, element, (x, y))
        cache[rounded_rectangle_id] = rounded_rectangle
        return rounded_rectangle

def create_corner(radius=100, factor=2):
    corner = Image.new('L', (factor * radius, factor * radius), 0)
    draw = ImageDraw.Draw(corner)
    draw.pieslice((0, 0, 2 * factor * radius, 2 * factor * radius),
        180, 270, fill=255)
    corner = corner.resize((radius, radius), Image.ANTIALIAS)
    return corner

#def paste(destination, source, box=(0, 0), mask=None, force=False):
#    """"Pastes the source image into the destination image while using an
#    alpha channel if available.
#
#    :param destination: destination image
#    :type destination:  PIL image object
#    :param source: source image
#    :type source: PIL image object
#    :param box:
#
#        The box argument is either a 2-tuple giving the upper left corner,
#        a 4-tuple defining the left, upper, right, and lower pixel coordinate,
#        or None (same as (0, 0)). If a 4-tuple is given, the size of the
#        pasted image must match the size of the region.
#
#    :type box: tuple
#    :param mask: mask or None
#
#    :type mask: bool or PIL image object
#    :param force:
#
#        With mask: Force the invert alpha paste or not.
#
#        Without mask:
#
#        - If ``True`` it will overwrite the alpha channel of the destination
#          with the alpha channel of the source image. So in that case the
#          pixels of the destination layer will be abandonned and replaced
#          by exactly the same pictures of the destination image. This is mostly
#          what you need if you paste on a transparant canvas.
#        - If ``False`` this will use a mask when the image has an alpha
#          channel. In this case pixels of the destination image will appear
#          through where the source image is transparent.
#
#    :type force: bool
#    """
#    # Paste on top
#    if source == mask:
#        if has_alpha(source):
#            # invert_alpha = the transparant pixels of the destination
#            if has_alpha(destination) and (destination.size == source.size
#                    or force):
#                invert_alpha = ImageOps.invert(get_alpha(destination))
#                if invert_alpha.size != source.size:
#                    # if sizes are not the same be careful!
#                    # check the results visually
#                    if len(box) == 2:
#                        w, h = source.size
#                        box = (box[0], box[1], box[0] + w, box[1] + h)
#                    invert_alpha = invert_alpha.crop(box)
#            else:
#                invert_alpha = None
#            # we don't want composite of the two alpha channels
#            source_without_alpha = remove_alpha(source)
#            # paste on top of the opaque destination pixels
#            destination.paste(source_without_alpha, box, source)
#            if invert_alpha != None:
#                # the alpha channel is ok now, so save it
#                destination_alpha = get_alpha(destination)
#                # paste on top of the transparant destination pixels
#                # the transparant pixels of the destination should
#                # be filled with the color information from the source
#                destination.paste(source_without_alpha, box, invert_alpha)
#                # restore the correct alpha channel
#                destination.putalpha(destination_alpha)
#        else:
#            destination.paste(source, box)
#    elif mask:
#        destination.paste(source, box, mask)
#    else:
#        destination.paste(source, box)
#        if force and has_alpha(source):
#            destination_alpha = get_alpha(destination)
#            source_alpha = get_alpha(source)
#            destination_alpha.paste(source_alpha, box)
#            destination.putalpha(destination_alpha)