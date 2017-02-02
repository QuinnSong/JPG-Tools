#coding=gbk
#########################
#开发日期:2009年4月19日\n\n版本:0.9
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
        '''向菜单栏添加大项菜单'''
        parent.Append(menu=self.File, title='文件(&F)')
        parent.Append(menu=self.Help, title='帮助(&H)')

    def _init_coll_File_Items(self, parent):
        '''创建文件菜单的子菜单项,并绑定事件'''
        parent.Append(help='退出程序', id=wxID_MAINFRAMEFILEITEMS1,
              kind=wx.ITEM_NORMAL, text='退出')
        self.Bind(wx.EVT_MENU, self.OnFileItems1Menu,
              id=wxID_MAINFRAMEFILEITEMS1)

    def _init_coll_Help_Items(self, parent):
        '''创建帮助菜单的子菜单项,并绑定事件'''
        parent.Append(help='关于此工具', id=wxID_MAINFRAMEHELPITEMS0,
              kind=wx.ITEM_NORMAL, text='关于')
        self.Bind(wx.EVT_MENU, self.OnHelpItems0Menu,
              id=wxID_MAINFRAMEHELPITEMS0)

    def _init_utils(self):
        '''菜单栏初始化'''
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
        '''界面元素初始化'''
        #主框架
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
        
        #主面板
        self.panel1 = wx.Panel(id=wxID_MAINFRAMEPANEL1, name='panel1',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(531, 571),
              style=wx.MAXIMIZE_BOX | wx.TAB_TRAVERSAL)
        self.panel1.SetToolTipString('')
        self.panel1.SetBackgroundColour(wx.Colour(212, 208, 200))
        
        #分割线
        self.staticLine1 = wx.StaticLine(id=wxID_MAINFRAMESTATICLINE1,
              name='staticLine1', parent=self.panel1, pos=wx.Point(0, 0),
              size=wx.Size(532, 2), style=0)
        
        #大标题
        self.softName = wx.StaticText(id=wxID_MAINFRAMESOFTNAME,
              label='图片水印快速生成工具',
              name='softName', parent=self.panel1, pos=wx.Point(145, 24),
              size=wx.Size(240, 24), style=0)
        self.softName.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL, False, '宋体'))
        self.softName.Center(wx.HORIZONTAL)
        
        #水印文字
        self.waterFont = wx.StaticText(id=wxID_MAINFRAMEWATERFONT,
              label='水印文字', name='waterFont', parent=self.panel1,
              pos=wx.Point(24, 96), size=wx.Size(48, 14), style=0)
        self.waterFont.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Tahoma'))
        
        self.wantText = wx.TextCtrl(id=wxID_MAINFRAMEWANTTEXT, name='wantText',
              parent=self.panel1, pos=wx.Point(88, 64), size=wx.Size(400, 72),
              style=wx.TE_MULTILINE,
              value=self.text)
        self.wantText.SetMaxLength(200)
        self.wantText.SetToolTipString("最多100个汉字.")
        self.wantText.Bind(wx.EVT_TEXT, self.OnWantText)
        
        #选择颜色
        self.pickColour = wx.StaticText(id=wxID_MAINFRAMEPICKCOLOUR,
              label='选择颜色:', name='pickColour',
              parent=self.panel1, pos=wx.Point(24, 157), size=wx.Size(52, 14),
              style=0)
        self.pickColour.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Tahoma'))
        
        self.chooseColour = wx.ColourPickerCtrl(col=wx.BLACK,
              id=wxID_MAINFRAMECHOOSECOLOUR, name='chooseColour',
              parent=self.panel1, pos=wx.Point(88, 152), size=wx.Size(24, 24),
              style=wx.CLRP_DEFAULT_STYLE,)
        self.chooseColour.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnChooseColourChanged)
        self.chooseColour.SetToolTipString("请选择您需要的字体颜色")
        
        #选择字体
        self.pickFont = wx.StaticText(id=wxID_MAINFRAMEPICKFONT,
              label='选择字体:', name='pickFont',
              parent=self.panel1, pos=wx.Point(152, 157), size=wx.Size(52, 14),
              style=0)
        self.pickFont.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'Tahoma'))
        
        self.chooseFont = wx.Button(self.panel1, -1, "Set Font",
                                     pos=wx.Point(216, 152),size=wx.Size(90, 24))
        self.Bind(wx.EVT_BUTTON, self.OnChooseFont, self.chooseFont)
        
        #不透明度
        self.pickTrans = wx.StaticText(id=wxID_MAINFRAMEPICKTRANS,
              label='不透明度:', name='pickTrans',
              parent=self.panel1, pos=wx.Point(336, 157), size=wx.Size(40, 14),
              style=0)
        self.pickTrans.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'Tahoma'))
        
        self.makeTrans = wx.Slider(id=wxID_MAINFRAMEMAKETRANS, maxValue=100,
              minValue=0, name='makeTrans', parent=self.panel1,
              pos=wx.Point(384, 140), size=wx.Size(100, 40),
              style=wx.SL_HORIZONTAL|wx.SL_LABELS, value=100)
        self.makeTrans.Bind(wx.EVT_SCROLL, self.OnMakeTransScroll)
                
        #源图片文件夹
        self.sourceFolder = wx.lib.filebrowsebutton.DirBrowseButton(buttonText='浏览',
              dialogTitle='选择文件夹',
              id=wxID_MAINFRAMESOURCEFOLDER,
              labelText='源图片文件夹:',
              newDirectory=False, parent=self.panel1, pos=wx.Point(24, 192),
              size=wx.Size(464, 40), startDirectory='.', style=wx.TAB_TRAVERSAL,
              toolTip="选择或输入源图片文件夹",
              changeCallback=self._setDefaultTarget)
        self.sourceFolder.SetName('sourceFolder')
        
        #使用默认
        self.useDefault = wx.CheckBox(id=wxID_MAINFRAMEUSEDEFAULT,
              label='使用默认保存地址(在您选择的源图片文件夹中创建WaterMaker文件夹)',
              name='useDefault', parent=self.panel1, pos=wx.Point(24, 248),
              size=wx.Size(456, 16), style=0)
        self.useDefault.SetValue(True)
        self.useDefault.Bind(wx.EVT_CHECKBOX, self.OnUseDefaultCheckbox,
              id=wxID_MAINFRAMEUSEDEFAULT)
        
        #保存至文件夹
        self.saveToFolder = wx.lib.filebrowsebutton.DirBrowseButton(buttonText='浏览',
              dialogTitle='保存至文件夹',
              id=wxID_MAINFRAMESAVETOFOLDER,
              labelText='保存至文件夹:',
              name='saveToFolder',
              newDirectory=True, parent=self.panel1, pos=wx.Point(24, 280),
              size=wx.Size(464, 40), startDirectory='WaterMaker',
              style=wx.TAB_TRAVERSAL,
              toolTip="选择或输入目标文件夹",
              changeCallback=self._setTargetFolder)
        self.saveToFolder.Enable(False)
        
        #水印位置面板
        self.waterPosition = wx.StaticBox(id=wxID_MAINFRAMEWATERPOSITION,
              label='水印位置', name='waterPosition',
              parent=self.panel1, pos=wx.Point(8, 344), size=wx.Size(240, 160),
              style=0)
        
        self.mainStaticBox = wx.StaticBox(id=wxID_MAINFRAMEMAINSTATICBOX,
              label='', name='mainStaticBox', parent=self.panel1,
              pos=wx.Point(8, 8), size=wx.Size(512, 336), style=0)
        
        #水印位置-----上
        self.LeftTop = wx.RadioButton(id=wxID_MAINFRAMELEFTTOP,
              label='左上', name='LeftTop', parent=self.panel1,
              pos=wx.Point(32, 368), size=wx.Size(48, 14), style=0)
        self.LeftTop.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton1Radiobutton,
              id=wxID_MAINFRAMELEFTTOP)
        
        self.centerTop = wx.RadioButton(id=wxID_MAINFRAMECENTERTOP,
              label='中上', name='centerTop', parent=self.panel1,
              pos=wx.Point(104, 368), size=wx.Size(48, 14), style=0)
        self.centerTop.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton1Radiobutton,
              id=wxID_MAINFRAMECENTERTOP)
        
        self.rightTop = wx.RadioButton(id=wxID_MAINFRAMERIGHTTOP,
              label='右上', name='rightTop', parent=self.panel1,
              pos=wx.Point(176, 368), size=wx.Size(48, 14), style=0)
        self.rightTop.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton1Radiobutton,
              id=wxID_MAINFRAMERIGHTTOP)
        
        
        #水印位置-----中
        self.centerLeft = wx.RadioButton(id=wxID_MAINFRAMECENTERLEFT,
              label='中左', name='centerLeft', parent=self.panel1,
              pos=wx.Point(32, 416), size=wx.Size(48, 14), style=0)
        self.centerLeft.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton1Radiobutton,
              id=wxID_MAINFRAMECENTERLEFT)
        
        self.center = wx.RadioButton(id=wxID_MAINFRAMECENTER,
              label='正中', name='center', parent=self.panel1,
              pos=wx.Point(104, 416), size=wx.Size(48, 14), style=0)
        self.center.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton1Radiobutton,
              id=wxID_MAINFRAMECENTER)
        
        self.centerRight = wx.RadioButton(id=wxID_MAINFRAMECENTERRIGHT,
              label='中右', name='centerRight', parent=self.panel1,
              pos=wx.Point(176, 416), size=wx.Size(48, 14), style=0)
        self.centerRight.Bind(wx.EVT_RADIOBUTTON,
              self.OnRadioButton1Radiobutton, id=wxID_MAINFRAMECENTERRIGHT)
        
        #水印位置-----下
        self.leftBottom = wx.RadioButton(id=wxID_MAINFRAMELEFTBOTTOM,
              label='左下', name='leftBottom', parent=self.panel1,
              pos=wx.Point(32, 464), size=wx.Size(48, 14), style=0)
        self.leftBottom.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton1Radiobutton,
              id=wxID_MAINFRAMELEFTBOTTOM)
        
        self.centerBottom = wx.RadioButton(id=wxID_MAINFRAMECENTERBOTTOM,
              label='中下', name='centerBottom', parent=self.panel1,
              pos=wx.Point(104, 464), size=wx.Size(48, 14), style=0)
        self.centerBottom.Bind(wx.EVT_RADIOBUTTON,
              self.OnRadioButton1Radiobutton, id=wxID_MAINFRAMECENTERBOTTOM)
        
        self.rightBottom = wx.RadioButton(id=wxID_MAINFRAMERIGHTBOTTOM,
              label='右下', name='rightBottom', parent=self.panel1,
              pos=wx.Point(176, 464), size=wx.Size(48, 14), style=0)
        self.rightBottom.SetValue(True)
        self.rightBottom.Bind(wx.EVT_RADIOBUTTON,
              self.OnRadioButton1Radiobutton, id=wxID_MAINFRAMERIGHTBOTTOM)   

        self.startMake = wx.Button(id=wxID_MAINFRAMESTARTMAKE,
              label='开始添加水印',
              name='startMake', parent=self.panel1, pos=wx.Point(340, 400),
              size=wx.Size(96, 32), style=0)
        self.startMake.Bind(wx.EVT_BUTTON, self.OnStartMakeButton,
              id=wxID_MAINFRAMESTARTMAKE)
        
        #进度条
        self.gauge = wx.Gauge(parent=self.panel1,range=0, pos=(8,510),size=(512,20))
        self.gauge.SetBezelFace(1)
        self.gauge.SetShadowWidth(1)
        self.gauge.Show(False)


    def __init__(self, parent):
        '''界面初始化方法'''
        #基本坐标
        self.Base = 20
        #默认文件夹名称
        self.Default_Target_Folder = "\\WaterMaker"
        #水印字
        self.text = unicode("快速水印制作工具","gbk")
        #源文件夹
        self.fromDir = ""
        #目标文件夹
        self.toDir = ""
        #字体样式
        self.fontStyle = "SIMSUN.TTC"
        #字体路径
        self.fontSrc = "C:\\WINDOWS\\Fonts\\"
        #字体大小
        self.fontSize = 30
        #字体颜色,默认黑色
        self.fontColour = (0,0,0)
        #透明度
        self.trans = 255
        #取最终颜色 = 颜色 + 透明度
        self._GetFinalColourWithAlpha()
        #水印位置,默认为右下
        self.fontPosition = 9
        self.tmpFont = wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL, False, "Tahoma")
        
        
        #系统字体集字典
        self.systemFontDict = self._GetSystemFontDict()
        
        self._init_ctrls(parent)
        
    def OnFileItems1Menu(self, event):
        self.Close(True)

    def OnHelpItems0Menu(self, event):
        '''关于'''
        msg = "感谢您使用图片水印快速生成工具!\n\n开发日期:2009年4月19日\n\n版本:0.9!"
        dlg = wx.MessageDialog(self, message=msg, caption='关于此工具', style=wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        event.Skip()

    def OnUseDefaultCheckbox(self, event):
        '''处理'使用默认保存路径'复选框的事件'''
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
        '''设置水印位置'''
        if self.LeftTop.GetValue():
            self.fontPosition = 1#左上
        elif self.centerTop.GetValue():
            self.fontPosition = 2#中上
        elif self.rightTop.GetValue():
            self.fontPosition = 3#右上
        elif self.centerLeft.GetValue():
            self.fontPosition = 4#中左
        elif self.center.GetValue():
            self.fontPosition = 5#正中
        elif self.centerRight.GetValue():
            self.fontPosition = 6#中右
        elif self.leftBottom.GetValue():
            self.fontPosition = 7#左下
        elif self.centerBottom.GetValue():
            self.fontPosition = 8#中下
        elif self.rightBottom.GetValue():
            self.fontPosition = 9#右下
        event.Skip()

    def OnStartMakeButton(self, event):
        '''开始制作水印'''
        self._Start()
        event.Skip()
        
    def OnWantText(self, event):
        '''当修改水印文字框时,同步更text的值'''
        self.text = self.wantText.GetValue()
        event.Skip()
    
    def OnChooseColourChanged(self,event):
        '''选择颜色时,改变预览框字体的颜色,并将颜色赋值给全局变量fontColour'''
        cc = self.chooseColour.GetColour()
        self.fontColour = cc.Get()
        self._GetFinalColourWithAlpha()
        event.Skip()
    
    
    def OnChooseFont(self, event):
        '''选择字体时,改变预览框字体的样式,并将赋值给全局变量fontStyle'''
        dlg = wx.FontDialog(self, wx.FontData())
        dlg.GetFontData().SetInitialFont(self.tmpFont)
        if dlg.ShowModal() == wx.ID_OK:
            self.tmpFont = fn = dlg.GetFontData().GetChosenFont()
            #设置字体大小
            self.fontSize = fn.GetPointSize()
            #取样式的系统字体TTF名
            fName = fn.GetFaceName()
            if fName==unicode("宋体","gbk") or fName==unicode("宋体-PUA","gbk") or fName==unicode("新宋体","gbk"):
                fName = unicode("宋体 & 新宋体","gbk")
            try:
                self.fontStyle = self.systemFontDict[fName]
            except:
                pass
        dlg.Destroy()
        event.Skip()
        
    def OnMakeTransScroll(self,event):
        self.trans = int(self.makeTrans.GetValue() * 0.01 * 255)#取百分比
        self._GetFinalColourWithAlpha()
        event.Skip()
        
    def _GetSystemFontDict(self):
        '''取系统的字体集,返回一个字典类型的对象,在初始化时被调用.'''
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
        '''在选择源文件夹后,设置全局的源文件夹,检查是否使用默认保存路径,如果使用,
         则在选择的路径后加入Default_Target_Folder,并设置ToDir'''
        self.fromDir = self.sourceFolder.GetValue()
        if self.useDefault.IsChecked():
            self.toDir = self.fromDir + self.Default_Target_Folder
            self.saveToFolder.SetValue(self.toDir)
        event.Skip()
    
    def _setTargetFolder(self,event):
        '''当保存生成结果文件夹被更改时,设置toDir'''
        self.toDir = self.saveToFolder.GetValue()
        event.Skip()
        
    def _GetFinalColourWithAlpha(self):
        r,g,b = self.fontColour
        a = self.trans
        self.finalColourWithAlpha = (r,g,b,a)
    
    def _Start(self):
        '''制作水印方法的入口'''
        if self.fromDir=="":
            self._alertAndStop("您没有选择源图片文件夹!")
            return
        elif self.toDir=="":
            self._alertAndStop("您没有选择保存目标的文件夹!")
            return
        name_reg = re.compile('jpg$', re.I)
        lists = []
        
        #检查源图片文件夹
        try:
            lists = os.listdir(self.fromDir)
        except WindowsError,we:
            self._alertAndStop("源图片文件夹不正确,请重新选择!\n\nErrorMessage: " + str(we))
            return
        #如果目标文件夹不存在,就创建
        if not os.path.isdir(self.toDir):
            os.mkdir(self.toDir)
        
        #设置进度条可显示,并设置边界值
        self.gauge.Show(True)
        self.gauge.SetValue(0)
        self.gauge.SetRange(len(lists)-1)
        #循环处理
        try:
            for i in range(len(lists)):
                if name_reg.search(lists[i]):
                    self._im_mark(os.path.join(self.fromDir, lists[i]), os.path.join(self.toDir, lists[i]))
                self.gauge.SetValue(i)
            self._alertAndStop("恭喜!添加水印完成!")
        except Exception,e:
            self._alertAndStop("Sorry,出错啦!请联系作者解决!\n\n原因: " + str(e))
    
    
    def _im_mark(self, filename, outfilename):
        '''进行制作的方法, 参数
            filename : 源文件名
            outfilename : 输出文件名
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
        #取坐标--------------------------
        w = watermark.size[0]
        h = watermark.size[1]
        self.PositionDict = self._PositionMap(w, h, textwidth, textheight)
        xy = self.PositionDict[self.fontPosition]
        #取坐标完成---------------------------------
        draw.setfont(font)
        draw.text(xy, text, fill=cor_fill)
        img.paste(watermark, None, watermark)
        img.save(outfilename)
        
    
    def _alertAndStop(self,msg):
        '''消息提示方法,参数
            msg: 要提示的信息
        '''
        dlg = wx.MessageDialog(self, message=msg, caption='提示', style=wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
    
    def _PositionMap(self,imgW, imgH, fontW, fontH):
        '''设置水印坐标函数,生成一个PositionDict的字典,并返回.参数:
           imgW : 图片宽度
           imgH : 图片高度
           fontW: 水印文字宽度
           fontH: 水印文字高度 
        '''
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
                         4:(self.Base, MY),#中左
                         5:(MX, MY),#正中
                         6:(RX, MY),#中右
                         7:(self.Base, BY),#左下
                         8:(MX, BY),#中下
                         9:(RX, BY)#右下
                         }
        return PositionDict
