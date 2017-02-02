# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.richtext
from wx.lib.pubsub import pub
from TestSync import theLoop
import time
from threading import Thread
###########################################################################
## Class MyFrame1
###########################################################################

class MyAPIFrame ( wx.Frame ):
	
	def __init__( self ):
		wx.Frame.__init__ ( self, None, id = wx.ID_ANY, title = u"Hessian API Testing with Python", pos = wx.DefaultPosition, size = wx.Size( 821,777 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter1 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )
		
		self.m_panel12 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_notebook2 = wx.Notebook( self.m_panel12, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel2 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.Size( 660,-1 ), wx.TAB_TRAVERSAL )
		self.m_notebook2.AddPage( self.m_panel2, u"Set", False )
		self.m_panel3 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel3, wx.ID_ANY, u"Test Case" ), wx.VERTICAL )
		
		m_checkListCasesChoices = ['Test Synchronization']
		self.m_checkListCases = wx.CheckListBox( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_checkListCasesChoices, 0 )
		sbSizer4.Add( self.m_checkListCases, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel3.SetSizer( sbSizer4 )
		self.m_panel3.Layout()
		sbSizer4.Fit( self.m_panel3 )
		self.m_notebook2.AddPage( self.m_panel3, u"Synchronization", True )
		self.m_panel4 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_notebook2.AddPage( self.m_panel4, u"a page", False )
		self.m_panel5 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_notebook2.AddPage( self.m_panel5, u"a page", False )
		self.m_panel6 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_notebook2.AddPage( self.m_panel6, u"a page", False )
		self.m_panel7 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_notebook2.AddPage( self.m_panel7, u"a page", False )
		self.m_panel8 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_notebook2.AddPage( self.m_panel8, u"a page", False )
		self.m_panel9 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_notebook2.AddPage( self.m_panel9, u"a page", False )
		self.m_panel10 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_notebook2.AddPage( self.m_panel10, u"a page", False )
		self.m_panel11 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_notebook2.AddPage( self.m_panel11, u"a page", False )
		
		bSizer5.Add( self.m_notebook2, 1, wx.EXPAND |wx.ALL, 5 )
		
		bSizerBtnAct = wx.BoxSizer( wx.VERTICAL )
		
		self.m_buttonExport = wx.Button( self.m_panel12, wx.ID_ANY, u"    EXPORT", wx.DefaultPosition, wx.Size( -1,50 ), 0 )
		bSizerBtnAct.Add( self.m_buttonExport, 0, wx.ALIGN_CENTER|wx.TOP, 25 )
		
		
		bSizerBtnAct.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_buttonRunSelected = wx.Button( self.m_panel12, wx.ID_ANY, u"    RUN \nSELECTED", wx.DefaultPosition, wx.Size( -1,50 ), 0 )
		bSizerBtnAct.Add( self.m_buttonRunSelected, 0, wx.ALIGN_CENTER|wx.ALL|wx.BOTTOM, 5 )
		
		self.m_buttonRunAll = wx.Button( self.m_panel12, wx.ID_ANY, u"RUN \nALL", wx.DefaultPosition, wx.Size( -1,50 ), 0 )
		bSizerBtnAct.Add( self.m_buttonRunAll, 0, wx.ALIGN_CENTER|wx.BOTTOM|wx.TOP, 5 )
		
		
		bSizer5.Add( bSizerBtnAct, 1, wx.EXPAND|wx.BOTTOM, 5 )
		
		
		bSizer2.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		
		self.m_panel12.SetSizer( bSizer2 )
		self.m_panel12.Layout()
		bSizer2.Fit( self.m_panel12 )
		self.m_panel13 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel13, wx.ID_ANY, u"Event Log Window" ), wx.VERTICAL )
		
		self.m_richTextLogWin = wx.richtext.RichTextCtrl( self.m_panel13, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		sbSizer2.Add( self.m_richTextLogWin, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizer4.Add( sbSizer2, 1, wx.EXPAND, 5 )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel13, wx.ID_ANY, u"Compare Result" ), wx.VERTICAL )
		
		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1 = wx.StaticText( self.m_panel13, wx.ID_ANY, u"OUTPUT:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer14.Add( self.m_staticText1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_textCtrl1 = wx.TextCtrl( self.m_panel13, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		bSizer14.Add( self.m_textCtrl1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		
		sbSizer3.Add( bSizer14, 1, wx.EXPAND, 5 )
		
		bSizer15 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText3 = wx.StaticText( self.m_panel13, wx.ID_ANY, u"EXPECT:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer15.Add( self.m_staticText3, 0, wx.ALL, 5 )
		
		self.m_textCtrl2 = wx.TextCtrl( self.m_panel13, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		bSizer15.Add( self.m_textCtrl2, 0, wx.ALL, 5 )
		
		
		sbSizer3.Add( bSizer15, 1, wx.EXPAND, 5 )
		
		
		bSizer9.Add( sbSizer3, 1, wx.EXPAND, 5 )
		
		bSizer13 = wx.BoxSizer( wx.VERTICAL )
		
		toolbar = self.CreateToolBar()
		toolbar.SetToolBitmapSize((16,16))
		
		ok_ico = wx.ArtProvider.GetBitmap(wx.ART_TICK_MARK, wx.ART_TOOLBAR, (16,16))
		error_ico = wx.ArtProvider.GetBitmap(wx.ART_ERROR, wx.ART_TOOLBAR, (16,16))
		self.m_bitmap1 = wx.StaticBitmap( self.m_panel13, wx.ID_ANY, ok_ico, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer13.Add( self.m_bitmap1, 1, 0, 5 )
		self.m_bitmap1.Show(False)
		
		bSizer9.Add( bSizer13, 1, wx.EXPAND, 5 )
		
		
		bSizer4.Add( bSizer9, 1, wx.EXPAND, 5 )
		
		self.m_staticline1 = wx.StaticLine( self.m_panel13, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer4.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer12.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_buttonHelp = wx.Button( self.m_panel13, wx.ID_ANY, u"?", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.m_buttonHelp, 0, wx.ALL, 5 )
		
		self.m_button12 = wx.Button( self.m_panel13, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.m_button12, 0, wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer12, 1, wx.EXPAND|wx.BOTTOM|wx.RIGHT, 5 )
		
		
		bSizer3.Add( bSizer4, 1, wx.EXPAND, 5 )
		
		
		self.m_panel13.SetSizer( bSizer3 )
		self.m_panel13.Layout()
		bSizer3.Fit( self.m_panel13 )
		self.m_splitter1.SplitHorizontally( self.m_panel12, self.m_panel13, 288 )
		bSizer1.Add( self.m_splitter1, 1, wx.EXPAND, 5 )
		
		pub.subscribe(self.update_log, ('update'))
		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_statusBar1 = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_buttonRunSelected.Bind( wx.EVT_BUTTON, self.onRunSelected )
		self.m_buttonRunAll.Bind( wx.EVT_BUTTON, self.onRunAll )
		self.m_buttonHelp.Bind( wx.EVT_BUTTON, self.onHelp )
		self.m_button12.Bind( wx.EVT_BUTTON, self.onClose )
		
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onRunSelected( self, event ):
		RunThread()
		self.m_statusBar1.SetStatusText('Test Case running...')
		btn = event.GetEventObject()
		btn.Disable()
		
	def update_log(self, msg = None):
		if isinstance(msg, str):
			self.m_richTextLogWin.AppendText(msg + '\n')
		else:
			self.m_statusBar1.SetStatusText('Test Case finished.')
			self.m_buttonRunSelected.Enable()
			self.m_bitmap1.Show()
	def onRunAll( self, event ):
		event.Skip()
	
	def onHelp( self, event ):
		event.Skip()
	
	def onClose( self, event ):
		event.Skip()
	
	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 288 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )

class RunThread(Thread):
    """Test Worker Thread Class."""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.start()    # start the thread
 
    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        for i in range(10):
            time.sleep(3)
            pub.sendMessage("update", msg = time.ctime())
        pub.sendMessage("update", msg = None)

#----------------------------------------------------------------------
if __name__ == '__main__':
        app = wx.App()
        frame = MyAPIFrame()
        frame.Show()
        app.MainLoop()
