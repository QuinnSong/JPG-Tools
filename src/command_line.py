#-*- coding: cp936 -*-

##########################################################################
# To handle command line arguments                                       #
##########################################################################

import os, sys, glob
from PIL import Image
from shutil import copy
import StringIO

JPG_QTY_MAX = 95

class cmd():   
    
    def __init__(self, path, save_path = None, dim_size_args = None, size_limit_arg = None, dpi = None):
        self.count = 0 # initialize the count
        self.path = path
        self.save_path = save_path
        self.dim_size_args = dim_size_args
        self.dpi = dpi
        self.retry = 0
        
        if size_limit_arg:
            self.size_limit_arg = int(size_limit_arg)
        else:
            self.size_limit_arg = size_limit_arg
        self.largeJpgList = []
        self.filepath = ''
        self.filepathnew = ''
        self.resizeImg()
        

    def resizeImg(self):
        """The func to limit jpg image file size"""
    
    
        if os.path.isdir(self.path): # path is dir
            if not self.save_path:
                self.mkDir(self.path + '\\New')
            picPaths = glob.glob(self.path + "\\*.jpg")
            try:               
                for filename in picPaths:
                    self.filepath = os.path.join(self.path, filename) # Get full path                    
                    self.fileResize()
                #isDone = True
            except Exception, e:
                raise #pass
            finally:
                if self.largeJpgList:
                    print '\r\n[Warning] JPG image demensions are too large. Please lower it first.'
                    print '\r\n'.join([a[0] for a  in self.largeJpgList])
                print
                print 'Total file processed: ' + str(self.count)
                    
                
        else: # path is file
            self.filepath = self.path
            if not self.save_path: self.mkDir(os.path.dirname(self.path) + '\\New')
            self.fileResize()
            print 'Job done.'
#---------------------------------------------------------------------------        
    def updateEvent(self):
        """Notify the listener to update"""
        self.count += 1
        print '.',
#---------------------------------------------------------------------------    
    def mkDir(self, path):#,new_path):
        """Create the new dir if not exists"""        

        if not os.path.exists(path):
            os.makedirs(path)
            # "not true"
        else:
            pass
            
#---------------------------------------------------------------------------    
    def tryResize(self, im, quality_val):
        """Part 1 of smart resize image"""
        
        self.retry = self.retry + 1
        
        fil = StringIO.StringIO()
        im.save(fil, 'JPEG', quality = quality_val, dpi = self.cur_dpi) #save to buffer
        ratio = (float)(fil.len/(float)(self.size_limit_arg * 1024))
        #print quality_val
        if ratio > 3:
            quality_val = quality_val - 20
        elif ratio >= 2:
            quality_val = quality_val - 10
        elif ratio >= 1:
            #quality_val = quality_val - 1
            self.tryResize2(im, quality_val)
            return
        elif ratio > 0.5:
            quality_val = quality_val + 6
        else:
            quality_val = quality_val + 12
        
        if self.retry <= 50:
            self.tryResize(im, quality_val)
        else: raise
#---------------------------------------------------------------------------
    def tryResize2(self, im, value):
        """Part 2 of smart resize image"""
        
        fil = StringIO.StringIO() 
        for quality_val in range(value, 1, -1):
            #print quality_val; for debug
            im.save(fil, 'JPEG', quality = quality_val, dpi = self.cur_dpi) #save to buffer                        
            
            if fil.len <= self.size_limit_arg * 1024:    # is the new image file size <= size_limit
                # if yes, then save the new image to new file: filepathnew
                im.save(self.filepathnew, 'JPEG', quality=quality_val, dpi = self.cur_dpi)
                self.updateEvent()
                break;                          # Stop the for loop
            else:
                fil = StringIO.StringIO()       # reset the buffer
