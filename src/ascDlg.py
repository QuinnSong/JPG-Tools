# -*- coding: cp936 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
###########################################################################
import wx, os
from img2ascii import image2ascii
from PIL import Image
###########################################################################
## Class AscDlg
###########################################################################

class AscDlg ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition,
				    size = wx.Size( 755,840 ), style = wx.DEFAULT_DIALOG_STYLE | wx.MINIMIZE_BOX ) #|wx.MAXIMIZE_BOX)
		
		self.parent = parent		
		self.SetIcon(self.parent.midi)
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizerMain = wx.BoxSizer( wx.VERTICAL )		
		bSizerAsc = wx.BoxSizer( wx.VERTICAL )
		
		self.m_textCtrlBox = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 745,750 ), wx.TE_MULTILINE|wx.TE_READONLY )
		self.m_textCtrlBox.SetFont( wx.Font( 6, 72, 90, 90, False, "Terminal" ) )		
		bSizerAsc.Add( self.m_textCtrlBox, 0, wx.ALL | wx.BOTTOM | wx.RIGHT, 5 )		
		
		bSizerMain.Add( bSizerAsc, 1, wx.EXPAND, 5 )
		
		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizerMain.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizerButton = wx.BoxSizer( wx.HORIZONTAL )	
		bSizerButton.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_buttonSave = wx.BitmapButton( self, wx.ID_ANY, self.parent.save32_ico, wx.DefaultPosition, wx.Size(48, 48), wx.NO_BORDER|wx.BU_EXACTFIT  )
		bSizerButton.Add( self.m_buttonSave, 0, wx.ALL, 5 )
		self.m_buttonSave.SetToolTipString(u'保存到文件')
		
		self.m_buttonCancel = wx.BitmapButton( self, wx.ID_ANY, self.parent.close32_ico, wx.DefaultPosition, wx.Size(48, 48), wx.NO_BORDER|wx.BU_EXACTFIT  )
		bSizerButton.Add( self.m_buttonCancel, 0, wx.ALL, 5 )
		self.m_buttonCancel.SetToolTipString(u'关闭')		
		
		bSizerMain.Add( bSizerButton, 1, wx.EXPAND, 5 )
		self.SetSizer( bSizerMain )
		self.Layout()
		
		self.Centre( wx.BOTH )
		self.DrawAscii()
		
		# Connect Events
		self.m_buttonSave.Bind( wx.EVT_BUTTON, self.OnSave )
		self.m_buttonCancel.Bind( wx.EVT_BUTTON, self.OnCancel )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnSave( self, event ):
		ascii_txt = self.m_textCtrlBox.GetValue()
		if len(ascii_txt) > 0:
			saveFileDialog = wx.FileDialog(self, "导出ASCII图形到文件", "", self.curJpg + ".txt", "文本文件 (*.txt)|*.txt", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
			saveFileDialog.ShowModal()
			txtFile = saveFileDialog.GetPath()
			saveFileDialog.Destroy()
			if  len(txtFile) > 0:
				# write to file
				with open(txtFile, 'w') as fileout:
					fileout.write(ascii_txt) #.encode('cp936'))
					wx.MessageBox(u'请用9号以下的等宽字体:\r\n如 Consolas，Courier New，Terminal\r\n在记事本中查看。', "恭喜！保存成功", wx.OK | wx.ICON_INFORMATION)
					os.startfile(txtFile)
		event.Skip()
	
	def AutoSave(self, filepath, newpath):
		# get ascii text
		im = Image.open(filepath)
		ascii = image2ascii(im)
		with open(newpath, 'w') as fileout:
			fileout.write(ascii) 
	
	def OnCancel( self, event ):
		self.Show(False)
		event.Skip()
		
	def DrawAscii(self):
		if not self.parent.im_preview:
			self.curJpg = self.parent.picPaths[self.parent.currentPicture]
			#try:
			#	title = ur"图片转ASCII码 (文件：" + os.path.basename(self.curJpg) + ur")" 
			#except:
			#	title = ur"图片转ASCII码 (文件：" + os.path.basename(self.curJpg.decode('cp936')) + ur")" 			
			im = Image.open(self.curJpg)
		else:
			im = self.parent.im_preview
		# set title
		self.SetTitle(self.parent.getGuiTitle(u"图片转ASCII码"))
		# do ascii conversion
		ascii = image2ascii(im)
		# update the text box
		self.m_textCtrlBox.SetValue(ascii)
	

