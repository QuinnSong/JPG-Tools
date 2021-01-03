#-*- coding: cp936 -*-
# ----------------------------------------
# image_viewer.py
# Recompiled 12-28-2020
# Author: Quinn
# ----------------------------------------

import glob
import os, sys, re
import wx
from wx.lib.pubsub import pub
import math
from threading import Thread
from PIL import Image, ImageGrab
from StringIO import StringIO
from shutil import copy
from configobj import ConfigObj
from command_line import cmd
import getopt
import iconfile
import codecs
import subprocess
from shadow import reduce_opacity, put_alpha

# ===== custom environment vars section starts========
exepath = unicode(os.path.dirname(sys.path[0]), 'cp936')
magick_home = os.path.join(exepath, 'imagic')
os.environ['PATH'] += ';' + magick_home
os.environ['MAGICK_HOME'] = magick_home
os.environ['MAGICK_CODER_MODULE_PATH'] = magick_home + os.sep + 'modules' + os.sep + 'coders'
# ===== custom environment vars section ends ==========

# ===== try to import wand ==================
try:
        from wand.image import Image as wImage
        HAS_WAND = True
        from jpgComment import CommentDialog
        from about import MyAboutDialog
        from myPicWorkGUI import MyJPGWorkDlg
        from ascDlg import AscDlg
        from converter import PicConverter
        from QRDlg import MyQRDialog
        from qrtools import QR
        
except ImportError:
	HAS_WAND = False
	
# ===== end of import try ===================

from PIL.PngImagePlugin import PngImageFile

import subprocess
from stack import Stack
from send2trash.plat_win import send2trash

################# For making registry file ###################//
REGDATA = u"""Windows Registry Editor Version 5.00\r\n\r\n

[HKEY_CLASSES_ROOT\*\shell\用JPG图片工具查看]\r\n\r\n

[HKEY_CLASSES_ROOT\*\shell\用JPG图片工具查看\command]\r\n
@="XX \\"%1\\""\r\n\r\n

[HKEY_CLASSES_ROOT\Directory\shell\用JPG图片工具查看]\r\n
@="用JPG图片工具查看"\r\n\r\n

[HKEY_CLASSES_ROOT\Directory\shell\用JPG图片工具查看\command]\r\n
@="XX \\"%1\\""
"""
################ Add to right-click menu ######################
REGFILE = os.path.join(exepath, u'添加此工具到右键菜单.reg')
###############################################################

# 定义常量
PIC_LIST = ['.JPG', '.JPEG', '.BMP', '.TIF', 'TIFF', '.GIF', '.PNG']
JPG_QTY_MAX = 95 ## 不是100
## The image quality, on a scale from 1 (worst) to 95 (best). The default is 75. Values above 95 should be avoided;
##100 disables portions of the JPEG compression algorithm, and results in large files with hardly any gain in = image quality.

