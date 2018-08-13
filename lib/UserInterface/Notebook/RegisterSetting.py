# -*- encoding:UTF-8 -*-
import wx
from NotebookBase import NotebookBase
from lib import Utility
from lib.UserInterface.Dialog.RegisterSetting import RadioFrequencyDialog, ProtocolStackDialog
from lib.Config import Instrument

reg = Instrument.get_register()
Logger = Utility.getLogger(__name__)


class RegisterSetting(NotebookBase):
    def __init__(self, parent):
        NotebookBase.__init__(self, parent=parent, name="寄存器设置")
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        ButtonSizer = wx.BoxSizer(wx.HORIZONTAL)

        button_RF = wx.Button(self, wx.ID_ANY, u"射频设置", wx.DefaultPosition, wx.DefaultSize, 0)
        button_PS = wx.Button(self, wx.ID_ANY, u"协议栈设置", wx.DefaultPosition, wx.DefaultSize, 0)
        button_save = wx.Button(self, wx.ID_ANY, u"保存到Excel", wx.DefaultPosition, wx.DefaultSize, 0)
        button_refresh = wx.Button(self, wx.ID_ANY, u"刷新", wx.DefaultPosition, wx.DefaultSize, 0)

        button_RF.Bind(wx.EVT_BUTTON, self.on_freq_setting)
        button_PS.Bind(wx.EVT_BUTTON, self.on_protocol_stack_setting)

        ButtonSizer.Add(button_RF, 0, wx.ALL, 5)
        ButtonSizer.Add(button_PS, 0, wx.ALL, 5)
        ButtonSizer.Add(button_save, 0, wx.ALL, 5)
        ButtonSizer.Add(button_refresh, 0, wx.ALL, 5)

        MainSizer.Add(ButtonSizer, 1, wx.EXPAND, 5)

        self.dialog_freq_setting = None
        self.dialog_prot_stack_setting = None
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

    def on_protocol_stack_setting(self, event):
        if not self.dialog_prot_stack_setting:
            self.dialog_prot_stack_setting = ProtocolStackDialog()
        if self.dialog_prot_stack_setting.IsShown():
            self.dialog_prot_stack_setting.Destroy()
        else:
            self.dialog_prot_stack_setting.Show()

    def close(self):
        if self.dialog_freq_setting and self.dialog_freq_setting.IsShown():
            self.dialog_freq_setting.Destroy()
        if self.dialog_prot_stack_setting and self.dialog_prot_stack_setting.IsShown():
            self.dialog_prot_stack_setting.Destroy()
