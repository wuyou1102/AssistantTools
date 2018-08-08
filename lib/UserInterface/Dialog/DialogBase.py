# -*- encoding:UTF-8 -*-
import wx
from lib import Utility

DialogNameStr = "WUYOU"


class DialogBase(wx.Dialog):
    def __init__(self, size, parent=None, id=wx.ID_ANY, name=DialogNameStr, pos=wx.DefaultPosition):
        wx.Dialog.__init__(self, parent=parent, id=id, title=name, size=size, pos=pos)
        self._name = name
        # self.Bind(wx.EVT_CLOSE, self.on_close)

    @property
    def name(self):
        return self._name
    #
    # def on_close(self, event):
    #     self.DES
    #     self.Destroy()
    #     event.Skip()
