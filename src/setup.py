#-*- coding: cp936 -*-

from cx_Freeze import setup, Executable as cxExecutable
import platform
#import os

def include_files():
    path_base = "C:\\Python27\\Lib\\site-packages\\wordcloud\\"
    skip_count = len(path_base)
    zip_includes = [(path_base, "wordcloud/")]
    for root, sub_folders, files in os.walk(path_base):
        for file_in_root in files:
            fileName = os.path.basename(file_in_root)
            baseFileName, ext = os.path.splitext(fileName)
            if ext not in ['.py']:
                zip_includes.append(
                    ("{}".format(os.path.join(root, file_in_root)),
                     "{}".format(os.path.join("wordcloud/", root[skip_count:], file_in_root))
                )
        )
    return zip_includes
        

if platform.system() == 'Windows':
    # base must be set on Windows to either console or gui app
    # testpubsub is currently a console application
    base = 'Win32GUI'
    #base = 'Console'
else:
    base = None

#-----------------------------------------------------------------------
# The following dlls should be manually included in the package
# since cx_Freeze 5.1 do not freeze them into the package:(
# \lib\pywintypes27.dll
# \lib\pythoncom27.dll
# \lib\libzbar-0.dll
# \lib\libiconv-2.dll
# \lib\tcl85.dll
# \lib\tk85.dll
#------------------------------------------------------------------------

opts = {# 'compressed' : True,
        # 'create_shared_zip' : False,
        # 'bin_includes' : bin_includes,
        # 'includes' : 'pywintypes',
         'packages' : ['pubsub.core.kwargs', 'pubsub.core.arg1', 'configobj', 'wordcloud', 'win32com'],
         #'zip_includes' : [('C:\\Python27\\Lib\site-packages\\wordcloud\\','wordcloud\\')]
         }

WIN_Target = cxExecutable(
    script='image_viewer.py',
    base=base,
    targetName=u'JPGTools.exe',
    #compress=True,
    #appendScriptToLibrary=False,
    #appendScriptToExe=False,    
    #excludes=['_ssl',  
    #'pyreadline','doctest', 'scipy',
    #'optparse', 'pickle', 'calendar'],  # Exclude standard library    
    )

setup(
    name=u'JPGTools',
    description=u"查看缩放裁剪等功能的图片工具",
    version=u'1.0.0',
    author=u'Quinn Song',
    
    options={'build_exe' : opts},
    executables=[WIN_Target]
    )