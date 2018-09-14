# -*- encoding:UTF-8 -*-
from math import log10

import wx

from NotebookBase import NotebookBase
from lib import Utility
from lib.Config import Instrument
from lib.ProtocolStack import Configuration
from lib.UserInterface.Dialog import RegisterSetting as Dialog

reg = Instrument.get_register()
logger = Utility.getLogger(__name__)

RegisterSettingPage = [Configuration.snr_config, Configuration.rssi_config, Configuration.bler_user_config,
                       Configuration.bler_br_config]
rssi_objects = [x['name'] for x in Configuration.rssi_config]
snr_object = [x['name'] for x in Configuration.snr_config]
bler_object = [x['name'] for x in Configuration.bler_user_config]
bler_object.append(Configuration.bler_br_config['name'])


class RegisterSetting(NotebookBase):
    def __init__(self, parent):
        NotebookBase.__init__(self, parent=parent, name="寄存器设置")
        self.font = wx.Font(11, wx.MODERN, wx.NORMAL, wx.BOLD, underline=True)
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        ButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        button_RF = wx.Button(self, wx.ID_ANY, u"射频设置", wx.DefaultPosition, wx.DefaultSize, 0)
        button_PS = wx.Button(self, wx.ID_ANY, u"基带设置", wx.DefaultPosition, wx.DefaultSize, 0)
        # button_save = wx.Button(self, wx.ID_ANY, u"保存到Excel", wx.DefaultPosition, wx.DefaultSize, 0)
        button_refresh = wx.Button(self, wx.ID_ANY, u"刷新", wx.DefaultPosition, wx.DefaultSize, 0)
        button_RF.Bind(wx.EVT_BUTTON, self.on_freq_setting)
        button_PS.Bind(wx.EVT_BUTTON, self.on_protocol_stack_setting)
        button_refresh.Bind(wx.EVT_BUTTON, self.on_refresh)
        ButtonSizer.Add(button_RF, 0, wx.ALL, 5)

        ButtonSizer.Add(button_PS, 0, wx.ALL, 5)
        # ButtonSizer.Add(button_save, 0, wx.ALL, 5)
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
        self.Refresh()

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
        return Sizer

    def __init_bler_sizer(self):
        Sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.HORIZONTAL)
        TitleSizer = self.__init_title_sizer(u"BLER", u"误块率：")
        Sizer.Add(TitleSizer, 0, wx.ALL, 0)
        ItemSizer = wx.BoxSizer(wx.HORIZONTAL)
        for item in Configuration.bler_user_config:
            self.__setattr__(item['name'], BLER_USER(self, item))
            sizer = self.__getattribute__(item['name']).get_sizer()
            ItemSizer.Add(sizer, 0, wx.ALL, 0)
        self.__setattr__(Configuration.bler_br_config['name'], BLER_BR(self, Configuration.bler_br_config))
        bler_br_sizer = self.__getattribute__(Configuration.bler_br_config['name']).get_sizer()
        ItemSizer.Add(bler_br_sizer, 0, wx.ALL, 0)
        Sizer.Add(ItemSizer, 1, wx.EXPAND | wx.ALL, 0)
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
        self.Refresh()

    def Refresh(self):
        if not reg.IsConnect():
            Utility.AlertError(u"无法获取寄存器，请检查：\n\t1.是否连接寄存器并给寄存器上电。\n\t2.是否打开了其他占用寄存器的应用。\n\t3.驱动是否安装正确。")
            return False

        for config in RegisterSettingPage:
            if type(config) == list:
                for item in config:
                    self.__getattribute__(item['name']).refresh()
            elif type(config) == dict:
                self.__getattribute__(config['name']).refresh()

    def close(self):
        dialogs = [self.dialog_freq_setting, self.dialog_prot_stack_setting, self.dialog_mpl]
        for dialog in dialogs:
            if dialog and dialog.IsShown():
                dialog.Destroy()

    def on_add_mpl(self, event):
        if not reg.IsConnect():
            Utility.AlertError(u"无法获取寄存器，请检查：\n\t1.是否连接寄存器并给寄存器上电。\n\t2.是否打开了其他占用寄存器的应用。\n\t3.驱动是否安装正确。")
            return False
        if not self.dialog_mpl:
            rssi = [self.__getattribute__(obj) for obj in rssi_objects]
            snr = [self.__getattribute__(obj) for obj in snr_object]
            bler = [self.__getattribute__(obj) for obj in bler_object]
            self.dialog_mpl = Dialog.MplDialog(rssi=rssi, snr=snr, bler=bler)
        if self.dialog_mpl.IsShown():
            self.dialog_mpl.Destroy()
        else:
            self.dialog_mpl.Show()


