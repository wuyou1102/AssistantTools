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
        self.__file_mapping_line = dict()
        self.__log_count = 0

        MainSizer = wx.BoxSizer(wx.VERTICAL)

        LogAnalysisSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "LogAnalysis"), wx.VERTICAL)
        PickerSizer = wx.BoxSizer(wx.HORIZONTAL)
        ButtonSizer = wx.BoxSizer(wx.VERTICAL)
        self.log_list_box = wx.ListBox(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                                       style=wx.LB_NEEDED_SB | wx.LB_SINGLE)
        self.log_list_box.Bind(wx.EVT_LISTBOX_DCLICK, self.double_click_on_logfile_item)
        self.browse_button = wx.Button(self, wx.ID_ANY, "Browse", wx.DefaultPosition, wx.DefaultSize, 0)
        self.browse_button.Bind(wx.EVT_BUTTON, self.__browse_log)
        self.clear_button = wx.Button(self, wx.ID_ANY, "Clear", wx.DefaultPosition, wx.DefaultSize, 0)
        self.analysis_button = wx.Button(self, wx.ID_ANY, "Analysis", wx.DefaultPosition, wx.DefaultSize, 0)
        self.analysis_button.Bind(wx.EVT_BUTTON, self.__analysis_log)

        ButtonSizer.Add(self.browse_button, 0, wx.ALL, 1)
        ButtonSizer.Add(self.analysis_button, 0, wx.ALL, 1)
        ButtonSizer.Add(self.clear_button, 0, wx.ALL, 1)

        PickerSizer.Add(self.log_list_box, 2, wx.EXPAND | wx.ALL, 1)
        PickerSizer.Add(ButtonSizer, 1, wx.ALL, 1)
        self.DVLC = DV.DataViewListCtrl(self, wx.ID_ANY)

        self.DVLC.Bind(DV.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.on_right_click)
        self.DVLC.Bind(DV.EVT_DATAVIEW_ITEM_ACTIVATED, self.double_click_on_filter_item)

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

    def __browse_log(self, event):
        dlg = wx.FileDialog(self,
                            message="Select logs",
                            wildcard="Log files (*.log)|*.log|All files (*.*)|*.*",
                            defaultDir="",
                            style=wx.FD_MULTIPLE
                            )
        if dlg.ShowModal() == wx.ID_OK:
            for log_path in dlg.GetPaths():
                if log_path not in self.log_list_box.Items:
                    try:
                        Utility.convert_timestamp(str=Utility.basename(log_path), time_fmt='%Y_%m_%d-%H_%M_%S.log')
                        self.log_list_box.Append(log_path)
                    except ValueError:
                        Logger.error("\"{0}\" is not a validated log name. Please check.".format(log_path))
                        msg_dlg = wx.MessageDialog(self, u"\"{0}\"\n不符合规范，请手动确认文件并修改文件名后再添加。".format(
                            log_path), u"   文件名错误", wx.OK | wx.ICON_ERROR)
                        if msg_dlg.ShowModal() == wx.ID_OK:
                            msg_dlg.Destroy()
        dlg.Destroy()

    def __analysis_log(self, event):
        def analysis(files):
            def parse(block):
                first_line = block[0]
                name = re.findall(AirMessage.trace_pattern[0], first_line)[0]
                return name, name, name, name, name, name

            print time.time()
            for log in self.yield_log(files, [AirMessage.trace_pattern, AirMessage.tdace_pattern]):
                self.__insert_log_data(data=log)
                data = [self.__log_count, log[0], 3, 4, 5, 6]
                CallAfter(self.DVLC.AppendItem, data)
            self.analysis_button.Enable()
            print time.time()

        self.analysis_button.Disable()
        log_files = self.log_list_box.Items
        self.__clear_log_data()
        Utility.append_work(target=analysis, files=log_files)

    def double_click_on_logfile_item(self, event):
        self.log_list_box.Delete(self.log_list_box.GetSelection())

    def double_click_on_filter_item(self, event):
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
        self.__file_mapping_line.clear()
        self.__log_data.clear()
        self.__log_count = 0
        self.DVLC.DeleteAllItems()

    def yield_line(self, files):
        counter = [0]
        for file in files:
            self.__file_mapping_line[file] = counter[0]
            print self.__file_mapping_line
            with open(file) as mfile:
                for line in mfile:
                    counter[0] = counter[0] + 1
                    yield counter[0], line

    def yield_log(self, file_paths, patterns):
        def find_start(line_num, line):
            for s_pattern, e_pattern in patterns:
                if re.search(s_pattern, line):
                    log_block = list()
                    log_block.append(line_num)
                    log_block.append(line)
                    if re.search(e_pattern, line) or find_end(pattern=e_pattern, block=log_block):
                        return log_block
            return None

        def find_end(pattern, block):
            for line_number, line in mLog:
                block.append(line)
                if re.search(pattern, line):
                    return True
            return False

        mLog = self.yield_line(files=file_paths)

        for line_number, line in mLog:
            block = find_start(line_num=line_number, line=line)
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
