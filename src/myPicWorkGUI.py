# -*- coding: cp936 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
###########################################################################

import wx, os
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont
from wx.lib.pubsub import pub
from round import round_image
from background import background, FILL_CHOICES
from shadow import drop_shadow, invert
from border_v2 import border
from molten import molten
from lighting import lighting
from reflection import reflect
from mirror import tile
from sketch import sketch
from ice import ice
from papercut import paper_cut
from tan import tan
from swirl import swirl
from spherize import spherize
#from wave import wave
from StringIO import StringIO
from de_yellow import deYellow
from np_puzzle import ImgSalon
from light import edge_blur
from corner_fold import EdgeFold
from tear import Tear
from Fade import Fade
from mix import MixColor
from color_replace import Replace
from np_pil import newPil
from auto_brightness import equalize, brightness
from shear import Shear
from img_mosaic import mosaic
from blendOrMask import AddMask, blend
from split import split
from slice_gone import slice_gone
import iconfile
import numpy as np
import _winreg
from openpyxl import load_workbook, workbook, worksheet
from openpyxl.utils.exceptions import InvalidFileException
import math

COLOR_FORMAT_TIP = u"手动输入时，请按照格式：\r\n(192, 192, 192, 255) 或者 #FF3CD2\r\n另外，您也可以先用鼠标点击该文本框，然后再点击图片完成取色"
BACKGROUND_TIP = u'打开背景设置\r\n为透明图片添加背景'
PUZZLE_TIP = u"打开拼图设置\r\n将大小相同的图片拼在一起"
SPLIT_TIP = u"打开图片分割设置\r\n将当前图片分割成大小相同的图片。\r\n注意：如果添加该任务，它将最后一个执行"
FOCUS_TIP = u'打开聚光设置\r\n提示：内圈和外圈半径是相对于图片内圆而言'
TEAR_TIP = u"打开锯齿设置\r\n在指定方向生成锯齿效果。"
REPLACE_TIP = u"打开颜色替换设置\r\n将图片中满足条件的一种颜色用另一种来替换"
SPLIT_LINE_COLOR_TIP = u"预览时的分割线颜色"
SLICE_TIP = u"请首先将需要去除的中间部分，用鼠标选中。可以进行上下或左右拼接"

wildcard = "所有文件 (*.*) | *.*|" \
	"JPG 图片 (*.jpg) | *.jpg|" \
	"BMP 图片 (*.bmp) | *.bmp|" \
	"PNG 图片 (*.png) | *.png"

###########################################################################
## Class MyJPGWorkDlg
###########################################################################

