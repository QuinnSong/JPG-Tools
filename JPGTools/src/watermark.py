from PIL import Image, ImageFont, ImageDraw
import ImageColor
import _imaging
import StringIO
import os
from glob import glob

jpg = 't:\\5.jpg'
text = 'MIDI@CCF'
angle = 15
myjpg = Image.new("RGBA", (1912 * 2, 1646 * 2), (255, 255, 255,0))
#myjpg.save("d:\\me.jpg", "JPEG")
draw = ImageDraw.Draw(myjpg)

#getting a list of installed fonts
fontdir = os.path.join(os.environ['windir'], "fonts")

ttf_fonts = [os.path.splitext(os.path.basename(font))[0] for font in glob(fontdir + "\\*.ttf")]
print ttf_fonts
#for i in glob(fontdir + "\\*.ttf"):
#    #print i
##for fontfile in glob(os.listdir(fontdir) + "\\.ttf"):
#    try:
#        font = ImageFont.truetype(i, 70)
#    except IOError:
#        print i
#    else:
#        pass#print font.getname()
##font = ImageFont.load('d:\arial.ttf')
font = ImageFont.truetype("SIMSUN.TTC", 70) #"arial.TTF", 70)


for x in range(50, 1890, 500):
    for y in range(50, 1600, 150):
        
        draw.text((x,y), "MIDI@CCF", (0, 255, 255), font= font)#ImageColor.getrgb('white')) #font = font)
#myjpg.save("d:\\me2.jpg", "JPEG")        
Fil = StringIO.StringIO()
#temp = myjpg.save(Fil, "JPEG")

im = Image.open(jpg)
im = im.convert("RGBA")

rot = myjpg.rotate(angle, expand=1) #.resize((1912, 1646))
rot = rot.crop((500, 500, 2412, 2146))


im.paste(rot, None, rot)
im.save('d:\\test.png')


"""
 
5
 
down vote  PIL is certainly capable of this. First you'll want to create an image that contains the repeated text.
It should be, oh, maybe twice the size of the image you want to watermark (since you'll need to rotate it and then crop it).
You can use Image.new() to create such an image, then ImageDraw.Draw.text() in a loop to repeatedly plaster your text onto it, and the image's rotate() method to rotate it 15 degrees or so. Then crop it to the size of the original image using the crop() method of the image.

To combine it first you'll want to use ImageChops.multiply() to superimpose the watermark onto a copy of the original image (which will have it at 100% opacity) then ImageChops.blend() to blend the watermarked copy with the original image at the desired opacity.

That should give you enough information to get going -- if you run into a roadblock, post code showing what you've got so far, and ask a specific question about what you're having difficulty with.
 

"""
