# -*- coding: cp936 -*-

import qrcode

def qrCode(str_data, box_size = 10, border = 4):
    qr = qrcode.QRCode(
        None,
        error_correction = qrcode.constants.ERROR_CORRECT_M,
        box_size = box_size,
        border = border,
    )
    try:
        qr.add_data(str_data)
        qr.make(fit=True)
        
        img = qr.make_image()
        return img
    except Exception as e:
        return None
        
    #http://blog.matael.org/writing/python-and-qrcodes/
