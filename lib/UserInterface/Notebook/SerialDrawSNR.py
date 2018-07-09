# -*- encoding:UTF-8 -*-
# -*- encoding:UTF-8 -*-
import wx
from NotebookBase import NotebookBase
from lib import Utility
from SimpleMatplotPanel import MatplotPanel
from lib.Instrument import Serial
from time import sleep
from matplotlib import animation
import numpy as np
import re

port_pattern = re.compile(r'(COM\d+)')
bler_pattern = re.compile(
    r'br \(\-?\d+,\-?\d+,(\-?\d+)\),fch \(\-?\d+,\-?\d+,(\-?\d+)\), ds \(\-?\d+,\-?\d+,(\-?\d+)\), new pkt \(\-?\d+,\-?\d+\), l1 stat:(ap,\d+|nd)')
rssi_snr_pattern = re.compile(
    r'rssi \(br:(\-?\d+),\-?\d+, ds:(\-?\d+),\-?\d+\), snr \(br:(\-?\d+),\-?\d+, ds:(\-?\d+),\-?\d+\), l1 stat:(ap,\d+|nd)')

Logger = Utility.getLogger(__name__)


class SerialDrawSNR(NotebookBase):
    def __init__(self, parent):
        NotebookBase.__init__(self, parent=parent, name="信号强度")
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        PortsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.C_ports = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, Serial.get_ports(), 0)
        self.session = None
        self.DC = None
        self.lines = list()
        self.mAnim1 = None
        self.mAnim2 = None
        self.mAnim3 = None
        B_Refresh = wx.Button(self, wx.ID_ANY, u"Refresh", wx.DefaultPosition, (60, 27), 0)
        B_Refresh.Bind(wx.EVT_BUTTON, self.on_refresh)
        B_Connect = wx.Button(self, wx.ID_ANY, u"Connect", wx.DefaultPosition, (-1, 27), 0)
        B_Connect.Bind(wx.EVT_BUTTON, self.on_connect)
        # B_New = wx.Button(self, wx.ID_ANY, u"+", wx.DefaultPosition, (30, 27), 0)
        # B_New.Bind(wx.EVT_BUTTON, self.on_new_window)

        PortsSizer.Add(B_Refresh, 0, wx.ALIGN_CENTER_VERTICAL)
        PortsSizer.Add(self.C_ports, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)
        PortsSizer.Add(B_Connect, 0, wx.ALIGN_CENTER_VERTICAL)
        # PortsSizer.Add(B_New, 0, wx.ALIGN_CENTER_VERTICAL)
        self.MPL_RSSI = MatplotPanel(self, 0, 50, -120, -30)
        self.MPL_BLER = MatplotPanel(self, 0, 50, 0, 100)
        self.MPL_SNR = MatplotPanel(self, 0, 50, -10, 30, ya=5, yi=1)

        OutputSizer = wx.BoxSizer(wx.VERTICAL)
        OutputSizer.Add(self.MPL_RSSI, 1, wx.EXPAND)
        OutputSizer.Add(self.MPL_SNR, 1, wx.EXPAND)
        OutputSizer.Add(self.MPL_BLER, 1, wx.EXPAND)

        MainSizer.Add(PortsSizer, 0, wx.ALL, 5)
        MainSizer.Add(OutputSizer, 1, wx.EXPAND)

        self.SetSizer(MainSizer)

    def on_connect(self, event):

        obj = event.GetEventObject()
        state = obj.GetLabel()
        if state == "Connect":
            self.StopDraw()
            port = self.C_ports.GetStringSelection()
            if not port:
                return False
            port = Utility.find_in_string(port_pattern, port)
            try:
                if self.session:
                    self.session.close()
                self.session = Serial.Serial(port=port, baudrate=921600)
                self.DC = DataCollect(session=self.session, R=self.MPL_RSSI.axes, S=self.MPL_SNR.axes,
                                      B=self.MPL_BLER.axes)
                self.StartDraw()
                obj.SetLabel("Disconnect")
            except IOError:
                Logger.error(u"At the same time, the same serial port can only be used by one device.")

        elif state == "Disconnect":
            if self.session:
                self.session.close()
            obj.SetLabel("Connect")
        else:
            if self.session:
                self.session.close()
            obj.SetLabel("Connect")

    def on_refresh(self, event):
        self.C_ports.Items = Serial.get_ports()

    def StartDraw(self):
        self.mAnim1 = animation.FuncAnimation(self.MPL_BLER.Figure, self.Update, frames=100,
                                              interval=500,
                                              blit=True)
        self.mAnim2 = animation.FuncAnimation(self.MPL_SNR.Figure, self.Update, frames=100,
                                              interval=500,
                                              blit=True)
        self.mAnim3 = animation.FuncAnimation(self.MPL_RSSI.Figure, self.Update, frames=100,
                                              interval=500,
                                              blit=True)

    def StopDraw(self):
        Logger.info('StopDrawLine')
        if self.mAnim1:
            self.mAnim1._stop()
            self.mAnim1 = None
        if self.mAnim2:
            self.mAnim2._stop()
            self.mAnim2 = None
        if self.mAnim3:
            self.mAnim3._stop()
            self.mAnim3 = None
        if self.DC:
            self.DC.stop()

        self.MPL_RSSI.cla()
        self.MPL_RSSI.init_axis()
        self.MPL_SNR.cla()
        self.MPL_SNR.init_axis()
        self.MPL_BLER.cla()
        self.MPL_BLER.init_axis()

    def Update(self, i):
        return self.lines


