from PIL import Image
from StringIO import StringIO

def color_replace(OLD, NEW, fil_old):
    R_OLD, G_OLD, B_OLD = OLD #(255, 255, 255)
    R_NEW, G_NEW, B_NEW = NEW #(0, 174, 239)

    im = Image.open(StringIO(fil_old.getvalue())).convert("RGBA")
    pixels = im.load()
    
    width, height = im.size
    for x in range(width):
        for y in range(height):
            r, g, b, a = pixels[x, y]
            if (r, g, b) == (R_OLD, G_OLD, B_OLD):
                pixels[x, y] = (R_NEW, G_NEW, B_NEW, 0)
    fil_new = StringIO()
    #im.save(fil_new, 'PNG')

    return im

image = "N:\\Desktop\\signs\NEW\\pdf.png"
im = Image.open(image).convert("RGBA")
fil_old = StringIO()
im.save(fil_old, 'PNG')
im = color_replace((0,0,0), (0,0,0), fil_old)
im.save("N:\\Desktop\\signs\NEW\\pdf_1.png", 'PNG')

"""----------------------------------------------
[Image-SIG] Re: how to make a transparent background 
Rob Myroon robmyroon@yahoo.com 
Wed, 6 Nov 2002 15:40:26 -0800 (PST) 

Previous message: [Image-SIG] Re: how to make transparent background? 
Next message: [Image-SIG] PIL palettes question.. 
Messages sorted by: [ date ] [ thread ] [ subject ] [ author ] 

--------------------------------------------------------------------------------

Hi Victor,

I think I solved my problem.  Remember ... I want to
save .png files with a transparent color.  I have
modified the PngImagePlugin.py file.  There already is
code to set a transparent color but it doesn't seem to
get executed.  My change executes that code.

To set a transparent color simply add a "transparency"
entry to the image's info dictionary.  (Don't do this
if you load a transparent gif or a transparent png ---
PIL creates a "transparency" entry in the info
dictionary.)

The image file must be "P" (palette).  ("L" might work
too but I haven't tried it.)

ex.

im = Image.open(file.xxx)    # ex. 8-bit .bmp
im.info["transparency"] = color number in the palette 
im.save("newfile.png")


Here is a section of code and my additions from
PngImagePlugin.py

def _save(im, fp, filename, chunk=putchunk, check=0):
    # save an image to disk (called by the save
method)

    .
    .
    .

    chunk(fp, "IHDR",
          o32(im.size[0]), o32(im.size[1]),     #  0:
size
          mode,                                 #  8:
depth/type
          chr(0),                               # 10:
compression
          chr(0),                               # 11:
filter category
          chr(0))                               # 12:
interlace flag

    if im.mode == "P":
        chunk(fp, "PLTE", im.im.getpalette("RGB"))

    # Added by R. Myroon 2002.11.06
    if not im.encoderinfo.has_key("transparency"):
        if im.info.has_key("transparency"):
            im.encoderinfo["transparency"] =
im.info["transparency"]
    # End code 2002.11.06
    
    if im.encoderinfo.has_key("transparency"):
        if im.mode == "P":
            transparency = max(0, min(255,
im.encoderinfo["transparency"]))
            chunk(fp, "tRNS", chr(255) * transparency
+ chr(0))
        elif im.mode == "L":
            transparency = max(0, min(65535,
im.encoderinfo["transparency"]))
            chunk(fp, "tRNS", o16(transparency))
        else:
            raise IOError, "cannot use transparency
for this mode"


__________________________________________________
Do you Yahoo!?
HotJobs - Search new jobs daily now
http://hotjobs.yahoo.com/




--------------------------------------------------------------------------------


Previous message: [Image-SIG] Re: how to make transparent background? 
Next message: [Image-SIG] PIL palettes question.. 
Messages sorted by: [ date ] [ thread ] [ subject ] [ author ] 

"""