class MyDialogQuality ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"质量选项", pos = wx.DefaultPosition, size = wx.Size( 321,165 ), style = wx.DEFAULT_DIALOG_STYLE )
		self.parent = parent
	
		bSizerQualityMain = wx.BoxSizer( wx.VERTICAL )
		
		bSizerQualityUp = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticTextChooseQuality = wx.StaticText( self, wx.ID_ANY, u"选择质量", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextChooseQuality.Wrap( -1 )
		bSizerQualityUp.Add( self.m_staticTextChooseQuality, 1, wx.ALL, 5 )
		
		m_comboBoxQualityChoices = [ u"低", u"中", u"高", u"最佳" ]
		self.m_intQualityChoices = [25, 50, 75, 95]
		self.m_comboBoxQuality = wx.ComboBox( self, wx.ID_ANY, u"高", wx.DefaultPosition, wx.Size( 150,-1 ), m_comboBoxQualityChoices, 0 )
		self.m_comboBoxQuality.SetSelection( 2 )
		bSizerQualityUp.Add( self.m_comboBoxQuality, 0, wx.ALL, 5 )
		
		
		bSizerQualityMain.Add( bSizerQualityUp, 1, wx.EXPAND, 5 )
		
		self.m_staticlineMiddle = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizerQualityMain.Add( self.m_staticlineMiddle, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizerQualityNote = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticTextNotes = wx.StaticText( self, wx.ID_ANY, u"请注意：质量越高，生成的文件将越大。", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextNotes.Wrap( -1 )
		bSizerQualityNote.Add( self.m_staticTextNotes, 0, wx.ALL, 5 )		
		
		bSizerQualityMain.Add( bSizerQualityNote, 1, wx.EXPAND, 5 )
		
		m_sdbSizerBtns = wx.StdDialogButtonSizer()
		self.m_sdbSizerBtnsOK = wx.Button( self, wx.ID_OK )
		m_sdbSizerBtns.AddButton( self.m_sdbSizerBtnsOK )
		self.m_sdbSizerBtnsCancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizerBtns.AddButton( self.m_sdbSizerBtnsCancel )
		m_sdbSizerBtns.Realize();
		
		bSizerQualityMain.Add( m_sdbSizerBtns, 1, wx.EXPAND, 5 )		
		
		self.SetSizer( bSizerQualityMain )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_sdbSizerBtnsCancel.Bind( wx.EVT_BUTTON, self.OnCancel )
		self.m_sdbSizerBtnsOK.Bind( wx.EVT_BUTTON, self.OnOK )
	
	# Virtual event handlers, overide them in your derived class
	def OnCancel( self, event ):
		self.parent.save_as_quality = None
		self.Hide()
		event.Skip()
	
	def OnOK( self, event ):
		self.parent.save_as_quality = self.m_intQualityChoices[ self.m_comboBoxQuality.GetSelection() ]
		self.Hide()
		event.Skip()

class ViewerPanel(wx.Panel):
        """Constructor of Panel"""
        #----------------------------------------------------------------------
        def __init__(self, parent):
                """Constructor"""
                wx.Panel.__init__(self, parent)
                self.parent = parent                              
                self.parent.SetIcon(midi)
                self.midi = midi
                self.pic_list = PIC_LIST

                width, height = wx.DisplaySize()
                self.picPaths = []
                self.currentPicture = 0
                self.totalPictures = 0
                self.img_ext = None # save image file extention
                self.count = 0
                self.history_limit = 10
                self.stack = Stack(10)
                self.current_dpi = None
                self.totalPics = None
                self.default_dpi = 96
                self.singleMode = False
                
                #init icons                
                self.remove_ico = iconfile.removeIcon.GetBitmap()                
                self.up_ico = iconfile.upIcon.GetBitmap()
                self.down_ico = iconfile.downIcon.GetBitmap()
                self.refresh_ico = iconfile.refreshIcon.GetBitmap()
                self.preview_ico = iconfile.previewIcon.GetBitmap()
                self.save_ico = iconfile.saveIcon.GetBitmap()
                self.save32_ico = iconfile.save32Icon.GetBitmap()
                self.close_ico = iconfile.getCloseBmp.GetBitmap()
                self.close32_ico = iconfile.closeIcon.GetBitmap()
                self.file_list = iconfile.file_list.GetBitmap()
                
                # used for sub dir processing
                self.progress_max = 50                
                
                self.isCancel = False
                self.isDone = False
                self.exceptionFileList = []
                self.isException = False
                self.scale = None
                self.scrolls = 0
                self.actual_image = None
                self.isBuildDone = None
                self.retry = 0
                
                # write/read config file
                self.config = None
                self.configfile = os.path.join(exepath, 'jpgconfig.ini')
                
                self.gui_margin = 400
                self.size_limit = 200 # default size in KB                
                self.framePosX, self.framePosY = 0, 0
                
                self.box_value = u'当前文件'
                self.option = None
                
                self.largeJpgList = []
                self.jpgfilelist = []                
                
                self.open_dir = exepath
                self.save_dir = ''
                self.show_sub_dir_warning = 'YES'
                self.show_custom_warning = 'YES'
                self.make_reg = 'YES'
                self.mask_path = ''
                self.save_as_quality = None
                self.mydlg_quality = None
                
                # water mark
                self.water_text = unicode('JPG图片水印', 'cp936')
                self.water_text_repeat = unicode('一次 -> 按左边水印位置', 'cp936')
                self.enablePin = False

                #self.water_NoRepeat_pos = 9
                self.water_text_angle = 0
                self.text_trans = 100
                self.txtDlg = None # the watermark dialog instance
                self.commentDlg = None # the comment dialog instance
                self.picGUI = None
                self.ascGUI = None
                self.qrDlg = None
                self.picConvertDlg = None
                self.im_preview = None
                self.onetime_xy = None # 自定义
                self.im_qr = None
                
                # read program config file
                self.readFile()
                
                #=============== prepare save dir =================
                if self.save_dir != '':
                        try:
                                # make it if it is not None and path not exist
                                self.mkDir(self.save_dir) 
                        except: self.save_dir = ''
                #==================================================
                
                self.photoMaxSize = height - self.gui_margin                
                pub.subscribe(self.updateImages, ("update images"))
                pub.subscribe(self.getNewPathBase, ("get new path"))
                
                #print  pub.getMsgProtocol()
                #self.rubber = None
                self.startPoint = None

                self.slideTimer = wx.Timer(None)
                self.slideTimer.Bind(wx.EVT_TIMER, self.update)
                
                self.layout()
                
                # 激活裁剪功能                
                self.rubber = wxPyRubberBander(self.imageCtrl)
                
                # for command line parameters
                if fileIn is not None:
                        fd = FileDropTarget(self.parent)
                        # reset this one for right-click action
                        self.currentPicture = 0
                        fd.OnDropFiles(0, 0, fileIn)
                # load images if open_dir is not emtpy
                elif self.open_dir != '':                        
                        # call the listener                     
                        pub.sendMessage("update images", msg = self.getPicPaths()) #picPaths)
                # init saved path
                if self.save_dir != '': self.path_base_new = self.save_dir
                elif self.open_dir != '':
                        savedPath = os.path.join(self.open_dir, 'NEW')
                        self.mkDir(savedPath)
                        self.path_base_new = self.force2unicode(savedPath)
                else: self.path_base_new = None
                
                #self.stack 在read config里有声明
        #----------------------------------------------------------------------
        def getPicPaths(self):
                """
                """
                picPaths = []
                for ext in PIC_LIST:
                        picPaths += glob.glob(self.open_dir + "\\*" + ext)
                return picPaths
        #----------------------------------------------------------------------
        def writeFile(self):
                """
                Save user setting to a file
                """
                self.config = ConfigObj(encoding='cp936') #work with unicode
                self.config.filename = self.configfile
                try:
                        if not self.config.has_key('GUI'):
                                self.config['GUI'] = {}
                        self.config['GUI']['SIZE_LIMIT'] = str(self.size_limit)
                        self.config['GUI']['GUI_MARGIN'] = str(self.gui_margin)
                        #self.config.set('GUI', 'TARGET', self.comboBox.Value)                  
                        self.config['GUI']['OPEN_DIR'] = self.open_dir #.replace('\\\\', '\\')
                        self.config['GUI']['SAVE_DIR'] = self.save_dir.replace('\\\\', '\\')
                        self.config['GUI']['SHOW_SUB_DIR_WARNING'] = self.show_sub_dir_warning
                        self.config['GUI']['LAST_PIC_INDEX'] = str(self.currentPicture)
                        self.config['GUI']['LAST_POS'] = str(self.framePosX), str(self.framePosY)
                        self.config['GUI']['MAKE_REG'] = 'NO'                        
                        self.config['GUI']['RECENT_DIR_KEEP'] = self.history_limit
                        self.config['GUI']['DEFAULT_DPI'] = self.default_dpi
                        
                        if not self.config.has_key('WATER MARK'):
                                self.config['WATER MARK'] = {}
                                self.config.comments['WATER MARK'].insert(0,'')
                        self.config['WATER MARK']['TEXT'] = self.water_text
                        self.config['WATER MARK']['REPEAT'] = self.water_text_repeat                        
                        #self.config['WATER MARK']['NoRepeat_POS'] = str(self.water_NoRepeat_Pos)
                        self.config['WATER MARK']['TEXT_ANGLE'] = str(self.water_text_angle)
                        self.config['WATER MARK']['TRANSPARENCY'] = self.text_trans
                        self.config['WATER MARK']['SHOW_CUSTOM_WARNING'] = str(self.show_custom_warning)                        
                        self.config['WATER MARK']['ENABLE_PIN'] = str(self.enablePin)
                        
                        if not self.config.has_key('IMAGE EFFECT'):
                                self.config['IMAGE EFFECT'] = {}
                                self.config.comments['IMAGE EFFECT'].insert(0,'')
                        self.config['IMAGE EFFECT']['MASK_PATH'] = self.mask_path
                        
                        
                        if not self.config.has_key('RECENT DIRS'):
                                self.config['RECENT DIRS'] = {}
                                self.config.comments['RECENT DIRS'].insert(0,'')
                        if not self.stack.isEmpty(): 
                                for i in range(self.stack.topOfStack(), 0, -1):
                                        order = self.stack.topOfStack() - i + 1
                                        self.config['RECENT DIRS'] ['DIR' + str(order)] = self.stack.items[i - 1]
                        self.config.write()
                except Exception, e: pass
                        
        def readFile(self):
                """
                read user setting from a file
                """
                # does the config file exist?
                self.config = ConfigObj(encoding='cp936') # work with unicode
                if os.path.isfile(self.configfile):                        
                        try:
                                self.config = ConfigObj(self.configfile)             
                                self.size_limit =  int(self.config['GUI']['SIZE_LIMIT'])
                                self.gui_margin = int(self.config['GUI']['GUI_MARGIN'])
                                #self.box_value = self.config.get('GUI', 'TARGET').encode('cp936')
                                self.open_dir = unicode(self.config['GUI']['OPEN_DIR'], 'cp936')
                                self.save_dir = unicode(self.config['GUI']['SAVE_DIR'], 'cp936')
                                self.show_sub_dir_warning = self.config['GUI']['SHOW_SUB_DIR_WARNING']
                                self.currentPicture = int(self.config['GUI']['LAST_PIC_INDEX'])
                                self.framePosX, self.framePosY = (int(self.config['GUI']['LAST_POS'][0]), \
                                            int(self.config['GUI']['LAST_POS'][1]))
                                self.make_reg = self.config['GUI']['MAKE_REG']
                                self.history_limit = int(self.config['GUI']['RECENT_DIR_KEEP'])
                                self.default_dpi = int(self.config['GUI']['DEFAULT_DPI'])
                                
                                # read water mark settings
                                self.water_text = unicode(self.config['WATER MARK']['TEXT'], 'cp936')
                                self.water_text_repeat = unicode(self.config['WATER MARK']['REPEAT'], 'cp936') 
                                self.water_text_angle = int(self.config['WATER MARK']['TEXT_ANGLE'])
                                self.text_trans = int(self.config['WATER MARK']['TRANSPARENCY'])
                                #self.fontColor = tuple([int(s) for s in self.config['WATER MARK']['FONT_COLOR']])
                                self.show_custom_warning = self.config['WATER MARK']['SHOW_CUSTOM_WARNING']
                                self.enablePin = (self.config['WATER MARK']['ENABLE_PIN'] == 'True')
                                
                                # read mask path
                                self.mask_path = unicode(self.config['IMAGE EFFECT']['MASK_PATH'], 'cp936')
                                
                                # read recent folder settings
                                self.stack = Stack(self.history_limit) # save history
                                for i in range(int(self.history_limit), 0, -1):
                                        try:  self.stack.push(self.force2unicode(self.config['RECENT DIRS']['DIR' + str(i)]))
                                        except: pass
                                
                        except Exception, e:
                                pass   
        #----------------------------------------------------------------------
        def layout(self):
                """
                Layout the widgets on the panel
                """
                
                self.mainSizer = wx.BoxSizer(wx.VERTICAL)
                btnSizer = wx.BoxSizer(wx.HORIZONTAL)
                # 空白图片初始化
                self.emptyImg = wx.EmptyImage(self.photoMaxSize,self.photoMaxSize)
                self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(self.emptyImg))                
                # 图片框初始化
                self.mainSizer.Add(self.imageCtrl, 0, wx.ALL | wx.CENTER, 5)
                self.imageLabel = wx.StaticText(self, label="")
                self.mainSizer.Add(self.imageLabel, 0, wx.ALL | wx.CENTER, 5)
                # 添加分割线
                self.mainSizer.Add(wx.StaticLine(self, wx.ID_ANY),
                                   0, wx.ALL|wx.EXPAND, 0)
                # 面板项目SIZER
                settingSizer = wx.BoxSizer(wx.HORIZONTAL)
                        
                self.lb_resize = wx.StaticText(self, label=u'调整尺寸:')
                self.lb_resize.SetForegroundColour(wx.RED)
                settingSizer.Add(self.lb_resize, 0, wx.ALL|wx.CENTER, 2 )
                
                # 宽度
                self.ctrlWidth = wx.TextCtrl(self, value = '', size = (50, -1))
                settingSizer.Add(self.ctrlWidth, 0, wx.Top, 5)
                self.Bind(wx.EVT_TEXT, self.onWorHChanged, self.ctrlWidth)
                # 添加 'x'
                lb_x = wx.StaticText(self, label="x") 
                settingSizer.Add(lb_x, 0,  wx.ALL|wx.CENTER, 2)
                # 高度
                self.ctrlHeight = wx.TextCtrl(self, value = '', size = (50, -1))
                settingSizer.Add(self.ctrlHeight, 0, wx.Top, 5)
                self.Bind(wx.EVT_TEXT, self.onWorHChanged, self.ctrlHeight)
                
                self.PnPList = [u'按百分比', u'按像素']
                self.PnPBox = wx.ComboBox(self, value = self.PnPList[1], choices = self.PnPList)
                settingSizer.Add(self.PnPBox, 0, wx.ALL|wx.CENTER, 2 )
                self.Bind(wx.EVT_COMBOBOX_CLOSEUP, self.onPnPBox, self.PnPBox)
                
                settingSizer.Add((15, -1))
                
                self.lb_sizeLimit = wx.StaticText(self, label=u'限制大小(KB):')
                self.lb_sizeLimit.SetForegroundColour(wx.RED)
                settingSizer.Add(self.lb_sizeLimit, 0, wx.ALL|wx.CENTER, 2 )
                
                self.textCtrl_size = wx.TextCtrl(self, value = str(self.size_limit), size = (50, -1))
                settingSizer.Add(self.textCtrl_size, 0, wx.Top, 5)
                
                settingSizer.Add((15, -1))
                #DPI setting
                self.m_textDPI = wx.StaticText( self, label = "DPI" )
                self.m_textDPI.SetForegroundColour(wx.RED)
                settingSizer.Add( self.m_textDPI, 0, wx.ALL, 5 )
                
                self.textCtrl_dpi = wx.TextCtrl(self, size = (60, -1))
                settingSizer.Add(self.textCtrl_dpi, 0, wx.Top, 5)
                self.textCtrl_dpi.Enable(False)
                
                self.m_checkBoxDPI = wx.CheckBox( self, label = "" )
                self.m_checkBoxDPI.Bind(wx.EVT_CHECKBOX, self.dpiChecked)
                settingSizer.Add( self.m_checkBoxDPI, 0, wx.ALL, 5 )
                # old apply button
                
                prev_btn = wx.Button(self, label=u"←上一张", size = (68, -1))
                prev_btn.Bind(wx.EVT_BUTTON, self.onPrevious)
                btnSizer.Add(prev_btn, 0, wx.ALL|wx.CENTER, 2 )
                
                self.middle_btn = wx.Button(self, label=u'幻灯播放↑', size = (68, -1))
                self.middle_btn.Bind(wx.EVT_BUTTON, self.onSlideShow)
                btnSizer.Add(self.middle_btn, 0, wx.ALL|wx.CENTER, 2 )
                
                next_btn = wx.Button(self, label= u"下一张→", size = (68, -1))
                next_btn.Bind(wx.EVT_BUTTON, self.onNext)
                btnSizer.Add(next_btn, 0, wx.ALL|wx.CENTER, 2 )
                      
                btnSizer.Add((15, -1))                        
                
                self.selectList = [u'调整尺寸', u'限制大小', u'调整并限制',
                                   u'查看备注', u'添加特效', u'ASCII图形']               
                self.selectBox = wx.ComboBox(self, value = self.selectList[2], choices = self.selectList, style = wx.CB_READONLY)
                btnSizer.Add(self.selectBox, 0, wx.ALL|wx.CENTER, 2 )
                self.Bind(wx.EVT_COMBOBOX_CLOSEUP, self.onSelectChanged, self.selectBox)   
                
                #
                boxList = [u'当前文件', u'当前目录', u'当前目录和子目录']
                self.comboBox = wx.ComboBox(self, value = self.box_value, choices = boxList, style = wx.CB_READONLY)            

                btnSizer.Add(self.comboBox, 0, wx.ALL|wx.CENTER, 2 )
                
                                
                # apply button new pos
                self.btnApply = wx.Button(self, label=u'应用(&A)', size = (60, -1))
                self.btnApply.Bind(wx.EVT_BUTTON, self.OnApply)
                btnSizer.Add(self.btnApply, 1, wx.ALL|wx.CENTER, 5 )
                
                self.mainSizer.Add(settingSizer, 0, wx.ALL | wx.CENTER, 1) 
                self.mainSizer.Add(btnSizer, 0, wx.ALL | wx.CENTER, 1)
                
                self.status = wx.StatusBar(self, name="status")
                self.status.SetFieldsCount(2)
                self.status.SetStatusWidths([-1, 80])
                
                self.status.Bind(wx.EVT_MOTION, self.motion)
                                
                # Handle focus event
                self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
                
                self.mainSizer.Add(self.status, 0, wx.EXPAND , 10)
                pub.subscribe(self.setStatus, ("set status"))
                self.SetSizer(self.mainSizer)

        #--------------------------------------------------------------------
        def onLeftDown (self, event):
                #self.parent.onActive(None)
                self.parent.SetFocus()
                
        def setStatus(self, msg = ''):
                if (msg != "OnMode"):
                        self.status.SetStatusText(msg, number = 0)
                else:
                        self.status.SetStatusText(self.singleMode * u"单文件模式" + (not self.singleMode) * "", number = 1)
        def dpiChecked(self, event):
                obj = event.GetEventObject()       
                self.textCtrl_dpi.Enable(obj.GetValue())
                

        def motion(self, event):                
                self.status.SetToolTipString(self.status.GetStatusText())
                event.Skip()
        #---------------------------------------------------------------------
        def setFontDlgPos(self, Dialog):
                """
                确保字体对话框就在GUI左右
                """
                screen_sizeX = wx.DisplaySize()[0]                
                
                if self.parent.Position.x + self.parent.GetSize().width + Dialog.GetSize().width <= screen_sizeX:
                        Dialog.SetPosition((self.parent.Position.x + self.parent.GetSize().width, self.parent.Position.y))
                else:
                        Dialog.SetPosition((self.parent.Position.x  - Dialog.GetSize().width, self.parent.Position.y))
                        
                # restore window (check if minimized)
                if not Dialog or Dialog.Size != Dialog.MinSize: Dialog.Show()
                else: Dialog.Restore()                
                        
        #---------------------------------------------------------------------
        def toggleUpThree(self, option):
                if option in [u'查看备注', u'ASCII图形', u'添加特效' ]:
                        self.enable_resize_panel(False) 
                        self.enable_size_limit_panel(False)
                        self.PnPBox.Enable(False)
                        
        def cropEnabled(self, w, h, enabled = False):
                if enabled:
                        # update status bar
                        msg = u"当前选定区域：" + str(w) + 'x' + str(h) + u" 像素。"                 
                        pub.sendMessage("set status", msg = msg)
                        
        #--------------------------------------------------------------------
        def callConvertDialog(self):
                if not self.picConvertDlg:
                        self.picConvertDlg = PicConverter(self)
                        self.setFontDlgPos(self.picConvertDlg)
                else:
                        self.setFontDlgPos(self.picConvertDlg)
        #---------------------------------------------------------------------
        def onSelectChanged(self, event):
                """
                Event handler on selection changes                
                """
                
                option = self.selectBox.GetValue()
                self.toggleUpThree(option)                
                              
                if    self.totalPictures > 0:                        
                        if not self.singleMode: 
                                self.enablePin = option == u'添加特效' and self.txtDlg and self.txtDlg.IsShown()
                                self.imgReload() 
                
                        if option == u'调整尺寸':
                                self.enable_resize_panel() 
                                self.enable_size_limit_panel(False)
                                self.PnPBox.Enable(True)
                        elif option == u'限制大小':
                                self.enable_resize_panel(False) 
                                self.enable_size_limit_panel()
                                self.PnPBox.Enable(False)  
                                        
                        elif  option == u'查看备注':   
                                if not self.commentDlg:
                                        self.commentDlg = CommentDialog(self)
                                        self.setFontDlgPos(self.commentDlg)
                                else:
                                        self.setFontDlgPos(self.commentDlg)
                                                
                        elif option == u'添加特效': self.doJpgWork()
                                        
                        elif    option == u'ASCII图形': 
                                if not self.ascGUI:
                                        self.ascGUI = AscDlg(self)
                                        self.setFontDlgPos(self.ascGUI)
                                        self.ascGUI.DrawAscii()
                                else:
                                        self.setFontDlgPos(self.ascGUI)
   
                        else:
                                self.enable_resize_panel() 
                                self.enable_size_limit_panel()
                                self.PnPBox.Enable(True)
                               
                elif self.imageLabel.GetLabel().startswith( u'(预览)未命名.png'):
                        pub.sendMessage("set status", msg = u"请先保存二维码图片，再进行此操作。")
                else:
                        wx.MessageBox(u"亲，您还没有加载图片呢 :-)", u"小提醒", wx.OK | wx.ICON_INFORMATION)
                        
        #---------------------------------------------------------------------
        def doJpgWork (self):
                """
                Start Jpg Work GUI
                """
                if not self.picGUI:
                        self.picGUI = MyJPGWorkDlg(self)
                        self.setFontDlgPos(self.picGUI)                                        
                else:
                        self.setFontDlgPos(self.picGUI)        


        #---------------------------------------------------------------------
        def onWorHChanged(self, event):
                """
                update Width if height changes; same for the other way 
                """
                if self.totalPictures > 0: 
                        obj = event.GetEventObject()                        
                        try:
                                if obj == self.ctrlWidth:
                                        if int(obj.Value) <= 0:
                                                self.ctrlWidth.Clear()
                                                self.ctrlWidth.SetFocus()
                                        else:
                                                if self.PnPBox.GetValue() == u'按百分比':
                                                        self.ctrlHeight.ChangeValue(self.ctrlWidth.Value)
                                                elif self.PnPBox.GetValue() == u'按像素':
                                                        self.ctrlHeight.ChangeValue(str(int(self.ctrlWidth.Value) * self.H / self.W))
                                else:
                                        if int(obj.Value) <= 0:
                                                self.ctrlHeight.Clear()
                                                self.ctrlHeight.SetFocus()
                                        else:
                                                if self.PnPBox.GetValue() == u'按百分比':
                                                        self.ctrlWidth.ChangeValue(self.ctrlHeight.Value)
                                                elif self.PnPBox.GetValue() == u'按像素':
                                                        self.ctrlWidth.ChangeValue(str(int(self.ctrlHeight.Value) * self.W / self.H))
                        except ValueError:
                                if obj == self.ctrlWidth:
                                        self.ctrlWidth.Clear()
                                        self.ctrlWidth.SetFocus()
                                else:
                                        self.ctrlHeight.Clear()
                                        self.ctrlHeight.SetFocus()
        #----------------------------------------------------------------------
        def enable_resize_panel(self, flag = True):
                """
                Constructor
                """
                self.lb_resize.Enable(flag)
                self.ctrlWidth.Enable(flag)
                self.ctrlHeight.Enable(flag)
                #self.PnPBox.Enable(flag)                                        
        #----------------------------------------------------------------------
        def enable_size_limit_panel(self, flag = True):
                """
                Constructor
                """
                self.lb_sizeLimit.Enable(flag)
                self.textCtrl_size.Enable(flag)
        #----------------------------------------------------------------------
        def onPnPBox(self, event):
                """Allow user to show sizes in pixels or percentage"""
                
                #cbResizeBox = event.GetEventObject()
                self.updateResizeBox()                  
        #----------------------------------------------------------------------
        #----------------------------------------------------------------------
        def calNewHW(self, img):
                """"""                                
                # scale the image, preserving the aspect ratio
                photoMaxSizeNew = self.photoMaxSize + int(self.scrolls * self.photoMaxSize / 20)
                if self.W > self.H:
                        self.NewW = photoMaxSizeNew
                        self.NewH = photoMaxSizeNew * self.H / self.W
                        self.scale = float(self.W) / float(self.NewW) 
                else:
                        self.NewH = photoMaxSizeNew
                        self.NewW = photoMaxSizeNew * self.W / self.H
                        self.scale = float(self.H) / float(self.NewH)
                        
                return img.Scale(self.NewW, self.NewH)
        #----------------------------------------------------------------------
        def getGuiTitle(self, label):
                """GUI title with file name in realtime"""
                curJpg = self.getCurJpg()
                title = label + ur" (文件：" + os.path.basename(curJpg) + ur")"
                return title
        #----------------------------------------------------------------------
        def getCurJpg(self):
                """Get current full jpg path"""
                if self.picPaths:
                        curJpg = self.force2unicode(self.picPaths[self.currentPicture])                
                        return curJpg
                else: return None
                
        def popFailedImg(self):
                self.picPaths.pop(self.currentPicture )
                self.progress_max = self.progress_max - 1 # total is also down by 1
                pub.sendMessage("update images", msg = self.picPaths)

        #--------------------------------------------------------------------
        def imageOpen(self, image):
                try:
                        im = Image.open(image)
                        return im
                except:
                        self.popFailedImg()
                        #pub.sendMessage("set status", msg = u"文件加载失败，已从列表中移除：" + image)
                        return None
        #---------------------------------------------------------------------
        def getImageDPI(self, image):
                # try to get dpi info
                try:
                        im = self.imageOpen(image) 
                        dpi = im.info['dpi']
                        return  str(dpi[0]) #4*' ' + str(dpi[0]) + 'DPI'
                except:
                        return None
        def getSettingDPI(self, image):
                # try to get dpi from setting panel
                if self.m_checkBoxDPI.GetValue(): return (int(self.textCtrl_dpi.GetValue()), int(self.textCtrl_dpi.GetValue()))
                else:
                        dpi = self.getImageDPI(image)
                        if dpi: return (int(dpi), int(dpi))
                        else: return (self.default_dpi, self.default_dpi) # default dpi is 96
                        
        def onQR(self):                
                if not self.qrDlg:                        
                        self.qrDlg = MyQRDialog(self.parent)
                self.setFontDlgPos(self.qrDlg)
                
        def showQR(self, image):
                # if it is QR code, show the text
                image_name = os.path.basename(image)
                mycode=QR(filename= image)
                if mycode.decode():
                        if not wx.TheClipboard.IsOpened():                                
                                data = wx.TextDataObject()
                                if wx.TheClipboard.Open():
                                        success = wx.TheClipboard.GetData(data)
                                        # clear clip board text if exists
                                        wx.TheClipboard.Clear()                                
                                        
                                self.onQR()
                                self.qrDlg.m_textCtrlBody.SetValue(mycode.data)                        
                                self.qrDlg.SetTitle(image_name)
                                
                                if success: wx.TheClipboard.SetData(data)
                                wx.TheClipboard.Close()
                                self.SetFocus()
                elif self.qrDlg: self.qrDlg.Show(False)
                
                self.parent.SetFocus() # fix for escape event
        
        #----------------------------------------------------------------------
        def loadImage(self, image):
                """
                Show image in the image panel
                """
                image_name = os.path.basename(image)
                img = wx.Image(image, wx.BITMAP_TYPE_ANY)

                dpi = self.getImageDPI(image)
                
                if dpi:
                        dpi_label = 4*' ' + dpi + 'DPI'
                        self.textCtrl_dpi.SetValue(dpi)
                else: dpi_label = ''
                
                # scale the image, preserving the aspect ratio
                self.W = img.GetWidth()
                self.H = img.GetHeight()               
                
                if not self.actual_image: img = self.calNewHW(img)

                self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
                imageSize = os.path.getsize(image)
                labelString = image_name + 4*' ' + str(self.W) + 'x' + str(self.H) + 4*' ' \
                                + str(self.convertSize(imageSize)) + dpi_label + \
                                + 4*' ' + str(self.currentPicture + 1) + '/' + str(self.totalPictures)
                
                self.imageLabel.SetLabel(labelString)
                
                # update resize part
                self.updateResizeBox()
                # read and set dpi value
                if isinstance(dpi, int):
                        self.textCtrl_dpi.SetValue(dpi)

                self.Refresh()
                
                # deal with rubber class
                del self.rubber
                self.rubber = wxPyRubberBander(self.imageCtrl)
                
                pub.sendMessage("resize", msg = "")
                
                # update status msg
                pub.sendMessage("set status", msg = u"当前工作目录：" + self.open_dir)
                
                # Set preview to None; clear the cache
                self.im_preview = None                
                
                # load comments if the dialog exits
                if self.commentDlg:
                        self.commentDlg.loadCurrentJpg(image)
                        self.commentDlg.Refresh()
                        
                if self.ascGUI: self.ascGUI.DrawAscii()                
                if self.picGUI:
                        self.picGUI.RefreshTitle()
                        self.picGUI.list_view_dlg = None # refresh dialog
                if self.picConvertDlg: self.picConvertDlg.RefreshTitle()
                
                wx.CallAfter(self.showQR, image)

        #----------------------------------------------------------------------
        def updateResizeBox(self):
                """ Constructor """
                if self.totalPictures > 0:
                        if self.PnPBox.GetValue() ==  u'按百分比':
                                self.ctrlWidth.ChangeValue('100')
                                self.ctrlHeight.ChangeValue('100')
                        elif self.PnPBox.GetValue() ==  u'按像素':
                                # update resize part
                                self.ctrlWidth.Value = str(self.W)
                                self.ctrlHeight.Value = str(self.H)
        #----------------------------------------------------------------------
        def nextPicture(self, event = None):
                """
                Loads the next picture in the directory
                """                        
                # check if totalPictures are 0?
                if self.totalPictures > 1:
                        if self.currentPicture == self.totalPictures - 1:
                                self.currentPicture = 0
                        else:
                                self.currentPicture += 1
                        # check if exists
                        if not os.path.exists( self.picPaths[self.currentPicture] ):
                                self.popFailedImg()
                                
                        self.loadImage(self.picPaths[self.currentPicture])
                                
        def imgReload(self):
                """
                Reload image
                """
                if self.picPaths: # make sure it's not empty
                        self.loadImage(self.picPaths[self.currentPicture])
                
        #----------------------------------------------------------------------
        def previousPicture(self, event = None):
                """
                Displays the previous picture in the directory
                """                        
                # check if totalPictures are 0?
                if self.totalPictures > 1:
                        if self.currentPicture == 0:
                                self.currentPicture = self.totalPictures - 1
                        else:
                                self.currentPicture -= 1
                                
                        # check if exists
                        if not os.path.exists( self.picPaths[self.currentPicture] ):
                                self.popFailedImg()
                        self.loadImage(self.picPaths[self.currentPicture])
                                
        #----------------------------------------------------------------------
        def update(self, event):
                """
                Called when the slideTimer's timer event fires. Loads the next
                picture from the folder by calling th nextPicture method
                """
                self.nextPicture()
                
        #----------------------------------------------------------------------
        def natural_sort(self, l): 
                convert = lambda text: int(text) if text.isdigit() else text.lower() 
                alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
                return sorted(l, key = alphanum_key)
        
        #---------------------------------------------------------------------
        def updateImages(self, msg = None):
                """
                Updates the picPaths list to contain the current folder's images (sorted)
                """
                # if there are pics found in the dir, then load the image
                if msg:
                        self.picPaths = self.natural_sort(msg) 
                        self.totalPictures = len(self.picPaths)  
                        self.currentPicture = 0  # reset current picture
                        # update open_dir
                        try:   
                                self.open_dir = self.force2unicode(os.path.dirname(self.picPaths[self.currentPicture]).replace("\\\\","\\"))
                                self.actual_image = None
                                self.loadImage(self.picPaths[self.currentPicture])
                                self.stack.push(self.force2unicode(self.open_dir))
                        except: pass
                else:   pub.sendMessage("set status", msg = u"指定目录 (" + self.open_dir + u") 没有图片可以加载;)")
        #----------------------------------------------------------------------
        def onNext(self, event):
                """
                Calls the nextPicture method
                """
                self.nextPicture()
        
        #----------------------------------------------------------------------
        def onPrevious(self, event):
                """
                Calls the previousPicture method
                """
                self.previousPicture()
        
        #----------------------------------------------------------------------
        def onSlideShow(self, event = None):
                """
                Starts and stops the slideshow
                """
                # 如果加载图片多于1个，就加幻灯播放
                if self.totalPictures > 1:
                        btn = self.middle_btn
                        label = btn.GetLabel()
                        if label == u'幻灯播放↑':
                                self.slideTimer.Start(3000)
                                btn.SetLabel(u'停止↓')
                        else:
                                self.slideTimer.Stop()
                                btn.SetLabel(u'幻灯播放↑')
        def doImgCut(self): 
                if self.rubber.crop:
                        self.theImg = self.force2unicode(self.picPaths[self.currentPicture])
                        ## send msg to listener to get new base update
                        pub.sendMessage("get new path", msg = self.theImg)
                        self.resizeImg(self.theImg, self.rubber.crop)                        
                else:  pub.sendMessage("set status", msg = u"您尚未选定要裁剪的区域呢;)")
        #---------------------------------------------------------------------------            
        def OnApply(self, event):
                """
                Process Apply button click event
                """
                if self.imageLabel.GetLabel().startswith( u'(预览)未命名.png'):
                        pub.sendMessage("set status", msg = u"请先保存二维码图片，再进行此操作。")
                        return

                if len(self.picPaths) == 0 or self.ctrlHeight.Value == '' \
                        or self.ctrlWidth.Value == '':
                        return
                self.theImg = self.force2unicode(self.picPaths[self.currentPicture])
                ## send msg to listener to get new base update
                pub.sendMessage("get new path", msg = self.theImg)                
                
                FileorDir = self.comboBox.GetValue()
                btn = self.btnApply

                if self.textCtrl_size.Value.isnumeric(): # get size_limit setting
                                self.size_limit = int(self.textCtrl_size.Value)
                                self.isDone = False
                                self.isCancel = False
                                self.isException = False
                                self.exceptionFileList = []
                                self.largeJpgList = []
                                self.totalPics = None
                                self.jpgfilelist = []
                                
                                btn.Disable()
                                pub.sendMessage("set status", msg = u"正在处理中，请稍候...") # reset status bar
                
                                if FileorDir == u'当前文件':      # option 1
                                        self.option = 1
                                        self.resizeImg(self.theImg, self.size_limit)
                                elif FileorDir == u'当前目录':   # option 2
                                        self.option = 2
                                        self.totalPics = self.totalPictures
                                        
                                        t = Thread(target=self.resizeImg, 
                                                   args=(os.path.dirname(self.theImg), self.size_limit))                                        
                                        t.start()                                
                                        
                                        self.progress_max = self.totalPictures
                                        dlg = MyProgressDialog(self)        
                                        dlg.ShowModal()
                                        
                                elif FileorDir == u'当前目录和子目录':    # option 3
                                        self.option = 3
                                        result = wx.ID_OK
                                        if self.show_sub_dir_warning == 'YES':
                                                dlg = WarningDialog(self)
                                                result = dlg.ShowModal()
                                                dlg.Destroy()
                                                self.show_sub_dir_warning = 'NO' 
                                        if  result == wx.ID_CANCEL:
                                                btn.Enable()
                                                pub.sendMessage("set status", msg = u"您已取消了本次操作。")
                                                return
                                        
                                        t_build = Thread(target = self.buildFileList)
                                        t_build.start()                                
                                        
                                        # show the list prepare window
                                        dlg = ListPrepDialog(self)        
                                        dlg.ShowModal()
                                        #更新进度条最大值
                                        self.progress_max = len(self.jpgfilelist)
                                        t = Thread(target=self.resizeImg, 
                                                   args=(None, self.size_limit))
                                        t.start()                                        
                                        
                                        dlg2 = MyProgressDialog(self)        
                                        dlg2.ShowModal()
                                        
                                btn.Enable()
                                self.rubber.crop = None # clear the crop field
                              
                else:
                        # if invalid size, clear the field and set focus
                        self.textCtrl_size.Clear()
                        self.textCtrl_size.SetFocus()
                
        def showResultDlg(self):
                if len(self.largeJpgList) > 0:                                        
                        maxlen = max(len(s[0]) for s in self.largeJpgList)
                        # maxlen
                        jpgListString = [a[0] + (maxlen - len(a[0]) ) * 2 * ' ' + ' : \t' +  self.convertSize(a[1]) for a in self.largeJpgList]
                        dlg = wx.MessageDialog(None, u'由于图片尺寸太大，而无法完成指定的操作！\r\n请缩小尺寸后再试。最小尺寸如下：\r\n\r\n' + \
                                '\r\n'.join(jpgListString), u'友情提示', style=wx.OK)
                        dlg.ShowModal()
                        pub.sendMessage("set status", msg = u"操作完成，但有些图片无法处理。")
                elif self.isDone or self.isCancel:
                        msg = u"当前操作已被取消。" * self.isCancel + u"恭喜！文件全部处理完毕。" * (not self.isCancel) * (self.option > 1) + \
                                u"文件已处理（保存）。" * (self.option == 1) + (u"处理有些文件时出现异常：" + '\r\n'.join(self.exceptionFileList)) * self.isException
                        pub.sendMessage("set status", msg = msg)
                        
        #------------------------------------------------------------
        def getEXT (self, ext):                
                """Get Image format string"""
                if ext.upper() in ['.JPG', '.JPEG']:
                        return 'JPEG'
                elif ext.upper() in ['.TIF', '.TIFF']:
                        return 'TIFF'
                else :
                        return ext.upper()[1:]
        #------------------------------------------------------------
        def saveToFil(self, img, EXT):
                """ save PIL image to buffer stringIO """
                fil = StringIO()
                EXT = self.getEXT(EXT) #; USE PNG FOR ALL PREVIEWS
                # if not RGBA, convert to RGBA
                #img = img.convert("RGBA")
                if img.format == 'JPEG':
                        img.save(fil, EXT, quality = JPG_QTY_MAX)
                else:
                        img.save(fil, EXT)
                return fil
        
        def saveToJpg (self, img, fileout, dpi, quality = JPG_QTY_MAX):
                """ save to JPEG image using max quality """
                img.save(fileout, 'JPEG', quality = quality, dpi = dpi)
                
        #------------------------------------------------------------
        def saveToFile(self, img, EXT, fileout, isManual = False):
                """ Save PIL image to a file """
                finished = True
                EXT = self.getEXT(EXT)                
                if not self.current_dpi: self.current_dpi = (96, 96)
                try:
                        if EXT == 'JPEG':
                                if isManual:
                                        if not self.mydlg_quality:
                                                self.mydlg_quality = MyDialogQuality(self)
                                        self.mydlg_quality.ShowModal()

                                        if self.save_as_quality:
                                                self.saveToJpg(img, fileout, self.current_dpi, self.save_as_quality)
                                        else: finished = False
                                else: self.saveToJpg(img, fileout, self.current_dpi)
                                        
                        elif EXT in ['PNG', 'TIFF']:
                                img.save(fileout, EXT, dpi = self.current_dpi)
                        else:
                                img = img.convert("RGB")
                                img.save(fileout, EXT)
                except: pass
                return finished
                
        #------------------------------------------------------------        
        def imgPreview(self, img, ext, isQR = False):
                """预览图片"""
                
                img = img.convert("RGBA")
                fil = self.saveToFil(img, ext)

                self.W, self.H = img.size
                
                # set image object
                self.im_preview = img
                
                # convert to wx.Image from stream data
                img = wx.ImageFromStream(StringIO(fil.getvalue()))
                
                self.actual_image = None
                if not self.actual_image:
                        # scale the image
                        img = self.calNewHW(img)
                else: self.scale = 1
                
                self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
                self.imageCtrl.Refresh()
                size_str_new = str(self.W) + 'x' + str(self.H)
                
                cur_label = self.imageLabel.GetLabel()
                if not isQR:
                        pattern = re.compile('.*\.\w{3,4}\s{4}[0-9]+x[0-9]+')                        
                        size_str_old = re.match(pattern, cur_label).group().split()[-1]                        
                        previewLabel = u"(预览)" + cur_label.replace(size_str_old, size_str_new).replace(u"(预览)" ,"")
                else:
                        previewLabel = u"(预览)未命名.png" + 4 * ' ' + size_str_new + 4 * ' ' + str(self.convertSize(fil.len)) 
                self.imageLabel.SetLabel(previewLabel)

                # update resize part
                self.updateResizeBox()
                self.Refresh()
                
                if self.txtDlg:
                        if self.txtDlg.textRepeatCtrl.GetValue() == u'一次 -> 按鼠标指定位置':
                                pub.sendMessage("set status", msg = u"小提示：当前水印设置(按鼠标指定位置)下，裁剪功能已被禁用o_O")
                        else: pub.sendMessage("set status", msg = u"小提示：预览状态下，裁剪功能已激活。")
                                
                else: pub.sendMessage("set status", msg = u"小提示：预览状态下，裁剪功能已激活。")
                
                pub.sendMessage("resize", msg = "")
        #---------------------------------------------------------------------------
        def wand2pil(self, im, ext):
                """
                converter between PIL image object and Wand image object
                PIL Image <---------> wand Image
                """
                fil = StringIO()
                if not self.current_dpi: self.current_dpi = (96, 96)
                if isinstance(im, PngImageFile): # PIL Image instance                 
                        fil = self.saveToFil(im, ext) #, dpi = self.current_dpi)
                        return wImage(blob = fil.getvalue(), format = ext) 
                        
                elif isinstance(im, wImage):
                        im.resolution = self.current_dpi[0]
                        im.compression_quality = 99
                        im.save(fil)
                        return Image.open(StringIO(fil.getvalue()))
                else: # isinstance(im, Image.Image):                        
                        fil = self.saveToFil(im, "." + ext) #, dpi = self.current_dpi)
                        return wImage(blob = fil.getvalue(), format = ext) 
                        
                #fil.close() # free buffer
        #--------------------------------------------------------------------------- 
        def convertSize(self, size):
                """
                Convert from bytes to KB, MB, GB, etc
                """
                size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
                i = int(math.floor(math.log(size,1024)))
                p = math.pow(1024,i)
                s = round(size/p,2)
                if (s > 0):
                        return '%s %s' % (s,size_name[i])
                else:
                        return '0B'
        #---------------------------------------------------------------------------    
        def resizeImg(self, path, size_limit):
                """
                The main entry for jpg image resize thread
                """                
                self.count = 0 # reset the counter
                ### send msg to listener to get new base update
                #pub.sendMessage("get new path", msg = self.theImg)
                if path and os.path.isfile(path):
                        self.img_ext = os.path.splitext(path)[1]
                        EXT = self.img_ext
                        self.current_dpi = self.getSettingDPI(path)
               
                if not isinstance(size_limit, int):  #-->For image cropping                               
                        (base, jpgfile) = os.path.split(path)
                       
                        self.filepathnew = os.path.join(self.path_base_new, jpgfile)
                        if self.imageLabel.GetLabel().startswith(u"(预览)"):
                                im = self.im_preview
                        else:
                                im = self.imageOpen(path)
                        im_cropped = im.crop(size_limit)
                        
                        try:
                                #im_cropped.save(self.filepathnew, EXT)
                                if self.saveToFile(im_cropped, EXT, self.filepathnew, True):
                                        w, h = im_cropped.size
                                        pub.sendMessage("set status", msg = u"文件已保存: " + self.filepathnew + " (尺寸：" + str(w) + "x" + str(h) + u" 像素)") # reset status bar
                        except IOError, e:
                                err_dlg = wx.MessageBox(u"出错啦！\r\n\r\n原因: " + str(e), wx.OK | wx.ICON_ERROR)
                                err_dlg.ShowModal()
                        finally: return
                        
                elif self.option == 2:  # path is dir
                        try:               
                                for filename in self.picPaths:
                                        if not self.isCancel and not self.isDone:                                                
                                                (base, jpgfile) = os.path.split(self.force2unicode(filename))                                                
                                                self.fileResize(base, jpgfile)
                                self.isDone = True
                        except Exception, e:  self.isException = True
                       
                elif self.option == 1:  # path is file
                        (base, jpgfile) = os.path.split(path)
                        self.fileResize(base, jpgfile)
                        self.isDone = True
                        
                elif self.option == 3:
                        for filename in self.jpgfilelist:
                                if not self.isCancel and not self.isDone:                                              
                                        self.fileResize(filename[0], filename[1])
                                        
                        self.isDone = True
                        
                else:  pass # Undefined option
                # 'show result windows'
                if self.option: self.showResultDlg() 

        #---------------------------------------------------------------------------
        def buildFileList(self):
                """
                Constructor to build all jpg list (in sub dir also)
                """
                self.isBuildDone = False
                
                for root, dirnames, filenames in os.walk(os.path.dirname(self.theImg)):
                        
                        for f in filenames:                                
                                if os.path.splitext(f)[1].upper() in PIC_LIST: #== '.jpg':
                                        self.jpgfilelist.append((root, f))                                                           
                self.isBuildDone = True
                self.totalPics = len(self.jpgfilelist)
                
                # update status bar
                pub.sendMessage("set status", msg = u"文件列表准备完毕！共有图片：" + str(len(self.jpgfilelist)) + u"张。")
        #---------------------------------------------------------------------------
        def getNewPathBase(self, msg=""):
                # prepare the base dir to save jpg files                
                cur_dir = os.path.dirname(msg)
                
                if self.save_dir == '':
                        self.mkDir(cur_dir + '\\NEW')
                        self.path_base_new = self.force2unicode(cur_dir +  '\\NEW')
                else:
                        self.path_base_new = self.save_dir
                
        #---------------------------------------------------------------------------
        def mkDir(self, new_path):
                """Create the new dir if not exists"""
                
                if not os.path.exists(new_path):
                        os.makedirs(new_path)
        #---------------------------------------------------------------------------        
        def updateEvent(self):
                """Notify the listener to update"""
                
                pub.sendMessage('update', msg = '')

        #---------------------------------------------------------------------------    
        def tryResize(self, im, quality_val, filepath):
                """Part 1 of smart resize image"""
                
                self.retry  = self.retry + 1 # counter up by 1
                fil = StringIO()
                im.save(fil, 'JPEG', quality = quality_val, dpi = self.current_dpi) #save to buffer
                ratio = (float)(fil.len/(float)(self.size_limit * 1024))
                
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

                if self.retry <= 50: # try maximun 50 times
                        self.tryResize(im, quality_val, filepath)
                else:
                        self.largeJpgList.append((os.path.basename(filepath), os.path.getsize(filepath)))
                        self.updateEvent() 

        #---------------------------------------------------------------------------
        def tryResize2(self, im, value):
                """Part 2 of smart resize image"""                
                
                fil = StringIO() 
                for quality_val in range(value, 1, -1):
                        
                        im.save(fil, 'JPEG', quality = quality_val, dpi = self.current_dpi) #save to buffer
                        if fil.len <= self.size_limit * 1024:    # is the new image file size <= size_limit
                                # if yes, then save the new image to new file: filepathnew
                                im.save(self.filepathnew, 'JPEG', quality=quality_val, dpi = self.current_dpi)
                                self.updateEvent()
                                break;                          # Stop the for loop
                        else:
                                fil = StringIO()       # reset the buffer
        #---------------------------------------------------------------------------
        def handleResize(self, im):
                ratio = (float(self.ctrlWidth.GetValue()) / float(self.ctrlHeight.GetValue())) / (float(im.size[0])/ float(im.size[1]))
                # "ratio=", ratio
                if self.selectBox.GetValue() != u'限制大小':
                        if self.PnPBox.GetValue() ==  u'按百分比':                                
                                newWidth, newHeight = im.size[0] * int(self.ctrlWidth.GetValue())/100, im.size[1] * int(self.ctrlHeight.GetValue())/100
                        elif  round(ratio, 2) == 1.0:
                                newWidth, newHeight = int(self.ctrlWidth.GetValue()), int(self.ctrlHeight.GetValue())
                        elif  round(ratio, 2) < 1.0:
                                newWidth, newHeight = int(self.ctrlWidth.GetValue()), int(self.ctrlWidth.GetValue()) * im.size[1] / im.size[0]
                        else:
                                newWidth, newHeight = int(self.ctrlHeight.GetValue()) * im.size[0] / im.size[1], int(self.ctrlHeight.GetValue())                        
                        # is png file format
                        if self.img_ext == '.PNG': im = self.pngResize(im)
                        if im:  im_resized = im.resize((newWidth, newHeight), Image.ANTIALIAS)
                        else: im_resized = None
                        
                if self.selectBox.GetValue() == u'调整尺寸':
                        return im_resized, False
                elif self.selectBox.GetValue() == u'限制大小':
                        return im, True                 
                else: #u'调整并限制'
                        return im_resized, True                 
        #---------------------------------------------------------------------------
        def pngResize (self, img):
                """ img: Image instance """
                import numpy
                try:
                        premult = numpy.fromstring(img.tostring(), dtype=numpy.uint8)
                        alphaLayer = premult[3::4] / 255.0
                        premult[::4] *= alphaLayer
                        premult[1::4] *= alphaLayer
                        premult[2::4] *= alphaLayer
                        return Image.fromstring("RGBA", img.size, premult.tostring())
                except ValueError, e:
                        statusmsg = self.status.GetStatusText()
                        pub.sendMessage("set status", msg = statusmsg + u"...出错啦： " + e.message )
                        return None
                        
        #--------------------------------------------------------------------------
        def force2unicode(self, string):
                if 'unicode' not in str(type(string)):
                        try: return  unicode(string, 'cp936')
                        except: return string
                else: return string
        def cutLongPathShort(self, longPath, _max):
                """ Cut the path string if it is too long """
                if len(longPath) > _max:
                        separator = "\\...\\"
                        max_len = _max - len(separator)
                        start = max_len/2
                        trunc = len(longPath) - max_len
                        substr = longPath[start : start + trunc]
                        return longPath.replace(substr, separator)
                else:   return longPath
                
        #---------------------------------------------------------------------------
        def fileResize(self, base, jpgfile):
                """Module to resize a single image file"""

                filepath = os.path.join(base, jpgfile)
                
                if self.totalPics: pre_msg = "[" + str(self.count + 1) + "/" + str(self.totalPics) + "]"
                else: pre_msg = ""
                wh = self.parent.Size
                
                msg = pre_msg + u"正在处理图片：" + self.cutLongPathShort(filepath, wh[0]/10)
                pub.sendMessage("set status", msg = msg)
 
                self.current_dpi = self.getSettingDPI(filepath)                
                self.img_ext = os.path.splitext(jpgfile)[1]
                EXT = self.img_ext

                try:            
                        im = self.imageOpen(filepath) 
                        self.filepathnew = os.path.join(self.path_base_new, jpgfile)                        
  
                        if self.selectBox.GetValue() == u'添加特效':
                                self.picGUI.DoEffects(filepath, self.filepathnew, False)
                                self.updateEvent()    
                        elif self.selectBox.GetValue() == u'查看备注':
                                if self.commentDlg:
                                        new_comment =  self.commentDlg.m_newRichText.GetValue().encode("cp936")
                                        self.commentDlg.setComment(filepath, new_comment)                                        
                                        self.updateEvent()
                        elif self.selectBox.GetValue() == u'ASCII图形':
                                self.ascGUI.AutoSave(filepath, self.filepathnew + ".txt")
                                self.updateEvent()
                        else:                                
                                fil = StringIO()
                                im, onFlag = self.handleResize(im)
                                fil = self.saveToFil(im, EXT) #'JPEG')
                                
                                if not im:
                                        self.updateEvent() # process error
                                
                                elif not onFlag:
                                        self.saveToFile(im, EXT, self.filepathnew) #'JPEG')
                                        self.updateEvent()
                                        #return
                                elif fil.len <= self.size_limit * 1024:
                                        self.saveToFile(im, EXT, self.filepathnew) #'JPEG') #, quality=quality_val)
                                        self.updateEvent()                                        
                                else:    
                                        if os.stat(filepath).st_size <= self.size_limit * 1024:
                                                #不同名就复制；同名就跳过
                                                if filepath != self.filepathnew:  copy(filepath, self.filepathnew) 
                                                self.updateEvent() 
                                        else: #if not self.isCancel:
                                                self.NeedMoreResize(im, filepath)                        
                except IOError:
                        self.updateEvent()                        
                        
                except Exception, e:
                        self.mkDir(self.path_base_new) # in case the dir is deleted by user
                        self.isException = True #print 'Problem occurred when processing ', filepath, ':', e
                        self.exceptionFileList.append(filepath)
                        self.updateEvent()
                        #pub.sendMessage("set status", msg = u"出现异常： " + e.message)
        #---------------------------------------------------------------------------
        def NeedMoreResize(self, im, filepath):
                """Check if the minimum quality of 1 can meet the """
                
                fil = StringIO()
                im.save(fil, 'JPEG', quality = 1, dpi = self.current_dpi)
                if fil.len == self.size_limit * 1024:
                        im.save(self.filepathnew, 'JPEG', quality= 1, dpi = self.current_dpi )
                        self.updateEvent()   
                elif  fil.len > self.size_limit * 1024:
                        self.largeJpgList.append((os.path.basename(filepath), fil.len))
                        self.updateEvent()   
                else:
                        self.retry = 0 # reset counter
                        self.tryResize(im, JPG_QTY_MAX, filepath)

        #--------------------------------------------------------------
        def readWandImage(self, fileIn, ext = None):
                """ Wand Image object read"""
                if not ext: 
                        ext = os.path.splitext(fileIn)[1]
                ext = self.getEXT (ext).lower()
                fileIn = self.force2unicode(fileIn)

                with open(fileIn, 'rb') as f :
                        try:
                                wand_im = wImage(file = f, format = ext)
                        except Exception, e:
                                pub.sendMessage("set status", msg = u"读取水印图片时出错: " + e.message)
                                return None
                return  wand_im

        def writeWandImage(self, fileOut, img, ext):
                """ Wand Image object write"""
                ext = ext[1:].lower() 
                img.resolution = self.current_dpi[0]
                img.compression_quality = 99
                img.format = ext
                fileOut = self.force2unicode(fileOut)
                try:
                        with open(fileOut, 'wb') as f :
                                img.save(file = f)
                except Exception, e:
                        pub.sendMessage("set status", msg = u"保存图片时出错: " + e.message)

                
########################################################################
class ViewerFrame(wx.Frame):
        """
        Main Frame Constructor
        """

        #----------------------------------------------------------------------
        def __init__(self):
                """Constructor"""
                
                wx.Frame.__init__(self, None, title=u"JPGTools 1.0.0", style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL)
                global midi, splash ## define variable icon

                self.panel = ViewerPanel(self)
                self.SetBackgroundColour(wx.NullColour) # replace default dark gray color
                
                self.initToolbar()
                self.sizer = wx.BoxSizer(wx.VERTICAL)
                self.sizer.Add(self.panel, 1, wx.EXPAND)
                self.SetSizer(self.sizer)
                
                dt1 = FileDropTarget(self.panel)
                self.panel.SetDropTarget(dt1)
                
                #close event
                self.Bind(wx.EVT_CLOSE, self.onClose)               
                if [self.panel.framePosX, self.panel.framePosY] == [0, 0]: self.Center()
                else:
                        ## user customized postion
                        self.SetPosition((self.panel.framePosX, self.panel.framePosY))
                        
                pub.subscribe(self.resizeFrame, ("resize"))
                self.sizer.Fit(self)
                        
                # Close splash and show main gui
                if splash : splash.Destroy()
                self.Show()     
        #----------------------------------------------------------------------
        def onClose(self, event = None):
                """
                Event handler when main window is closing
                Save all user config settings
                """
                self.panel.framePosX, self.panel.framePosY = self.GetPosition() # get current pos
                pub.sendMessage("set status", msg = u"正在保存设置...")
                self.panel.writeFile() #update config file
                pub.sendMessage("set status", msg = u"正在生成注册表文件...")
                self.makeRegFile()                
                self.DestroyChildren()
                self.Destroy()        
        #----------------------------------------------------------------------
        def makeRegFile(self):
                """
                Constructor to make our registry file
                """
                if self.panel.make_reg == 'YES':                        
                        with codecs.open(REGFILE, 'wb', 'utf-16') as regfile:
                                exename = sys.argv[0].decode('cp936').replace("\\", "\\\\")
                                regfile.write(REGDATA.replace('XX', exename))                              
                
        #----------------------------------------------------------------------
        def initToolbar(self):
                """
                Initialize the toolbar
                """
                toolbar = self.CreateToolBar()                
                toolbar.SetToolBitmapSize((16,16))  
                
                open_ico = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (16,16))                
                self.openTool = toolbar.AddSimpleTool(wx.ID_ANY, open_ico, r"打开图片所在目录 ALT+O", "", 0)                
                self.Bind(wx.EVT_MENU, self.onOpenDirectory, self.openTool)
                                                
                recent_ico = iconfile.getRecent.GetBitmap()
                recentTool = toolbar.AddSimpleTool(wx.ID_ANY, recent_ico, "最近打开目录", "", 0)
                self.Bind(wx.EVT_MENU, self.openRecent, recentTool)

                toolbar.AddSeparator()
                
                save_ico = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, (16,16))
                saveTool = toolbar.AddSimpleTool(wx.ID_ANY, save_ico, r"自定义保存路径  ALT+D", "", 0)
                self.Bind(wx.EVT_MENU, self.onSaveDirectory, saveTool)
                                                
                browse_ico = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_TOOLBAR, (16,16))
                browseTool = toolbar.AddSimpleTool(wx.ID_ANY, browse_ico, r"浏览保存目录  ALT+B", "", 0)
                self.Bind(wx.EVT_MENU, self.onBrowseDirectory, browseTool)
                
                toolbar.AddSeparator()
                
                paste_ico = wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR, (16,16))
                pasteTool = toolbar.AddSimpleTool(wx.ID_ANY, paste_ico, r"从剪贴板粘贴  CTRL+V", "", 0)
                self.Bind(wx.EVT_MENU, self.onPaste, pasteTool)
                
                self.Bind(wx.EVT_ACTIVATE, self.onActive)
                
                cut_ico = wx.ArtProvider.GetBitmap(wx.ART_CUT, wx.ART_TOOLBAR, (16,16))
                cutTool = toolbar.AddSimpleTool(wx.ID_ANY, cut_ico, r"裁剪并保存  CTRL+X", "", 0)
                self.Bind(wx.EVT_MENU, self.onCut, cutTool)
                                                
                saveAs_ico = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_TOOLBAR, (16,16))                
                saveAsTool = toolbar.AddSimpleTool(wx.ID_ANY, saveAs_ico, r"另存为  ALT+S", "", 0)
                self.Bind(wx.EVT_MENU, self.onSaveAs, saveAsTool)
                
                toolbar.AddSeparator()
                
                effect_ico = iconfile.e.GetBitmap()
                effectTool = toolbar.AddSimpleTool(wx.ID_ANY, effect_ico, r"图片特效  ALT+E", "", 0)
                self.Bind(wx.EVT_MENU, self.onEffect, effectTool)            
                
                convert_ico = iconfile.convert.GetBitmap()
                convertTool = toolbar.AddSimpleTool(wx.ID_ANY, convert_ico, r"格式转换  ALT+C", "", 0)
                self.Bind(wx.EVT_MENU, self.onConvert, convertTool)                
                
                qr_ico = iconfile.qr.GetBitmap() #getQR.GetBitmap()
                qrTool = toolbar.AddSimpleTool(wx.ID_ANY, qr_ico, r"生成二维码  ALT+Q", "", 0)
                self.Bind(wx.EVT_MENU, self.onQR, qrTool)
                
                toolbar.AddSeparator()
                
                colorPicker_ico = iconfile.colorPicker.GetBitmap()
                self.colorPickTool = toolbar.AddSimpleTool(wx.ID_ANY, colorPicker_ico, "连续拾取像素", "", wx.ALIGN_RIGHT)
                
                #                
                self.mode_btn = wx.ToggleButton( toolbar, wx.ID_ANY, u"+1", wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER | wx.BU_EXACTFIT )
                toolbar.AddControl(self.mode_btn)
                self.mode_btn.Bind(wx.EVT_TOGGLEBUTTON, self.OnMode)
                self.mode_btn.SetToolTipString(u"打开单文件模式")
                toolbar.AddSeparator()
                #                
                self.actual_btn = wx.Button( toolbar, wx.ID_ANY, u" "*10, wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER | wx.BU_EXACTFIT )
                toolbar.AddControl(self.actual_btn)
                self.actual_btn.Bind(wx.EVT_BUTTON, self.OnRestore)
                self.Bind(wx.EVT_IDLE, self.updatePercentInfo)
                
                help_ico = wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_TOOLBAR, (16,16))
                helpTool = toolbar.AddSimpleTool(wx.ID_ANY, help_ico, r"关于  F1", "", 0)
                self.Bind(wx.EVT_MENU, self.onHelp, helpTool)
                #
                # Handle escape key press
                self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
                # Handle Zoom in and out
                self.Bind(wx.EVT_MOUSEWHEEL, self.OnScroll)

                id_list = [ pasteId, openId, saveId, browseId, cutId, saveAsId, effectId, convertId, qrId,  helpId, restoreId, applyId, deleteId, copyId, 
                rightId, leftId, upId, downId] = [ wx.NewId() for i in xrange(18)]
                id_data = [(self.onPaste, wx.ACCEL_CTRL,  ord('V')),
                (self.onOpenDirectory,  wx.ACCEL_ALT, ord('O')),
                (self.onSaveDirectory,   wx.ACCEL_ALT, ord('D')),
                (self.onBrowseDirectory,  wx.ACCEL_ALT, ord('B')),
                (self.onCut,  wx.ACCEL_CTRL, ord('X')),
                (self.onSaveAs,  wx.ACCEL_ALT, ord('S')),
                (self.onEffect,  wx.ACCEL_ALT, ord('E')),
                (self.onConvert, wx.ACCEL_ALT, ord('C')),
                (self.panel.onQR, wx.ACCEL_ALT, ord('Q')),
                (self.onHelp, wx.ACCEL_NORMAL, wx.WXK_F1),
                (self.OnRestore, wx.ACCEL_NORMAL, wx.WXK_F11),
                (self.panel.OnApply, wx.ACCEL_ALT, ord('A')),
                (self.OnDelete, wx.ACCEL_NORMAL, wx.WXK_DELETE),
                (self.onCopy, wx.ACCEL_CTRL, ord('C')),
                (self.panel.nextPicture, wx.ACCEL_NORMAL, wx.WXK_RIGHT),
                (self.panel.previousPicture,  wx.ACCEL_NORMAL, wx.WXK_LEFT),
                (self.panel.onSlideShow, wx.ACCEL_NORMAL, wx.WXK_UP),
                (self.panel.onSlideShow, wx.ACCEL_NORMAL, wx.WXK_DOWN)]
                
                [self.Bind(wx.EVT_MENU, id_data[i][0], id = id_list[i]) for i in xrange(18)]                
                accel_tbl = wx.AcceleratorTable([(id_data[i][1], id_data[i][2], id_list[i]) for i in xrange(18)]) 
                self.SetAcceleratorTable(accel_tbl)
                
                toolbar.Realize()                
                
        def onActive(self, event):
                pass
        
        def OnMode (self, event):
                if self.panel.imageLabel.GetLabel().startswith( u'(预览)未命名.png'):
                        pub.sendMessage("set status", msg = u"请先保存二维码图片，再进行此操作。")
                        self.mode_btn.SetValue(False)
                else:
                        self.panel.singleMode = self.mode_btn.GetValue()
                        self.mode_btn.SetLabel('1'* self.panel.singleMode + '+1' * (not self.panel.singleMode))
                        self.mode_btn.SetToolTipString(u"打开单文件模式" * (not self.panel.singleMode)+ u"关闭单文件模式" * self.panel.singleMode)
                        pub.sendMessage("set status", msg = "OnMode")
        
        def setBtnPercent (self, tooltip, per = "100%"):
                if self.actual_btn.GetLabel() != per:
                        self.actual_btn.SetLabel(per)
                        self.actual_btn.SetToolTipString(tooltip)                
        
        def updatePercentInfo (self, event):
                """Update percentage info when frame is idle"""

                if self.panel.actual_image:
                        self.panel.scale = 1
                        self.setBtnPercent(u"退出原始尺寸  F11", "100%")
                elif self.panel.scale:
                        per = int(100 /self.panel.scale)
                        if per != 100:
                                self.panel.actual_image = False

                                self.setBtnPercent(u"显示原始尺寸  F11", str(per) + "%")
                        else:
                                self.panel.actual_image = True
                                self.setBtnPercent(u"退出原始尺寸  F11", "100%")
        
        def OnRestore (self, event):                
                self.panel.actual_image = not self.panel.actual_image                
                self.panel.imgReload()
                self.panel.rubber.crop = None # reset crop when zooming
        
        def OnScroll(self, event):
                """Scale the image display when mouse wheel scrolling..."""                
                # this breaks the full mode                
                if self.panel.actual_image: self.panel.actual_image = False
                self.panel.scrolls_new = self.panel.scrolls + int(event.GetWheelRotation()/120)
                self.panel.scrolls_new = sorted( [0, self.panel.scrolls_new, 400])[1]
                if self.panel.scrolls != self.panel.scrolls_new:
                        self.panel.scrolls = self.panel.scrolls_new
                        self.panel.imgReload()
                self.panel.rubber.crop = None # reset crop when zooming
        
        def onCopy (self, event):
                if self.panel.rubber.crop:
                        self.imgToClipboard(self.panel.rubber.crop)
                        pub.sendMessage("set status", msg = u"选中区域已复制到剪贴板。")
                        self.panel.rubber.crop = None # clear the crop rect
                else:
                        self.imgToClipboard()
                        pub.sendMessage("set status", msg = u"整个图片已复制到剪贴板。")
                        
        def imgToClipboard(self, bbox = None):
                fil = StringIO()
                im = self.panel.imageOpen(self.panel.picPaths[self.panel.currentPicture]).convert("RGB")
                if bbox: im.crop(bbox).save(fil, 'BMP')
                else: im.save(fil, 'BMP')
                #if not wx.TheClipboard.IsOpened(): wx.TheClipboard.Open()
                clipdata = wx.BitmapDataObject()
                clipdata.SetData(fil.getvalue()[14:])
                # The file header offset of bmp is 14 bytes; 
                wx.TheClipboard.Open()
                wx.TheClipboard.SetData(clipdata)
                wx.TheClipboard.Close()
        def OnDelete (self, event):
                dlg = wx.MessageDialog(None, u'确实要把当前文件放入回收站吗？', u'删除文件', style= wx.YES_NO | wx.YES_DEFAULT)
                if dlg.ShowModal() == wx.ID_YES: self.recycleImage()  
                
        def OnKeyDown(self, event):
                #self.ctrl_down = event.ControlDown()
                if event.GetKeyCode() == wx.WXK_ESCAPE: self.onClose() # ESC to close    

        def recycleImage(self, isRecycle = True):
                if isRecycle: send2trash(self.panel.picPaths[self.panel.currentPicture])
                self.panel.picPaths.pop(self.panel.currentPicture)                               
                pub.sendMessage("update images", msg = self.panel.getPicPaths())
                        
        def onQR (self, event = None):
                """
                Show QR window
                """
                if not self.panel.qrDlg:
                        self.panel.qrDlg = MyQRDialog(self)
                        self.panel.setFontDlgPos(self.panel.qrDlg)                                        
                else:
                        self.panel.setFontDlgPos(self.panel.qrDlg)
        
        def onPicker(self):
                # 只在非预览下拾取像素
                if self.panel.imageLabel.GetLabel().startswith(u"(预览)"):
                     pub.sendMessage("set status", msg = u"小提示：预览状态下，像素拾取已被禁用。")   
                      
        def openRecent(self, event):
                tool_recent = event.GetEventObject()
                pos = (tool_recent.GetPosition()[0] + 22, tool_recent.GetPosition()[1] + tool_recent.GetSize()[1] - 2)
                
                menu = wx.Menu()
                self.emtpy = None                
                
                if self.panel.stack.isEmpty():
                        self.empty = menu.Append(0, "(没有历史记录)")
                else:
                        for i in range(self.panel.stack.topOfStack()):
                                item  = menu.Append( -1, str(i + 1) + '. ' + self.panel.stack.items[self.panel.stack.topOfStack() - i -1])                
                                self.Bind(wx.EVT_MENU, self.onItemSelected, item)
                self.PopupMenu(menu, pos)
                
        def onItemSelected(self, event):
                menu = event.GetEventObject()
                item = menu.FindItemById(event.GetId())
                self.panel.open_dir = item.GetText()[3:] # remove the num prefix          
                pub.sendMessage("update images", msg = self.panel.getPicPaths())
                
        #----------------------------------------------------------------------
        def onPaste(self, event):
                #self.panel.comboBox.Enable(False)
                img = ImageGrab.grabclipboard()
                from PIL.BmpImagePlugin import DibImageFile
                dpi = (self.panel.default_dpi, self.panel.default_dpi) # default should be added
                
                if isinstance(img, DibImageFile):  
                        untitled_pic = os.path.join(self.panel.open_dir, u"新建图片.PNG")
                        img.save(untitled_pic, 'PNG', compress_level = 0, dpi = dpi) # modified on 2015-11-10
                        # above from: http://pillow.readthedocs.org/en/3.0.x/handbook/image-file-formats.html
                        picPaths = [untitled_pic]
                        pub.sendMessage("update images", msg = picPaths)
                        #self.imgPreview(img, '.jpg', True)
                        
                        pub.sendMessage("set status", msg = u"文件已保存：" +
                                        untitled_pic + u"。 您可以继续编辑...")
                else:
                        pub.sendMessage("set status", msg = u"剪贴板中没有图像数据。")
                        
        def onCut(self, event):
                if    self.panel.totalPictures > 0:   self.panel.doImgCut()
                
        def onConvert(self, event):
                if    self.panel.totalPictures > 0:  self.panel.callConvertDialog()
                
        def onEffect (self, event):
                self.panel.selectBox.SetValue(u'添加特效')
                self.panel.toggleUpThree(u'添加特效') 
                self.panel.doJpgWork()
        
        def dirProcess(self, _dir):
                _dirItemList = _dir.split("\\")
                if _dirItemList[-1] != _dirItemList[-2]: return _dir, os.path.isdir (_dir)
                elif os.path.isdir (_dir):  return _dir, True
                else:
                        _dirItemList.pop()
                        new_dir = "\\".join(_dirItemList)
                        if os.path.isdir (new_dir):  return new_dir, True
                        else: return _dir, os.path.isdir (_dir)
                        
                
        #----------------------------------------------------------------------
        def onOpenDirectory(self, event):
                """
                Opens a DirDialog to allow the user to open a folder with pictures
                """
                dlg = wx.DirDialog(None, "打开图片所在目录", defaultPath = self.panel.open_dir, name = '', style=1)
               
                if dlg.ShowModal() == wx.ID_OK:
                        newDir, isDir = self.dirProcess(dlg.GetPath())
                        if isDir:                        
                                #self.folderPath = dlg.GetPath()
                                self.panel.open_dir = newDir #self.folderPath
                                self.panel.currentPicture = 0   
                                pub.sendMessage("update images", msg = self.panel.getPicPaths()) #picPaths)                                
                        else:                                
                                pub.sendMessage("set status", msg = u"指定的目录不存在：" + newDir) #dlg.GetPath())
                dlg.Destroy()
                                
        def onBrowseDirectory(self, event):
                """ Open the saved dir"""

                if self.panel.path_base_new:
                        os.startfile(self.panel.path_base_new)
                        #subprocess.Popen('explorer /e:, ' + self.panel.path_base_new)
                event.Skip()
                        
        #----------------------------------------------------------------------
        def onSaveDirectory(self, event):
                """
                For users who wish to define their own save path
                """
                dlg = wx.DirDialog(self, "自定义保存路径", defaultPath = self.panel.save_dir,
                                   style = wx.DD_DEFAULT_STYLE)
                
                if dlg.ShowModal() == wx.ID_OK:
                        self.panel.save_dir = dlg.GetPath()
                        pub.sendMessage("set status", msg = u"自定义保存路径: " + dlg.GetPath())
                        self.panel.mkDir(self.panel.save_dir) 
                        self.panel.path_base_new = self.panel.save_dir
        #---------------------------------------------------------------------
        def onSaveAs (self, event):                
                if not self.panel.im_preview and not self.panel.getCurJpg():
                        pub.sendMessage("set status", msg = u"没有图片可以保存，当前操作已取消。")
                else:
                        wildcard = u"JPEG 图片 (*.jpg)|*.jpg|BMP 图片 (*.bmp)|*.bmp|PNG 图片 (*.png)|*.png|" +\
                                u"GIF 图片 (*.gif)|*.gif|TIF 图片 (*.tif; *.tiff)|*.tif; *.tiff" 
                                
                        dlg = wx.FileDialog(self, u"文件另存为", self.panel.save_dir, "", wildcard, \
                                            wx.SAVE|wx.OVERWRITE_PROMPT)
                        result = dlg.ShowModal()
                        fileIn = dlg.GetPath()
                        dlg.Destroy()
                        
                        if result == wx.ID_OK:          #Save button was pressed
                                ext = os.path.splitext(fileIn)[1]
                                        
                                if self.panel.im_preview:                                        
                                        im = self.panel.im_preview
                                else:
                                        im = self.panel.imageOpen(self.panel.picPaths[self.panel.currentPicture])
                                
                                if self.panel.saveToFile(im, ext, fileIn, True):
                                        pub.sendMessage("set status", msg = u"恭喜！文件保存成功：" + fileIn)
                                        if self.panel.imageLabel.GetLabelText().startswith(u"(预览)未命名.png" ):
                                                # load the QR image
                                                pub.sendMessage("update images", msg = [ fileIn ])
                                        # open saved folder in explorer
                                        subprocess.Popen(ur'explorer /select, "{}"'.format(fileIn))

                        elif result == wx.ID_CANCEL:    #Either the cancel button was pressed or the window was closed
                                pass
                
        #----------------------------------------------------------------------               
        def resizeFrame(self, msg=None):
                """Resize to fit the Frame"""
                
                self.sizer.Fit(self)
                
        def onHelp (self, event):
                MyAboutDialog(self).Show()

                
