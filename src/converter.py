# -*- coding: cp936 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
###########################################################################

import wx
#import img2py
from PIL import Image as pImage
from wand.image import Image as wImage
#import numpy
from wand.image import Image
from glob import glob
import os, uuid
from StringIO import StringIO
from wx.lib.pubsub import pub
import win32com.client
import ConversionsIcon
from subprocess import call
from installed_progs import appDetect
import re
import sys

PIC_LIST = ['.JPG', '.JPEG', '.BMP', '.TIF', '.TIFF', '.GIF', '.PNG', '.PSD']
exepath = unicode(os.path.dirname(sys.path[0]), 'cp936')
gs_home = os.path.join(exepath, 'gs', 'bin')
os.environ['PATH'] += ';' + gs_home

###########################################################################
## Class PicConverter
###########################################################################

class PicConverter ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"ͼƬת��", pos = wx.DefaultPosition,
				    size = wx.Size( 700,820 ), style = wx.DEFAULT_DIALOG_STYLE | wx.MINIMIZE_BOX )
		
		self.parent = parent		
		self.SetIcon(self.parent.midi)
		self.success  = True
		self.task_count = 0
		self.statusmsg = ''
		self.cur_img  = ''
		self.filename = ''
		self.RefreshTitle()
		#################
		single_pic = ConversionsIcon.singlePic.GetBitmap()
		multi_pic = ConversionsIcon.multiPic.GetBitmap()
		to = ConversionsIcon.to.GetBitmap()
		ppt = ConversionsIcon.ppt.GetBitmap()
		pdf = ConversionsIcon.pdf.GetBitmap()
		play48 = ConversionsIcon.play48.GetBitmap()
		close48 = ConversionsIcon.close48.GetBitmap()
		icon = ConversionsIcon.icon.GetBitmap()
		#################
		
		bSizerMain = wx.BoxSizer( wx.VERTICAL )
		#ͼƬתICO
		sbSizerToIco = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"ͼƬתICO" ), wx.VERTICAL )
		
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_bitmap8 = wx.StaticBitmap( self, wx.ID_ANY, single_pic, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_bitmap8, 0, wx.ALL, 5 )
		self.m_bitmap8.SetToolTipString(u'��ǰͼƬתICO�ļ�')
		
		self.m_bitmap9 = wx.StaticBitmap( self, wx.ID_ANY, to, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_bitmap9, 0, wx.TOP, 10 )
		
		self.m_bitmap10 = wx.StaticBitmap( self, wx.ID_ANY, icon, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_bitmap10, 0, wx.LEFT|wx.TOP, 5 )
		self.m_bitmap10.SetToolTipString(u'��ǰͼƬתICO�ļ�')
		
		sbSizerToIco.Add( bSizer10, 1, 0, 5 )
		
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		self.m_staticBoxComment = wx.StaticBox( self, wx.ID_ANY, u"ͼƬ˵��" )		
		sbSizerComment = wx.StaticBoxSizer( self.m_staticBoxComment, wx.VERTICAL )
		#self.m_staticBoxComment.Enable(False)
		
		self.m_staticTextFormat = wx.StaticText( self, wx.ID_ANY, u"��ʽ��PNG|JPEG|GIF|BMP��", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextFormat.Wrap( -1 )
		sbSizerComment.Add( self.m_staticTextFormat, 0, wx.ALL, 5 )
		#self.m_staticTextFormat.Enable(False)
		
		self.m_staticTextRatio = wx.StaticText( self, wx.ID_ANY, u"���������鷽�εĳ����", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextRatio.Wrap( -1 )
		sbSizerComment.Add( self.m_staticTextRatio, 0, wx.ALL, 5 )
		#self.m_staticTextRatio.Enable(False)
		
		self.m_staticTextSize = wx.StaticText( self, wx.ID_ANY, u"��С���ļ�������3MB", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextSize.Wrap( -1 )
		sbSizerComment.Add( self.m_staticTextSize, 0, wx.ALL, 5 )
		#self.m_staticTextSize.Enable(False)
		
		bSizer11.Add( sbSizerComment, 1, wx.EXPAND | wx.ALL, 3 )
		
		sbSizerSize = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"ICO���ش�С" ), wx.HORIZONTAL )
		
		bSizerSize1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_checkBox16 = wx.CheckBox( self, wx.ID_ANY, u"16 x 16", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerSize1.Add( self.m_checkBox16, 0, wx.ALL, 5 )
		
		self.m_checkBox32 = wx.CheckBox( self, wx.ID_ANY, u"32 x 32", wx.DefaultPosition, wx.DefaultSize, 0 )
		#self.m_checkBox32.SetValue(True) 
		bSizerSize1.Add( self.m_checkBox32, 0, wx.ALL, 5 )
		
		self.m_checkBox64 = wx.CheckBox( self, wx.ID_ANY, u"64 x 64", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerSize1.Add( self.m_checkBox64, 0, wx.ALL, 5 )
		
		self.m_checkBox96 = wx.CheckBox( self, wx.ID_ANY, u"96 x 96", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerSize1.Add( self.m_checkBox96, 0, wx.ALL, 5 )
		
		self.m_checkBox256 = wx.CheckBox( self, wx.ID_ANY, u"256 x 256", wx.DefaultPosition, wx.DefaultSize, 0 ) #(ֻ֧��32λ��ɫ)
		bSizerSize1.Add( self.m_checkBox256, 0, wx.ALL, 5 )
		
		
		sbSizerSize.Add( bSizerSize1, 1, wx.EXPAND, 5 )
		
		bSizerSize2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_checkBox24 = wx.CheckBox( self, wx.ID_ANY, u"24 x 24", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerSize2.Add( self.m_checkBox24, 0, wx.ALL, 5 )
		
		self.m_checkBox48 = wx.CheckBox( self, wx.ID_ANY, u"48 x 48", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerSize2.Add( self.m_checkBox48, 0, wx.ALL, 5 )
		
		self.m_checkBox72 = wx.CheckBox( self, wx.ID_ANY, u"72 x 72", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerSize2.Add( self.m_checkBox72, 0, wx.ALL, 5 )
		
		self.m_checkBox128 = wx.CheckBox( self, wx.ID_ANY, u"128 x 128", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerSize2.Add( self.m_checkBox128, 0, wx.ALL, 5 )		
		
		sbSizerSize.Add( bSizerSize2, 1, wx.EXPAND, 5 )		
		bSizer11.Add( sbSizerSize, 1, wx.EXPAND | wx.ALL, 3 )
		
		self.pixelSizeDict = {self.m_checkBox16 : 16, self.m_checkBox24 : 24, self.m_checkBox32 : 32, self.m_checkBox48 : 48,
						 self.m_checkBox64 : 64, self.m_checkBox72 : 72, self.m_checkBox96 : 96, self.m_checkBox128 : 128,
						 self.m_checkBox256 : 256}
		
		sbSizerDepth = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"ICO����" ), wx.VERTICAL )
		
		
		m_comboBoxBitChoices = [ u"8λ (256ɫ)", u"32λ (���ɫ)" ]
		self.m_comboBoxBit = wx.ComboBox( self, wx.ID_ANY, u"���ɫ (32λ)", wx.DefaultPosition, wx.Size( 150,-1 ), m_comboBoxBitChoices, wx.CB_READONLY )
		self.m_comboBoxBit.SetSelection( 1 )
		self.m_comboBoxBit.Enable( False )
		sbSizerDepth.Add( self.m_comboBoxBit, 0, wx.ALL, 5 )
		
		self.m_checkBoxMultiSave = wx.CheckBox( self, wx.ID_ANY, u"�ϲ��������ص�һ��ICO�ļ�", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizerDepth.Add( self.m_checkBoxMultiSave, 0, wx.ALL, 5 )
		self.m_checkBoxMultiSave.SetValue(True)
		
		bSizer11.Add( sbSizerDepth, 1, wx.EXPAND | wx.ALL, 3 )
		
		
		sbSizerToIco.Add( bSizer11, 0, 0, 5 )
		
		
		bSizerMain.Add( sbSizerToIco, 1, wx.ALL |wx.EXPAND, 5 )
		#ͼƬ��PDFת��
		sbSizerToPdf = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"ͼƬ��PDFת��" ), wx.VERTICAL )
		
		bSizerPicSource = wx.BoxSizer( wx.HORIZONTAL )
		
				
		self.m_checkBoxNonePic = wx.RadioButton( self, wx.ID_ANY, u"ʲô����ѡ", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
		#wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxNonePic.Bind(wx.EVT_RADIOBUTTON, self.OnNonePic)
		bSizerPicSource.Add( self.m_checkBoxNonePic, 0, wx.ALIGN_CENTER | wx.ALL, 5 )
		
		self.m_checkBoxSinglePic = wx.RadioButton( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize) #, wx.RB_GROUP )
		#wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxSinglePic.Bind(wx.EVT_RADIOBUTTON, self.OnSinglePic)
		bSizerPicSource.Add( self.m_checkBoxSinglePic, 0, wx.ALIGN_CENTER | wx.ALL, 5 )
		
		self.m_bitmapSingle = wx.StaticBitmap( self, wx.ID_ANY, single_pic, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_bitmapSingle.SetToolTipString( u"���浱ǰͼƬ��һ��PDF�ļ�" )
		
		bSizerPicSource.Add( self.m_bitmapSingle, 0, wx.ALL, 5 )
		
		self.m_checkBoxMultiPic = wx.RadioButton( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		#wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxMultiPic.Bind(wx.EVT_RADIOBUTTON, self.OnMultiPic)
		bSizerPicSource.Add( self.m_checkBoxMultiPic, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5 )
		
		self.m_bitmapMultiPics = wx.StaticBitmap( self, wx.ID_ANY, multi_pic, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_bitmapMultiPics.SetToolTipString( u"��������ͼƬ��һ��PDF�ļ�" )
		
		bSizerPicSource.Add( self.m_bitmapMultiPics, 0, wx.ALIGN_CENTER_VERTICAL| wx.ALL, 5 )
		
		self.m_bitmapArrow = wx.StaticBitmap( self, wx.ID_ANY, to, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerPicSource.Add( self.m_bitmapArrow, 0, wx.ALIGN_CENTER_VERTICAL |wx.ALL, 0 )
		
		self.m_bitmapPdf = wx.StaticBitmap( self, wx.ID_ANY, pdf, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerPicSource.Add( self.m_bitmapPdf, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5 )
		self.m_bitmapPdf.SetToolTipString( u"ת��һ������ͼƬ��PDF" )
		#---------added-----------------
		bSizerPicSource.Add( ( 30, -1) )
		self.m_checkBoxPdf2Pic = wx.RadioButton( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize)
		#wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxPdf2Pic.Bind(wx.EVT_RADIOBUTTON, self.OnPdf2Pic)
		bSizerPicSource.Add( self.m_checkBoxPdf2Pic, 0, wx.ALIGN_CENTER | wx.ALL, 5 )
		
		self.m_bitmapPdf2 = wx.StaticBitmap( self, wx.ID_ANY, pdf, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerPicSource.Add( self.m_bitmapPdf2, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5 )

		self.m_bitmapArrow2 = wx.StaticBitmap( self, wx.ID_ANY, to, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerPicSource.Add( self.m_bitmapArrow2, 0, wx.ALIGN_CENTER_VERTICAL |wx.ALL, 5 )

		self.m_bitmapSingle2 = wx.StaticBitmap( self, wx.ID_ANY, single_pic, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_bitmapSingle2.SetToolTipString( u"ת��ѡ���PDF��PNG" )
		bSizerPicSource.Add( self.m_bitmapSingle2, 0, wx.ALIGN_CENTER_VERTICAL |wx.ALL, 5 )
		
		self.set_tooltip()
		
		#---------- added res --------------
		bSizerPicSource.Add( ( 10, -1) )
		self.m_staticSplitRes = wx.StaticText( self, wx.ID_ANY, u"�ֱ���", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerPicSource.Add( self.m_staticSplitRes, 0, wx.ALL, 5 )
		self.m_staticSplitRes.Hide()
				
		self.m_SplitResList = [u'75 dpi', u'150 dpi', u'200 dpi', u'300 dpi', u'600 dpi']      
		self.m_SplitResBox = wx.ComboBox( self, value = self.m_SplitResList[1], choices = self.m_SplitResList, style = wx.CB_READONLY)
		bSizerPicSource.Add( self.m_SplitResBox, 0, wx.ALL, 5 )
		self.m_SplitResBox.Hide()
		
		#-----------res end -----------------
		
		#---------added end--------------
		
		sbSizerToPdf.Add( bSizerPicSource, 1, wx.EXPAND|wx.TOP, 5 )
		
		bSizerPath = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticTextPdf = wx.StaticText( self, wx.ID_ANY, u"Ŀ��PDF�ļ�����", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerPath.Add( self.m_staticTextPdf, 0, wx.ALL, 5 )		
		
		self.m_textCtrlPdfName = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerPath.Add( self.m_textCtrlPdfName, 1, wx.ALL, 5 )
		#self.filename = os.path.splitext(os.path.basename(self.cur_img))[0]
		#self.m_textCtrlPdfName.SetValue(self.filename)
		
		self.m_staticTextSuf = wx.StaticText( self, wx.ID_ANY, u".PDF", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerPath.Add( self.m_staticTextSuf, 0, wx.ALL, 12 )
		
		self.m_buttonPdfBrowse = wx.Button( self, wx.ID_ANY, u"...", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		self.m_buttonPdfBrowse.SetToolTipString( u"���PDF�ļ�" )
		self.m_buttonPdfBrowse.Bind( wx.EVT_BUTTON, self.OnPdfBrowse )
		self.m_buttonPdfBrowse.Hide()
		
		bSizerPath.Add( self.m_buttonPdfBrowse, 0, wx.ALL, 5 )
		
		
		sbSizerToPdf.Add( bSizerPath, 1, wx.EXPAND|wx.TOP, 0 )
		
		bSizerMain.Add( sbSizerToPdf, 1, wx.ALL |wx.BOTTOM|wx.EXPAND, 5 )
		#PPTתͼƬ
		sbSizerToPic = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"PPTתͼƬ" ), wx.VERTICAL )
		
		bSizerIcons = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_checkBoxPpt = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerIcons.Add( self.m_checkBoxPpt, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_bitmapPpt = wx.StaticBitmap( self, wx.ID_ANY, ppt, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_bitmapPpt.SetToolTipString( u"��PowerPoint�еĻõƱ���Ϊ������ͼƬ" )
		
		bSizerIcons.Add( self.m_bitmapPpt, 0, wx.ALL, 5 )
		
		self.m_bitmapArrow = wx.StaticBitmap( self, wx.ID_ANY, to, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerIcons.Add( self.m_bitmapArrow, 0, wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM, 5 )
		
		self.m_bitmapMultiPics = wx.StaticBitmap( self, wx.ID_ANY, multi_pic, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerIcons.Add( self.m_bitmapMultiPics, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		self.m_bitmapMultiPics.SetToolTipString( u"��PowerPoint�еĻõƱ���Ϊ������ͼƬ" )
		
		#---------- added size --------------
		bSizerIcons.Add( ( 20, -1) )
		self.m_staticPicSize = wx.StaticText( self, wx.ID_ANY, u"ͼƬ�ֱ���", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerIcons.Add( self.m_staticPicSize, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
				
		self.m_PicSizeList = [u'800 x 600', u'1200 x 900', u'1600 x 1200']      
		self.m_PicSizeBox = wx.ComboBox( self, value = self.m_PicSizeList[0], choices = self.m_PicSizeList, style = wx.CB_READONLY)
		bSizerIcons.Add( self.m_PicSizeBox, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		#---------- added format --------------
		bSizerIcons.Add( ( 10, -1) )
		self.m_staticPicFormat = wx.StaticText( self, wx.ID_ANY, u"ͼƬ��ʽ", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerIcons.Add( self.m_staticPicFormat, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
				
		self.m_PicFormatList = [u'.JPG', u'.PNG']      
		self.m_PicFormatBox = wx.ComboBox( self, value = self.m_PicFormatList[0], choices = self.m_PicFormatList, style = wx.CB_READONLY)
		bSizerIcons.Add( self.m_PicFormatBox, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		sbSizerToPic.Add( bSizerIcons, 1, wx.EXPAND, 5 )
		
		bSizerPpt = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticTextSrcPpt = wx.StaticText( self, wx.ID_ANY, u"��ѡ��PPTԴ�ļ���", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerPpt.Add( self.m_staticTextSrcPpt, 0, wx.ALL, 5 )
		
		self.m_textCtrlPptPath = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		bSizerPpt.Add( self.m_textCtrlPptPath, 1, wx.ALL, 5 )
		
		self.m_buttonPptBrowse = wx.Button( self, wx.ID_ANY, u"...", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		self.m_buttonPptBrowse.SetToolTipString( u"���PPT�ļ�" )
		
		bSizerPpt.Add( self.m_buttonPptBrowse, 0, wx.ALL, 5 )
		
		sbSizerToPic.Add( bSizerPpt, 1, wx.EXPAND, 5 )					
				
		self.m_staticTextNote = wx.StaticText( self, wx.ID_ANY, u"ÿ�Żõƿɴ�Ϊһ��ָ���ֱ���/��ʽ��ͼƬ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextNote.Wrap( -1 )
		self.m_staticTextNote.Enable( False )
		
		sbSizerToPic.Add( self.m_staticTextNote, 0, wx.ALIGN_CENTER, 5 )
		
		
		bSizerMain.Add( sbSizerToPic, 1, wx.ALL|wx.EXPAND, 5 )

		# ͼƬ��ʽת��
		sbSizerTrans = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"ͼƬ��ʽת��" ), wx.VERTICAL )
		
		bSizerPicSrc = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_radioBtnCurPic = wx.RadioButton( self, wx.ID_ANY, u"Դ�ļ�Ϊ��ǰͼƬ", wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
		bSizerPicSrc.Add( self.m_radioBtnCurPic, 0, wx.ALL, 5 )
		self.m_radioBtnCurPic.Bind(wx.EVT_RADIOBUTTON, self.OnTogglePicSrc)
		
		self.m_radioBtnPsd = wx.RadioButton( self, wx.ID_ANY, u"Դ�ļ�ΪPSD/PDD�ļ�", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerPicSrc.Add( self.m_radioBtnPsd, 0, wx.ALL, 5 )
		self.m_radioBtnPsd.Bind(wx.EVT_RADIOBUTTON, self.OnTogglePicSrc)
		
		self.m_textCtrlPsdPath = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerPicSrc.Add( self.m_textCtrlPsdPath, 1, wx.ALL, 5 )
		self.m_textCtrlPsdPath.Enable(False)		
		
		self.m_buttonOpen = wx.Button( self, wx.ID_ANY, u"...", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		bSizerPicSrc.Add( self.m_buttonOpen, 0, wx.ALL, 5 )
		self.m_buttonOpen.Enable(False)
		self.m_buttonOpen.Bind(wx.EVT_BUTTON, self.OnOpen)
		
		sbSizerTrans.Add( bSizerPicSrc, 1, wx.EXPAND, 5 )
		
		bSizerSaveAs = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_checkBoxSaveAs = wx.CheckBox( self, wx.ID_ANY, u"���Ϊ�ļ�����", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerSaveAs.Add( self.m_checkBoxSaveAs, 0, wx.ALL, 5 )		
		
		self.m_textCtrlNameAlternate = wx.TextCtrl( self, wx.ID_ANY, self.filename, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerSaveAs.Add( self.m_textCtrlNameAlternate, 1, wx.ALL, 5 )		
		
		m_comboBoxFormatListChoices = PIC_LIST
		self.m_comboBoxFormatList = wx.ComboBox( self, wx.ID_ANY, m_comboBoxFormatListChoices[6], wx.DefaultPosition, wx.DefaultSize, m_comboBoxFormatListChoices, wx.CB_READONLY )
		bSizerSaveAs.Add( self.m_comboBoxFormatList, 0, wx.ALL, 5 )
		
		
		sbSizerTrans.Add( bSizerSaveAs, 1, wx.EXPAND, 5 )
		
						
		self.m_staticTextPsdNote = wx.StaticText( self, wx.ID_ANY, u"���PSD/PDD�ļ��ϴ󣬾���Ҫ�������ĺ�", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextPsdNote.Wrap( -1 )
		self.m_staticTextPsdNote.Enable( False )
		
		sbSizerTrans.Add( self.m_staticTextPsdNote, 0, wx.ALIGN_CENTER, 5 )
		
		
		bSizerMain.Add( sbSizerTrans, 1, wx.ALL|wx.EXPAND, 5 )
		
				
		self.m_staticline = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizerMain.Add( self.m_staticline, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizerBtnGroup = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizerBtnGroup.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_buttonTry = wx.BitmapButton( self, wx.ID_ANY, play48, wx.DefaultPosition, wx.Size(48, 48), wx.BU_EXACTFIT | wx.NO_BORDER )
		self.m_buttonTry.SetToolTipString( u"���Կ�" )
		bSizerBtnGroup.Add( self.m_buttonTry, 0, wx.ALL, 5 )
		
		self.m_buttonClose = wx.BitmapButton( self, wx.ID_ANY, close48, wx.DefaultPosition, wx.Size(48, 48), wx.BU_EXACTFIT| wx.NO_BORDER )
		self.m_buttonClose.SetToolTipString( u"�ر�" )
		bSizerBtnGroup.Add( self.m_buttonClose, 0, wx.ALL, 5 )
		
		
		bSizerMain.Add( bSizerBtnGroup, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.status = wx.StatusBar(self, -1, name="status")               
		bSizerMain.Add(self.status, 0, wx.EXPAND, 5)
		self.status.Bind(wx.EVT_MOTION, self.motion)
		
		self.SetSizer( bSizerMain )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_buttonPptBrowse.Bind( wx.EVT_BUTTON, self.OnPptBrowse )
		self.m_buttonTry.Bind( wx.EVT_BUTTON, self.OnTry )
		self.m_buttonClose.Bind( wx.EVT_BUTTON, self.OnClose )
	
	def __del__( self ):
		pass
	
	def set_tooltip(self):
		gs_exists = os.path.exists(gs_home)
		tooltip = (u'�����Ŀǰ�����á�ԭ���ǣ�\r\nϵͳ��δ��⵽Ghostģ��' ) if not gs_exists else u"ת��ѡ���PDF��PNG"  
		self.m_bitmapPdf2.SetToolTipString( tooltip )		
		self.m_bitmapSingle2.SetToolTipString( tooltip )
		self.m_checkBoxPdf2Pic.Enable(gs_exists)
	
	def motion(self, event):                
		self.status.SetToolTipString(self.status.GetStatusText())
		event.Skip()	
	
	def OnOpen( self, event ):
		"""��PSD/PDD�ļ�"""
		psdInDialog = wx.FileDialog(self, u"��ѡ��һ��PSD/PDD�ļ�", "", "", u"Photoshop�ļ� (*.psd;*.pdd)|*.psd;*.pdd", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
		psdInDialog.ShowModal()
		psdFile = psdInDialog.GetPath()
		filename = os.path.splitext(os.path.basename(psdFile))[0]
		self.m_textCtrlNameAlternate.SetValue(filename)
		psdInDialog.Destroy()
		self.m_textCtrlPsdPath.SetValue(psdFile)
	
	def OnTogglePicSrc(self, event):
		isPsd = not self.m_radioBtnCurPic.GetValue()
		if isPsd:
			#self.m_checkBoxSaveAs.SetValue(False)
			self.m_textCtrlPsdPath.SetToolTipString(u"PSD/PDD��Photoshopר�õ�ͼ���ļ���ʽ��")
		else: self.m_textCtrlNameAlternate.SetValue(self.filename)
		self.m_buttonOpen.SetToolTipString( isPsd * u'���Photoshop�ļ�')
		self.m_textCtrlPsdPath.Enable(isPsd)
		self.m_buttonOpen.Enable(isPsd)
		event.Skip()
	
	# Virtual event handlers, overide them in your derived class
	def OnPptBrowse( self, event ):
		"""��PPT�ļ�"""
		pptInDialog = wx.FileDialog(self, u"��ѡ��һ��PPT�ļ�", "", "", u"PowerPoint�ļ� (*.ppt; *.pptx)|*.ppt; *.pptx", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
		pptInDialog.ShowModal()
		pptFile = pptInDialog.GetPath()
		pptInDialog.Destroy()
		self.m_textCtrlPptPath.SetValue(pptFile)
		
	# Virtual event handlers, overide them in your derived class
	def OnPdfBrowse( self, event ):
		"""��PDF�ļ�"""
		pdfInDialog = wx.FileDialog(self, u"��ѡ��һ��PDF�ļ�", "", "", u"PDF�ļ� (*.pdf)|*.pdf", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
		pdfInDialog.ShowModal()
		pdfFile = pdfInDialog.GetPath()
		pdfInDialog.Destroy()
		self.m_textCtrlPdfName.SetLabel(pdfFile)
		
	def DoConvert(self, fileIn):
		#ICON convert part
		self.statusmsg = ''		
		self.success = True
		self.task_count = 0
		try:
			# image -> icon part
			size_list = [self.pixelSizeDict[f] for f in self.pixelSizeDict.keys() if f.GetValue()]			
			ImgTemp = None
			if len(size_list) > 0:
				self.task_count += 1
				# check if size is under limit of 3M
				if os.path.getsize(fileIn) > (3 * 1024 * 1024):
					self.statusmsg = u"ת��ICO����: ͼƬ��С������3M��" #.ICON_INFORMATION)
					self.success = False
				else:	
					for size in size_list:
						Img = self.pngResize(size, fileIn)
						if not self.m_checkBoxMultiSave.GetValue():
							sizestr = '_' + str(size)
							self.saveIcon(sizestr, fileIn, Img)
						elif not ImgTemp:
							ImgTemp = Img
						elif ImgTemp:
							ImgTemp.sequence.append(Img)
					if ImgTemp:
						sizestr = ''
						self.saveIcon(sizestr, fileIn, ImgTemp)
			# image <-> PDF part
			if self.m_checkBoxSinglePic.GetValue():
				self.task_count += 1
				page = self.parent.readWandImage(fileIn)						
				fileOut = os.path.join(self.parent.path_base_new, self.m_textCtrlPdfName.GetValue() + '.pdf',)						
				self.parent.writeWandImage(fileOut, page, '.pdf')
			elif self.m_checkBoxMultiPic.GetValue():
				self.task_count += 1
				self.savePdf()
			elif self.m_checkBoxPdf2Pic.GetValue():
				path =  self.m_textCtrlPdfName.GetValue()
				if path and os.path.isfile(path) and path.lower().endswith('.pdf'):
					self.task_count += 1
					res = int(self.m_SplitResBox.GetValue().split()[0])
					self.pdf2png(path, res)
			else: pass # not selected
							
			# PPT to image part
			if self.m_checkBoxPpt.GetValue() and self.m_textCtrlPptPath.GetValue():
				self.task_count += 1
				self.ppt2pics()
				
			# Format trans part
			filename = self.m_textCtrlNameAlternate.GetValue()
			if self.m_checkBoxSaveAs.GetValue() and len(filename) > 0:
				self.task_count += 1
				ext = self.m_comboBoxFormatList.GetValue().encode('cp936')
				if self.m_radioBtnCurPic.GetValue():
					EXT = self.parent.getEXT(ext)

					im = self.parent.readWandImage(fileIn, ext)
					
					fileOut = os.path.join(self.parent.path_base_new, filename + ext)
				else:
					## it's psd file process
					fileIn = self.m_textCtrlPsdPath.GetValue().encode('cp936')
					im = self.parent.readWandImage(fileIn, ext)

					#filename = os.path.splitext(os.path.basename(fileIn))[0]
					fileOut = os.path.join(self.parent.path_base_new, filename + ext)
						
				self.parent.writeWandImage(fileOut, im, ext)
		except Exception, e:
			self.statusmsg += ' ' +  e.message
			self.success = False
	def OnTry( self, event ):
		#clear status msg
		self.status.SetStatusText('')
		# get current pic = self.cur_img
		## send msg to listener to get new base update
		pub.sendMessage("get new path", msg = self.cur_img)
		
		wx.BeginBusyCursor()	
		self.DoConvert(self.cur_img)
		wx.EndBusyCursor()
		
		if self.task_count == 0:
			self.statusmsg = u'û��ת����ѡ�У�����δָ���ļ���/·������'
		elif not self.success:
			if self.m_checkBoxSaveAs.GetValue() and len(self.m_textCtrlPsdPath.GetValue()) == 0:
				self.statusmsg = u'PSD/PDD�ļ���·������Ϊ�ա�' + self.statusmsg	
			else: self.statusmsg = u'ת������:' + self.statusmsg			
		else: 
			self.statusmsg = u'��ϲ���ɹ������ѡ' + str(self.task_count) + u'��ת����'

		self.status.SetStatusText(self.statusmsg)
		self.status.SetToolTipString(self.statusmsg)
		event.Skip()
	
	def OnClose( self, event ):
		self.Show(False)
		event.Skip()
		
	def pngResize(self, size, fileIn):
		if fileIn.lower().endswith('.ico'):
			img = self.parent.readWandImage(fileIn, 'ico')			
			img.resize(size, size)
			return img
		else:
			fil = StringIO()
			img = pImage.open(fileIn).convert("RGBA")
			img = self.parent.pngResize(img)
			img = img.resize((size, size), pImage.ANTIALIAS)
			EXT = os.path.splitext(fileIn)[1]
			
			fil = self.parent.saveToFil(img, EXT)
			
			return Image(blob = fil.getvalue())
	
	def saveIcon(self, sizestr, fileIn, img):
		filename = os.path.basename(fileIn)
		
		fileOut = os.path.join(self.parent.path_base_new, os.path.splitext(filename)[0] + sizestr + '.ico')
		self.parent.writeWandImage(fileOut, img, '.ico')
		
	def savePdf(self):
		fileOut = os.path.join(self.parent.path_base_new, self.m_textCtrlPdfName.GetValue() + '.pdf')
		uuid_fileOut = os.path.join(self.parent.path_base_new, str(uuid.uuid1()) + '.pdf')
		files = self.parent.getPicPaths()		
		with Image() as orig: #create emtpy Image object
			for f in files:
				try:
					page = self.parent.readWandImage(f)
					orig.sequence.append(page)
				except:
					continue
			orig.save(filename= uuid_fileOut)
			# rename to the right name
			if os.path.exists(fileOut):
				os.remove(fileOut)
			os.rename(uuid_fileOut, fileOut)
			
	def pathWithSpace (self, path):
		return '"' + path + '"' if isinstance(path, unicode) else unicode('"' + path + '"', 'cp936')
		
	def pdf2png (self, fileIn, resolution):
		fname = os.path.splitext(os.path.basename(fileIn))[0]
		fileOut = os.path.join(self.parent.path_base_new, fname + '.png')
		convert_path = os.path.join(os.environ['MAGICK_HOME'], 'convert.exe')
		try:
			command = self.pathWithSpace( convert_path )+ ur" -density %s %s %s" % (resolution, self.pathWithSpace(fileIn), self.pathWithSpace(fileOut))
			call (command, shell=True)
		except:
			self.statusmsg = u'��ȡPDF�ļ�ʱ����: ' + fileIn + ';' + self.statusmsg
			
	def RefreshTitle (self):
		self.SetTitle(self.parent.getGuiTitle(u"ͼƬת��"))
		self.cur_img = self.parent.getCurJpg()
		self.filename = os.path.splitext(os.path.basename(self.cur_img))[0]
		# get current image dpi
		self.parent.current_dpi = self.parent.getSettingDPI(self.cur_img)
	
	def GetPdfName(self, fname):
		fileOut = os.path.join(self.parent.path_base_new, fname + '.pdf')
		index = 0
		while os.path.exists(fileOut):
			index = index + 1
			fileOut = os.path.join(self.parent.path_base_new, fname + '(%s).pdf' % (index))
		return os.path.basename(fileOut).rstrip('.pdf')
	
	def OnSinglePic(self, event):
		self.m_textCtrlPdfName.SetValue(self.GetPdfName(self.filename))
		self.togglePdf2Pic()
		event.Skip()
		
	def OnMultiPic(self, event):
		folder = os.path.basename(os.path.dirname(self.cur_img))
		self.m_textCtrlPdfName.SetValue(self.GetPdfName(folder))
		self.togglePdf2Pic()
		event.Skip()
		
	def OnNonePic(self, event):
		#folder = os.path.basename(os.path.dirname(self.cur_img))
		self.m_textCtrlPdfName.SetValue(wx.EmptyString)
		self.togglePdf2Pic()
		event.Skip()
		
	def OnPdf2Pic (self, event):
		self.set_tooltip()
		if self.m_checkBoxPdf2Pic.Enabled:
			self.togglePdf2Pic()
		event.Skip()
	
	def togglePdf2Pic (self):
		flag = self.m_checkBoxPdf2Pic.GetValue()
		self.m_staticSplitRes.Show(flag)
		self.m_SplitResBox.Show(flag)
		self.m_buttonPdfBrowse.Show(flag)
		self.m_staticTextSuf.Show(not flag)
		# reset path
		if flag: self.m_textCtrlPdfName.Clear()
		self.m_textCtrlPdfName.SetEditable(not flag)
		label = u"Ŀ��PDF�ļ�����" if not flag else u"��ѡ��PDFԴ�ļ���"
		self.m_staticTextPdf.SetLabel(label)
		self.Layout()
	def ppt2pics(self):	
		pathToPPT = self.m_textCtrlPptPath.GetValue()
		w,h = re.findall('\d+', self.m_PicSizeBox.GetValue()) # '800','600' e.g.
		ext = self.m_PicFormatBox.GetValue()

		Application = win32com.client.Dispatch("PowerPoint.Application")
		Application.Visible = True

		try:
			Presentation = Application.Presentations.Open(pathToPPT)
			filename = os.path.splitext(os.path.basename(pathToPPT))[0]
			for slide_index in range(len(Presentation.Slides)):
				fileOut = os.path.join(self.parent.path_base_new, filename 
							   + '_Slide' + str(slide_index + 1) + ext.lower())
				Presentation.Slides[slide_index].Export(fileOut, ext[1:], int(w), int(h) ) #default is 720 * 540
			Application.Quit()
		except Exception as e:
			self.statusmsg += ' ' + e.excepinfo[2]
			self.success = False
#if __name__ == '__main__':
#	app = wx.App(False)
#	dlg = PicConverter(None)
#	#dlg.Show()
#	#app.MainLoop()
#	#dlg.ToIcon()
#	#dlg.saveIcon()
#	dlg.pngResize()