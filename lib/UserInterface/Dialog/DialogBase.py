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


class DialogWindow(wx.Frame):
    def __init__(self, size, id=wx.ID_ANY, name=DialogNameStr, pos=wx.DefaultPosition,
                 style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX):
        wx.Frame.__init__(self, None, id=id, title=name, pos=pos, size=size, style=style)
        self._name = name

    @property
    def name(self):
        return self._name




if __name__ == '__main__':
    app = wx.App()
    f = DialogWindow((400, 300))
    f.Show()
    app.MainLoop()
