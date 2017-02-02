from PIL import Image
import numpy as np

class testnumpy(object):
	def __init__(self, im):
		self.cur_im = im
	def MakeReplace (self):		
			color_old = (255,255,255,255) #self.getColor(self.ctrlOldColor)
			color_new = (255,0,0,255) #self.getColor(self.ctrlNewColor)
			flag = "=" #self.m_ColorCompareBox.GetValue()
			
			w, h = self.cur_im.size
			im_array = np.array(self.cur_im.convert("RGBA"))
			print "im_array shape: ", im_array.shape
			if True: #self.parent.rubber.crop:
				x1,y1,x2,y2 = 0,0,160,226#self.parent.rubber.crop
				region_array = im_array[y1:y2, x1:x2]
				print "region_array: ", region_array.shape
				if  True: #self.m_checkBoxReplaceStyle.Selection == 0:		
					
					region_array_new = self.Replace(region_array, color_old, color_new, flag = flag)
					
					
				#else:
				#	
				#	region = self.newPil(x2-x1, y2-y1, fill = color_new)
				#	region_array_new = np.asarray(region)
				
				im_array.setflags(write = 1)	
				im_array[y1:y2, x1:x2] = region_array_new
				
				self.cur_im = Image.fromarray(im_array)
				#self.parent.rubber.crop = None
				self.cur_im.save("d:\\windows\\desktop\\11.jpg")
			#else:
			#	if self.m_checkBoxReplaceStyle.Selection == 0:
			#		
			#		self.cur_im = Image.fromarray(Replace(im_array, color_old, color_new, flag = flag))
			#	else: # create a numpy image with color_new
			#		self.cur_im = self.newPil(w,h,color_new)
	
	def Replace(self, im_array, color_old, color_new, flag = "=" ):
		""""""
		r1,g1,b1,a1 = color_old
		r,g,b,a = im_array[:,:,0], im_array[:,:,1], im_array[:,:,2], im_array[:,:,3]
		mask = (r == r1)&(g==g1)&(b==b1)&(a==a1)
		im_array[:,:,:4][mask] = color_new
		#if flag == '>': im_array_new = np.where(im_array > color_old, color_new, im_array).astype(np.uint8)
		#elif flag == '=': im_array_new = np.where(im_array == color_old, color_new, im_array).astype(np.uint8)
		#else: im_array_new = np.where(im_array < color_old, color_new, im_array).astype(np.uint8)
		#Image.fromarray(im_array_new, mode="RGBA").save("d:\\windows\\desktop\\12.jpg")
		im = Image.fromarray(im_array)
		im.save("d:\\windows\\desktop\\new2.jpg")
		return im_array
if __name__ == '__main__':
	im = Image.open("d:\\windows\\desktop\\canon.jpg")
	tn = testnumpy(im)
	tn.MakeReplace()