class MyJPGWorkDlg ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"图片特效", pos = wx.DefaultPosition,
				    size = wx.Size( 570, 820 ), style = wx.DEFAULT_DIALOG_STYLE |wx.MINIMIZE_BOX | wx.TE_PROCESS_ENTER )				
		self.parent = parent
		self.list_view_dlg = None
		self.SetIcon(self.parent.midi)	
		self.ctrlOnFocus = None
		self.settingCounts = 0
		self.out_dir = None
		#self.lastBtnPressed = None
		self.cur_im = None # the current Image object
		self.cur_img = None # the image current working on
		#self.txtDlg = None # watermark instance
		self.taskMapper = {u"圆角效果": self.MakeRound, u"背景效果": self.MakeBackground, \
				   u"边框效果": self.MakeBorder, u"阴影效果": self.MakeShadow, \
				   u"倒影效果": self.MakeReflection, u"灰度效果": self.MakeGrayscale, \
				   
				   u"黑白效果": self.MakeBlkWht, u"图像增强": self.MakeEnhance, \
				   u"滤镜效果": self.MakeFilter, u"旋转效果": self.MakeRotate, \
				   u"镜像翻转": self.MakeMirror, u"底片效果": self.MakeInvert, \
				   
				   u"熔铸效果": self.MakeMolten, u"灯光效果":  self.MakeLighting, \
				   u"素描效果": self.MakeSketch, u"冰冻效果": self.MakeIce, \
				   u"剪纸效果": self.MakePapercut, u"聚光效果": self.MakeFocus,\
				   
				   u"新照片": self.MakeDeYellow, u"老照片": self.MakeTan, \
				   u"漩涡效果": self.MakeSwirl, u"哈哈镜": self.MakeSpherize, \
				   u"拼图效果": self.MakePuzzle, u"折角效果": self.MakeCornerFold, \
				   u"锯齿边缘": self.MakeTear, u"渐变效果": self.MakeFade, \
				   u"混色效果": self.MakeMix, u"颜色替换": self.MakeReplace, \
				   u"自动亮度": self.MakeAutoBrightness, u"滚动效果": self.MakeRoll, \
				   u"倾斜效果": self.MakeShear, u"马赛克": self.MakeMosaic, \
				   u"蒙版效果": self.AddMask, u"混合效果": self.MakeBlend, \
				   u"水印效果": self.MakeWaterMark, u"图片分割": self.MakeSplit, \
				   u"中间去除": self.SliceGone }
		
		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizerMain = wx.BoxSizer( wx.VERTICAL )
		
		bSizerTask = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizerTaskSub = wx.BoxSizer( wx.HORIZONTAL )            
		sbSizerTaskList = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, u"任务列表排序" ), wx.VERTICAL )         
		self.m_checkList1Choices = []
		self.m_checkList1 = wx.ListBox( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.Size( 440,200 ), self.m_checkList1Choices, wx.LB_NEEDED_SB|wx.LB_SINGLE )
		sbSizerTaskList.Add( self.m_checkList1, 0, wx.ALL|wx.EXPAND, 5 )
		self.m_checkList1.Bind(wx.EVT_LISTBOX, self.KeyDown)
		self.m_checkList1.SetToolTipString(u'点击"+" 按钮添加效果到列表')            
		bSizerTask.Add( sbSizerTaskList, 1, wx.EXPAND, 5 )
		
		bSizerUpDown = wx.BoxSizer( wx.VERTICAL )
		self.m_buttonDel = wx.BitmapButton( self.m_panel1, wx.ID_ANY, self.parent.remove_ico, wx.DefaultPosition, wx.Size(24, 24), wx.BU_EXACTFIT  )
		bSizerUpDown.Add( self.m_buttonDel, 0, wx.ALL | wx.CENTER, 5 )
		self.m_buttonDel.SetToolTipString(u'移除所选任务')		
		
		self.m_buttonDelAll = wx.Button( self.m_panel1, wx.ID_ANY, "", wx.DefaultPosition, wx.Size(24, 24), 0 )
		bSizerUpDown.Add( self.m_buttonDelAll, 0, wx.ALL |  wx.CENTER, 5 )
		self.m_buttonDelAll.SetToolTipString(u'清空任务列表')         
		bSizerUpDown.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )		
		
		self.m_btnUP = wx.BitmapButton( self.m_panel1, wx.ID_ANY, self.parent.up_ico, wx.DefaultPosition, wx.Size(24, 24), wx.BU_EXACTFIT  )
		bSizerUpDown.Add( self.m_btnUP, 0, wx.ALL | wx.CENTER, 5 )
		self.m_btnUP.SetToolTipString(u'上移')

		self.m_btnDown = wx.BitmapButton( self.m_panel1, wx.ID_ANY, self.parent.down_ico, wx.DefaultPosition, wx.Size(24, 24), wx.BU_EXACTFIT  )
		bSizerUpDown.Add( self.m_btnDown, 0, wx.ALL |  wx.CENTER, 5 )
		self.m_btnDown.SetToolTipString(u'下移')		
		
		bSizerTask.Add( bSizerUpDown, 1, wx.EXPAND, 5 )
		bSizerMain.Add( bSizerTask, 1, wx.EXPAND, 5 )
		
		# Create a panel for all available effects ---------------              
		sbSizerTaskPanel = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, u"可选效果"), wx.VERTICAL )
		sbSizerTaskPanel_1 = wx.BoxSizer(wx.HORIZONTAL)
		sbSizerTaskPanel_2 = wx.BoxSizer(wx.HORIZONTAL)
		sbSizerTaskPanel_3 = wx.BoxSizer(wx.HORIZONTAL)
		sbSizerTaskPanel_4 = wx.BoxSizer(wx.HORIZONTAL)
		sbSizerTaskPanel_5 = wx.BoxSizer(wx.HORIZONTAL)
		sbSizerTaskPanel_6 = wx.BoxSizer(wx.HORIZONTAL)
		sbSizerTaskPanel_7 = wx.BoxSizer(wx.HORIZONTAL)
		
		self.m_buttonRound = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"圆角效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_1.Add( self.m_buttonRound, 0, wx.ALL, 5 )
		#self.m_buttonRound.SetValue(True)
		self.m_buttonRound.SetToolTipString(u'打开圆角设置')
		
		self.m_buttonBackground = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"背景效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_1.Add( self.m_buttonBackground, 0, wx.ALL, 5 )
		self.m_buttonBackground.SetToolTipString(BACKGROUND_TIP)
		
		self.m_buttonBorder = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"边框效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_1.Add( self.m_buttonBorder, 0, wx.ALL, 5 )
		self.m_buttonBorder.SetToolTipString(u'打开边框设置')
		## 
		self.m_buttonShadow = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"阴影效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_1.Add( self.m_buttonShadow, 0, wx.ALL, 5 )
		self.m_buttonShadow.SetToolTipString(u'打开阴影设置')
		
		self.m_buttonReflection = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"倒影效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_1.Add( self.m_buttonReflection, 0, wx.ALL, 5 )
		self.m_buttonReflection.SetToolTipString(u'打开倒影设置')
		
		self.m_buttonGrayscale = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"灰度效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_1.Add( self.m_buttonGrayscale, 0, wx.ALL, 5 )		
		
		self.m_buttonBlkWht = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"黑白效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_2.Add( self.m_buttonBlkWht, 0, wx.ALL, 5 )     
		# 增强
		self.m_buttonEnhance = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"图像增强", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_2.Add( self.m_buttonEnhance, 0, wx.ALL, 5 )
		self.m_buttonEnhance.SetToolTipString(u'打开图像增强设置')        
		
		self.m_buttonFilter = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"滤镜效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_2.Add( self.m_buttonFilter, 0, wx.ALL, 5 )
		self.m_buttonFilter.SetToolTipString(u'打开滤镜设置')
		
		self.m_buttonRotate = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"旋转效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_2.Add( self.m_buttonRotate, 0, wx.ALL, 5 )
		self.m_buttonRotate.SetToolTipString(u'打开旋转设置')
		
		self.m_buttonMirror = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"镜像翻转", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_2.Add( self.m_buttonMirror, 0, wx.ALL, 5 )
		self.m_buttonMirror.SetToolTipString(u'打开镜像翻转设置')
		
		self.m_buttonInvert = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"底片效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_2.Add( self.m_buttonInvert, 0, wx.ALL, 5 )
		self.m_buttonInvert.SetToolTipString(u'打开底片设置')
		
		self.m_buttonMolten = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"熔铸效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_3.Add( self.m_buttonMolten, 0, wx.ALL, 5 )
		# No config needed
		self.m_buttonLighting = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"灯光效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_3.Add( self.m_buttonLighting, 0, wx.ALL, 5 )
		self.m_buttonLighting.SetToolTipString(u'打开灯光设置')

		self.m_buttonSketch = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"素描效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_3.Add( self.m_buttonSketch, 0, wx.ALL, 5 )
		self.m_buttonSketch.SetToolTipString(u'打开素描设置')
		
		self.m_buttonIce = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"冰冻效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_3.Add( self.m_buttonIce, 0, wx.ALL, 5 )
		# No config needed
		
		self.m_buttonPapercut = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"剪纸效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_3.Add( self.m_buttonPapercut, 0, wx.ALL, 5 )
		self.m_buttonPapercut.SetToolTipString(u'打开剪纸设置')
		
		self.m_buttonFocus = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"聚光效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_3.Add( self.m_buttonFocus, 0, wx.ALL, 5 )
		self.m_buttonFocus.SetToolTipString(FOCUS_TIP)
		
		size = self.m_buttonPapercut.GetSize()
		
		self.m_buttonDeYellow = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"新照片", wx.DefaultPosition, size) #wx.DefaultSize) #, wx.BU_EXACTFIT )
		sbSizerTaskPanel_4.Add( self.m_buttonDeYellow, 0, wx.ALL, 5 )
		self.m_buttonDeYellow.SetToolTipString(u'打开新照片设置')
		
		self.m_buttonTan = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"老照片", wx.DefaultPosition, size) #wx.DefaultSize) #, wx.BU_EXACTFIT )
		sbSizerTaskPanel_4.Add( self.m_buttonTan, 0, wx.ALL, 5 )
		# No config needed
		
		self.m_buttonSwirl = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"漩涡效果", wx.DefaultPosition, size) #wx.DefaultSize) #, wx.BU_EXACTFIT )
		sbSizerTaskPanel_4.Add( self.m_buttonSwirl, 0, wx.ALL, 5 )
		self.m_buttonSwirl.SetToolTipString(u'打开漩涡设置')        
		
		self.m_buttonSpherize = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"哈哈镜", wx.DefaultPosition, size) #wx.DefaultSize) #, wx.BU_EXACTFIT )
		sbSizerTaskPanel_4.Add( self.m_buttonSpherize, 0, wx.ALL, 5 )
		# No config needed
		# 拼图
		self.m_buttonPuzzle = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"拼图效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_4.Add( self.m_buttonPuzzle, 0, wx.ALL, 5 )
		self.m_buttonPuzzle.SetToolTipString(PUZZLE_TIP) 
		
		# 折角
		self.m_buttonCornerFold = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"折角效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_4.Add( self.m_buttonCornerFold, 0, wx.ALL, 5 )
		self.m_buttonCornerFold.SetToolTipString(u'打开折角设置')
		
		# 折角
		self.m_buttonTear = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"锯齿边缘", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_5.Add( self.m_buttonTear, 0, wx.ALL, 5 )
		self.m_buttonTear.SetToolTipString(TEAR_TIP)
		
		self.m_buttonFade = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"渐变效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_5.Add( self.m_buttonFade, 0, wx.ALL, 5 )
		self.m_buttonFade.SetToolTipString(u'打开渐变设置')
		
		self.m_buttonMix = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"混色效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_5.Add( self.m_buttonMix, 0, wx.ALL, 5 )
		self.m_buttonMix.SetToolTipString(u'打开混色设置')
		
		self.m_buttonReplace = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"颜色替换", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_5.Add( self.m_buttonReplace, 0, wx.ALL, 5 )
		self.m_buttonReplace.SetToolTipString(REPLACE_TIP)
		
		self.m_buttonAutoBrightness = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"自动亮度", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_5.Add( self.m_buttonAutoBrightness, 0, wx.ALL, 5 )
		self.m_buttonAutoBrightness.SetToolTipString(u'打开自动亮度设置\r\n调节图片到指定的亮度')
		
		self.m_buttonRoll = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"滚动效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_5.Add( self.m_buttonRoll, 0, wx.ALL, 5 )
		self.m_buttonRoll.SetToolTipString(u'打开滚动设置')
		
		self.m_buttonShear = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"倾斜效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_6.Add( self.m_buttonShear, 0, wx.ALL, 5 )
		self.m_buttonShear.SetToolTipString(u'打开倾斜设置')
		
		self.m_buttonMosaic = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"马赛克", wx.DefaultPosition, self.m_buttonShear.GetSize(), 0)
		sbSizerTaskPanel_6.Add( self.m_buttonMosaic, 0, wx.ALL, 5 )
		self.m_buttonMosaic.SetToolTipString(u'打开马赛克设置')
		
		self.m_buttonMask = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"蒙版效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_6.Add( self.m_buttonMask, 0, wx.ALL, 5 )
		self.m_buttonMask.SetToolTipString(u'打开蒙版设置')
		
		self.m_buttonBlend = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"混合效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_6.Add( self.m_buttonBlend, 0, wx.ALL, 5 )
		self.m_buttonBlend.SetToolTipString(u'打开混合设置')
		
		self.m_buttonWaterMark = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"水印效果", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_6.Add( self.m_buttonWaterMark, 0, wx.ALL, 5 )
		self.m_buttonWaterMark.SetToolTipString(u'打开水印设置')
		
		# 分割
		self.m_buttonSplit = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"图片分割", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_6.Add( self.m_buttonSplit, 0, wx.ALL, 5 )
		self.m_buttonSplit.SetToolTipString(SPLIT_TIP)
		
		self.m_buttonSlice = wx.ToggleButton( self.m_panel1, wx.ID_ANY, u"中间去除", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		sbSizerTaskPanel_7.Add( self.m_buttonSlice, 0, wx.ALL, 5 )
		self.m_buttonSlice.SetToolTipString(SLICE_TIP) 
		
		self.m_bpButtonPlus = wx.Button( self.m_panel1, wx.ID_ANY, "+", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )		
		sbSizerTaskPanel_7.Add( self.m_bpButtonPlus, 0, wx.ALL, 5 )
		
		self.m_bpButtonPlus.SetToolTipString(u'添加到任务列表')
		sbSizerTaskPanel.Add(sbSizerTaskPanel_1, 1, wx.ALL | wx.TOP, 0 )
		sbSizerTaskPanel.Add(sbSizerTaskPanel_2, 1, wx.ALL | wx.TOP, 0 )
		sbSizerTaskPanel.Add(sbSizerTaskPanel_3, 1, wx.ALL | wx.TOP, 0 )
		sbSizerTaskPanel.Add(sbSizerTaskPanel_4, 1, wx.ALL | wx.TOP, 0 )
		sbSizerTaskPanel.Add(sbSizerTaskPanel_5, 1, wx.ALL | wx.TOP, 0 )
		sbSizerTaskPanel.Add(sbSizerTaskPanel_6, 1, wx.ALL | wx.TOP, 0 )
		sbSizerTaskPanel.Add(sbSizerTaskPanel_7, 1, wx.ALL | wx.TOP, 0 )
		
		#Task dict
		self.taskListBtns = [self.m_buttonRound, self.m_buttonBackground, self.m_buttonBorder, self.m_buttonShadow,
					 self.m_buttonReflection, self.m_buttonGrayscale, self.m_buttonBlkWht, self.m_buttonEnhance,
					 self.m_buttonFilter, self.m_buttonRotate, self.m_buttonMirror, self.m_buttonInvert, self.m_buttonMolten,
					 self.m_buttonLighting, self.m_buttonSketch, self.m_buttonIce, self.m_buttonPapercut, self.m_buttonFocus,
					 self.m_buttonDeYellow, self.m_buttonTan, self.m_buttonSwirl, self.m_buttonSpherize,
					 self.m_buttonPuzzle, self.m_buttonCornerFold, self.m_buttonTear, self.m_buttonFade, self.m_buttonMix,
					 self.m_buttonReplace, self.m_buttonAutoBrightness, self.m_buttonRoll, self.m_buttonShear, self.m_buttonMosaic,
					 self.m_buttonMask, self.m_buttonBlend, self.m_buttonWaterMark, self.m_buttonSplit, self.m_buttonSlice ]
		
		bSizerMain.Add( sbSizerTaskPanel, 1, wx.EXPAND, 0 )
		#---------------------panel ends ---------------------      
		#------------setting for round corner starts-----------
		bSizerSetting = wx.BoxSizer( wx.VERTICAL )
		self.staticRound = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"圆角设置" )
		self.sbSizerRound = wx.StaticBoxSizer( self.staticRound , wx.VERTICAL )
		
		bSizerRoundCkBox = wx.BoxSizer( wx.VERTICAL )
		
		self.m_checkBoxDefault = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"选择默认", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxDefault.SetValue(True)
		bSizerRoundCkBox.Add( self.m_checkBoxDefault, 0, wx.ALL, 5 )            
		
		self.sbSizerRound.Add( bSizerRoundCkBox, 1, wx.EXPAND, 5 )              
		
		bSizerValue = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticTextRound = wx.StaticText( self.m_panel1, wx.ID_ANY, u"圆角半径", wx.DefaultPosition, wx.DefaultSize, 0 )
		#self.m_staticTextRound.Wrap( -1 )
		#self.m_staticTextRound.Enable( False )
		bSizerValue.Add( self.m_staticTextRound, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_spinCtrlNum = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"5", wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, 0, 50, 0 )
		bSizerValue.Add( self.m_spinCtrlNum, 0, wx.ALIGN_CENTER|wx.ALL, 5 )		
		
		self.m_staticTextSize = wx.StaticText( self.m_panel1, wx.ID_ANY, u"% 图片尺寸", wx.DefaultPosition, wx.DefaultSize, 0 )
		#self.m_staticTextSize.Wrap( -1 )
		bSizerValue.Add( self.m_staticTextSize, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.sbSizerRound.Add( bSizerValue, 1, wx.EXPAND, 5 )
		bSizerSetting.Add( self.sbSizerRound, 1, wx.EXPAND, 0 )
		#------------setting for round corner ends-----------
		#------------setting for backgroound setting starts-----------
		self.staticBackground = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"背景设置" )
		self.sbSizerBg = wx.StaticBoxSizer( self.staticBackground, wx.HORIZONTAL )
		
		bSizerSource = wx.BoxSizer( wx.VERTICAL )               
		bSizerSrcColor = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_radioBtnCkColor = wx.RadioButton( self.m_panel1, wx.ID_ANY, u"颜色", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
		bSizerSrcColor.Add( self.m_radioBtnCkColor, 0, wx.ALL, 5 )		
		
		self.m_bgColourPicker = wx.ColourPickerCtrl( self.m_panel1, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.Size( 50,13 ), wx.CLRP_USE_TEXTCTRL) #wx.CLRP_DEFAULT_STYLE )
		bSizerSrcColor.Add( self.m_bgColourPicker, 0, wx.ALL, 5 )
		#self.cur_bgColor = wx.BLACK
		
		bSizerSrcColor.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_methodText = wx.StaticText( self.m_panel1, label = u"叠加方式")
		bSizerSrcColor.Add( self.m_methodText, 0, wx.ALL, 5 )
		self.m_MethodList = [u'平铺', u'比例', u'偏移']
		self.m_comboMethod = wx.ComboBox( self.m_panel1, value = self.m_MethodList[2], choices = self.m_MethodList, style = wx.CB_READONLY)
		bSizerSrcColor.Add(self.m_comboMethod, 0, wx.ALL|wx.RIGHT, 5 )
		self.m_comboMethod.Bind(wx.EVT_COMBOBOX_CLOSEUP, self.onMethodChanged)   
		
		bSizerSource.Add( bSizerSrcColor, 1, wx.EXPAND, 5 )
		
		bSizerSrcPic = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_radioBtnCkPic = wx.RadioButton( self.m_panel1, wx.ID_ANY, u"图片", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerSrcPic.Add( self.m_radioBtnCkPic, 0, wx.ALIGN_TOP|wx.ALL, 5 )
		
		self.m_textCtrlPath = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, (150, -1), wx.TE_READONLY)
		bSizerSrcPic.Add( self.m_textCtrlPath, 0, wx.ALL, 5 )
		self.pic = None         
		
		self.m_btnBrowse = wx.Button( self.m_panel1, wx.ID_ANY, u"...", wx.DefaultPosition, (-1, 21), wx.BU_EXACTFIT )
		bSizerSrcPic.Add( self.m_btnBrowse, 0, wx.ALL, 5 )              
		
		bSizerSource.Add( bSizerSrcPic, 1, wx.EXPAND, 5 )
		self.sbSizerBg.Add( bSizerSource, 1, wx.EXPAND, 5 )
		
		bSizerOffset = wx.BoxSizer( wx.VERTICAL )               
		bSizerOffsetH = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticTextHPos = wx.StaticText( self.m_panel1, wx.ID_ANY, u"水平位置", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextHPos.Wrap( -1 )
		bSizerOffsetH.Add( self.m_staticTextHPos, 0, wx.ALL|wx.RIGHT, 5 )
		
		self.m_HPosList = [u'左', u'中', u'右']
		self.m_VPosList = [u'上', u'中', u'下']
		
		self.m_comboTextHPos = wx.ComboBox( self.m_panel1, value = self.m_HPosList[0], choices = self.m_HPosList, style = wx.CB_READONLY)
		bSizerOffsetH.Add( self.m_comboTextHPos, 0, wx.ALL|wx.RIGHT, 5 )
		
		#---
		self.m_staticTextHtxt = wx.StaticText( self.m_panel1, wx.ID_ANY, u"水平偏移(像素)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextHtxt.Wrap( -1 )
		bSizerOffsetH.Add( self.m_staticTextHtxt, 0, wx.ALL|wx.RIGHT, 5 )
		
		self.m_textCtrlHbox = wx.TextCtrl( self.m_panel1, wx.ID_ANY, '0', wx.DefaultPosition, (60, -1), 0 )
		bSizerOffsetH.Add( self.m_textCtrlHbox, 0, wx.ALL, 5 )
		#---
		
		bSizerOffset.Add( bSizerOffsetH, 1, wx.EXPAND, 5 )              
		bSizerV = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticTextVPos = wx.StaticText( self.m_panel1, wx.ID_ANY, u"垂直位置", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextVPos.Wrap( -1 )
		bSizerV.Add( self.m_staticTextVPos, 0, wx.ALL|wx.RIGHT, 5 )
		
		self.m_comboTextVPos = wx.ComboBox( self.m_panel1, value = self.m_VPosList[0], choices = self.m_VPosList, style = wx.CB_READONLY)
		bSizerV.Add( self.m_comboTextVPos, 0, wx.ALL|wx.RIGHT, 5 )
		
		#--------
		self.m_staticTextVtxt = wx.StaticText( self.m_panel1, wx.ID_ANY, u"垂直偏移(像素)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextVtxt.Wrap( -1 )
		bSizerV.Add( self.m_staticTextVtxt, 0, wx.ALL|wx.RIGHT, 5 )
		
		self.m_textCtrlVbox = wx.TextCtrl( self.m_panel1, wx.ID_ANY, '0', wx.DefaultPosition, (60, -1), 0 )
		bSizerV.Add( self.m_textCtrlVbox, 0, wx.ALL, 5 )
		#----------             
		
		bSizerOffset.Add( bSizerV, 1, wx.EXPAND, 5 )
		self.sbSizerBg.Add( bSizerOffset, 1, wx.EXPAND, 5 )             
		
		bSizerSetting.Add( self.sbSizerBg, 1, wx.EXPAND, 0 )
		#-------------- Add border feature ------------     
		self.staticBorder = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"边框设置" )
		sbSizerStaticBorder = wx.StaticBoxSizer( self.staticBorder, wx.HORIZONTAL )
		
		self.m_staticTextBorder = wx.StaticText( self.m_panel1, wx.ID_ANY, u"边距(像素)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextBorder.Wrap( -1 )
		sbSizerStaticBorder.Add( self.m_staticTextBorder, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		
		self.m_textCtrlBorderBox = wx.TextCtrl( self.m_panel1, wx.ID_ANY, '20', wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		sbSizerStaticBorder.Add( self.m_textCtrlBorderBox, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		
		
		sbSizerStaticBorder.Add((20, -1))
		
		self.m_staticTextColor = wx.StaticText( self.m_panel1, wx.ID_ANY, u"边框颜色", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextColor.Wrap( -1 )
		sbSizerStaticBorder.Add( self.m_staticTextColor, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		
		self.cur_borderColor = wx.Colour(178, 178, 178)
		self.m_borderColourPicker = wx.ColourPickerCtrl( self.m_panel1, wx.ID_ANY, self.cur_borderColor, wx.DefaultPosition, wx.Size( 50,12 ), wx.CLRP_DEFAULT_STYLE )
		sbSizerStaticBorder.Add( self.m_borderColourPicker, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )		
				
		sbSizerStaticBorder.Add((20, -1))
		
		self.m_staticTextOpacity = wx.StaticText( self.m_panel1, wx.ID_ANY, u'不透明度', wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextOpacity.Wrap( -1 )
		sbSizerStaticBorder.Add( self.m_staticTextOpacity, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_sliderOpacity = wx.Slider( self.m_panel1, wx.ID_ANY, 80, 0, 100, wx.DefaultPosition, wx.DefaultSize, style=wx.SL_HORIZONTAL|wx.SL_LABELS )
		sbSizerStaticBorder.Add( self.m_sliderOpacity, 0, wx.ALIGN_CENTER|wx.ALL, 5 )     

		bSizerSetting.Add(sbSizerStaticBorder, 1, wx.EXPAND, 0)
		#---------------border feature ends -----------
		#---------------shadow feature starts ----------
		self.staticShadow = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"阴影设置" )
		sbSizerStaticShadow = wx.StaticBoxSizer( self.staticShadow, wx.HORIZONTAL )
		
		#sbSizerStaticShadow.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticHTextShadow = wx.StaticText( self.m_panel1, wx.ID_ANY, u"水平偏移(像素)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticHTextShadow.Wrap( -1 )
		sbSizerStaticShadow.Add( self.m_staticHTextShadow, 0, wx.ALIGN_CENTER|wx.RIGHT, 5 )
		
		self.m_textCtrlShadowHBox = wx.TextCtrl( self.m_panel1, wx.ID_ANY, '10', wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		sbSizerStaticShadow.Add( self.m_textCtrlShadowHBox, 0, wx.ALIGN_CENTER, 5 )
		
		sbSizerStaticShadow.Add( (20, -1))
		
		self.m_staticVTextShadow = wx.StaticText( self.m_panel1, wx.ID_ANY, u"垂直偏移(像素)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticVTextShadow.Wrap( -1 )
		sbSizerStaticShadow.Add( self.m_staticVTextShadow, 0, wx.ALIGN_CENTER|wx.RIGHT, 5 )
		
		self.m_textCtrlShadowVBox = wx.TextCtrl( self.m_panel1, wx.ID_ANY, '10', wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		sbSizerStaticShadow.Add( self.m_textCtrlShadowVBox, 0, wx.ALIGN_CENTER, 5 )      

		bSizerSetting.Add( sbSizerStaticShadow, 1, wx.EXPAND, 0 )       
		#---------------shadow feature ends ------------
		#--------------- reflection starts -------------   
		self.staticReflection = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"倒影设置" )
		sbSizerStaticReflection = wx.StaticBoxSizer( self.staticReflection, wx.HORIZONTAL )
		
		self.m_staticTextDepth = wx.StaticText( self.m_panel1, wx.ID_ANY, u"倒影深度(像素)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextDepth.Wrap( -1 )
		sbSizerStaticReflection.Add( self.m_staticTextDepth, 0, wx.ALIGN_CENTER|wx.RIGHT, 5 )
		
		self.m_textCtrlDepthBox = wx.TextCtrl( self.m_panel1, wx.ID_ANY, '500', wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		sbSizerStaticReflection.Add( self.m_textCtrlDepthBox, 0, wx.ALIGN_CENTER, 5 )
		
		sbSizerStaticReflection.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticReflectionBgColor = wx.StaticText( self.m_panel1, wx.ID_ANY, u"背景颜色", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticReflectionBgColor.Wrap( -1 )
		sbSizerStaticReflection.Add( self.m_staticReflectionBgColor, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		
		self.m_ReflectionBgColourPicker = wx.ColourPickerCtrl( self.m_panel1, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.Size( 50,12 ), wx.CLRP_DEFAULT_STYLE )
		sbSizerStaticReflection.Add( self.m_ReflectionBgColourPicker, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		#self.cur_ReflectionBgColor = wx.BLACK
		
		sbSizerStaticReflection.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticReflectionOpacity = wx.StaticText( self.m_panel1, wx.ID_ANY, u'不透明度', wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticReflectionOpacity.Wrap( -1 )
		sbSizerStaticReflection.Add( self.m_staticReflectionOpacity, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		
		self.m_sliderReflectionOpacity = wx.Slider( self.m_panel1, wx.ID_ANY, 0, 0, 100, wx.DefaultPosition, wx.DefaultSize, style=wx.SL_HORIZONTAL|wx.SL_LABELS )
		sbSizerStaticReflection.Add( self.m_sliderReflectionOpacity, 0, wx.ALIGN_CENTER | wx.LEFT, 5 )

		bSizerSetting.Add( sbSizerStaticReflection, 1, wx.EXPAND, 0 )
		#----------------reflection ends ---------------
		#---------------enhance starts ------------------
		self.staticEnhance = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"图像增强设置" )
		sbSizerStaticEnhance = wx.StaticBoxSizer( self.staticEnhance, wx.HORIZONTAL )
		#sbSizerStaticEnhance.Add(self.staticEnhance, 0, wx.ALL|wx.RIGHT, 5 )
		
		self.m_staticTextFactor = wx.StaticText( self.m_panel1, wx.ID_ANY, u"增强系数(-100 ~ 100)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextFactor.Wrap( -1 )
		sbSizerStaticEnhance.Add( self.m_staticTextFactor, 0, wx.ALIGN_CENTER | wx.RIGHT, 5 )    
		
		self.m_spinCtrlFactor = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"20", wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, -100, 100, 20 )
		sbSizerStaticEnhance.Add( self.m_spinCtrlFactor, 0, wx.ALIGN_CENTER| wx.RIGHT, 5 )
		
		sbSizerStaticEnhance.Add( ( 20, 0) )
		
		self.m_staticTextEnhance = wx.StaticText( self.m_panel1, wx.ID_ANY, u"增强方案", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextEnhance.Wrap( -1 )
		sbSizerStaticEnhance.Add( self.m_staticTextEnhance, 0, wx.ALIGN_CENTER| wx.RIGHT, 5 )
				
		self.m_EnhanceModeList = [u'锐化', u'色调', u'亮度', u'对比度']      
		self.m_EnhanceBox = wx.ComboBox( self.m_panel1, value = self.m_EnhanceModeList[3], choices = self.m_EnhanceModeList, style = wx.CB_READONLY)
		sbSizerStaticEnhance.Add( self.m_EnhanceBox, 0, wx.ALIGN_CENTER, 5 )     

		bSizerSetting.Add( sbSizerStaticEnhance, 1, wx.EXPAND, 0 )
		#---------------enhance ends --------------------
		#---------------Filter starts ------------------
		self.staticFilter = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"滤镜设置" )
		sbSizerStaticFilter = wx.StaticBoxSizer( self.staticFilter, wx.HORIZONTAL )
				
		#self.m_FilterModeList = [u'模糊', u'高斯模糊', u'浮雕', u'轮廓', u'边缘增强', u'平滑', u'中值滤波', u'锐化', u'细节']
		self.m_checkBoxBlur = wx.CheckBox(self.m_panel1, label=u'模糊', style = wx.BU_EXACTFIT )
		self.m_checkBoxGBlur = wx.CheckBox(self.m_panel1, label=u'高斯模糊', style = wx.BU_EXACTFIT )
		self.m_checkBoxEmboss = wx.CheckBox(self.m_panel1, label=u'浮雕', style = wx.BU_EXACTFIT )
		self.m_checkBoxContour = wx.CheckBox(self.m_panel1, label=u'轮廓', style = wx.BU_EXACTFIT )
		self.m_checkBoxEdge = wx.CheckBox(self.m_panel1, label=u'边缘增强', style = wx.BU_EXACTFIT )
		self.m_checkBoxSmooth = wx.CheckBox(self.m_panel1, label=u'平滑', style = wx.BU_EXACTFIT )
		self.m_checkBoxMedFilter = wx.CheckBox(self.m_panel1, label=u'中值滤波', style = wx.BU_EXACTFIT )
		self.m_checkBoxSharpen = wx.CheckBox(self.m_panel1, label=u'锐化', style = wx.BU_EXACTFIT )
		self.m_checkBoxDetail = wx.CheckBox(self.m_panel1, label=u'细节', style = wx.BU_EXACTFIT )
		self.m_FilterBoxList = [self.m_checkBoxBlur, self.m_checkBoxGBlur, self.m_checkBoxEmboss,self.m_checkBoxContour,
					self.m_checkBoxEdge, self.m_checkBoxSmooth, self.m_checkBoxMedFilter, self.m_checkBoxSharpen,
					self.m_checkBoxDetail ]
		self.m_checkBoxGBlur.SetValue(True)
		for checkbox in self.m_FilterBoxList:           
			sbSizerStaticFilter.Add(checkbox, 0, wx.ALL|wx.CENTER, 3 )		
		
		bSizerSetting.Add( sbSizerStaticFilter, 1, wx.EXPAND, 0 )
		#---------------Filter ends ------------------
		#---------------rotate starts ------------------        
		self.staticRotate = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"旋转设置" )
		sbSizerStaticRotate = wx.StaticBoxSizer( self.staticRotate, wx.HORIZONTAL )		

		self.m_radioBtnFixed = wx.RadioButton( self.m_panel1, wx.ID_ANY, u"固定角度", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )		
		sbSizerStaticRotate.Add( self.m_radioBtnFixed, 0, wx.ALIGN_CENTER | wx.RIGHT, 5 )		
		
		m_choiceFixedChoices = [ u"90", u"180", u"270" ]
		self.m_choiceFixed = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceFixedChoices, 0 )
		self.m_choiceFixed.SetSelection( 0 )
		sbSizerStaticRotate.Add( self.m_choiceFixed, 0, wx.ALIGN_CENTER| wx.RIGHT, 5 )		
		
		sbSizerStaticRotate.Add( ( 20, -1))
		
		self.m_radioBtnAny = wx.RadioButton( self.m_panel1, wx.ID_ANY, u"任意角度(0~360)", wx.DefaultPosition, wx.DefaultSize, 0 )		
		sbSizerStaticRotate.Add( self.m_radioBtnAny, 0, wx.ALIGN_CENTER| wx.RIGHT, 5 )
		
		self.m_spinCtrlAny = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size(80, -1), wx.SP_ARROW_KEYS, 0, 360, 0 )
		self.m_spinCtrlAny.Enable(False)		
		sbSizerStaticRotate.Add( self.m_spinCtrlAny, 0, wx.ALIGN_CENTER, 5 )			

		bSizerSetting.Add( sbSizerStaticRotate, 1, wx.EXPAND, 0 )
		#---------------rotate ends --------------------
		#---------------mirror starts ------------------        
		self.staticMirror = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"镜像翻转设置" )
		sbSizerStaticMirror = wx.StaticBoxSizer( self.staticMirror, wx.HORIZONTAL )
		
		self.m_staticTextMirror = wx.StaticText( self.m_panel1, wx.ID_ANY, u"翻转方向", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextMirror.Wrap( -1 )
		sbSizerStaticMirror.Add( self.m_staticTextMirror, 0, wx.ALIGN_CENTER | wx.RIGHT, 5 )  
		
		self.m_MirrorModeList = [u'上下镜像', u'左右镜像', u'两者皆选']     
		self.m_MirrorBox = wx.ComboBox( self.m_panel1, value = self.m_MirrorModeList[0], choices = self.m_MirrorModeList, style = wx.CB_READONLY)
		sbSizerStaticMirror.Add( self.m_MirrorBox, 0, wx.ALIGN_CENTER, 5 )  

		bSizerSetting.Add( sbSizerStaticMirror, 1, wx.EXPAND, 0 )
		#---------------mirror ends --------------------
		#--------------- invert starts -----------------
		self.staticInvert = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"底片设置" )
		sbSizerStaticInvert = wx.StaticBoxSizer( self.staticInvert, wx.HORIZONTAL )
		
		self.m_staticTextInvert = wx.StaticText( self.m_panel1, wx.ID_ANY, u"参数调节(-50 ～ 50)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextInvert.Wrap( -1 )
		sbSizerStaticInvert.Add( self.m_staticTextInvert, 0, wx.ALIGN_CENTER|wx.RIGHT, 5 )
		
		self.m_spinCtrlInvert = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"50", wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, -50, 50, 50 )
		sbSizerStaticInvert.Add( self.m_spinCtrlInvert, 0, wx.ALIGN_CENTER, 5 )
		
		bSizerSetting.Add( sbSizerStaticInvert, 1, wx.EXPAND, 0 )
		#----------------invert ends -------------------
		#---------------- lighting starts -------------------
		self.staticLighting = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"灯光设置" )
		sbSizerStaticLighting = wx.StaticBoxSizer( self.staticLighting, wx.HORIZONTAL )
		
		self.m_staticTextLightingPos = wx.StaticText( self.m_panel1, wx.ID_ANY, u"光源位置", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextLightingPos.Wrap( -1 )
		sbSizerStaticLighting.Add( self.m_staticTextLightingPos, 0, wx.ALIGN_CENTER|wx.RIGHT, 5 )
		
		self.m_PosList = [u'左上', u'左中', u'左下', u'中上', u'正中', u'中下', u'右上', u'右中',u'右下']	
		self.m_comboTextLightingPos = wx.ComboBox( self.m_panel1, value = self.m_PosList[4], choices = self.m_PosList, style = wx.CB_READONLY)
		sbSizerStaticLighting.Add( self.m_comboTextLightingPos, 0, wx.ALIGN_CENTER|wx.RIGHT, 5 )
		
		sbSizerStaticLighting.Add( ( 20, -1))
		
		self.m_staticTextLighting = wx.StaticText( self.m_panel1, wx.ID_ANY, u"光照强度(0 ～ 50)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextLighting.Wrap( -1 )
		sbSizerStaticLighting.Add( self.m_staticTextLighting, 0, wx.ALIGN_CENTER|wx.RIGHT, 5 )
		
		self.m_spinCtrlLighting = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"20", wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, 0, 50, 20 )
		sbSizerStaticLighting.Add( self.m_spinCtrlLighting, 0, wx.ALIGN_CENTER, 5 )
		
		bSizerSetting.Add( sbSizerStaticLighting, 1, wx.EXPAND, 0 )
		#----------------lighting ends -------------------		
		#---------------- sketch starts -------------------
		self.staticSketch = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"素描设置" )
		sbSizerStaticSketch = wx.StaticBoxSizer( self.staticSketch, wx.HORIZONTAL )
		
		self.m_staticTextSketch = wx.StaticText( self.m_panel1, wx.ID_ANY, u"边界值(0 ～100)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextSketch.Wrap( -1 )
		sbSizerStaticSketch.Add( self.m_staticTextSketch, 0, wx.ALIGN_CENTER|wx.RIGHT, 5 )
		
		self.m_spinCtrlSketch = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"15", wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, 0, 100, 15 )
		sbSizerStaticSketch.Add( self.m_spinCtrlSketch, 0, wx.ALIGN_CENTER, 5 )
		
		bSizerSetting.Add( sbSizerStaticSketch, 1, wx.EXPAND, 0 )
		#----------------sketch ends -------------------		
		#---------------- papercut starts -------------------
		self.staticPapercut = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"剪纸设置" )
		sbSizerStaticPapercut = wx.StaticBoxSizer( self.staticPapercut, wx.HORIZONTAL )
		
		self.m_staticPapercutBgColor = wx.StaticText( self.m_panel1, wx.ID_ANY, u"背景颜色", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticPapercutBgColor.Wrap( -1 )
		sbSizerStaticPapercut.Add( self.m_staticPapercutBgColor, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		
		self.m_PapercutBgColourPicker = wx.ColourPickerCtrl( self.m_panel1, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.Size( 50,12 ), wx.CLRP_DEFAULT_STYLE )
		sbSizerStaticPapercut.Add( self.m_PapercutBgColourPicker, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		self.cur_PapercutBgColor = wx.BLACK
		
		sbSizerStaticPapercut.Add( ( 20, -1))
		
		self.m_staticPapercutFgColor = wx.StaticText( self.m_panel1, wx.ID_ANY, u"前景颜色", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticPapercutFgColor.Wrap( -1 )		
		sbSizerStaticPapercut.Add( self.m_staticPapercutFgColor, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		
		self.m_PapercutFgColourPicker = wx.ColourPickerCtrl( self.m_panel1, wx.ID_ANY, wx.RED, wx.DefaultPosition, wx.Size( 50,12 ), wx.CLRP_DEFAULT_STYLE )
		sbSizerStaticPapercut.Add( self.m_PapercutFgColourPicker, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		self.cur_PapercutFgColor = wx.RED
		
		sbSizerStaticPapercut.Add( ( 20, -1))
		
		self.m_staticTextPapercut = wx.StaticText( self.m_panel1, wx.ID_ANY, u"边界值(0 ～255)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextPapercut.Wrap( -1 )
		sbSizerStaticPapercut.Add( self.m_staticTextPapercut, 0, wx.ALIGN_CENTER|wx.RIGHT, 5 )
		
		self.m_spinCtrlPapercut = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"20", wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, 0, 255, 20 )
		sbSizerStaticPapercut.Add( self.m_spinCtrlPapercut, 0, wx.ALIGN_CENTER, 5 )
		
		bSizerSetting.Add( sbSizerStaticPapercut, 1, wx.EXPAND, 0 )
		#----------------papercut ends -------------------
		#---------------- deYellow starts -------------------
		self.staticDeYellow = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"新照片设置" )
		sbSizerStaticDeYellow = wx.StaticBoxSizer( self.staticDeYellow, wx.HORIZONTAL )
		
		self.m_radioBoxDeYellow_1 = wx.RadioButton( self.m_panel1, wx.ID_ANY, u"方案1", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
		self.m_radioBoxDeYellow_2 = wx.RadioButton( self.m_panel1, wx.ID_ANY, u"方案2", wx.DefaultPosition, wx.DefaultSize, 0 )		
		sbSizerStaticDeYellow.Add(self.m_radioBoxDeYellow_1, 0, wx.ALL|wx.CENTER, 5 )
		sbSizerStaticDeYellow.Add(self.m_radioBoxDeYellow_2, 0, wx.ALL|wx.CENTER, 5 )		
		bSizerSetting.Add( sbSizerStaticDeYellow, 1, wx.EXPAND, 0 )		
		#----------------deYellow ends -------------------
		#---------------- swirl starts -------------------
		self.staticSwirl = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"漩涡设置" )
		sbSizerStaticSwirl = wx.StaticBoxSizer( self.staticSwirl, wx.HORIZONTAL )
		
		self.m_staticTextSwirl = wx.StaticText( self.m_panel1, wx.ID_ANY, u"漩涡大小", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextSwirl.Wrap( -1 )
		sbSizerStaticSwirl.Add( self.m_staticTextSwirl, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		
		self.m_sliderSwirlOpacity = wx.Slider( self.m_panel1, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, style=wx.SL_HORIZONTAL|wx.SL_LABELS )
		sbSizerStaticSwirl.Add( self.m_sliderSwirlOpacity, 0, wx.ALIGN_CENTER | wx.LEFT, 5 )
		
		bSizerSetting.Add( sbSizerStaticSwirl, 1, wx.EXPAND, 0 )
		#----------------swirl ends -------------------
		#--------------- puzzle starts ------------------
		self.staticPuzzle = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"拼图设置" )
		sbSizerStaticPuzzle = wx.StaticBoxSizer( self.staticPuzzle, wx.VERTICAL )
		bSizerPuzzleUp = wx.BoxSizer( wx.HORIZONTAL )
		bSizerPuzzleDown = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticTextQtyX = wx.StaticText( self.m_panel1, wx.ID_ANY, u"水平数目", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextQtyX.Wrap( -1 )
		bSizerPuzzleUp.Add( self.m_staticTextQtyX, 0, wx.ALL, 5 )    
		
		self.m_spinCtrlQtyX = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"2", wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, 1, 100, 2 )
		bSizerPuzzleUp.Add( self.m_spinCtrlQtyX, 0, wx.ALL, 5 )
		
		bSizerPuzzleUp.Add( ( 5, -1) )
		
		self.m_staticTextQtyY = wx.StaticText( self.m_panel1, wx.ID_ANY, u"垂直数目", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextQtyY.Wrap( -1 )
		bSizerPuzzleUp.Add( self.m_staticTextQtyY, 0, wx.ALL, 5 )    
		
		self.m_spinCtrlQtyY = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"2", wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, 1, 100, 2 )
		bSizerPuzzleUp.Add( self.m_spinCtrlQtyY, 0, wx.ALL, 5 )
		
		bSizerPuzzleUp.Add( ( 5, -1) )
		
		self.m_checkBoxResize = wx.CheckBox(self.m_panel1, label=u'允许缩放', style = wx.BU_EXACTFIT )
		bSizerPuzzleUp.Add( self.m_checkBoxResize, 0, wx.ALL, 5 )
				
		bSizerPuzzleUp.Add( ( 5, -1) )
		
		self.m_staticPuzzleBgColor = wx.StaticText( self.m_panel1, wx.ID_ANY, u"背景颜色", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerPuzzleUp.Add( self.m_staticPuzzleBgColor, 0, wx.ALL, 5 )
		
		self.m_PuzzleBgColourPicker = wx.ColourPickerCtrl( self.m_panel1, wx.ID_ANY, wx.WHITE, wx.DefaultPosition, wx.Size( 45,12 ), wx.CLRP_DEFAULT_STYLE )
		bSizerPuzzleUp.Add( self.m_PuzzleBgColourPicker, 0, wx.ALL, 5 )
		
		bSizerPuzzleUp.Add( ( 5, -1) )	
		
		self.m_PuzzleOrderList = [u'按行', u'按列']      
		self.m_PuzzleOrderBox = wx.ComboBox( self.m_panel1, value = self.m_PuzzleOrderList[0], choices = self.m_PuzzleOrderList, style = wx.CB_READONLY)
		bSizerPuzzleDown.Add( self.m_PuzzleOrderBox, 0, wx.ALL, 5 )
		
		bSizerPuzzleDown.Add( ( 5, -1) )
		
		#self.m_staticTextSrc = wx.StaticText( self.m_panel1, wx.ID_ANY, u"图片来源", wx.DefaultPosition, wx.DefaultSize, 0 )
		#self.m_staticTextSrc.Wrap( -1 )
		#bSizerPuzzleDown.Add( self.m_staticTextSrc, 0, wx.ALIGN_CENTER |wx.RIGHT, 5 )
				
		self.m_PuzzleSrcModeList = [u'重复当前图片', u'所有加载图片']      
		self.m_PuzzleSrcBox = wx.ComboBox( self.m_panel1, value = self.m_PuzzleSrcModeList[0], choices = self.m_PuzzleSrcModeList, style = wx.CB_READONLY)
		bSizerPuzzleDown.Add( self.m_PuzzleSrcBox, 0, wx.ALL, 5 )
		
		bSizerPuzzleDown.Add( ( 15, -1) )
		
		self.m_staticTextGap = wx.StaticText( self.m_panel1, wx.ID_ANY, u"图片间隔(像素)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextGap.Wrap( -1 )
		bSizerPuzzleDown.Add( self.m_staticTextGap, 0, wx.ALL, 5 )    
		
		self.m_spinCtrlGap = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, 0, 100, 0 )
		bSizerPuzzleDown.Add( self.m_spinCtrlGap, 0, wx.ALL, 5 )
		
		self.m_buttonListView = wx.BitmapButton( self.m_panel1, wx.ID_ANY, self.parent.file_list, wx.DefaultPosition, wx.Size(24, 24), wx.NO_BORDER |wx.BU_EXACTFIT  )
		bSizerPuzzleDown.Add( self.m_buttonListView, 0, wx.ALL, 5 )
		self.m_buttonListView.SetToolTipString(u'查看文件列表')
		
		#self.m_buttonListView = wx.Button( self.m_panel1, wx.ID_ANY, u"查看列表", wx.DefaultPosition, wx.DefaultSize, 0 )
		#bSizerPuzzleDown.Add( self.m_buttonListView, 0, wx.ALL, 5 )
		
		sbSizerStaticPuzzle.Add(bSizerPuzzleUp, 1, wx.EXPAND, 5)
		sbSizerStaticPuzzle.Add(bSizerPuzzleDown, 1, wx.EXPAND, 5)

		#self.cur_PuzzleBgColor = (255,255,255,255) #(0, 255, 255, 255)

		bSizerSetting.Add( sbSizerStaticPuzzle, 1, wx.EXPAND, 5 )
		
		#bSizerMain.Add( bSizerSetting, 1, wx.EXPAND, 5 )
		#--------------- puzzle ends -------------------------------
		#--------------- flash light starts ------------------------
		self.staticFocus = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"聚光设置" )
		sbSizerStaticFocus = wx.StaticBoxSizer( self.staticFocus, wx.HORIZONTAL )
		
		self.m_staticTextRadiusIn = wx.StaticText( self.m_panel1, wx.ID_ANY, u"内圈半径(%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticFocus.Add( self.m_staticTextRadiusIn, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_spinCtrlRadiusIn = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"60", wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, 0, 200, 60 )
		sbSizerStaticFocus.Add( self.m_spinCtrlRadiusIn, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		sbSizerStaticFocus.Add((10, -1))
		
		self.m_staticTextRadiusOut = wx.StaticText( self.m_panel1, wx.ID_ANY, u"外圈半径(%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticFocus.Add( self.m_staticTextRadiusOut, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_spinCtrlRadiusOut = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"100", wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, 0, 400, 100 )
		sbSizerStaticFocus.Add( self.m_spinCtrlRadiusOut, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		sbSizerStaticFocus.Add((10, -1))
		
		self.m_staticFocusEdgeColor = wx.StaticText( self.m_panel1, wx.ID_ANY, u"边缘颜色", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticFocus.Add( self.m_staticFocusEdgeColor, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		
		self.m_FocusEdgeColourPicker = wx.ColourPickerCtrl( self.m_panel1, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.Size( 50,12 ), wx.CLRP_DEFAULT_STYLE )
		sbSizerStaticFocus.Add( self.m_FocusEdgeColourPicker, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		
		sbSizerStaticFocus.Add((10, -1))
		
		self.m_checkBoxFocusEdge = wx.CheckBox(self.m_panel1, label=u'边缘透明', style = wx.BU_EXACTFIT )
		sbSizerStaticFocus.Add( self.m_checkBoxFocusEdge, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		bSizerSetting.Add( sbSizerStaticFocus, 1, wx.EXPAND, 0 )
		#---------------- flash light ends -------------------------
		
		#--------------- edge fold starts ------------------------
		self.staticCornerFold = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"折角设置" )
		sbSizerStaticCornerFold = wx.StaticBoxSizer( self.staticCornerFold, wx.HORIZONTAL )
		
		self.m_staticTextEdge = wx.StaticText( self.m_panel1, wx.ID_ANY, u"边距(%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticCornerFold.Add( self.m_staticTextEdge, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_spinCtrlEdge = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"15", wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, 0, 100, 15 )
		sbSizerStaticCornerFold.Add( self.m_spinCtrlEdge, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		sbSizerStaticCornerFold.Add((10, -1))
		
		self.m_staticTextWhitePercent = wx.StaticText( self.m_panel1, wx.ID_ANY, u"白色增强(%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticCornerFold.Add( self.m_staticTextWhitePercent, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_spinCtrlWhitePercent = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"80", wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, 0, 100, 80 )
		sbSizerStaticCornerFold.Add( self.m_spinCtrlWhitePercent, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		sbSizerStaticCornerFold.Add((10, -1))
		
		self.m_staticFoldPos = wx.StaticText( self.m_panel1, wx.ID_ANY, u"折角位置", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticCornerFold.Add( self.m_staticFoldPos, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_FoldPosModeList = [u'左边', u'右边']      
		self.m_FoldPosBox = wx.ComboBox( self.m_panel1, value = self.m_FoldPosModeList[1], choices = self.m_FoldPosModeList, style = wx.CB_READONLY)
		sbSizerStaticCornerFold.Add( self.m_FoldPosBox, 0, wx.ALIGN_CENTER, 5 )
		bSizerSetting.Add( sbSizerStaticCornerFold, 1, wx.EXPAND, 0 )

		#---------------- edge fold ends -------------------------
		#--------------- tear starts ------------------------
		self.staticTear = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"锯齿边缘设置" )
		sbSizerStaticTear = wx.StaticBoxSizer( self.staticTear, wx.HORIZONTAL )		
		
		self.m_staticTearDirection = wx.StaticText( self.m_panel1, wx.ID_ANY, u"锯齿方向", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticTear.Add( self.m_staticTearDirection, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_TearPosModeList = [u'左右', u'上下']      
		self.m_TearPosBox = wx.ComboBox( self.m_panel1, value = self.m_TearPosModeList[0], choices = self.m_TearPosModeList, style = wx.CB_READONLY)
		sbSizerStaticTear.Add( self.m_TearPosBox, 0, wx.ALIGN_CENTER, 5 )
		sbSizerStaticTear.Add((10, -1))
		
		self.m_staticTextTear = wx.StaticText( self.m_panel1, wx.ID_ANY, u"锯齿位置(%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticTear.Add( self.m_staticTextTear, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_spinCtrlTear = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"80", wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, 0, 100, 80 )
		sbSizerStaticTear.Add( self.m_spinCtrlTear, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_checkBoxIsCut = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"自动裁剪", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxIsCut.SetValue(True)
		sbSizerStaticTear.Add( self.m_checkBoxIsCut, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		bSizerSetting.Add( sbSizerStaticTear, 1, wx.EXPAND, 0 )
		#--------------- tear ends ------------------------
		#--------------- Fade starts ------------------------
		self.staticFade = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"渐变设置" )
		sbSizerStaticFade = wx.StaticBoxSizer( self.staticFade, wx.HORIZONTAL )
		
		self.m_staticTextFadePos = wx.StaticText( self.m_panel1, wx.ID_ANY, u"渐变位置(%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticFade.Add( self.m_staticTextFadePos, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_spinCtrlFadePos = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"70", wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, 0, 100, 70 )
		sbSizerStaticFade.Add( self.m_spinCtrlFadePos, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		sbSizerStaticFade.Add((10, -1))
		
		self.m_staticFadeMode = wx.StaticText( self.m_panel1, wx.ID_ANY, u"渐变模式", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticFade.Add( self.m_staticFadeMode, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		
		self.m_FadeModeList = [u'淡入', u'淡出']      
		self.m_FadeModeBox = wx.ComboBox( self.m_panel1, value = self.m_FadeModeList[1], choices = self.m_FadeModeList, style = wx.CB_READONLY)
		sbSizerStaticFade.Add( self.m_FadeModeBox, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		
		sbSizerStaticFade.Add((10, -1))
		
		self.m_staticFadeColor = wx.StaticText( self.m_panel1, wx.ID_ANY, u"渐变颜色", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticFade.Add( self.m_staticFadeColor, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		
		self.m_FadeColourPicker = wx.ColourPickerCtrl( self.m_panel1, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.Size( 50,12 ), wx.CLRP_DEFAULT_STYLE )
		sbSizerStaticFade.Add( self.m_FadeColourPicker, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		
		bSizerSetting.Add( sbSizerStaticFade, 1, wx.EXPAND, 0 )
		
		#--------------- Mix starts ------------------------
		self.staticMix = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"混色设置" )
		sbSizerStaticMix = wx.StaticBoxSizer( self.staticMix, wx.HORIZONTAL )
		
		self.m_staticTextMixFactor = wx.StaticText( self.m_panel1, wx.ID_ANY, u"增强系数(%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticMix.Add( self.m_staticTextMixFactor, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_spinCtrlMixFactor = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"20", wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, 0, 100, 20 )
		sbSizerStaticMix.Add( self.m_spinCtrlMixFactor, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		sbSizerStaticMix.Add((10, -1))
		
		self.m_staticMixColor = wx.StaticText( self.m_panel1, wx.ID_ANY, u"添加颜色", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticMix.Add( self.m_staticMixColor, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )

		self.m_MixColourPicker = wx.ColourPickerCtrl( self.m_panel1, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.Size( 50,12 ), wx.CLRP_DEFAULT_STYLE)
		sbSizerStaticMix.Add(self.m_MixColourPicker, 0, wx.ALIGN_CENTER|wx.LEFT, 5)
				
		self.ctrlColor = wx.TextCtrl( self.m_panel1, wx.ID_ANY, '(0, 0, 0, 255)', wx.DefaultPosition, wx.Size( 120,-1 ), wx.TE_PROCESS_ENTER )
		sbSizerStaticMix.Add( self.ctrlColor, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		
		self.ctrlColor.SetToolTipString(COLOR_FORMAT_TIP)
		self.ctrlColor.Bind(wx.EVT_TEXT, self.OnMixTxtChanged)
		
		bSizerSetting.Add( sbSizerStaticMix, 1, wx.EXPAND, 0 )
		
				
		#--------------- color replace starts ------------------------
		self.staticReplace = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"颜色替换设置" )
		sbSizerStaticReplace = wx.StaticBoxSizer( self.staticReplace, wx.VERTICAL )		
		sbSizerStaticRegion = wx.BoxSizer(wx.HORIZONTAL )
		sbSizerStaticColorReplace = wx.BoxSizer(wx.HORIZONTAL )
		
		self.replaceModeStyleList = [u'颜色替换', u'颜色填充']
		self.m_checkBoxReplaceStyle = wx.ComboBox(self.m_panel1, value = self.replaceModeStyleList[0], choices = self.replaceModeStyleList, style = wx.CB_READONLY )
		sbSizerStaticRegion.Add( self.m_checkBoxReplaceStyle, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		self.m_staticTextModeTip = wx.StaticText( self.m_panel1, label = u"处理鼠标选定的区域；默认是整个图片。" )
		self.m_staticTextModeTip.Enable( False )
		sbSizerStaticRegion.Add( self.m_staticTextModeTip, 0, wx.ALIGN_CENTER|wx.LEFT, 5 ) #wx.LEFT | wx.TOP, 22 )
		self.m_checkBoxReplaceStyle.Bind(wx.EVT_COMBOBOX_CLOSEUP, self.OnReplaceModeChanged)
		
		self.m_staticOldColor = wx.StaticText( self.m_panel1, wx.ID_ANY, u"旧颜色", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticColorReplace.Add( self.m_staticOldColor, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		
		fgSizerReplace = wx.FlexGridSizer( 2, 3, 0, 0 )
		fgSizerReplace.SetFlexibleDirection( wx.HORIZONTAL )
		fgSizerReplace.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_ColorCompare = [u'>',u'=', u'≠',u'<',u'从']      
		self.m_ColorCompareBox = wx.ComboBox( self.m_panel1, value = self.m_ColorCompare[1], choices = self.m_ColorCompare, style = wx.CB_READONLY)
		fgSizerReplace.Add( self.m_ColorCompareBox, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		self.m_ColorCompareBox.Bind (wx.EVT_COMBOBOX, self.OnColorComboChanged )

		self.m_OldColourPicker = wx.ColourPickerCtrl( self.m_panel1, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.Size( 50,12 ), wx.CLRP_DEFAULT_STYLE)
		fgSizerReplace.Add(self.m_OldColourPicker, 0, wx.ALIGN_CENTER|wx.LEFT, 5)	
				
		self.ctrlOldColor = wx.TextCtrl( self.m_panel1, wx.ID_ANY, '(0, 0, 0, 255)', wx.DefaultPosition, wx.Size( 120,-1 ), wx.TE_PROCESS_ENTER )
		fgSizerReplace.Add( self.ctrlOldColor, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
				
		self.ctrlOldColor.SetToolTipString(COLOR_FORMAT_TIP)
		self.ctrlOldColor.Bind(wx.EVT_TEXT, self.OnOldTxtChanged)
		
		self.m_staticTextOldMax = wx.StaticText( self.m_panel1, wx.ID_ANY, u"到", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerReplace.Add( self.m_staticTextOldMax, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.m_OldColourMaxPicker = wx.ColourPickerCtrl( self.m_panel1, wx.ID_ANY, wx.WHITE, wx.DefaultPosition, wx.Size( 50,12 ), wx.CLRP_DEFAULT_STYLE)
		fgSizerReplace.Add(self.m_OldColourMaxPicker, 0, wx.ALIGN_CENTER|wx.LEFT, 5)	
				
		self.ctrlOldColorMax = wx.TextCtrl( self.m_panel1, wx.ID_ANY, '(255, 255, 255, 255)', wx.DefaultPosition, wx.Size( 120,-1 ), wx.TE_PROCESS_ENTER )
		fgSizerReplace.Add( self.ctrlOldColorMax, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
				
		self.ctrlOldColorMax.SetToolTipString(COLOR_FORMAT_TIP)
		self.ctrlOldColorMax.Bind(wx.EVT_TEXT, self.OnOldTxtMaxChanged)
		
		sbSizerStaticColorReplace.Add( fgSizerReplace, 1, wx.ALIGN_CENTER|wx.LEFT, 0 )
		
		sbSizerStaticReplace.Add((15, -1))
		
		self.m_staticNewColor = wx.StaticText( self.m_panel1, wx.ID_ANY, u"新颜色", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticColorReplace.Add( self.m_staticNewColor, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )

		self.m_NewColourPicker = wx.ColourPickerCtrl( self.m_panel1, wx.ID_ANY, wx.RED, wx.DefaultPosition, wx.Size( 50,12 ), wx.CLRP_DEFAULT_STYLE)
		sbSizerStaticColorReplace.Add(self.m_NewColourPicker, 0, wx.ALIGN_CENTER|wx.LEFT, 5)
				
		self.ctrlNewColor = wx.TextCtrl( self.m_panel1, wx.ID_ANY, '(255, 0, 0, 255)', wx.DefaultPosition, wx.Size( 120,-1 ), wx.TE_PROCESS_ENTER )
		sbSizerStaticColorReplace.Add( self.ctrlNewColor, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		
		self.ctrlNewColor.SetToolTipString(COLOR_FORMAT_TIP)
		self.ctrlNewColor.Bind(wx.EVT_TEXT, self.OnNewTxtChanged)
		
		sbSizerStaticReplace.Add( sbSizerStaticRegion, 1, wx.EXPAND, 0 )
		sbSizerStaticReplace.Add( sbSizerStaticColorReplace, 1, wx.EXPAND, 0 )
		bSizerSetting.Add( sbSizerStaticReplace, 1, wx.EXPAND, 0 )
		#--------------- Auto brightness starts ------------------------
		self.staticAutoBrightness = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"自动亮度设置" )
		sbSizerStaticAutoBrightness = wx.StaticBoxSizer( self.staticAutoBrightness, wx.HORIZONTAL )
		
		self.m_staticCurBrightness = wx.StaticText( self.m_panel1, wx.ID_ANY, u"当前亮度", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticAutoBrightness.Add( self.m_staticCurBrightness, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		self.ctrlCurBrightness = wx.TextCtrl( self.m_panel1, wx.ID_ANY, '', wx.DefaultPosition, wx.Size( 80,-1 ), wx.TE_READONLY )
		sbSizerStaticAutoBrightness.Add( self.ctrlCurBrightness, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		
		sbSizerStaticAutoBrightness.Add((15, -1))
		
		self.m_staticNewBrightness = wx.StaticText( self.m_panel1, wx.ID_ANY, u"新亮度", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticAutoBrightness.Add( self.m_staticNewBrightness, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		self.m_spinCtrlNewBrightness = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"200", wx.DefaultPosition, wx.Size( 80,-1 ), wx.SP_ARROW_KEYS, 0, 255, 200 )
		sbSizerStaticAutoBrightness.Add( self.m_spinCtrlNewBrightness, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		bSizerSetting.Add( sbSizerStaticAutoBrightness, 1, wx.EXPAND, 0 )
		#--------------- roll starts --------------------------
		self.staticRoll = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"滚动设置" )
		sbSizerStaticRoll = wx.StaticBoxSizer( self.staticRoll, wx.HORIZONTAL )
		
		#sbSizerStaticRoll.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticHTextRoll = wx.StaticText( self.m_panel1, wx.ID_ANY, u"水平偏移(像素)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticHTextRoll.Wrap( -1 )
		sbSizerStaticRoll.Add( self.m_staticHTextRoll, 0, wx.ALIGN_CENTER|wx.RIGHT, 5 )
		
		self.m_textCtrlRollHBox = wx.TextCtrl( self.m_panel1, wx.ID_ANY, '10', wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		sbSizerStaticRoll.Add( self.m_textCtrlRollHBox, 0, wx.ALIGN_CENTER, 5 )
		
		sbSizerStaticRoll.Add( (20, -1))
		
		self.m_staticVTextRoll = wx.StaticText( self.m_panel1, wx.ID_ANY, u"垂直偏移(像素)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticVTextRoll.Wrap( -1 )
		sbSizerStaticRoll.Add( self.m_staticVTextRoll, 0, wx.ALIGN_CENTER|wx.RIGHT, 5 )
		
		self.m_textCtrlRollVBox = wx.TextCtrl( self.m_panel1, wx.ID_ANY, '10', wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		sbSizerStaticRoll.Add( self.m_textCtrlRollVBox, 0, wx.ALIGN_CENTER, 5 )      

		bSizerSetting.Add( sbSizerStaticRoll, 1, wx.EXPAND, 0 ) 
		#---------------  shear starts ------------------------
		self.staticShear = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"倾斜效果设置" )
		sbSizerStaticShear = wx.StaticBoxSizer( self.staticShear, wx.HORIZONTAL )
		
		self.m_staticTextXdegree = wx.StaticText( self.m_panel1, wx.ID_ANY, u"X方向(度)", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticShear.Add( self.m_staticTextXdegree, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_spinCtrlXdegree = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"30", wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, 0, 90, 30 )
		sbSizerStaticShear.Add( self.m_spinCtrlXdegree, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		sbSizerStaticShear.Add((10, -1))
		
		self.m_staticTextYdegree = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Y方向(度)", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticShear.Add( self.m_staticTextYdegree, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_spinCtrlYdegree = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, 0, 90, 0 )
		sbSizerStaticShear.Add( self.m_spinCtrlYdegree, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		sbSizerStaticShear.Add((10, -1))
		
		self.m_staticShearBkColor = wx.StaticText( self.m_panel1, wx.ID_ANY, u"背景颜色", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticShear.Add( self.m_staticShearBkColor, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )

		self.m_ShearColorPicker = wx.ColourPickerCtrl( self.m_panel1, wx.ID_ANY, wx.RED, wx.DefaultPosition, wx.Size( 50,12 ), wx.CLRP_DEFAULT_STYLE)
		sbSizerStaticShear.Add(self.m_ShearColorPicker, 0, wx.ALIGN_CENTER|wx.LEFT, 5)
				
		self.ctrlShearBkColor = wx.TextCtrl( self.m_panel1, wx.ID_ANY, '(255, 0, 0, 255)', wx.DefaultPosition, wx.Size( 120,-1 ), wx.TE_PROCESS_ENTER )
		sbSizerStaticShear.Add( self.ctrlShearBkColor, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		self.ctrlShearBkColor.SetToolTipString(COLOR_FORMAT_TIP)
		self.ctrlShearBkColor.Bind(wx.EVT_TEXT, self.OnShearTxtChanged)
		bSizerSetting.Add( sbSizerStaticShear, 1, wx.EXPAND, 0 )
		
		#--------------- Mosaic starts ------------------------
		self.staticMosaic = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"马赛克设置" )
		sbSizerStaticMosaic = wx.StaticBoxSizer( self.staticMosaic, wx.HORIZONTAL )
		
		self.m_staticTextMosaicSize = wx.StaticText( self.m_panel1, wx.ID_ANY, u"马赛克大小(像素)", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticMosaic.Add( self.m_staticTextMosaicSize, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_spinCtrlMosaicSize = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"8", wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, 2, 200, 8 )
		sbSizerStaticMosaic.Add( self.m_spinCtrlMosaicSize, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		sbSizerStaticMosaic.Add((10, -1))
		self.m_staticTextMosaicTip = wx.StaticText( self.m_panel1, label = u"处理鼠标选定的区域；默认是整个图片。" )
		self.m_staticTextMosaicTip.Enable( False )
		sbSizerStaticMosaic.Add( self.m_staticTextMosaicTip, 0, wx.ALIGN_CENTER|wx.ALL, 5 ) #wx.LEFT | wx.TOP, 22 )	
		
		bSizerSetting.Add( sbSizerStaticMosaic, 1, wx.EXPAND, 0 )
		
		#---------------- Mask starts -----------------------------
		self.staticMask = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"蒙版效果设置" )
		sbSizerStaticMask = wx.StaticBoxSizer( self.staticMask, wx.HORIZONTAL )
		
		self.m_staticTextMask = wx.StaticText( self.m_panel1, wx.ID_ANY, u"选择蒙版", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticMask.Add( self.m_staticTextMask, 0, wx.ALIGN_CENTER|wx.RIGHT, 5 )
		
		self.m_textCtrlMaskPath = wx.TextCtrl( self.m_panel1, wx.ID_ANY, self.parent.mask_path, wx.DefaultPosition, (180, -1), wx.TE_READONLY)
		sbSizerStaticMask.Add( self.m_textCtrlMaskPath, 0, wx.ALIGN_CENTER|wx.RIGHT, 5 )
		self.mask = None         
		
		self.m_btnMaskBrowse = wx.Button( self.m_panel1, wx.ID_ANY, u"...", wx.DefaultPosition, (-1, 21), wx.BU_EXACTFIT )
		sbSizerStaticMask.Add( self.m_btnMaskBrowse, 0, wx.ALIGN_CENTER|wx.RIGHT, 5 )
		self.m_btnMaskBrowse.SetToolTipString('要求指定的蒙版与当前图片大小相同；\r\n否则会引起缩放失真。')
		
		self.m_staticTextMaskBg = wx.StaticText( self.m_panel1, wx.ID_ANY, u"背景颜色", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticMask.Add( self.m_staticTextMaskBg, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )
		
		self.m_MaskBgColorPicker = wx.ColourPickerCtrl( self.m_panel1, wx.ID_ANY, wx.WHITE, wx.DefaultPosition, wx.Size( 50,12 ), wx.CLRP_DEFAULT_STYLE)
		sbSizerStaticMask.Add(self.m_MaskBgColorPicker, 0, wx.ALIGN_CENTER|wx.LEFT, 5)
				
		self.ctrlMaskBgColor = wx.TextCtrl( self.m_panel1, wx.ID_ANY, '(255, 255, 255, 255)', wx.DefaultPosition, wx.Size( 120,-1 ), wx.TE_PROCESS_ENTER )
		sbSizerStaticMask.Add( self.ctrlMaskBgColor, 0, wx.ALIGN_CENTER|wx.LEFT | wx.RIGHT, 5 )
		
		self.ctrlMaskBgColor.SetToolTipString(COLOR_FORMAT_TIP)
		self.ctrlMaskBgColor.Bind(wx.EVT_TEXT, self.OnMaskBgTxtChanged)
		
		bSizerSetting.Add( sbSizerStaticMask, 1, wx.EXPAND, 0 )
		
		#---------------- Blend starts -----------------------------
		self.staticBlend = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"混合效果设置" )
		sbSizerStaticBlend = wx.StaticBoxSizer( self.staticBlend, wx.HORIZONTAL )
		
		self.m_staticTextBlend = wx.StaticText( self.m_panel1, wx.ID_ANY, u"选择图片", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticBlend.Add( self.m_staticTextBlend, 0, wx.ALIGN_CENTER|wx.RIGHT, 5 )
		
		self.m_textCtrlImg2Path = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, (220, -1), wx.TE_READONLY)
		sbSizerStaticBlend.Add( self.m_textCtrlImg2Path, 0, wx.ALIGN_CENTER|wx.RIGHT, 5 )
		self.img2 = None         
		
		self.m_btnBlendBrowse = wx.Button( self.m_panel1, wx.ID_ANY, u"...", wx.DefaultPosition, (-1, 21), wx.BU_EXACTFIT )
		sbSizerStaticBlend.Add( self.m_btnBlendBrowse, 0, wx.ALIGN_CENTER|wx.RIGHT, 5 )
		self.m_btnBlendBrowse.SetToolTipString('要求指定的图片与当前图片大小相同；\r\n否则会引起缩放失真。')
		
		sbSizerStaticBlend.AddSpacer( ( 10, 0) )
		
		self.m_staticTextAlpha = wx.StaticText( self.m_panel1, wx.ID_ANY, u"不透明度", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticBlend.Add( self.m_staticTextAlpha, 0, wx.ALIGN_CENTER|wx.RIGHT, 5 )
		
		self.m_spinCtrlAlpha = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"50", wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, 0, 100, 0 )
		sbSizerStaticBlend.Add( self.m_spinCtrlAlpha, 0, wx.ALIGN_CENTER|wx.RIGHT, 5 )		
		
		self.m_staticTextPercent = wx.StaticText( self.m_panel1, wx.ID_ANY, u"%", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticBlend.Add( self.m_staticTextPercent, 0, wx.ALIGN_CENTER|wx.RIGHT, 5 )
		
		bSizerSetting.Add( sbSizerStaticBlend, 1, wx.EXPAND, 0 )
		#------------------ split starts ---------------------------
		self.staticSplit = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"图片分割" )
		sbSizerStaticSplit = wx.StaticBoxSizer( self.staticSplit, wx.HORIZONTAL )
		#sbSizerStaticEnhance.Add(self.staticEnhance, 0, wx.ALL|wx.RIGHT, 5 )
		
		#self.m_staticTextRow = wx.StaticText( self.m_panel1, wx.ID_ANY, u"水平数目", wx.DefaultPosition, wx.DefaultSize, 0 )
		#self.m_staticTextRow.Wrap( -1 )
		#sbSizerStaticSplit.Add( self.m_staticTextRow, 0, wx.ALIGN_CENTER | wx.RIGHT, 5 )
		
		# add pixel option
		m_choicePixelChoicesX = [ u"水平数目", u"水平像素" ]
		self.m_choicePixelX = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choicePixelChoicesX, 0 )
		self.m_choicePixelX.SetSelection( 0 )
		sbSizerStaticSplit.Add( self.m_choicePixelX, 0, wx.ALL | wx.ALIGN_CENTER, 5 )
		
		self.m_spinCtrlRow = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"2", wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, 1, 10000, 2 )
		sbSizerStaticSplit.Add( self.m_spinCtrlRow, 0, wx.ALL | wx.ALIGN_CENTER, 5 )
		
		sbSizerStaticSplit.Add( ( 15, -1) )
		
		#self.m_staticTextCol = wx.StaticText( self.m_panel1, wx.ID_ANY, u"垂直数目", wx.DefaultPosition, wx.DefaultSize, 0 )
		#self.m_staticTextCol.Wrap( -1 )
		#sbSizerStaticSplit.Add( self.m_staticTextCol, 0, wx.ALIGN_CENTER | wx.RIGHT, 5 )
		m_choicePixelChoicesY = [ u"垂直数目", u"垂直像素" ]
		self.m_choicePixelY = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choicePixelChoicesY, 0 )
		self.m_choicePixelY.SetSelection( 0 )
		sbSizerStaticSplit.Add( self.m_choicePixelY, 0, wx.ALL | wx.ALIGN_CENTER, 5 )
		
		self.m_spinCtrlCol = wx.SpinCtrl( self.m_panel1, wx.ID_ANY, u"2", wx.DefaultPosition, wx.Size( 60,-1 ), wx.SP_ARROW_KEYS, 1, 10000, 2 )
		sbSizerStaticSplit.Add( self.m_spinCtrlCol, 0, wx.ALL | wx.ALIGN_CENTER, 5 )	
		
		sbSizerStaticSplit.Add((5, -1))
		
		self.m_staticLineColor = wx.StaticText( self.m_panel1, wx.ID_ANY, u"预览线条颜色", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticSplit.Add( self.m_staticLineColor, 0, wx.ALL | wx.ALIGN_CENTER|wx.LEFT, 5 )

		self.m_LineColourPicker = wx.ColourPickerCtrl( self.m_panel1, wx.ID_ANY, wx.WHITE, wx.DefaultPosition, wx.Size( 50,12 ), wx.CLRP_DEFAULT_STYLE)
		sbSizerStaticSplit.Add(self.m_LineColourPicker, 0, wx.ALL | wx.ALIGN_CENTER|wx.LEFT, 5)				
	
		self.m_LineColourPicker.SetToolTipString(SPLIT_LINE_COLOR_TIP)

		bSizerSetting.Add( sbSizerStaticSplit, 1, wx.EXPAND, 0 )
		# ------------------------------------ slice gone ----------------------				
		self.staticSliceGone = wx.StaticBox( self.m_panel1, wx.ID_ANY, u"中间去除" )
		sbSizerStaticSliceGone = wx.StaticBoxSizer( self.staticSliceGone, wx.HORIZONTAL )
		
		self.sliceModeStyleList = [u'上下', u'左右']
		self.m_checkBoxSliceStyle = wx.ComboBox(self.m_panel1, value = self.sliceModeStyleList[0], choices = self.sliceModeStyleList, style = wx.CB_READONLY )
		sbSizerStaticSliceGone.Add( self.m_checkBoxSliceStyle, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticSlice = wx.StaticText( self.m_panel1, wx.ID_ANY, u"拼接", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerStaticSliceGone.Add( self.m_staticSlice, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		sbSizerStaticSliceGone.Add((10, -1))
		
		self.m_staticSliceModeTip = wx.StaticText( self.m_panel1, label = u"请使用鼠标，选定要去除的中间部分" )
		self.m_staticSliceModeTip.Enable( False )
		sbSizerStaticSliceGone.Add( self.m_staticSliceModeTip, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		bSizerSetting.Add( sbSizerStaticSliceGone, 1, wx.EXPAND, 0 )

		#--------------the bottom buttons starts -------------------
		bSizerMain.Add( bSizerSetting, 1, wx.EXPAND, 5 )
		
		bSizerBtnBottom = wx.BoxSizer( wx.HORIZONTAL )  
		bSizerBtnBottom.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_preview = wx.BitmapButton( self.m_panel1, wx.ID_ANY, self.parent.preview_ico, wx.DefaultPosition, wx.Size(48, 48), wx.NO_BORDER |wx.BU_EXACTFIT  )
		bSizerBtnBottom.Add( self.m_preview, 0, wx.ALL|wx.RIGHT, 5 )
		self.m_preview.SetToolTipString(u'预览效果')
		
		self.m_reset = wx.BitmapButton( self.m_panel1, wx.ID_ANY, self.parent.refresh_ico, wx.DefaultPosition, wx.Size(48, 48), wx.NO_BORDER|wx.BU_EXACTFIT  )
		bSizerBtnBottom.Add( self.m_reset, 0, wx.ALL|wx.RIGHT, 5 )
		self.m_reset.SetToolTipString(u'重新加载')
		
		self.m_close = wx.BitmapButton( self.m_panel1, wx.ID_ANY, self.parent.close32_ico, wx.DefaultPosition, wx.Size(48, 48), wx.NO_BORDER|wx.BU_EXACTFIT  )
		bSizerBtnBottom.Add( self.m_close, 0, wx.ALL|wx.RIGHT, 5 )
		self.m_close.SetToolTipString(u'关闭')
		
		bSizerMain.Add( bSizerBtnBottom, 1, wx.EXPAND, 5 )
		
		self.lb_info = wx.StaticText(self, label=u'友情提示：有些效果需要较长时间, 请耐心等待。')
		self.lb_info.Enable(False)
		bSizerMain.Add(self.lb_info, 0, wx.ALL|wx.CENTER, 5 )
		#--------------the bottom buttons starts -------------------		
		
		self.m_panel1.SetSizer( bSizerMain )
		self.m_panel1.Layout()
		bSizerMain.Fit( self.m_panel1 )
		bSizer1.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )

		self.SetSizer( bSizer1 )                
		self.Layout()           
		self.Centre( wx.BOTH )
		self.RefreshTitle()
		
		# Connect Events
		self.m_buttonDel.Bind( wx.EVT_BUTTON, self.OnDel)
		self.m_buttonDelAll.Bind( wx.EVT_BUTTON, self.OnDelAll)
		self.m_btnUP.Bind( wx.EVT_BUTTON, self.OnBtnUp )
		self.m_btnDown.Bind( wx.EVT_BUTTON, self.OnBtnDown )
		self.m_buttonRound.Bind( wx.EVT_TOGGLEBUTTON, self.OnRoundClick )
		self.m_buttonBackground.Bind( wx.EVT_TOGGLEBUTTON, self.OnBackgroundClick )
		self.m_bpButtonPlus.Bind( wx.EVT_BUTTON, self.OnPlus )
		self.m_checkBoxDefault.Bind( wx.EVT_CHECKBOX, self.OnCheckDefault )
		#self.m_checkBoxIsCut.Bind (wx.EVT_CHECKBOX, self.OnCheckIsCut )
		self.m_radioBtnCkColor.Bind( wx.EVT_RADIOBUTTON, self.OnCheckColor )
		self.m_radioBtnCkPic.Bind( wx.EVT_RADIOBUTTON, self.OnCheckPic )
		self.m_btnBrowse.Bind( wx.EVT_BUTTON, self.OnBtnBrowse )
		self.m_btnMaskBrowse.Bind (wx.EVT_BUTTON, self.OnBtnMaskBrowse )
		self.m_btnBlendBrowse.Bind ( wx.EVT_BUTTON, self.OnBtnBlendBrowse )
		self.m_preview.Bind( wx.EVT_BUTTON, self.OnPreview )
		self.m_reset.Bind( wx.EVT_BUTTON, self.OnReset )
		self.m_close.Bind( wx.EVT_BUTTON, self.OnClose )
		#self.m_bgColourPicker.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnBgColorChanged)
		self.m_buttonBorder.Bind(wx.EVT_TOGGLEBUTTON, self.OnBorderClick)
		#self.m_borderColourPicker.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnBorderColorChanged)
		self.m_buttonShadow.Bind(wx.EVT_TOGGLEBUTTON, self.OnShadowClick)
		#self.m_ReflectionBgColourPicker.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnReflectionColorChanged)
		self.m_buttonReflection.Bind(wx.EVT_TOGGLEBUTTON, self.OnReflectionClick)
		self.m_buttonEnhance.Bind(wx.EVT_TOGGLEBUTTON, self.OnEnhanceClick)
		self.m_buttonFilter.Bind(wx.EVT_TOGGLEBUTTON, self.OnFilterClick)
		self.m_buttonRotate.Bind(wx.EVT_TOGGLEBUTTON, self.OnRotateClick)
		self.m_buttonMirror.Bind(wx.EVT_TOGGLEBUTTON, self.OnMirrorClick)
		self.m_buttonInvert.Bind(wx.EVT_TOGGLEBUTTON, self.OnInvertClick)
		#self.m_buttonMolten.Bind(wx.EVT_TOGGLEBUTTON, self.OnMoltenClick)
		self.m_buttonLighting.Bind(wx.EVT_TOGGLEBUTTON, self.OnLightingClick)
		self.m_buttonSketch.Bind(wx.EVT_TOGGLEBUTTON, self.OnSketchClick)
		#self.m_buttonIce.Bind(wx.EVT_TOGGLEBUTTON, self.OnIceClick)
		self.m_buttonPapercut.Bind(wx.EVT_TOGGLEBUTTON, self.OnPapercutClick)
		#self.m_buttonTan.Bind(wx.EVT_TOGGLEBUTTON, self.OnTanClick)
		self.m_buttonSwirl.Bind(wx.EVT_TOGGLEBUTTON, self.OnSwirlClick)
		#self.m_buttonSpherize.Bind(wx.EVT_TOGGLEBUTTON, self.OnSpherizeClick)
		self.m_buttonDeYellow.Bind(wx.EVT_TOGGLEBUTTON, self.OnDeYellowClick)				
		self.m_radioBtnAny.Bind(wx.EVT_RADIOBUTTON, self.OnBtnAnyClick)
		self.m_radioBtnFixed.Bind(wx.EVT_RADIOBUTTON, self.OnBtnFixedClick)
		self.m_buttonPuzzle.Bind(wx.EVT_TOGGLEBUTTON, self.OnPuzzleClick)
		self.m_buttonFocus.Bind(wx.EVT_TOGGLEBUTTON, self.OnFocusClick)
		self.m_buttonCornerFold.Bind(wx.EVT_TOGGLEBUTTON, self.OnCornerFoldClick)
		self.m_buttonTear.Bind(wx.EVT_TOGGLEBUTTON, self.OnTearClick)
		self.m_buttonFade.Bind(wx.EVT_TOGGLEBUTTON, self.OnFadeClick)
		self.m_buttonMix.Bind(wx.EVT_TOGGLEBUTTON, self.OnMixClick)
		self.m_buttonReplace.Bind(wx.EVT_TOGGLEBUTTON, self.OnReplaceClick)
		self.m_MixColourPicker.Bind (wx.EVT_COLOURPICKER_CHANGED, self.OnMixColorChanged)
		self.m_OldColourPicker.Bind (wx.EVT_COLOURPICKER_CHANGED, self.OnOldColorChanged)
		self.m_OldColourMaxPicker.Bind (wx.EVT_COLOURPICKER_CHANGED, self.OnOldColorMaxChanged)
		self.m_NewColourPicker.Bind (wx.EVT_COLOURPICKER_CHANGED, self.OnNewColorChanged)
		self.m_MaskBgColorPicker.Bind (wx.EVT_COLOURPICKER_CHANGED, self.OnMaskBgColorChanged)
		self.m_buttonAutoBrightness.Bind(wx.EVT_TOGGLEBUTTON, self.OnAutoBrightnessClick)
		self.m_ShearColorPicker.Bind (wx.EVT_COLOURPICKER_CHANGED, self.OnShearColorChanged)
		self.m_buttonShear.Bind(wx.EVT_TOGGLEBUTTON, self.OnShearClick)
		self.m_buttonRoll.Bind(wx.EVT_TOGGLEBUTTON, self.OnRollClick)
		self.m_buttonMosaic.Bind(wx.EVT_TOGGLEBUTTON, self.OnMosaicClick)
		self.m_buttonMask.Bind(wx.EVT_TOGGLEBUTTON, self.OnMaskClick)
		self.m_buttonBlend.Bind(wx.EVT_TOGGLEBUTTON, self.OnBlendClick)
		self.m_buttonWaterMark.Bind(wx.EVT_TOGGLEBUTTON, self.OnWaterMarkClick)
		self.m_buttonSplit.Bind(wx.EVT_TOGGLEBUTTON, self.OnSplitClick)
		self.m_buttonSlice.Bind(wx.EVT_TOGGLEBUTTON, self.OnSliceClick)
		self.m_buttonListView.Bind( wx.EVT_BUTTON, self.OnListView )
		
		#self.Bind (wx.EVT_LEAVE_WINDOW, self.OnLeave)
		
		# Toggle the following controls
		self.toggleCheckBox(self.m_checkBoxDefault)
		self.toggleRoundPanel(False)
		self.toggleBackgroundPanel(False)
		self.toggleRadioBox()
		self.toggleBorderPanel(False)
		self.toggleShadowPanel(False)
		self.toggleReflectionPanel(False)
		self.toggleEnhancePanel(False)
		self.toggleFilterPanel(False)		
		self.toggleRotatePanel(False)
		self.toggleMirrorPanel(False)
		self.toggleInvertPanel(False)
		self.toggleLightingPanel(False)
		self.toggleSketchPanel(False)
		self.togglePapercutPanel(False)
		self.toggleSwirlPanel(False)		
		#self.toggleSpherizePanel(False)
		self.toggleDeYellowPanel(False)
		self.togglePuzzlePanel(False)
		self.toggleFocusPanel(False)
		self.toggleCornerFoldPanel(False)
		self.toggleTearPanel(False)
		self.toggleFadePanel(False)
		self.toggleMixPanel (False)
		self.toggleReplacePanel (False)
		self.toggleAutoBrightnessPanel (False )
		self.toggleShearPanel (False)
		self.toggleRollPanel (False)
		self.toggleMosaicPanel(False)
		self.toggleMaskPanel(False)
		self.toggleBlendPanel (False)
		self.toggleSplitPanel (False)
		self.toggleSlicePanel (False)
		
		ctrl_focus_list = [self.ctrlOldColor, self.ctrlOldColorMax, self.ctrlNewColor, self.ctrlShearBkColor, self.ctrlMaskBgColor, self.ctrlColor ]
		for ctrl in ctrl_focus_list: ctrl.Bind(wx.EVT_LEFT_DOWN, self.OnCtrlClick)
	
	def OnListView( self, event ):
		if not self.list_view_dlg:
			self.list_view_dlg = ShowListDlg (self)
		self.list_view_dlg.addlines(self.parent.picPaths)
		self.list_view_dlg.ShowModal()
		
		event.Skip()
	
	def  OnCtrlClick (self, event):
		ctrl = event.GetEventObject()
		if self.ctrlOnFocus: self.ctrlOnFocus.SetSelection(0, 0)
		self.ctrlOnFocus = ctrl
		event.Skip()
	
	def SetPickedColor (self, X, Y): #color):
		"""
		Set value passed from Main UI
		"""
		#if self.ctrlOnFocus: self.ctrlOnFocus.SetValue(color)
		if not self.parent.imageLabel.GetLabel().startswith(u"(预览)"):
			img = self.parent.imageOpen(self.parent.getCurJpg()).convert("RGBA")
		else:
			img = self.parent.im_preview
		pixels = img.load()
		if self.ctrlOnFocus:  self.ctrlOnFocus.SetValue(str(pixels[X, Y]))

	def RefreshTitle (self):
		self.SetTitle(self.parent.getGuiTitle(u"图片特效"))
		im = self.parent.imageOpen(self.parent.picPaths[self.parent.currentPicture]).convert("RGBA")
		brightness_current = str(int(brightness(im)))
		self.ctrlCurBrightness.SetValue(brightness_current)
		self.m_spinCtrlMosaicSize.SetRange(2, min(im.size[0], im.size[1]))
		self.m_spinCtrlMosaicSize.SetValue(min(8, (min(im.size[0], im.size[1]))))
	
	def OnDel( self, event ):
		sel = self.m_checkList1.GetSelection()
		if sel != -1:
			self.m_checkList1.Delete(sel)
			if len(self.m_checkList1.Items) > 0:
				self.m_checkList1.SetSelection(len(self.m_checkList1.Items) - 1 )
		event.Skip()
		
	def OnDelAll( self, event ):
		self.m_checkList1.Clear()
		event.Skip()
	
	# Virtual event handlers, overide them in your derived class
	def OnBtnUp( self, event ):
		sel = self.m_checkList1.GetSelection()
		items = self.m_checkList1.Items
		if sel > 0: # selected not -1 And not zero
			self.moveUpDown(1)              
		event.Skip()
	def moveUpDown(self, row):
		sel = self.m_checkList1.GetSelection()
		sel_string = self.m_checkList1.GetString(sel)
		items = self.m_checkList1.Items         
		if sel != len(items) + row:
			self.m_checkList1.Delete(sel)
			self.m_checkList1.Insert(sel_string, sel - row)
			self.m_checkList1.SetSelection(sel - row)
	
	def OnBtnDown( self, event ):
		sel = self.m_checkList1.GetSelection()
		items = self.m_checkList1.Items
		if sel not in [ -1, len(items) - 1]:
			self.moveUpDown(-1)
		event.Skip()
	def noOpenSetting(self, isPressed):
		if isPressed and  self.settingCounts == 2:
			wx.MessageBox("抱歉！达到了设置面板数打开的最大限制", "小提醒", wx.OK | wx.ICON_INFORMATION)                  
			return True
		else:
			return False
	def OnSettingClick( self, event, togglePanel, tooltip ):                
		btn = event.GetEventObject()
		isPressed = btn.GetValue()
		if not self.noOpenSetting(isPressed):
			togglePanel(isPressed)
			if isPressed:
				btn.UnsetToolTip()
				self.settingCounts += 1
			else:
				btn.SetToolTipString(tooltip)
				self.settingCounts -= 1
		else:
			btn.SetValue(False)
		event.Skip()
		
	def OnRoundClick( self, event ):
		self.OnSettingClick(event, self.toggleRoundPanel, u'打开圆角设置')
		event.Skip()
		
	def toggleRoundPanel(self, isPressed):
		# 圆角效果框
		ctrl_list = [self.m_checkBoxDefault, self.m_staticTextRound, self.m_spinCtrlNum, \
		self.m_staticTextSize, self.staticRound ]
		self.toggleSettingPanel (ctrl_list, isPressed)

	def toggleSettingPanel(self, ctrl_list, isPressed):		
		for ctrl in ctrl_list: ctrl.Show(isPressed)
		self.Layout()
	
	def OnBackgroundClick( self, event ):
		self.OnSettingClick(event, self.toggleBackgroundPanel, BACKGROUND_TIP)
		event.Skip()
		
	def toggleBackgroundPanel (self, isPressed):
		# 背景框           
		ctrl_list = [self.m_radioBtnCkColor, self.m_bgColourPicker, self.m_radioBtnCkPic, self.m_textCtrlPath, \
		self.m_btnBrowse, self.m_staticTextHtxt, self.m_textCtrlHbox, self.m_staticTextVtxt, self.m_textCtrlVbox, \
		self.staticBackground, self.m_comboTextHPos, self.m_comboTextVPos, self.m_staticTextHPos, self.m_staticTextVPos, \
		self.m_methodText, self.m_comboMethod ]
		self.toggleSettingPanel (ctrl_list, isPressed)
	def OnMosaicClick( self, event ):
		self.OnSettingClick(event, self.toggleMosaicPanel, u'打开马赛克设置')
		event.Skip()
		
	def	toggleMosaicPanel(self, isPressed):
		#Mosaic
		ctrl_list = [self.staticMosaic, self.m_staticTextMosaicSize, self.m_spinCtrlMosaicSize, self.m_staticTextMosaicTip ]
		self.toggleSettingPanel (ctrl_list, isPressed)
		
	def OnMaskClick( self, event ):
		self.OnSettingClick(event, self.toggleMaskPanel, u'打开蒙版设置')
		event.Skip()
		
	def OnWaterMarkClick (self, event ):
		#self.OnSettingClick(event, self.toggleTxtDlg, u'打开水印设置')
		btn = event.GetEventObject()
		isPressed = btn.GetValue()

		if isPressed: btn.UnsetToolTip()
		else:	btn.SetToolTipString(u'打开水印设置')

		self.toggleTxtDlg(isPressed)
		event.Skip()
		
	def toggleTxtDlg (self, isPressed):
		if isPressed:
			if self.parent.txtDlg: self.parent.txtDlg.Show()
			else: self.doTxtDlg()
	

	def toggleMaskPanel(self, isPressed):
		#Mosaic
		ctrl_list = [self.staticMask, self.m_staticTextMask, self.m_textCtrlMaskPath, self.m_btnMaskBrowse, self.m_staticTextMaskBg, \
					 self.m_MaskBgColorPicker, self.ctrlMaskBgColor ]
		self.toggleSettingPanel (ctrl_list, isPressed)		
		
	def OnBlendClick (self, event ):
		self.OnSettingClick(event, self.toggleBlendPanel, u'打开混合设置')
		event.Skip()

	def OnSplitClick (self, event ):
		self.OnSettingClick(event, self.toggleSplitPanel, SPLIT_TIP)
		event.Skip()
		
	def OnSliceClick (self, event ):
		self.OnSettingClick(event, self.toggleSlicePanel, SLICE_TIP)
		event.Skip()
		
	def toggleSplitPanel(self, isPressed):
		#Mosaic
		ctrl_list = [self.staticSplit, self.m_choicePixelX , self.m_spinCtrlRow, self.m_choicePixelY, self.m_spinCtrlCol, \
					 self.m_staticLineColor, self.m_LineColourPicker ]
		self.toggleSettingPanel (ctrl_list, isPressed)
		
	def toggleSlicePanel(self, isPressed):
		#Mosaic
		ctrl_list = [self.staticSliceGone, self.m_checkBoxSliceStyle , self.m_staticSliceModeTip, self.m_staticSlice ]
		self.toggleSettingPanel (ctrl_list, isPressed)
		
	def toggleBlendPanel(self, isPressed):
		#Mosaic
		ctrl_list = [self.staticBlend, self.m_staticTextBlend, self.m_textCtrlImg2Path, self.m_btnBlendBrowse, self.m_staticTextAlpha, self.m_spinCtrlAlpha, \
					 self.m_staticTextPercent ]
		self.toggleSettingPanel (ctrl_list, isPressed)	
		
	def OnBorderClick(self, event):
		self.OnSettingClick(event, self.toggleBorderPanel, u'打开边框设置')
		event.Skip()
		
	def toggleBorderPanel (self, isPressed):
		# 边框
		ctrl_list = [self.staticBorder, self.m_staticTextBorder, self.m_textCtrlBorderBox, self.m_staticTextColor, \
		self.m_borderColourPicker, self.m_staticTextOpacity, self.m_sliderOpacity ]
		self.toggleSettingPanel (ctrl_list, isPressed)
		
	def OnShadowClick(self, event):
		self.OnSettingClick(event, self.toggleShadowPanel, u'打开阴影设置')
		event.Skip()

	def toggleShadowPanel(self, isPressed):
		#阴影
		ctrl_list = [self.m_staticHTextShadow, self.m_textCtrlShadowHBox, self.m_staticVTextShadow, self.m_textCtrlShadowVBox, self.staticShadow ]
		self.toggleSettingPanel (ctrl_list, isPressed)
		
	def OnRollClick(self, event):
		self.OnSettingClick(event, self.toggleRollPanel, u'打开滚动设置')
		event.Skip()

	def toggleRollPanel(self, isPressed):
		#滚动
		ctrl_list = [self.m_staticHTextRoll, self.m_textCtrlRollHBox, self.m_staticVTextRoll, self.m_textCtrlRollVBox, self.staticRoll ]
		self.toggleSettingPanel (ctrl_list, isPressed)
		
	def toggleShearPanel (self, isPressed):
		# 倾斜
		ctrl_list = [self.staticShear, self.m_staticTextXdegree, self.m_spinCtrlXdegree, self.m_staticTextYdegree, \
			     self.m_spinCtrlYdegree, self.m_staticShearBkColor, self.m_ShearColorPicker, self.ctrlShearBkColor ]
		self.toggleSettingPanel (ctrl_list, isPressed)
		
	def OnShearClick(self, event):
		self.OnSettingClick(event, self.toggleShearPanel, u'打开倾斜设置')
		event.Skip()
		
	def OnReflectionClick(self, event):
		self.OnSettingClick(event, self.toggleReflectionPanel, u'打开倒影设置')
		event.Skip()
	
	def toggleReflectionPanel (self, isPressed):
		ctrl_list = [self.staticReflection, self.m_staticTextDepth, self.m_textCtrlDepthBox, self.m_staticReflectionBgColor, \
		self.m_ReflectionBgColourPicker, self.m_staticReflectionOpacity, self.m_sliderReflectionOpacity ]
		self.toggleSettingPanel (ctrl_list, isPressed)	
		
	def OnEnhanceClick( self, event ):
		#图像增强
		self.OnSettingClick(event, self.toggleEnhancePanel, u'打开图像增强设置')
		event.Skip()
		
	def toggleEnhancePanel (self, isPressed):
		# 增强框
		ctrl_list = [self.staticEnhance, self.m_staticTextFactor, self.m_spinCtrlFactor, self.m_staticTextEnhance, self.m_EnhanceBox ]
		self.toggleSettingPanel (ctrl_list, isPressed)
		
	def OnFilterClick( self, event ):
		self.OnSettingClick(event, self.toggleFilterPanel, u'打开滤镜设置')
		event.Skip()
		
	def toggleFilterPanel (self, isPressed):
		# 滤镜
		for checkbox in self.m_FilterBoxList:
			checkbox.Show(isPressed)        
		self.staticFilter.Show(isPressed)
		self.Layout()
		
	def OnRotateClick( self, event ):
		self.OnSettingClick(event, self.toggleRotatePanel, u'打开旋转设置')
		event.Skip()
		
	def toggleRotatePanel (self, isPressed):
		# 旋转
		ctrl_list = [self.staticRotate, self.m_radioBtnFixed, self.m_choiceFixed, self.m_radioBtnAny, self.m_spinCtrlAny ]
		self.toggleSettingPanel (ctrl_list, isPressed)
		
	def OnMirrorClick( self, event ):
		self.OnSettingClick(event, self.toggleMirrorPanel, u'打开镜像翻转设置')
		event.Skip()
		
	def toggleMirrorPanel (self, isPressed):
		# 镜像翻转  
		self.staticMirror.Show(isPressed)
		self.m_staticTextMirror.Show(isPressed)
		self.m_MirrorBox.Show(isPressed)
		self.Layout()		
		
	def OnInvertClick( self, event ):
		self.OnSettingClick(event, self.toggleInvertPanel, u'打开底片设置')
		event.Skip()
		
	def toggleInvertPanel (self, isPressed):
		# 镜像翻转  
		self.staticInvert.Show(isPressed)
		self.m_staticTextInvert.Show(isPressed)
		self.m_spinCtrlInvert.Show(isPressed)
		self.Layout()
		
	def OnLightingClick( self, event ):
		self.OnSettingClick(event, self.toggleLightingPanel, u'打开光照设置')
		event.Skip()
		
	def toggleLightingPanel (self, isPressed):
		# 光照
		ctrl_list = [self.staticLighting, self.m_staticTextLightingPos, self.m_comboTextLightingPos, self.m_staticTextLighting, self.m_spinCtrlLighting ]
		self.toggleSettingPanel (ctrl_list, isPressed)
		
	def OnSketchClick( self, event ):
		self.OnSettingClick(event, self.toggleSketchPanel, u'打开素描设置')
		event.Skip()
		
	def toggleSketchPanel (self, isPressed):
		# 素描  
		self.staticSketch.Show(isPressed)
		self.m_staticTextSketch.Show(isPressed)
		self.m_spinCtrlSketch.Show(isPressed)
		self.Layout()
		
	def OnPapercutClick( self, event ):
		self.OnSettingClick(event, self.togglePapercutPanel, u'打开剪纸设置')
		event.Skip()
		
	def togglePapercutPanel (self, isPressed):
		# 剪纸
		ctrl_list = [self.staticPapercut, self.m_staticPapercutBgColor, self.m_PapercutBgColourPicker, self.m_staticPapercutFgColor, \
		self.m_PapercutFgColourPicker, self.m_staticTextPapercut, self.m_spinCtrlPapercut ]
		self.toggleSettingPanel (ctrl_list, isPressed)
		
	def OnPuzzleClick( self, event ):
		self.OnSettingClick(event, self.togglePuzzlePanel, PUZZLE_TIP)
		event.Skip()
		
	def togglePuzzlePanel (self, isPressed):
		# 拼图
		ctrl_list = [self.staticPuzzle, self.m_staticTextQtyX, self.m_staticTextQtyY, self.m_spinCtrlQtyX, self.m_spinCtrlQtyY, self.m_buttonListView, \
		self.m_PuzzleSrcBox, self.m_staticPuzzleBgColor, self.m_PuzzleBgColourPicker, self.m_PuzzleOrderBox, self.m_spinCtrlGap, self.m_staticTextGap, self.m_checkBoxResize ]		
		self.toggleSettingPanel (ctrl_list, isPressed)
		
	def OnTearClick( self, event ):               
		self.OnSettingClick(event, self.toggleTearPanel, TEAR_TIP)
		event.Skip()
		
	def toggleTearPanel (self, isPressed):
		# 剪纸
		ctrl_list = [self.staticTear, self.m_staticTearDirection, self.m_TearPosBox, self.m_staticTextTear, self.m_spinCtrlTear, self.m_checkBoxIsCut ]
		self.toggleSettingPanel (ctrl_list, isPressed)
		
	def OnMixClick( self, event ):               
		self.OnSettingClick(event, self.toggleMixPanel, u'打开混色设置')
		event.Skip()
		
	def OnReplaceClick( self, event ):
		self.OnSettingClick(event, self.toggleReplacePanel, REPLACE_TIP)
		event.Skip()
		
	def toggleReplacePanel (self, isPressed):
		# 颜色替换
		ctrl_list = [self.staticReplace, self.m_checkBoxReplaceStyle, self.m_staticTextModeTip, self.m_staticOldColor, self.m_ColorCompareBox, self.m_OldColourPicker, self.ctrlOldColor, \
		self.m_staticNewColor, self.m_NewColourPicker, self.ctrlNewColor, self.ctrlOldColor ]
		self.toggleSettingPanel (ctrl_list, isPressed)
		ctrl_list_range = [ self.m_staticTextOldMax, self.m_OldColourMaxPicker, self.ctrlOldColorMax]

		flag = self.m_ColorCompareBox.GetValue()
		isRange = flag == u'从'
		self.toggleSettingPanel (ctrl_list_range, isPressed and isRange)
		
	def OnColorComboChanged (self, event):
		self.toggleReplacePanel (True)
	
	def OnReplaceModeChanged(self, event):
		isFill = (self.m_checkBoxReplaceStyle.Selection == 1)
		ctrl_list = [self.m_staticOldColor, self.m_OldColourPicker, self.m_ColorCompareBox, self.ctrlOldColor]
		[ oldCtrls.Enable(not isFill) for oldCtrls in ctrl_list ]
		ctrl_list_range = [ self.m_staticTextOldMax, self.m_OldColourMaxPicker, self.ctrlOldColorMax]
		
		flag = self.m_ColorCompareBox.GetValue()
		isRange = flag == u'从'
		self.toggleSettingPanel (ctrl_list_range, isRange)
		
	def toggleMixPanel (self, isPressed):
		# 混色
		ctrl_list = [self.staticMix, self.m_staticTextMixFactor, self.m_spinCtrlMixFactor, \
		self.m_staticMixColor, self.m_MixColourPicker, self.ctrlColor ]
		self.toggleSettingPanel (ctrl_list, isPressed)	
		
	def OnFadeClick( self, event ):
		self.OnSettingClick(event, self.toggleFadePanel, u'打开渐变设置')
		event.Skip()
		
	def toggleFadePanel (self, isPressed):
		# 渐变
		ctrl_list = [self.staticFade, self.m_staticTextFadePos, self.m_spinCtrlFadePos, self.m_staticFadeMode, \
		self.m_FadeModeBox, self.m_staticFadeColor, self.m_FadeColourPicker ]
		self.toggleSettingPanel (ctrl_list, isPressed)
	
	def OnFocusClick( self, event ):
		# 聚光
		self.OnSettingClick(event, self.toggleFocusPanel, FOCUS_TIP )
		event.Skip()
	def OnAutoBrightnessClick (self, event):
		# 自动亮度
		self.OnSettingClick(event, self.toggleAutoBrightnessPanel, u'打开自动亮度设置\r\n调节图片到指定的亮度' )
		event.Skip()
		
	def toggleFocusPanel (self, isPressed):
		# 聚光
		ctrl_list = [self.staticFocus, self.m_staticTextRadiusIn, self.m_spinCtrlRadiusIn, self.m_staticTextRadiusOut, \
		self.m_spinCtrlRadiusOut, self.m_staticFocusEdgeColor, self.m_FocusEdgeColourPicker, self.m_checkBoxFocusEdge ]
		self.toggleSettingPanel (ctrl_list, isPressed)
		
	def toggleAutoBrightnessPanel (self, isPressed):
		#自动亮度
		ctrl_list = [self.staticAutoBrightness, self.m_staticCurBrightness, self.ctrlCurBrightness, \
					 self.m_staticNewBrightness, self.m_spinCtrlNewBrightness ]
		self.toggleSettingPanel (ctrl_list, isPressed)
		
	def OnSwirlClick( self, event ):
		self.OnSettingClick(event, self.toggleSwirlPanel, u'打开漩涡设置')
		event.Skip()
		
	def toggleSwirlPanel (self, isPressed):
		# 漩涡 
		self.staticSwirl.Show(isPressed)
		self.m_staticTextSwirl.Show(isPressed)
		self.m_sliderSwirlOpacity.Show(isPressed)
		self.Layout()
		
	def OnDeYellowClick( self, event ):
		self.OnSettingClick(event, self.toggleDeYellowPanel, u'打开新照片设置')
		event.Skip()
		
	def toggleDeYellowPanel (self, isPressed):
		# 新照片 
		self.staticDeYellow.Show(isPressed)
		self.m_radioBoxDeYellow_1.Show(isPressed)
		self.m_radioBoxDeYellow_2.Show(isPressed)
		self.Layout()
		
	def OnPlus( self, event ):
		for btn in self.taskListBtns:
			if btn.GetValue():
				self.m_checkList1.Append(btn.Label)
		event.Skip()
	
	def OnBtnFixedClick(self, event):
		self.m_choiceFixed.Enable(True)
		self.m_spinCtrlAny.Enable(False)
		event.Skip()
		
	def OnBtnAnyClick(self, event):
		self.m_spinCtrlAny.Enable(True)
		self.m_choiceFixed.Enable(False)
		event.Skip()
		
	def toggleCheckBox(self, button):               
		self.m_spinCtrlNum.Enable( not button.GetValue() )
		if button.GetValue(): self.m_spinCtrlNum.SetValue(5)
		
	def toggleRadioBox(self):
		isColorChecked = self.m_radioBtnCkColor.GetValue()
		self.m_bgColourPicker.Enable(isColorChecked)            
		#self.m_textCtrlPath.Enable(not isColorChecked)
		self.m_btnBrowse.Enable(not isColorChecked)
		self.m_methodText.Enable(not isColorChecked)
		self.m_comboMethod.Enable(not isColorChecked)
		self.offsetGroupStatus()
		
	def OnCornerFoldClick( self, event ):
		self.OnSettingClick(event, self.toggleCornerFoldPanel, u'打开折角设置\r\n注意：只有PNG和GIF才有透明效果')
		event.Skip()
		
	def toggleCornerFoldPanel (self, isPressed):
		# 新照片
		ctrl_list = [self.staticCornerFold, self.m_staticTextEdge, self.m_spinCtrlEdge, self.m_staticTextWhitePercent, \
		self.m_spinCtrlWhitePercent, self.m_staticFoldPos, self.m_FoldPosBox ]
		self.toggleSettingPanel (ctrl_list, isPressed)		

	def OnCheckDefault( self, event ):
		btn = event.GetEventObject()            
		self.toggleCheckBox(self.m_checkBoxDefault)             
		event.Skip()
		
	def OnCheckPic(self, event):
		self.toggleRadioBox()
		event.Skip()
		
	def OnCheckColor(self, event):
		self.toggleRadioBox()
		event.Skip()            
	
	def KeyDown(self, event):
		curSel = event.GetSelection()
		event.Skip()
		
	def OnBtnBrowse( self, event ):			
		fd = wx.FileDialog(self, u'请选择一张背景图片', self.m_textCtrlPath.GetValue(), wx.EmptyString, wildcard, wx.OPEN)
		if fd.ShowModal() == wx.ID_OK:
			self.pic = fd.GetPath()
			self.m_textCtrlPath.SetValue(self.pic)
			self.m_textCtrlPath.SetToolTip(wx.ToolTip(self.pic))
		fd.Destroy()
		event.Skip()
		
	def OnBtnMaskBrowse( self, event ):
		fd = wx.FileDialog(self, u'请选择一张蒙版图片', self.m_textCtrlPath.GetValue(), wx.EmptyString, wildcard, wx.OPEN)
		if fd.ShowModal() == wx.ID_OK:			
			try:
				path = fd.GetPath()
				self.mask = Image.open (path)
				self.m_textCtrlMaskPath.SetValue(path)
				self.m_textCtrlMaskPath.SetToolTipString (path)
				self.parent.mask_path = path	
			except:
				wx.MessageBox("抱歉！打开蒙版时出错，请再试。", "小提醒", wx.OK | wx.ICON_INFORMATION) 
		fd.Destroy()
		event.Skip()
		
	def OnBtnBlendBrowse( self, event ):			
		fd = wx.FileDialog(self, u'请选择一张图片', wx.EmptyString, wx.EmptyString, wildcard, wx.OPEN)
		if fd.ShowModal() == wx.ID_OK:
			try:
				path = fd.GetPath()
				self.img2 = Image.open (path)
				self.m_textCtrlImg2Path.SetValue(path)
				self.m_textCtrlImg2Path.SetToolTipString(path)
			except:
				wx.MessageBox("抱歉！打开图片时出错，请再试。", "小提醒", wx.OK | wx.ICON_INFORMATION)
		fd.Destroy()
		event.Skip()
	
	def OnPreview( self, event ):
		# get current picture to display
		img = self.parent.getCurJpg()
		self.m_preview.Enable(False)
		wx.BeginBusyCursor()	
		self.DoEffects(img)
		wx.EndBusyCursor()
		self.m_preview.Enable(True)
		event.Skip()
		
	def OnReset( self, event ):
		self.parent.imgReload()
		self.parent.rubber.crop = None #清除鼠标选定区域
		event.Skip()
		
	def OnClose( self, event ):
		self.Show(False)
		event.Skip()
	
	def DoEffects( self, filename, outfilename = '', istemp = True ):
		# check if single mode
		if self.parent.singleMode and self.parent.im_preview:			
			self.cur_im = self.parent.im_preview			
		else: 	self.cur_im = Image.open(filename)
		
		# define current image
		self.cur_img = filename
		
		#
		btnPressedList = []
		[btnPressedList.append(btn) for btn in self.taskListBtns if btn.GetValue() ]		
			
		# 如果用户忘记添加了，帮用户加上
		for btn in btnPressedList:
			if btn.Label not in self.m_checkList1.Items:
				self.m_checkList1.Append(btn.Label)
		#[self.m_checkList1.Append(btn.Label) for btn in btnPressedList if (btn.Label not in self.m_checkList1.Items)]

		# move image split to end if available
		index = self.m_checkList1.FindString(u"图片分割")
		if index != wx.NOT_FOUND and index != self.m_checkList1.GetCount() - 1:
			self.m_checkList1.Delete(index)
			self.m_checkList1.Append(u"图片分割")

		self.out_dir = outfilename if not istemp else None
			
		tasks = self.m_checkList1.Items
		try:
			if tasks:
				for task in tasks:
					self.taskMapper[task]()
				if istemp:	
					self.parent.imgPreview(self.cur_im, '.PNG') #ext)
				elif self.cur_im:
					ext = os.path.splitext(filename)[1]
					if ext.upper() in ['.JPG', '.JPEG']:
						self.cur_im.save(outfilename, 'JPEG', quality = 95, optimize = True, dpi = self.parent.current_dpi)
					else: self.cur_im.save(outfilename, dpi = self.parent.current_dpi)
		except: raise

	def MakeRound (self):
		r = self.m_spinCtrlNum.GetValue()
		if not self.m_checkBoxDefault.GetValue():
			self.cur_im = round_image(self.cur_im, radius = self.m_spinCtrlNum.GetValue())
		else:
			self.cur_im = round_image(self.cur_im) # use default 5
		#return img
	def MakeBackground (self):      
		method = self.m_comboMethod.GetValue() #u'偏移' #'Scale' #'Tile'
		if self.m_radioBtnCkColor.GetValue(): choice_index = 0
		else: choice_index = 1
		
		mark = self.pic
		bgColor = self.m_bgColourPicker.GetColour()
		h_offset, v_offset = int(self.m_textCtrlHbox.GetValue()), int(self.m_textCtrlVbox.GetValue())
		self.cur_im = background(self.cur_im, FILL_CHOICES[choice_index], mark, bgColor, horizontal_offset = h_offset, vertical_offset = v_offset, method = method,
				  horizontal_justification=self.m_comboTextHPos.GetValue(),
				  vertical_justification=self.m_comboTextVPos.GetValue())
	def MakeShadow (self):
		h_offset, v_offset = int(self.m_textCtrlShadowHBox.GetValue()), int(self.m_textCtrlShadowVBox.GetValue())
		self.cur_im = drop_shadow(self.cur_im, horizontal_offset = h_offset, vertical_offset = v_offset)
	
	def MakeRoll (self):
		h_offset, v_offset = int(self.m_textCtrlRollHBox.GetValue()), int(self.m_textCtrlRollVBox.GetValue())
		self.cur_im = self.cur_im.offset(h_offset, v_offset)
		
	def onMethodChanged(self, event):
		self.offsetGroupStatus()
		event.Skip()            
		
	def offsetGroupStatus(self):
		isOffsetMethod = (self.m_radioBtnCkPic.GetValue() and self.m_comboMethod.GetValue() == u'偏移')
		self.m_staticTextHtxt.Enable(isOffsetMethod)
		self.m_textCtrlHbox.Enable(isOffsetMethod)
		self.m_staticTextVtxt.Enable(isOffsetMethod)
		self.m_textCtrlVbox.Enable(isOffsetMethod)
		self.m_comboTextHPos.Enable(isOffsetMethod)
		self.m_comboTextVPos.Enable(isOffsetMethod)
		self.m_staticTextHPos.Enable(isOffsetMethod)
		self.m_staticTextVPos.Enable(isOffsetMethod)
	def MakeBorder(self):
		width = int(self.m_textCtrlBorderBox.GetValue())  # may throw error!
		opacity = self.m_sliderOpacity.GetValue()
		borderColor = self.m_borderColourPicker.GetColour()
		self.cur_im = border(self.cur_im, border_width = width, color= borderColor, opacity = opacity)
	def MakeReflection (self):
		depth = int(self.m_textCtrlDepthBox.GetValue())
		opacity = self.m_sliderReflectionOpacity.GetValue()
		reflectionBgColor = self.m_ReflectionBgColourPicker.GetColour()
		self.cur_im = reflect(self.cur_im, depth, 90, reflectionBgColor, opacity, 'BICUBIC')

	def MakeGrayscale(self):
		self.cur_im = self.cur_im.convert('L')
		
	def MakeEnhance(self):
		modeMapper = {u'锐化':ImageEnhance.Sharpness, u'色调':ImageEnhance.Color, u'亮度':ImageEnhance.Brightness, u'对比度':ImageEnhance.Contrast}
		factor = 1.0 + self.m_spinCtrlFactor.GetValue() / 70.0  # allow range from 0 to 2.9
		mode = self.m_EnhanceBox.GetValue()
		
		enhancer = modeMapper[mode](self.cur_im)
		self.cur_im = enhancer.enhance(factor)
	
	def MakeFilter(self):
		filtermode = [ImageFilter.BLUR, ImageFilter.GaussianBlur, ImageFilter.EMBOSS, ImageFilter.CONTOUR,
				  ImageFilter.EDGE_ENHANCE, ImageFilter.SMOOTH, ImageFilter.MedianFilter, ImageFilter.SHARPEN,
				  ImageFilter.DETAIL]
		for checkbox in self.m_FilterBoxList:           
			if checkbox.GetValue():
				index = [i for i in range(len(self.m_FilterBoxList)) if self.m_FilterBoxList[i] == checkbox]
				if  self.cur_im.mode != '1':
					self.cur_im = self.cur_im.convert("RGBA")
					self.cur_im = self.cur_im.filter(filtermode[index.pop()])
				
	def MakeBlkWht(self):
		self.cur_im = self.cur_im.convert('1')
		
	def MakeRotate(self):
		# First check if user selected fixed angle?
		rotate_map = {0:Image.ROTATE_270, 1:Image.ROTATE_180, 2:Image.ROTATE_90}
		select = self.m_choiceFixed.Selection
		if self.m_radioBtnFixed.GetValue():
			self.cur_im = self.cur_im.transpose(rotate_map[select])
		else:
			# make it clockwise for positive angle
			angle = -int(self.m_spinCtrlAny.GetValue()) 
			self.cur_im = self.cur_im.rotate(angle, expand = 1)
		
	def MakeMirror(self):
		direction = self.m_MirrorBox.GetValue()
		self.cur_im = tile(self.cur_im, direction)
		
	def MakeInvert(self):
		amount = self.m_spinCtrlInvert.GetValue() + 50 # -50->0, 50 ->100
		self.cur_im = invert(self.cur_im, amount)
		
	def MakeMolten(self):
		self.cur_im = molten(self.cur_im)
	
	def MakeLighting(self):
		W, H = self.cur_im.size
		
		self.m_PosList = [u'左上', u'左中', u'左下', u'中上', u'正中', u'中下', u'右上', u'右中',u'右下']
		self.m_PosList_Map = {u'左上':(W/4,H/4), u'左中':(W/4, H/2), u'左下':(W/4, (H*3)/4),
				u'中上':(W/2, H/4), u'正中':(W/2,H/2), u'中下': (W/2, (H*3)/4),
				u'右上':((W*3)/4, H/4), u'右中':((W*3)/4, H/2),u'右下':((W*3)/4, (H*3)/4)}
		pos = self.m_comboTextLightingPos.GetValue()
		power = self.m_spinCtrlLighting.GetValue()
		self.cur_im = lighting(self.cur_im, power, self.m_PosList_Map[pos])
		
	def MakeSketch(self):
		threshold = self.m_spinCtrlSketch.GetValue()
		self.cur_im = sketch(self.cur_im, threshold)
		
	def MakeIce(self):
		self.cur_im = ice(self.cur_im)
		
	def ColorWithAlpha(self, color, a):
		r,g,b = color
		return (r,g,b,a)
		
	def MakePapercut(self):
		threshold = self.m_spinCtrlPapercut.GetValue()
		bg_color = self.m_PapercutBgColourPicker.GetColour() #(255, 255, 255, 0)
		fg_color = self.m_PapercutFgColourPicker.GetColour() #(255, 0, 0, 255)
		self.cur_im = paper_cut(self.cur_im, threshold, self.ColorWithAlpha(bg_color,0), self.ColorWithAlpha(fg_color, 255))

	def MakeDeYellow(self):
		if self.m_radioBoxDeYellow_1.GetValue(): method = 0
		else: method = 1
		self.cur_im = deYellow(self.cur_im, method)
		
	def MakeTan(self):
		self.cur_im = tan(self.cur_im)
		
	def MakeSwirl(self):
		degree = self.m_sliderSwirlOpacity.GetValue()
		self.cur_im = swirl(self.cur_im, degree)
		
	def MakeSpherize(self):
		self.cur_im = spherize(self.cur_im)
		
	def MakePuzzle(self):
		#print "start puzzle"
		if self.m_PuzzleSrcBox.GetValue() == self.m_PuzzleSrcModeList[0]:		
			im_list = [ self.cur_im.convert("RGBA") ]
		else:
			im_list = [ Image.open(i).convert("RGBA") for i in self.parent.picPaths ]

		x_qty = self.m_spinCtrlQtyX.GetValue()
		y_qty = self.m_spinCtrlQtyY.GetValue()
		is_column = self.m_PuzzleOrderBox.GetValue() == u'按列'
		gap = self.m_spinCtrlGap.GetValue()
		allow_resize = self.m_checkBoxResize.GetValue()
		self.cur_im = ImgSalon(x_qty, y_qty, im_list, self.ColorWithAlpha(self.m_PuzzleBgColourPicker.GetColour(), 255), is_column, gap, allow_resize)
	
	def MakeFocus (self):
		edge_color = self.ColorWithAlpha (self.m_FocusEdgeColourPicker.GetColour(), 255)
		radius = min(self.cur_im.size[0], self.cur_im.size[1]) / 2
		radius_in = radius * self.m_spinCtrlRadiusIn.GetValue() /100 
		radius_out = radius * self.m_spinCtrlRadiusOut.GetValue() /100
		edge_transparent = self.m_checkBoxFocusEdge.IsChecked()
		self.cur_im = edge_blur(edge_color, self.cur_im, radius_in, radius_out, edge_transparent)
		
	def MakeCornerFold (self):
		edge = self.m_spinCtrlEdge.GetValue()
		white_percent = self.m_spinCtrlWhitePercent.GetValue()
		pos = self.m_FoldPosBox.GetValue()
		self.cur_im = EdgeFold(self.cur_im, edge, white_percent, pos)
		
	def MakeTear (self):
		direction = self.m_TearPosBox.GetValue()
		pos = self.m_spinCtrlTear.GetValue()
		isCut = self.m_checkBoxIsCut.GetValue()
		self.cur_im = Tear(self.cur_im, pos, direction, isCut)
		
	def MakeFade (self):
		pos = self.m_spinCtrlFadePos.GetValue()
		mode = self.m_FadeModeBox.GetValue()
		color = self.ColorWithAlpha (self.m_FadeColourPicker.GetColour(), 255)
		self.cur_im = Fade(self.cur_im, pos, mode, color)
	def MakeMix (self):
		factor = self.m_spinCtrlMixFactor.GetValue()
		color = self.getColor(self.ctrlColor)
		self.cur_im = MixColor(self.cur_im, factor, color)
		
	def AddMask (self):
		if self.mask:
			bg_color = self.getColor(self.ctrlMaskBgColor)
			self.cur_im = AddMask(self.cur_im, self.mask, bg_color)
			
	def MakeBlend (self):
		if self.img2:
			alpha = '%.2f' %  (int(self.m_spinCtrlAlpha.GetValue()) /100.0)
			self.cur_im = blend (self.cur_im, self.img2, float(alpha))
			
	def MakeSplit (self):
		rows, cols = self.m_spinCtrlRow.GetValue(), self.m_spinCtrlCol.GetValue()
		isPx, isPy = self.m_choicePixelX.GetSelection() == 1, self.m_choicePixelY.GetSelection() == 1
		w, h = self.cur_im.size
		
		# check if valid values
		if rows > w: rows = w
		if cols > h: cols = h
		
		img = self.parent.getCurJpg()
		line_color = self.m_LineColourPicker.GetColour().Get(includeAlpha=True)

		out_dir = os.path.splitext(self.out_dir)[0] if self.out_dir else None
		
		self.cur_im = split (self.cur_im, rows, cols, line_color, isPx, isPy, out_dir )
		
	def SliceGone (self):
		horizontal = self.m_checkBoxSliceStyle.GetValue() == u"左右"
		if self.parent.rubber.crop:
			x1,y1,x2,y2 = self.parent.rubber.crop
			if not horizontal:
				self.cur_im = slice_gone(self.cur_im, y1, y2, False)
			else: 
				self.cur_im = slice_gone(self.cur_im, x1, x2, True)
			
	def MakeWaterMark (self):
		#img = self.parent.getCurJpg()
		img = self.cur_img
		self.cur_im = self.parent.txtDlg.DoWaterMark(img, self.cur_im)
		
	def OnMixColorChanged (self, event):
		self.colorPicker2Ctrl(self.m_MixColourPicker, self.ctrlColor)
		event.Skip()
		
	def OnMaskBgColorChanged (self, event):
		self.colorPicker2Ctrl(self.m_MaskBgColorPicker, self.ctrlMaskBgColor)
		event.Skip()
		
	def OnMaskBgTxtChanged (self, event):
		self.ctrl2ColorPicker(self.ctrlMaskBgColor, self.m_MaskBgColorPicker)
		event.Skip()
		
	def OnMixTxtChanged (self, event):
		self.ctrl2ColorPicker(self.ctrlColor, self.m_MixColourPicker)
		event.Skip()
	
	def OnOldTxtChanged (self, event):
		self.ctrl2ColorPicker(self.ctrlOldColor, self.m_OldColourPicker)
		event.Skip()

	def OnOldTxtMaxChanged (self, event):
		self.ctrl2ColorPicker(self.ctrlOldColorMax, self.m_OldColourMaxPicker)
		event.Skip()
		
	def OnNewTxtChanged (self, event):
		self.ctrl2ColorPicker(self.ctrlNewColor, self.m_NewColourPicker)
		event.Skip()
		
	def OnOldColorChanged (self, event):
		self.colorPicker2Ctrl(self.m_OldColourPicker, self.ctrlOldColor)
		event.Skip()
		
	def OnOldColorMaxChanged (self, event):
		self.colorPicker2Ctrl(self.m_OldColourMaxPicker, self.ctrlOldColorMax)
		event.Skip()
		
	def OnNewColorChanged (self, event):
		self.colorPicker2Ctrl(self.m_NewColourPicker, self.ctrlNewColor)
		event.Skip()
	def OnShearTxtChanged (self, event):
		self.ctrl2ColorPicker(self.ctrlShearBkColor, self.m_ShearColorPicker)
		event.Skip()
		
	def OnShearColorChanged (self, event):
		self.colorPicker2Ctrl(self.m_ShearColorPicker, self.ctrlShearBkColor)
		event.Skip()
		
	def colorPicker2Ctrl (self, colorPicker, txtCtrl):
		r, g, b= colorPicker.GetColour()
		color = r, g, b, 255
		txtCtrl.SetValue(str(color))
	
	def ctrl2ColorPicker (self, txtCtrl, colorPicker):
		color = txtCtrl.GetValue()
		try:
			if '#' not in color: color = eval(color)
			colorPicker.SetColour(color)
			colorPicker.Refresh()
		except: pass
	def getColor(self, txtCtrl):
		color_str = txtCtrl.GetValue()
		if '#' not in color_str: color = eval(color_str)
		else:
			color = wx.Colour()
			color.SetFromString(color_str)
			color = color.Get(True)
		return color

	def MakeReplace (self):		
		color_old = self.getColor(self.ctrlOldColor)
		color_old_max = self.getColor (self.ctrlOldColorMax)
		color_new = self.getColor(self.ctrlNewColor)
		flag = self.m_ColorCompareBox.GetValue()
		w, h = self.cur_im.size
		im_array = np.array(self.cur_im.convert("RGBA"))
		if self.parent.rubber.crop:
			x1,y1,x2,y2 = self.parent.rubber.crop
			region_array = im_array[y1:y2, x1:x2]
			if self.m_checkBoxReplaceStyle.Selection == 0:	
				region_array_new = Replace(region_array, color_old, color_new, flag, color_old_max)								
			else:				
				region = newPil(x2-x1, y2-y1, fill = color_new)				
				region_array_new = np.array(region).astype(np.uint8)			
	
			im_array[ y1:y2, x1:x2] = region_array_new			
			self.cur_im = Image.fromarray(im_array)			
		else:
			if self.m_checkBoxReplaceStyle.Selection == 0:				
				self.cur_im = Image.fromarray(Replace(im_array, color_old, color_new, flag, color_old_max))
			else: # create a numpy image with color_new
				self.cur_im = newPil(w,h,color_new)
		
	def MakeAutoBrightness (self):
		new_brightness = self.m_spinCtrlNewBrightness.GetValue()
		self.cur_im = equalize(self.cur_im, new_brightness )
		
	def MakeShear (self):
		x_degree = self.m_spinCtrlXdegree.GetValue()
		y_degree = self.m_spinCtrlYdegree.GetValue()
		bk_color = self.getColor(self.ctrlShearBkColor)
		self.cur_im = Shear(self.cur_im, x_degree, y_degree, bk_color)
	
	def MakeMosaic (self):
		mosaic_size = self.m_spinCtrlMosaicSize.GetValue()
		if self.parent.rubber.crop:
			x0, y0, x1, y1 = self.parent.rubber.crop
		else:
			x0, y0, x1, y1 = 0, 0, self.cur_im.size[0], self.cur_im.size[1]
		self.cur_im = mosaic(self.cur_im, x0, y0, x1, y1, mosaic_size)		
		
	#---------------------------------------------------------------------                
	def doTxtDlg (self):
		"""
		Start Water Mark GUI
		"""
		pub.sendMessage("set status", msg = u"小提示：使用图片水印功能，您可以批量添加自己的印章呵。")
		# only popup font dlg after jpg is loaded
		if not self.parent.txtDlg:
			self.parent.txtDlg = MyTextDialog(self.parent)
			self.parent.setFontDlgPos(self.parent.txtDlg)                                
		else:
			self.parent.setFontDlgPos(self.parent.txtDlg)
			# get saved pin state
			self.parent.enablePin = (self.parent.txtDlg.textRepeatCtrl.GetValue() == u'一次 -> 按鼠标指定位置')                
##################################################################
class MyTextDialog(wx.Dialog):
        """"""
        #-------------------------------------------------------------
        def __init__(self, parent):                
                """界面初始化方法"""

                self.parent = parent
                
                #基本坐标
                self.Base = 40 # old = 20
                #水印字
                self.text = self.parent.water_text
                self.txtEnabled = True                
               
                #系统字体集字典
                self.systemFontDict = self._GetSystemFontDict()
                
                #字体样式
                self.fontStyle = None
                
                #字体文件
                self.fontFile = "SIMSUN.TTC"
                
                #字体路径
                self.fontSrc = os.path.join(os.environ['windir'], "fonts") ##"C:\\WINDOWS\\Fonts\\"
                #字体大小
                self.fontSize = 20
                #字体颜色,默认红色
                self.fontColour = (0,0,0) # 
                #透明度
                self.trans = self.parent.text_trans
                #取最终颜色 = 颜色 + 透明度
                #self._GetFinalColourWithAlpha()
                #水印位置,默认为右下
                self.fontPosition = 9 #the default
                
                # Do not initialize your font here; Get the font chosen by the user
                self.curFont =  wx.Font(self.fontSize, 70, 90, 90, False, wx.EmptyString )
                self.fName = unicode("宋体", "cp936")
                self.LABEL_FONT = wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL, False,'Tahoma')

                wx.Dialog.__init__(self, parent, title='添加文字或图片水印', size=(600, 820), style = wx.DEFAULT_DIALOG_STYLE |wx.MINIMIZE_BOX )
                self.SetIcon(self.parent.midi)                
                
                self.sizer = wx.BoxSizer(wx.VERTICAL)
                self.sizer.Add(wx.StaticLine(self, wx.ID_ANY), 0, wx.ALL|wx.EXPAND, 0)
                #self.watermarkSizer = wx.BoxSizer(wx.HORIZONTAL)
                
                #水印文字
                staticChoice = wx.StaticBox (self, wx.ID_ANY, u"水印来源")
                sizerChoice = wx.StaticBoxSizer(staticChoice, wx.HORIZONTAL)
                
                fgSizerSrc = wx.FlexGridSizer( 2, 2, 0, 50 )
                fgSizerSrc.SetFlexibleDirection(wx.BOTH)
                fgSizerSrc.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
                
                bSizerPicName = wx.BoxSizer(wx.VERTICAL)
                self.m_radioPicName = wx.RadioButton( self, wx.ID_ANY, u"图片名称", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP)
                bSizerPicName.Add( self.m_radioPicName, 0, wx.ALL, 5 )
                fgSizerSrc.Add( bSizerPicName, 1, wx.EXPAND, 5 )
                self.m_radioPicName.Bind(wx.EVT_RADIOBUTTON, self.OnRadioBtns)
                
                # 图片水印选项  
                bSizerPic = wx.BoxSizer( wx.HORIZONTAL )
                self.m_radioPic = wx.RadioButton( self, wx.ID_ANY, u"图片水印", wx.DefaultPosition, wx.DefaultSize, 0 )
                bSizerPic.Add( self.m_radioPic, 0, wx.ALL, 5 )
                self.m_radioPic.Bind(wx.EVT_RADIOBUTTON, self.OnRadioBtns)
                          
                self.m_textCtrlPath = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, (300, -1), wx.TE_READONLY )
                bSizerPic.Add( self.m_textCtrlPath, 0, wx.ALL, 5 )
                self.pic = None
                self.m_btnBrowse = wx.Button( self, wx.ID_ANY, u"...", wx.DefaultPosition, (-1, 21), wx.BU_EXACTFIT )
                self.m_btnBrowse.Bind(wx.EVT_BUTTON, self.onPicBrowse)
                bSizerPic.Add( self.m_btnBrowse, 0, wx.ALL, 5 )
                fgSizerSrc.Add( bSizerPic, 1, wx.ALL, 0 )
                
                bSizerUniText = wx.BoxSizer(wx.VERTICAL)
                self.m_radioTxt = wx.RadioButton( self, wx.ID_ANY, u"文字水印", wx.DefaultPosition, wx.DefaultSize, 0 )                
                self.m_radioTxt.Bind(wx.EVT_RADIOBUTTON, self.OnRadioBtns)
                bSizerUniText.Add( self.m_radioTxt, 0, wx.ALL, 5 )
                fgSizerSrc.Add( bSizerUniText, 1, wx.EXPAND, 5 )
                
                #文字水印列表
                bSizerFileList = wx.BoxSizer( wx.HORIZONTAL )
                self.m_radioFileList = wx.RadioButton( self, wx.ID_ANY, u"载入文件", wx.DefaultPosition, wx.DefaultSize, 0 )
                bSizerFileList.Add( self.m_radioFileList, 0, wx.ALL, 5 )
                self.m_radioFileList.Bind(wx.EVT_RADIOBUTTON, self.OnRadioBtns)
                
                self.m_fileListCtrlPath = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, (300, -1), wx.TE_READONLY )
                bSizerFileList.Add( self.m_fileListCtrlPath, 0, wx.ALL, 5 )
                
                self.listFile = None
                self.excel_pic_names = None
                
                self.m_btnBrowseFileList = wx.Button( self, wx.ID_ANY, u"...", wx.DefaultPosition, (-1, 21), wx.BU_EXACTFIT )
                self.m_btnBrowseFileList.Bind(wx.EVT_BUTTON, self.onFileListBrowse)
                bSizerFileList.Add( self.m_btnBrowseFileList, 0, wx.ALL, 5 )
                fgSizerSrc.Add( bSizerFileList, 1, wx.EXPAND, 0 )
                
                sizerChoice.Add(fgSizerSrc, 0, wx.EXPAND, 5 )
                self.sizer.Add(sizerChoice, 0, wx.LEFT | wx.TOP | wx.RIGHT | wx.EXPAND, 13)
                self.m_radioTxt.SetValue(True)
                
                ##
                self.sizer.AddSpacer( ( -1, 5))
                ###
                self.staticTxtMark = wx.StaticBox( self, wx.ID_ANY, u"文字水印" )
                self.bSizerSrcWaterMark = wx.StaticBoxSizer( self.staticTxtMark, wx.VERTICAL )
                
                self.waterText = wx.TextCtrl(id=wx.ID_ANY, name='waterText',
                      parent=self, pos=wx.Point(88, 64), size=wx.Size(556, 300),
                      style=wx.TE_MULTILINE,
                      value=self.text)
                self.waterText.SetMaxLength(400)
                self.waterText.SetToolTipString("最多200个汉字")
                self.waterText.Bind(wx.EVT_TEXT, self.OnWaterText)
                self.bSizerSrcWaterMark.Add(self.waterText, 0, wx.ALL | wx.CENTER, 2)
                
                # 当前字体状态
                self.statusSizer = wx.BoxSizer(wx.HORIZONTAL)
                font_status = self.GetFontStatus()                
                self.fontStatusLabel = wx.StaticText(self, label = font_status, size = (332, -1))
                self.fontStatusLabel.SetFont(self.LABEL_FONT)
                self.fontStatusLabel.SetForegroundColour(self.fontColour)
                self.statusSizer.Add(self.fontStatusLabel, 0, wx.TOP | wx.LEFT, 5)
                
                #选择字体                
                self.chooseFont = wx.Button(self, label = "更改当前字体")
                self.chooseFont.SetFont(self.LABEL_FONT)
                self.Bind(wx.EVT_BUTTON, self.OnChooseFont, self.chooseFont)
                self.statusSizer.Add(self.chooseFont, 0, wx.TOP |wx.LEFT | wx.BOTTOM, 5)
                               
                # 水印位置SIZER
                self.waterPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
                
                #水印位置面板				
                self.waterPosition = wx.StaticBox(self, label='水印位置', size=wx.Size(220, 180))
                self.waterPosition.SetFont(self.LABEL_FONT)
                self.btnGroupBoxSizer = wx.StaticBoxSizer(self.waterPosition, wx.VERTICAL)
                #self.waterPanelSizer.Add(self.waterPosition, 0, wx.LEFT, 8)
                
                gSizerBtnGroup = wx.GridSizer( 3, 3, 0, 0 )
                
                #水印位置9个
                self.LeftTop = wx.RadioButton(self, label='左上', pos = wx.DefaultPosition, style = wx.RB_GROUP)
                self.LeftTop.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton)
                self.CenterTop = wx.RadioButton(self, label='中上', pos = wx.DefaultPosition)
                self.CenterTop.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton)
                self.RightTop = wx.RadioButton(self, label='右上', pos = wx.DefaultPosition)
                self.RightTop.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton)
                self.LeftCenter = wx.RadioButton(self, label='左中', pos = wx.DefaultPosition)
                self.LeftCenter.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton)
                self.Center = wx.RadioButton(self, label='正中', pos = wx.DefaultPosition)
                self.Center.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton)
                self.RightCenter = wx.RadioButton(self, label='右中', pos = wx.DefaultPosition)
                self.RightCenter.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton)
                self.LeftBotm = wx.RadioButton(self, label='左下', pos = wx.DefaultPosition)
                self.LeftBotm.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton)
                self.CenterBotm = wx.RadioButton(self, label='中下', pos = wx.DefaultPosition)
                self.CenterBotm.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton)
                self.RightBotm = wx.RadioButton(self, label='右下', pos = wx.DefaultPosition)                
                self.RightBotm.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton)
                
                self.NineBtns = [self.LeftTop, self.CenterTop, self.RightTop, self.LeftCenter, self.Center, self.RightCenter,
                            self.LeftBotm, self.CenterBotm, self.RightBotm]
                for btn in self.NineBtns:
                        btn.SetFont(self.LABEL_FONT)
                        gSizerBtnGroup.Add( btn, 0, wx.ALL, 15 )
                self.btnGroupBoxSizer.Add( gSizerBtnGroup, 1, wx.EXPAND, 0 )
                self.waterPanelSizer.Add(self.btnGroupBoxSizer, 1, wx.ALL |wx.EXPAND, 15)
           
                self.fontEffectSizer = wx.BoxSizer(wx.VERTICAL)
                
                #字体效果设置
                self.textRepeat = wx.StaticText(self, label='水印重复次数:')
                self.textRepeat.SetFont(self.LABEL_FONT)
                self.repeatList = [u'一次 -> 按左边水印位置', u'一次 -> 按鼠标指定位置', u'多次']#, u'最多']                
                # 加载重复次数字符串
                if self.parent.water_text_repeat in [self.repeatList[0], self.repeatList[2]]: value = self.parent.water_text_repeat
                else: value = self.repeatList[0]
                
                self.textRepeatCtrl = wx.ComboBox(self, value = value, choices = self.repeatList, size = (160, -1), style = wx.CB_READONLY)
                self.Bind(wx.EVT_COMBOBOX, self.OnSelect, self.textRepeatCtrl)
                
                self.fontEffectSizer.Add((10, -1))
                
                #不透明度 
                self.pickTrans = wx.StaticText(self, label='不透明度(0~100):')
                self.pickTrans.SetFont(self.LABEL_FONT)
                self.transCtrl = wx.Slider(self, maxValue=100, minValue=0, size = (160, -1),
                        style=wx.SL_HORIZONTAL|wx.SL_LABELS, value = self.parent.text_trans)
                
                # 旋转
                self.textRotate = wx.StaticText(self, label = '旋转角度(0~360):')
                self.textRotate.SetFont(self.LABEL_FONT)
                value = self.parent.water_text_angle
                self.textRotateCtrl = wx.Slider(self, maxValue=360, minValue=0, size = (160, -1),
                        style=wx.SL_HORIZONTAL|wx.SL_LABELS, value = value)
                
                self.m_btnBrowse.Enable(False)
                self.m_btnBrowseFileList.Enable(False)
                
                self.fontEffectSizer.Add(self.textRepeat, 0, wx.ALL | wx.TOP, 2)
                self.fontEffectSizer.Add(self.textRepeatCtrl, 0, wx.ALL | wx.TOP, 2)
                self.fontEffectSizer.Add((-1, 10))
                self.fontEffectSizer.Add(self.pickTrans, 0, wx.ALL | wx.TOP, 2)
                self.fontEffectSizer.Add(self.transCtrl , 0, wx.ALL | wx.TOP , 2)
                self.fontEffectSizer.Add(self.textRotate , 0, wx.ALL | wx.TOP , 2)
                self.fontEffectSizer.Add(self.textRotateCtrl , 0, wx.ALL | wx.TOP , 2)
                
                self.waterPanelSizer.Add(self.fontEffectSizer, 1, wx.LEFT | wx.TOP, 10)
                
                # add a slide factor
                self.bSizerFaq = wx.BoxSizer( wx.VERTICAL )
        
                self.m_staticTextFaq = wx.StaticText( self, wx.ID_ANY, u"频率调节", wx.DefaultPosition, wx.DefaultSize, 0 )
                self.m_staticTextFaq.Wrap( -1 )
                self.bSizerFaq.Add( self.m_staticTextFaq, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
                
                self.m_sliderFaq = wx.Slider( self, wx.ID_ANY, 5, 1, 10, wx.DefaultPosition, wx.DefaultSize, wx.SL_LABELS|wx.SL_VERTICAL )
                self.bSizerFaq.Add( self.m_sliderFaq, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
                
                self.waterPanelSizer.Add(self.bSizerFaq, 1, wx.TOP, 15)
                # finish the slide faq

                self.bSizerSrcWaterMark.Add(self.statusSizer, 0, wx.LEFT, 3)       
                self.sizer.Add(self.bSizerSrcWaterMark, 0, wx.ALL | wx.CENTER, 1)                                   
                self.sizer.Add((-1, 10))
                self.sizer.Add(self.waterPanelSizer, 0, wx.ALL | wx.EXPAND, 0)
                
                # add a separator
                self.sizer.Add(wx.StaticLine(self, wx.ID_ANY),
                                   0, wx.ALL|wx.EXPAND, 5)
                self.btnSizer = wx.BoxSizer(wx.HORIZONTAL)
                
                # toggle between
                self.ToggleRepeatFeq() 
                
                okBtn = wx.BitmapButton( self, wx.ID_ANY, self.parent.preview_ico, wx.DefaultPosition, wx.Size(48, 48), wx.NO_BORDER |wx.BU_EXACTFIT  )
                okBtn.Bind(wx.EVT_BUTTON, self.OnOK)
                self.btnSizer.Add(okBtn, 0, wx.ALL | wx.Center, 6)
                okBtn.SetToolTipString(u'预览效果')
                
                resetBtn = wx.BitmapButton( self, wx.ID_ANY, self.parent.refresh_ico, wx.DefaultPosition, wx.Size(48, 48), wx.NO_BORDER|wx.BU_EXACTFIT  )
                resetBtn.Bind(wx.EVT_BUTTON, self.OnReset)
                self.btnSizer.Add(resetBtn, 0, wx.ALL | wx.Center, 6)
                resetBtn.SetToolTipString(u'重新加载图片')
                
                cancelBtn = wx.BitmapButton( self, wx.ID_ANY, self.parent.close32_ico, wx.DefaultPosition, wx.Size(48, 48), wx.NO_BORDER|wx.BU_EXACTFIT  )
                cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancel)    
                self.btnSizer.Add(cancelBtn, 0, wx.TOP | wx.RIGHT, 6)
                cancelBtn.SetToolTipString(u'关闭')

                self.sizer.Add(self.btnSizer, 0, wx.TOP | wx.ALIGN_RIGHT, 6)                
                self.SetSizer(self.sizer)
                
                self.UpdateText()                
                self.RightBotm.SetValue(True) # 默认选中
                self.m_radioTxt.SetValue(True)
                
        def OnTxtSrc (self, event):
                event.Skip()
                
        def OnTxtSrcChoice (self, event):
                event.Skip()
                
        def OnRadioBtns (self, event):
                self.txtEnabled = self.m_radioTxt.GetValue()
                # process pic buttons
                self.m_btnBrowse.Enable( self.m_radioPic.GetValue())
                if self.m_btnBrowse.IsEnabled(): self.m_btnBrowse.SetFocus()
                # process text buttons
                self.m_btnBrowseFileList.Enable( self.m_radioFileList.GetValue())
                if self.m_btnBrowseFileList.IsEnabled(): self.m_btnBrowseFileList.SetFocus()
                
                self.ToggleWatermarkSrc(self.txtEnabled)
                self.setRotateCtrl()
                event.Skip()
        #---------------------------------------------------------
               
        def onPicBrowse(self, event):
                wildcard = "所有文件 (*.*)|*.*|JPEG 图片 (*.jpg)|*.jpg|BMP 图片 (*.bmp)|*.bmp|PNG 图片 (*.png)|*.png|" +\
                        "GIF 图片 (*.gif)|*.gif|TIF 图片 (*.tif; *.tiff)|*.tif; *.tiff|ICO 图标 (*.ico)|*.ico" 
                        
                fd = wx.FileDialog(self, u'请选择一张水印图片', os.getcwd(), '', wildcard, wx.FD_CHANGE_DIR | wx.OPEN)
                if fd.ShowModal() == wx.ID_OK:
                        self.pic = fd.GetPath()
                        self.m_textCtrlPath.SetValue(self.pic)
                        self.m_textCtrlPath.SetToolTip(wx.ToolTip(self.pic))
                fd.Destroy()
                event.Skip()
                
        def onFileListBrowse (self, event):
                wildcard = "文本文件 (*.txt)|*.txt|Excel文件 (*.xlsx)|*.xlsx|所有文件 (*.*)|*.*"                 
                if self.m_fileListCtrlPath.GetValue() != "": initDir = os.path.dirname(self.m_fileListCtrlPath.GetValue())
                else: initDir = os.getcwd()
                
                fd = wx.FileDialog(self, u'请选择对应的列表文件', initDir , '', wildcard, wx.FD_CHANGE_DIR | wx.OPEN)
                
                if fd.ShowModal() == wx.ID_OK:
                        filein = fd.GetPath()
                        if os.path.isfile(filein): self.ReadExternalFile(filein)   # check if file exitsf                        
                fd.Destroy()
                event.Skip()
                
        def ReadExternalFile(self, filein):
                
                # reset lists
                self.excel_pic_names = []
                self.listFile = []
                try:
                        wb = load_workbook(filein)
                        sheet = wb.get_active_sheet()
                        rows =  sheet.get_highest_row()
                        cols = sheet.get_highest_column()

                        for row in xrange(rows):
                                v = sheet.cell(row=row + 1, column=1).value
                                line = sheet.cell(row=row + 1, column=2).value
                                self.excel_pic_names.append(v.lower())
                                self.listFile.append(line)
                        self.CheckListFiles(rows, filein)
                        
                        
                except InvalidFileException:
                        with open(filein, 'rb') as fileIn:
                                lines = unicode(fileIn.read(),'cp936')
                                rows = len(lines.split("\r\n"))
                                self.listFile = lines.split("\r\n")
                                self.CheckListFiles(rows, filein)
                                
                                
        def CheckListFiles(self, rows, filein):
                if  rows == len(self.parent.picPaths):                        
                        if True in [ (len(j) > 200 ) for j in self.listFile]:
                                wx.MessageBox("列表中有的水印字数超出限制，请检查文件。", "小提醒", wx.OK | wx.ICON_INFORMATION)
                                self.listFile = None
                                self.m_fileListCtrlPath.Clear()
                        else:
                                self.m_fileListCtrlPath.SetValue(filein)
                                self.m_fileListCtrlPath.SetToolTip(wx.ToolTip(filein))                                               
                else:
                        error = '图片总数( %s )与载入列表( %s )不匹配！请重试。' % (len(self.parent.picPaths), rows)
                        self.listFile = None
                        self.m_fileListCtrlPath.Clear()
                        wx.MessageBox(error, "小提醒", wx.OK | wx.ICON_INFORMATION)
                        
                        
                
        #---------------------------------------------------------
        def ToggleWatermarkSrc(self, enableTxt = True):
                #self.m_textCtrlPath.Enable(not enableTxt)
                #self.m_btnBrowse.Enable(not enableTxt)                
                self.staticTxtMark.Enable(not self.m_radioPic.GetValue())
                self.waterText.Enable(enableTxt)
                self.fontStatusLabel.Enable(not self.m_radioPic.GetValue())
                self.chooseFont.Enable(not self.m_radioPic.GetValue()) 
        #----------------------------------------------------------
        def GetFontStatus(self):
                return u"当前字体: " + self.curFont.GetNativeFontInfoUserDesc(). \
                replace("windows-936", u"中文").replace("windows-1252", u"西方语言")
        #----------------------------------------------------------
        def OnSelect(self, event):
                # reload image if not single mode
                if not self.parent.singleMode: self.parent.imgReload()
                self.parent.water_text_repeat = self.textRepeatCtrl.GetValue()
                
                if self.textRepeatCtrl.GetValue() == u'一次 -> 按鼠标指定位置':
                        if self.parent.show_custom_warning == 'YES':
                                wx.MessageBox(u"请用鼠标左键单击水印的位置。", u"自定义水印位置", wx.OK | wx.ICON_INFORMATION)
                                self.parent.show_custom_warning = 'NO'
                        else: pub.sendMessage("set status", msg = u"请用鼠标左键单击水印的位置。")
                        # enable crop when the control is enbaled
                        if not self.parent.rubber: self.parent.rubber = wxPyRubberBander(self.parent.imageCtrl)
                        
                # 0 = no repeat; 1 = repeat
                self.ToggleRepeatFeq()
                self.parent.startPoint = None                
                event.Skip()
                
        ##----------------------------------------------------------
        def ToggleRepeatFeq(self):
                # define enable or not
                repeat_once = (u'一次' in self.textRepeatCtrl.GetValue())
                self.parent.enablePin = (self.textRepeatCtrl.GetValue() == u'一次 -> 按鼠标指定位置')
                self.m_staticTextFaq.Enable(not repeat_once)
                self.m_sliderFaq.Enable(not repeat_once)
                posFlag = (self.textRepeatCtrl.GetValue() == u'一次 -> 按左边水印位置')
                self.waterPosition.Enable(posFlag)
                for radioBtn in self.NineBtns: radioBtn.Enable(posFlag) 
                self.setRotateCtrl()
                # 初始化 google drop
                if self.parent.enablePin:
                        if not self.parent.rubber:
                                self.parent.rubber = wxPyRubberBander(self.parent.imageCtrl)
        ##----------------------------------------------------------
        def setRotateCtrl(self):
                flag = u'一次' in self.textRepeatCtrl.GetValue() #and (self.txtEnabled or self.m_radioFileList.GetValue()))
                self.textRotateCtrl.Enable(not flag )
                self.textRotate.Enable(not flag)
        #----------------------------------------------------------
        def OnChooseFont(self, event):
                """
                选择字体时,改变预览框字体的样式,并将赋值给全局变量fontFile
                """
                fontData = wx.FontData()
                dlg = wx.FontDialog(self, fontData)
                fontData = dlg.GetFontData()
                fontData.SetInitialFont(self.curFont)
                fontData.SetColour(self.fontColour)
                #fontData.SetAllowSymbols(False)                
                #fontData.EnableEffects(False)                 
                
                if dlg.ShowModal() == wx.ID_OK:
                        fontData = dlg.GetFontData()
                        #取得所选字体
                        self.curFont = fontData.GetChosenFont()
                        #取得字体颜色                        
                        self.fontColour = fontData.GetColour()
                        
                        #设置字体大小
                        self.fontSize = self.curFont.GetPointSize()
                        #取样式的系统字体TTF名                    
                        self.fName = self.curFont.GetFaceName()
                        #取字体样式
                        self.fontStyle  = self.curFont.GetStyle()
                        
                        # set font status label                        
                        self.fontStatusLabel.SetLabel(self.GetFontStatus())
                        self.fontStatusLabel.SetForegroundColour(self.fontColour)
                        #self.fontStatusLabel.SetFont(self.curFont)

                        if self.fName in [unicode(font,"cp936") for font in ["宋体", "宋体-PUA","新宋体"]]:
                                self.fName = unicode("SimSun & NSimSun", "cp936")
                        elif self.fName == unicode("仿宋","cp936"):
                                self.fName = unicode("FangSong", "cp936")
                        elif self.fName == unicode("黑体","cp936"):
                                self.fName = unicode("SimHei", "cp936")
                        elif self.fName == unicode("楷体","cp936"):
                                self.fName = unicode("KaiTi", "cp936")
                        elif self.fName == unicode("微软雅黑","cp936"):
                                self.fName = unicode("Microsoft YaHei", "cp936")
                                
                        # process font name starts with "@"
                        elif self.fName in [unicode(font, "cp936") for font in ["@宋体", "@新宋体", "@仿宋"]]:
                                self.fName = unicode("SimSun-ExtB", "cp936")
                        elif self.fName == unicode("@楷体", "cp936"):
                                self.fName = unicode("DFKai-SB", "cp936")
                        elif self.fName == unicode("@黑体", "cp936"):
                                self.fName = unicode("Microsoft JhengHei & Microsoft JhengHei UI", "cp936")
                        elif self.fName == unicode("@微软雅黑", "cp936"):
                                self.fName = unicode("Microsoft YaHei & Microsoft YaHei UI", "cp936")
                        elif self.fName.startswith(unicode("@", "cp936")):
                                self.fName = unicode("MingLiU & PMingLiU & MingLiU_HKSCS", "cp936")
                        #if self.fName==unicode("宋体","cp936") or self.fName==unicode("宋体-PUA","cp936") or self.fName==unicode("新宋体","cp936"):
                        #        self.fName = unicode("宋体 & 新宋体","cp936")
                        try:
                                self.fontFile = self.systemFontDict[self.fName] 
                        except:
                                # upon exception, use default font                          
                                self.fName = unicode("SimSun & NSimSun", "cp936")
                                self.fontFile = self.systemFontDict[self.fName]
                        finally:
                                self.UpdateText()
                                self.waterText.Refresh()
                dlg.Destroy()
                event.Skip()
        #----------------------------------------------------------
        def UpdateText(self):                
                #self.curFont = wx.Font(self.fontSize, self.family, self.fontFile, self.weight, self.isUnderlined, self.fName)
                self.waterText.SetFont(self.curFont)
                self.waterText.SetOwnForegroundColour(self.fontColour) 
                #self.waterText.SetStrikethrough(self.strikethrough)

        #-----------------------------------------------------------
        def OnWaterText(self, event):
                """
                当修改水印文字框时,同步更新text的值
                """
                self.text = self.waterText.GetValue()
                self.parent.water_text = self.text
                event.Skip()
         #------------------------------------------------------------
        def DoWaterMark(self, filename, im):
                """"""
                return self._im_mark(filename, False, im)                
        
        #-----------------------------------------------------------
        def _GetSystemFontDict(self):
                """
                取系统的字体集,返回一个字典类型的对象,在初始化时被调用.
                """
                
                hkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
                                       "Software\\Microsoft\\Windows NT\\CurrentVersion\\Fonts") 
                nSubKey, nSubValue, lastModify = _winreg.QueryInfoKey(hkey)
                d = {}
                for i in range(nSubValue): 
                        valueName, valueObj,valueType = _winreg.EnumValue(hkey, i)
                        key = valueName.split(" (")[0]
                        d[unicode(key,"cp936")] = valueObj

                _winreg.CloseKey(hkey)
                return d
        
        def pic_watermark(self, isRepeat, ANGLE, percentage, filename, faq, im = None):
                if im:
                        im = im.convert("RGBA")
                        img = self.parent.wand2pil(im, 'PNG')
                # check if single mode
                elif self.parent.singleMode and self.parent.im_preview:
                        img = self.parent.wand2pil(self.parent.im_preview, 'PNG')
                else:   img = self.parent.readWandImage(filename)
                
                try:
                        imgTop = self.parent.readWandImage(self.pic)
                        imgTop.rotate(ANGLE) 
                        textwidth, textheight = imgTop.size
                        if (textwidth > self.parent.W or textheight > self.parent.H):
                                wx.MessageBox("您选择的图片太大了！请缩小尺寸后再试。", "小提醒", wx.OK | wx.ICON_INFORMATION)
                                return
                except:  return
                
                isPosSet, xy = self.isMousePos(textwidth, textheight,img.size[0], img.size[1])
                if not isPosSet: return
                
                #draw.setfont(font)
                if isRepeat:
                        weight = 10.0 / faq
                        #4 / self.repeatList.index(self.parent.water_text_repeat)
                        for x in range(self.Base / 2, 2 * img.size[0], textwidth + int(45 * weight)):
                                for y in range(self.Base / 2, 2 * img.size[1], textheight + int(60 * weight)):
                                        img.watermark(imgTop, 1 - percentage, x, y)
                else:
                        img.watermark(imgTop, 1 - percentage, xy[0], xy[1])
                return self.parent.wand2pil(img, 'PNG')

        def isMousePos(self, textwidth, textheight, w, h):
                # check if mouse position is set manually?
                isPosSet = True
                if self.textRepeatCtrl.GetValue() == u'一次 -> 按鼠标指定位置':
                        if self.parent.startPoint:
                                left = self.parent.startPoint
                                scale = self.parent.scale
                                xy = (int(left.x * scale), int(left.y * scale))
                        else:
                                wx.MessageBox("您还没有指定水印位置呢:-)。", "小提醒", wx.OK | wx.ICON_INFORMATION)
                                isPosSet = False
                                xy = None
                else: 
                        self.PositionDict = self._PositionMap(w, h, textwidth, textheight)                 
                        xy = self.PositionDict[self.fontPosition]
                return isPosSet, xy
        
        def GetWaterMarkText(self, filename):
                """
                get corresponding water mark
                """
                base = os.path.basename(filename) # only the filename
                if self.txtEnabled: return self.text
                elif self.m_radioPicName.GetValue(): return base
                elif self.m_radioFileList.GetValue():
                        # process text file or excel file # include self.text also
                        if self.excel_pic_names and self.listFile:
                                return self.text + '\n' + self.listFile[self.excel_pic_names.index(base.lower())]
                        else:
                            return self.text + '\n' + self.listFile[self.parent.picPaths.index(filename)]
                else: return None
                       
        #-----------------------------------------------------------
        def _im_mark(self, filename, istemp = True, im = None):
                """
                进行制作的方法, 参数
                    filename : 源文件名
                    im: 输入Image实例
                """
                
                # Check if we need to continue
                if (self.m_radioPic.GetValue() and self.m_textCtrlPath.GetValue() == "") or (self.m_radioFileList.GetValue() and self.m_fileListCtrlPath.GetValue() == "") or \
                (self.m_radioTxt.GetValue() and self.text == ""):
                        #print "invalid"
                        return
                
                ##############################
                # update parent parameters
                # 0 = no repeat; 1 = repeat
                self.parent.water_text_repeat = self.textRepeatCtrl.GetValue()
                self.parent.water_text_angle = self.textRotateCtrl.GetValue()
                self.parent.text_trans = self.transCtrl.GetValue()
                ANGLE = self.parent.water_text_angle
                isRepeat = not (self.parent.water_text_repeat.startswith( u'一次'))
                faq = self.m_sliderFaq.GetValue()
                percentage = self.transCtrl.GetValue() * 0.01 
                ##############################
                
                # 处理水印来源
                text = self.GetWaterMarkText(filename) #self.text
                #print filename, text
                if isinstance(text, str): text = unicode(text, 'cp936')
                
                picEnabled = self.m_radioPic.GetValue()
                if not picEnabled:
                
                        FONT = self.fontFile  
                        
                        # 设定字体颜色和透明度 -------------#
                        r,g,b = self.fontColour
                        
                        a = int( percentage * 255)#取百分比
                        self.finalColourWithAlpha = (r,g,b, a)
                        #-----------------------------------#                                                

                        cor_fill = self.finalColourWithAlpha
                        
                        if im:  img = im.convert("RGBA") # it is actual processing
                        
                        # Check if it is single mode
                        elif self.parent.singleMode and self.parent.im_preview:
                                img = self.parent.im_preview
                        else:   img = self.parent.imageOpen(filename).convert("RGBA") #
                        
                        # create a new water mark image
                        if isRepeat:                        
                                watermark = Image.new("RGBA", (2 * img.size[0], 2 * img.size[1]))
                        else:
                                watermark = Image.new("RGBA", (img.size[0], img.size[1]))

                        draw = ImageDraw.ImageDraw(watermark, "RGBA")
                        font = ImageFont.truetype(FONT, self.fontSize)
        
                        nexttextwidth, nexttextheight = font.getsize(text)
                        textwidth, textheight = nexttextwidth, nexttextheight
                        
                        #取坐标开始---------------------------------
                        w, h = watermark.size
                        
                        isPosSet, xy = self.isMousePos(textwidth, textheight, w, h)
                        if not isPosSet: return
        
                        #取坐标完成---------------------------------
                        
                        #draw.setfont(font)
                        if isRepeat:
                                #weight = 4 / self.repeatList.index(self.parent.water_text_repeat)
                                if faq == 1:
                                    r = math.radians(ANGLE)
                                    #
                                    xy = self.Base/2, self.Base/2
                                    for line in text.split('\n'):
                                        draw.text(xy, line, fill=cor_fill, font = font)
                                        xy = xy[0], xy[1] + textheight * 1.5
                                    text_list = text.split('\n')
                                    text_list.sort(key = lambda s: len(s))
                                    max_textwidth = font.getsize(text_list[-1])[0]
                                    rot_img = watermark.rotate(ANGLE, expand = 1)
                                    watermark = rot_img.crop((self.Base/2, int(self.Base /2 + math.sin(r) * (img.size[0] * 2 - max_textwidth - 15 )), (self.Base/2 + img.size[0]), int(self.Base /2 + math.sin(r) * ( img.size[0] * 2 - max_textwidth - 15) + img.size[1]) ) )
                                   
                                else:
                                    weight = 10.0 / faq
                                    for x in range(self.Base / 2, 2 * img.size[0], textwidth + int(45 * weight)):
                                            for y in range(self.Base / 2, 2 * img.size[1], textheight + int(60 * weight)):
                                                    draw.text((x,y), text, fill=cor_fill, font=font)
                                    rot_img = watermark.rotate(ANGLE, expand = 0)
                                    watermark = rot_img.crop((img.size[0]/2, img.size[1]/2, (img.size[0] * 3)/2, (img.size[1] * 3)/2) )                       
                        else:
                            for line in text.split('\n'):
                                draw.text(xy, line, fill=cor_fill, font = font)
                                xy = xy[0], xy[1] + textheight * 1.5
                                
                        # PIL merge of two images with alpha channels
                        img = Image.alpha_composite(img, watermark)
                else:
                        img = self.pic_watermark(isRepeat, ANGLE, percentage, filename, faq, im ) 
                if img:
                        if istemp:
                                ext = os.path.splitext(filename)[1]
                                self.parent.imgPreview(img, ext)                                            
                        else:
                                return img
                             
        #------------------------------------------------------------
        def _PositionMap(self,imgW, imgH, fontW, fontH):
                """
                设置水印坐标函数,生成一个PositionDict的字典,并返回.参数:
                   imgW : 图片宽度
                   imgH : 图片高度
                   fontW: 水印文字宽度
                   fontH: 水印文字高度 
                """
                #纵向第二列的X坐标
                MX = (imgW-fontW)/2
                #纵向第三列的X坐标
                RX = imgW - fontW - self.Base
                #横向第二列的Y坐标 
                MY = (imgH-fontH)/2
                #横向第三列下部的Y坐标
                BY = imgH-fontH-self.Base
                PositionDict = {
                                 1:(self.Base, self.Base),#左上
                                 2:(MX, self.Base),#中上
                                 3:(RX, self.Base),#右上
                                 4:(self.Base, MY),#左中
                                 5:(MX, MY),#正中
                                 6:(RX, MY),#右中
                                 7:(self.Base, BY),#左下
                                 8:(MX, BY),#中下
                                 9:(RX, BY)#右下
                                 }
                return PositionDict
        #-----------------------------------------------------------
        def OnRadioButton(self, event):
                # 获得水印位置
                if self.LeftTop.GetValue():
                    self.fontPosition = 1#左上
                elif self.CenterTop.GetValue():
                    self.fontPosition = 2#中上
                elif self.RightTop.GetValue():
                    self.fontPosition = 3#右上
                elif self.LeftCenter.GetValue():
                    self.fontPosition = 4#左中
                elif self.Center.GetValue():
                    self.fontPosition = 5#正中
                elif self.RightCenter.GetValue():
                    self.fontPosition = 6#右中
                elif self.LeftBotm.GetValue():
                    self.fontPosition = 7#左下
                elif self.CenterBotm.GetValue():
                    self.fontPosition = 8#中下
                elif self.RightBotm.GetValue():
                    self.fontPosition = 9#右下
                event.Skip()
        #------------------------------------------------------------
        def OnCancel(self, event):                
                #self.parent.isCancel = True
                #self.parent.picGUI.m_buttonWaterMark.SetValue(False)
                self.Hide() #不要现在删除
        #-------------------------------------------------------------
        def OnOK(self, event):   # preview             
                img = self.parent.getCurJpg()
                self.parent.current_dpi = self.parent.getSettingDPI(img)
                self._im_mark(img)
                #self.Show(False)
        #-----------------------------------------------------------
        def OnReset(self, event):
                self.parent.imgReload()
                
class ShowListDlg ( wx.Dialog ):
        
        def __init__( self, parent ):
                wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"当前文件列表", pos = wx.DefaultPosition, size = wx.Size( 587,530 ), style = wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX | wx.RESIZE_BORDER )
                
                sizer = wx.BoxSizer(wx.VERTICAL)
                panel = wx.Panel(self, wx.ID_ANY)
                self.index = 0
                
                self.m_listCtrlImgList = wx.ListCtrl( panel, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, 400), wx.BORDER_SUNKEN|wx.LC_REPORT )
                self.m_listCtrlImgList.InsertColumn(0, u'编号')                
                self.m_listCtrlImgList.InsertColumn(1, u'名称', width = 100)
                self.m_listCtrlImgList.InsertColumn(2, u'路径', width = 700)
                
                btn = wx.Button(panel, label=u"关闭")
                btn.Bind(wx.EVT_BUTTON, self.close)
                
                sizer.Add(self.m_listCtrlImgList, 0, wx.ALL|wx.EXPAND, 5)
                sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
                panel.SetSizer(sizer)

        # Virtual event handlers, overide them in your derived class
        def close ( self, event ):
                self.Hide()
                event.Skip()
                
        def addlines ( self, fileList ):
                while self.index < len(fileList):
                        path = os.path.dirname(fileList[self.index])
                        fname = os.path.basename(fileList[self.index])
                        self.m_listCtrlImgList.InsertStringItem(self.index, '%i' % (self.index + 1))
                        self.m_listCtrlImgList.SetStringItem(self.index, 1, fname)
                        self.m_listCtrlImgList.SetStringItem(self.index, 2, path)
                        self.index += 1