########################################################################
class WarningDialog(wx.Dialog):
    """
    Dialog to remind user sub dir option may take a while to finish
    """

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        
        wx.Dialog.__init__(self, parent = parent, title = u'友情提示',size = (250, 95))
        vbox = wx.BoxSizer(wx.VERTICAL)
        stline = wx.StaticText(self, -1, u'该操作可能需要较长时间。继续？', (90, 15))
        vbox.Add(stline, 1, wx.ALIGN_LEFT | wx.TOP, 5)        
        
        btnOk = wx.Button(self, wx.ID_OK, label = u'知道了', size = (68, -1))
        btnCancel = wx.Button(self, wx.ID_CANCEL, label = u'不玩了', size = (68, -1))

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add((80, -1))
        btnSizer.Add(btnOk, 0, wx.ALL, border = 5)
        btnSizer.Add(btnCancel,  0, wx.ALL, border = 5)
        #btnSizer.Realize()
        vbox.Add(btnSizer)
        self.SetSizer(vbox)

##################################################################
class FileDropTarget(wx.FileDropTarget):
        """Handler to support drag 'n drop """
        
        def __init__(self, window):
                wx.FileDropTarget.__init__(self)
                self.window = window                
                
        def OnDropFiles(self,x, y, filenames):
                # convert to unicode
                filenames = [unicode(f,'cp936') if 'str' in str(type(f)) else f for f in filenames]

                picPaths = []
                if os.path.isdir(filenames[0]):
                        for ext in PIC_LIST:
                                picPaths += glob.glob(filenames[0] + "\\*" + ext)
                        picPaths = [unicode(p, 'cp936') if 'str' in str(type(p)) else p for p in picPaths]
                elif [os.path.isfile(a) for a in filenames] == [True] * len(filenames):
                        picPaths = filenames
                else: return  
                        
                if len(picPaths) > 0:
                        pub.sendMessage("update images", msg = picPaths)
                        
                else: pub.sendMessage("set status", msg = u"亲，您确定拖放的文件/目录有图片可以加载吗？")
                