class RSSI(Dialog.ObjectBase):
    def __init__(self, panel, item):
        Dialog.ObjectBase.__init__(self, item=item)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
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
        self.list_a0 = list()
        self.list_a1 = list()
        self.list_a2 = list()
        self.list_a3 = list()

    def disable(self):
        self.a0_tc.Disable()
        self.a1_tc.Disable()
        self.a2_tc.Disable()
        self.a3_tc.Disable()

    def refresh(self):
        self.a0_tc.SetValue(self.get_reg_data(self.a0))
        self.a1_tc.SetValue(self.get_reg_data(self.a1))
        self.a2_tc.SetValue(self.get_reg_data(self.a2))
        self.a3_tc.SetValue(self.get_reg_data(self.a3))

    def clear(self):
        self.list_a0 = list()
        self.list_a1 = list()
        self.list_a2 = list()
        self.list_a3 = list()
        return self.list_a0, self.list_a1, self.list_a2, self.list_a3,

    def next(self):
        self.a0_tc.SetValue(self.__get_reg_data(self.a0, self.list_a0))
        self.a1_tc.SetValue(self.__get_reg_data(self.a1, self.list_a1))
        self.a2_tc.SetValue(self.__get_reg_data(self.a2, self.list_a2))
        self.a3_tc.SetValue(self.__get_reg_data(self.a3, self.list_a3))
        return self.list_a0, self.list_a1, self.list_a2, self.list_a3,

    def get_reg_data(self, address):
        sim_address, dig_address = address
        data = reg.GetBytes(address=sim_address, reverse=1)
        sim_rssi = ord(data[sim_address % 4])
        dig_rssi = ord(data[dig_address % 4])
        rssi = -(sim_rssi + dig_rssi)
        logger.debug('%s:sim:%s,dig:%s' % (self.item['name'], sim_rssi, dig_rssi))
        return str(rssi)

    def __get_reg_data(self, address, lst):
        sim_address, dig_address = address
        data = reg.GetBytes(address=sim_address, reverse=1)
        sim_rssi = ord(data[sim_address % 4])
        dig_rssi = ord(data[dig_address % 4])
        rssi = -(sim_rssi + dig_rssi)
        lst.append(int(rssi))
        logger.debug('%s:sim:%s,dig:%s' % (self.item['name'], sim_rssi, dig_rssi))
        return str(rssi)


