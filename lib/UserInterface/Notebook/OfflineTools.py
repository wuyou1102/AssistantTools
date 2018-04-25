# -*- encoding:UTF-8 -*-
import wx
from NotebookBase import NotebookBase
from lib import Utility
from wx import CallAfter
import time
from wx import dataview as DV
from lib.ProtocolStack import AirMessage
import re
from lib.UserInterface.Dialog import AirMessageDialog

Logger = Utility.getLogger(__name__)


class OfflineTools(NotebookBase):
    def __init__(self, parent):
        NotebookBase.__init__(self, parent=parent, name="OFFLINE")
        self.__log_data = dict()
        self.__log_count = 0

        MainSizer = wx.BoxSizer(wx.VERTICAL)

        LogAnalysisSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "LogAnalysis"), wx.VERTICAL)
        PickerSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.log_picker = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, "Select a file",
                                            "Log files (*.log)|*.log|All files (*.*)|*.*", wx.DefaultPosition,
                                            wx.DefaultSize, wx.FLP_DEFAULT_STYLE)
        self.log_picker.SetPath("C:\Users\dell\Desktop\Serial-COM9111617serial-com9.log")
        self.analysis_button = wx.Button(self, wx.ID_ANY, "Analysis", wx.DefaultPosition, wx.DefaultSize, 0)
        self.analysis_button.Bind(wx.EVT_BUTTON, self.__analysis_log)
        PickerSizer.Add(self.log_picker, 1, wx.ALL, 1)
        PickerSizer.Add(self.analysis_button, 0, wx.ALL, 1)

        self.DVLC = DV.DataViewListCtrl(self, wx.ID_ANY)

        self.DVLC.Bind(DV.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.on_right_click)
        self.DVLC.Bind(DV.EVT_DATAVIEW_ITEM_ACTIVATED, self.on_double_click)
        DV.DATAVIEW_CELL_INERT
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
        def analysis(log_file):
            def parse(block):
                first_line = block[0]
                name = re.findall(AirMessage.trace_pattern[0], first_line)[0]
                return name, name, name, name, name, name

            print time.time()

            for log in self.__yield_log(log_file, [AirMessage.trace_pattern, AirMessage.tdace_pattern]):
                self.__insert_log_data(data=log)
                data = [self.__log_count, log[0], 3, 4, 5, 6]
                CallAfter(self.DVLC.AppendItem, data)
            self.analysis_button.Enable()
            print time.time()

        self.analysis_button.Disable()
        log_file = self.log_picker.GetPath()
        if Utility.exists(log_file):
            self.__clear_log_data()
            Utility.append_work(target=analysis, log_file=log_file)
        else:
            Logger.warn('\"%s\" does not exist.' % log_file)
            self.analysis_button.Enable()

    def on_double_click(self, event):
        row = self.DVLC.GetSelectedRow()
        dialog = AirMessageDialog(self.__log_data.get(row))
        dialog.Show()

    def on_right_click(self, event):
        menu = wx.Menu()
        menu.Append(1, 'Detail')
        self.PopupMenu(menu)
        menu.Destroy()

    def __insert_log_data(self, data):
        self.__log_data[self.__log_count] = data
        self.__log_count += 1

    def __clear_log_data(self):
        print self.__log_data
        self.__log_data.clear()
        self.__log_count = 0
        print self.__log_data
        self.DVLC.DeleteAllItems()

    @staticmethod
    def __yield_log(path, patterns):
        def find_start(line):
            for s_pattern, e_pattern in patterns:
                if re.search(s_pattern, line):
                    print counter[0]
                    log_block = list()
                    log_block.append(line)
                    if re.search(e_pattern, line) or find_end(pattern=e_pattern, block=log_block):
                        return log_block
            return None

        def find_end(pattern, block):
            for line in mLog:
                counter[0] = counter[0] + 1
                block.append(line)
                if re.search(pattern, line):
                    print counter[0]
                    return True
            return False

        counter = [0]
        with open(path) as mLog:
            for line in mLog:
                counter[0] = counter[0] + 1
                block = find_start(line=line)
                if block:
                    yield block

# class Log(object):
#     def __init__(self, path, patterns):
#         with open(path) as mLog:
#             self.__lines = mLog.readlines()
#         self.__length = len(self.__lines)
#         self.__patterns = patterns
#         self.__current_number = 0
#
#     def __iter__(self):
#         return self
#
#     def __find_end(self, s_number, e_pattern):
#         for current_number in xrange(s_number, self.__length):
#             line = self.__lines[current_number]
#             if re.search(e_pattern, line):
#                 return s_number, current_number
#         return s_number, None
#
#     def __find_log(self, s_number):
#         for current_number in xrange(s_number, self.__length):
#             line = self.__lines[current_number]
#             for s_pattern, e_pattern in self.__patterns:
#                 if re.search(s_pattern, line):
#                     return self.__find_end(s_number=current_number, e_pattern=e_pattern)
#         return None, None
#
#     def next(self):
#         if self.__current_number < self.__length:
#             start_line, end_line = self.__find_log(self.__current_number)
#             if not start_line or not end_line:
#                 raise StopIteration()
#             self.__current_number = end_line + 1
#             return self.__lines[start_line:end_line]
#         raise StopIteration()
#