##################################################################
class ListPrepDialog(wx.Dialog):
        """
        Dialog for jpg list preparing...
        """
        #-------------------------------------------------------------
        def __init__(self, parent):
                """Constructor"""
                wx.Dialog.__init__(self, parent, title=u'正在准备文件列表。请稍候...', size=(350, 120))
                self.SetIcon(midi)
                
                self.count = 0
                self.timer = wx.Timer(self)
                #self.timer.Interval = 10
                self.Bind(wx.EVT_TIMER, self.updatePrepDlg, self.timer)
                sizer = wx.BoxSizer(wx.VERTICAL)                
                
                lbTop = wx.StaticText(self, label="")        
                sizer.Add(lbTop, 0, wx.TOP, 10 )
                
                self.progress = wx.Gauge(self, range = 50, size=(-1, 20))        
                sizer.Add(self.progress, 0, wx.EXPAND)
                
                cancelBtn = wx.Button(self, label = u'取消', size = (68, -1))
                cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancel)
                
                sizer.Add(cancelBtn, 0, wx.CENTER | wx.TOP, 15)
                self.SetSizer(sizer)
                self.timer.Start(1000)

        #----------------------------------------------------------
        def updatePrepDlg(self, event):
                """
                Update the progress bar
                """
                if self.IsActive:
                        self.count += 1
                        
                        if not self.Parent.isBuildDone and not self.Parent.isCancel:
                                if self.count == 50:
                                        self.count = 0
                                else:
                                        self.progress.SetValue(self.count)  
                        else:
                                self.timer.Stop()
                                self.Destroy()
                                
        #------------------------------------------------------------
        def OnCancel(self, parent):                
                self.Parent.isCancel = True
                pub.sendMessage("set status", msg = u"当前操作已被取消。")
                self.Destroy()                

