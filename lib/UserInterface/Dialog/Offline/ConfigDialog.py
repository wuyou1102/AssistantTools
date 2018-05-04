# encoding: utf-8
from lib.UserInterface.Dialog import DialogBase
from lib.UserInterface.Notebook import OfflineLibs
import wx


class ConfigDialog(DialogBase.DialogBase):
    def __init__(self):
        DialogBase.DialogBase.__init__(self, name="Config", size=(400, 400))
        MainSizer = wx.BoxSizer(wx.VERTICAL)


        self.SetSizer(MainSizer)
