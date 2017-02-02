#-*- coding: cp936 -*-

from PIL import Image

from utils import Img2bin_arr, bin_arr2Img


def paper_cut(img, threshold, bg_color, fg_color):
    '''
    @Ч������ֽ
    @param img: instance of Image
    @param threshold: ��С��Χ[0, 255]
    @param bg_color: ����ɫ��Ԫ�����ͣ���ʽ��(L)���Ҷȣ�,(R, G, B)������(R, G, B, A)
    @param fg_color: ǰ��ɫ
    @return: instance of Image
    '''
    matrix = Img2bin_arr(img, threshold) # λͼת��Ϊ��ά��ֵ����
    return bin_arr2Img(matrix, bg_color, fg_color) # ��ά��ֵ����ת��Ϊλͼ