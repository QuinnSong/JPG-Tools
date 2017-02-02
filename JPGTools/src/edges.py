from PIL   import Image
img = Image.open(r'D:\windows\Desktop\20140630\20140727 src\PIC\Cloud-Data-Storage.jpg')
print help(img.smooth)
smoothImg = img.smooth(aperture=(11,11)) #smooth, or do any filtering
edgeMap = img.edges() 
edgeMap = edgeMap.smooth(aperture=(3,3)).threshold(50) # this will widen the edges
finalImg = img.blit(smoothImg,mask = edgeMap) #copy the smoothed image only where edgemap is white
finalImg.show()