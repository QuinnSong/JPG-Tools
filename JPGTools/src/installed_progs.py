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
        return u'ϵͳ��δ��⵽%s��\r\n��������Ҫ��ģ���֧�֣��밲װ%s�����ԡ�' % (app, app)
    elif not hasPath(appInPath, exe):
        return u'ϵͳ·����δ��⵽%s��\r\n�뽫����ӵ�ϵͳ��PATH�����������ԡ�' % (app)
    elif app == 'ImageMagick':
        try: mh = os.environ['MAGICK_HOME']
        except: mh = None
        if not mh: return u'��������MAGICK_HOME��δ���á����򼴽��˳���'
        elif os.path.isfile(os.path.join(mh, 'convert.exe')): return None
        else: return u'��������MAGICK_HOME���ò���ȷ�����򼴽��˳���'
    else: return None
    
#if __name__ == '__main__':
#    print appDetect('ImageMagick', 'ImageMagick', 'convert.exe')
    #print appDetect('Ghostscript', '\\gs\\', 'gswin32c.exe') 
