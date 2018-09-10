# encoding: utf-8
from lib.UserInterface.Dialog import DialogBase
import wx
from lib.Config import Instrument
from lib.ProtocolStack import Configuration
from ObjectBase import ObjectBase
from lib import Utility
import logging

logger = logging.getLogger(__name__)
reg = Instrument.get_register()
PS_configs = [
    Configuration.user_interleave_config, Configuration.br_interleave_config,
    Configuration.user_bandwidth_config, Configuration.br_cs_bandwidth_config,
    Configuration.clear_config, Configuration.lock_config,
    Configuration.reset_config, Configuration.MCS_config,
    Configuration.antenna_mode_config,
    Configuration.slot_mimo_mode_config,
]


class ProtocolStackDialog(DialogBase.DialogWindow):
    def __init__(self, name=u"基带设置", size=(790, 673)):
        DialogBase.DialogWindow.__init__(self, name=name, size=size)
        self.panel = Panel(self)
        self.panel.Refresh()


class Panel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                          style=wx.TAB_TRAVERSAL)
        self.font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, underline=True)
        self.title_size = (70, -1)
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        FourthRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        SecondRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        ThirdRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        InterleaverSizer = self.__init_interleaver_sizer()
        MCS_Sizer = self.__init_MCS_sizer()
        BandwidthSizer = self.__init_bandwidth_sizer()
        SlotMIMO_Sizer = self.__init_slot_mimo_sizer()
        LockSizer = self.__init_lock_sizer()
        ClearSizer = self.__init_clear_sizer()
        ButtonSizer = self.__init_button_sizer()
        ResetSizer = self.__init_reset_sizer()
        LeftMiddleSizer = wx.BoxSizer(wx.VERTICAL)
        FirstRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        FirstRowSizer.Add(ResetSizer, 0, wx.EXPAND | wx.LEFT, 5)
        FirstRowSizer.Add(LockSizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 3)
        FirstRowSizer.Add(ClearSizer, 0, wx.EXPAND | wx.RIGHT, 5)

        FourthRowSizer.Add(InterleaverSizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        SecondRowSizer.Add(BandwidthSizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        ThirdRowSizer.Add(MCS_Sizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        LeftMiddleSizer.Add(SecondRowSizer, 0, wx.EXPAND | wx.ALL, 0)
        LeftMiddleSizer.Add(ThirdRowSizer, 0, wx.EXPAND | wx.ALL, 0)
        MiddleSizer = wx.BoxSizer(wx.HORIZONTAL)
        MiddleSizer.Add(LeftMiddleSizer, 0, wx.EXPAND | wx.ALL, 0)
        MiddleSizer.Add(ButtonSizer, 1, wx.EXPAND | wx.RIGHT, 5)

        MainSizer.Add(FirstRowSizer, 0, wx.EXPAND | wx.ALL, 0)
        MainSizer.Add(MiddleSizer, 0, wx.EXPAND | wx.ALL, 0)
        MainSizer.Add(FourthRowSizer, 0, wx.EXPAND | wx.ALL, 0)

        MainSizer.Add(SlotMIMO_Sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        self.SetSizer(MainSizer)
        self.Layout()

    def Refresh(self):
        if not reg.IsConnect():
            Utility.AlertError(u"无法获取寄存器，请检查：\n\t1.是否连接寄存器并给寄存器上电。\n\t2.是否打开了其他占用寄存器的应用。\n\t3.驱动是否安装正确。")
            return False
        for config in PS_configs:
            if type(config) == list:
                for item in config:
                    self.__getattribute__(item['name']).refresh()
            elif type(config) == dict:
                self.__getattribute__(config['name']).refresh()

    def on_TODO(self, event):
        pass

    def on_refresh(self, event):
        self.Refresh()

    def __init_button_sizer(self):
        button_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.VERTICAL)
        refresh_button = wx.Button(self, wx.ID_ANY, u"刷新", wx.DefaultPosition, wx.DefaultSize, 0)
        import_button = wx.Button(self, wx.ID_ANY, u"导入", wx.DefaultPosition, wx.DefaultSize, 0)
        export_button = wx.Button(self, wx.ID_ANY, u"导出", wx.DefaultPosition, wx.DefaultSize, 0)
        close_button = wx.Button(self, wx.ID_ANY, u"关闭", wx.DefaultPosition, wx.DefaultSize, 0)
        refresh_button.Bind(wx.EVT_BUTTON, self.on_refresh)
        import_button.Bind(wx.EVT_BUTTON, self.on_refresh)
        export_button.Bind(wx.EVT_BUTTON, self.on_refresh)
        close_button.Bind(wx.EVT_BUTTON, self.on_refresh)
        button_sizer.Add(refresh_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 5)
        button_sizer.Add(import_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 5)
        button_sizer.Add(export_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 5)
        button_sizer.Add(close_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 5)
        import_button.Disable()
        export_button.Disable()
        return button_sizer

    def __init_interleaver_sizer(self):
        InterleaverSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.HORIZONTAL)
        TitleSizer = wx.BoxSizer(wx.VERTICAL)
        title_interleaver_setting = wx.StaticText(self, wx.ID_ANY, u"交织设置", wx.DefaultPosition, self.title_size, 0)
        title_interleaver_setting.SetFont(self.font)
        title_total = wx.StaticText(self, wx.ID_ANY, u"符号总个数：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        title_mode = wx.StaticText(self, wx.ID_ANY, u"  交织模式：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        title_count = wx.StaticText(self, wx.ID_ANY, u"交织块个数：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        TitleSizer.Add(title_interleaver_setting, 0, wx.ALIGN_LEFT | wx.TOP, 10)
        TitleSizer.Add(title_total, 0, wx.ALIGN_CENTER | wx.TOP, 16)
        TitleSizer.Add(title_mode, 0, wx.ALIGN_CENTER | wx.TOP, 16)
        TitleSizer.Add(title_count, 0, wx.ALIGN_CENTER | wx.TOP, 16)
        InterleaverSizer.Add(TitleSizer, 0, wx.ALL, 0)
        for item in Configuration.user_interleave_config:
            self.__setattr__(item['name'], UserInterleave(self, item))
            sizer = self.__getattribute__(item['name']).get_sizer()
            InterleaverSizer.Add(sizer, 0, wx.ALL, 0)
        for item in Configuration.br_interleave_config:
            self.__setattr__(item['name'], BrInterleave(self, item))
            sizer = self.__getattribute__(item['name']).get_sizer()
            InterleaverSizer.Add(sizer, 0, wx.ALL, 0)
        return InterleaverSizer

    def __init_MCS_sizer(self):
        Sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.HORIZONTAL)
        TitleSizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, wx.ID_ANY, u"调制编码", wx.DefaultPosition, self.title_size, 0)
        title.SetFont(self.font)
        title_modulation = wx.StaticText(self, wx.ID_ANY, u"调制：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        title_coding = wx.StaticText(self, wx.ID_ANY, u"编码：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        title_repeat = wx.StaticText(self, wx.ID_ANY, u"重复：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        TitleSizer.Add(title, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        TitleSizer.Add(title_modulation, 0, wx.ALIGN_CENTER | wx.TOP, 16)
        TitleSizer.Add(title_coding, 0, wx.ALIGN_CENTER | wx.TOP, 16)
        TitleSizer.Add(title_repeat, 0, wx.ALIGN_CENTER | wx.TOP, 16)
        Sizer.Add(TitleSizer, 0, wx.ALL, 0)
        for item in Configuration.MCS_config:
            self.__setattr__(item['name'], ModulationCodingSchemeSetting(self, item))
            sizer = self.__getattribute__(item['name']).get_sizer()
            Sizer.Add(sizer, 0, wx.ALL, 0)
        return Sizer

    def __init_bandwidth_sizer(self):
        Sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.HORIZONTAL)
        TitleSizer = wx.BoxSizer(wx.VERTICAL)
        title_name = wx.StaticText(self, wx.ID_ANY, u"带宽设置", wx.DefaultPosition, self.title_size, 0)
        title_name.SetFont(self.font)
        title_recv = wx.StaticText(self, wx.ID_ANY, u"接收：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        title_send = wx.StaticText(self, wx.ID_ANY, u"发送：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        TitleSizer.Add(title_name, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        TitleSizer.Add(title_send, 0, wx.ALIGN_CENTER | wx.TOP, 16)
        TitleSizer.Add(title_recv, 0, wx.ALIGN_CENTER | wx.TOP, 16)
        Sizer.Add(TitleSizer, 0, wx.ALL, 0)
        self.__setattr__(Configuration.br_cs_bandwidth_config['name'],
                         BR_CS_BandwidthSetting(self, Configuration.br_cs_bandwidth_config))
        br_cs_sizer = self.__getattribute__(Configuration.br_cs_bandwidth_config['name']).get_sizer()
        for item in Configuration.user_bandwidth_config:
            self.__setattr__(item['name'], UserBandwidthSetting(self, item))
            sizer = self.__getattribute__(item['name']).get_sizer()
            Sizer.Add(sizer, 0, wx.ALL, 0)
        Sizer.Add(br_cs_sizer, 0, wx.ALL, 0)
        return Sizer

    def __init_slot_mimo_sizer(self):
        Sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.VERTICAL)
        TitleSizer = wx.BoxSizer(wx.VERTICAL)
        title_name = wx.StaticText(self, wx.ID_ANY, u"MIMO模式", wx.DefaultPosition, self.title_size, 0)

        title_name.SetFont(self.font)
        TitleSizer.Add(title_name, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        Sizer.Add(TitleSizer, 0, wx.ALL, 0)
        self.__setattr__(Configuration.antenna_mode_config['name'],
                         AntennaModeSetting(self, Configuration.antenna_mode_config))
        antenna_mode_sizer = self.__getattribute__(Configuration.antenna_mode_config['name']).get_sizer()
        self.__setattr__(Configuration.slot_mimo_mode_config['name'],
                         SlotMimoModeSetting(self, Configuration.slot_mimo_mode_config))
        user_sizer = self.__getattribute__(Configuration.slot_mimo_mode_config['name']).get_sizer()
        Sizer.Add(antenna_mode_sizer, 0, wx.ALL, 0)
        Sizer.Add(user_sizer, 0, wx.ALL, 0)
        return Sizer

    def __init_lock_sizer(self):
        Sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.VERTICAL)
        TitleSizer = wx.BoxSizer(wx.VERTICAL)
        title_name = wx.StaticText(self, wx.ID_ANY, u"UNLOCK", wx.DefaultPosition, wx.DefaultSize, 0)

        title_name.SetFont(self.font)
        TitleSizer.Add(title_name, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        Sizer.Add(TitleSizer, 0, wx.ALL, 0)
        LockSizerContainer = wx.BoxSizer(wx.HORIZONTAL)
        for item in Configuration.lock_config:
            self.__setattr__(item['name'], LockSetting(self, item))
            lock_sizer = self.__getattribute__(item['name']).get_sizer()
            LockSizerContainer.Add(lock_sizer, 0, wx.ALL, 0)
        Sizer.Add(LockSizerContainer, 0, wx.LEFT, 5)
        return Sizer

    def __init_clear_sizer(self):
        Sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.VERTICAL)
        TitleSizer = wx.BoxSizer(wx.VERTICAL)
        title_name = wx.StaticText(self, wx.ID_ANY, u"CLEAR", wx.DefaultPosition, wx.DefaultSize, 0)

        title_name.SetFont(self.font)
        TitleSizer.Add(title_name, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        Sizer.Add(TitleSizer, 0, wx.ALL, 0)
        ClearSizerContainer = wx.BoxSizer(wx.HORIZONTAL)
        for item in Configuration.clear_config:
            self.__setattr__(item['name'], ClearSetting(self, item))
            clear_sizer = self.__getattribute__(item['name']).get_sizer()
            ClearSizerContainer.Add(clear_sizer, 0, wx.ALL, 0)
        Sizer.Add(ClearSizerContainer, 0, wx.LEFT, 5)
        return Sizer

    def __init_reset_sizer(self):
        Sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.VERTICAL)
        TitleSizer = wx.BoxSizer(wx.VERTICAL)
        title_name = wx.StaticText(self, wx.ID_ANY, u"RESET", wx.DefaultPosition, wx.DefaultSize, 0)

        title_name.SetFont(self.font)
        TitleSizer.Add(title_name, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        Sizer.Add(TitleSizer, 0, wx.ALL, 0)
        for item in Configuration.reset_config:
            self.__setattr__(item['name'], ResetSetting(self, item))
            reset_sizer = self.__getattribute__(item['name']).get_sizer()
            Sizer.Add(reset_sizer, 0, wx.LEFT | wx.TOP, 1)
        return Sizer


class UserInterleave(ObjectBase):
    def __init__(self, panel, item):
        ObjectBase.__init__(self, item=item)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.item = item
        title_name = wx.StaticText(panel, wx.ID_ANY, item["title"], wx.DefaultPosition, wx.DefaultSize, 0)
        t = ['12', '24', '48', '96']
        m = ['12', '24', '48']
        width = 57
        self.total_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), t, 0)
        self.total_choice.Bind(wx.EVT_CHOICE, self.update_total)
        self.mode_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), m, 0)
        self.mode_choice.Bind(wx.EVT_CHOICE, self.update_mode)
        self.text_ctrl = wx.TextCtrl(panel, wx.ID_ANY, "", wx.DefaultPosition, (width, -1),
                                     wx.TE_LEFT | wx.TE_READONLY)

        self.sizer.Add(title_name, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        self.sizer.Add(self.total_choice, 0, wx.ALL, 5)
        self.sizer.Add(self.mode_choice, 0, wx.ALL, 5)
        self.sizer.Add(self.text_ctrl, 0, wx.ALL, 5)
        self.total = item['total']
        self.mode = item['mode']
        self.dict_mapping_t = {
            u'12': '001',
            u'24': '011',
            u'48': '100',
            u'96': '101',
        }
        self.dict_t = {v: k for k, v in self.dict_mapping_t.items()}
        self.dict_mapping_m = {
            u'12': '101',
            u'24': '110',
            u'48': '111',
        }
        self.dict_m = {v: k for k, v in self.dict_mapping_m.items()}

    def refresh(self):
        t_a, t_s, t_e = self.total
        m_a, m_s, m_e = self.mode
        t_value = Utility.convert2bin(reg.GetByte(t_a))[7 - t_e:8 - t_s]
        m_value = Utility.convert2bin(reg.GetByte(m_a))[7 - m_e:8 - m_s]
        self.SetStringSelection(selection=self.dict_t.get(t_value, None), wx_choice=self.total_choice)
        self.SetStringSelection(selection=self.dict_m.get(m_value, None), wx_choice=self.mode_choice)
        self.update_tc_value()

    def get_sizer(self):
        return self.sizer

    def update_total(self, event):
        change_value = self.dict_mapping_t[self.total_choice.GetStringSelection()]

        address, start, end = self.total
        byte = reg.GetByte(address=address)
        byte = Utility.replace_bits(byte=byte, need_replace=change_value, start=start)
        reg.SetByte(address=address, byte=int(byte, 2))
        t_a, t_s, t_e = self.total
        t_value = Utility.convert2bin(reg.GetByte(t_a))[7 - t_e:8 - t_s]
        self.SetStringSelection(selection=self.dict_t.get(t_value, None), wx_choice=self.total_choice)
        self.update_tc_value()

    def update_mode(self, event):
        change_value = self.dict_mapping_m[self.mode_choice.GetStringSelection()]
        address, start, end = self.mode
        byte = reg.GetByte(address=address)
        byte = Utility.replace_bits(byte=byte, need_replace=change_value, start=start)
        reg.SetByte(address=address, byte=int(byte, 2))
        m_a, m_s, m_e = self.mode
        m_value = Utility.convert2bin(reg.GetByte(m_a))[7 - m_e:8 - m_s]
        self.SetStringSelection(selection=self.dict_m.get(m_value, None), wx_choice=self.mode_choice)
        self.update_tc_value()

    def update_tc_value(self):
        total = self.total_choice.GetStringSelection()
        mode = self.mode_choice.GetStringSelection()
        if total and mode:
            self.text_ctrl.SetValue(str(int(total) / int(mode)))
        else:
            self.text_ctrl.SetValue('')


# class UserInterleave(ObjectBase):
#     def __init__(self, panel, item):
#         ObjectBase.__init__(self, item=item)
#         self.sizer = wx.BoxSizer(wx.VERTICAL)
#         self.item = item
#         title_name = wx.StaticText(panel, wx.ID_ANY, item["title"], wx.DefaultPosition, wx.DefaultSize, 0)
#         t = ['12', '24', '48', '96']
#         m = ['12', '24', '48']
#         width = 70
#         self.total_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), t, 0)
#         self.total_choice.Bind(wx.EVT_CHOICE, self.update_total)
#         self.mode_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), m, 0)
#         self.mode_choice.Bind(wx.EVT_CHOICE, self.update_mode)
#         self.text_ctrl = wx.TextCtrl(panel, wx.ID_ANY, "1152", wx.DefaultPosition, (width, -1),
#                                      wx.TE_LEFT | wx.TE_READONLY)
#
#         self.sizer.Add(title_name, 0, wx.ALIGN_CENTER | wx.TOP, 10)
#         self.sizer.Add(self.total_choice, 0, wx.ALL, 5)
#         self.sizer.Add(self.mode_choice, 0, wx.ALL, 5)
#         self.sizer.Add(self.text_ctrl, 0, wx.ALL, 5)
#         self.total_users = [item['total_address']['user%s' % x] for x in range(4)]
#         self.mode_users = [item['mode_address']['user%s' % x] for x in range(4)]
#         self.dict_mapping_t = {
#             u'12': '001',
#             u'24': '011',
#             u'48': '100',
#             u'96': '101',
#         }
#         self.dict_t = {v: k for k, v in self.dict_mapping_t.items()}
#         self.dict_mapping_m = {
#             u'12': '101',
#             u'24': '110',
#             u'48': '111',
#         }
#         self.dict_m = {v: k for k, v in self.dict_mapping_m.items()}
#
#     def refresh(self):
#         t_a, t_s, t_e = self.total_users[0]  # total _ address _start_bit _end_bit
#         m_a, m_s, m_e = self.mode_users[0]  # mode
#         t_value = Utility.convert2bin(reg.GetByte(t_a))[7 - t_e:8 - t_s]
#         m_value = Utility.convert2bin(reg.GetByte(m_a))[7 - m_e:8 - m_s]
#         self.SetStringSelection(selection=self.dict_t.get(t_value, None), wx_choice=self.total_choice)
#         self.SetStringSelection(selection=self.dict_m.get(m_value, None), wx_choice=self.mode_choice)
#         self.update_tc_value()
#
#     def get_sizer(self):
#         return self.sizer
#
#     def update_total(self, event):
#         change_value = self.dict_mapping_t[self.total_choice.GetStringSelection()]
#         for user in self.total_users:
#             address, start, end = user
#             byte = reg.GetByte(address=address)
#             byte = Utility.replace_bits(byte=byte, need_replace=change_value, start=start)
#             reg.SetByte(address=address, byte=int(byte, 2))
#         self.update_tc_value()
#
#     def update_mode(self, event):
#         change_value = self.dict_mapping_m[self.mode_choice.GetStringSelection()]
#         for user in self.mode_users:
#             address, start, end = user
#             byte = reg.GetByte(address=address)
#             byte = Utility.replace_bits(byte=byte, need_replace=change_value, start=start)
#             reg.SetByte(address=address, byte=int(byte, 2))
#         self.update_tc_value()
#
#     def update_tc_value(self):
#         total = self.total_choice.GetStringSelection()
#         mode = self.mode_choice.GetStringSelection()
#         if total and mode:
#             self.text_ctrl.SetValue(str(int(total) * int(mode)))
#         else:
#             self.text_ctrl.SetValue('')


class BrInterleave(ObjectBase):
    def __init__(self, panel, item):
        ObjectBase.__init__(self, item=item)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.item = item
        title_name = wx.StaticText(panel, wx.ID_ANY, item["title"], wx.DefaultPosition, wx.DefaultSize, 0)
        t = ['6', '12', '24']
        m = []
        width = 57
        self.total_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), t, 0)
        self.total_choice.Bind(wx.EVT_CHOICE, self.update_total)
        self.mode_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), m, 0)
        self.text_ctrl = wx.TextCtrl(panel, wx.ID_ANY, "", wx.DefaultPosition, (width, -1),
                                     wx.TE_LEFT | wx.TE_READONLY)
        self.mode_choice.Disable()
        self.text_ctrl.Disable()
        self.sizer.Add(title_name, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        self.sizer.Add(self.total_choice, 0, wx.ALL, 5)
        self.sizer.Add(self.mode_choice, 0, wx.ALL, 5)
        self.sizer.Add(self.text_ctrl, 0, wx.ALL, 5)
        self.total = item['total_address']
        self.dict_mapping_t = {
            '6': '000',
            '12': '001',
            '24': '011',
        }
        self.dict_t = {v: k for k, v in self.dict_mapping_t.items()}

    def refresh(self):
        total, start, end = self.total  # total _ address _start_bit _end_bit
        value = Utility.convert2bin(reg.GetByte(total))[7 - end:8 - start]
        self.SetStringSelection(self.dict_t.get(value, None), self.total_choice)

    def get_sizer(self):
        return self.sizer

    def update_total(self, event):
        change_value = self.dict_mapping_t[self.total_choice.GetStringSelection()]
        address, start, end = self.total
        byte = reg.GetByte(address=address)
        byte = Utility.replace_bits(byte=byte, need_replace=change_value, start=start)
        reg.SetByte(address=address, byte=int(byte, 2))
        self.refresh()


class ModulationCodingSchemeSetting(ObjectBase):
    def __init__(self, panel, item):
        ObjectBase.__init__(self, item=item)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.item = item
        name = item['name']

        modulations = ['BPSK', 'QPSK', '16QAM', '64QAM', '256QAM'] if name.startswith("user") else ['BPSK', 'QPSK']
        codings = ['1/2', '2/3A', '2/3B', '3/4A', '3/4B', '5/6'] if name.startswith("user") else ['1/2', '2/3']
        repeats = ['T:1 | F:1', 'T:1 | F:2', 'T:1 | F:4', 'T:2 | F:1', 'T:2 | F:2', 'T:2 | F:4', 'T:4 | F:1',
                   'T:4 | F:2']

        width = 75
        title_name = wx.StaticText(panel, wx.ID_ANY, item["title"], wx.DefaultPosition, wx.DefaultSize, 0)
        self.modulation_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), modulations, 0)
        self.modulation_choice.Bind(wx.EVT_CHOICE, self.update_modulation)
        self.encoding_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), codings, 0)
        self.encoding_choice.Bind(wx.EVT_CHOICE, self.update_encoding)
        self.repeat_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), repeats, 0)
        self.repeat_choice.Bind(wx.EVT_CHOICE, self.update_repeat)
        self.sizer.Add(title_name, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        self.sizer.Add(self.modulation_choice, 0, wx.ALL, 5)
        self.sizer.Add(self.encoding_choice, 0, wx.ALL, 5)
        self.sizer.Add(self.repeat_choice, 0, wx.ALL, 5)
        self.modem = item['modem']
        self.encode = item['encode']
        self.repeat = item['repeat']
        self.dict_mapping_modulations = {
            'BPSK': '000',
            'QPSK': '001',
            '16QAM': '010',
            '64QAM': '011',
            '256QAM': '100'
        }
        self.dict_mapping_codings = {
            '1/2': '000',
            '2/3': '001',
            '2/3A': '001',
            '2/3B': '010',
            '3/4A': '011',
            '3/4B': '100',
            '5/6': '101'
        }
        self.dict_mapping_repeats = {
            'T:1 | F:1': '000',
            'T:1 | F:2': '001',
            'T:1 | F:4': '010',
            'T:2 | F:1': '011',
            'T:2 | F:2': '100',
            'T:2 | F:4': '101',
            'T:4 | F:1': '110',
            'T:4 | F:2': '111',
        }

    def get_sizer(self):
        return self.sizer

    def refresh(self):
        modem = self.get_part_bits(*self.modem)
        self.SetSelection(modem, self.modulation_choice)
        encode = self.get_part_bits(*self.encode)
        self.SetSelection(encode, self.encoding_choice)
        repeat = self.get_part_bits(*self.repeat)
        self.SetSelection(repeat, self.repeat_choice)

    def get_part_bits(self, address, start, end):
        if end == -1:
            return reg.GetBit(address=address, bit=start)
        return Utility.convert2bin(reg.GetByte(address))[7 - end:8 - start]

    def SetSelection(self, n, wx_choice):
        n = int(n, 2)
        c = len(wx_choice.Items)
        if n > c:
            wx_choice.SetSelection(wx.NOT_FOUND)
        else:
            wx_choice.SetSelection(n)

    def update_modulation(self, event):
        address, start, end = self.modem
        n = self.modulation_choice.GetSelection()
        self.__update(value=n, start=start, end=end, address=address)
        modem = self.get_part_bits(*self.modem)
        self.SetSelection(modem, self.modulation_choice)

    def update_encoding(self, event):
        address, start, end = self.encode
        n = self.encoding_choice.GetSelection()
        self.__update(value=n, start=start, end=end, address=address)
        encode = self.get_part_bits(*self.encode)
        self.SetSelection(encode, self.encoding_choice)

    def update_repeat(self, event):
        address, start, end = self.repeat
        n = self.repeat_choice.GetSelection()
        self.__update(value=n, start=start, end=end, address=address)
        repeat = self.get_part_bits(*self.repeat)
        self.SetSelection(repeat, self.repeat_choice)

    def __update(self, value, address, start, end):
        bits = self.__convert2bits(value=value, start=start, end=end)
        byte = reg.GetByte(address=address)
        byte = Utility.replace_bits(byte=byte, start=start, need_replace=bits)
        reg.SetByte(address=address, byte=int(byte, 2))

    def __convert2bits(self, value, start, end):
        if end == -1:
            return str(value)
        else:
            length = end - start + 1
            bits = bin(value)[2:]
            if len(bits) > length:
                logger.error('bits:%s' % bits)
                return ''
            else:
                return (length - len(bits)) * '0' + bits


class BR_CS_BandwidthSetting(ObjectBase):
    def __init__(self, panel, item):
        ObjectBase.__init__(self, item=item)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        br_sizer = wx.BoxSizer(wx.VERTICAL)
        cs_sizer = wx.BoxSizer(wx.VERTICAL)
        self.item = item
        bandwidth = ['2.5MHz', '5MHz', '10MHz', '20MHz']  # , '40MHz'
        self.dict_mapping_bandwidth = {
            u'2.5MHz': '001',
            u'5MHz': '010',
            u'10MHz': '011',
            u'20MHz': '100',
            # u'40MHz': '101',
        }
        self.dict_bandwidth = {v: k for k, v in self.dict_mapping_bandwidth.items()}
        self.br = item['BR']
        self.cs = item['CS']
        self.br_recv = self.br['recv_address']
        self.cs_recv = self.cs['recv_address']
        self.send = self.cs['send_address']
        width = 75
        br_title_name = wx.StaticText(panel, wx.ID_ANY, self.br["title"], wx.DefaultPosition, wx.DefaultSize, 0)
        cs_title_name = wx.StaticText(panel, wx.ID_ANY, self.cs["title"], wx.DefaultPosition, wx.DefaultSize, 0)
        self.br_recv_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), bandwidth, 0)
        self.br_recv_choice.Bind(wx.EVT_CHOICE, self.update_br_recv)
        self.br_send_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), bandwidth, 0)
        self.br_send_choice.Bind(wx.EVT_CHOICE, self.update_send)
        self.cs_recv_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), bandwidth, 0)
        self.cs_recv_choice.Bind(wx.EVT_CHOICE, self.update_cs_recv)
        self.cs_send_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), bandwidth, 0)
        self.cs_send_choice.Bind(wx.EVT_CHOICE, self.update_send)

        br_sizer.Add(br_title_name, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        br_sizer.Add(self.br_send_choice, 0, wx.ALL, 5)
        br_sizer.Add(self.br_recv_choice, 0, wx.ALL, 5)
        cs_sizer.Add(cs_title_name, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        cs_sizer.Add(self.cs_send_choice, 0, wx.ALL, 5)
        cs_sizer.Add(self.cs_recv_choice, 0, wx.ALL, 5)
        self.sizer.Add(br_sizer, 0, wx.ALL, 0)
        self.sizer.Add(cs_sizer, 0, wx.ALL, 0)

    def refresh(self):
        br_rx_address, br_rx_start, br_rx_end = self.br_recv
        cs_rx_address, cs_rx_start, cs_rx_end = self.cs_recv
        tx_address, tx_start, tx_end = self.send

        br_rx_value = Utility.convert2bin(reg.GetByte(br_rx_address))[7 - br_rx_end:8 - br_rx_start]
        cs_rx_value = Utility.convert2bin(reg.GetByte(cs_rx_address))[7 - cs_rx_end:8 - cs_rx_start]
        tx_value = Utility.convert2bin(reg.GetByte(tx_address))[7 - tx_end:8 - tx_start]

        self.SetStringSelection(selection=self.dict_bandwidth.get(br_rx_value, None), wx_choice=self.br_recv_choice)
        self.SetStringSelection(selection=self.dict_bandwidth.get(cs_rx_value, None), wx_choice=self.cs_recv_choice)
        self.SetStringSelection(selection=self.dict_bandwidth.get(tx_value, None), wx_choice=self.br_send_choice)
        self.SetStringSelection(selection=self.dict_bandwidth.get(tx_value, None), wx_choice=self.cs_send_choice)

    def get_sizer(self):
        return self.sizer

    def update_br_recv(self, event):
        change_value = self.dict_mapping_bandwidth[self.br_recv_choice.GetStringSelection()]
        address, start, end = self.br_recv
        byte = reg.GetByte(address=address)
        byte = Utility.replace_bits(byte=byte, need_replace=change_value, start=start)
        reg.SetByte(address=address, byte=int(byte, 2))
        self.refresh()

    def update_cs_recv(self, event):
        change_value = self.dict_mapping_bandwidth[self.cs_recv_choice.GetStringSelection()]
        address, start, end = self.cs_recv
        byte = reg.GetByte(address=address)
        byte = Utility.replace_bits(byte=byte, need_replace=change_value, start=start)
        reg.SetByte(address=address, byte=int(byte, 2))
        self.refresh()

    def update_send(self, event):
        obj = event.GetEventObject()
        selection = obj.GetStringSelection()
        self.br_send_choice.SetStringSelection(selection)
        self.cs_send_choice.SetStringSelection(selection)
        change_value = self.dict_mapping_bandwidth[selection]
        address, start, end = self.send
        byte = reg.GetByte(address=address)
        byte = Utility.replace_bits(byte=byte, need_replace=change_value, start=start)
        reg.SetByte(address=address, byte=int(byte, 2))
        self.refresh()


class UserBandwidthSetting(ObjectBase):
    def __init__(self, panel, item):
        ObjectBase.__init__(self, item=item)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.item = item
        bandwidth = ['2.5MHz', '5MHz', '10MHz', '20MHz']  # , '40MHz'
        # TODO
        # ERROR 增加不匹配的情况
        self.dict_mapping_bandwidth = {
            u'2.5MHz': '001',
            u'5MHz': '010',
            u'10MHz': '011',
            u'20MHz': '100',
            # u'40MHz': '101',
        }
        self.recv_user = item['recv_address']
        self.send_user = item['send_address']
        self.dict_bandwidth = {v: k for k, v in self.dict_mapping_bandwidth.items()}
        width = 75
        title_name = wx.StaticText(panel, wx.ID_ANY, item["title"], wx.DefaultPosition, wx.DefaultSize, 0)
        self.recv_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), bandwidth, 0)
        self.recv_choice.Bind(wx.EVT_CHOICE, self.update_recv)
        self.send_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), bandwidth, 0)
        self.send_choice.Bind(wx.EVT_CHOICE, self.update_send)
        self.sizer.Add(title_name, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        self.sizer.Add(self.send_choice, 0, wx.ALL, 5)
        self.sizer.Add(self.recv_choice, 0, wx.ALL, 5)

    def refresh(self):
        self.__refresh(wx_choice=self.recv_choice, config=self.recv_user)
        self.__refresh(wx_choice=self.send_choice, config=self.send_user)
        # rx_address, rx_start, rx_end = self.recv_user
        # tx_address, tx_start, tx_end = self.send_user
        # rx_value = Utility.convert2bin(reg.GetByte(rx_address))[7 - rx_end:8 - rx_start]
        # tx_value = Utility.convert2bin(reg.GetByte(tx_address))[7 - tx_end:8 - tx_start]
        # self.SetStringSelection(selection=self.dict_bandwidth.get(rx_value, None), wx_choice=self.recv_choice)
        # self.SetStringSelection(selection=self.dict_bandwidth.get(tx_value, None), wx_choice=self.send_choice)

    def __refresh(self, wx_choice, config):
        address, start, end = config
        value = Utility.convert2bin(reg.GetByte(address))[7 - end:8 - start]
        self.SetStringSelection(selection=self.dict_bandwidth.get(value, None), wx_choice=wx_choice)

    def get_sizer(self):
        return self.sizer

    def update_recv(self, event):
        change_value = self.dict_mapping_bandwidth[self.recv_choice.GetStringSelection()]
        address, start, end = self.recv_user
        byte = reg.GetByte(address=address)
        byte = Utility.replace_bits(byte=byte, need_replace=change_value, start=start)
        reg.SetByte(address=address, byte=int(byte, 2))
        self.__refresh(wx_choice=self.recv_choice, config=self.recv_user)

    def update_send(self, event):
        change_value = self.dict_mapping_bandwidth[self.send_choice.GetStringSelection()]
        address, start, end = self.send_user
        byte = reg.GetByte(address=address)
        byte = Utility.replace_bits(byte=byte, need_replace=change_value, start=start)
        reg.SetByte(address=address, byte=int(byte, 2))
        self.__refresh(wx_choice=self.send_choice, config=self.send_user)


# class UserBandwidthSetting(ObjectBase):
#     def __init__(self, panel, item):
#         ObjectBase.__init__(self, item=item)
#         self.sizer = wx.BoxSizer(wx.VERTICAL)
#         self.item = item
#         bandwidth = ['2.5MHz', '5MHz', '10MHz', '20MHz', '40MHz']
#         self.dict_mapping_bandwidth = {
#             u'2.5MHz': '001',
#             u'5MHz': '010',
#             u'10MHz': '011',
#             u'20MHz': '100',
#             u'40MHz': '101',
#         }
#         self.recv_users = [item['recv_address']['user%s' % x] for x in range(4)]
#         self.send_users = [item['send_address']['user%s' % x] for x in range(4)]
#         self.dict_bandwidth = {v: k for k, v in self.dict_mapping_bandwidth.items()}
#         width = 60
#         title_name = wx.StaticText(panel, wx.ID_ANY, item["title"], wx.DefaultPosition, wx.DefaultSize, 0)
#         self.recv_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), bandwidth, 0)
#         self.recv_choice.Bind(wx.EVT_CHOICE, self.update_recv)
#         self.send_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), bandwidth, 0)
#         self.send_choice.Bind(wx.EVT_CHOICE, self.update_send)
#         self.sizer.Add(title_name, 0, wx.ALIGN_CENTER | wx.TOP, 10)
#         self.sizer.Add(self.send_choice, 0, wx.ALL, 5)
#         self.sizer.Add(self.recv_choice, 0, wx.ALL, 5)
#
#     def refresh(self):
#         rx_address, rx_start, rx_end = self.recv_users[0]  # total _ address _start_bit _end_bit
#         tx_address, tx_start, tx_end = self.send_users[0]  # mode
#         rx_value = Utility.convert2bin(reg.GetByte(rx_address))[7 - rx_end:8 - rx_start]
#         tx_value = Utility.convert2bin(reg.GetByte(tx_address))[7 - tx_end:8 - tx_start]
#         self.SetStringSelection(selection=self.dict_bandwidth.get(rx_value, None), wx_choice=self.recv_choice)
#         self.SetStringSelection(selection=self.dict_bandwidth.get(tx_value, None), wx_choice=self.send_choice)
#
#     def get_sizer(self):
#         return self.sizer
#
#     def update_recv(self, event):
#         change_value = self.dict_mapping_bandwidth[self.recv_choice.GetStringSelection()]
#         for user in self.recv_users:
#             address, start, end = user
#             byte = reg.GetByte(address=address)
#             byte = Utility.replace_bits(byte=byte, need_replace=change_value, start=start)
#             reg.SetByte(address=address, byte=int(byte, 2))
#
#     def update_send(self, event):
#         change_value = self.dict_mapping_bandwidth[self.send_choice.GetStringSelection()]
#         for user in self.send_users:
#             address, start, end = user
#             byte = reg.GetByte(address=address)
#             byte = Utility.replace_bits(byte=byte, need_replace=change_value, start=start)
#             reg.SetByte(address=address, byte=int(byte, 2))
#

class AntennaModeSetting(ObjectBase):
    def __init__(self, panel, item):
        ObjectBase.__init__(self, item=item)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.item = item
        send_ANT_choice = [u'1天线', u'2天线']
        recv_ANT_choice = [u'1天线', u'2天线', u'4天线']
        self.dict_mapping_send = {
            u'1天线': '0',
            u'2天线': '1',
        }
        self.dict_send = {v: k for k, v in self.dict_mapping_send.items()}
        self.dict_recv = {
            '00': u'1天线',
            '01': u'2天线',
            '10': u'4天线',
            '11': u'4天线',
        }
        send_title = item['send']['title']
        recv_title = item['recv']['title']
        self.send = item['send']['address']
        self.recv = item['recv']['address']
        SL = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        width = 60
        send_title = wx.StaticText(panel, wx.ID_ANY, send_title, wx.DefaultPosition, wx.DefaultSize, 0)
        recv_title = wx.StaticText(panel, wx.ID_ANY, recv_title, wx.DefaultPosition, wx.DefaultSize, 0)
        self.recv_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), recv_ANT_choice, 0)
        self.send_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), send_ANT_choice, 0)
        self.send_choice.Bind(wx.EVT_CHOICE, self.update_send)
        self.recv_choice.Disable()
        self.sizer.Add(send_title, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.sizer.Add(self.send_choice, 0, wx.ALL, 5)
        self.sizer.Add(SL, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        self.sizer.Add(recv_title, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.sizer.Add(self.recv_choice, 0, wx.ALL, 5)

    def get_sizer(self):
        return self.sizer

    def refresh(self):
        send_value = self.get_part_bits(*self.send)
        recv_value = self.get_part_bits(*self.recv)
        self.SetStringSelection(selection=self.dict_send.get(send_value, None), wx_choice=self.send_choice)
        self.SetStringSelection(selection=self.dict_recv.get(recv_value, None), wx_choice=self.recv_choice)

    def get_part_bits(self, address, start, end):
        if end == -1:
            return reg.GetBit(address=address, bit=start)
        return Utility.convert2bin(reg.GetByte(address))[7 - end:8 - start]

    def update_send(self, event):
        change_value = self.dict_mapping_send[self.send_choice.GetStringSelection()]
        address, start, end = self.send
        byte = reg.GetByte(address=address)
        byte = Utility.replace_bits(byte=byte, need_replace=change_value, start=start)
        reg.SetByte(address=address, byte=int(byte, 2))
        self.refresh()


class SlotMimoModeSetting(ObjectBase):
    def __init__(self, panel, item):
        ObjectBase.__init__(self, item=item)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.item = item
        slot_choice = ['1T1R', '1T2R', '1T4R', '2T2R', '2T4R']
        self.dict_mapping_slot = {
            '1T1R': '000',
            '1T2R': '010',
            '1T4R': '011',
            '2T2R': '100',
            '2T4R': '110',
        }
        self.dict_slot = {
            '000': '1T1R',
            '001': '1T1R',
            '010': '1T2R',
            '011': '1T4R',
            '100': '2T2R',
            '101': '2T2R',
            '110': '2T4R',
            '111': '2T4R',
        }
        width = 60
        SL1 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        SL2 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        SL3 = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        self.user0 = item['user0']
        self.user1 = item['user1']
        self.user2 = item['user2']
        self.user3 = item['user3']

        user0_title = wx.StaticText(panel, wx.ID_ANY, self.user0["title"], wx.DefaultPosition, wx.DefaultSize, 0)
        user1_title = wx.StaticText(panel, wx.ID_ANY, self.user1["title"], wx.DefaultPosition, wx.DefaultSize, 0)
        user2_title = wx.StaticText(panel, wx.ID_ANY, self.user2["title"], wx.DefaultPosition, wx.DefaultSize, 0)
        user3_title = wx.StaticText(panel, wx.ID_ANY, self.user3["title"], wx.DefaultPosition, wx.DefaultSize, 0)

        self.user0_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), slot_choice, 0)
        self.user1_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), slot_choice, 0)
        self.user2_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), slot_choice, 0)
        self.user3_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), slot_choice, 0)
        self.user0_choice.Bind(wx.EVT_CHOICE, self.update_user0)
        self.user1_choice.Bind(wx.EVT_CHOICE, self.update_user1)
        self.user2_choice.Bind(wx.EVT_CHOICE, self.update_user2)
        self.user3_choice.Bind(wx.EVT_CHOICE, self.update_user3)
        self.sizer.Add(user0_title, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.sizer.Add(self.user0_choice, 0, wx.ALL, 5)
        self.sizer.Add(SL1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 6)
        self.sizer.Add(user1_title, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.sizer.Add(self.user1_choice, 0, wx.ALL, 5)
        self.sizer.Add(SL2, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        self.sizer.Add(user2_title, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.sizer.Add(self.user2_choice, 0, wx.ALL, 5)
        self.sizer.Add(SL3, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        self.sizer.Add(user3_title, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.sizer.Add(self.user3_choice, 0, wx.ALL, 5)

    def get_sizer(self):
        return self.sizer

    def refresh(self):
        self.__refresh(self.user0, self.user0_choice)
        self.__refresh(self.user1, self.user1_choice)
        self.__refresh(self.user2, self.user2_choice)
        self.__refresh(self.user3, self.user3_choice)

    def update_user0(self, event):
        self.__update(self.user0, self.user0_choice)
        self.__refresh(self.user0, self.user0_choice)

    def update_user1(self, event):
        self.__update(self.user1, self.user1_choice)
        self.__refresh(self.user1, self.user1_choice)

    def update_user2(self, event):
        self.__update(self.user2, self.user2_choice)
        self.__refresh(self.user2, self.user2_choice)

    def update_user3(self, event):
        self.__update(self.user3, self.user3_choice)
        self.__refresh(self.user3, self.user3_choice)

    def __update(self, user, wx_choice):
        change_value = self.dict_mapping_slot[wx_choice.GetStringSelection()]
        address, start, end = user['address']
        byte = reg.GetByte(address=address)
        byte = Utility.replace_bits(byte=byte, need_replace=change_value, start=start)
        reg.SetByte(address=address, byte=int(byte, 2))

    def __refresh(self, user, wx_choice):
        value = self.get_part_bits(*user['address'])
        self.SetStringSelection(selection=self.dict_slot.get(value, None), wx_choice=wx_choice)

    def get_part_bits(self, address, start, end):
        if end == -1:
            return reg.GetBit(address=address, bit=start)
        return Utility.convert2bin(reg.GetByte(address))[7 - end:8 - start]


class LockSetting(ObjectBase):
    def __init__(self, panel, item):
        ObjectBase.__init__(self, item=item)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.item = item
        size = (53, -1)
        title = wx.StaticText(panel, wx.ID_ANY, self.item["title"], wx.DefaultPosition, size, 0)
        fch_name, self.fch = item['fch']
        slot_name, self.slot = item['slot']
        self.check_fch = wx.CheckBox(panel, wx.ID_ANY, fch_name, wx.DefaultPosition, size, 0)
        self.check_fch.Bind(wx.EVT_CHECKBOX, self.update_fch)
        self.check_slot = wx.CheckBox(panel, wx.ID_ANY, slot_name, wx.DefaultPosition, size, 0)
        self.check_slot.Bind(wx.EVT_CHECKBOX, self.update_slot)
        self.sizer.Add(title, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.sizer.Add(self.check_fch, 0, wx.ALL, 5)
        self.sizer.Add(self.check_slot, 0, wx.ALL, 5)

    def get_sizer(self):
        return self.sizer

    def refresh(self):
        self.__refresh(self.fch, self.check_fch)
        self.__refresh(self.slot, self.check_slot)

    def __refresh(self, config, wx_checkbox):
        address, start, end = config
        value = reg.GetBit(address=address, bit=start)
        self.SetCheck(value=value, wx_checkbox=wx_checkbox)

    def update_fch(self, event):
        address, start, end = self.fch
        reg.SetBit(address=address, bit=start, is_true=self.check_fch.GetValue())
        self.__refresh(self.fch, self.check_fch)

    def update_slot(self, event):
        address, start, end = self.slot
        reg.SetBit(address=address, bit=start, is_true=self.check_slot.GetValue())
        self.__refresh(self.slot, self.check_slot)


class ClearSetting(ObjectBase):
    def __init__(self, panel, item):
        ObjectBase.__init__(self, item=item)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.item = item
        size = (38, -1)
        title = wx.StaticText(panel, wx.ID_ANY, self.item["title"], wx.DefaultPosition, size, 0)
        self.rx = item['rx']
        self.tx = item['tx']
        self.check_rx = wx.CheckBox(panel, wx.ID_ANY, 'RX', wx.DefaultPosition, size, 0)
        self.check_rx.Bind(wx.EVT_CHECKBOX, self.update_rx)

        self.check_tx = wx.CheckBox(panel, wx.ID_ANY, 'TX', wx.DefaultPosition, size, 0)
        self.check_tx.Bind(wx.EVT_CHECKBOX, self.update_tx)
        self.sizer.Add(title, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.sizer.Add(self.check_rx, 0, wx.ALL, 5)
        self.sizer.Add(self.check_tx, 0, wx.ALL, 5)

    def get_sizer(self):
        return self.sizer

    def refresh(self):
        self.__refresh(self.rx, self.check_rx)
        self.__refresh(self.tx, self.check_tx)

    def __refresh(self, config, wx_checkbox):
        address, start, end = config
        value = reg.GetBit(address=address, bit=start)
        self.SetCheck(value=value, wx_checkbox=wx_checkbox)

    def update_rx(self, event):
        address, start, end = self.rx
        reg.SetBit(address=address, bit=start, is_true=self.check_rx.GetValue())
        self.__refresh(self.rx, self.check_rx)

    def update_tx(self, event):
        address, start, end = self.tx
        reg.SetBit(address=address, bit=start, is_true=self.check_tx.GetValue())
        self.__refresh(self.tx, self.check_tx)


class ResetSetting(ObjectBase):
    def __init__(self, panel, item):
        ObjectBase.__init__(self, item=item)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.item = item
        self.config = item['address']
        self.check_reset = wx.CheckBox(panel, wx.ID_ANY, self.item["title"], wx.DefaultPosition, wx.DefaultSize, 0)
        self.check_reset.Bind(wx.EVT_CHECKBOX, self.update)
        self.sizer.Add(self.check_reset, 0, wx.ALL, 5)

    def get_sizer(self):
        return self.sizer

    def refresh(self):
        address, start, end = self.config
        value = reg.GetBit(address=address, bit=start)
        self.SetCheck(value=value, wx_checkbox=self.check_reset)

    def update(self, event):
        address, start, end = self.config
        reg.SetBit(address=address, bit=start, is_true=self.check_reset.GetValue())
        self.refresh()


if __name__ == '__main__':
    app = wx.App()
    frame = ProtocolStackDialog()
    frame.Show()
    app.MainLoop()