#---------------------------------------------------------------------------
    def handleResize(self, im):
        [W, H] = im.size
        
        if not self.dim_size_args:
            return im, True #no option to adjust dimension
        
        if (len(self.dim_size_args.split()) == 1): # dimension change by percentage
            percentage = float(self.dim_size_args.split()[0])
            newWidth, newHeight = W * percentage, H * percentage
        elif (len(self.dim_size_args.split()) == 2): # dimension change by pixels
            [req_width, req_height] = self.dim_size_args.split()
            ratio = (float(req_width)/float(req_height))/(float(W)/float(H))
            if round(ratio, 2) == 1.0:
                newWidth, newHeight = int(req_width), int(req_height)
            elif round(ratio, 2) < 1.0:
                newWidth, newHeight = int(req_width), int(req_width) * H / W
            else:
                newWidth, newHeight = int(req_height) * W/H, int(req_height)            
        im_resized = im.resize((int(newWidth), int(newHeight)), Image.ANTIALIAS)
            
        if self.size_limit_arg: # select all 
            return im_resized, True
        else:#adjust dimension only
            return im_resized, False
#--------------------------------------------------------------------------
    def getImageDPI(self, image):
            # try to get dpi info
            try:
                    im = Image.open(image)
                    dpi = im.info['dpi']
                    return  dpi
            except:
                    return  (96, 96) # default value
        
#---------------------------------------------------------------------------    
    def fileResize(self):
        """Module to resize a single image file"""
        
        try:            
            im = Image.open(self.filepath)
            
            (base, jpgfile) = os.path.split(self.filepath)
            if not self.save_path:
                self.filepathnew = base + '\\New\\' + jpgfile  # new path
            else:
                self.mkDir(self.save_path)
                self.filepathnew = os.path.join(self.save_path, jpgfile)
                
            # process dpi request; if done, then return
            if self.dpi:
                try: im.save(self.filepathnew, 'JPEG', quality=JPG_QTY_MAX, dpi = (int(self.dpi), int(self.dpi)))
                except: pass
                self.updateEvent()
                return
            # calculate current image dpi
            self.cur_dpi = self.getImageDPI(self.filepath)
                
            # Check if resize panel is enabled
            im_new, onFlag = self.handleResize(im)        
    
            if not onFlag: # adjust dimension only
                im_new.save(self.filepathnew, 'JPEG', quality=JPG_QTY_MAX, dpi = self.cur_dpi)
                self.updateEvent()
                return # stop here
            elif self.dim_size_args: #im_reszied
                # CALCULATE ADJUSTED SIZE (IM)
                fil = StringIO.StringIO()
                im_new.save(fil, 'JPEG', quality=JPG_QTY_MAX, dpi = self.cur_dpi)
            
                if fil.len <= self.size_limit_arg * 1024:
                    im_new.save(self.filepathnew, 'JPEG', quality=JPG_QTY_MAX, dpi = self.cur_dpi)
                    self.updateEvent() 
                    return
                else:
                    self.NeedMoreResize(im_new)
            else: # limit size only
                
                #fil = StringIO.StringIO()   # define a buffer to hold resized image
                # resize jpg image to 800 * 600
                #im_resized = im.resize((800, 600), Image.ANTIALIAS)
                if os.stat(self.filepath).st_size <= self.size_limit_arg * 1024:
                    copy(self.filepath, self.filepathnew)
                    self.updateEvent()
                else:
                    self.NeedMoreResize(im)
            
        except Exception, e:
            #raise #pass #print 'Problem occurred when processing ', filepath, ':', e
            pass
#---------------------------------------------------------------------------
    def NeedMoreResize(self, im):
        """Check if the minimum quality of 1 can meet the """
        
        fil = StringIO.StringIO()
        im.save(fil, 'JPEG', quality = 1, dpi = self.cur_dpi)
        if fil.len == self.size_limit_arg * 1024:
            im.save(self.filepathnew, 'JPEG', quality= 1, dpi = self.cur_dpi)
            self.updateEvent()   
        elif  fil.len > self.size_limit_arg * 1024:
            self.largeJpgList.append((os.path.basename(self.filepath), fil.len))
            self.updateEvent()   
        else:
            self.retry = 0
            self.tryResize(im, JPG_QTY_MAX)
