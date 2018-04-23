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
        self.DVLC.AppendTextColumn(u"信号")
        LogAnalysisSizer.Add(PickerSizer, 0, wx.EXPAND)
        LogAnalysisSizer.Add(self.DVLC, 1, wx.EXPAND | wx.ALL, 1)
        MainSizer.Add(LogAnalysisSizer, 1, wx.EXPAND, 5)
        self.SetSizer(MainSizer)

    def __analysis_log(self, event):
        print time.time()

        def analysis(log_file):
            def parse(block):
                first_line = block[0]
                name = re.findall(AirMessage.trace_pattern[0], first_line)[0]
                return name,name,name,name,name,name

            for log in self.__yield_log(log_file, [AirMessage.trace_pattern]):
                data = parse(log)
                # data = [count, log[2], log[3], log[4], log[5], log[6]]
                CallAfter(self.DVLC.AppendItem, data)
            self.analysis_button.Enable()
            print time.time()

        self.analysis_button.Disable()
        log_file = self.log_picker.GetPath()
        if Utility.exists(log_file):
            Utility.append_work(target=analysis, log_file=log_file)
        else:
            Logger.warn('\"%s\" does not exist.' % log_file)
            self.analysis_button.Enable()

    @staticmethod
    def __yield_log(path, patterns):
        def find_start(line):
            for s_pattern, e_pattern in patterns:
                if re.search(s_pattern, line):
                    log_block = list()
                    log_block.append(line)
                    if find_end(e_pattern, log_block):
                        return log_block
            return None

        def find_end(pattern, block):
            for line in mLog:
                block.append(line)
                if re.search(pattern, line):
                    return True
            return False

        with open(path) as mLog:
            for line in mLog:
                block = find_start(line=line)
                if block:
                    yield block


class Log(object):
    def __init__(self, path, patterns):
        with open(path) as mLog:
            self.__lines = mLog.readlines()
        self.__length = len(self.__lines)
        self.__patterns = patterns
        self.__current_number = 0

    def __iter__(self):
        return self

    def __find_end(self, s_number, e_pattern):
        for current_number in xrange(s_number, self.__length):
            line = self.__lines[current_number]
            if re.search(e_pattern, line):
                return s_number, current_number
        return s_number, None

    def __find_log(self, s_number):
        for current_number in xrange(s_number, self.__length):
            line = self.__lines[current_number]
            for s_pattern, e_pattern in self.__patterns:
                if re.search(s_pattern, line):
                    return self.__find_end(s_number=current_number, e_pattern=e_pattern)
        return None, None

    def next(self):
        if self.__current_number < self.__length:
            start_line, end_line = self.__find_log(self.__current_number)
            if not start_line or not end_line:
                raise StopIteration()
            self.__current_number = end_line + 1
            return self.__lines[start_line:end_line]
        raise StopIteration()
