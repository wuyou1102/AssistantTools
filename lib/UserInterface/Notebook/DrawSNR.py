# -*- encoding:UTF-8 -*-
import wx
from NotebookBase import NotebookBase
from lib import Utility
from MatplotPanel import MatplotPanel
from time import sleep
from lib.Config import Instrument
from matplotlib import animation
import numpy as np

Logger = Utility.getLogger(__name__)

filter_list = ['BR']


class DrawSNR(NotebookBase):
    def __init__(self, parent):
        NotebookBase.__init__(self, parent=parent, name=u"信号强度")
        self.MPL = MatplotPanel(self)
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        MplSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u""), wx.VERTICAL)
        MplSizer.Add(self.MPL, 1, wx.EXPAND)
        MainSizer.Add(MplSizer, 1, wx.EXPAND | wx.ALL, 5)
        self.mAnim = None
        self.interval = 0.5
        self.lines = list()
        self.count = 0
        self.SD = SignalData(self.MPL.axes)
        self.__pause = False
        self.SetSizer(MainSizer)

    def StartDraw(self):
        # if not Utility.is_alive('__CollectSignalData'):
        #     self.SD.reset_data()
        # else:
        #     return True
        # self.__pause = False
        if self.mAnim:
            Logger.info("Draw is already running.")
            return True

        # self.SD.collect_data(self.interval)
        self.SD.reset_data()
        self.mAnim = animation.FuncAnimation(self.MPL.Figure, self.UpdateSignal, frames=100,
                                             interval=self.interval * 1000,
                                             blit=True)

    def UpdateSignal(self, i):
        if self.__pause:
            return self.lines
        if self.count>100:
            self.MPL.axis([self.count - 100, self.count, None, None])
        self.SD.updata(count=self.count)
        self.count += 1
        return self.lines

        # def __DrawSignal(self, interval):

    #     sleep(0.5)
    #     while True:
    #         if self.__pause:
    #             continue
    #         sleep(interval)
    #         if not self.SD:
    #             break
    #         else:
    #             snr1, snr2, times = self.SD.get_data()
    #             if len(times) > 100:
    #                 self.MPL.axis([times[-100], times[-1], None, None])
    #             self.line_snr1.set_data(snr1, times)
    #             self.MPL.axes.draw_artist(self.line_snr1)
    #
    #             # self.MPL.plot(times, snr1, color="green", linewidth=0.35, linestyle="-")
    #         # self.MPL.plot(times, snr2, color="red", linewidth=0.35, linestyle="-")

    def PauseDraw(self, boolean):
        Logger.info('PauseDraw:%s' % boolean)
        self.__pause = boolean

    def StopDraw(self):
        if self.mAnim:
            Logger.info('StopDrawLine')
            self.mAnim._stop()
            self.mAnim = None


class SignalData(object):
    def __init__(self, axes):
        self.__reg = Instrument.get_register()
        self.axes = axes
        self.BR = BR(self.axes)
        self.CS = CS(self.axes)
        self.USER0 = USER0(self.axes)
        self.USER1 = USER1(self.axes)
        self.USER2 = USER2(self.axes)
        self.USER3 = USER3(self.axes)

    def reset_data(self):
        self.BR.resest()
        self.CS.resest()
        self.USER0.resest()
        self.USER1.resest()
        self.USER2.resest()
        self.USER3.resest()

    # def stop(self):
    #     self.__stop = True

    # def collect_data(self, interval):
    #     Logger.info('Start Collect Signal Data')
    #     Utility.append_work(target=self.__CollectSignalData, interval=interval, allow_dupl=False)

    # def __CollectSignalData(self, interval):
    #     count = 0
    #     while True:
    #         if self.__stop:
    #             break
    #         self.BR.update(count)
    #         self.CS.update(count)
    #         self.USER0.update(count)
    #         self.USER1.update(count)
    #         self.USER2.update(count)
    #         self.USER3.update(count)
    #         count += 1
    #         sleep(interval)

    def updata(self, count):
        for f in filter_list:
            self.__getattribute__(f).update(count)
            # self.BR.update(count)
            # self.CS.update(count)
            # self.USER0.update(count)
            # self.USER1.update(count)
            # self.USER2.update(count)
            # self.USER3.update(count)