class SNR(Dialog.ObjectBase):
    def __init__(self, panel, item, _type):
        Dialog.ObjectBase.__init__(self, item=item)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.usr = item['usr']
        logger.debug("SNR Data:Init")
        logger.debug(item)

        width = 95
        title = wx.StaticText(panel, wx.ID_ANY, item['title'], wx.DefaultPosition, wx.DefaultSize, 0)
        self.snr_tc = wx.TextCtrl(panel, wx.ID_ANY, '', wx.DefaultPosition, (width, -1), wx.TE_CENTER)
        self.sizer.Add(title, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.sizer.Add(self.snr_tc, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        self.lst = list()

    def clear(self):
        self.lst = list()

    def next(self):
        self.snr_tc.SetValue(self.__get_reg_data(self.usr, self.lst))
        return self.lst

    def disable(self):
        self.snr_tc.Disable()

    def refresh(self):
        self.snr_tc.SetValue(self.get_reg_data(self.usr))

    def __get_reg_data(self, address, lst):
        first_address, second_address = address
        data = reg.GetBytes(first_address, reverse=1)
        first_value = ord(data[first_address % 4])
        second_value = ord(data[second_address % 4])
        logger.info('%s:1st:%s,2nd:%s ' % (self.item['name'], first_value, second_value))
        value = second_value * 256 + first_value
        data = value / 64.0
        if data == 0:
            lst.append(0)
            return '0'
        data = round(10 * log10(data), 1)
        lst.append(data)
        return str(data)

    def get_reg_data(self, address):
        first_address, second_address = address
        data = reg.GetBytes(first_address, reverse=1)
        first_value = ord(data[first_address % 4])
        second_value = ord(data[second_address % 4])
        logger.info('%s:1st:%s,2nd:%s ' % (self.item['name'], first_value, second_value))
        value = second_value * 256 + first_value
        data = value / 64.0
        if data == 0:
            return '0'
        data = round(10 * log10(data), 1)
        return str(data)


class BLER_USER(Dialog.ObjectBase):
    def __init__(self, panel, item):
        Dialog.ObjectBase.__init__(self, item=item)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.total = item['total']
        self.error = item['error']
        logger.debug("BLER_USER Data:Init")
        logger.debug(item)
        width = 95
        title = wx.StaticText(panel, wx.ID_ANY, item['title'], wx.DefaultPosition, wx.DefaultSize, 0)
        self.bler_tc = wx.TextCtrl(panel, wx.ID_ANY, '', wx.DefaultPosition, (width, -1), wx.TE_CENTER)
        self.sizer.Add(title, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.sizer.Add(self.bler_tc, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        self.lst = list()

    def clear(self):
        self.lst = list()

    def disable(self):
        self.bler_tc.Disable()

    def refresh(self):
        self.bler_tc.SetValue(self.get_reg_data(self.total, self.error))

    def next(self):
        self.bler_tc.SetValue(self.__get_reg_data(self.total, self.error, self.lst))
        return self.lst

    def get_reg_data(self, total, error):
        def get_value(address):
            first_address, second_address = address
            data = reg.GetBytes(first_address, reverse=1)
            value = ord(data[second_address % 4]) * 256 + ord(data[first_address % 4])
            return value

        total_value = get_value(total)
        error_value = get_value(error)
        logger.info('%s:error:%s,total:%s' % (self.item['name'], error_value, total_value))
        if total_value == 0:
            return '0'
        return str(error_value * 100 / total_value)

    def __get_reg_data(self, total, error, lst):
        def get_value(address):
            first_address, second_address = address
            data = reg.GetBytes(first_address, reverse=1)
            value = ord(data[second_address % 4]) * 256 + ord(data[first_address % 4])
            return value

        total_value = get_value(total)
        error_value = get_value(error)
        logger.info('%s:error:%s,total:%s' % (self.item['name'], error_value, total_value))
        if total_value == 0:
            lst.append(0)
            return '0'
        value = error_value * 100 / total_value
        lst.append(value)
        return str(value)


# BLER里面加上BR的BLER,计算方法：
# 1算LDPC_NUM


# 2 算BR_PACKET
# BR_PACKET=2^(0x316[7:5])
# 3 算BR的BLER
# BR_BLER== 0x4dc/(BR_PACKET*LDPC_NUM)
class BLER_BR(Dialog.ObjectBase):
    def __init__(self, panel, item):
        Dialog.ObjectBase.__init__(self, item=item)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        logger.debug("BLER_BR Data:Init")
        logger.debug(item)
        width = 95
        title = wx.StaticText(panel, wx.ID_ANY, 'BR', wx.DefaultPosition, wx.DefaultSize, 0)
        self.bler_tc = wx.TextCtrl(panel, wx.ID_ANY, '', wx.DefaultPosition, (width, -1), wx.TE_CENTER)
        self.sizer.Add(title, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.sizer.Add(self.bler_tc, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        self.lst = list()
        self.FFT = {
            '001': 192,
            '010': 384,
            '011': 768,
            '100': 1536,
        }
        self.Symbols = {
            '000': 6,
            '001': 12,
            '011': 24,
        }
        self.Repeat = {
            '000': 1,
            '001': 2,
            '010': 4,
            '011': 2,
            '100': 4,
            '101': 8,
            '110': 4,
            '111': 8,
        }
        self.QamBits = {
            '0': 1,
            '1': 2,
        }

    def clear(self):
        self.lst = list()

    def disable(self):
        self.bler_tc.Disable()

    def refresh(self):
        self.bler_tc.SetValue(self.get_reg_data())

    def next(self):
        self.bler_tc.SetValue(self.__get_reg_data(self.lst))
        return self.lst

    def get_reg_data(self):
        value = self.__calc_br_bler()
        return str(value)

    def __get_reg_data(self, lst):
        value = self.__calc_br_bler()
        lst.append(value)
        return str(value)

    def __calc_br_bler(self):
        ldpc_num = self.__calc_ldpc_num()
        br_packet = self.__calc_br_packet()
        error = ord(reg.GetByte(self.item['error'][0]))
        return error / ldpc_num / br_packet

    def __calc_br_packet(self):
        packet = self.get_part_bits(*self.item['packet'])
        i = int(packet, 2)
        return 2 ** i

    def __calc_ldpc_num(self):
        ldpc_num = self.__get_fft() * self.__get_symbols() / self.__get_repeat() / 576 * self.__get_qam_bits()
        return ldpc_num

    def __get_fft(self):
        return self.FFT[self.get_part_bits(*self.item['fft'])]

    def __get_symbols(self):
        return self.Symbols[self.get_part_bits(*self.item['symbols'])]

    def __get_repeat(self):
        return self.Repeat[self.get_part_bits(*self.item['repeat'])]

    def __get_qam_bits(self):
        return self.QamBits[self.get_part_bits(*self.item['qam_bits'])]

    def get_part_bits(self, address, start, end):
        if end == -1:
            return reg.GetBit(address=address, bit=start)
        return Utility.convert2bin(reg.GetByte(address))[7 - end:8 - start]
