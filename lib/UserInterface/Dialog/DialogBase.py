# -*- encoding:UTF-8 -*-
import wx
from lib import Utility
DialogNameStr = "WUYOU"


class DialogBase(wx.Dialog):
    def __init__(self, size, parent=None, id=wx.ID_ANY, name=DialogNameStr):
        wx.Dialog.__init__(self, parent=parent, id=id, title=name, size=size)
        self._name = name

    @property
    def name(self):
        return self._name
