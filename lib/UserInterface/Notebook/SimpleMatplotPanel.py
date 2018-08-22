# -*- coding: utf-8 -*-

import wx
import numpy as np
import matplotlib

# matplotlib采用WXAgg为后台,将matplotlib嵌入wxPython中
matplotlib.use("WXAgg")
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

from matplotlib.ticker import MultipleLocator


######################################################################################
class MatplotPanel(wx.Panel):
    def __init__(self, parent, x1, x2, y1, y2, xa=2, xi=1, ya=10, yi=2):
        wx.Panel.__init__(self, parent=parent, id=-1)
        self.Figure = matplotlib.figure.Figure()
        self.axes = self.Figure.add_axes([0.05, 0.05, 0.93, 0.94])

        self.FigureCanvas = FigureCanvas(self, -1, self.Figure)
        self.x1, self.x2, self.y1, self.y2 = x1, x2, y1, y2
        self.xa, self.xi, self.ya, self.yi = xa, xi, ya, yi
        self.TopBoxSizer = wx.BoxSizer(wx.VERTICAL)
        self.TopBoxSizer.Add(self.FigureCanvas, proportion=-10, border=2, flag=wx.ALL | wx.EXPAND)
        self.SetSizer(self.TopBoxSizer)
        self.init_axis()

    def init_axis(self):
        self.axis([self.x1, self.x2, self.y1, self.y2])  # 设置默认坐标系
        self.axes.tick_params(labelsize=8)  # 设置坐标系哥都文字大小
        self.axes.xaxis.set_major_locator(MultipleLocator(self.xa))  # 设置x轴主坐标刻度为5
        self.axes.xaxis.set_minor_locator(MultipleLocator(self.xi))  # 设置x轴次坐标刻度为1
        self.axes.yaxis.set_major_locator(MultipleLocator(self.ya))  # 设置y轴主坐标刻度为5
        self.axes.yaxis.set_minor_locator(MultipleLocator(self.yi))
        self.axes.xaxis.grid(True, which='major')
        self.axes.yaxis.grid(True, which='major')
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
