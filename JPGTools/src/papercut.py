#-*- coding: cp936 -*-

from PIL import Image

from utils import Img2bin_arr, bin_arr2Img


def paper_cut(img, threshold, bg_color, fg_color):
    '''
    @效果：剪纸
    @param img: instance of Image
    @param threshold: 大小范围[0, 255]
    @param bg_color: 背景色，元组类型，格式：(L)（灰度）,(R, G, B)，或者(R, G, B, A)
    @param fg_color: 前景色
    @return: instance of Image
    '''
    matrix = Img2bin_arr(img, threshold) # 位图转化为二维二值数组
    return bin_arr2Img(matrix, bg_color, fg_color) # 二维二值数组转化为位图