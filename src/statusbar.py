# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

###########################################################################
## Class StatusBar
###########################################################################

class StatusBar ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_statusBar1 = self.CreateStatusBar( 3, wx.ST_SIZEGRIP, wx.ID_ANY )
		print help(self.m_statusBar1)
		#barPanel1 = self.m_statusBar1.GetField(1)
		#barPanel2 = self.m_statusBar1.GetField(2)
		#barPanel3 = self.m_statusBar1.GetField(3)
		#print help(barPanel1)
		self.m_statusBar1.SetStatusText("field1", 0)
		self.m_statusBar1.SetStatusText("field2", 1)
		self.m_statusBar1.SetStatusText("field3", 2)
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass

if __name__ == '__main__':
	app = wx.App(False)
	frame = StatusBar(None)
	frame.Show()
	app.MainLoop()