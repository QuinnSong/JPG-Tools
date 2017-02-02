# Modified based on Phatch

#---PIL modules import
from shadow import has_transparency, has_alpha, get_alpha, \
    convert_safe_mode, paste
from PIL import Image, ImageDraw
import math

OPTIONS = ['Equal for all sides', 'Different for each side']

def border(image, method, border_width=0, left=0, right=0, top=0, bottom=0,
        color=0, opacity=100):
    """

    """
    #set up sizes, and make the target img
    if method == OPTIONS[0]:
        left, right, top, bottom = (border_width, ) * 4
    else:
        left, right, top, bottom = [x for x in left, right, top, bottom]

    #new image size attributes could get really messed up by negatives...
    new_width = sum([x for x in image.size[0], left, right if x >= 0])
    new_height = sum([x for x in image.size[1], top, bottom if x >= 0])

    # only need to do conversions when preserving transparency, or when
    # dealing with transparent overlays
    negative = [x for x in left, right, top, bottom if x < 0]
    if (negative and (opacity < 100)) or has_transparency(image):
        new_image = Image.new('RGBA', (new_width, new_height), color)
    else:
        new_image = Image.new('RGB', (new_width, new_height), color)

    # now for the masking component. The size of the mask needs to be the size
    # of the original image, and totally opaque. then we will have draw in
    # negative border values with an opacity scaled appropriately.
    # NOTE: the technique here is that rotating the image allows me to do
    # this with one simple draw operation, no need to add and subtract and
    # otherwise introduce geometry errors
    if negative:
        #draw transparent overlays
        mask = Image.new('L', image.size, 255)
        drawcolor = int(255 - (opacity / 100.0 * 255))
        for val in left, top, right, bottom:
            if val < 0:
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.rectangle((0, 0, abs(val), max(mask.size)),
                    drawcolor)
                del mask_draw
            mask = mask.rotate(90)
    else:
        mask = None

    # negative paste position values mess with the result.
    left = max(left, 0)
    top = max(top, 0)
    paste(new_image, image, (left, top), mask)

    return new_image