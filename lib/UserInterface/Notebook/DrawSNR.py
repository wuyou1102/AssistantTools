# -*- encoding:UTF-8 -*-
import wx
from NotebookBase import NotebookBase
from lib import Utility
from MatplotPanel import MatplotPanel
from time import sleep
from lib.Config import Instrument
from matplotlib import animation

Logger = Utility.getLogger(__name__)


class DrawSNR(NotebookBase):
    def __init__(self, parent):
        NotebookBase.__init__(self, parent=parent, name=u"信号强度")
        self.MPL = MatplotPanel(self)
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        MplSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.VERTICAL)
        MplSizer.Add(self.MPL, 1, wx.EXPAND)
        MainSizer.Add(MplSizer, 1, wx.EXPAND | wx.ALL, 5)

        self.line_snr1, = self.MPL.axes.plot([], [], color="green", linewidth=0.35, linestyle="-")
        self.line_snr2, = self.MPL.axes.plot([], [], color="red", linewidth=0.35, linestyle="-")

        self.SD = None
        self.__pause = False
        self.SetSizer(MainSizer)

    def StartDraw(self):
        if not Utility.is_alive('__CollectSignalData'):
            self.SD = None
        if self.SD:
            return True
        self.SD = SignalData()
        self.__pause = False
        self.MPL.cla()
        self.MPL.init_axis()
        interval = 0.5
        self.SD.collect_data(interval)
        anim = animation.FuncAnimation(self.MPL.Figure, self.__UpdateSignal)
        # Utility.append_work(target=self.__DrawSignal, interval=interval, allow_dupl=False)

    def __UpdateSignal(self, i):
        snr1, snr2, times = self.SD.get_data()
        snr1 = self.MPL.array(snr1)
        snr2 = self.MPL.array(snr2)
        times = self.MPL.array(times)
        self.line_snr1.set_data(snr1, times)

        return self.line_snr1,

    def __DrawSignal(self, interval):
        sleep(0.5)
        while True:
            if self.__pause:
                continue
            sleep(interval)
            if not self.SD:
                break
            else:
                snr1, snr2, times = self.SD.get_data()
                if len(times) > 100:
                    self.MPL.axis([times[-100], times[-1], None, None])
                self.line_snr1.set_data(snr1, times)
                self.MPL.axes.draw_artist(self.line_snr1)

                # self.MPL.plot(times, snr1, color="green", linewidth=0.35, linestyle="-")
            # self.MPL.plot(times, snr2, color="red", linewidth=0.35, linestyle="-")

    def PauseDraw(self, boolean):
        Logger.info('PauseDraw:%s' % boolean)
        self.__pause = boolean

    def StopDraw(self):
        if self.SD:
            Logger.info('StopDraw')
            self.SD.stop()
            self.SD = None
        else:
            Logger.info('Nothing need stop.')


class SignalData(object):
    def __init__(self):
        self.__reg = Instrument.get_register()
        # self.__reg.Set(0x60680000, 0x000B0201)
        # sleep(0.1)
        # self.__reg.Set(0x60680000, 0x000B0200)
        self.__count = 0
        self.__RSSI_0 = list()
        self.__RSSI_1 = list()
        self.__times = list()
        self.__stop = False

    def stop(self):
        self.__stop = True

    def get_minimum(self):
        minimum = min(
            len(self.__RSSI_0),
            len(self.__RSSI_1),
            len(self.__times),
        )
        return minimum

    def get_data(self):
        minimum = self.get_minimum()
        return \
            self.__RSSI_0[:minimum], \
            self.__RSSI_1[:minimum], \
            self.__times[:minimum]

    def collect_data(self, interval):
        Logger.info('Start Collect Signal Data')
        Utility.append_work(target=self.__CollectSignalData, interval=interval, allow_dupl=False)

    def __CollectSignalData(self, interval):
        while True:
            if self.__stop:
                break
            self.__append(self.__times, self.__count)
            self.__append(self.__RSSI_0, self.__get_register_rssi_0())
            self.__append(self.__RSSI_1, self.__get_register_rssi_1())
            self.__count += 1
            sleep(interval)

    def __append(self, lst, element):
        # if len(lst) > 10:
        #     lst.pop(0)
        lst.append(element)

    def __get_register_rssi_1(self):
        data = self.__reg.Get(0x6068040C)
        return self.convert_data_to_rssi(data=data, start=4)

    def __get_register_rssi_0(self):
        data = self.__reg.Get(0x6068040C)
        return self.convert_data_to_rssi(data=data, start=0)

    def convert_data_to_rssi(self, data, start=0):
        # data = data[start:start + 4]
        # sim = '0x%s' % tmp[2:4]
        # dig = '0x%s' % tmp[0:2]
        rssi = int(data[start:start + 2], 16) + int(data[start + 2:start + 4], 16)
        # print rssi
        return -rssi


if __name__ == '__main__':
    sd = SignalData()
    sd.collect_data(interval=1)
    while True:
        continue
