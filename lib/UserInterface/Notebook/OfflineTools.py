# -*- encoding:UTF-8 -*-
import wx
from NotebookBase import NotebookBase
from lib import Utility

Logger = Utility.getLogger(__name__)


class OfflineTools(NotebookBase):
    def __init__(self, parent):
        NotebookBase.__init__(self, parent=parent, name="OFFLINE")

        sizer = wx.GridBagSizer(9, 9)
        sizer.Add(wx.Button(self, -1, "按钮1"), (0, 0), wx.DefaultSpan,
                  wx.ALL, 5)
        sizer.Add(wx.Button(self, -1, "按钮2"), (1, 1), (1, 7), wx.EXPAND)
        sizer.Add(wx.Button(self, -1, "按钮3"), (6, 6), (3, 3), wx.EXPAND)
        sizer.Add(wx.Button(self, -1, "按钮4"), (3, 0), (1, 1),
                  wx.ALIGN_CENTER)
        sizer.Add(wx.Button(self, -1, "按钮5"), (4, 0), (1, 1),
                  wx.ALIGN_LEFT)
        sizer.Add(wx.Button(self, -1, "按钮6"), (5, 0), (1, 1),
                  wx.ALIGN_RIGHT)
        sizer.AddGrowableRow(6)
        sizer.AddGrowableCol(6)
        self.SetSizerAndFit(sizer)
        self.Centre()

        self.SetSizerAndFit(sizer)


