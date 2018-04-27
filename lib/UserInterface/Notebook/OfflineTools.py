# -*- encoding:UTF-8 -*-
import wx
from NotebookBase import NotebookBase
from lib import Utility
from wx import CallAfter
import time
from wx.lib.splitter import MultiSplitterWindow
from ObjectListView import ObjectListView, ColumnDefn
from lib.ProtocolStack import AirMessage
import re
from lib.UserInterface.Dialog import AirMessageDialog
from os import system

Logger = Utility.getLogger(__name__)


class OfflineTools(NotebookBase):
    def __init__(self, parent):
        NotebookBase.__init__(self, parent=parent, name="OFFLINE")
        self.__log_data = dict()
        self.__line_mapping_file = dict()
        self.__log_count = 0

        MainSizer = wx.BoxSizer(wx.VERTICAL)

        LogAnalysisSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "LogAnalysis"), wx.VERTICAL)
        PickerSizer = wx.BoxSizer(wx.HORIZONTAL)
        ButtonSizer = wx.BoxSizer(wx.VERTICAL)
        SplitterSizer = wx.BoxSizer(wx.VERTICAL)

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

        SplitterWindow = MultiSplitterWindow(parent=self, style=wx.SP_LIVE_UPDATE)
        SplitterWindow.SetOrientation(wx.VERTICAL)

        SplitterPanel1 = wx.Panel(parent=SplitterWindow)

        self.OLV = ObjectListView(SplitterPanel1, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        self.OLV.Bind(wx.EVT_CONTEXT_MENU, self.on_right_click)
        self.DM = DataModule(ListView=self.OLV)
        ListViewSizer = wx.BoxSizer(wx.VERTICAL)
        ListViewSizer.Add(self.OLV, 1, wx.EXPAND)
        SplitterPanel1.SetSizer(ListViewSizer)

        SplitterPanel2 = wx.Panel(parent=SplitterWindow)
        SplitterPanel2.SetBackgroundColour('#999983')

        SplitterWindow.AppendWindow(SplitterPanel1)
        SplitterWindow.AppendWindow(SplitterPanel2)
        LogAnalysisSizer.Add(PickerSizer, 0, wx.EXPAND)
        # SplitterSizer.Add(SplitterWindow, wx.SizerFlags().Expand().Proportion(1).Border(wx.ALL, 5))
        SplitterSizer.Add(SplitterWindow, 1, wx.EXPAND)
        MainSizer.Add(LogAnalysisSizer, 0, wx.EXPAND, 5)
        MainSizer.Add(SplitterSizer, 1, wx.EXPAND, 5)

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
        self.analysis_button.Disable()
        log_files = self.log_list_box.Items
        Utility.append_work(target=self.DM.Analysis, files=log_files)

        #
        # def analysis(files):
        #     print time.time()
        #     for row, log in self.yield_log(files, [AirMessage.trace_patterns, AirMessage.e2e_patterns,
        #                                            AirMessage.NPR_patterns]):
        #         self.__insert_log_data(log=log, row=row)
        #     self.analysis_button.Enable()
        #     print time.time()
        #
        # self.analysis_button.Disable()
        # log_files = self.log_list_box.Items
        # self.__clear_log_data()

    def double_click_on_logfile_item(self, event):
        self.log_list_box.Delete(self.log_list_box.GetSelection())

    def double_click_on_filter_item(self, event):
        row = self.DVLC.GetSelectedRow()
        dialog = AirMessageDialog(self.__log_data.get(row))
        dialog.Show()

    def on_right_click(self, event):
        if self.OLV.GetSelectedObject():
            menu = wx.Menu()
            menu.Append(500, '在文件中打开')
            self.Bind(wx.EVT_MENU, self.__open_in_file, id=500)
            self.PopupMenu(menu)
            menu.Destroy()

    def __open_in_file(self, event):
        line_number = self.OLV.GetSelectedObject()
        print line_number
        print line_number._id

        def find_in_file(number):
            keys = self.__line_mapping_file.keys()
            keys.sort(reverse=True)
            number = int(number)
            for key in keys:
                if number > key:
                    return number - key, self.__line_mapping_file.get(key)

        line_number, log_file = find_in_file(line_number)
        cmd = 'cmd /c start {0} -n{1} {2}'.format(Utility.Path.EXE_NOTEPAD, line_number, log_file)
        system(cmd)

    def __insert_log_data(self, row, log):
        def convert_data():
            d = ['' for x in range(10)]
            d[0] = self.__log_count + 1  # 第一位是log序号
            d[1] = row  # 第二位log出现的行号
            name, src, dest, _type = self.parse_log(log=log)
            d[2] = name  # 消息名
            d[3] = src  # 源
            d[4] = dest  # 目标
            d[5] = _type  # 类型
            return d[:self.DVLC.GetColumnCount()]

        data = convert_data()
        self.__log_data[self.__log_count] = (data, log)
        self.__log_count += 1
        CallAfter(self.DVLC.AppendItem, data)

    def __clear_log_data(self):
        self.__line_mapping_file.clear()
        self.__log_data.clear()
        self.__log_count = 0
        self.DVLC.DeleteAllItems()

    def yield_line(self, files):
        counter = [0]
        for file in files:
            self.__line_mapping_file[counter[0]] = file
            with open(file) as mfile:
                for line in mfile:
                    counter[0] = counter[0] + 1
                    yield counter[0], line

    def yield_log(self, file_paths, patterns):
        def find_start(line_num, line):
            for s_pattern, e_pattern in patterns:
                if re.search(s_pattern, line):
                    log_block = list()
                    start_row = line_num
                    log_block.append(line)
                    if re.search(e_pattern, line) or find_end(pattern=e_pattern, block=log_block):
                        return start_row, log_block
            return None, None

        def find_end(pattern, block):
            for line_number, line in mLog:
                block.append(line)
                if re.search(pattern, line):
                    return True
            return False

        mLog = self.yield_line(files=file_paths)
        for line_number, line in mLog:
            row, block = find_start(line_num=line_number, line=line)
            if row and block:
                yield row, block

    def parse_log(self, log):
        def case_npr_msg():
            name = src = dest = _type = ''
            name = Utility.find_in_string(pattern=AirMessage.NPR_begin_pattern, string=start_line)
            return name, src, dest, _type

        def case_e2e_msg():
            name = src = dest = _type = ''
            # name = 'e2e msg header information'
            for line in log:
                if 'dest_id      = ' in line:
                    dest = Utility.find_in_string(pattern=AirMessage.dest_pattern, string=line)
                elif 'src_id       =' in line:
                    src = Utility.find_in_string(pattern=AirMessage.src_pattern, string=line)
            _type = 'e2e'
            return name, src, dest, _type

        def case_air_msg():
            name = src = dest = _type = ''
            name = re.findall(AirMessage.trace_patterns[0], start_line)[0]
            _type = 'air message'
            return name, src, dest, _type

        start_line = log[0]
        if 'Print e2e msg header information start' in start_line:
            return case_e2e_msg()
        elif ' air message begin' in start_line:
            return case_air_msg()
        elif 'recv stack_primitive' in start_line:
            return case_npr_msg()

        else:
            Logger.error('=' * 50)
            Logger.error('Unknow type.Please check.')
            for line in log:
                Logger.error(repr(line))
            Logger.error('=' * 50)


class DataModule(object):
    class Message(object):
        def __init__(self, log):
            self._id = Utility.randint(30, 100)
            self._msg = Utility.randstr()
            self._src = str(Utility.randint(0, 10))
            self._dest = Utility.randint(10, 20)

    def __init__(self, ListView):
        self.list_view = ListView
        self.__set_columns()
        self.list_view.rowFormatter = self.__set_row_formatter

    def Analysis(self, files):
        for x in range(100):
            self.list_view.AddObject(self.Message(log=files))

    def Append(self, log):
        pass

    def __set_columns(self):
        self.list_view.SetColumns(
            [
                ColumnDefn(title=u"No.", align="left", width=80, valueGetter='_no'),
                ColumnDefn(title=u"Time", align="left", width=80, valueGetter='_time'),
                ColumnDefn(title=u"Protocol", align="left", width=200, valueGetter='_prot'),
                ColumnDefn(title=u"Source", align="center", width=80, valueGetter="_src"),
                ColumnDefn(title=u"Dest.", align="center", width=80, valueGetter="_dest"),
                ColumnDefn(title=u"Info", align="left", width=80, valueGetter="_info"),
                # ColumnDefn("Mfg", "left", 180, "_dest")
            ]
        )

    @staticmethod
    def __set_row_formatter(list_view, item):

        if item._dest > 15:
            list_view.SetBackgroundColour(wx.Colour('#FFB90F'))
