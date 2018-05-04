# encoding: utf-8
from lib.UserInterface.Dialog import DialogBase
from lib.UserInterface.Notebook import OfflineLibs
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
        LeftSizer = wx.BoxSizer(wx.VERTICAL)
        Rightizer = wx.BoxSizer(wx.VERTICAL)
        self.OLV = ObjectListView(self, wx.ID_ANY,
                                  style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        self.OLV.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.double_click_on_item)
        self.OLV.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, self.right_click_on_col)
        LeftSizer.Add(self.OLV, 1, wx.EXPAND)
        MainSizer.Add(LeftSizer, 1, wx.EXPAND | wx.ALL, 5)
        MainSizer.Add(Rightizer, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(MainSizer)
        self.__set_columns()
        self.__set_row_formatter()
        self.__filter = dict()
        self.__init_data()
        self.__filter_dict = dict()

    def right_click_on_col(self, event):
        col_obj = self.GetColumn(event=event)
        field_name = col_obj.valueGetter
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
        menu.GetLabel(_id)
        if not event.IsChecked():
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
        tmp = []
        for k, v in self.__filter_dict.items():
            if not v:
                continue
            f = Filter.Predicate(lambda x: str(x.__getattribute__(k)) not in v)

            tmp.append(f)
        chain = Filter.Chain(*tmp)
        self.OLV.SetFilter(chain)
        self.OLV.RepopulateList()
        print len(self.OLV.GetFilteredObjects())

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
        dlg = wx.TextEntryDialog(None, "", 'Add Comments', obj._comments)
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
            yield Line(counter, line)

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