##################################################################
class MyProgressDialog(wx.Dialog):
        """
        Progress dialog
        """
        #-------------------------------------------------------------
        def __init__(self, parent):
                """Constructor"""
                self.parent = parent
                wx.Dialog.__init__(self, parent, title=u'正在处理图片文件列表。请稍候...', size=(350, 120))
                self.SetIcon(midi)
                
                self.count = 0
                sizer = wx.BoxSizer(wx.VERTICAL)                
                
                lbTop = wx.StaticText(self, label="")        
                sizer.Add(lbTop, 0, wx.TOP, 10 )
                
                self.progress = wx.Gauge(self, range = self.parent.progress_max, size=(-1,20))
                self.progress.SetBezelFace(1)
                self.progress.SetShadowWidth(1)
                sizer.Add(self.progress, 0, wx.EXPAND)
                
                cancelBtn = wx.Button(self, label = u'取消', size = (68, -1))
                cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancel)
                #sizer.Add((-1, 50))
                sizer.Add(cancelBtn, 0, wx.CENTER | wx.TOP, 15)
                self.SetSizer(sizer)
                
                # create a pubsub listener
                pub.subscribe(self.updateProgress, 'update')

        #----------------------------------------------------------
        def updateProgress(self, msg):
                """
                Update the progress bar
                """                
                self.parent.count += 1
                
                if  self.parent.isCancel or self.parent.count == self.parent.progress_max:
                        self.Destroy()
                else:                        
                        self.progress.SetValue(self.parent.count)                 
                        
        #------------------------------------------------------------
        def OnCancel(self, parent):                
                self.parent.isCancel = True
                pub.sendMessage("set status", msg = u"当前操作已被取消。")
                self.Destroy()
