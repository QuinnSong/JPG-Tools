from PIL import Image
import numpy as np

threshold=100
dist=5
img=Image.open("d:\\windows\\desktop\\leaf.png").convert('RGBA')
# np.asarray(img) is read only. Wrap it in np.array to make it modifiable.
arr=np.array(np.asarray(img))
r,g,b,a=np.rollaxis(arr,axis=-1)    
mask=((r>threshold)
      & (g>threshold)
      & (b>threshold)
      & (np.abs(r-g)<dist)
      & (np.abs(r-b)<dist)
      & (np.abs(g-b)<dist)
      )
arr[mask,3]=0
img=Image.fromarray(arr,mode='RGBA')
img.save('c:/out.png')