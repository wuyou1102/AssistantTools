# -*- encoding:UTF-8 -*-
import wx
from NotebookBase import NotebookBase
from lib import Utility
from wx import CallAfter
import OfflineLibs
from wx.lib.splitter import MultiSplitterWindow
from ObjectListView import ObjectListView, ColumnDefn, Filter
import re
from lib.UserInterface.Dialog import Offline
from os import system

Logger = Utility.getLogger(__name__)


class OfflineLogParse(NotebookBase):
    def __init__(self, parent):
        NotebookBase.__init__(self, parent=parent, name="OFFLINE")
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
        self.clear_button.Bind(wx.EVT_BUTTON, self.__clear_log)
        self.config_button = wx.Button(self, wx.ID_ANY, "Config", wx.DefaultPosition, wx.DefaultSize, 0)
        self.config_button.Bind(wx.EVT_BUTTON, self.__on_config)
        self.analysis_button = wx.Button(self, wx.ID_ANY, "Analysis", wx.DefaultPosition, wx.DefaultSize, 0)
        self.analysis_button.Bind(wx.EVT_BUTTON, self.__analysis_log)

        ButtonSizer.Add(self.browse_button, 0, wx.ALL, 1)
        ButtonSizer.Add(self.analysis_button, 0, wx.ALL, 1)
        ButtonSizer.Add(self.clear_button, 0, wx.ALL, 1)
        ButtonSizer.Add(self.config_button, 0, wx.ALL, 1)

        CheckSizer = wx.BoxSizer(wx.VERTICAL)
        self.NPR_checkbox = wx.CheckBox(self, wx.ID_ANY, u"层间原语", wx.DefaultPosition, wx.DefaultSize, 0)
        self.AIR_checkbox = wx.CheckBox(self, wx.ID_ANY, u"空口消息", wx.DefaultPosition, wx.DefaultSize, 0)
        self.NPR_checkbox.SetValue(True)
        self.AIR_checkbox.SetValue(True)
        self.NPR_checkbox.Bind(wx.EVT_CHECKBOX, self.__filter)
        self.AIR_checkbox.Bind(wx.EVT_CHECKBOX, self.__filter)
        CheckSizer.Add(self.NPR_checkbox, 0, wx.ALL, 5)
        CheckSizer.Add(self.AIR_checkbox, 0, wx.ALL, 5)

        PickerSizer.Add(self.log_list_box, 2, wx.EXPAND | wx.ALL, 1)
        PickerSizer.Add(ButtonSizer, 0, wx.ALL, 1)
        PickerSizer.Add(CheckSizer, 0, wx.ALL, 1)

        SplitterWindow = MultiSplitterWindow(parent=self, style=wx.SP_LIVE_UPDATE | wx.SP_HORIZONTAL)
        SplitterWindow.SetOrientation(wx.VERTICAL)

        SplitterPanel1 = wx.Panel(parent=SplitterWindow)
        self.OLV = ObjectListView(SplitterPanel1, wx.ID_ANY,
                                  style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        self.OLV.Bind(wx.EVT_CONTEXT_MENU, self.on_right_click)
        self.OLV.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)
        self.OLV.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.double_click_on_item)

        ListViewSizer = wx.BoxSizer(wx.VERTICAL)
        ListViewSizer.Add(self.OLV, 1, wx.EXPAND)
        SplitterPanel1.SetSizer(ListViewSizer)

        SplitterPanel2 = wx.Panel(parent=SplitterWindow)
        TextCtrlSizer = wx.BoxSizer(wx.VERTICAL)
        self.text_ctrl = wx.TextCtrl(SplitterPanel2, -1, value="", style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        TextCtrlSizer.Add(self.text_ctrl, 1, wx.EXPAND)
        SplitterPanel2.SetSizer(TextCtrlSizer)

        SplitterWindow.AppendWindow(SplitterPanel1)
        SplitterWindow.AppendWindow(SplitterPanel2)
        LogAnalysisSizer.Add(PickerSizer, 0, wx.EXPAND)
        # SplitterSizer.Add(SplitterWindow, wx.SizerFlags().Expand().Proportion(1).Border(wx.ALL, 5))
        SplitterSizer.Add(SplitterWindow, 1, wx.EXPAND)
        MainSizer.Add(LogAnalysisSizer, 0, wx.EXPAND, 5)
        MainSizer.Add(SplitterSizer, 1, wx.EXPAND, 5)

        self.SetSizer(MainSizer)

    def __filter(self, event):
        _type_list = ["e2eMessage"]
        self.OLV.SetFilter(Filter.Chain())
        if self.NPR_checkbox.IsChecked():
            _type_list.append("NprMessage")
        if self.AIR_checkbox.IsChecked():
            _type_list.append("AirMessage")
        _filter = Filter.Chain(Filter.Predicate(lambda item: item._type in _type_list))
        self.OLV.SetFilter(Filter.Chain(_filter))
        self.OLV.RepopulateList()

    def __clear_log(self, event):
        self.log_list_box.Clear()

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
        self.OLV.DeleteAllItems()
        self.DM = DataModule(ListView=self.OLV, LogFiles=self.log_list_box.Items, Button=self.analysis_button)
        self.DM.Analysis()

    def __on_config(self, event):
        dialog = Offline.LogDialog()
        dialog.ShowModal()

    def double_click_on_logfile_item(self, event):
        self.log_list_box.Delete(self.log_list_box.GetSelection())

    def double_click_on_item(self, event):
        dialog = Offline.LogDialog(obj=self.OLV.GetSelectedObject(), line_mapping_file=self.DM.get_line_mapping())
        dialog.ShowModal()

    def on_right_click(self, event):
        if self.OLV.GetSelectedObject():
            menu = wx.Menu()
            menu.Append(500, '在文件中打开')
            self.Bind(wx.EVT_MENU, self.__open_in_file, id=500)
            self.PopupMenu(menu)
            menu.Destroy()

    def on_item_selected(self, event):
        obj = self.OLV.GetSelectedObject()
        self.text_ctrl.SetValue("")
        for line in obj._block:
            try:
                wx.CallAfter(self.text_ctrl.AppendText, text=line.strip('\r\n') + '\n')
            except Exception:
                print repr(line)

    def __open_in_file(self, event):
        obj = self.OLV.GetSelectedObject()
        self.DM.open_in_file(obj)


class DataModule(object):
    def __init__(self, ListView, LogFiles, Button):
        self.__log_files = self.__sorted_files(LogFiles)  # 通过文件名排序 不在乎路径是地址
        self.__list_view = ListView
        self.__button = Button
        self.__coarse_strings = ['smac-stack-sap.h', 'asc_proc_func_def.c', 'ntx_proc_func_def.c']
        self.__set_columns()
        self.__list_view.rowFormatter = self.__set_row_formatter
        self.__data = []
        self.__line_mapping_file = dict()
        self.__patterns = [OfflineLibs.trace_patterns, OfflineLibs.e2e_patterns, OfflineLibs.NPR_patterns]
        self.__buff = []
        self.__log_count = 0

    def get_line_mapping(self):
        return self.__line_mapping_file

    def __sorted_files(self, files):
        return sorted(files, key=lambda x: Utility.convert_timestamp(str=Utility.basename(x),
                                                                     time_fmt='%Y_%m_%d-%H_%M_%S.log'))

    def __analysis(self):
        print Utility.get_timestamp()
        self.__button.Disable()
        for line_number, block in self.yield_log(self.__log_files, self.__patterns):
            self.Append(line_nubmer=line_number, block=block)
        self.__button.Enable()
        print Utility.get_timestamp()

    def Analysis(self):
        Utility.append_work(target=self.__analysis)

    def Append(self, line_nubmer, block):
        self.__log_count += 1
        first_line = block[0]
        if ' NPR proc recv stack_primitive ' in first_line:
            npr = OfflineLibs.NprMessage(_no=self.__log_count, block=block, line=line_nubmer)
            self.__check_last_msg()
            self.__data.append(npr)
            CallAfter(self.__list_view.AddObject, npr)
        elif 'Print e2e msg header information start' in first_line:
            e2e = OfflineLibs.e2eMessage(_no=self.__log_count, block=block, line=line_nubmer)
            self.__data.append(e2e)
            # CallAfter(self.__list_view.AddObject, e2e)
        elif 'air message begin ' in first_line:
            air = OfflineLibs.AirMessage(_no=self.__log_count, block=block, line=line_nubmer)
            self.__merge_air_and_e2e(air=air)
            self.__data.append(air)
            CallAfter(self.__list_view.AddObject, air)

    def __merge_air_and_e2e(self, air):
        last_msg = self.__data[-1]
        if type(last_msg) == OfflineLibs.e2eMessage:
            if air.merge(last_msg):
                self.__data.pop(-1)
                self.__merge_air_and_e2e(air)
                return
            else:
                CallAfter(self.__list_view.AddObject, last_msg)
                return
        return

    def __check_last_msg(self):
        if not self.__data:
            return
        last_msg = self.__data[-1]
        if type(last_msg) == OfflineLibs.e2eMessage:
            CallAfter(self.__list_view.AddObject, last_msg)

    def __set_columns(self):
        self.__list_view.SetColumns(
            [
                ColumnDefn(title=u"No.", align="left", width=80, valueGetter='_no', checkStateSetter=True),
                ColumnDefn(title=u"Time", align="left", width=80, valueGetter='_time'),
                ColumnDefn(title=u"Protocol", align="left", width=200, valueGetter='_prot'),
                ColumnDefn(title=u"Source", align="center", width=80, valueGetter="_src"),
                ColumnDefn(title=u"Dest.", align="center", width=80, valueGetter="_dest"),
                ColumnDefn(title=u"Info", align="left", width=80, valueGetter="_info"),
            ]
        )

    @staticmethod
    def __set_row_formatter(list_view, item):
        # 优先级高的需要写在前面
        from OfflineLibs import Colour
        if item._type == 'e2eMessage':
            list_view.SetBackgroundColour(wx.RED)
        elif item._prot == "S_SMAC_BR":
            list_view.SetBackgroundColour(Colour.Orange)
        elif item._type == 'AirMessage':
            list_view.SetBackgroundColour(Colour.LightCyan)
        elif item._type == 'NprMessage':
            list_view.SetBackgroundColour(Colour.White)
        else:
            list_view.SetBackgroundColour(Colour.White)

    def yield_line(self, files):
        counter = 0
        for file in files:
            self.__line_mapping_file[counter] = file
            with open(file) as mfile:
                for line in mfile:
                    counter += 1
                    yield counter, line

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
            counter = 0
            for line_number, line in mLog:
                if counter >= 400:
                    break
                counter += 1
                block.append(line)
                if re.search(pattern, line):
                    return True
            return False

        mLog = self.yield_line(files=file_paths)
        for line_number, line in mLog:
            if self.__coarse_filtration(line=line):
                continue
            row, block = find_start(line_num=line_number, line=line)
            if row and block:
                yield row, block

    def __coarse_filtration(self, line):
        for string in self.__coarse_strings:
            if string in line:
                return True
        return False

    def open_in_file(self, obj):
        def find_in_file(number):
            keys = self.__line_mapping_file.keys()
            keys.sort(reverse=True)
            number = int(number)
            for key in keys:
                if number > key:
                    return number - key, self.__line_mapping_file.get(key)

        line_number, log_file = find_in_file(obj._line)
        cmd = 'cmd /c start {0} -n{1} {2}'.format(Utility.Path.EXE_NOTEPAD, line_number, log_file)
        system(cmd)