######################################################################


#####################################################################

# This class describes a generic method of drawing rubberbands
# on a wxPython canvas object (wxStaticBitmap, wxPanel etc) when
# the user presses the left mouse button and drags it over a rectangular
# area. It has methods to return the selected area by the user as 
# a rectangular 4 tuple / Clear the selected area.

# Beginning of code

class wxPyRubberBander:
    """ A class to manage mouse events/ rubberbanding of a wxPython
        canvas object """

    def __init__(self, canvas):
        # canvas object
        self._canvas = canvas
        # mouse selection start point
        self.m_stpoint=wx.Point(0,0)
        # mouse selection end point
        self.m_endpoint=wx.Point(0,0)
        # mouse selection cache point
        self.m_savepoint=wx.Point(0,0)
        
        # flags for left click/ selection
        self._leftclicked=False
        self._selected=False
        
        # pin icon
        pin = iconfile.pinIcon.GetData()        
        self.im_pin = wImage(blob = pin)
        
        # for crop image
        self.parent = self._canvas.GetParent()
        self.crop = None
        #self.scale = self.parent.scale
        self.scale = None

        # Register event handlers for mouse
        self.RegisterEventHandlers()

    def RegisterEventHandlers(self):
        """ Register event handlers for this object """

        wx.EVT_LEFT_DOWN(self._canvas, self.OnMouseEvent)
        wx.EVT_LEFT_UP(self._canvas, self.OnMouseEvent)
        wx.EVT_MOTION(self._canvas, self.OnMouseEvent)

    
    def OnMouseEvent(self, event):
        """ This function manages mouse events """

        if event:
            
            # set mouse cursor
            self._canvas.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
            # get device context of canvas
            dc= wx.ClientDC(self._canvas)
            
            # Set logical function to XOR for rubberbanding
            dc.SetLogicalFunction(wx.XOR)
            
            # Set dc brush and pen
            # Here I set brush and pen to white and grey respectively
            # You can set it to your own choices
            
            # The brush setting is not really needed since we
            # dont do any filling of the dc. It is set just for 
            # the sake of completion.

            wbrush = wx.Brush(wx.Colour(255,255,255), wx.TRANSPARENT)
            wpen = wx.Pen(wx.Colour(200, 200, 200), 1, wx.DOT) #SOLID)
            dc.SetBrush(wbrush)
            dc.SetPen(wpen)
        
            
        if event.LeftDown():
 
           # Left mouse button down, change cursor to
           # something else to denote event capture
           self.m_stpoint = event.GetPosition()
           self.parent.startPoint = self.m_stpoint
           self.scale = self.parent.scale
           
           self.crop = None # reset cropped area
           pub.sendMessage("set status", msg = "") #Reset status bar
           
           # 如果加载了图片，并且可以用鼠标指定位置的话
           if self.parent.totalPictures > 0:
                if self.parent.enablePin and self.parent.txtDlg.IsShown() and self.parent.selectBox.GetValue() == u"添加特效":
                        left = self.m_stpoint
                        box = (int(left.x * self.scale ) - 25, int(left.y * self.scale) - 81)
                        preview_backup = [] # cache the preview image object for later restore
                        if self.parent.im_preview: preview_backup.append(self.parent.im_preview)
                        else: preview_backup.append(None)
                        # check if single mode is on
                        if self.parent.singleMode and self.parent.im_preview:                                
                                img = self.parent.wand2pil(self.parent.im_preview, 'PNG')                                
                        else:
                                img = self.parent.readWandImage(self.parent.picPaths[self.parent.currentPicture])
                                img.format = "PNG"
                        img.watermark(self.im_pin, 0, box[0], box[1])                        
                        img = self.parent.wand2pil(img, 'PNG')
                        self.parent.imgPreview(img, '.PNG') # use instead of '.JPG' for transparent images
                        # restore the image preview object
                        if self.parent.singleMode: self.parent.im_preview = preview_backup[0]
                else:
                        cur = wx.StockCursor(wx.CURSOR_CROSS)  
                        self._canvas.SetCursor(cur)
                        self.pickTheColor(startpoint = self.m_stpoint)
                        # invalidate current canvas
                        self._canvas.Refresh()
                        self._canvas.SetFocus() # added for ctrl+v paste
                        # cache current position
                        self.m_savepoint = self.m_stpoint
                        self._selected = False
                        self._leftclicked = True

   
        elif event.Dragging():
            # User is dragging the mouse, check if
            # left button is down
            
            if self._leftclicked:

                # reset dc bounding box
                dc.ResetBoundingBox()
                dc.BeginDrawing()                
                
                w = (self.m_savepoint.x - self.m_stpoint.x)
                h = (self.m_savepoint.y - self.m_stpoint.y)
                
                # To erase previous rectangle
                dc.DrawRectangle(self.m_stpoint.x, self.m_stpoint.y, w, h)
                
                # Draw new rectangle
                self.m_endpoint =  event.GetPosition()
                
                w = (self.m_endpoint.x - self.m_stpoint.x)
                h = (self.m_endpoint.y - self.m_stpoint.y)
                
                # Set clipping region to rectangle corners
                dc.SetClippingRegion(self.m_stpoint.x, self.m_stpoint.y, w,h)
                dc.DrawRectangle(self.m_stpoint.x, self.m_stpoint.y, w, h) 
                dc.EndDrawing()
               
                self.m_savepoint = self.m_endpoint # cache current endpoint
                
                self.crop = self.GetCurrentSelection()
                
                # show the cropped image size (width and height)                
                [cropX1, cropY1, cropX2, cropY2] = self.crop
                w1, h1 = int(cropX2 - cropX1), int(cropY2 - cropY1)
                #
                #self.parent.ctrlWidth.SetValue(str(w))
                #self.parent.ctrlHeight.SetValue(str(h))
                
                if self.parent.totalPictures > 0:
                        if self.parent.Parent.colorPickTool.IsToggled():
                               
                                self.pickTheColor(endpoint = self.m_endpoint)
                        else:
                                self.parent.cropEnabled(w1, h1, True)
                        ## update status bar
                        #msg = (u"您选定的区域是：" + str(w) + 'x' + str(h)) * (w * h > 0)                
                        #pub.sendMessage("set status", msg = msg)
                        
                # set to pixel control
                self.parent.PnPBox.ChangeValue(u'按像素')

        elif event.LeftUp():

            # User released left button, change cursor back
            self._canvas.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))       
            self._selected = True  #selection is done
            self._leftclicked = False # end of clicking
            
    def pickTheColor(self, startpoint = None, endpoint = None):
        # 十字的坐标
        if not endpoint: point = startpoint
        else: point = endpoint
        X = point.x * self.scale
        Y = point.y * self.scale

        # pass to myPicWorkGUI's old color value
        if self.parent.picGUI:                
                self.parent.picGUI.SetPickedColor(X, Y) #str(pixels[X, Y]))
        # 拾取像素
        if not self.parent.imageLabel.GetLabel().startswith(u"(预览)"):
                img = self.parent.imageOpen(self.parent.getCurJpg()).convert("RGBA")
                pixels = img.load()
                
                r,g,b,a = pixels[X, Y]
                pub.sendMessage("set status", msg = u"像素：[" + ",".join(str(f) for f in (r,g,b,a)) + "]" )#str(r) + "," + str(g) + "," + str(b) + "]")
        else: self.parent.parent.onPicker()

    def GetCurrentSelection(self):
        """ Return the current selected rectangle """
        
        # if there is no selection, selection defaults to
        # current viewport
        
        left = wx.Point(0,0)
        right = wx.Point(0,0)
        
        # user dragged mouse to right
        if self.m_endpoint.y > self.m_stpoint.y:
            right = self.m_endpoint
            left = self.m_stpoint
        # user dragged mouse to left
        elif self.m_endpoint.y < self.m_stpoint.y:
            right = self.m_stpoint
            left = self.m_endpoint
        #self.scale = self.parent.scale
        
        # convert the scaled image to original size
        return (int(left.x * self.scale), int(left.y * self.scale), int(right.x * self.scale), int(right.y * self.scale))       

