# -*- encoding:UTF-8 -*-
import wx
from NotebookBase import NotebookBase
from lib import Utility
from lib.UserInterface.Dialog import RegisterSetting as Dialog
from lib.Config import Instrument
from lib.ProtocolStack import Configuration
from math import log10

reg = Instrument.get_register()
logger = Utility.getLogger(__name__)

RegisterSettingPage = [Configuration.snr_config, Configuration.rssi_config, Configuration.bler_config]


class RegisterSetting(NotebookBase):
    def __init__(self, parent):
        NotebookBase.__init__(self, parent=parent, name="寄存器设置")
        self.font = wx.Font(11, wx.MODERN, wx.NORMAL, wx.BOLD, underline=True)
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        ButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        button_RF = wx.Button(self, wx.ID_ANY, u"射频设置", wx.DefaultPosition, wx.DefaultSize, 0)
        button_PS = wx.Button(self, wx.ID_ANY, u"基带设置", wx.DefaultPosition, wx.DefaultSize, 0)
        button_save = wx.Button(self, wx.ID_ANY, u"保存到Excel", wx.DefaultPosition, wx.DefaultSize, 0)
        button_refresh = wx.Button(self, wx.ID_ANY, u"刷新", wx.DefaultPosition, wx.DefaultSize, 0)
        button_RF.Bind(wx.EVT_BUTTON, self.on_freq_setting)
        button_PS.Bind(wx.EVT_BUTTON, self.on_protocol_stack_setting)
        button_refresh.Bind(wx.EVT_BUTTON, self.on_refresh)
        ButtonSizer.Add(button_RF, 0, wx.ALL, 5)

        ButtonSizer.Add(button_PS, 0, wx.ALL, 5)
        ButtonSizer.Add(button_save, 0, wx.ALL, 5)
        ButtonSizer.Add(button_refresh, 0, wx.ALL, 5)
        InfoSizer = wx.BoxSizer(wx.VERTICAL)
        RSSI_Sizer = self.__init_rssi_sizer()
        SNR_Sizer = self.__init_snr_sizer()
        BLER_Sizer = self.__init_bler_sizer()
        InfoSizer.Add(RSSI_Sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        InfoSizer.Add(SNR_Sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        InfoSizer.Add(BLER_Sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        CenterSizer = wx.BoxSizer(wx.HORIZONTAL)
        CenterSizer.Add(InfoSizer, 1, wx.EXPAND | wx.ALL, 0)
        button_add_mpl = wx.Button(self, wx.ID_ANY, u">", wx.DefaultPosition, (25, -1), 0)
        button_add_mpl.Bind(wx.EVT_BUTTON, self.on_add_mpl)
        CenterSizer.Add(button_add_mpl, 0, wx.EXPAND | wx.TOP, 6)

        QuickSettingSizer = self.__init_quick_setting_sizer()
        MainSizer.Add(ButtonSizer, 0, wx.EXPAND | wx.ALL, 5)
        MainSizer.Add(CenterSizer, 0, wx.EXPAND | wx.ALL, 5)
        MainSizer.Add(QuickSettingSizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        self.dialog_freq_setting = None
        self.dialog_prot_stack_setting = None
        self.dialog_mpl = None

        self.SetSizer(MainSizer)
        self.Layout()

    def __init_title_sizer(self, title, *items, **kwargs):
        Sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, wx.ID_ANY, title, wx.DefaultPosition, wx.DefaultSize, 0)
        title.SetFont(self.font)
        Sizer.Add(title, 0, wx.ALIGN_LEFT | wx.TOP, 5)
        ItemSizer = wx.BoxSizer(wx.VERTICAL)
        for item in items:
            item_title = wx.StaticText(self, wx.ID_ANY, item, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
            ItemSizer.Add(item_title, 0, wx.ALIGN_CENTER | wx.TOP, 11)
        Sizer.Add(ItemSizer, 0, wx.ALIGN_CENTER | wx.ALL, 1)
        return Sizer

    def __init_rssi_sizer(self):
        Sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.HORIZONTAL)
        TitleSizer = self.__init_title_sizer(u"RSSI", u"天线0 ：", u"天线1 ：", u"天线2 ：", u"天线3 ：")
        Sizer.Add(TitleSizer, 0, wx.ALL, 0)
        ItemSizer = wx.BoxSizer(wx.HORIZONTAL)
        for item in Configuration.rssi_config:
            self.__setattr__(item['name'], RSSI(self, item))
            sizer = self.__getattribute__(item['name']).get_sizer()
            ItemSizer.Add(sizer, 0, wx.ALL, 0)
        Sizer.Add(ItemSizer, 1, wx.EXPAND | wx.ALL, 0)
        # button_add_rssi = wx.Button(self, wx.ID_ANY, u">", wx.DefaultPosition, (25, -1), 0)
        # button_add_rssi.Bind(wx.EVT_BUTTON, self.on_add_rssi_mpl)
        # Sizer.Add(button_add_rssi, 0, wx.EXPAND | wx.RIGHT, 0)
        return Sizer

    def __init_snr_sizer(self):
        Sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.HORIZONTAL)
        TitleSizer = self.__init_title_sizer(u"SNR", u"信噪比：")
        Sizer.Add(TitleSizer, 0, wx.ALL, 0)
        ItemSizer = wx.BoxSizer(wx.HORIZONTAL)
        for item in Configuration.snr_config:
            self.__setattr__(item['name'], SNR(self, item, _type="1"))
            sizer = self.__getattribute__(item['name']).get_sizer()
            ItemSizer.Add(sizer, 0, wx.ALL, 0)
        Sizer.Add(ItemSizer, 1, wx.EXPAND | wx.ALL, 0)
        # button_add_snr = wx.Button(self, wx.ID_ANY, u">", wx.DefaultPosition, (25, -1), 0)
        # button_add_snr.Bind(wx.EVT_BUTTON, self.on_add_snr_mpl)
        # Sizer.Add(button_add_snr, 0, wx.EXPAND | wx.RIGHT, 0)
        return Sizer

    def __init_bler_sizer(self):
        Sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.HORIZONTAL)
        TitleSizer = self.__init_title_sizer(u"BLER", u"误块率：")
        Sizer.Add(TitleSizer, 0, wx.ALL, 0)
        ItemSizer = wx.BoxSizer(wx.HORIZONTAL)
        for item in Configuration.bler_config:
            self.__setattr__(item['name'], BLER(self, item))
            sizer = self.__getattribute__(item['name']).get_sizer()
            ItemSizer.Add(sizer, 0, wx.ALL, 0)
        Sizer.Add(ItemSizer, 1, wx.EXPAND | wx.ALL, 0)
        # button_add_bler = wx.Button(self, wx.ID_ANY, u">", wx.DefaultPosition, (25, -1), 0)
        # button_add_bler.Bind(wx.EVT_BUTTON, self.on_add_bler_mpl)
        # Sizer.Add(button_add_bler, 0, wx.EXPAND | wx.RIGHT, 0)
        return Sizer

    def __init_quick_setting_sizer(self):
        Sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.HORIZONTAL)
        title = wx.StaticText(self, wx.ID_ANY, u"#TODO:把常用的设置放这里，方便直接使用", wx.DefaultPosition, wx.DefaultSize, 0)
        font = wx.Font(20, wx.MODERN, wx.NORMAL, wx.BOLD, underline=True)
        title.SetFont(font)
        Sizer.Add(title, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        return Sizer

    def on_freq_setting(self, event):
        if not self.dialog_freq_setting:
            self.dialog_freq_setting = Dialog.RadioFrequencyDialog()
        if self.dialog_freq_setting.IsShown():
            self.dialog_freq_setting.Destroy()
        else:
            self.dialog_freq_setting.Show()

    def on_protocol_stack_setting(self, event):
        if not self.dialog_prot_stack_setting:
            self.dialog_prot_stack_setting = Dialog.ProtocolStackDialog()
        if self.dialog_prot_stack_setting.IsShown():
            self.dialog_prot_stack_setting.Destroy()
        else:
            self.dialog_prot_stack_setting.Show()

    def on_refresh(self, event):
        for config in RegisterSettingPage:
            for item in config:
                self.__getattribute__(item['name']).refresh()

    def close(self):
        dialogs = [self.dialog_freq_setting, self.dialog_prot_stack_setting, self.dialog_mpl]
        for dialog in dialogs:
            if dialog and dialog.IsShown():
                dialog.Destroy()

    def on_add_mpl(self, event):
        if not self.dialog_mpl:
            for config in RegisterSettingPage:
                for item in config:


            self.dialog_mpl = Dialog.MplDialog(RegisterSettingPage)
        if self.dialog_mpl.IsShown():
            self.dialog_mpl.Destroy()
        else:
            self.dialog_mpl.Show()


class RSSI(object):
    def __init__(self, panel, item):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.item = item
        logger.debug("RSSI Data:Init")
        logger.debug(item)
        width = 95
        self.a0 = item['address'][0]
        self.a1 = item['address'][1]
        self.a2 = item['address'][2]
        self.a3 = item['address'][3]

        title = wx.StaticText(panel, wx.ID_ANY, item['title'], wx.DefaultPosition, wx.DefaultSize, 0)
        self.a0_tc = wx.TextCtrl(panel, wx.ID_ANY, '', wx.DefaultPosition, (width, -1), wx.TE_CENTER | wx.TE_READONLY)
        self.a1_tc = wx.TextCtrl(panel, wx.ID_ANY, '', wx.DefaultPosition, (width, -1), wx.TE_CENTER | wx.TE_READONLY)
        self.a2_tc = wx.TextCtrl(panel, wx.ID_ANY, '', wx.DefaultPosition, (width, -1), wx.TE_CENTER | wx.TE_READONLY)
        self.a3_tc = wx.TextCtrl(panel, wx.ID_ANY, '', wx.DefaultPosition, (width, -1), wx.TE_CENTER | wx.TE_READONLY)
        self.sizer.Add(title, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.sizer.Add(self.a0_tc, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        self.sizer.Add(self.a1_tc, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        self.sizer.Add(self.a2_tc, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        self.sizer.Add(self.a3_tc, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        self.refresh()

    def disable(self):
        self.a0_tc.Disable()
        self.a1_tc.Disable()
        self.a2_tc.Disable()
        self.a3_tc.Disable()

    def refresh(self):
        self.a0_tc.SetValue(self.__get_reg_data(self.a0))
        self.a1_tc.SetValue(self.__get_reg_data(self.a1))
        self.a2_tc.SetValue(self.__get_reg_data(self.a2))
        self.a3_tc.SetValue(self.__get_reg_data(self.a3))

    def __get_reg_data(self, address):
        sim_address, dig_address = address
        data = reg.GetByte(address=sim_address, reverse=1)
        sim_rssi = ord(data[sim_address % 4])
        dig_rssi = ord(data[dig_address % 4])
        logger.debug('%s:sim:%s,dig:%s' % (self.item['name'], sim_rssi, dig_rssi))
        return str(-(sim_rssi + dig_rssi))

    def get_sizer(self):
        return self.sizer


class SNR(object):
    def __init__(self, panel, item, _type):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.item = item
        self.usr = item['usr']
        logger.debug("SNR Data:Init")
        logger.debug(item)
        width = 95
        title = wx.StaticText(panel, wx.ID_ANY, item['title'], wx.DefaultPosition, wx.DefaultSize, 0)
        self.snr_tc = wx.TextCtrl(panel, wx.ID_ANY, '', wx.DefaultPosition, (width, -1), wx.TE_CENTER)
        self.sizer.Add(title, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.sizer.Add(self.snr_tc, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        self.refresh()

    def disable(self):
        self.snr_tc.Disable()

    def refresh(self):
        self.snr_tc.SetValue(self.__get_reg_data(self.usr))

    def __get_reg_data(self, address):
        first_address, second_address = address
        data = reg.GetByte(first_address, reverse=1)
        first_value = ord(data[first_address % 4])
        second_value = ord(data[second_address % 4])
        logger.info('%s:1st:%s,2nd:%s ' % (self.item['name'], first_value, second_value))
        value = second_value * 256 + first_value
        data = value / 64.0
        if data == 0:
            return '0'
        data = round(10 * log10(data), 1)
        return str(data)

    def get_sizer(self):
        return self.sizer


class BLER(object):
    def __init__(self, panel, item):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.item = item
        self.total = item['total']
        self.error = item['error']
        logger.debug("BLER Data:Init")
        logger.debug(item)
        width = 95
        title = wx.StaticText(panel, wx.ID_ANY, item['title'], wx.DefaultPosition, wx.DefaultSize, 0)
        self.bler_tc = wx.TextCtrl(panel, wx.ID_ANY, '', wx.DefaultPosition, (width, -1), wx.TE_CENTER)
        self.sizer.Add(title, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.sizer.Add(self.bler_tc, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        self.refresh()

    def disable(self):
        self.bler_tc.Disable()

    def refresh(self):
        self.bler_tc.SetValue(self.__get_reg_data(self.total, self.error))

    def __get_reg_data(self, total, error):
        def get_value(address):
            first_address, second_address = address
            data = reg.GetByte(first_address, reverse=1)
            value = ord(data[second_address % 4]) * 256 + ord(data[first_address % 4])
            return value

        total_value = get_value(total)
        error_value = get_value(error)
        logger.info('%s:error:%s,total:%s' % (self.item['name'], error_value, total_value))
        if total_value == 0:
            return '0'
        return str(error_value / total_value)

    def get_sizer(self):
        return self.sizer
