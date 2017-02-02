#-*- coding: utf-8 -*-
# Phatch - Code

from PIL import Image
from shadow import paste, convert_safe_mode

#DIRECTIONS = [BOTH, HORIZONTAL, VERTICAL]

def tile(image, direction):
    """镜像效果"""
    if image.mode == 'P':
        image = convert_safe_mode(image)
    result = Image.new(image.mode, get_dimensions(image, direction))
    paste(result, image, (0, 0))

    if direction == u'两者皆选':
        x_mirror(image, result)
        y_mirror(image, result)
        xy_mirror(image, result)
    if direction == u'左右镜像':
        x_mirror(image, result)
    if direction == u'上下镜像':
        y_mirror(image, result)

    return result


def get_dimensions(image, direction):
    width, height = image.size
    x_scale, y_scale = get_scales(direction)
    return width * x_scale, height * y_scale


def get_scales(direction):
    x_scale, y_scale = 1, 1

    if direction == u'两者皆选':
        x_scale, y_scale = 2, 2
    if direction == u'左右镜像':
        x_scale = 2
    if direction == u'上下镜像':
        y_scale = 2

    return x_scale, y_scale


def x_mirror(image, result):
    width, height = image.size
    paste(result, image.transpose(Image.FLIP_LEFT_RIGHT), (width, 0))


def y_mirror(image, result):
    width, height = image.size
    paste(result, image.transpose(Image.FLIP_TOP_BOTTOM), (0, height))


def xy_mirror(image, result):
    paste(result, image.transpose(Image.ROTATE_180), image.size)