class RSSI(object):
    def __init__(self, axes, color, label, linestyle, linewidth=0.75):
        self.axes = axes
        self.color = color
        self.label = label
        self.linestyle = linestyle
        self.linewidth = linewidth
        self._singal = np.array([])
        self._sequence = np.array([])
        self._line, = self.axes.plot(self._singal, self._sequence, label=self.label, color=self.color,
                                     linewidth=self.linewidth,
                                     linestyle=self.linestyle)

    def Append(self, signal, number):
        self._singal = np.append(self._singal, signal)
        self._sequence = np.append(self._sequence, number)
        self._line.set_data(self._sequence, self._singal, )

    def GetData(self):
        return self._sequence, self._singal

    def GetLine(self):
        self._line

    def Init(self):
        self._singal = np.array([])
        self._sequence = np.array([])
        self._line.set_data(self._sequence, self._singal, )


class Aerial(object):
    def __init__(self, axes, lable, color):
        self.label = lable
        self.axes = axes
        self.A0 = RSSI(label=self.label + u'_0', color=color, linestyle='-', axes=axes)
        self.A1 = RSSI(label=self.label + u'_1', color=color, linestyle='-.', axes=axes)
        self.A2 = RSSI(label=self.label + u'_2', color=color, linestyle=':', axes=axes)
        self.A3 = RSSI(label=self.label + u'_3', color=color, linestyle='--', axes=axes)

    def resest(self):
        self.A0.Init()
        self.A1.Init()
        self.A2.Init()
        self.A3.Init()

    def Aerials(self):
        return self.A0, self.A1, self.A2, self.A3

    def A0_Line(self):
        return self.A0.GetLine()

    def A1_Line(self):
        return self.A1.GetLine()

    def A2_Line(self):
        return self.A2.GetLine()

    def A3_Line(self):
        return self.A3.GetLine()

    def A0_Data(self):
        return self.A0.GetData()

    def A1_Data(self):
        return self.A1.GetData()

    def A2_Data(self):
        return self.A2.GetData()

    def A3_Data(self):
        return self.A3.GetData()

    def _read_register(self, address):
        reg = Instrument.get_register()
        byte = reg.GetByte(address=address)
        if byte:
            return byte[0], byte[1], byte[2], byte[3]
        return False, False, False, False

    @staticmethod
    def _merge_signal(simulation, digit):
        if simulation and digit:
            return -ord(simulation) - ord(digit)
        return None


class BR(Aerial):
    def __init__(self, axes, label='BR', color='g'):
        Aerial.__init__(self, axes, label, color)

    def update(self, i):
        # s=simulation  d=digit  p=placeholder

        s0, d0, s1, d1 = self._read_register(0x60680450)
        s2, d2, s3, d3 = self._read_register(0x60680454)
        self.A0.Append(self._merge_signal(s0, d0), i)
        self.A1.Append(self._merge_signal(s1, d1), i)
        self.A2.Append(self._merge_signal(s2, d2), i)
        self.A3.Append(self._merge_signal(s3, d3), i)


class CS(Aerial):
    def __init__(self, axes, label='CS', color='b'):
        Aerial.__init__(self, axes, label, color)
        # 0x442 天线0的模拟AGC增益
        # 0x443 天线0的数字AGC增益
        # 0x444 天线1的模拟AGC增益
        # 0x445 天线1的数字AGC增益
        # 0x446 天线2的模拟AGC增益
        # 0x447 天线2的数字AGC增益
        # 0x448 天线3的模拟AGC增益
        # 0x449 天线3的数字AGC增益

    def update(self, i):
        # s=simulation  d=digit  p=placeholder
        p0, p1, s0, d0 = self._read_register(0x60680440)
        s1, d1, s2, d2 = self._read_register(0x60680444)
        s3, d3, p2, p3 = self._read_register(0x60680448)
        self.A0.Append(self._merge_signal(s0, d0), i)
        self.A1.Append(self._merge_signal(s1, d1), i)
        self.A2.Append(self._merge_signal(s2, d2), i)
        self.A3.Append(self._merge_signal(s3, d3), i)


