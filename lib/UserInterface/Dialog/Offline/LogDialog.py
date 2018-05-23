# encoding: utf-8
from lib.UserInterface.Dialog import DialogBase
from lib.UserInterface import OfflineLibs
import wx
from ObjectListView import ObjectListView, ColumnDefn, Filter
from lib import Utility
from re import compile
import re


class LogDialog(DialogBase.DialogBase):
    def __init__(self, obj, line_mapping_file):
        DialogBase.DialogBase.__init__(self, name="Log", size=(1000, 800))
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.obj = obj
        self.line_mapping_file = line_mapping_file
        self.select_obj = None
        LeftSizer = wx.BoxSizer(wx.VERTICAL)

        Rightizer = wx.BoxSizer(wx.VERTICAL)

        SearchSizer = wx.BoxSizer(wx.HORIZONTAL)
        # f_choice = ['', 'Value']
        # self.filed_choice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, f_choice, 0)
        # self.filed_choice.SetSelection(0)
        # e_choice = ['', 'contains', 'not contain', '==', '!=']
        # self.expression_choice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, e_choice, 0)
        # self.expression_choice.SetSelection(0)
        self.content_tc = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.content_tc.Bind(wx.EVT_TEXT, self.input_content)

        # search_button = wx.Button(self, wx.ID_ANY, u"搜索", wx.DefaultPosition, wx.DefaultSize, 0)
        # clear_button = wx.Button(self, wx.ID_ANY, u"清空", wx.DefaultPosition, wx.DefaultSize, 0)
        # search_button.Bind(wx.EVT_BUTTON, self.on_search)
        # clear_button.Bind(wx.EVT_BUTTON, self.on_clear)

        # SearchSizer.Add(self.filed_choice, 0, wx.TOP | wx.ALL, 7 | 5)
        # SearchSizer.Add(self.expression_choice, 0, wx.TOP | wx.ALL, 7 | 5)
        SearchSizer.Add(self.content_tc, 1, wx.EXPAND | wx.ALL, 5)
        # SearchSizer.Add(search_button, 0, wx.ALL, 5)
        # SearchSizer.Add(clear_button, 0, wx.ALL, 5)
        self.OLV = ObjectListView(self, wx.ID_ANY,
                                  style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        self.OLV.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.double_click_on_item)
        self.OLV.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, self.right_click_on_col)
        LeftSizer.Add(SearchSizer, 0, wx.EXPAND)
        LeftSizer.Add(self.OLV, 1, wx.EXPAND)
        MainSizer.Add(LeftSizer, 1, wx.EXPAND | wx.ALL, 5)
        MainSizer.Add(Rightizer, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(MainSizer)
        self.__set_columns()
        self.__set_row_formatter()
        self.__filter = dict()
        self.__init_data()
        self.__init_shortcut_key()
        self.__filter_dict = dict()

    def __init_shortcut_key(self):
        def create_key(func):
            key_id = wx.NewId()
            self.Bind(wx.EVT_MENU, func, id=key_id)
            return key_id

        self.ctrl_f_id = create_key(self.ctrl_f)
        self.ctrl_d_id = create_key(self.ctrl_d)
        self.ctrl_g_id = create_key(self.ctrl_g)

        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('F'), self.ctrl_f_id),
            (wx.ACCEL_CTRL, ord('D'), self.ctrl_d_id),
            (wx.ACCEL_CTRL, ord('G'), self.ctrl_g_id),
        ])
        self.SetAcceleratorTable(accel_tbl)

    def on_search(self, event):
        pass

    def on_clear(self, event):
        pass

    d_flag = False
    g_flag = False

    def ctrl_d(self, event):
        self.d_flag = not self.d_flag
        if self.OLV.GetSelectedObject():
            self.select_obj = self.OLV.GetSelectedObject()
        if self.d_flag:
            self.display_marked()
            self.select_last_object()
        else:
            self.display_search()
            self.select_last_object()

    def select_last_object(self):
        if self.select_obj:
            self.OLV.SelectObject(self.select_obj, ensureVisible=True)

    def ctrl_f(self, event):
        self.content_tc.SetFocus()
        self.content_tc.SelectAll()

    def ctrl_g(self, event):
        if self.OLV.GetSelectedObject():
            self.select_obj = self.OLV.GetSelectedObject()
            self.g_flag = not self.g_flag
            if self.g_flag:
                self.OLV.SetFilter(None)
                self.OLV.RepopulateList()
            else:
                self.display_search()
            self.select_last_object()

    def display_search(self):
        text = self.content_tc.GetValue()
        if text:
            self.OLV.SetFilter(Filter.TextSearch(self.OLV, text=text))
            self.OLV.RepopulateList()
        else:
            self.set_filter()

    def input_content(self, event):
        # if self.filed_choice.GetStringSelection() or self.expression_choice.GetStringSelection():
        #     return
        # else:
        self.display_search()

    def right_click_on_col(self, event):
        col_obj = self.GetColumn(event=event)
        field_name = col_obj.valueGetter
        if field_name in ['_no', '_time', '_func_num', '_value']:
            return
        col_values = self.GetColValues(field_name)
        col_values.sort()

        menu = wx.Menu()
        for value in col_values:
            item = self.__init_menu_item(text=value, parent=menu)
            menu.Append(item)
            if value not in self.__filter_dict.get(field_name, []):
                item.Check(True)
        self.Bind(wx.EVT_MENU, lambda evt, menu=menu, field=field_name: self.set_filter_dict(evt, menu, field))
        self.PopupMenu(menu)
        menu.Destroy()

    def __init_menu_item(self, text, parent):
        text = str(text) if text else u'空'
        item = wx.MenuItem(parent, wx.ID_ANY, text=text, kind=wx.ITEM_CHECK)
        return item

    def set_filter_dict(self, event, menu, field):
        _id = event.GetId()
        if _id == self.ctrl_d_id:
            return self.ctrl_d(event)
        elif _id == self.ctrl_f_id:
            return self.ctrl_f(event)
        elif _id == self.ctrl_g_id:
            return self.ctrl_g(event)

        elif not event.IsChecked():
            tmp = self.__filter_dict.get(field, [])
            string = menu.GetLabel(_id) if menu.GetLabel(_id) != u'空' else ''
            tmp.append(string)
            self.__filter_dict[field] = tmp
        else:
            tmp = self.__filter_dict.get(field)
            string = menu.GetLabel(_id) if menu.GetLabel(_id) != u'空' else ''
            tmp.remove(string)
            self.__filter_dict[field] = tmp
        self.set_filter()

    def set_filter(self):
        f = Filter.Predicate(lambda x: x.filter(self.__filter_dict))
        chain = Filter.Chain(f)
        self.OLV.SetFilter(chain)
        self.OLV.RepopulateList()

    def display_marked(self):
        f = Filter.Predicate(lambda x: x._marked)
        chain = Filter.Chain(f)
        self.OLV.SetFilter(chain)
        self.OLV.RepopulateList()

    def GetColValues(self, attr_name):
        tmp = []
        for obj in self.OLV.GetObjects():
            attr = obj.__getattribute__(attr_name)
            if attr not in tmp:
                tmp.append(attr)
        return tmp

    def GetColumn(self, event):
        i = event.GetColumn()
        if i == -1:
            return None
        else:
            return self.OLV.columns[i]

    def double_click_on_item(self, event):
        obj = self.OLV.GetSelectedObject()
        if not obj:
            return
        dlg = wx.TextEntryDialog(None, obj._ori, 'Add Comments', obj._comments)
        if dlg.ShowModal() == wx.ID_OK:
            response = dlg.GetValue()
            obj._comments = response

            obj._marked = True if response else False
            self.OLV.RefreshObject(obj)

    def __init_data(self):
        line_number = self.obj._line
        start_line = line_number - OfflineLibs.FORWARD_ROW if line_number > OfflineLibs.FORWARD_ROW else 0
        end_line = line_number + len(self.obj._block) + OfflineLibs.BACKWARD_ROW
        files = self.__sorted_files(files=self.line_mapping_file.values())
        objects = list()
        for obj in self.yield_object(files=files, start=start_line, end=end_line):
            objects.append(obj)
        self.OLV.SetObjects(objects)

        self.OLV.SetFocus()
        self.OLV.SelectObject(self.OLV.GetObjects()[line_number - start_line - 1], ensureVisible=True)

    def find_start_file(self, line):
        keys = self.line_mapping_file.keys()
        keys.sort(reverse=True)
        for key in keys:
            if line >= key:
                return line - key, self.line_mapping_file.get(key)
        return None, None

    def __sorted_files(self, files):
        return sorted(files, key=lambda x: Utility.convert_timestamp(str=Utility.basename(x),
                                                                     time_fmt='%Y_%m_%d-%H_%M_%S.log'))

    def yield_object(self, files, start, end):
        start_line, log_file = self.find_start_file(start)
        end_line = start_line + (end - start)
        a = files.index(log_file)
        tmp = list()
        for f in files[a:]:
            with open(f, 'rb') as mfile:
                tmp.extend(mfile.readlines())
                if len(tmp) > end_line:
                    break
        counter = start
        for line in tmp[start_line:end_line]:
            counter += 1
            if line == '\n':
                continue
            line_obj = Line(counter, line)
            if line_obj._ori in self.obj._block:
                line_obj.set_flag()
            yield line_obj

    def __set_columns(self):
        self.OLV.SetColumns(
            [
                ColumnDefn(title=u"No.", align="left", width=60, valueGetter='_no'),
                ColumnDefn(title=u"不知道是什么", align="left", width=40, valueGetter='_f'),
                ColumnDefn(title=u"Name", align="center", width=60, valueGetter='_name'),
                ColumnDefn(title=u"Level", align="center", width=40, valueGetter='_level'),
                ColumnDefn(title=u"Time", align="left", width=80, valueGetter='_time'),
                ColumnDefn(title=u"Function", align="left", width=80, valueGetter='_func'),
                ColumnDefn(title=u"又不知道", align="center", width=80, valueGetter='_func_num'),
                ColumnDefn(title=u"Value", align="left", width=500, valueGetter='_value'),
                ColumnDefn(title=u"Comments", align="left", width=100, valueGetter='_comments'),
            ]
        )

    def __set_row_formatter(self):
        self.OLV.rowFormatter = self.row_formatter

    @staticmethod
    def row_formatter(OLV, item):
        if item._marked:
            OLV.SetBackgroundColour(OfflineLibs.LightCyan)
        elif item._flag:
            OLV.SetBackgroundColour(OfflineLibs.LemonChiffon)
        else:
            OLV.SetBackgroundColour(OfflineLibs.White)


