# -*- coding: cp936 -*- 

from wordcloud import (WordCloud, get_single_color_func, STOPWORDS)
#import imageio
import jieba
import io
from PIL import Image
import numpy
from random import Random
import colorsys

def get_single_color_func((color, wc_enable_random_color)):
    old_r, old_g, old_b, old_a = color
    enable_random_color = wc_enable_random_color
    
    rgb_max = 255
    h, s, v = colorsys.rgb_to_hsv(old_r / rgb_max,
                                  old_g / rgb_max,
                                  old_b / rgb_max)
    
    def single_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
        """ Random color generation
            random_state : random.Random object or None, (default=None)
            If a random object is given, this is used for generating random
            numbers.
        """
        if random_state is None:
            random_state = Random()
        #h = 0
        #s = 100
        #l = int(50 * (float(random_state.randint(1, 255))/100.0))
        if enable_random_color:
            r, g, b = colorsys.hsv_to_rgb(h, s, random_state.uniform(0.2, 1))
        else:
            r, g, b = colorsys.hsv_to_rgb(h, s, v)

        #return 'hsl({},{}%, {}%)'.format(int(h), int(s), l)
        return 'rgb({:.0f}, {:.0f}, {:.0f})'.format(r * rgb_max,
                                                    g * rgb_max,
                                                    b * rgb_max)
    
    return single_color_func
    
    
def generate_word_cloud(words, font_path, font_color, bg_color, custom_stopwords, mask, allow_numbers = True, scale = 4, repeat = False):
    # use imageio to generate mask [optional]
    # mask = imageio.imread(image_file)
    # mask = numpy.array(Image.open(image_file).convert('RGBA'))
    sw = set(STOPWORDS)
    [ sw.add(i) for i in custom_stopwords ]
    word_cloud = WordCloud(
                           #width = 400,
                           #height = 200,
                           # Larger canvases takes longer. If a large word cloud, try
                           # a lower canvas size and set the scale parameter.
                           font_path= font_path, # example: 'c:/windows/Fonts/simhei.ttf'
                           max_words = 2000,
                           max_font_size = 100,
                           color_func = get_single_color_func(font_color) if font_color else None, # can userandom_red_color_func [default is None]
                           background_color = bg_color, #'example: rgba(191,191,191,255)', 'white'[default is None]
                           stopwords = sw,
                           mask = mask,
                           repeat = repeat,
                           include_numbers = allow_numbers,
                           mode = 'RGBA',
                           scale = scale).generate(words)
    im = word_cloud.to_image()
    #im.show()
    #im.save(saved_name)
    #word_cloud.to_file(saved_name)
    return im
    
if __name__ == '__main__':
    words = 'Paris, France, Houston, Italy, America, Roma, \
    Austin, Seattle, Miami, London, Boston, Beijing, Shanghai, Macau, \
    Moscow, Venice, Germany, Australia, Netherlands, Detroit'
    
    words = u'北京, 西安, 上海, 广州, 大连, 重庆, 天津, 济南, 长沙, 郑州, 唐山, 无锡, 张家口, \
            青岛, 保定, 太原, 丹东, 吉林, 哈尔滨, 南京, 杭州, 合肥, 武汉, 海口, 成都, 昆明, 西宁'
    
    words = ' '.join(jieba.cut(words))
    
    #generate_word_cloud(words, 'heart.png', 'word_cloud.png')
    mask = numpy.array(Image.open('alice_mask.png').convert('RGBA'))
    generate_word_cloud(words, 'c:/windows/Fonts/simhei.ttf', None, None, [], mask)#, 'word_cloud.png')
    #generate_word_cloud(words, 'alice_mask.png', 'word_cloud.png')
    import matplotlib.font_manager as fontman
    font_list = fontman.findSystemFonts()
    with open(u'wiki.txt') as words_file:
        content = words_file.read()
        import re
        re.findall(r"\w[\w']+", content)