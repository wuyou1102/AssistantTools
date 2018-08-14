# -*- encoding:UTF-8 -*-
import wx
from NotebookBase import NotebookBase
from lib import Utility
from lib.UserInterface.Dialog.RegisterSetting import RadioFrequencyDialog, ProtocolStackDialog
from lib.Config import Instrument
from lib.ProtocolStack import Configuration

reg = Instrument.get_register()
Logger = Utility.getLogger(__name__)


class RegisterSetting(NotebookBase):
    def __init__(self, parent):
        NotebookBase.__init__(self, parent=parent, name="寄存器设置")
        self.font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, underline=True)
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
        RSSI_Sizer = self.__init_rssi_sizer()
        SNR_Sizer = self.__init_snr_sizer()
        BLER_Sizer = self.__init_bler_sizer()

        MainSizer.Add(ButtonSizer, 0, wx.EXPAND | wx.ALL, 5)
        MainSizer.Add(RSSI_Sizer, 0, wx.EXPAND | wx.ALL, 5)
        MainSizer.Add(SNR_Sizer, 0, wx.EXPAND | wx.ALL, 5)
        MainSizer.Add(BLER_Sizer, 0, wx.EXPAND | wx.ALL, 5)

        self.dialog_freq_setting = None
        self.dialog_prot_stack_setting = None
        self.SetSizer(MainSizer)
        self.Layout()

    def __init_title_sizer(self, title, *items, **kwargs):
        Sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, wx.ID_ANY, title, wx.DefaultPosition, wx.DefaultSize, 0)
        title.SetFont(self.font)
        Sizer.Add(title, 0, wx.ALIGN_LEFT | wx.TOP, 10)
        for item in items:
            item_title = wx.StaticText(self, wx.ID_ANY, item, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
            Sizer.Add(item_title, 0, wx.ALIGN_CENTER | wx.TOP, 16)
        return Sizer

    def __init_rssi_sizer(self):
        Sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.VERTICAL)
        TitleSizer = self.__init_title_sizer(u"RSSI", u"天线0 ：", u"天线1 ：", u"天线2 ：", u"天线3 ：")
        Sizer.Add(TitleSizer, 0, wx.ALL, 0)
        for item in Configuration.rssi_config:
            self.__setattr__(item['name'], RSSI(self, item))
            sizer = self.__getattribute__(item['name']).get_sizer()
            Sizer.Add(sizer, 0, wx.ALL, 0)
        return Sizer

    def __init_snr_sizer(self):
        Sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.VERTICAL)
        TitleSizer = self.__init_title_sizer(u"SNR", u"信噪比：")
        Sizer.Add(TitleSizer, 0, wx.ALL, 0)
        return Sizer

    def __init_bler_sizer(self):
        Sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.VERTICAL)
        Sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.VERTICAL)
        TitleSizer = self.__init_title_sizer(u"BLER", u"误块率：")
        Sizer.Add(TitleSizer, 0, wx.ALL, 0)
        return Sizer

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


class RSSI(object):
    def __init__(self, panel, item):
        self.sizer = wx.BoxSizer(wx.VERTICAL)

    def get_sizer(self):
        return self.sizer
