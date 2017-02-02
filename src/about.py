# -*- coding: cp936 -*- 
import wx
import iconfile
#from time import sleep
###########################################################################
## Class MyAboutDialog
## Credit to Mike for his "Doing a Fade-in with wxPython"
###########################################################################

class MyAboutDialog ( wx.Dialog ):	
	def __init__( self, parent ):		
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"关于", pos = wx.DefaultPosition, size = wx.Size( 405,315 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		bSizerAboutMain = wx.BoxSizer( wx.VERTICAL )
		
		bSizerLogo = wx.BoxSizer( wx.VERTICAL )
		
		logo = iconfile.getLogoPng.GetBitmap()
		self.m_bitmap2 = wx.StaticBitmap( self, wx.ID_ANY, logo, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerLogo.Add( self.m_bitmap2, 0, wx.ALL|wx.EXPAND, 5 )
		bSizerAboutMain.Add( bSizerLogo, 1, wx.EXPAND, 5 )
		
		bSizerDescription = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticTextProduct = wx.StaticText( self, wx.ID_ANY, u"软件名称：JPG图片工具", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextProduct.Wrap( -1 )
		bSizerDescription.Add( self.m_staticTextProduct, 0, wx.ALL, 5 )
		
		self.m_staticTextVersion = wx.StaticText( self, wx.ID_ANY, u"软件版本：0.93", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextVersion.Wrap( -1 )
		bSizerDescription.Add( self.m_staticTextVersion, 0, wx.ALL, 5 )
		
		self.m_staticTextAuthor = wx.StaticText( self, wx.ID_ANY, u"联系作者：Quinn Song | 47396280（QQ）", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextAuthor.Wrap( -1 )
		bSizerDescription.Add( self.m_staticTextAuthor, 0, wx.ALL, 5 )
		
		
		bSizerAboutMain.Add( bSizerDescription, 1, wx.ALIGN_CENTER, 5 )
		bSizerAboutBottom = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticline3 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizerAboutBottom.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_buttonOK = wx.Button( self, wx.ID_ANY, u"确定(&O)", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerAboutBottom.Add( self.m_buttonOK, 0, wx.ALIGN_CENTER|wx.ALL, 5 )		
		
		bSizerAboutMain.Add( bSizerAboutBottom, 1, wx.EXPAND, 5 )
		self.SetSizer( bSizerAboutMain )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_buttonOK.Bind( wx.EVT_BUTTON, self.OnOK )
		
		#------------Fade in tech-------------
		self.amount = 5
		self.delta = 5
		self.SetTransparent(self.amount) 
		## ------- Fader Timer -------- ##
		self.timer = wx.Timer(self, wx.ID_ANY)
		self.timer.Start(60) #60)
		self.Bind(wx.EVT_TIMER, self.AlphaCycle)
		## ---------------------------- ##
	
	def __del__( self ):
		pass	
	
	# Virtual event handlers, overide them in your derived class
	def OnOK( self, event ):
		self.Bind(wx.EVT_TIMER, self.AlphaCycle)
		#self.Close()
		event.Skip()
	
	def AlphaCycle(self, event):
		self.amount += self.delta
		if self.amount >= 255:			
			self.delta = - self.delta
			self.amount = 255
			self.Unbind(wx.EVT_TIMER) #, self.AlphaCycle)
		if self.amount <= 0:
			self.amount = 0
		self.SetTransparent(self.amount)