UTF16_LE_BOM = "\xff\x7f"
line_pattern = compile(
    r'(\[\d+\])([\sa-zA-Z0-9]*) (Info|Warm) (\d+/\d+/\d+,MS:\d+) (.*?) (\d+) (.*)')


class Line(object):
    def __init__(self, no, value):
        self._no = no
        self._ori = value
        self._value = value if UTF16_LE_BOM not in value else value.replace(UTF16_LE_BOM, 'Unknown')
        self._f = ''
        self._name = ''
        self._level = ''
        self._time = ''
        self._func = ''
        self._func_num = ''
        self._marked = False
        self._comments = ''
        self._flag = False
        self.__parse()

    def __parse(self):
        result = re.findall(line_pattern, self._value)
        if result:
            t_group = result[0]
            self._f = t_group[0]
            self._name = t_group[1]
            self._level = t_group[2]
            self._time = t_group[3]
            self._func = t_group[4]
            self._func_num = t_group[5]
            self._value = t_group[6]

    def filter(self, filter_dict):
        if self._f in filter_dict.get('_f', []):
            return False
        elif self._name in filter_dict.get('_name', []):
            return False
        elif self._level in filter_dict.get('_level', []):
            return False
        elif self._func in filter_dict.get('_func', []):
            return False
        elif self._comments in filter_dict.get('_comments', []):
            return False
        else:
            return True

    def set_flag(self):
        self._flag = True
