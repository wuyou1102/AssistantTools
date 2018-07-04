# -*- encoding:UTF-8 -*-
import wx
from NotebookBase import NotebookBase
from lib import Utility
from lib.Instrument import Serial
import re

port_pattern = re.compile(r'(COM\d+)')
Logger = Utility.getLogger(__name__)


class SerialTool(NotebookBase):
    def __init__(self, parent):
        NotebookBase.__init__(self, parent=parent, name="串口工具")
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        PortsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.C_ports = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, Serial.get_ports(), 0)
        baudrates = ['115200', '921600']
        self.session = None
        self.filters = list()
        self.C_baudrate = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, baudrates, 0)
        self.C_baudrate.SetSelection(0)
        B_Refresh = wx.Button(self, wx.ID_ANY, u"Refresh", wx.DefaultPosition, (60, 27), 0)
        B_Refresh.Bind(wx.EVT_BUTTON, self.on_refresh)
        B_Connect = wx.Button(self, wx.ID_ANY, u"Connect", wx.DefaultPosition, (-1, 27), 0)
        B_Connect.Bind(wx.EVT_BUTTON, self.on_connect)
        B_New = wx.Button(self, wx.ID_ANY, u"+", wx.DefaultPosition, (30, 27), 0)
        B_New.Bind(wx.EVT_BUTTON, self.on_new_window)

        PortsSizer.Add(B_Refresh, 0, wx.ALIGN_CENTER_VERTICAL)
        PortsSizer.Add(self.C_ports, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)
        PortsSizer.Add(self.C_baudrate, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)
        PortsSizer.Add(B_Connect, 0, wx.ALIGN_CENTER_VERTICAL)
        PortsSizer.Add(B_New, 0, wx.ALIGN_CENTER_VERTICAL)

        FilterSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.filter_tc = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        B_OK = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, (40, 32), 0)
        B_OK.Bind(wx.EVT_BUTTON, self.on_ok)

        FilterSizer.Add(self.filter_tc, 1, wx.EXPAND)
        FilterSizer.Add(B_OK, 0, wx.ALIGN_CENTER_VERTICAL)
        OutputSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.log_tc = wx.TextCtrl(self, wx.ID_ANY, '',
                                  style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        self.log_tc.SetInsertionPointEnd()
        self.log_tc.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL, False))
        OutputSizer.Add(self.log_tc, 1, wx.EXPAND)
        InputSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.input_tc = wx.TextCtrl(self, wx.ID_ANY, '', style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
        self.input_tc.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL, False))
        self.input_tc.Bind(wx.EVT_TEXT_ENTER, self.after_enter)
        InputSizer.Add(self.input_tc, 1, wx.EXPAND)

        MainSizer.Add(PortsSizer, 0, wx.ALL, 5)
        MainSizer.Add(FilterSizer, 0, wx.EXPAND | wx.ALL, 5)
        MainSizer.Add(OutputSizer, 4, wx.EXPAND | wx.ALL, 5)
        MainSizer.Add(InputSizer, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(MainSizer)

    def after_enter(self, event):
        values = self.input_tc.GetValue()
        print repr(values)
        for cmd in values.split('\n'):
            if self.session:
                self.session.send_command(cmd)
        self.input_tc.SetValue('')
        event.Skip()

    def on_connect(self, event):
        obj = event.GetEventObject()
        state = obj.GetLabel()
        if state == "Connect":
            port = self.C_ports.GetStringSelection()
            if not port:
                return False
            port = Utility.find_in_string(port_pattern, port)
            try:
                if self.session:
                    self.session.close()
                self.session = Serial.Serial(port=port, baudrate=int(self.C_baudrate.GetStringSelection()))
                Utility.append_work(self.LOG_OUTPUT)
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

    def on_new_window(self, event):
        dialog = SerialDialog(size=(700, 560), name="")
        dialog.Show()

    def on_ok(self, event):
        string = self.filter_tc.GetValue()
        print string
        if "|" in string:
            self.filters = string.split('|')
        else:
            self.filters = [string]
        print self.filters

    def LOG_OUTPUT(self):
        while self.session.is_open():
            line = self.session.read_line()
            if not line:
                continue
            msg = '{time}:{line}\n'.format(time=Utility.get_timestamp(), line=line)
            if self.filters:
                for f in self.filters:
                    if line.startswith(f):
                        wx.CallAfter(self.log_tc.AppendText, msg)
            else:
                wx.CallAfter(self.log_tc.AppendText, msg)


from lib.UserInterface.Dialog import DialogBase


class SerialDialog(DialogBase.DialogBase):
    def __init__(self, size, name="", positon=wx.DefaultPosition):
        DialogBase.DialogBase.__init__(self, name=name, size=size, pos=positon)
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        PortsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.C_ports = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, Serial.get_ports(), 0)
        baudrates = ['115200', '921600']
        self.session = None
        self.filters = list()
        self.C_baudrate = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, baudrates, 0)
        self.C_baudrate.SetSelection(0)
        B_Refresh = wx.Button(self, wx.ID_ANY, u"Refresh", wx.DefaultPosition, (60, 27), 0)
        B_Refresh.Bind(wx.EVT_BUTTON, self.on_refresh)
        B_Connect = wx.Button(self, wx.ID_ANY, u"Connect", wx.DefaultPosition, (-1, 27), 0)
        B_Connect.Bind(wx.EVT_BUTTON, self.on_connect)

        PortsSizer.Add(B_Refresh, 0, wx.ALIGN_CENTER_VERTICAL)
        PortsSizer.Add(self.C_ports, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)
        PortsSizer.Add(self.C_baudrate, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)
        PortsSizer.Add(B_Connect, 0, wx.ALIGN_CENTER_VERTICAL)

        FilterSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.filter_tc = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        B_OK = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, (40, 32), 0)
        B_OK.Bind(wx.EVT_BUTTON, self.on_ok)

        FilterSizer.Add(self.filter_tc, 1, wx.EXPAND)
        FilterSizer.Add(B_OK, 0, wx.ALIGN_CENTER_VERTICAL)
        OutputSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.log_tc = wx.TextCtrl(self, wx.ID_ANY, '',
                                  style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        self.log_tc.SetInsertionPointEnd()
        self.log_tc.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL, False))
        OutputSizer.Add(self.log_tc, 1, wx.EXPAND)
        InputSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.input_tc = wx.TextCtrl(self, wx.ID_ANY, '', style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
        self.input_tc.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL, False))
        self.input_tc.Bind(wx.EVT_TEXT_ENTER, self.after_enter)
        InputSizer.Add(self.input_tc, 1, wx.EXPAND)

        MainSizer.Add(PortsSizer, 0, wx.ALL, 5)
        MainSizer.Add(FilterSizer, 0, wx.EXPAND | wx.ALL, 5)
        MainSizer.Add(OutputSizer, 4, wx.EXPAND | wx.ALL, 5)
        MainSizer.Add(InputSizer, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(MainSizer)

    def on_connect(self, event):
        obj = event.GetEventObject()
        state = obj.GetLabel()
        if state == "Connect":
            port = self.C_ports.GetStringSelection()
            if not port:
                return False
            port = Utility.find_in_string(port_pattern, port)
            try:
                if self.session:
                    self.session.close()
                self.session = Serial.Serial(port=port, baudrate=int(self.C_baudrate.GetStringSelection()))
                Utility.append_work(self.LOG_OUTPUT, thread_name="LOG_OUTPUT: %s" % self.session.get_port())
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

    def on_ok(self, event):
        string = self.filter_tc.GetValue()
        print string
        if "|" in string:
            self.filters = string.split('|')
        else:
            self.filters = [string]
        print self.filters

    def LOG_OUTPUT(self):
        while self.session.is_open():
            line = self.session.read_line()
            if not line:
                continue
            msg = '{time}:{line}\n'.format(time=Utility.get_timestamp(), line=line)
            if self.filters:
                for f in self.filters:
                    if line.startswith(f):
                        wx.CallAfter(self.log_tc.AppendText, msg)
            else:
                wx.CallAfter(self.log_tc.AppendText, msg)
    def after_enter(self, event):
        values = self.input_tc.GetValue()
        print repr(values)
        for cmd in values.split('\n'):
            if self.session:
                self.session.send_command(cmd)
        self.input_tc.SetValue('')
        event.Skip()
