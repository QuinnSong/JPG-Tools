from wand.image import Image
from StringIO import StringIO
im1 = Image(filename = "n:\\desktop\\preview-file.png")
im2 = Image( filename = "n:\\desktop\\png\\save.png")

#im1.composite_channel(channel = 'all_channels', image = im2, operator = 'overlay',left = 0, top = 0)
im1.watermark(im2, 0.5, 20, 20 )
#im1.save(filename = 'n:\\desktop\\png\\sample.png')
# http://docs.wand-py.org/en/latest/wand/image.html
# http://en.wikibooks.org/wiki/Python_Imaging_Library/Editing_Pixels
# http://bytes.com/topic/python/answers/22566-overlaying-transparent-images-pil
# http://stackoverflow.com/questions/2181292/using-the-image-point-method-in-pil-to-manipulate-pixel-data

#fil = StringIO()
#im1.save(fil)
#fil.write("n:\\desktop\\png\\fil_sample.png")
#import wx
#img = wx.ImageFromStream(StringIO(fil.getvalue()))
#from PIL import Image as pImage
#aaa = pImage.open(StringIO(fil.getvalue())).convert("RGBA")
#aaa.save("n:\\desktop\\png\\fil_sample.png")
im1.save(filename = "n:\\desktop\\png\\watermark.png")
