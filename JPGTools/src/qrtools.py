#!/usr/bin/env python

# Authors:
#   David Green <david4dev@gmail.com>
#   Ramiro Algozino <algozino@gmail.com>
#
# qrtools.py: Library for encoding/decoding QR Codes (2D barcodes).
# Copyright (C) 2011 David Green <david4dev@gmail.com>
#
# `qrtools.py` is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# `qrtools.py` is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along
# with `qr.py`.  If not, see <http://www.gnu.org/licenses/>.
import subprocess
import os
import time
import zbar
#import Image
from PIL import Image
import re

class QR(object):

    data_decode = {
        'text': lambda data: data,
        'url': lambda data: data,
        'email': lambda data: data.replace(u"mailto:",u"").replace(u"MAILTO:",u""),
        'emailmessage': lambda data: re.findall(u"MATMSG:TO:(.+);SUB:(.+);BODY:(.+);;", data, re.IGNORECASE)[0],
        'telephone': lambda data: data.replace(u"tel:",u"").replace(u"TEL:",u""),
        'sms': lambda data: re.findall(u"SMSTO:(.+):(.+)", data, re.IGNORECASE)[0],
    }

    def __init__(
        self, data=u'NULL', pixel_size=3, level='L', margin_size=4,
        data_type=u'text', filename=None
    ):
        self.pixel_size = pixel_size
        self.level = level
        self.margin_size = margin_size
        #you should pass data as a unicode object.
        self.data = data
        #get a temp directory
        #self.directory = os.path.join('/tmp', 'qr-%f' % time.time())
        self.filename = filename
        #os.makedirs(self.directory)

    def decode(self, filename=None):
        self.filename = filename or self.filename
        if self.filename:
            scanner = zbar.ImageScanner()
            # configure the reader
            scanner.parse_config('enable')
            # obtain image data
            pil = Image.open(self.filename).convert('L')
            width, height = pil.size
            raw = pil.tostring()
            # wrap image data
            image = zbar.Image(width, height, 'Y800', raw)
            # scan the image for barcodes
            result = scanner.scan(image)
            # extract results
            if result == 0: 
                return False
            else:
                for symbol in image:
                    pass
                # clean up
                del(image)
                #Assuming data is encoded in utf8
                self.data = symbol.data.decode(u'utf-8')
                return True
        else:
            return False
        
    #def destroy(self):
    #    shutil.rmtree(self.directory)