class USER0(Aerial):
    def __init__(self, axes, label='User0', color='r'):
        Aerial.__init__(self, axes, label, color)

        # 0x40a
        # usr0天线0的模拟AGC增益
        # 0x40b
        # usr0天线0的数字AGC增益
        # 0x40c
        # usr0天线1的模拟AGC增益
        # 0x40d
        # usr0天线1的数字AGC增益
        # 0x40e
        # usr0天线2的模拟AGC增益
        # 0x40f
        # usr0天线2的数字AGC增益
        # 0x410
        # usr0天线3的模拟AGC增益
        # 0x411
        # usr0天线3的数字AGC增益

    def update(self, i):
        p0, p1, s0, d0 = self._read_register(0x60680408)
        s1, d1, s2, d2 = self._read_register(0x6068040c)
        s3, d3, p2, p3 = self._read_register(0x60680410)
        self.A0.Append(self._merge_signal(s0, d0), i)
        self.A1.Append(self._merge_signal(s1, d1), i)
        self.A2.Append(self._merge_signal(s2, d2), i)
        self.A3.Append(self._merge_signal(s3, d3), i)


class USER1(Aerial):
    def __init__(self, axes, label='User1', color='c'):
        Aerial.__init__(self, axes, label, color)
        #
        # 0x418
        # usr1天线0的模拟AGC增益
        # 0x419
        # usr1天线0的数字AGC增益
        # 0x41a
        # usr1天线1的模拟AGC增益
        # 0x41b
        # usr1天线1的数字AGC增益
        # 0x41c
        # usr1天线2的模拟AGC增益
        # 0x41d
        # usr1天线2的数字AGC增益
        # 0x41e
        # usr1天线3的模拟AGC增益
        # 0x41f
        # usr1天线3的数字AGC增益

    def update(self, i):
        s0, d0, s1, d1 = self._read_register(0x60680418)
        s2, d2, s3, d3 = self._read_register(0x6068041c)
        self.A0.Append(self._merge_signal(s0, d0), i)
        self.A1.Append(self._merge_signal(s1, d1), i)
        self.A2.Append(self._merge_signal(s2, d2), i)
        self.A3.Append(self._merge_signal(s3, d3), i)


class USER2(Aerial):
    def __init__(self, axes, label='User2', color='m'):
        Aerial.__init__(self, axes, label, color)

        # 0x426
        # usr2天线0的模拟AGC增益
        # 0x427
        # usr2天线0的数字AGC增益
        # 0x428
        # usr2天线1的模拟AGC增益
        # 0x429
        # usr2天线1的数字AGC增益
        # 0x42a
        # usr2天线2的模拟AGC增益
        # 0x42b
        # usr2天线2的数字AGC增益
        # 0x42c
        # usr2天线3的模拟AGC增益
        # 0x42d
        # usr2天线3的数字AGC增益

    def update(self, i):
        p0, p1, s0, d0 = self._read_register(0x60680424)
        s1, d1, s2, d2 = self._read_register(0x60680428)
        s3, d3, p2, p3 = self._read_register(0x6068042c)
        self.A0.Append(self._merge_signal(s0, d0), i)
        self.A1.Append(self._merge_signal(s1, d1), i)
        self.A2.Append(self._merge_signal(s2, d2), i)
        self.A3.Append(self._merge_signal(s3, d3), i)


class USER3(Aerial):
    def __init__(self, axes, label='User3', color='y'):
        Aerial.__init__(self, axes, label, color)
        # 0x434
        # usr3天线0的模拟AGC增益
        # 0x435
        # usr3天线0的数字AGC增益
        # 0x436
        # usr3天线1的模拟AGC增益
        # 0x437
        # usr3天线1的数字AGC增益
        # 0x438
        # usr3天线2的模拟AGC增益
        # 0x439
        # usr3天线2的数字AGC增益
        # 0x43a
        # usr3天线3的模拟AGC增益
        # 0x43b
        # usr3天线3的数字AGC增益

    def update(self, i):
        s0, d0, s1, d1 = self._read_register(0x60680434)
        s2, d2, s3, d3 = self._read_register(0x60680438)
        self.A0.Append(self._merge_signal(s0, d0), i)
        self.A1.Append(self._merge_signal(s1, d1), i)
        self.A2.Append(self._merge_signal(s2, d2), i)
        self.A3.Append(self._merge_signal(s3, d3), i)


class SNR(object):
    def __init__(self):
        pass


if __name__ == '__main__':
    br = BR()
    import time

    for x in range(100):
        br.update(x)
        time.sleep(0.2)
    a, b = br.A1.GetData()
    print a
    print b