def usage():
        print 'Usage:\t[executable] [OPTIONS]'
        print
        print '[OPTIONS]'    
        print '-f {image}:'.ljust(25) + 'Specify the path of jpg file or directory'
        print '-o {output dir}:'.ljust(25) + 'The directory to save new jpg file(s)[OPTIONAL]'
        print '-l {size limit}:'.ljust(25) + 'Specify the the size limit'
        print '-r {resolution}:'.ljust(25) + 'Specify the new resolution by pixels or percentages'
        print '-h:'.ljust(25) + 'Print this help'
        print '-d {debug}:'.ljust(25) + 'For debug purpose[NOT IMPLEMENTED]'
        print '-D {DPI}:'.ljust(25) + 'update image dpi value'
        
def commandline():
        try:
                opts,args = getopt.getopt(sys.argv[1:], "hf:o:l:r:D:", ["file", "outputdir", "limit", "resolution", "DPI"])
        except getopt.GetoptError:
                usage()
                return 1
        save_path = imagefile = sizelimit = res = debug = dpi = None
        global fileIn

        for opt, arg in opts:

                if opt == '-h':
                        usage()
                        sys.exit()
                elif opt in ('-f', '--file'):
                        imagefile = arg
                elif opt in ('-o', '--outputdir'):
                        save_path = arg
                elif opt in ('-l', 'sizelimit'):
                        sizelimit = arg
                elif opt in ('-r', '--resolution'):
                        res = arg
                elif opt in ('-D', '--DPI'):
                        dpi = arg
                elif opt in ('-d', '--debug'):
                        debug = arg
                else:
                        assert False, "unhandled option"

        if not imagefile or ([sizelimit, res, dpi] == [None] * 3):                            
                fileIn = sys.argv[1:]
                usage()    
                return 2        
              
        cmd(imagefile, save_path  = save_path, dim_size_args = res, size_limit_arg = sizelimit, dpi = dpi) 
        
        
