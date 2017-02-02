# -*- coding: cp936 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Feb 26 2014)
## http://www.wxformbuilder.org/
###########################################################################
import wx
#"memory leak of type 'wxPyXmlSubclassFactory *', no destructor found” error
#import wx.xrc
import wx.richtext
from pyexiv2 import ImageMetadata
import os, sys
import iconfile

###########################################################################
## Class CommentDialog
###########################################################################

class CommentDialog ( wx.Dialog ):
	"""The Dialog to view and edit JPEG comment"""
	def __init__( self, parent ):
				
		
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = "", pos = wx.DefaultPosition,
				    size = wx.Size( 450,532 ), style = wx.DEFAULT_DIALOG_STYLE | wx.MINIMIZE_BOX )
		
		self.parent = parent		
		self.curJpg = self.parent.picPaths[self.parent.currentPicture]
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )		
		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"当前备注：" ), wx.VERTICAL )
		
		self.m_curRichText = wx.richtext.RichTextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,170 ), wx.VSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		self.m_curRichText.SetToolTipString( u"当前备注" )
		self.m_curRichText.SetEditable(False) 
		self.m_curRichText.SetBackgroundColour( wx.Colour( 176, 176, 176 ) )
		
		sbSizer1.Add( self.m_curRichText, 1, wx.EXPAND |wx.ALL, 5 )
		bSizer1.Add( sbSizer1, 1, wx.ALL | wx.EXPAND, 5 )
		
		# init icons
		toolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL | wx.NO_BORDER)
		toolbar.SetToolBitmapSize((16,16))
		del_ico = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, (16,16))		
		
		save_ico = self.parent.save_ico 
		copy_ico = iconfile.getCopyBmp.GetBitmap()
		import_ico = iconfile.getImportBmp.GetBitmap()
		export_ico = iconfile.getExportBmp.GetBitmap()
		close_ico = self.parent.close_ico #iconfile.getCloseBmp.GetBitmap()		
		self.SetIcon(self.parent.midi) # set title icon
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"新备注：" ), wx.VERTICAL )		
		self.m_newRichText = wx.richtext.RichTextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,160 ), 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )		
		self.m_newRichText.SetToolTipString( u"编辑或添加备注" )		
		sbSizer2.Add( self.m_newRichText, 1, wx.EXPAND|wx.ALL, 5 )              
		
		bSizer1.Add( sbSizer2, 1, wx.ALL | wx.EXPAND, 5 )
		
		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		btnSizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_clearBtn = wx.BitmapButton( self, wx.ID_ANY, del_ico, wx.DefaultPosition, wx.Size(24,24), wx.NO_BORDER | wx.BU_EXACTFIT )		
		self.m_clearBtn.SetToolTipString( u"清除" )		
		btnSizer.Add( self.m_clearBtn, 0, wx.RIGHT, 150 )		
		
		self.m_updateBtn = wx.BitmapButton( self, wx.ID_ANY, save_ico, wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER | wx.BU_EXACTFIT  ) #48*48
		self.m_updateBtn.SetToolTipString( u"更新当前备注" )          
		btnSizer.Add( self.m_updateBtn, 0, wx.RIGHT, 5 )
		
		self.m_import = wx.BitmapButton( self, wx.ID_ANY, import_ico, wx.DefaultPosition, wx.Size(48,48), wx.NO_BORDER | wx.BU_EXACTFIT  )
		self.m_import.SetToolTipString( u"从ANSI文本文件导入备注" )
		btnSizer.Add( self.m_import, 0, wx.RIGHT, 5 )
		
		self.m_copy = wx.BitmapButton( self, wx.ID_ANY, copy_ico, wx.DefaultPosition, wx.Size(48,48), wx.NO_BORDER | wx.BU_EXACTFIT  )
		self.m_copy.SetToolTipString( u"复制当前备注" )
		btnSizer.Add( self.m_copy, 0, wx.RIGHT, 5 )		
		
		self.m_export = wx.BitmapButton( self, wx.ID_ANY, export_ico, wx.DefaultPosition, wx.Size(48,48), wx.NO_BORDER | wx.BU_EXACTFIT  )
		self.m_export.SetToolTipString( u"导出当前备注到文件" )                
		btnSizer.Add( self.m_export, 0, wx.RIGHT, 5 )
		
		self.m_cancel = wx.BitmapButton( self, wx.ID_ANY, close_ico, wx.DefaultPosition, wx.Size(48,48), wx.NO_BORDER | wx.BU_EXACTFIT  )
		self.m_cancel.SetToolTipString( u"取消编辑并退出" )		
		btnSizer.Add( self.m_cancel, 0, wx.RIGHT, 5 )
		
		
		bSizer1.Add( btnSizer, 1, wx.CENTER | wx.ALIGN_RIGHT, 5 )
		
		self.status = wx.StatusBar(self, -1, name="status")               
		bSizer1.Add(self.status, 0, wx.EXPAND, 5)
		
		self.loadCurrentJpg(self.curJpg)
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_newRichText.SetFocus()
		self.Centre( wx.BOTH )
		self.status.SetStatusText(u'注意：只有JPG图片支持此项功能！')
		
		# Connect Events
		self.m_newRichText.Bind( wx.EVT_KEY_UP, self.onKeyUp )
		self.m_updateBtn.Bind( wx.EVT_BUTTON, self.OnEdit )
		self.m_import.Bind( wx.EVT_BUTTON, self.OnImport )
		self.m_copy.Bind( wx.EVT_BUTTON, self.OnCopy )
		self.m_export.Bind( wx.EVT_BUTTON, self.OnExport )
		self.m_cancel.Bind( wx.EVT_BUTTON, self.OnCancel )
		self.m_clearBtn.Bind( wx.EVT_BUTTON, self.onClear )
		self.m_clearBtn.Show(False) # hide it first	

	#def onActivate (self, event):           
	#	self.pasteFromClipboard()

	# Virtual event handlers, overide them in your derived class
	def onKeyUp( self, event ):		
		self.toggleClearBtn()
	def toggleClearBtn(self):
		new_comment =  self.m_newRichText.GetValue().encode("cp936")		
		self.m_clearBtn.Show(len(new_comment) > 0)
		
	def onClear(self, event):
		"""Cear the comment on button click"""
		self.m_newRichText.Clear()
		self.m_clearBtn.Show(False)
		event.Skip()
	
	def loadCurrentJpg(self, curJpg):
		"""Load comment of current jpg file"""		
		try:
			comment = self.getComment(curJpg)
			self.m_curRichText.SetValue(comment.decode('cp936'))
		except:
			pass # Fails due to unknown encoding	
		
		#try:
		#	title = u"添加或编辑备注 " + ur"(文件：" + os.path.basename(curJpg) + ur")"
		#except:
		#	title = u"添加或编辑备注 " + ur"(文件：" + os.path.basename(curJpg.decode('cp936')) + ur")"
		self.SetTitle(self.parent.getGuiTitle(u"添加或编辑备注" ))
	
	def OnEdit( self, event ):
		"""Update with new comment"""
		new_comment =  self.m_newRichText.GetValue().encode("cp936")
		if self.setComment(self.curJpg, new_comment):
			self.status.SetStatusText(u'备注更新完毕！')
			# set display with new value
			self.m_curRichText.SetValue(new_comment.decode('cp936'))
		event.Skip()
		
	def OnImport (self, event):
		"""Import comment from file"""
		importDialog = wx.FileDialog(self, "从文件导入备注", "", "", "文本文件 (*.txt)|*.txt", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
		importDialog.ShowModal()
		txtFile = importDialog.GetPath()
		importDialog.Destroy()
		if len(txtFile) > 0:
			# read comments from txt file( must be in ASCII format)
			try:
				with open(txtFile, 'rb') as filein:
					comment = filein.read()
					self.m_newRichText.SetValue(comment)
					self.status.SetStatusText(u'备注导入成功！')
					self.toggleClearBtn()
			except:
				pass
	def OnCopy (self, event):
		"""Copy content from current comment"""
		comment = self.m_curRichText.GetValue()
		if len(comment) > 0:
			self.m_newRichText.SetValue(comment)
			# write data to clipboard
			clipdata = wx.TextDataObject()
			clipdata.SetText(comment)
			wx.TheClipboard.Open()
			wx.TheClipboard.SetData(clipdata)
			wx.TheClipboard.Close()
			self.status.SetStatusText(u'当前备注已复制！')
			self.toggleClearBtn()
	#def pasteFromClipboard (self):                  
	#	if not self.tried and not wx.TheClipboard.IsOpened() :  # may crash, otherwise                  
	#		do = wx.TextDataObject()
	#		wx.TheClipboard.Open()
	#		success = wx.TheClipboard.GetData(do)
	#		wx.TheClipboard.Close()                 
	#		if success:
	#		    self.m_newRichText.SetValue(do.GetText().encode('cp936'))
	#		else:
	#		    #self.text.SetValue("No data in the clipboard in the required format")
	#		    pass
	#		self.tried = True
	#	else:
	#		self.tried = False # reset flag	
	
	def OnExport( self, event ):
		"""Export current comment to a file"""
		comment = self.m_curRichText.GetValue().replace('\n', '\r\n')
		if len(comment) > 0:
			saveFileDialog = wx.FileDialog(self, "导出备注到文件", "", "", "文本文件 (*.txt)|*.txt", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
			saveFileDialog.ShowModal()
			txtFile = saveFileDialog.GetPath()
			saveFileDialog.Destroy()
			if  len(txtFile) > 0:
				# write to file
				with open(txtFile, 'wb') as fileout:
					fileout.write(comment.encode('cp936'))					
					self.status.SetStatusText(u'备注导出成功！')
	
	def OnCancel( self, event ):
		"""On exit event"""
		self.Hide()		
		event.Skip()
		
	def getComment(self, filePath):
		"""Function to retrieve comment from JPEG file"""
		"""
		Get comment info from the image specified
		filePath: full path of the image file 
		"""
		metadata = ImageMetadata(filePath)
		metadata.read()
		return metadata.comment
		
	def setComment(self, filePath, comment):
		"""
		Set comment info to the image specified
		filePath: full path of the image file 
		comment: contains comment tag info
		"""
		metadata = ImageMetadata(filePath)
		metadata.read()
		try:
		    metadata.comment = comment
		    metadata.write()
		    return True
		except Exception as e:
		    return False