# -*- coding: utf-8 -*-

import wx

import numpy as np
import matplotlib
# from matplotlib import pyplot
# matplotlib采用WXAgg为后台,将matplotlib嵌入wxPython中
# matplotlib.use("WXAgg")
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx
from matplotlib.ticker import MultipleLocator


######################################################################################
class MatplotPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=-1)
        self.Figure = matplotlib.figure.Figure()
        self.axes = self.Figure.add_axes([0.05, 0.05, 0.93, 0.94])
        self.FigureCanvas = FigureCanvas(self, -1, self.Figure)

        self.NavigationToolbar = Toolbar(self.FigureCanvas,
                                         mPause=parent.PauseDraw,
                                         mStart=parent.StartDraw,
                                         mStop=parent.StopDraw,
                                         mSetAxis=parent.SetAxis
                                         )
        self.TopBoxSizer = wx.BoxSizer(wx.VERTICAL)
        self.TopBoxSizer.Add(self.FigureCanvas, proportion=-10, border=2, flag=wx.ALL | wx.EXPAND)
        self.TopBoxSizer.Add(self.NavigationToolbar, 0, wx.ALL | wx.EXPAND)
        self.SetSizer(self.TopBoxSizer)
        self.init_axis()

        ###方便调用

        self.np = np


    def init_axis(self):
        self.axis([0, 100, -90, -30])  # 设置默认坐标系
        self.axes.tick_params(labelsize=8)  # 设置坐标系哥都文字大小
        self.axes.xaxis.set_major_locator(MultipleLocator(5))  # 设置x轴主坐标刻度为5
        self.axes.xaxis.set_minor_locator(MultipleLocator(1))  # 设置x轴次坐标刻度为1
        self.axes.yaxis.set_major_locator(MultipleLocator(5))  # 设置y轴主坐标刻度为5
        self.axes.yaxis.set_minor_locator(MultipleLocator(1))
        self.axes.xaxis.grid(True, which='major')  # x坐标轴的网格使用次刻度
        self.axes.yaxis.grid(True, which='major')  # x坐标轴的网格使用次刻度
        self.UpdatePlot()

    def UpdatePlot(self):
        '''#修改图形的任何属性后都必须使用self.UpdatePlot()更新GUI界面 '''
        self.FigureCanvas.draw()

    def axis(self, *args, **kwargs):
        return self.axes.axis(*args, **kwargs)

    def plot(self, *args, **kwargs):
        '''#最常用的绘图命令plot '''

        self.axes.plot(*args, **kwargs)
        self.UpdatePlot()

    def pause(self, *args, **kwargs):
        self.plt.pause(*args, **kwargs)

    def semilogx(self, *args, **kwargs):
        ''' #对数坐标绘图命令 '''
        self.axes.semilogx(*args, **kwargs)
        self.UpdatePlot()

    def semilogy(self, *args, **kwargs):
        ''' #对数坐标绘图命令 '''
        self.axes.semilogy(*args, **kwargs)
        self.UpdatePlot()

    def loglog(self, *args, **kwargs):
        ''' #对数坐标绘图命令 '''
        self.axes.loglog(*args, **kwargs)
        self.UpdatePlot()

    def grid(self, flag=True):
        ''' ##显示网格  '''
        if flag:
            self.axes.grid()
        else:
            self.axes.grid(False)

    def title_MPL(self, TitleString="wxMatPlotLib Example In wxPython"):
        ''' # 给图像添加一个标题   '''
        self.axes.set_title(TitleString)

    def xlabel(self, XabelString="X"):
        ''' # Add xlabel to the plotting    '''
        self.axes.set_xlabel(XabelString)

    def ylabel(self, YabelString="Y"):
        ''' # Add ylabel to the plotting '''
        self.axes.set_ylabel(YabelString)

    def xticker(self, major_ticker=1.0, minor_ticker=0.1):
        ''' # 设置X轴的刻度大小 '''

        self.axes.xaxis.set_major_locator(MultipleLocator(major_ticker))
        self.axes.xaxis.set_minor_locator(MultipleLocator(minor_ticker))

    def yticker(self, major_ticker=1.0, minor_ticker=0.1):
        ''' # 设置Y轴的刻度大小 '''
        self.axes.yaxis.set_major_locator(MultipleLocator(major_ticker))
        self.axes.yaxis.set_minor_locator(MultipleLocator(minor_ticker))

    def legend(self, *args, **kwargs):
        ''' #图例legend for the plotting  '''
        self.axes.legend(*args, **kwargs)

    def xlim(self, x_min, x_max):
        ''' # 设置x轴的显示范围  '''
        self.axes.set_xlim(x_min, x_max)

    def ylim(self, y_min, y_max):
        ''' # 设置y轴的显示范围   '''
        self.axes.set_ylim(y_min, y_max)

    def savefig(self, *args, **kwargs):
        ''' #保存图形到文件 '''
        self.Figure.savefig(*args, **kwargs)

    def cla(self):
        ''' # 再次画图前,必须调用该命令清空原来的图形  '''
        self.axes.clear()
        self.Figure.set_canvas(self.FigureCanvas)
        self.UpdatePlot()

    def ShowHelpString(self, HelpString="Show Help String"):
        ''' #可以用它来显示一些帮助信息,如鼠标位置等 '''
        self.StaticText.SetLabel(HelpString)

    def array(self, *args, **kwargs):
        return np.array(*args, **kwargs)