from lib.UserInterface.Dialog import DialogBase


class DataCollect(object):
    def __init__(self, session, R, S, B):
        self.R = R
        self.S = S
        self.B = B
        self.session = session
        self.flag = True
        Utility.append_work(target=self.COLLECT_DATA)

    def stop(self):
        self.flag = False

    def COLLECT_DATA(self):
        while self.session.is_open() and self.flag:
            line = self.session.read_line()
            if not line:
                continue
            if line.startswith("br ("):
                try:
                    br, fch, ds, mode = Utility.find_in_string(bler_pattern, line)
                except ValueError:
                    continue
                name = 'bler_%s' % mode.replace(',', '_')
                try:
                    self.__getattribute__(name)
                except AttributeError:
                    self.init_bler_line(name)
                self.update_bler_line(name, br, fch, ds)
            elif line.startswith('rssi ('):
                try:
                    r_br, r_ds, s_br, s_ds, mode = Utility.find_in_string(rssi_snr_pattern, line)
                except ValueError:
                    continue
                r_name = 'rssi_%s' % mode.replace(',', '_')
                s_name = 'snr_%s' % mode.replace(',', '_')
                try:
                    self.__getattribute__(r_name)
                except AttributeError:
                    self.init_rssi_line(r_name)
                self.update_rssi_line(r_name, r_br, r_ds)
                try:
                    self.__getattribute__(s_name)
                except AttributeError:
                    self.init_snr_line(s_name)
                self.update_snr_line(s_name, s_br, s_ds)

    def init_bler_line(self, name):
        if 'ap' in name:
            self.__setattr__(name, True)
            self.__setattr__('%s_fch' % name, Line(label='%s_fch' % name, linestyle='-', axes=self.B))
            self.__setattr__('%s_ds' % name, Line(label='%s_ds' % name, linestyle='-', axes=self.B))
            # self.__setattr__('%s_br' % name, Line(label='%s_br' % name, linestyle='-', axes=self.B))
            self.B.legend(loc='best', ncol=2, fontsize='x-small', framealpha=0.4)
        else:
            self.__setattr__(name, True)
            self.__setattr__('%s_fch' % name, Line(label='%s_fch' % name, linestyle='-', axes=self.B))
            self.__setattr__('%s_ds' % name, Line(label='%s_ds' % name, linestyle='-', axes=self.B))
            self.__setattr__('%s_br' % name, Line(label='%s_br' % name, linestyle='-', axes=self.B))
            self.B.legend(loc='best', ncol=3, fontsize='x-small', framealpha=0.4)

    def update_bler_line(self, name, fch, br, ds):
        if 'ap' in name:
            self.__getattribute__('%s_fch' % name).Append(int(fch))
            # self.__getattribute__('%s_br' % name).Append(int(br))
            self.__getattribute__('%s_ds' % name).Append(int(ds))
        else:
            self.__getattribute__('%s_fch' % name).Append(int(fch))
            self.__getattribute__('%s_br' % name).Append(int(br))
            self.__getattribute__('%s_ds' % name).Append(int(ds))

    def init_rssi_line(self, name):
        if 'ap' in name:
            self.__setattr__(name, True)
            self.__setattr__('%s_ds' % name, Line(label='%s_ds' % name, linestyle='-', axes=self.R))
            # self.__setattr__('%s_br' % name, Line(label='%s_br' % name, linestyle='-', axes=self.R))
            self.R.legend(loc='best', ncol=3, fontsize='x-small', framealpha=0.4)
        else:
            self.__setattr__(name, True)
            self.__setattr__('%s_ds' % name, Line(label='%s_ds' % name, linestyle='-', axes=self.R))
            self.__setattr__('%s_br' % name, Line(label='%s_br' % name, linestyle='-', axes=self.R))
            self.R.legend(loc='best', ncol=3, fontsize='x-small', framealpha=0.4)

    def update_rssi_line(self, name, br, ds):
        if 'ap' in name:
            # self.__getattribute__('%s_br' % name).Append(int(br))
            self.__getattribute__('%s_ds' % name).Append(int(ds))
        else:
            self.__getattribute__('%s_br' % name).Append(int(br))
            self.__getattribute__('%s_ds' % name).Append(int(ds))

    def init_snr_line(self, name):
        if 'ap' in name:
            self.__setattr__(name, True)
            self.__setattr__('%s_ds' % name, Line(label='%s_ds' % name, linestyle='-', axes=self.S))
            # self.__setattr__('%s_br' % name, Line(label='%s_br' % name, linestyle='-', axes=self.S))
            self.S.legend(loc='best', ncol=3, fontsize='x-small', framealpha=0.4)
        else:
            self.__setattr__(name, True)
            self.__setattr__('%s_ds' % name, Line(label='%s_ds' % name, linestyle='-', axes=self.S))
            self.__setattr__('%s_br' % name, Line(label='%s_br' % name, linestyle='-', axes=self.S))
            self.S.legend(loc='best', ncol=3, fontsize='x-small', framealpha=0.4)

    def update_snr_line(self, name, br, ds):
        if 'ap' in name:
            # self.__getattribute__('%s_br' % name).Append(int(br))
            self.__getattribute__('%s_ds' % name).Append(int(ds))
        else:
            self.__getattribute__('%s_br' % name).Append(int(br))
            self.__getattribute__('%s_ds' % name).Append(int(ds))


