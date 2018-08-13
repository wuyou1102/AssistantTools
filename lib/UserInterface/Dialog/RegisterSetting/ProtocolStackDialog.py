# encoding: utf-8
from lib.UserInterface.Dialog import DialogBase
import wx
from lib.Config import Instrument
import Configuration

reg = Instrument.get_register()


class ProtocolStackDialog(DialogBase.DialogBase):
    def __init__(self, name=u"协议栈设置", size=(790, 560)):
        DialogBase.DialogBase.__init__(self, name=name, size=size)
        self.panel = Panel(self)

    def Show(self, show=1):
        self.panel.Refresh()
        super(DialogBase.DialogBase, self).Show(show=show)


class Panel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                          style=wx.TAB_TRAVERSAL)
        self.font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, underline=True)
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        FirstRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        ThirdRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        InterleaverSizer = self.__init_interleaver_sizer()
        MCS_Sizer = self.__init_MCS_sizer()
        BandwidthSizer = self.__init_bandwidth_sizer()
        SlotMIMO_Sizer = self.__init_slot_mimo_sizer()
        LockSizer = self.__init_lock_sizer()
        ClearSizer = self.__init_clear_sizer()
        ButtonSizer = self.__init_button_sizer()
        ResetSizer = self.__init_reset_sizer()
        LeftTopSizer = wx.BoxSizer(wx.VERTICAL)
        LockAndClearSizer = wx.BoxSizer(wx.HORIZONTAL)
        LockAndClearSizer.Add(ClearSizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        LockAndClearSizer.Add(LockSizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        FirstRowSizer.Add(InterleaverSizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        FirstRowSizer.Add(BandwidthSizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        ThirdRowSizer.Add(ResetSizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        ThirdRowSizer.Add(MCS_Sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        LeftTopSizer.Add(FirstRowSizer, 0, wx.EXPAND | wx.ALL, 0)
        LeftTopSizer.Add(LockAndClearSizer, 0, wx.EXPAND | wx.ALL, 0)
        TopSizer = wx.BoxSizer(wx.HORIZONTAL)
        TopSizer.Add(LeftTopSizer, 0, wx.EXPAND | wx.ALL, 0)
        TopSizer.Add(ButtonSizer, 1, wx.EXPAND | wx.ALL, 0)

        MainSizer.Add(TopSizer, 0, wx.EXPAND | wx.ALL, 0)
        MainSizer.Add(ThirdRowSizer, 0, wx.EXPAND | wx.ALL, 0)
        MainSizer.Add(SlotMIMO_Sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        self.SetSizer(MainSizer)
        self.Layout()

    def Refresh(self):
        pass

    def on_TODO(self, event):
        pass

    def on_refresh(self, event):
        pass

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
        title_interleaver_setting = wx.StaticText(self, wx.ID_ANY, u"交织设置", wx.DefaultPosition, wx.DefaultSize, 0)
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
        title_interleaver_setting = wx.StaticText(self, wx.ID_ANY, u"MCS", wx.DefaultPosition, wx.DefaultSize, 0)
        title_interleaver_setting.SetFont(self.font)
        title_modulation = wx.StaticText(self, wx.ID_ANY, u"调制：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        title_coding = wx.StaticText(self, wx.ID_ANY, u"编码：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        title_repeat = wx.StaticText(self, wx.ID_ANY, u"重复：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        TitleSizer.Add(title_interleaver_setting, 0, wx.ALIGN_CENTER | wx.TOP, 10)
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
        title_name = wx.StaticText(self, wx.ID_ANY, u"带宽设置", wx.DefaultPosition, wx.DefaultSize, 0)
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
        self.__setattr__(Configuration.user_bandwidth_config['name'],
                         UserBandwidthSetting(self, Configuration.user_bandwidth_config))
        user_sizer = self.__getattribute__(Configuration.user_bandwidth_config['name']).get_sizer()
        Sizer.Add(br_cs_sizer, 0, wx.ALL, 0)
        Sizer.Add(user_sizer, 0, wx.ALL, 0)
        return Sizer

    def __init_slot_mimo_sizer(self):
        Sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.VERTICAL)
        TitleSizer = wx.BoxSizer(wx.VERTICAL)
        title_name = wx.StaticText(self, wx.ID_ANY, u"MIMO模式", wx.DefaultPosition, wx.DefaultSize, 0)

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
        title_name = wx.StaticText(self, wx.ID_ANY, u"LOCK", wx.DefaultPosition, wx.DefaultSize, 0)

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
            Sizer.Add(reset_sizer, 0, wx.LEFT | wx.TOP, 7)
        return Sizer


class UserInterleave(object):
    def __init__(self, panel, item):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.item = item
        title_name = wx.StaticText(panel, wx.ID_ANY, item["title"], wx.DefaultPosition, wx.DefaultSize, 0)
        t = ['12', '24', '48', '96']
        m = ['12', '24', '48']
        width = 60
        self.total_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), t, 0)
        self.mode_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), m, 0)
        self.text_ctrl = wx.TextCtrl(panel, wx.ID_ANY, "1152", wx.DefaultPosition, (width, -1),
                                     wx.TE_LEFT | wx.TE_READONLY)

        self.sizer.Add(title_name, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        self.sizer.Add(self.total_choice, 0, wx.ALL, 5)
        self.sizer.Add(self.mode_choice, 0, wx.ALL, 5)
        self.sizer.Add(self.text_ctrl, 0, wx.ALL, 5)

    def get_sizer(self):
        return self.sizer


class BrInterleave(object):
    def __init__(self, panel, item):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.item = item
        title_name = wx.StaticText(panel, wx.ID_ANY, item["title"], wx.DefaultPosition, wx.DefaultSize, 0)
        t = ['6', '12', '24']
        m = []
        width = 60
        self.total_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), t, 0)
        self.mode_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), m, 0)
        self.text_ctrl = wx.TextCtrl(panel, wx.ID_ANY, "", wx.DefaultPosition, (width, -1),
                                     wx.TE_LEFT | wx.TE_READONLY)
        self.mode_choice.Disable()
        self.text_ctrl.Disable()
        self.sizer.Add(title_name, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        self.sizer.Add(self.total_choice, 0, wx.ALL, 5)
        self.sizer.Add(self.mode_choice, 0, wx.ALL, 5)
        self.sizer.Add(self.text_ctrl, 0, wx.ALL, 5)

    def get_sizer(self):
        return self.sizer


class ModulationCodingSchemeSetting(object):
    def __init__(self, panel, item):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.item = item
        name = item['name']

        modulations = ['BPSK', 'QPSK', '16QAM', '64QAM', '256QAM'] if name.startswith("user") else ['BPSK', 'QPSK']
        codings = ['1/2', '2/3A', '2/3B', '3/4A', '3/4B', '5/6'] if name.startswith("user") else ['1/2', '2/3']
        repeats = ['hello', 'world']

        width = 60
        title_name = wx.StaticText(panel, wx.ID_ANY, item["title"], wx.DefaultPosition, wx.DefaultSize, 0)
        self.modulation_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), modulations, 0)
        self.coding_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), codings, 0)
        self.repeat_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), repeats, 0)

        self.sizer.Add(title_name, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        self.sizer.Add(self.modulation_choice, 0, wx.ALL, 5)
        self.sizer.Add(self.coding_choice, 0, wx.ALL, 5)
        self.sizer.Add(self.repeat_choice, 0, wx.ALL, 5)

    def get_sizer(self):
        return self.sizer


class BR_CS_BandwidthSetting(object):
    def __init__(self, panel, item):
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        br_sizer = wx.BoxSizer(wx.VERTICAL)
        cs_sizer = wx.BoxSizer(wx.VERTICAL)
        self.item = item
        bandwitdth = ['2.5MHz', '5MHz', '10MHz', '20MHz', '40MHz']
        self.br = item['BR']
        self.cs = item['CS']
        width = 60
        br_title_name = wx.StaticText(panel, wx.ID_ANY, self.br["title"], wx.DefaultPosition, wx.DefaultSize, 0)
        cs_title_name = wx.StaticText(panel, wx.ID_ANY, self.cs["title"], wx.DefaultPosition, wx.DefaultSize, 0)
        self.br_recv_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), bandwitdth, 0)
        self.br_send_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), bandwitdth, 0)
        self.cs_recv_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), bandwitdth, 0)
        self.cs_send_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), bandwitdth, 0)
        br_sizer.Add(br_title_name, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        br_sizer.Add(self.br_send_choice, 0, wx.ALL, 5)
        br_sizer.Add(self.br_recv_choice, 0, wx.ALL, 5)
        cs_sizer.Add(cs_title_name, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        cs_sizer.Add(self.cs_send_choice, 0, wx.ALL, 5)
        cs_sizer.Add(self.cs_recv_choice, 0, wx.ALL, 5)

        self.sizer.Add(br_sizer, 0, wx.ALL, 0)
        self.sizer.Add(cs_sizer, 0, wx.ALL, 0)

    def get_sizer(self):
        return self.sizer


class UserBandwidthSetting(object):
    def __init__(self, panel, item):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.item = item
        bandwitdth = ['2.5MHz', '5MHz', '10MHz', '20MHz', '40MHz']
        width = 60
        title_name = wx.StaticText(panel, wx.ID_ANY, item["title"], wx.DefaultPosition, wx.DefaultSize, 0)
        self.recv_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), bandwitdth, 0)
        self.send_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), bandwitdth, 0)
        self.sizer.Add(title_name, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        self.sizer.Add(self.send_choice, 0, wx.ALL, 5)
        self.sizer.Add(self.recv_choice, 0, wx.ALL, 5)

    def get_sizer(self):
        return self.sizer


class AntennaModeSetting(object):
    def __init__(self, panel, item):
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.item = item
        send_ANT_choice = [u'1天线', u'2天线']
        recv_ANT_choice = [u'1天线', u'2天线', u'4天线']
        self.send = item['send']
        self.recv = item['recv']
        SL = wx.StaticLine(panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        width = 60
        send_title = wx.StaticText(panel, wx.ID_ANY, self.send["title"], wx.DefaultPosition, wx.DefaultSize, 0)
        recv_title = wx.StaticText(panel, wx.ID_ANY, self.recv["title"], wx.DefaultPosition, wx.DefaultSize, 0)
        self.recv_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), recv_ANT_choice, 0)
        self.send_choice = wx.Choice(panel, wx.ID_ANY, wx.DefaultPosition, (width, -1), send_ANT_choice, 0)
        self.sizer.Add(send_title, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.sizer.Add(self.send_choice, 0, wx.ALL, 5)
        self.sizer.Add(SL, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        self.sizer.Add(recv_title, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.sizer.Add(self.recv_choice, 0, wx.ALL, 5)

    def get_sizer(self):
        return self.sizer


class SlotMimoModeSetting(object):
    def __init__(self, panel, item):
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.item = item
        slot_choice = ['1t1r', '1t2r', '1t4r', '2t2r', '2t4r']
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


class LockSetting(object):
    def __init__(self, panel, item):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.item = item
        title = wx.StaticText(panel, wx.ID_ANY, self.item["title"], wx.DefaultPosition, wx.DefaultSize, 0)
        self.fch = item['fch']
        self.slot = item['slot']
        self.check_fch = wx.CheckBox(panel, wx.ID_ANY, self.fch[0], wx.DefaultPosition, wx.DefaultSize, 0)
        self.check_slot = wx.CheckBox(panel, wx.ID_ANY, self.slot[0], wx.DefaultPosition, wx.DefaultSize, 0)
        self.sizer.Add(title, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.sizer.Add(self.check_fch, 0, wx.ALL, 5)
        self.sizer.Add(self.check_slot, 0, wx.ALL, 5)

    def get_sizer(self):
        return self.sizer


class ClearSetting(object):
    def __init__(self, panel, item):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.item = item
        title = wx.StaticText(panel, wx.ID_ANY, self.item["title"], wx.DefaultPosition, wx.DefaultSize, 0)
        self.check_rx = wx.CheckBox(panel, wx.ID_ANY, 'RX', wx.DefaultPosition, wx.DefaultSize, 0)
        self.check_tx = wx.CheckBox(panel, wx.ID_ANY, 'TX', wx.DefaultPosition, wx.DefaultSize, 0)
        self.sizer.Add(title, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.sizer.Add(self.check_rx, 0, wx.ALL, 5)
        self.sizer.Add(self.check_tx, 0, wx.ALL, 5)

    def get_sizer(self):
        return self.sizer


class ResetSetting(object):
    def __init__(self, panel, item):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.item = item
        self.check_reset = wx.CheckBox(panel, wx.ID_ANY, self.item["title"], wx.DefaultPosition, wx.DefaultSize, 0)
        self.sizer.Add(self.check_reset, 0, wx.ALL, 5)

    def get_sizer(self):
        return self.sizer
