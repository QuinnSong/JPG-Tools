#-*- coding: cp936 -*-

from cx_Freeze import setup, Executable as cxExecutable
import platform

if platform.system() == 'Windows':
    # base must be set on Windows to either console or gui app
    # testpubsub is currently a console application
    base = 'Win32GUI'
    #base = 'Console'
else:
    base = None

opts = { 'compressed' : True,
         'create_shared_zip' : False,
         'packages' : ['pubsub.core.kwargs', 'pubsub.core.arg1', 'configobj'],
         }

WIN_Target = cxExecutable(
    script='image_viewer.py',
    base=base,
    targetName=u'JPG图片工具.exe',
    compress=True,
    appendScriptToLibrary=False,
    appendScriptToExe=False,    
    excludes=['_ssl',  
    'pyreadline','doctest', 'scipy',
    'optparse', 'pickle', 'calendar'],  # Exclude standard library    
    )

setup(
    name=u'Jpg图片工具',
    description=u"查看缩放裁剪等功能的图片工具",
    version=u'0.93',
    author=u'Quinn Song',
    
    options={'build_exe' : opts},
    executables=[WIN_Target]
    )