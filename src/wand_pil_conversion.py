from PIL import Image
from wand.image import Image as wImage
from wand.display import display
from StringIO import StringIO
from PIL.PngImagePlugin import PngImageFile
import iconfile

pin = iconfile.pinIcon.GetData()
wim = wImage(blob = pin)
display(wim)
im = Image.open("c:\p.png")
#help(im)
if isinstance(im, PngImageFile):
    print "pil instance"
fil = StringIO()
im.save(fil, 'PNG')
wim = wImage(blob = fil.getvalue())
help(wim)
if isinstance(wim, wImage):
    print "wim"
fil.close()
#display(wim)
fil2 = StringIO()
wim.save(fil2)
im2 = Image.open(StringIO(fil2.getvalue()))
im2.save("c:\\test2.png")

