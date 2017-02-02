# -*- coding: utf-8 -*-

import wx
import iconfile
from qr_code import qrCode
import os
from Tkinter import Tk

WILDCARD = u"JPEG 图片 (*.jpg)|*.jpg|BMP 图片 (*.bmp)|*.bmp|PNG 图片 (*.png)|*.png|" +\
		u"GIF 图片 (*.gif)|*.gif|TIF 图片 (*.tif; *.tiff)|*.tif; *.tiff" 

###########################################################################
## Class MyQRDialog
###########################################################################

class MyQRDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"根据字符串生成二维码", pos = wx.DefaultPosition, size = wx.Size( 440,360 ), style = wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.RESIZE_BORDER |wx.MINIMIZE_BOX )
		self.parent = parent
		self.SetSizeHintsSz( wx.Size( 430,270 ), wx.DefaultSize )
		midi = iconfile.getIcon.GetIcon()
		self.SetIcon(midi)	
		
		bSizerMain = wx.BoxSizer( wx.VERTICAL )
		
		sbSizerString = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"请输入字符串(最多300个字符)" ), wx.VERTICAL )
		
		self.m_textCtrlBody = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		sbSizerString.Add( self.m_textCtrlBody, 3, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticTextTip = wx.StaticText( self, wx.ID_ANY, u"二维码估计尺寸: 115x115", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextTip.Wrap( -1 )
		#self.m_staticTextTip.Enable( False )
		
		sbSizerString.Add( self.m_staticTextTip, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		
		bSizerMain.Add( sbSizerString, 3, wx.EXPAND, 5 )
		
		sbSizerSetting = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"参数设置" ), wx.HORIZONTAL )
		
		self.m_staticTextSize = wx.StaticText( self, wx.ID_ANY, u"大小控制", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextSize.Wrap( -1 )
		sbSizerSetting.Add( self.m_staticTextSize, 0, wx.ALL, 5 )
		
		self.m_spinCtrlSize = wx.SpinCtrl( self, wx.ID_ANY, "5", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 40, 5 )
		sbSizerSetting.Add( self.m_spinCtrlSize, 0, wx.ALL, 5 )
		
		self.m_staticTextBorder = wx.StaticText( self, wx.ID_ANY, u"边缘控制", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextBorder.Wrap( -1 )
		sbSizerSetting.Add( self.m_staticTextBorder, 0, wx.ALL, 5 )
		
		self.m_spinCtrlBorder = wx.SpinCtrl( self, wx.ID_ANY, '1', wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 20, 1 )
		sbSizerSetting.Add( self.m_spinCtrlBorder, 0, wx.ALL, 5 )
		
		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		sbSizerSetting.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizerMain.Add( sbSizerSetting, 1, wx.EXPAND, 5 )
		
		bSizerButton = wx.BoxSizer( wx.HORIZONTAL )
		
		self.preview_ico = iconfile.previewIcon.GetBitmap()
		self.m_buttonPreview = wx.BitmapButton( self, wx.ID_ANY, self.preview_ico, wx.DefaultPosition, wx.Size(48, 48), wx.NO_BORDER |wx.BU_EXACTFIT  )
		bSizerButton.Add( self.m_buttonPreview, 0, wx.ALL|wx.RIGHT, 5 )
		self.m_buttonPreview.SetToolTipString(u'预览')
		
		self.save32_ico = iconfile.save32Icon.GetBitmap()
		self.m_buttonSave = wx.BitmapButton( self, wx.ID_ANY, self.save32_ico, wx.DefaultPosition, wx.Size(48, 48), wx.NO_BORDER|wx.BU_EXACTFIT  )
		bSizerButton.Add( self.m_buttonSave, 0, wx.ALL|wx.RIGHT, 5 )
		self.m_buttonSave.SetToolTipString(u'生成并保存')
		
		self.close32_ico = iconfile.closeIcon.GetBitmap()
		self.m_buttonClose = wx.BitmapButton( self, wx.ID_ANY, self.close32_ico, wx.DefaultPosition, wx.Size(48, 48), wx.NO_BORDER|wx.BU_EXACTFIT  )
		bSizerButton.Add( self.m_buttonClose, 0, wx.ALL|wx.RIGHT, 5 )
		self.m_buttonClose.SetToolTipString(u'关闭')		
		
		bSizerMain.Add( bSizerButton, 1, wx.ALIGN_RIGHT, 5 )
		self.status = wx.StatusBar(self, -1, name="status")
		self.status.SetFieldsCount(2)
		self.status.SetStatusText(u'当前字符总计: 0', number = 1)
		self.status.SetStatusWidths([-1, 120])
		self.body_len = 0
		bSizerMain.Add(self.status, 0, wx.EXPAND, 5)
		
		self.SetSizer( bSizerMain )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_spinCtrlSize.Bind( wx.EVT_SPINCTRL, self.OnSizeChanged )
		self.m_spinCtrlBorder.Bind( wx.EVT_SPINCTRL, self.OnSizeChanged )
		self.m_buttonPreview.Bind( wx.EVT_BUTTON, self.OnPreview )
		self.m_buttonSave.Bind( wx.EVT_BUTTON, self.OnSave )
		self.m_buttonClose.Bind( wx.EVT_BUTTON, self.OnClose )
		self.m_textCtrlBody.Bind( wx.EVT_TEXT, self.OnTextChange)
		self.Bind(wx.EVT_ACTIVATE, self.onActive)
		
	
	def __del__( self ):
		pass
	
	def SetTitle(self, filename = None):
		if filename: self.Title = u'根据字符串生成二维码' + u'(文件：%s)' % (filename)
		else: self.Title = u'根据字符串生成二维码'
	
	def OnTextChange(self, event):
		self.body_len = len(self.m_textCtrlBody.GetValue())
		self.status.SetStatusText(u'当前字符总计: ' + str(self.body_len), number = 1)
		self.checkLength(self.body_len)
	
	def onActive(self, event):
		""" get clipboard text if available"""
		try:
			data = Tk().clipboard_get()			
			if isinstance(data, str) and self.m_textCtrlBody.GetValue() == "": self.m_textCtrlBody.SetValue(data)
		except: pass
		#event.Skip()
	
	# Virtual event handlers, overide them in your derived class
	def OnSizeChanged( self, event ):
		
		size = self.m_spinCtrlSize.GetValue()
		border = self.m_spinCtrlBorder.GetValue() * size * 2
		self.m_staticTextTip.SetLabelText( u"二维码估计尺寸: " + str(size * 21 + border) + str("x") +str(size * 21 + border))
				
		event.Skip()
	
	def getQR (self):
			box_size = self.m_spinCtrlSize.GetValue()
			border = self.m_spinCtrlBorder.GetValue()			
			return qrCode(self.m_textCtrlBody.GetValue(), box_size = box_size, border = border )			
	
	def checkLength(self, length):
		if length == 0:
			self.status.SetStatusText(u'亲，请输入二维码字符串。', number = 0)
			return False
		elif length > 300:
			self.status.SetStatusText(u'亲，字符串超出了300个字符的限制。', number = 0)
			return False
		else:
			self.status.SetStatusText(u'', number = 0)
			return True

	def OnPreview( self, event):
		
		if self.checkLength(self.body_len):
			self.status.SetStatusText(u'正在生成二维码...', number = 0)
			""" Preview a QR code"""
			self.m_buttonPreview.Enable(False)
			im = self.getQR()
			if im:
				im = im.convert("RGBA")
				self.status.SetStatusText("", number = 0)        
				self.parent.panel.imgPreview(im, '.PNG', isQR = True)
				self.SetTitle()
				self.status.SetStatusText(u"", number = 0)
				self.m_staticTextTip.SetLabelText( u"二维码实际尺寸: " + str(im.size[0]) + str("x") +str(im.size[1]))
			else:
				self.status.SetStatusText(u'二维码生成失败！', number = 0)
				#self.m_textCtrlBody.SetFocus()
			self.m_buttonPreview.Enable(True)   
		event.Skip()
	
	def OnSave( self, event ):
		if self.checkLength(self.body_len):
			self.status.SetStatusText(u'正在生成二维码...', number = 0)
			"""Save to image"""
			self.m_buttonPreview.Enable(False)
			im = self.getQR()
			if im:
				im = im.convert("RGBA")
				dlg = wx.FileDialog(self, u"请指定保存路径", self.parent.panel.save_dir, u"未命名", WILDCARD, wx.SAVE|wx.OVERWRITE_PROMPT)
				result = dlg.ShowModal()
				fileIn = dlg.GetPath()
				dlg.Destroy()
				
				if result == wx.ID_OK:          #Save button was pressed
						ext = os.path.splitext(fileIn)[1]					
						self.parent.panel.saveToFile(im, ext, fileIn)					
						self.status.SetStatusText(u"恭喜！二维码已生成并保存至："  + fileIn, number = 0)
						# load the saved file
						from image_viewer import pub
						pub.sendMessage("update images", msg = [ fileIn ])
				else:
					self.status.SetStatusText(u"", number = 0)
			else:
				self.status.SetStatusText(u'二维码生成失败！建议联系作者。', number = 0)				
			self.m_buttonPreview.Enable(True)
		event.Skip()
	
	def OnClose( self, event ):
		self.Show(False)
		event.Skip()