# -*- coding:utf-8 -*-
import wx
from wx._core import BoxSizer, GridSizer
from wx.lib.splitter import MultiSplitterWindow, MultiSplitterEvent
from wx.lib.agw.fourwaysplitter import FourWaySplitter



class ProxyFrame(wx.ScrolledWindow):
    def __init__(self, parent):
        wx.ScrolledWindow.__init__(self, parent)
        self.createWidget()

    def createWidget(self):
        self.proxy_split_mult = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE, size=(800, 450))
        self.proxy_split_mult.SetMinimumPaneSize(10)  # 最小面板大小

        self.proxy_split_top = wx.SplitterWindow(self.proxy_split_mult)  # 上结构
        self.proxy_split_bottom = wx.SplitterWindow(self.proxy_split_mult)  # 下结构

        ########## 结构上左右 ##########  
        self.proxy_scrol_leftTop = wx.ScrolledWindow(self.proxy_split_top)
        self.proxy_scrol_leftTop.SetBackgroundColour(wx.WHITE)
        self.proxy_scrol_leftTop.SetScrollbars(10, 10, 400, 300)
        self.proxy_scrol_leftTop.SetAutoLayout(1)

        self.proxy_scrol_rightTop = wx.ScrolledWindow(self.proxy_split_top)
        self.proxy_scrol_rightTop.SetBackgroundColour(wx.BLACK)

        self.proxy_split_top.SetMinimumPaneSize(10)  # 最小面板大小
        self.proxy_split_top.SplitVertically(self.proxy_scrol_leftTop, self.proxy_scrol_rightTop)  # 分割面板
        self.proxy_split_top.SetSashGravity(0.5)
        ########## 结构上左右 end ##########  

        ########## 结构下左右 ##########  
        self.proxy_scrol_leftBottom = wx.ScrolledWindow(self.proxy_split_bottom)
        self.proxy_scrol_leftBottom.SetBackgroundColour(wx.WHITE)
        self.proxy_scrol_rightBottom = wx.ScrolledWindow(self.proxy_split_bottom)
        self.proxy_scrol_rightBottom.SetBackgroundColour(wx.BLACK)

        self.proxy_split_bottom.SetMinimumPaneSize(10)  # 最小面板大小
        self.proxy_split_bottom.SplitVertically(self.proxy_scrol_leftBottom, self.proxy_scrol_rightBottom)  # 分割面板
        self.proxy_split_bottom.SetSashGravity(0.5)
        ########## 结构下左右 end ##########  

        self.proxy_split_mult.SplitHorizontally(self.proxy_split_top, self.proxy_split_bottom)  # 分割面板
        self.proxy_split_mult.SetSashGravity(0.5)

        self.SetScrollbars(10, 10, 400, 300)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.proxy_split_mult, 1, flag=wx.EXPAND)  # 自动缩放
        self.SetSizer(sizer)


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "My Frame", size=(800, 450))
        self.createWidget()

    def createWidget(self):
        ########## 窗体底部状态栏 ##########  
        self.statusbar = self.CreateStatusBar(2)
        self.statusbar.SetStatusText("", 0)
        self.statusbar.SetStatusText("", 1)

        ########## HTTP代理书签页 ##########  
        self.createProxyWidget()

        # HTTP代理书签页

    def createProxyWidget(self):
        self.proxy_nb = wx.Notebook(self, -1, name="proxy_nb")
        self.proxyFrame = ProxyFrame(self.proxy_nb)
        self.proxy_nb.AddPage(self.proxyFrame, u"HTTP代理")


def main():
    # 设置了主窗口的初始大小960x540 800x450 640x360
    root = wx.App()
    frame = MainFrame()
    frame.Show(True)
    root.MainLoop()


if __name__ == "__main__":
    main()  