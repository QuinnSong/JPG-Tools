# Thanks to:
#http://playpython.blogspot.ca/2012/08/generate-ascii-image-of-yours.html

#Steps which i am following
#1) Read Image; 2) Resize image; 3) Convert it to grayscale
#4) get RGB value; 5) map RGB values to ASCII chars

#Still you can achive high resolution ASCII image by selecting more specific charachters for different gray colors
############################################################
#Note: RGB values are tuple like (255,33,98)
#For gray scale RGB value will be int starting from 255 to 0
#255  is white
#0 is black
############################################################

#!/usr/bin/python
from PIL import Image
from  PIL import ImageOps
import sys, os

def image2ascii(image):
    w,h = image.size
    if w > 120: x = 120
    else: x = w
    y = int(float(h) * float(x) /w )
    #x, y = 150, 150
    im = image.resize((x,y))
    im = im.convert("L")
    
    #build up str
    str = ""
    #with open("image.txt", "w") as f:      # open text file    
    for pixely in range(y):  
        for pixelx in range(x):                
            color = im.getpixel((pixelx,pixely))
            if color >= 253 : ch = " "
            elif color >= 250 : ch = "."
            elif color >= 230 : ch = ","
            elif color >= 210 : ch = '"'
            elif color >= 190 : ch = '^'
            elif color >= 170 : ch = "%"
            elif color >= 150 : ch = "&"
            elif color >= 130 : ch = "a"
            elif color >= 110 : ch = "o"
            elif color >= 90 : ch = "0"
            elif color >= 70 : ch = 'L'
            elif color >= 50 : ch = 'y'
            elif color >= 30 : ch = "Y"
            elif color >= 10 : ch = "H"
            elif color >= 0 : ch = "#"
            else:ch = " "
            str += ch
        str += "\r\n"
    return str    #f.write(str)
    #os.startfile('image.txt')
#Open with wordpad and ctrl+ mousewheel to change font size..   cheers :)