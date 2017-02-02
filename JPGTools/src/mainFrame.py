#coding=gbk
#########################
#��������:2009��4��19��\n\n�汾:0.9
#########################

import wx
import wx.lib.filebrowsebutton
import _winreg,os,re
from PIL import Image, ImageDraw, ImageFont


def create(parent):
    return mainFrame(parent)

[wxID_MAINFRAME, wxID_MAINFRAMECENTER, wxID_MAINFRAMECENTERBOTTOM, 
 wxID_MAINFRAMECENTERLEFT, wxID_MAINFRAMECENTERRIGHT, wxID_MAINFRAMECENTERTOP, 
 wxID_MAINFRAMECHOOSECOLOUR, wxID_MAINFRAMECHOOSEFONT, 
 wxID_MAINFRAMELEFTBOTTOM, wxID_MAINFRAMELEFTTOP, wxID_MAINFRAMEMAINSTATICBOX, 
 wxID_MAINFRAMEMAKETRANS, wxID_MAINFRAMEPANEL1, wxID_MAINFRAMEPICKCOLOUR, 
 wxID_MAINFRAMEPICKFONT, wxID_MAINFRAMEPICKTRANS, wxID_MAINFRAMERIGHTBOTTOM, 
 wxID_MAINFRAMERIGHTTOP, wxID_MAINFRAMESAVETOFOLDER, wxID_MAINFRAMESOFTNAME, 
 wxID_MAINFRAMESOURCEFOLDER, wxID_MAINFRAMESTARTMAKE, 
 wxID_MAINFRAMESTATICLINE1, wxID_MAINFRAMESTATUSBAR1, 
 wxID_MAINFRAMEUSEDEFAULT, wxID_MAINFRAMEVIEWDEMO, wxID_MAINFRAMEWANTTEXT, 
 wxID_MAINFRAMEWATERFONT, wxID_MAINFRAMEWATERPOSITION, 
] = [wx.NewId() for _init_ctrls in range(29)]

[wxID_MAINFRAMEFILEITEMS1, 
] = [wx.NewId() for _init_coll_File_Items in range(1)]

[wxID_MAINFRAMEHELPITEMS0] = [wx.NewId() for _init_coll_Help_Items in range(1)]

