# -*- coding: cp936 -*- 

import StringIO
import wmi
import os
from _winreg import (HKEY_LOCAL_MACHINE, EnumValue)

def isInstalled (prog):
    r = wmi.Registry ()
    result, names = r.EnumKey (hDefKey=HKEY_LOCAL_MACHINE, sSubKeyName=r"Software\Microsoft\Windows\CurrentVersion\Uninstall")
    return len( [ subkey for subkey in names if prog in subkey]) >= 1
def hasPath (prog, exe):
    paths =  os.environ['PATH'].split(os.pathsep)
    return any( prog in path and os.path.isfile(os.path.join(path, exe)) for path in paths  )
    
def appDetect(app, appInPath, exe):
    if not isInstalled (app):
        return u'系统上未检测到%s。\r\n本工具需要此模块的支持，请安装%s后再试。' % (app, app)
    elif not hasPath(appInPath, exe):
        return u'系统路径上未检测到%s；\r\n请将其添加到系统的PATH环境变量再试。' % (app)
    elif app == 'ImageMagick':
        try: mh = os.environ['MAGICK_HOME']
        except: mh = None
        if not mh: return u'环境变量MAGICK_HOME尚未设置。程序即将退出。'
        elif os.path.isfile(os.path.join(mh, 'convert.exe')): return None
        else: return u'环境变量MAGICK_HOME设置不正确。程序即将退出。'
    else: return None
    
#if __name__ == '__main__':
#    print appDetect('ImageMagick', 'ImageMagick', 'convert.exe')
    #print appDetect('Ghostscript', '\\gs\\', 'gswin32c.exe') 
