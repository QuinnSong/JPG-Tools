# Modified based on Phatch

#---PIL modules import
from shadow import fill_background_color, generate_layer, \
    remove_alpha, has_transparency, get_alpha, paste
from PIL import Image
#from reflection import HTMLColorToRGBA

FILL_CHOICES = ('Color', 'Image')

def background(image, fill, mark, color,
        horizontal_offset=None, vertical_offset=None,
        horizontal_justification=None, vertical_justification=None,
        orientation=None, method=None, opacity=100):
    """color is RGB"""
    if not has_transparency(image):
        return image
    if image.mode == 'P':
        image = image.convert('RGBA')
    if fill == FILL_CHOICES[0]:
        opacity = (255 * opacity) / 100
        r,g,b = color
        return fill_background_color(image, (r,g,b, opacity))
    elif fill == FILL_CHOICES[1]:
        layer = generate_layer(image.size, mark, method,
                               horizontal_offset, vertical_offset,
                               horizontal_justification,
                               vertical_justification,
                               orientation, opacity)
        paste(layer, image, mask=image)
        return layer