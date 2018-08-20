# -*- encoding:UTF-8 -*-
import wx
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
import numpy
import pylab
from lib.UserInterface.Dialog import DialogBase
import logging

matplotlib.use('WXAgg')
logger = logging.getLogger(__name__)


class MplDialog(DialogBase.DialogWindow):
    def __init__(self, name=u"趋势图", **kwargs):
        DialogBase.DialogWindow.__init__(self, name=name, size=wx.DefaultSize)
        x0, y0, x1, y1 = wx.ClientDisplayRect()
        self.SetSize(wx.Size(x1, y1))
        self.SetPosition(wx.Point(x0, y0))

        self.__init_menu_bar()
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        LeftSizer = wx.BoxSizer(wx.VERTICAL)
        CenterSizer = wx.BoxSizer(wx.VERTICAL)
        RightSizer = wx.BoxSizer(wx.VERTICAL)

        self.use0 = RSSIPanel(self)
        self.use1 = RSSIPanel(self)
        self.use2 = RSSIPanel(self)
        self.use3 = RSSIPanel(self)
        self.snr = SNRPanel(self)
        self.bler = BLERPanel(self)

        LeftSizer.Add(self.use0, 1, wx.EXPAND | wx.ALL, 0)
        LeftSizer.Add(self.use2, 1, wx.EXPAND | wx.ALL, 0)
        CenterSizer.Add(self.use1, 1, wx.EXPAND | wx.ALL, 0)
        CenterSizer.Add(self.use3, 1, wx.EXPAND | wx.ALL, 0)
        RightSizer.Add(self.snr, 1, wx.EXPAND | wx.ALL, 0)
        RightSizer.Add(self.bler, 1, wx.EXPAND | wx.ALL, 0)

        MainSizer.Add(LeftSizer, 1, wx.EXPAND | wx.ALL, 0)
        MainSizer.Add(CenterSizer, 1, wx.EXPAND | wx.ALL, 0)
        MainSizer.Add(RightSizer, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(MainSizer)
        self.Layout()

    def Show(self, show=1):
        super(DialogBase.DialogWindow, self).Show(show=show)

    def __init_menu_bar(self):
        menu_bar = wx.MenuBar()
        menu_rssi = wx.Menu()
        menu_bar.Append(menu_rssi, "&RSSI")
        self.SetMenuBar(menu_bar)


class RSSIPanel(wx.Panel):
    def __init__(self, parent, obj):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                          style=wx.TAB_TRAVERSAL)
        self.obj = obj
        colors = ["blue", "red", "yellow", "grey", "pink", "white"]
        import random
        self.SetBackgroundColour(random.choice(colors))


class SNRPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                          style=wx.TAB_TRAVERSAL)
        colors = ["blue", "red", "yellow", "grey", "pink", "white"]
        import random
        self.SetBackgroundColour(random.choice(colors))


class BLERPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                          style=wx.TAB_TRAVERSAL)
        colors = ["blue", "red", "yellow", "grey", "pink", "white"]
        import random
        self.SetBackgroundColour(random.choice(colors))
