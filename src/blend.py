from PIL import Image, ImageChops
from color_replace import Replace
from shadow import has_alpha, paste

img1 = Image.open('img2.png')

img2 = Image.open('water.jpg')
img1 = Image.new('RGBA', img2.size, color = 'white')
mask = Image.open(r'D:\windows\Desktop\Folder keep\FSViewer50\Mask\mask76.jpg')
#img1.show()

def blend(image1, image2, alpha):
    image1, image2 = [image.convert('RGBA') for image in [image1, image2] ]   
    return Image.blend(image1, image2, alpha)

def composite (image1, image2, mask):
    image1, image2, mask = [image.convert('RGBA') for image in [image1, image2, mask] ]
    
    im_mask = mask.resize(image1.size, Image.ANTIALIAS)
    #im_mask = Replace()
    return Image.composite(image1, image2, im_mask)

#im = blend(img1, img2, 0.5)
#im = composite(img1, img2, mask)
img1, img2 = [image.convert('RGBA') for image in [img1, img2] ]
mask = mask.convert('L')
mask = mask.resize(img1.size, Image.ANTIALIAS)

paste(img2, Image.new('RGB', img2.size, 'blue'), (0, 0), ImageChops.invert(mask))
#img2.putalpha(mask)
img2.show()
#im.show()