class Line(object):
    def __init__(self, axes, label, linestyle, color='#FF0000', linewidth=0.85):
        if 'ap_0' in label:
            color = '#FF0000'
        elif 'ap_1' in label:
            color = '#000000'
        elif 'ap_2' in label:
            color = '#00BFA5'
        else:
            color = '#000000'

        if 'ds' in label:
            marker = 'o'
            markersize = '3'
        elif 'br' in label:
            linestyle = '--'
            marker = '*'
            markersize = '5'
        else:
            linestyle = ':'
            marker = ''
            markersize = '1'
            linewidth = 1.25

        self.axes = axes
        self.label = label
        self.color = color
        self.linestyle = linestyle
        self.linewidth = linewidth
        self._singal = []
        self._sequence = []
        self._line, = self.axes.plot(np.array(self._singal), np.array(self._sequence), label=self.label,
                                     color=self.color,
                                     linewidth=self.linewidth,
                                     linestyle=self.linestyle,
                                     marker=marker,
                                     markersize=markersize)
        self.count = 0
        self.np_seq = np.arange(0, 50, 1)

    def Append(self, signal):
        self._singal.append(signal)
        if self.count < 49:
            self._sequence.append(self.count)
            self._line.set_data(np.array(self._sequence), np.array(self._singal), )
            self.count += 1
        else:
            self._line.set_data(self.np_seq, np.array(self._singal[-50:]), )

    def GetData(self):
        return self._sequence, self._singal

    def GetLine(self):
        return self._line

    # def Init(self):
    #     self._singal = np.array([])
    #     self._sequence = np.array([])
    #     self._line.set_data(self._sequence, self._singal, )

    def get_count(self):
        return self.count
