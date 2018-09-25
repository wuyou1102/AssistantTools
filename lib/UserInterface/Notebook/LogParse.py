# -*- encoding:UTF-8 -*-
import wx
from NotebookBase import NotebookBase
from lib import Utility
from wx import CallAfter
from lib.UserInterface import libs
from wx.lib.splitter import MultiSplitterWindow
from ObjectListView import ObjectListView, ColumnDefn, Filter
import re
from lib.Instrument import Serial
from serial import SerialException

Logger = Utility.getLogger(__name__)


class LogParse(NotebookBase):
    def __init__(self, parent):
        NotebookBase.__init__(self, parent=parent, name="在线日志分析")
        self.serial = None
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        source_sizer = self.__init_source_sizer()
        filter_sizer = self.__init_filter_sizer()
        splitter_sizer = self.__init_splitter_sizer()
        TopSizer = wx.BoxSizer(wx.HORIZONTAL)
        TopSizer.Add(source_sizer, 1, wx.EXPAND | wx.ALL, 5)
        TopSizer.Add(filter_sizer, 0, wx.EXPAND | wx.ALL, 5)
        MainSizer.Add(TopSizer, 0, wx.EXPAND | wx.ALL, 0)
        MainSizer.Add(splitter_sizer, 1, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(MainSizer)

    def __init_source_sizer(self):
        sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"串口"), wx.VERTICAL)
        # from_file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        from_serial_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # file_title = wx.StaticText(self, wx.ID_ANY, u"日志:", wx.DefaultPosition, wx.DefaultSize, 0)
        # serial_title = wx.StaticText(self, wx.ID_ANY, u"串口:", wx.DefaultPosition, wx.DefaultSize, 0)
        # self.fpc = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"选择日志文件", u"*.log", wx.DefaultPosition,
        #                              wx.DefaultSize, wx.FLP_DEFAULT_STYLE | wx.FLP_SMALL)
        self.serial_port = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, Serial.get_ports(), 0)
        button_size = (40, 26)
        self.connect = wx.Button(self, wx.ID_ANY, u"连接", wx.DefaultPosition, button_size, 0)
        self.disconnect = wx.Button(self, wx.ID_ANY, u"断开", wx.DefaultPosition, button_size, 0)
        refresh = wx.Button(self, wx.ID_ANY, u"刷新", wx.DefaultPosition, button_size, 0)
        refresh.Bind(wx.EVT_BUTTON, self.on_refresh)
        self.connect.Bind(wx.EVT_BUTTON, self.on_connect)
        self.disconnect.Bind(wx.EVT_BUTTON, self.on_disconnect)
        # from_file_sizer.Add(file_title, 0, wx.ALIGN_CENTER | wx.ALL, 1)
        # from_file_sizer.Add(self.fpc, 1, wx.EXPAND | wx.ALL, 1)
        # from_serial_sizer.Add(serial_title, 0, wx.ALIGN_CENTER | wx.ALL, 1)
        from_serial_sizer.Add(refresh, 0, wx.ALL, 1)
        from_serial_sizer.Add(self.serial_port, 1, wx.EXPAND | wx.ALL, 1)

        from_serial_sizer.Add(self.connect, 0, wx.ALL, 1)
        from_serial_sizer.Add(self.disconnect, 0, wx.ALL, 1)

        # sizer.Add(from_file_sizer, 1, wx.EXPAND | wx.ALL, 0)
        sizer.Add(from_serial_sizer, 1, wx.EXPAND | wx.ALL, 0)
        return sizer

    def __init_filter_sizer(self):
        sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "筛选"), wx.HORIZONTAL)
        self.NPR_checkbox = wx.CheckBox(self, wx.ID_ANY, u"层间原语", wx.DefaultPosition, wx.DefaultSize, 0)
        self.AIR_checkbox = wx.CheckBox(self, wx.ID_ANY, u"空口消息", wx.DefaultPosition, wx.DefaultSize, 0)
        self.NPR_checkbox.SetValue(True)
        self.AIR_checkbox.SetValue(True)
        self.NPR_checkbox.Bind(wx.EVT_CHECKBOX, self.on_filter)
        self.AIR_checkbox.Bind(wx.EVT_CHECKBOX, self.on_filter)
        sizer.Add(self.NPR_checkbox, 0, wx.ALL, 1)
        sizer.Add(self.AIR_checkbox, 0, wx.ALL, 1)
        return sizer

    def __init_splitter_sizer(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        splitter_window = MultiSplitterWindow(parent=self, style=wx.SP_LIVE_UPDATE | wx.SP_HORIZONTAL)
        splitter_window.SetOrientation(wx.VERTICAL)
        self.log_ctrl = LogCtrlPanel(parent=splitter_window)
        self.obj_list = ObjectListPanel(parent=splitter_window, log_display=self.log_ctrl)

        splitter_window.AppendWindow(self.obj_list)
        splitter_window.AppendWindow(self.log_ctrl)
        sizer.Add(splitter_window, 1, wx.EXPAND | wx.ALL, 0)
        return sizer

    def on_refresh(self, event):
        self.serial_port.Items = Serial.get_ports()

    def on_connect(self, event):
        try:
            self.serial = Serial.Serial(port=self.serial_port.GetStringSelection())
            self.obj_list.parse(serial=self.serial)
            self.serial_port.Disable()
            self.connect.Disable()
        except SerialException, e:
            Utility.AlertError(e.message)

    def on_disconnect(self, event):
        if self.serial is not None:
            self.serial.close()
            self.serial_port.Enable()
            self.connect.Enable()

    def on_filter(self, event):
        need_filter = ["e2eMessage"]
        if self.NPR_checkbox.IsChecked():
            need_filter.append("NprMessage")
        if self.AIR_checkbox.IsChecked():
            need_filter.append("AirMessage")
        self.obj_list.filter(need_filter)


class ObjectListPanel(wx.Panel):
    def __init__(self, parent, log_display):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.OLV = ObjectListView(self, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        sizer.Add(self.OLV, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        self.SetSizer(sizer)
        self.log_display = log_display

        # self.OLV.Bind(wx.EVT_CONTEXT_MENU, self.on_right_click)
        self.OLV.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)
        # self.OLV.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.double_click_on_item)

    def filter(self, need_filter):
        _filter = Filter.Chain(Filter.Predicate(lambda item: item._type in need_filter))
        self.OLV.SetFilter(Filter.Chain(_filter))
        self.OLV.RepopulateList()

    def parse(self, serial):
        self.data = Data(obj_list=self.OLV, serial=serial)
        self.data.Analysis()

    def stop(self):
        if self.data:
            self.data.stop()

    def on_item_selected(self, event):
        obj = self.OLV.GetSelectedObject()
        self.log_display.SetValue("")
        for line in obj._block:
            wx.CallAfter(self.log_display.AppendText, text=line.strip('\t\r\n') + '\n')


class LogCtrlPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.text_ctrl = wx.TextCtrl(self, wx.ID_ANY, value="", style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        sizer.Add(self.text_ctrl, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        self.SetSizer(sizer)

    def SetValue(self, value):
        self.text_ctrl.SetValue(value=value)

    def AppendText(self, text):
        try:
            self.text_ctrl.AppendText(text)
        except Exception:
            self.text_ctrl.AppendText(repr(text))


class Data(object):
    def __init__(self, obj_list, serial):
        self.__serial = serial
        self.__list_view = obj_list
        self.__coarse_strings = ['smac-stack-sap.h', 'asc_proc_func_def.c', 'ntx_proc_func_def.c']
        self.__set_columns()
        self.__list_view.rowFormatter = self.__set_row_formatter
        self.__data = []
        self.__patterns = [libs.trace_patterns, libs.e2e_patterns, libs.NPR_patterns]
        self.__buff = []
        self.__log_count = 0
        self.__flag = True

    def stop(self):
        self.__flag = False

    def __analysis_serial(self):
        for line_number, block in self.yield_log(self.__patterns):
            self.Append(line_nubmer=line_number, block=block)

    def Analysis(self):
        Utility.append_work(target=self.__analysis_serial)

    def Append(self, line_nubmer, block):
        self.__log_count += 1
        first_line = block[0]
        if ' NPR proc recv stack_primitive ' in first_line:
            npr = libs.NprMessage(_no=self.__log_count, block=block, line=line_nubmer)
            self.__check_last_msg()
            self.__data.append(npr)
            CallAfter(self.__list_view.AddObject, npr)
        elif 'Print e2e msg header information start' in first_line:
            e2e = libs.e2eMessage(_no=self.__log_count, block=block, line=line_nubmer)
            self.__data.append(e2e)
            # CallAfter(self.__list_view.AddObject, e2e)
        elif 'air message begin ' in first_line:
            air = libs.AirMessage(_no=self.__log_count, block=block, line=line_nubmer)
            self.__merge_air_and_e2e(air=air)
            self.__data.append(air)
            CallAfter(self.__list_view.AddObject, air)

    def __merge_air_and_e2e(self, air):
        try:
            last_msg = self.__data[-1]
        except IndexError:
            last_msg = None
        if type(last_msg) == libs.e2eMessage:
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
        if type(last_msg) == libs.e2eMessage:
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
        from lib.UserInterface.libs import Colour
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

    def yield_line(self):
        counter = 0
        while self.__serial.is_open() and self.__flag:
            line = self.__serial.read_line()
            counter += 1
            yield counter, line.replace('\x00', '')

    def yield_log(self, patterns):
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

        mLog = self.yield_line()
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
