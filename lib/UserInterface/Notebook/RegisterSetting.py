# -*- encoding:UTF-8 -*-
import wx
from NotebookBase import NotebookBase
from lib import Utility
from lib.UserInterface.Dialog.RegisterSetting import RadioFrequencyDialog
from lib.Config import Instrument

reg = Instrument.get_register()
Logger = Utility.getLogger(__name__)


class RegisterSetting(NotebookBase):
    def __init__(self, parent):
        NotebookBase.__init__(self, parent=parent, name="寄存器设置")
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        ButtonSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.FreqSetting = wx.Button(self, wx.ID_ANY, u"射频设置", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button2 = wx.Button(self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button3 = wx.Button(self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button4 = wx.Button(self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0)
        self.FreqSetting.Bind(wx.EVT_BUTTON, self.on_freq_setting)

        ButtonSizer.Add(self.FreqSetting, 0, wx.ALL, 5)
        ButtonSizer.Add(self.m_button2, 0, wx.ALL, 5)
        ButtonSizer.Add(self.m_button3, 0, wx.ALL, 5)
        ButtonSizer.Add(self.m_button4, 0, wx.ALL, 5)
        MainSizer.Add(ButtonSizer, 1, wx.EXPAND, 5)

        self.dialog_freq_setting = None
        self.SetSizer(MainSizer)
        self.Layout()

    def __del__(self):
        pass

    def on_freq_setting(self, event):
        if not self.dialog_freq_setting:
            self.dialog_freq_setting = RadioFrequencyDialog()
        if self.dialog_freq_setting.IsShown():
            self.dialog_freq_setting.Destroy()
        else:
            self.dialog_freq_setting.Show()
