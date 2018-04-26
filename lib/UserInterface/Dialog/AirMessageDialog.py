# encoding: utf-8
from lib.UserInterface.Dialog import DialogBase
import wx


class AirMessageDialog(DialogBase.DialogBase):
    def __init__(self, data):
        DialogBase.DialogBase.__init__(self, name="Air Message Detail", size=(1000, 500))
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        TC = wx.TextCtrl(self, -1, value="", style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        data, log = data
        for line in log:
            try:
                wx.CallAfter(TC.AppendText, text=line.strip('\r\n') + '\n')
            except Exception:
                print repr(line)
        # TC.SetFont(wx.Font(5, wx.MODERN, wx.NORMAL, wx.BOLD))
        MainSizer.Add(TC, 1, wx.EXPAND, 10)
        self.SetSizer(MainSizer)
