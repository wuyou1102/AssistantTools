# encoding: utf-8
from lib.UserInterface.Dialog import DialogBase
import wx
from lib.Config import Instrument
from lib.ProtocolStack import Configuration
import logging
from ObjectBase import ObjectBase
from lib import Utility

logger = logging.getLogger(__name__)
reg = Instrument.get_register()
RF_configs = [Configuration.freq_point_config, Configuration.PA_config, Configuration.RF_channel_config,
              Configuration.baseband_power_config]


def set_radio_box(value, bit, radio_box):
    b = '{0:08b}'.format(ord(value))[::-1]
    radio_box.SetSelection(int(b[bit]))


class RadioFrequencyDialog(DialogBase.DialogWindow):
    def __init__(self, name=u"射频设置", size=(790, 692)):
        DialogBase.DialogWindow.__init__(self, name=name, size=size)
        self.panel = Panel(self)
        self.panel.Refresh()

    # def Show(self, show=1):
    #     self.panel.Refresh()
    #     super(DialogBase.DialogWindow, self).Show(show=show)


class Panel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                          style=wx.TAB_TRAVERSAL)
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        ButtonSizer = self.__init_button_sizer()
        FreqPointSizer = self.__init_freq_point_sizer()
        PA_Sizer = self.__init_PA_sizer()
        RF_ChannelSizer = self.__init_RF_channel_sizer()

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
        if not reg.IsConnect():
            Utility.AlertError(u"无法获取寄存器，请检查：\n\t1.是否连接寄存器并给寄存器上电。\n\t2.是否打开了其他占用寄存器的应用。\n\t3.驱动是否安装正确。")
            return False
        for config in RF_configs:
            for item in config:
                self.__getattribute__(item['name']).refresh()

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

    def __init_freq_point_sizer(self):
        FreqPointSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.HORIZONTAL)
        TitleSizer = wx.BoxSizer(wx.VERTICAL)
        title_freq_setting = wx.StaticText(self, wx.ID_ANY, u"频点设置", wx.DefaultPosition, wx.DefaultSize, 0)
        font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, underline=True)
        title_freq_setting.SetFont(font)
        title_tx = wx.StaticText(self, wx.ID_ANY, u"发送：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        title_rx = wx.StaticText(self, wx.ID_ANY, u"接收：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        TitleSizer.Add(title_freq_setting, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        TitleSizer.Add(title_tx, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        TitleSizer.Add(title_rx, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        FreqPointSizer.Add(TitleSizer, 0, wx.ALL, 0)
        for item in Configuration.freq_point_config:
            self.__setattr__(item['name'], FreqPointSetting(self, item))
            sizer = self.__getattribute__(item['name']).get_sizer()
            FreqPointSizer.Add(sizer, 0, wx.ALL, 0)
        return FreqPointSizer

    def __init_RF_channel_sizer(self):
        RF_ChannelSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.HORIZONTAL)
        TitleSizer = wx.BoxSizer(wx.VERTICAL)
        title_freq_setting = wx.StaticText(self, wx.ID_ANY, u"PA:2G/5G", wx.DefaultPosition, wx.DefaultSize, 0)
        font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, underline=True)
        title_freq_setting.SetFont(font)
        title_tx = wx.StaticText(self, wx.ID_ANY, u"发送：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        title_rx = wx.StaticText(self, wx.ID_ANY, u"接收：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        TitleSizer.Add(title_freq_setting, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        TitleSizer.Add(title_tx, 0, wx.ALIGN_CENTER | wx.TOP, 25)
        TitleSizer.Add(title_rx, 0, wx.ALIGN_CENTER | wx.TOP, 30)
        RF_ChannelSizer.Add(TitleSizer, 0, wx.ALL, 0)
        for item in Configuration.RF_channel_config:
            self.__setattr__(item['name'], RFChannelSetting(self, item))
            sizer = self.__getattribute__(item['name']).get_sizer()
            RF_ChannelSizer.Add(sizer, 0, wx.ALL, 0)
        return RF_ChannelSizer

    def __init_PA_sizer(self):
        Sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.HORIZONTAL)
        TitleSizer = wx.BoxSizer(wx.VERTICAL)
        title_freq_setting = wx.StaticText(self, wx.ID_ANY, u"通道设置", wx.DefaultPosition, wx.DefaultSize, 0)
        font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, underline=True)
        title_freq_setting.SetFont(font)
        title_tx_2_0 = wx.StaticText(self, wx.ID_ANY, u"2G通道0：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        title_tx_2_1 = wx.StaticText(self, wx.ID_ANY, u"2G通道1：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        title_tx_5_0 = wx.StaticText(self, wx.ID_ANY, u"5G通道0：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        title_tx_5_1 = wx.StaticText(self, wx.ID_ANY, u"5G通道1：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER)
        TitleSizer.Add(title_freq_setting, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        TitleSizer.Add(title_tx_2_0, 0, wx.ALIGN_CENTER | wx.TOP, 25)
        TitleSizer.Add(title_tx_2_1, 0, wx.ALIGN_CENTER | wx.TOP, 30)
        TitleSizer.Add(title_tx_5_0, 0, wx.ALIGN_CENTER | wx.TOP, 30)
        TitleSizer.Add(title_tx_5_1, 0, wx.ALIGN_CENTER | wx.TOP, 30)
        Sizer.Add(TitleSizer, 0, wx.ALL, 0)
        for item in Configuration.PA_config:
            self.__setattr__(item['name'], PA_Setting(self, item))
            sizer = self.__getattribute__(item['name']).get_sizer()
            Sizer.Add(sizer, 0, wx.ALL, 0)
        return Sizer

    def __init_baseband_power_sizer(self):
        BasebandSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.VERTICAL)
        TitleSizer = wx.BoxSizer(wx.HORIZONTAL)
        title_freq_setting = wx.StaticText(self, wx.ID_ANY, u"基带功率偏移", wx.DefaultPosition, wx.DefaultSize, 0)
        font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, underline=True)
        title_freq_setting.SetFont(font)
        TitleSizer.Add(title_freq_setting, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        BasebandSizer.Add(TitleSizer, 0, wx.ALL, 0)
        for item in Configuration.baseband_power_config:
            self.__setattr__(item['name'], BandbasePowerSetting(self, item))
            sizer = self.__getattribute__(item['name']).get_sizer()
            line = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
            BasebandSizer.Add(sizer, 0, wx.EXPAND | wx.TOP, 10)
            BasebandSizer.Add(line, 0, wx.EXPAND | wx.RIGHT | wx.LEFT, 5)
        return BasebandSizer


class BandbasePowerSetting(ObjectBase):
    def __init__(self, panel, item):
        ObjectBase.__init__(self, item=item)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.item = item
        logger.debug("BandbasePowerSetting:Init")
        logger.debug(item)
        self.address = item['address']
        title_name = wx.StaticText(panel, wx.ID_ANY, item['title'], wx.DefaultPosition, (120, -1), 0)
        title_name.Wrap(-1)
        self.slider = wx.Slider(panel, wx.ID_ANY, 0, 1, 63, wx.DefaultPosition, wx.DefaultSize,
                                wx.SL_HORIZONTAL | wx.SL_SELRANGE | wx.SL_TICKS)
        self.slider.Bind(wx.EVT_SCROLL_CHANGED, self.on_scroll_changed)
        self.slider.Bind(wx.EVT_SLIDER, self.on_scroll)
        self.static_text = wx.StaticText(panel, wx.ID_ANY, u"", wx.DefaultPosition, (50, -1), 0)
        self.sizer.Add(title_name, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)
        self.sizer.Add(self.slider, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)
        self.sizer.Add(self.static_text, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)

    def get_sizer(self):
        return self.sizer

    def refresh(self):
        value = reg.GetByte(self.address)
        b = '{0:08b}'.format(ord(value))
        b = int(b[2:], 2)
        self.slider.SetValue(b)
        self.static_text.SetLabel(str(-15.5 + 0.25 * (b - 1)))

    def on_scroll_changed(self, event):
        x = self.slider.GetValue()
        self.static_text.SetLabel(str(-15.5 + 0.25 * (x - 1)))
        byte = reg.GetByte(address=self.address)
        b = '{0:08b}'.format(ord(byte))[0:2]
        x = '{0:06b}'.format(x)
        value = int(b + x, 2)
        reg.SetByte(address=self.address, byte=value)

    def on_scroll(self, event):
        x = self.slider.GetValue()
        self.static_text.SetLabel(str(-15.5 + 0.25 * (x - 1)))


class FreqPointSetting(ObjectBase):
    def __init__(self, panel, item):
        ObjectBase.__init__(self, item=item)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.item = item
        logger.debug("FreqPointSetting:Init")
        logger.debug(item)
        width = 95
        self.multi_2_4 = 30
        self.multi_5_8 = 60
        self.freq_pow = 16777216.0
        self.title = wx.StaticText(panel, wx.ID_ANY, item['title'], wx.DefaultPosition, wx.DefaultSize, 0)
        self.tx_tc = wx.TextCtrl(panel, wx.ID_ANY, '', wx.DefaultPosition, (width, -1),
                                 wx.TE_CENTER | wx.TE_PROCESS_ENTER)
        self.tx_tc.Bind(wx.EVT_TEXT_ENTER, self.update_tx)

        self.rx_tc = wx.TextCtrl(panel, wx.ID_ANY, '', wx.DefaultPosition, (width, -1),
                                 wx.TE_CENTER | wx.TE_PROCESS_ENTER)
        self.rx_tc.Bind(wx.EVT_TEXT_ENTER, self.update_rx)

        self.tx_address = item['tx']
        self.rx_address = item['rx']
        self.sizer.Add(self.title, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.sizer.Add(self.tx_tc, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        self.sizer.Add(self.rx_tc, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        if not item['tx']:
            self.tx_tc.Disable()
        if not item['rx']:
            self.rx_tc.Disable()

    def refresh(self):
        self.__refresh(self.rx_address, self.rx_tc)
        self.__refresh(self.tx_address, self.tx_tc)

    def __refresh(self, address, text_ctrl):
        if not address:
            return
        value = reg.Get(address=address, reverse=-1)
        d3d1 = value[0:6]
        d0 = value[6:]
        rf_multi = self.multi_2_4 if d0 in ['50', '51', '52'] else self.multi_5_8
        d1d3 = Utility.swap_to_d1d3(d3d1)
        d1d3 = int(d1d3, 16)
        d0 = int(d0, 16)
        f = round((d1d3 / self.freq_pow + d0) * rf_multi, 2)
        text_ctrl.SetValue(str(f))

    def update_rx(self, event):
        value = self.GetInput(text_ctrl=self.rx_tc, address=self.rx_address)
        if value is None:
            pass
        else:
            self.__update(address=self.rx_address, value=value)
            self.title.SetFocus()
            self.__refresh(self.rx_address, self.rx_tc)

    def update_tx(self, event):
        value = self.GetInput(text_ctrl=self.tx_tc, address=self.tx_address)
        if value is None:
            pass
        else:
            self.__update(address=self.tx_address, value=value)
            self.title.SetFocus()
            self.__refresh(self.tx_address, self.tx_tc)

    def __update(self, address, value):
        rf_multi = self.multi_2_4 if 2250 <= value <= 2500 else self.multi_5_8
        d1d3 = value / rf_multi
        d1d3 = int((d1d3 - int(d1d3)) * self.freq_pow)
        d1d3 = hex(d1d3)[2:]
        d3d1 = Utility.swap_to_d1d3(d1d3).zfill(6)
        d0 = hex(int(value / rf_multi))[2:]
        reg.Set(address=address, data=d3d1 + d0)

    def get_sizer(self):
        return self.sizer

    def GetInput(self, text_ctrl, address):
        try:
            value = float(text_ctrl.GetValue())
        except ValueError:
            self.__refresh(address, text_ctrl)
            Utility.AlertError(u"输入不合法，非数字。")
            return None
        if 2250 <= value <= 2500 or 5000 <= value <= 6000:
            return value
        else:
            self.__refresh(address, text_ctrl)
            Utility.AlertError(u"输入不合法：数值不在范围内。")
            return None


class PA_Setting(ObjectBase):
    def __init__(self, panel, item):
        ObjectBase.__init__(self, item=item)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.item = item
        logger.debug("PA_Setting:Init")
        logger.debug(item)
        width = 95
        self.a20 = self.item['a20']
        self.a21 = self.item['a21']
        self.a50 = self.item['a50']
        self.a51 = self.item['a51']

        title = wx.StaticText(panel, wx.ID_ANY, item['title'], wx.DefaultPosition, wx.DefaultSize, 0)
        self.a20_rb = wx.RadioBox(panel, -1, '', pos=wx.DefaultPosition, size=(width, -1), choices=[u'关', u'开'],
                                  majorDimension=1, style=wx.RA_SPECIFY_ROWS, name='a20')
        self.a21_rb = wx.RadioBox(panel, -1, '', pos=wx.DefaultPosition, size=(width, -1), choices=[u'关', u'开'],
                                  majorDimension=1, style=wx.RA_SPECIFY_ROWS, name='a21')
        self.a50_rb = wx.RadioBox(panel, -1, '', pos=wx.DefaultPosition, size=(width, -1), choices=[u'关', u'开'],
                                  majorDimension=1, style=wx.RA_SPECIFY_ROWS, name='a50')
        self.a51_rb = wx.RadioBox(panel, -1, '', pos=wx.DefaultPosition, size=(width, -1), choices=[u'关', u'开'],
                                  majorDimension=1, style=wx.RA_SPECIFY_ROWS, name='a51')

        self.a20_rb.Bind(wx.EVT_RADIOBOX, self.update)
        self.a21_rb.Bind(wx.EVT_RADIOBOX, self.update)
        self.a50_rb.Bind(wx.EVT_RADIOBOX, self.update)
        self.a51_rb.Bind(wx.EVT_RADIOBOX, self.update)
        self.sizer.Add(title, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.sizer.Add(self.a20_rb, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 2)
        self.sizer.Add(self.a21_rb, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 2)
        self.sizer.Add(self.a50_rb, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 2)
        self.sizer.Add(self.a51_rb, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 2)
        self.disable_useless()

    def get_sizer(self):
        return self.sizer

    def disable_useless(self):
        if self.a20:
            self.lst.append((self.a20, self.a20_rb))
        else:
            self.a20_rb.Disable()
        if self.a21:
            self.lst.append((self.a21, self.a21_rb))
        else:
            self.a21_rb.Disable()
        if self.a50:
            self.lst.append((self.a50, self.a50_rb))
        else:
            self.a50_rb.Disable()
        if self.a51:
            self.lst.append((self.a51, self.a51_rb))
        else:
            self.a51_rb.Disable()

    def refresh(self):
        self.last_address = None
        self.last_value = None
        for address, radio_box in self.lst:
            self.__refresh(address, radio_box)

    def __refresh(self, address, radio_box):
        address, bit = address
        if self.last_address == address:
            set_radio_box(self.last_value, bit, radio_box)
        else:
            self.last_address = address
            self.last_value = reg.GetByte(address=address)
            set_radio_box(self.last_value, bit, radio_box)

    def update(self, event):
        obj = event.GetEventObject()
        address, bit = self.__getattribute__(obj.GetName())
        is_true = True if obj.GetSelection() == 1 else False
        reg.SetBit(address=address, bit=bit, is_true=is_true)


class RFChannelSetting(ObjectBase):
    def __init__(self, panel, item):
        ObjectBase.__init__(self, item=item)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.item = item
        logger.debug("RFChannelSetting:Init")
        logger.debug(item)
        width = 95
        title = wx.StaticText(panel, wx.ID_ANY, item['title'], wx.DefaultPosition, wx.DefaultSize, 0)
        self.tx_rb = wx.RadioBox(panel, -1, '', pos=wx.DefaultPosition, size=(width, -1), choices=['2G', '5G'],
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS, name='tx')
        self.rx_rb = wx.RadioBox(panel, -1, '', pos=wx.DefaultPosition, size=(width, -1), choices=['2G', '5G'],
                                 majorDimension=1, style=wx.RA_SPECIFY_ROWS, name='rx')
        self.tx_rb.Bind(wx.EVT_RADIOBOX, self.update)
        self.rx_rb.Bind(wx.EVT_RADIOBOX, self.update)
        self.sizer.Add(title, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.sizer.Add(self.tx_rb, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 2)
        self.sizer.Add(self.rx_rb, 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 2)
        self.tx = item['tx']
        self.rx = item['rx']
        self.disable_useless()

    def get_sizer(self):
        return self.sizer

    def disable_useless(self):
        if self.tx:
            self.lst.append((self.tx, self.tx_rb))
        else:
            self.tx_rb.Disable()
        if self.rx:
            self.lst.append((self.rx, self.rx_rb))
        else:
            self.rx_rb.Disable()

    def refresh(self):
        self.last_address = None
        self.last_value = None
        for address, radio_box in self.lst:
            self.__refresh(address, radio_box)

    def __refresh(self, address, radio_box):
        address, bit = address
        if self.last_address == address:
            set_radio_box(self.last_value, bit, radio_box)
        else:
            self.last_address = address
            self.last_value = reg.GetByte(address=address)
            set_radio_box(self.last_value, bit, radio_box)

    def update(self, event):
        obj = event.GetEventObject()
        address, bit = self.__getattribute__(obj.GetName())
        is_true = True if obj.GetSelection() == 1 else False
        reg.SetBit(address=address, bit=bit, is_true=is_true)


if __name__ == '__main__':
    app = wx.App()
    frame = RadioFrequencyDialog()
    frame.Show()
    app.MainLoop()
