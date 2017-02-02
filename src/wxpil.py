import wx
import Image

def piltoimage(pil, alpha=True):
    """Convert PIL Image to wx.Image."""
    if alpha:
        image = apply( wx.EmptyImage, pil.size )
        image.SetData( pil.convert( "RGB").tostring() )
        image.SetAlphaData(pil.convert("RGBA").tostring()[3::4])
    else:
        image = wx.EmptyImage(pil.size[0], pil.size[1])
        new_image = pil.convert('RGB')
        data = new_image.tostring()
        image.SetData(data)
    return image

def imagetopil(image):
    """Convert wx.Image to PIL Image."""
    w, h = image.GetSize()
    data = image.GetData()
    
    redImage = Image.new("L", (w, h))
    redImage.fromstring(data[0::3])
    greenImage = Image.new("L", (w, h))
    greenImage.fromstring(data[1::3])
    blueImage = Image.new("L", (w, h))
    blueImage.fromstring(data[2::3])
    
    if image.HasAlpha():
        alphaImage = Image.new("L", (w, h))
        alphaImage.fromstring(image.GetAlphaData())
        pil = Image.merge('RGBA', (redImage, greenImage, blueImage, alphaImage))
    else:
        pil = Image.merge('RGB', (redImage, greenImage, blueImage))
    return pil
