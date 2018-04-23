# -*- encoding:UTF-8 -*-
import wx
from NotebookBase import NotebookBase
from lib import Utility
from wx import CallAfter
import time
from wx import dataview as DV
from lib.ProtocolStack import AirMessage
import re

Logger = Utility.getLogger(__name__)


class OfflineTools(NotebookBase):
    def __init__(self, parent):
        NotebookBase.__init__(self, parent=parent, name="OFFLINE")
        MainSizer = wx.BoxSizer(wx.VERTICAL)

        LogAnalysisSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "LogAnalysis"), wx.VERTICAL)
        PickerSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.log_picker = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, "Select a file",
                                            "Log files (*.log)|*.log|All files (*.*)|*.*", wx.DefaultPosition,
                                            wx.DefaultSize, wx.FLP_DEFAULT_STYLE)
        self.analysis_button = wx.Button(self, wx.ID_ANY, "Analysis", wx.DefaultPosition, wx.DefaultSize, 0)
        self.analysis_button.Bind(wx.EVT_BUTTON, self.__analysis_log)
        PickerSizer.Add(self.log_picker, 1, wx.ALL, 1)
        PickerSizer.Add(self.analysis_button, 0, wx.ALL, 1)

        self.DVLC = DV.DataViewListCtrl(self, wx.ID_ANY)
        self.DVLC.AppendTextColumn(u"时间")
        self.DVLC.AppendTextColumn(u"优先级")
        self.DVLC.AppendTextColumn(u"消息名")
        self.DVLC.AppendTextColumn(u"消息源")
        self.DVLC.AppendTextColumn(u"目标源")
        self.DVLC.AppendProgressColumn(u"信号")
        LogAnalysisSizer.Add(PickerSizer, 0, wx.EXPAND)
        LogAnalysisSizer.Add(self.DVLC, 1, wx.EXPAND | wx.ALL, 1)
        MainSizer.Add(LogAnalysisSizer, 1, wx.EXPAND, 5)
        self.SetSizer(MainSizer)

    def __analysis_log(self, event):
        def analysis(log_file):

            with open(log_file) as mLog:
                lines = mLog.readlines()
            split_logs = self.__split_log(lines, [AirMessage.trace_pattern])
            for log in split_logs:
                first = lines[log[0]]
                data = [first[1], first[2], first[3], first[4], first[5], first[6]]
                CallAfter(self.DVLC.AppendItem, data)

            self.analysis_button.Enable()


        self.analysis_button.Disable()
        log_file = self.log_picker.GetPath()
        if Utility.exists(log_file):
            Utility.append_work(target=analysis, log_file=log_file)
        else:
            Logger.warn('\"%s\" does not exist.' % log_file)
            self.analysis_button.Enable()

    @staticmethod
    def __split_log(lines, patterns):
        def find_end(s_number, e_pattern):
            for current_number in xrange(s_number, length):
                line = lines[current_number]
                if re.search(e_pattern, line):
                    return s_number, current_number
            return s_number, None

        def find_log(s_number):
            for current_number in xrange(s_number, length):
                line = lines[current_number]
                for s_pattern, e_pattern in patterns:
                    if re.search(s_pattern, line):
                        return find_end(s_number=current_number, e_pattern=e_pattern)
            return None, None

        length = len(lines)
        logs = list()
        line_number = 0
        while line_number < length:
            start_line, end_line = find_log(line_number)
            if not start_line or not end_line:
                break
            line_number = end_line + 1
            logs.append((start_line, end_line))
        return logs


class Log(object):
    def __init__(self, path):
        with open(path) as mLog:
            lines = mLog.readlines()

    def __iter__(self):
        return self

    def next(self):
        if self.n < self.max:
            r = self.b
            self.a, self.b = self.b, self.a + self.b
            self.n = self.n + 1
            return r
        raise StopIteration()