class mainFrame(wx.Frame):
    
    def _init_coll_myMenuBar_Menus(self, parent):
        '''��˵�����Ӵ���˵�'''
        parent.Append(menu=self.File, title='�ļ�(&F)')
        parent.Append(menu=self.Help, title='����(&H)')

    def _init_coll_File_Items(self, parent):
        '''�����ļ��˵����Ӳ˵���,�����¼�'''
        parent.Append(help='�˳�����', id=wxID_MAINFRAMEFILEITEMS1,
              kind=wx.ITEM_NORMAL, text='�˳�')
        self.Bind(wx.EVT_MENU, self.OnFileItems1Menu,
              id=wxID_MAINFRAMEFILEITEMS1)

    def _init_coll_Help_Items(self, parent):
        '''���������˵����Ӳ˵���,�����¼�'''
        parent.Append(help='���ڴ˹���', id=wxID_MAINFRAMEHELPITEMS0,
              kind=wx.ITEM_NORMAL, text='����')
        self.Bind(wx.EVT_MENU, self.OnHelpItems0Menu,
              id=wxID_MAINFRAMEHELPITEMS0)

    def _init_utils(self):
        '''�˵�����ʼ��'''
        self.myMenuBar = wx.MenuBar()
        self.myMenuBar.SetWindowStyleFlag(1)
        self.myMenuBar.SetHelpText('')

        self.File = wx.Menu(title='')
        self.File.SetEvtHandlerEnabled(True)

        self.Help = wx.Menu(title='')

        self._init_coll_myMenuBar_Menus(self.myMenuBar)
        self._init_coll_File_Items(self.File)
        self._init_coll_Help_Items(self.Help)

    def _init_ctrls(self, prnt):
        '''����Ԫ�س�ʼ��'''
        #�����
        wx.Frame.__init__(self, id=wxID_MAINFRAME, name='mainFrame',
              parent=prnt, pos=wx.Point(372, 72), size=wx.Size(535, 600),
              style=wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX),
              title='WaterMaker')
        self._init_utils()
        self.SetMenuBar(self.myMenuBar)
        self.SetThemeEnabled(True)
        self.SetToolTipString('mainFrame')
        #self.SetIcon(wx.Icon(u'ICON.ico',wx.BITMAP_TYPE_ICO))

        self.statusBar1 = wx.StatusBar(id=wxID_MAINFRAMESTATUSBAR1,
              name='statusBar1', parent=self, style=0)
        self.SetStatusBar(self.statusBar1)
        
        #�����
        self.panel1 = wx.Panel(id=wxID_MAINFRAMEPANEL1, name='panel1',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(531, 571),
              style=wx.MAXIMIZE_BOX | wx.TAB_TRAVERSAL)
        self.panel1.SetToolTipString('')
        self.panel1.SetBackgroundColour(wx.Colour(212, 208, 200))
        
        #�ָ���
        self.staticLine1 = wx.StaticLine(id=wxID_MAINFRAMESTATICLINE1,
              name='staticLine1', parent=self.panel1, pos=wx.Point(0, 0),
              size=wx.Size(532, 2), style=0)
        
        #�����
        self.softName = wx.StaticText(id=wxID_MAINFRAMESOFTNAME,
              label='ͼƬˮӡ�������ɹ���',
              name='softName', parent=self.panel1, pos=wx.Point(145, 24),
              size=wx.Size(240, 24), style=0)
        self.softName.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL, False, '����'))
        self.softName.Center(wx.HORIZONTAL)
        
        #ˮӡ����
        self.waterFont = wx.StaticText(id=wxID_MAINFRAMEWATERFONT,
              label='ˮӡ����', name='waterFont', parent=self.panel1,
              pos=wx.Point(24, 96), size=wx.Size(48, 14), style=0)
        self.waterFont.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Tahoma'))
        
        self.wantText = wx.TextCtrl(id=wxID_MAINFRAMEWANTTEXT, name='wantText',
              parent=self.panel1, pos=wx.Point(88, 64), size=wx.Size(400, 72),
              style=wx.TE_MULTILINE,
              value=self.text)
        self.wantText.SetMaxLength(200)
        self.wantText.SetToolTipString("���100������.")
        self.wantText.Bind(wx.EVT_TEXT, self.OnWantText)
        
        #ѡ����ɫ
        self.pickColour = wx.StaticText(id=wxID_MAINFRAMEPICKCOLOUR,
              label='ѡ����ɫ:', name='pickColour',
              parent=self.panel1, pos=wx.Point(24, 157), size=wx.Size(52, 14),
              style=0)
        self.pickColour.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Tahoma'))
        
        self.chooseColour = wx.ColourPickerCtrl(col=wx.BLACK,
              id=wxID_MAINFRAMECHOOSECOLOUR, name='chooseColour',
              parent=self.panel1, pos=wx.Point(88, 152), size=wx.Size(24, 24),
              style=wx.CLRP_DEFAULT_STYLE,)
        self.chooseColour.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnChooseColourChanged)
        self.chooseColour.SetToolTipString("��ѡ������Ҫ��������ɫ")
        
        #ѡ������
        self.pickFont = wx.StaticText(id=wxID_MAINFRAMEPICKFONT,
              label='ѡ������:', name='pickFont',
              parent=self.panel1, pos=wx.Point(152, 157), size=wx.Size(52, 14),
              style=0)
        self.pickFont.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'Tahoma'))
        
        self.chooseFont = wx.Button(self.panel1, -1, "Set Font",
                                     pos=wx.Point(216, 152),size=wx.Size(90, 24))
        self.Bind(wx.EVT_BUTTON, self.OnChooseFont, self.chooseFont)
        
        #��͸����
        self.pickTrans = wx.StaticText(id=wxID_MAINFRAMEPICKTRANS,
              label='��͸����:', name='pickTrans',
              parent=self.panel1, pos=wx.Point(336, 157), size=wx.Size(40, 14),
              style=0)
        self.pickTrans.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Tahoma'))
        
        self.makeTrans = wx.Slider(id=wxID_MAINFRAMEMAKETRANS, maxValue=100,
              minValue=0, name='makeTrans', parent=self.panel1,
              pos=wx.Point(384, 140), size=wx.Size(100, 40),
              style=wx.SL_HORIZONTAL|wx.SL_LABELS, value=100)
        self.makeTrans.Bind(wx.EVT_SCROLL, self.OnMakeTransScroll)
                
        #ԴͼƬ�ļ���
        self.sourceFolder = wx.lib.filebrowsebutton.DirBrowseButton(buttonText='���',
              dialogTitle='ѡ���ļ���',
              id=wxID_MAINFRAMESOURCEFOLDER,
              labelText='ԴͼƬ�ļ���:',
              newDirectory=False, parent=self.panel1, pos=wx.Point(24, 192),
              size=wx.Size(464, 40), startDirectory='.', style=wx.TAB_TRAVERSAL,
              toolTip="ѡ�������ԴͼƬ�ļ���",
              changeCallback=self._setDefaultTarget)
        self.sourceFolder.SetName('sourceFolder')
        
        #ʹ��Ĭ��
        self.useDefault = wx.CheckBox(id=wxID_MAINFRAMEUSEDEFAULT,
              label='ʹ��Ĭ�ϱ����ַ(����ѡ���ԴͼƬ�ļ����д���WaterMaker�ļ���)',
              name='useDefault', parent=self.panel1, pos=wx.Point(24, 248),
              size=wx.Size(456, 16), style=0)
        self.useDefault.SetValue(True)
        self.useDefault.Bind(wx.EVT_CHECKBOX, self.OnUseDefaultCheckbox,
              id=wxID_MAINFRAMEUSEDEFAULT)
        
        #�������ļ���
        self.saveToFolder = wx.lib.filebrowsebutton.DirBrowseButton(buttonText='���',
              dialogTitle='�������ļ���',
              id=wxID_MAINFRAMESAVETOFOLDER,
              labelText='�������ļ���:',
              name='saveToFolder',
              newDirectory=True, parent=self.panel1, pos=wx.Point(24, 280),
              size=wx.Size(464, 40), startDirectory='WaterMaker',
              style=wx.TAB_TRAVERSAL,
              toolTip="ѡ�������Ŀ���ļ���",
              changeCallback=self._setTargetFolder)
        self.saveToFolder.Enable(False)
        
        #ˮӡλ�����
        self.waterPosition = wx.StaticBox(id=wxID_MAINFRAMEWATERPOSITION,
              label='ˮӡλ��', name='waterPosition',
              parent=self.panel1, pos=wx.Point(8, 344), size=wx.Size(240, 160),
              style=0)
        
        self.mainStaticBox = wx.StaticBox(id=wxID_MAINFRAMEMAINSTATICBOX,
              label='', name='mainStaticBox', parent=self.panel1,
              pos=wx.Point(8, 8), size=wx.Size(512, 336), style=0)
        
        #ˮӡλ��-----��
        self.LeftTop = wx.RadioButton(id=wxID_MAINFRAMELEFTTOP,
              label='����', name='LeftTop', parent=self.panel1,
              pos=wx.Point(32, 368), size=wx.Size(48, 14), style=0)
        self.LeftTop.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton1Radiobutton,
              id=wxID_MAINFRAMELEFTTOP)
        
        self.centerTop = wx.RadioButton(id=wxID_MAINFRAMECENTERTOP,
              label='����', name='centerTop', parent=self.panel1,
              pos=wx.Point(104, 368), size=wx.Size(48, 14), style=0)
        self.centerTop.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton1Radiobutton,
              id=wxID_MAINFRAMECENTERTOP)
        
        self.rightTop = wx.RadioButton(id=wxID_MAINFRAMERIGHTTOP,
              label='����', name='rightTop', parent=self.panel1,
              pos=wx.Point(176, 368), size=wx.Size(48, 14), style=0)
        self.rightTop.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton1Radiobutton,
              id=wxID_MAINFRAMERIGHTTOP)
        
        
        #ˮӡλ��-----��
        self.centerLeft = wx.RadioButton(id=wxID_MAINFRAMECENTERLEFT,
              label='����', name='centerLeft', parent=self.panel1,
              pos=wx.Point(32, 416), size=wx.Size(48, 14), style=0)
        self.centerLeft.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton1Radiobutton,
              id=wxID_MAINFRAMECENTERLEFT)
        
        self.center = wx.RadioButton(id=wxID_MAINFRAMECENTER,
              label='����', name='center', parent=self.panel1,
              pos=wx.Point(104, 416), size=wx.Size(48, 14), style=0)
        self.center.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton1Radiobutton,
              id=wxID_MAINFRAMECENTER)
        
        self.centerRight = wx.RadioButton(id=wxID_MAINFRAMECENTERRIGHT,
              label='����', name='centerRight', parent=self.panel1,
              pos=wx.Point(176, 416), size=wx.Size(48, 14), style=0)
        self.centerRight.Bind(wx.EVT_RADIOBUTTON,
              self.OnRadioButton1Radiobutton, id=wxID_MAINFRAMECENTERRIGHT)
        
        #ˮӡλ��-----��
        self.leftBottom = wx.RadioButton(id=wxID_MAINFRAMELEFTBOTTOM,
              label='����', name='leftBottom', parent=self.panel1,
              pos=wx.Point(32, 464), size=wx.Size(48, 14), style=0)
        self.leftBottom.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton1Radiobutton,
              id=wxID_MAINFRAMELEFTBOTTOM)
        
        self.centerBottom = wx.RadioButton(id=wxID_MAINFRAMECENTERBOTTOM,
              label='����', name='centerBottom', parent=self.panel1,
              pos=wx.Point(104, 464), size=wx.Size(48, 14), style=0)
        self.centerBottom.Bind(wx.EVT_RADIOBUTTON,
              self.OnRadioButton1Radiobutton, id=wxID_MAINFRAMECENTERBOTTOM)
        
        self.rightBottom = wx.RadioButton(id=wxID_MAINFRAMERIGHTBOTTOM,
              label='����', name='rightBottom', parent=self.panel1,
              pos=wx.Point(176, 464), size=wx.Size(48, 14), style=0)
        self.rightBottom.SetValue(True)
        self.rightBottom.Bind(wx.EVT_RADIOBUTTON,
              self.OnRadioButton1Radiobutton, id=wxID_MAINFRAMERIGHTBOTTOM)   

        self.startMake = wx.Button(id=wxID_MAINFRAMESTARTMAKE,
              label='��ʼ���ˮӡ',
              name='startMake', parent=self.panel1, pos=wx.Point(340, 400),
              size=wx.Size(96, 32), style=0)
        self.startMake.Bind(wx.EVT_BUTTON, self.OnStartMakeButton,
              id=wxID_MAINFRAMESTARTMAKE)
        
        #������
        self.gauge = wx.Gauge(parent=self.panel1,range=0, pos=(8,510),size=(512,20))
        self.gauge.SetBezelFace(1)
        self.gauge.SetShadowWidth(1)
        self.gauge.Show(False)


    def __init__(self, parent):
        '''�����ʼ������'''
        #��������
        self.Base = 20
        #Ĭ���ļ�������
        self.Default_Target_Folder = "\\WaterMaker"
        #ˮӡ��
        self.text = unicode("����ˮӡ��������","gbk")
        #Դ�ļ���
        self.fromDir = ""
        #Ŀ���ļ���
        self.toDir = ""
        #������ʽ
        self.fontStyle = "SIMSUN.TTC"
        #����·��
        self.fontSrc = "C:\\WINDOWS\\Fonts\\"
        #�����С
        self.fontSize = 30
        #������ɫ,Ĭ�Ϻ�ɫ
        self.fontColour = (0,0,0)
        #͸����
        self.trans = 255
        #ȡ������ɫ = ��ɫ + ͸����
        self._GetFinalColourWithAlpha()
        #ˮӡλ��,Ĭ��Ϊ����
        self.fontPosition = 9
        self.tmpFont = wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL, False, "Tahoma")
        
        
        #ϵͳ���弯�ֵ�
        self.systemFontDict = self._GetSystemFontDict()
        
        self._init_ctrls(parent)
        
    def OnFileItems1Menu(self, event):
        self.Close(True)

    def OnHelpItems0Menu(self, event):
        '''����'''
        msg = "��л��ʹ��ͼƬˮӡ�������ɹ���!\n\n��������:2009��4��19��\n\n�汾:0.9!"
        dlg = wx.MessageDialog(self, message=msg, caption='���ڴ˹���', style=wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        event.Skip()

    def OnUseDefaultCheckbox(self, event):
        '''����'ʹ��Ĭ�ϱ���·��'��ѡ����¼�'''
        if self.useDefault.IsChecked():
            self.saveToFolder.Enable(False)
            sv = self.sourceFolder.GetValue()
            tv = self.saveToFolder.GetValue()
            if sv!=tv:
                self.saveToFolder.SetValue(sv + self.Default_Target_Folder)
        else:
            self.saveToFolder.Enable(True)
        event.Skip()

    def OnRadioButton1Radiobutton(self, event):
        '''����ˮӡλ��'''
        if self.LeftTop.GetValue():
            self.fontPosition = 1#����
        elif self.centerTop.GetValue():
            self.fontPosition = 2#����
        elif self.rightTop.GetValue():
            self.fontPosition = 3#����
        elif self.centerLeft.GetValue():
            self.fontPosition = 4#����
        elif self.center.GetValue():
            self.fontPosition = 5#����
        elif self.centerRight.GetValue():
            self.fontPosition = 6#����
        elif self.leftBottom.GetValue():
            self.fontPosition = 7#����
        elif self.centerBottom.GetValue():
            self.fontPosition = 8#����
        elif self.rightBottom.GetValue():
            self.fontPosition = 9#����
        event.Skip()

    def OnStartMakeButton(self, event):
        '''��ʼ����ˮӡ'''
        self._Start()
        event.Skip()
        
    def OnWantText(self, event):
        '''���޸�ˮӡ���ֿ�ʱ,ͬ����text��ֵ'''
        self.text = self.wantText.GetValue()
        event.Skip()
    
    def OnChooseColourChanged(self,event):
        '''ѡ����ɫʱ,�ı�Ԥ�����������ɫ,������ɫ��ֵ��ȫ�ֱ���fontColour'''
        cc = self.chooseColour.GetColour()
        self.fontColour = cc.Get()
        self._GetFinalColourWithAlpha()
        event.Skip()
    
    
    def OnChooseFont(self, event):
        '''ѡ������ʱ,�ı�Ԥ�����������ʽ,������ֵ��ȫ�ֱ���fontStyle'''
        dlg = wx.FontDialog(self, wx.FontData())
        dlg.GetFontData().SetInitialFont(self.tmpFont)
        if dlg.ShowModal() == wx.ID_OK:
            self.tmpFont = fn = dlg.GetFontData().GetChosenFont()
            #���������С
            self.fontSize = fn.GetPointSize()
            #ȡ��ʽ��ϵͳ����TTF��
            fName = fn.GetFaceName()
            if fName==unicode("����","gbk") or fName==unicode("����-PUA","gbk") or fName==unicode("������","gbk"):
                fName = unicode("���� & ������","gbk")
            try:
                self.fontStyle = self.systemFontDict[fName]
            except:
                pass
        dlg.Destroy()
        event.Skip()
        
    def OnMakeTransScroll(self,event):
        self.trans = int(self.makeTrans.GetValue() * 0.01 * 255)#ȡ�ٷֱ�
        self._GetFinalColourWithAlpha()
        event.Skip()
        
    def _GetSystemFontDict(self):
        '''ȡϵͳ�����弯,����һ���ֵ����͵Ķ���,�ڳ�ʼ��ʱ������.'''
        hkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
                               "Software\\Microsoft\\Windows NT\\CurrentVersion\\Fonts") 
        nSubKey, nSubValue, lastModify = _winreg.QueryInfoKey(hkey)
        d = {}
        for i in range(nSubValue): 
            valueName, valueObj,valueType = _winreg.EnumValue(hkey, i)
            key = valueName.split(" (")[0]
            d[unicode(key,"gbk")] = valueObj
        _winreg.CloseKey(hkey)
        return d
    
    def _setDefaultTarget(self,event):
        '''��ѡ��Դ�ļ��к�,����ȫ�ֵ�Դ�ļ���,����Ƿ�ʹ��Ĭ�ϱ���·��,���ʹ��,
         ����ѡ���·�������Default_Target_Folder,������ToDir'''
        self.fromDir = self.sourceFolder.GetValue()
        if self.useDefault.IsChecked():
            self.toDir = self.fromDir + self.Default_Target_Folder
            self.saveToFolder.SetValue(self.toDir)
        event.Skip()
    
    def _setTargetFolder(self,event):
        '''���������ɽ���ļ��б�����ʱ,����toDir'''
        self.toDir = self.saveToFolder.GetValue()
        event.Skip()
        
    def _GetFinalColourWithAlpha(self):
        r,g,b = self.fontColour
        a = self.trans
        self.finalColourWithAlpha = (r,g,b,a)
    
    def _Start(self):
        '''����ˮӡ���������'''
        if self.fromDir=="":
            self._alertAndStop("��û��ѡ��ԴͼƬ�ļ���!")
            return
        elif self.toDir=="":
            self._alertAndStop("��û��ѡ�񱣴�Ŀ����ļ���!")
            return
        name_reg = re.compile('jpg$', re.I)
        lists = []
        
        #���ԴͼƬ�ļ���
        try:
            lists = os.listdir(self.fromDir)
        except WindowsError,we:
            self._alertAndStop("ԴͼƬ�ļ��в���ȷ,������ѡ��!\n\nErrorMessage: " + str(we))
            return
        #���Ŀ���ļ��в�����,�ʹ���
        if not os.path.isdir(self.toDir):
            os.mkdir(self.toDir)
        
        #���ý���������ʾ,�����ñ߽�ֵ
        self.gauge.Show(True)
        self.gauge.SetValue(0)
        self.gauge.SetRange(len(lists)-1)
        #ѭ������
        try:
            for i in range(len(lists)):
                if name_reg.search(lists[i]):
                    self._im_mark(os.path.join(self.fromDir, lists[i]), os.path.join(self.toDir, lists[i]))
                self.gauge.SetValue(i)
            self._alertAndStop("��ϲ!���ˮӡ���!")
        except Exception,e:
            self._alertAndStop("Sorry,������!����ϵ���߽��!\n\nԭ��: " + str(e))
    
    
    def _im_mark(self, filename, outfilename):
        '''���������ķ���, ����
            filename : Դ�ļ���
            outfilename : ����ļ���
        '''
        FONT = self.fontSrc + self.fontStyle
        cor_fill = self.finalColourWithAlpha
        text = self.text
        img = Image.open(filename).convert("RGB")
        watermark = Image.new("RGBA", (img.size[0], img.size[1]))
        draw = ImageDraw.ImageDraw(watermark, "RGBA")
        font = ImageFont.truetype(FONT, self.fontSize)
        nexttextwidth, nexttextheight = font.getsize(text)
        textwidth, textheight = nexttextwidth, nexttextheight
        #ȡ����--------------------------
        w = watermark.size[0]
        h = watermark.size[1]
        self.PositionDict = self._PositionMap(w, h, textwidth, textheight)
        xy = self.PositionDict[self.fontPosition]
        #ȡ�������---------------------------------
        draw.setfont(font)
        draw.text(xy, text, fill=cor_fill)
        img.paste(watermark, None, watermark)
        img.save(outfilename)
        
    
    def _alertAndStop(self,msg):
        '''��Ϣ��ʾ����,����
            msg: Ҫ��ʾ����Ϣ
        '''
        dlg = wx.MessageDialog(self, message=msg, caption='��ʾ', style=wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
    
    def _PositionMap(self,imgW, imgH, fontW, fontH):
        '''����ˮӡ���꺯��,����һ��PositionDict���ֵ�,������.����:
           imgW : ͼƬ���
           imgH : ͼƬ�߶�
           fontW: ˮӡ���ֿ��
           fontH: ˮӡ���ָ߶� 
        '''
        #����ڶ��е�X����
        MX = (imgW-fontW)/2
        #��������е�X����
        RX = imgW - fontW - self.Base
        #����ڶ��е�Y���� 
        MY = (imgH-fontH)/2
        #����������²���Y����
        BY = imgH-fontH-self.Base
        PositionDict = {
                         1:(self.Base, self.Base),#����
                         2:(MX, self.Base),#����
                         3:(RX, self.Base),#����
                         4:(self.Base, MY),#����
                         5:(MX, MY),#����
                         6:(RX, MY),#����
                         7:(self.Base, BY),#����
                         8:(MX, BY),#����
                         9:(RX, BY)#����
                         }
        return PositionDict
