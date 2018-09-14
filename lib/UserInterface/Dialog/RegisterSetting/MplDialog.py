# -*- encoding:UTF-8 -*-
import wx
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
import numpy
from lib.UserInterface.Dialog import DialogBase
import logging
from matplotlib.ticker import MultipleLocator
from lib import Utility
import os

matplotlib.use('WXAgg')
logger = logging.getLogger(__name__)


class MplDialog(DialogBase.DialogWindow):
    def __init__(self, name=u"趋势图", rssi=None, snr=None, bler=None):
        DialogBase.DialogWindow.__init__(self, name=name, size=wx.DefaultSize)
        x0, y0, x1, y1 = wx.ClientDisplayRect()
        self.SetSize(wx.Size(x1, y1))
        self.SetPosition(wx.Point(x0, y0))
        self.__init_menu_bar()

        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        LeftSizer = wx.BoxSizer(wx.VERTICAL)
        CenterSizer = wx.BoxSizer(wx.VERTICAL)
        RightSizer = wx.BoxSizer(wx.VERTICAL)
        self.__init_rssi_mpl(rssi)
        self.__init_snr_mpl(snr)
        self.__init_bler_mpl(bler)
        LeftSizer.Add(self.user0, 1, wx.EXPAND | wx.ALL, 0)
        LeftSizer.Add(self.user2, 1, wx.EXPAND | wx.ALL, 0)
        CenterSizer.Add(self.user1, 1, wx.EXPAND | wx.ALL, 0)
        CenterSizer.Add(self.user3, 1, wx.EXPAND | wx.ALL, 0)
        RightSizer.Add(self.snr, 1, wx.EXPAND | wx.ALL, 0)
        RightSizer.Add(self.bler, 1, wx.EXPAND | wx.ALL, 0)
        self.mpl_list = [self.user0, self.user1, self.user2, self.user3, self.snr, self.bler]
        MainSizer.Add(LeftSizer, 1, wx.EXPAND | wx.ALL, 0)
        MainSizer.Add(CenterSizer, 1, wx.EXPAND | wx.ALL, 0)
        MainSizer.Add(RightSizer, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(MainSizer)
        self.Layout()
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        for mpl in self.mpl_list:
            mpl.close_timer()
        event.Skip()

    def __init_rssi_mpl(self, rssi_objects):
        for obj in rssi_objects:
            if 'user0' in obj.get_name():
                self.user0 = RSSIPanel(parent=self, obj=obj)
            elif 'user1' in obj.get_name():
                self.user1 = RSSIPanel(parent=self, obj=obj)
            elif 'user2' in obj.get_name():
                self.user2 = RSSIPanel(parent=self, obj=obj)
            elif 'user3' in obj.get_name():
                self.user3 = RSSIPanel(parent=self, obj=obj)
            else:
                raise NameError

    def __init_snr_mpl(self, snr_objects):
        self.snr = SNRPanel(self, snr_objects)

    def __init_bler_mpl(self, bler_objects):
        self.bler = BLERPanel(self, bler_objects)

    def Show(self, show=1):
        super(DialogBase.DialogWindow, self).Show(show=show)

    def Destroy(self):
        self.user0.close_timer()
        self.user1.close_timer()
        self.user2.close_timer()
        self.user3.close_timer()
        self.snr.close_timer()
        self.bler.close_timer()
        return super(DialogBase.DialogWindow, self).Destroy()

    def __init_menu_bar(self):
        menu_bar = wx.MenuBar()
        menu_rssi = wx.Menu()
        menu_bar.Append(menu_rssi, "&RSSI")
        self.SetMenuBar(menu_bar)


class BaseMplPanel(wx.Panel):
    def __init__(self, parent, line_num=4):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                          style=wx.TAB_TRAVERSAL)
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        MplSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.VERTICAL)
        self.line_num = line_num
        # 配置项『
        self.dpi = 100
        self.facecolor = '#FEF9E7'
        self.title = ''

        # 配置项』
        self.Figure = Figure((1.6, 0.9), self.dpi)
        self.Axes = self.Figure.add_axes([0.05, 0.05, 0.92, 0.88])
        self.FigureCanvas = FigureCanvasWxAgg(self, -1, self.Figure)
        SettingSizer = self.__init_setting_sizer()
        MplSizer.Add(self.FigureCanvas, 1, wx.EXPAND | wx.ALL, 0)
        MplSizer.Add(SettingSizer, 0, wx.EXPAND | wx.ALL, 0)
        MainSizer.Add(MplSizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
        self.SetSizer(MainSizer)
        self.Update()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.refresh, self.timer)
        self.timer.Start(1000)

    def __init_setting_sizer(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        y_set_sizer = wx.BoxSizer(wx.VERTICAL)

        max_sizer = wx.BoxSizer(wx.HORIZONTAL)
        min_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(self, wx.ID_ANY, u"设置", wx.DefaultPosition, (50, -1), 0)
        save_button = wx.Button(self, wx.ID_ANY, u"保存", wx.DefaultPosition, (50, -1), 0)
        ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        save_button.Bind(wx.EVT_BUTTON, self.on_save)
        title_max = wx.StaticText(self, wx.ID_ANY, u"Y坐标最大值：", wx.DefaultPosition, wx.DefaultSize, 0)
        title_min = wx.StaticText(self, wx.ID_ANY, u"Y坐标最小值：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.max_tc = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.min_tc = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        line_check_sizer = self.__init_line_check_sizer(self.line_num)
        max_sizer.Add(title_max, 0, wx.ALL, 0)
        max_sizer.Add(self.max_tc, 0, wx.ALL, 0)
        min_sizer.Add(title_min, 0, wx.ALL, 0)
        min_sizer.Add(self.min_tc, 0, wx.ALL, 0)
        y_set_sizer.Add(max_sizer, 0, wx.ALL, 0)
        y_set_sizer.Add(min_sizer, 0, wx.ALL, 0)
        sizer.Add(y_set_sizer, 0, wx.ALL, 0)
        sizer.Add(ok_button, 0, wx.EXPAND | wx.LEFT, 5)
        sizer.Add(line_check_sizer, 0, wx.EXPAND | wx.LEFT, 5)
        sizer.Add(save_button, 0, wx.EXPAND | wx.LEFT, 5)
        return sizer

    def __init_line_check_sizer(self, line_num):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.line0_cb = wx.CheckBox(self, wx.ID_ANY, u"Line0", wx.DefaultPosition, wx.DefaultSize, 0)
        self.line1_cb = wx.CheckBox(self, wx.ID_ANY, u"Line1", wx.DefaultPosition, wx.DefaultSize, 0)
        self.line2_cb = wx.CheckBox(self, wx.ID_ANY, u"Line2", wx.DefaultPosition, wx.DefaultSize, 0)
        self.line3_cb = wx.CheckBox(self, wx.ID_ANY, u"Line3", wx.DefaultPosition, wx.DefaultSize, 0)
        self.line0_cb.SetValue(True)
        self.line1_cb.SetValue(True)
        self.line2_cb.SetValue(True)
        self.line3_cb.SetValue(True)
        line_set_sizer1 = wx.BoxSizer(wx.VERTICAL)
        line_set_sizer2 = wx.BoxSizer(wx.VERTICAL)
        line_set_sizer1.Add(self.line0_cb, 0, wx.ALL, 0)
        line_set_sizer1.Add(self.line2_cb, 0, wx.ALL, 0)
        line_set_sizer2.Add(self.line1_cb, 0, wx.ALL, 0)
        line_set_sizer2.Add(self.line3_cb, 0, wx.ALL, 0)
        sizer.Add(line_set_sizer1, 0, wx.ALIGN_CENTER | wx.LEFT, 10)
        sizer.Add(line_set_sizer2, 0, wx.ALIGN_CENTER | wx.LEFT, 10)
        if line_num == 5:
            self.line4_cb = wx.CheckBox(self, wx.ID_ANY, u"Line3", wx.DefaultPosition, wx.DefaultSize, 0)
            self.line4_cb.SetValue(True)
            line_set_sizer3 = wx.BoxSizer(wx.VERTICAL)
            line_set_sizer3.Add(self.line4_cb, 0, wx.ALL, 0)
            sizer.Add(line_set_sizer3, 0, wx.ALIGN_CENTER | wx.LEFT, 10)
        else:
            self.line4_cb = None
        return sizer

    def on_ok(self, event):
        try:
            y_max = int(self.max_tc.GetValue())
            y_min = int(self.min_tc.GetValue())
            if y_max < y_min:
                y_min, y_max = y_max, y_min
            self.set_ybound(lower=y_min, upper=y_max)
        except ValueError:
            logger.error("Input Error: \"%s\" and \"%s\"" % (self.max_tc.GetValue(), self.min_tc.GetValue()))

    def on_save(self, event):
        dlg = wx.FileDialog(
            self,
            message="Save plot as...",
            defaultDir=os.getcwd(),
            defaultFile="%s-%s.png" % (self.get_title(), Utility.get_timestamp()),
            wildcard="PNG (*.png)|*.png",
            style=wx.FD_SAVE)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.FigureCanvas.print_figure(path, dpi=self.dpi)

    def get_title(self):
        return self.title

    def close_timer(self):
        self.timer.Stop()

    def refresh(self, event):
        raise NotImplementedError('MPL must have refresh function')

    def get_object(self):
        return self.obj

    def update(self):
        self.FigureCanvas.draw()

    def set_ybound(self, lower, upper):
        self.min_tc.SetValue(str(lower))
        self.max_tc.SetValue(str(upper))
        self.Axes.set_ybound(lower=lower, upper=upper)

    def init_axes(self, y_lower, y_upper, x_lower=0, x_upper=80):
        self.Axes.set_facecolor(self.facecolor)
        self.Axes.set_xbound(lower=x_lower, upper=x_upper)
        self.set_ybound(lower=y_lower, upper=y_upper)
        self.Axes.xaxis.set_major_locator(MultipleLocator(10))
        self.Axes.xaxis.set_minor_locator(MultipleLocator(5))
        self.Axes.yaxis.set_major_locator(MultipleLocator(10))
        self.Axes.yaxis.set_minor_locator(MultipleLocator(2))
        self.Axes.xaxis.grid(True, which='major')  # x坐标轴的网格使用次刻度
        self.Axes.yaxis.grid(True, which='major')  # x坐标轴的网格使用次刻度
        self.Axes.tick_params(labelsize=6, direction='in', grid_alpha=0.3)  # 设置坐标系文字大小
        self.Axes.set_title(self.title, size=10)
        self.update()

    def set_checkbox_label(self, *args):
        self.line0_cb.SetLabel(args[0])
        self.line1_cb.SetLabel(args[1])
        self.line2_cb.SetLabel(args[2])
        self.line3_cb.SetLabel(args[3])
        if self.line4_cb and args[4]:
            self.line4_cb.SetLabel(args[4])


class RSSIPanel(BaseMplPanel):
    def __init__(self, parent, obj):
        BaseMplPanel.__init__(self, parent)
        self.obj = obj
        self.obj.clear()
        self.title = obj.get_mpl_title()
        self.set_checkbox_label(u"Ant 0", u"Ant 1", u"Ant 2", u"Ant 3")
        self.__init_plot()
        self.init_axes(-150, -30)

    def __init_plot(self, linestyle='-'):
        linewidth = 0.9
        self._line0, = self.Axes.plot(numpy.array([]), numpy.array([]), color="#2E86C1", linewidth=linewidth,
                                      label=u'Ant 0', linestyle=linestyle)
        self._line1, = self.Axes.plot(numpy.array([]), numpy.array([]), color="black", linewidth=linewidth,
                                      label=u'Ant 1', linestyle=linestyle)
        self._line2, = self.Axes.plot(numpy.array([]), numpy.array([]), color="#C0392B", linewidth=linewidth,
                                      label=u'Ant 2', linestyle=linestyle)
        self._line3, = self.Axes.plot(numpy.array([]), numpy.array([]), color="#27AE60", linewidth=linewidth,
                                      label=u'Ant 3', linestyle=linestyle)
        self.Axes.legend()

    def refresh(self, event):
        if self.line0_cb.IsChecked() or self.line1_cb.IsChecked() or self.line2_cb.IsChecked() or self.line3_cb.IsChecked():
            a0, a1, a2, a3 = self.obj.next()
            x_max = len(a0) if len(a0) > 80 else 80
            x_min = x_max - 80
            self.Axes.set_xbound(lower=x_min, upper=x_max)
        else:
            return
        if self.line0_cb.IsChecked():
            self._line0.set_xdata(numpy.arange(len(a0)))
            self._line0.set_ydata(numpy.array(a0))
        if self.line1_cb.IsChecked():
            self._line1.set_xdata(numpy.arange(len(a1)))
            self._line1.set_ydata(numpy.array(a1))
        if self.line2_cb.IsChecked():
            self._line2.set_xdata(numpy.arange(len(a2)))
            self._line2.set_ydata(numpy.array(a2))
        if self.line3_cb.IsChecked():
            self._line3.set_xdata(numpy.arange(len(a3)))
            self._line3.set_ydata(numpy.array(a3))
        self.update()


class SNRPanel(BaseMplPanel):
    def __init__(self, parent, objs):
        BaseMplPanel.__init__(self, parent)
        self.set_checkbox_label(u"User 0", u"User 1", u"User 2", u"User 3")
        self.user0 = self.get_object(objs, 'user0')
        self.user1 = self.get_object(objs, 'user1')
        self.user2 = self.get_object(objs, 'user2')
        self.user3 = self.get_object(objs, 'user3')
        self.user0.clear()
        self.user1.clear()
        self.user2.clear()
        self.user3.clear()
        self.title = "SNR"
        self.__init_plot()
        self.init_axes(-10, 30)

    def get_object(self, objs, name):
        for obj in objs:
            if name in obj.get_name():
                return obj
        return None

    def refresh(self, event):
        if self.line0_cb.IsChecked() or self.line1_cb.IsChecked() or self.line2_cb.IsChecked() or self.line3_cb.IsChecked():
            pass
        else:
            return
        a0 = self.user0.next()
        a1 = self.user1.next()
        a2 = self.user2.next()
        a3 = self.user3.next()
        x_max = len(a0) if len(a0) > 80 else 80
        x_min = x_max - 80
        self.Axes.set_xbound(lower=x_min, upper=x_max)
        if self.line0_cb.IsChecked():
            self._line0.set_xdata(numpy.arange(len(a0)))
            self._line0.set_ydata(numpy.array(a0))
        if self.line1_cb.IsChecked():
            self._line1.set_xdata(numpy.arange(len(a1)))
            self._line1.set_ydata(numpy.array(a1))
        if self.line2_cb.IsChecked():
            self._line2.set_xdata(numpy.arange(len(a2)))
            self._line2.set_ydata(numpy.array(a2))
        if self.line3_cb.IsChecked():
            self._line3.set_xdata(numpy.arange(len(a3)))
            self._line3.set_ydata(numpy.array(a3))
        self.update()

    def __init_plot(self, linestyle='--'):
        linewidth = 1.1
        self._line0, = self.Axes.plot(numpy.array([]), numpy.array([]), color="#2E86C1", linewidth=linewidth,
                                      label=u'User 0', linestyle=linestyle)
        self._line1, = self.Axes.plot(numpy.array([]), numpy.array([]), color="black", linewidth=linewidth,
                                      label=u'User 1', linestyle=linestyle)
        self._line2, = self.Axes.plot(numpy.array([]), numpy.array([]), color="#C0392B", linewidth=linewidth,
                                      label=u'User 2', linestyle=linestyle)
        self._line3, = self.Axes.plot(numpy.array([]), numpy.array([]), color="#27AE60", linewidth=linewidth,
                                      label=u'User 3', linestyle=linestyle)
        self.Axes.legend()


class BLERPanel(BaseMplPanel):
    def __init__(self, parent, objs):
        BaseMplPanel.__init__(self, parent, line_num=5)
        self.set_checkbox_label(u"User 0", u"User 1", u"User 2", u"User 3", u"BR")
        self.user0 = self.get_object(objs, 'user0')
        self.user1 = self.get_object(objs, 'user1')
        self.user2 = self.get_object(objs, 'user2')
        self.user3 = self.get_object(objs, 'user3')
        self.br = self.get_object(objs, 'br')
        self.user0.clear()
        self.user1.clear()
        self.user2.clear()
        self.user3.clear()
        self.br.clear()
        self.title = "BLER"
        self.__init_plot()
        self.init_axes(0, 100)

    def get_object(self, objs, name):
        for obj in objs:
            if name in obj.get_name():
                return obj
        return None

    def refresh(self, event):
        if self.line0_cb.IsChecked() or self.line1_cb.IsChecked() or self.line2_cb.IsChecked() or self.line3_cb.IsChecked():
            pass
        else:
            return
        a0 = self.user0.next()
        a1 = self.user1.next()
        a2 = self.user2.next()
        a3 = self.user3.next()
        br = self.br.next()
        x_max = len(a0) if len(a0) > 80 else 80
        x_min = x_max - 80
        self.Axes.set_xbound(lower=x_min, upper=x_max)
        if self.line0_cb.IsChecked():
            self._line0.set_xdata(numpy.arange(len(a0)))
            self._line0.set_ydata(numpy.array(a0))
        if self.line1_cb.IsChecked():
            self._line1.set_xdata(numpy.arange(len(a1)))
            self._line1.set_ydata(numpy.array(a1))
        if self.line2_cb.IsChecked():
            self._line2.set_xdata(numpy.arange(len(a2)))
            self._line2.set_ydata(numpy.array(a2))
        if self.line3_cb.IsChecked():
            self._line3.set_xdata(numpy.arange(len(a3)))
            self._line3.set_ydata(numpy.array(a3))
        if self.line4_cb.IsChecked():
            self._line4.set_xdata(numpy.arange(len(br)))
            self._line4.set_ydata(numpy.array(br))
        self.update()

    def __init_plot(self, linestyle='--'):
        linewidth = 1.1
        self._line0, = self.Axes.plot(numpy.array([]), numpy.array([]), color="#2E86C1", linewidth=linewidth,
                                      label=u'User 0', linestyle=linestyle)
        self._line1, = self.Axes.plot(numpy.array([]), numpy.array([]), color="black", linewidth=linewidth,
                                      label=u'User 1', linestyle=linestyle)
        self._line2, = self.Axes.plot(numpy.array([]), numpy.array([]), color="#C0392B", linewidth=linewidth,
                                      label=u'User 2', linestyle=linestyle)
        self._line3, = self.Axes.plot(numpy.array([]), numpy.array([]), color="#27AE60", linewidth=linewidth,
                                      label=u'User 3', linestyle=linestyle)
        self._line4, = self.Axes.plot(numpy.array([]), numpy.array([]), color="#A569BD", linewidth=linewidth,
                                      label=u'BR', linestyle=linestyle)
        self.Axes.legend()

    def __init_line_check_szer(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        return sizer