#----------------------------------------------------------------------
if __name__ == "__main__":
        
        fileIn = None
        
        if len(sys.argv) > 1:  
                commandline()

        if len(sys.argv) == 1 or fileIn is not None:
                # create wx.App object first
                app = wx.App(False)
                
                # check if wand imported properly
                HAS_IMAGICK = os.path.exists(os.path.join(exepath, 'imagic', 'convert.exe'))
                #MSG = appDetect('ImageMagick', 'ImageMagick', 'convert.exe')

                if not (HAS_WAND and HAS_IMAGICK):
                        MSG = u'系统上未检测到ImageMagick模块。程序即将退出。'
                        wx.MessageBox(u'警告：' + MSG, u"JPGTools", wx.OK | wx.ICON_INFORMATION)
                        sys.exit()
                else:
                        # After wx.App is created with can call icon func                
                        logo = iconfile.getLogoPng.GetBitmap()
                        midi = iconfile.getIcon.GetIcon()
                                                      
                        #show splash logo only once
                        #splashBmp = wx.Image(name = logo).ConvertToBitmap()
                        splash = None
                        if not os.path.exists(os.path.join(exepath, 'jpgconfig.ini')):
                                splash = wx.SplashScreen(logo, wx.SPLASH_CENTRE_ON_SCREEN, 2000, None, style=wx.NO_BORDER|wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP)
        
                        frame = ViewerFrame()    
                        app.MainLoop()  