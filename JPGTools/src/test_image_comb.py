import os, numpy
import numpy as np
import Image
import re
indir ="/export/data2/gene3d/neuropWeb/src/website/static/images/diab_neurop/"
# Access all PNG files in directory
allfiles=os.listdir(indir)
imlist=[]
filt=[305,395]
for f in allfiles:
    if f.endswith("png") and f.startswith("dude_api_pain"):
        numo=re.sub("[^0-9]", "", f)
        if int(numo) not in filt: continue
        imlist.append(os.path.join(indir,f))
print imlist

def alpha_to_color(image, color=(255, 255, 255)):
    """Set all fully transparent pixels of an RGBA image to the specified color.
    This is a very simple solution that might leave over some ugly edges, due
    to semi-transparent areas. You should use alpha_composite_with color instead.

    Source: http://stackoverflow.com/a/9166671/284318

    Keyword Arguments:
    image -- PIL RGBA Image object
    color -- Tuple r, g, b (default 255, 255, 255)

    """ 
    return image
    x = np.array(image)
    r, g, b, a = np.rollaxis(x, axis=-1)
    r[a == 0] = color[0]
    g[a == 0] = color[1]
    b[a == 0] = color[2] 
    x = np.dstack([r, g, b, a])
    return Image.fromarray(x, 'RGBA')


# Assuming all images are the same size, get dimensions of first image
x=alpha_to_color(Image.open(imlist[0]))

w,h = x.size
N=len(imlist)
print N,w,h
# Create a numpy array of floats to store the average (assume RGB images)
arr=numpy.zeros((h,w,4),numpy.float)

# Build up average pixel intensities, casting each image as an array of floats
for im in imlist:
    

    x=Image.open(im)
    x=alpha_to_color(x)  
    print "A", x.size,w,h,x.format, x.mode
    imarr=numpy.array(x,dtype=numpy.float)
    print "B", arr.shape,imarr.shape
    arr=arr+(imarr/N)

# Round values in array and cast as 8-bit integer
arr=numpy.array(numpy.round(arr),dtype=numpy.uint8)

# Generate, save and preview final image
out=Image.fromarray(arr,mode="RGBA")
out.save("Average.png")
out.show()