class Toolbar(NavigationToolbar2Wx):
    def __init__(self, canvas, mStart, mPause, mStop, mSetAxis):
        self.toolitems = (
            ('Home', 'Reset original view', 'home', 'home'),
            ('Back', 'Back to  previous view', 'back', 'back'),
            ('Forward', 'Forward to next view', 'forward', 'forward'),
            ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            ('Save', 'Save the figure', 'filesave', 'save_figure'),
            ('Start', 'Start draw the view', 'start', 'start'),
            ('Stop', 'Stop draw the view', 'stop', 'stop'),
            ('Setting', 'Set up the line', 'subplots', 'setting')

        )
        self.mPause = mPause
        self.mStart = mStart
        self.mStop = mStop
        self.mSetAxis = mSetAxis
        self.setting_dialog = None

        NavigationToolbar2Wx.__init__(self, canvas=canvas)
        self.ctrl_pan = self.FindById(self.wx_ids['Pan'])
        self.ctrl_zoom = self.FindById(self.wx_ids['Zoom'])

    def back(self, event):
        super(Toolbar, self).back(event)
        self.mSetAxis()

    def forward(self, event):
        super(Toolbar, self).forward(event)
        self.mSetAxis()

    def pan(self, event):
        self.mPause(self.ctrl_pan.IsToggled())
        super(Toolbar, self).pan(event)

    def start(self, event):
        self.mStart()

    def stop(self, event):
        self.mStop()

    def release_zoom(self, event):
        super(Toolbar, self).release_zoom(event)
        self.mSetAxis()

    def save_figure(self, event):
        self.mPause(True)
        super(Toolbar, self).save_figure(event)
        if self.ctrl_zoom.IsToggled() or self.ctrl_pan.IsToggled():
            self.mPause(True)
        else:
            self.mPause(False)

    def setting(self, event):
        if self.setting_dialog:
            self.setting_dialog.Destroy()
        else:
            self.setting_dialog = SettingDialog(size=(600, 200))
            self.setting_dialog.Show()


from lib.UserInterface.Dialog import DialogBase
from lib.UserInterface.libs import Config


class SettingDialog(DialogBase.DialogBase):
    def __init__(self, size, positon=wx.DefaultPosition):
        DialogBase.DialogBase.__init__(self, name="Setting", size=size, pos=positon)
        Main = wx.BoxSizer(wx.HORIZONTAL)
        BR_Sizer = self.__init_checkbox("BR")
        CS_Sizer = self.__init_checkbox("CS")
        User0_Sizer = self.__init_checkbox("User0")
        User1_Sizer = self.__init_checkbox("User1")
        User2_Sizer = self.__init_checkbox("User2")
        User3_Sizer = self.__init_checkbox("User3")

        Main.Add(BR_Sizer, 1, wx.EXPAND, 5)
        Main.Add(CS_Sizer, 1, wx.EXPAND, 5)
        Main.Add(User0_Sizer, 1, wx.EXPAND, 5)
        Main.Add(User1_Sizer, 1, wx.EXPAND, 5)
        Main.Add(User2_Sizer, 1, wx.EXPAND, 5)
        Main.Add(User3_Sizer, 1, wx.EXPAND, 5)
        self.SetSizer(Main)

    def __init_checkbox(self, label):
        Sizer = wx.BoxSizer(wx.VERTICAL)
        for x in range(4):
            tmp = u"%s_%s" % (label, x)
            CB = wx.CheckBox(self, wx.ID_ANY, tmp, wx.DefaultPosition, wx.DefaultSize, 0)
            CB.Bind(wx.EVT_CHECKBOX, self.on_check)
            CB.SetValue(self.get_display(tmp))
            Sizer.Add(CB, 0, wx.ALL, 5)
        return Sizer

    def on_check(self, event):
        obj = event.GetEventObject()
        self.set_display(obj.GetLabel(), obj.IsChecked())

    def get_display(self, key):
        print key

        print Config.Line.get(key)

        return Config.Line.get(key)[0]

    def set_display(self, key, boolean):
        Config.Line.get(key)[0] = boolean
