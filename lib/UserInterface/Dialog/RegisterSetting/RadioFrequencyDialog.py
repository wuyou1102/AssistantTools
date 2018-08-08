# encoding: utf-8
from lib.UserInterface.Dialog import DialogBase
import wx
from lib.Config import Instrument
import Configuration

reg = Instrument.get_register()


class RadioFrequencyDialog(DialogBase.DialogBase):
    def __init__(self, name=u"射频设置", size=(790, 692)):
        DialogBase.DialogBase.__init__(self, name=name, size=size)
        self.panel = Panel(self)

    def Show(self, show=1):
        self.panel.Refresh()
        super(DialogBase.DialogBase, self).Show(show=show)


class Panel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                          style=wx.TAB_TRAVERSAL)
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        ButtonSizer = self.__init_button_sizer()
        FreqPointSizer = self.__init_freq_point_sizer()
        RF_ChannelSizer = self.__init_RF_channel_sizer()
        PA_Sizer = self.__init_PA_sizer()
        Baseband_Sizer = self.__init_baseband_power_sizer()
        TopSizer = wx.BoxSizer(wx.HORIZONTAL)
        TopLeftSizer = wx.BoxSizer(wx.VERTICAL)
        TopLeftSizer.Add(FreqPointSizer, 0, wx.EXPAND, 0)
        TopLeftSizer.Add(PA_Sizer, 0, wx.EXPAND, 0)
        TopSizer.Add(TopLeftSizer, 0, wx.ALL, 0)
        TopSizer.Add(ButtonSizer, 1, wx.EXPAND | wx.LEFT, 5)

        MainSizer.Add(TopSizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        MainSizer.Add(RF_ChannelSizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        MainSizer.Add(Baseband_Sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

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

    def __init_freq_point_sizer(self):
        def init_item(name, tx, rx):
            ItemSizer = wx.BoxSizer(wx.VERTICAL)
            title_name = wx.StaticText(self, wx.ID_ANY, name, wx.DefaultPosition, wx.DefaultSize, 0)
            self.__setattr__("freq_point_setting_%s_tx" % name,
                             FreqPointTextCtrl(self, wx.ID_ANY, str(tx), wx.DefaultPosition, wx.TE_CENTER,
                                               address=tx))
            self.__setattr__("freq_point_setting_%s_rx" % name,
                             FreqPointTextCtrl(self, wx.ID_ANY, str(rx), wx.DefaultPosition, wx.TE_CENTER,
                                               address=rx))

            ItemSizer.Add(title_name, 0, wx.ALIGN_CENTER | wx.ALL, 5)
            ItemSizer.Add(self.__getattribute__("freq_point_setting_%s_tx" % name), 0, wx.ALIGN_CENTER | wx.ALL, 2)
            ItemSizer.Add(self.__getattribute__("freq_point_setting_%s_rx" % name), 0, wx.ALIGN_CENTER | wx.ALL, 2)
            return ItemSizer

        FreqPointSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.HORIZONTAL)
        TitleSizer = wx.BoxSizer(wx.VERTICAL)
        title_freq_setting = wx.StaticText(self, wx.ID_ANY, u"频点设置", wx.DefaultPosition, wx.DefaultSize, 0)
        font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, underline=True)
        title_freq_setting.SetFont(font)
        title_tx = wx.StaticText(self, wx.ID_ANY, u"发送：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        title_rx = wx.StaticText(self, wx.ID_ANY, u"接收：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        TitleSizer.Add(title_freq_setting, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        TitleSizer.Add(title_tx, 0, wx.ALIGN_CENTER | wx.TOP, 12)
        TitleSizer.Add(title_rx, 0, wx.ALIGN_CENTER | wx.TOP, 15)
        FreqPointSizer.Add(TitleSizer, 0, wx.ALL, 0)
        for item in Configuration.freq_point_config:
            item_sizer = init_item(*item)
            FreqPointSizer.Add(item_sizer, 0, wx.ALL, 0)
        return FreqPointSizer

    def __init_RF_channel_sizer(self):
        def init_item(name, tx, rx):
            ItemSizer = wx.BoxSizer(wx.VERTICAL)
            tx_address, tx_bit = tx
            rx_address, rx_bit = rx
            title_name = wx.StaticText(self, wx.ID_ANY, name, wx.DefaultPosition, wx.DefaultSize, 0)

            self.__setattr__("RF_channel_%s_tx" % name,
                             RF_PA_RadioBox(self, -1, '', pos=wx.DefaultPosition, choices=['2G', '5G'],
                                            majorDimension=1, style=wx.RA_SPECIFY_ROWS, address=tx_address,
                                            bit=tx_bit))
            self.__setattr__("RF_channel_%s_rx" % name,
                             RF_PA_RadioBox(self, -1, '', pos=wx.DefaultPosition, choices=['2G', '5G'],
                                            majorDimension=1, style=wx.RA_SPECIFY_ROWS, address=rx_address,
                                            bit=rx_bit))
            ItemSizer.Add(title_name, 0, wx.ALIGN_CENTER | wx.ALL, 5)
            ItemSizer.Add(self.__getattribute__("RF_channel_%s_tx" % name), 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 2)
            ItemSizer.Add(self.__getattribute__("RF_channel_%s_rx" % name), 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 2)
            return ItemSizer

        RF_ChannelSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.HORIZONTAL)
        TitleSizer = wx.BoxSizer(wx.VERTICAL)
        title_freq_setting = wx.StaticText(self, wx.ID_ANY, u"射频通道", wx.DefaultPosition, wx.DefaultSize, 0)
        font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, underline=True)
        title_freq_setting.SetFont(font)
        title_tx = wx.StaticText(self, wx.ID_ANY, u"发送：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        title_rx = wx.StaticText(self, wx.ID_ANY, u"接收：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        TitleSizer.Add(title_freq_setting, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        TitleSizer.Add(title_tx, 0, wx.ALIGN_CENTER | wx.TOP, 25)
        TitleSizer.Add(title_rx, 0, wx.ALIGN_CENTER | wx.TOP, 30)
        RF_ChannelSizer.Add(TitleSizer, 0, wx.ALL, 0)

        for item in Configuration.RF_channel_config:
            item_sizer = init_item(*item)
            RF_ChannelSizer.Add(item_sizer, 0, wx.ALL, 0)
        return RF_ChannelSizer

    def __init_PA_sizer(self):
        def init_item(name, t2_0, t2_1, t5_0, t5_1):
            ItemSizer = wx.BoxSizer(wx.VERTICAL)
            t2_0_address, t2_0_bit = t2_0
            t2_1_address, t2_1_bit = t2_1
            t5_0_address, t5_0_bit = t5_0
            t5_1_address, t5_1_bit = t5_1
            title_name = wx.StaticText(self, wx.ID_ANY, name, wx.DefaultPosition, wx.DefaultSize, 0)

            self.__setattr__("PA_2_0_%s" % name,
                             RF_PA_RadioBox(self, -1, '', pos=wx.DefaultPosition, choices=['关', '开'],
                                            majorDimension=1, style=wx.RA_SPECIFY_ROWS, address=t2_0_address,
                                            bit=t2_0_bit))
            self.__setattr__("PA_2_1_%s" % name,
                             RF_PA_RadioBox(self, -1, '', pos=wx.DefaultPosition, choices=['关', '开'],
                                            majorDimension=1, style=wx.RA_SPECIFY_ROWS, address=t2_1_address,
                                            bit=t2_1_bit))
            self.__setattr__("PA_5_0_%s" % name,
                             RF_PA_RadioBox(self, -1, '', pos=wx.DefaultPosition, choices=['关', '开'],
                                            majorDimension=1, style=wx.RA_SPECIFY_ROWS, address=t5_0_address,
                                            bit=t5_0_bit))
            self.__setattr__("PA_5_1_%s" % name,
                             RF_PA_RadioBox(self, -1, '', pos=wx.DefaultPosition, choices=['关', '开'],
                                            majorDimension=1, style=wx.RA_SPECIFY_ROWS, address=t5_1_address,
                                            bit=t5_1_bit))

            ItemSizer.Add(title_name, 0, wx.ALIGN_CENTER | wx.ALL, 5)
            ItemSizer.Add(self.__getattribute__("PA_2_0_%s" % name), 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 2)
            ItemSizer.Add(self.__getattribute__("PA_2_1_%s" % name), 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 2)
            ItemSizer.Add(self.__getattribute__("PA_5_0_%s" % name), 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 2)
            ItemSizer.Add(self.__getattribute__("PA_5_1_%s" % name), 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 2)
            return ItemSizer

        RF_ChannelSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.HORIZONTAL)
        TitleSizer = wx.BoxSizer(wx.VERTICAL)
        title_freq_setting = wx.StaticText(self, wx.ID_ANY, u" PA设置 ", wx.DefaultPosition, wx.DefaultSize, 0)
        font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, underline=True)
        title_freq_setting.SetFont(font)
        title_tx_2_0 = wx.StaticText(self, wx.ID_ANY, u"2G天线0：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        title_tx_2_1 = wx.StaticText(self, wx.ID_ANY, u"2G天线1：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        title_tx_5_0 = wx.StaticText(self, wx.ID_ANY, u"5G天线0：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        title_tx_5_1 = wx.StaticText(self, wx.ID_ANY, u"5G天线1：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        TitleSizer.Add(title_freq_setting, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        TitleSizer.Add(title_tx_2_0, 0, wx.ALIGN_CENTER | wx.TOP, 25)
        TitleSizer.Add(title_tx_2_1, 0, wx.ALIGN_CENTER | wx.TOP, 30)
        TitleSizer.Add(title_tx_5_0, 0, wx.ALIGN_CENTER | wx.TOP, 30)
        TitleSizer.Add(title_tx_5_1, 0, wx.ALIGN_CENTER | wx.TOP, 30)
        RF_ChannelSizer.Add(TitleSizer, 0, wx.ALL, 0)
        for item in Configuration.PA_config:
            item_sizer = init_item(*item)
            RF_ChannelSizer.Add(item_sizer, 0, wx.ALL, 0)
        return RF_ChannelSizer

    def __init_baseband_power_sizer(self):
        def init_item(name, address, title):
            self.__setattr__(name, BandbasePowerSlider(self, title, address))

            return self.__getattribute__(name).get_sizer()

        BasebandSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.VERTICAL)
        TitleSizer = wx.BoxSizer(wx.HORIZONTAL)
        title_freq_setting = wx.StaticText(self, wx.ID_ANY, u"基带功率偏移", wx.DefaultPosition, wx.DefaultSize, 0)
        font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, underline=True)
        title_freq_setting.SetFont(font)
        TitleSizer.Add(title_freq_setting, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        BasebandSizer.Add(TitleSizer, 0, wx.ALL, 0)

        for item in Configuration.baseband_power_config:
            item_sizer = init_item(*item)
            line = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
            BasebandSizer.Add(item_sizer, 0, wx.EXPAND | wx.TOP, 10)
            BasebandSizer.Add(line, 0, wx.EXPAND | wx.RIGHT | wx.LEFT, 5)
        return BasebandSizer


class FreqPointTextCtrl(wx.TextCtrl):
    def __init__(self, parent=None, id=None, value=None, pos=None, style=0, address='', s_bit='',
                 e_bit=''):
        wx.TextCtrl.__init__(self, parent, id, value, pos, (95, -1), style)
        self.address = address
        self.s_bit = s_bit
        self.e_bit = e_bit
        self.UpdateValue()
        if not self.address:
            self.Disable()

    def UpdateValue(self):
        if self.address:
            self.SetValue("asdddsad")

    def read_reg(self):
        pass

    def write_reg(self):
        pass


class RF_PA_RadioBox(wx.RadioBox):
    def __init__(self, parent=None, id=None, label=None, pos=None, choices=[], majorDimension=0, style=None,
                 address="", bit=""):
        wx.RadioBox.__init__(self, parent, id, label, pos, (95, -1), choices, majorDimension, style)
        self.index = address % 4 if address else 0
        self.address = address if address else 0
        if not self.address:
            self.Disable()
        self.bit = bit
        self.UpdateSelection()

    def UpdateSelection(self):
        if self.address:
            self.SetSelection(self.read_reg())

    def read_reg(self):
        bytes = reg.GetByte(address=self.address)
        b = bin(ord(bytes[self.index]))[2:]
        b = "0" * (8 - len(b)) + b
        return 1 if b[7 - self.bit] == '1' else 0

    def write_reg(self):
        pass


class BandbasePowerSlider(object):
    def __init__(self, panel, title, address):
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        title_name = wx.StaticText(panel, wx.ID_ANY, title, wx.DefaultPosition, (120, -1), 0)
        title_name.Wrap(-1)
        self.slider = wx.Slider(panel, wx.ID_ANY, 0, 1, 63, wx.DefaultPosition, wx.DefaultSize,
                                wx.SL_HORIZONTAL | wx.SL_SELRANGE | wx.SL_TICKS)
        self.slider.Bind(wx.EVT_SCROLL_CHANGED, self.on_scroll_changed)
        self.slider.Bind(wx.EVT_SLIDER, self.on_scroll)
        self.static_text = wx.StaticText(panel, wx.ID_ANY, u"", wx.DefaultPosition, (50, -1), 0)
        self.sizer.Add(title_name, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)
        self.sizer.Add(self.slider, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)
        self.sizer.Add(self.static_text, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)
        self.UpdateValue()

    def get_sizer(self):
        return self.sizer

    def UpdateValue(self):
        import random
        x = random.randint(0, 63)
        self.slider.SetValue(x)
        self.static_text.SetLabel(str(-15.5 + 0.25 * x))

    def on_scroll_changed(self, event):
        pass
        # x = self.slider.GetValue()
        # self.static_text.SetLabel(str(-15.5 + 0.25 * x))

    def on_scroll(self, event):
        x = self.slider.GetValue()
        self.static_text.SetLabel(str(-15.5 + 0.25 * (x - 1)))
