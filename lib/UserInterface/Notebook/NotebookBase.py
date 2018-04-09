# -*- encoding:UTF-8 -*-
import wx

PanelNameStr = "WUYOU"


class NotebookBase(wx.Panel):
    def __init__(self, parent=None, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TAB_TRAVERSAL,
                 name=PanelNameStr):
        wx.Panel.__init__(self, parent=parent, id=id, pos=pos, size=size, style=style, name=name)
