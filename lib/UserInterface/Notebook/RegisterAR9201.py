# -*- encoding:UTF-8 -*-
import wx
from wx import grid
from NotebookBase import NotebookBase
from lib import Utility
from lib.Config import Instrument
import time

Logger = Utility.getLogger(__name__)
import binascii


def get_cell_label():
    cols = "0123456789ABCDEF"
    rows = "0123456789ABCDEF"
    lst = list()
    for x in rows:
        for y in cols:
            lst.append("%s%s" % (x, y))
    return lst


NA = u"NA"
bit_str = "bit_%s"
cell_label = get_cell_label()


class RegisterAR9201(NotebookBase):
    def __init__(self, parent):
        NotebookBase.__init__(self, parent=parent, name="AR9201")
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        LeftSizer = wx.BoxSizer(wx.VERTICAL)
        RightSizer = wx.BoxSizer(wx.VERTICAL)
        self.RegisterMapping = {
            "chengwei": 0x60630000,
            "BB AXI configure": 0x60640000,
            "BB APB configure": 0x60680000,
        }

        self.LB_AddressCategory = wx.ListBox(parent=self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=(160, -1),
                                             choices=self.RegisterMapping.keys())
        self.LB_AddressCategory.Bind(wx.EVT_LISTBOX, self.on_item_select)

        AddressSizer = self.__init_address()
        BitSizer = self.__init_bit()
        self.AF_flag = True
        self.DG = DataGridFF(self)
        RightTopSizer = wx.BoxSizer(wx.HORIZONTAL)
        OpSizer = self.__init_operation()
        LeftSizer.Add(self.LB_AddressCategory, 1, wx.EXPAND | wx.ALL, 5)
        LeftSizer.Add(OpSizer, 0, wx.EXPAND | wx.ALL, 5)

        RightTopSizer.Add(AddressSizer, 0, wx.EXPAND)
        RightTopSizer.Add(BitSizer, 0, wx.LEFT, 5)

        RightSizer.Add(RightTopSizer, 0, wx.EXPAND | wx.ALL, 0)
        RightSizer.Add(self.DG, 1, wx.EXPAND | wx.TOP, 1)

        MainSizer.Add(LeftSizer, 1, wx.EXPAND | wx.ALL, 1)
        MainSizer.Add(RightSizer, 0, wx.EXPAND | wx.ALL, 1)
        self.SetSizer(MainSizer)

    def __init_operation(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        refresh_button = wx.Button(self, wx.ID_ANY, u"Refresh", wx.DefaultPosition, wx.DefaultSize, 0)
        import_button = wx.Button(self, wx.ID_ANY, u"Import", wx.DefaultPosition, wx.DefaultSize, 0)
        export_button = wx.Button(self, wx.ID_ANY, u"Export", wx.DefaultPosition, wx.DefaultSize, 0)

        refresh_button.Bind(wx.EVT_BUTTON, self.on_refresh)
        refresh_button.Bind(wx.EVT_RIGHT_DCLICK, self.auto_refresh)
        export_button.Bind(wx.EVT_BUTTON, self.on_export)
        import_button.Bind(wx.EVT_BUTTON, self.on_import)
        sizer.Add(refresh_button, 1, wx.EXPAND | wx.ALL, 0)
        sizer.Add(import_button, 1, wx.EXPAND | wx.ALL, 0)
        sizer.Add(export_button, 1, wx.EXPAND | wx.ALL, 0)
        return sizer

    def __init_bit(self):
        sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Bit"), wx.HORIZONTAL)
        toggle_size = (25, 25)
        for x in range(8):
            self.__setattr__(bit_str % x,
                             wx.ToggleButton(self, wx.ID_ANY, u"%s" % (7 - x), wx.DefaultPosition, toggle_size, 0))
            obj = self.__getattribute__(bit_str % x)
            obj.Bind(wx.EVT_TOGGLEBUTTON, self.on_bit_change)
            sizer.Add(obj, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)

        # for x in range(7, -1, -1):
        #     obj = self.__getattribute__(bit_str % x)
        #     obj.Bind(wx.EVT_TOGGLEBUTTON, self.on_bit_change)
        #     sizer.Add(obj, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)
        return sizer

    def __init_address(self):
        sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Address"), wx.HORIZONTAL)
        button_size = (30, 30)
        forward = wx.Button(self, wx.ID_ANY, u"<", wx.DefaultPosition, button_size, 0)
        fforward = wx.Button(self, wx.ID_ANY, u"<<", wx.DefaultPosition, button_size, 0)
        backward = wx.Button(self, wx.ID_ANY, u">", wx.DefaultPosition, button_size, 0)
        bbackward = wx.Button(self, wx.ID_ANY, u">>", wx.DefaultPosition, button_size, 0)
        add = wx.Button(self, wx.ID_ANY, u"+", wx.DefaultPosition, button_size, 0)
        forward.Bind(wx.EVT_BUTTON, self.on_forward)
        fforward.Bind(wx.EVT_BUTTON, self.on_fforward)
        backward.Bind(wx.EVT_BUTTON, self.on_backward)
        bbackward.Bind(wx.EVT_BUTTON, self.on_bbackward)
        add.Bind(wx.EVT_BUTTON, self.add_new_dialog)
        st_current_text = wx.StaticText(self, wx.ID_ANY, u"Current Page: ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.st_current_address = wx.TextCtrl(self, wx.ID_ANY, "0x00000000", wx.DefaultPosition, (97, 20), 0)
        sizer.Add(fforward, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(forward, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(st_current_text, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        sizer.Add(self.st_current_address, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
        sizer.Add(backward, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(bbackward, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(add, 0, wx.ALIGN_CENTER_VERTICAL)
        return sizer

    def on_export(self, event):
        dlg = wx.FileDialog(self,
                            message="Save Current Page",
                            wildcard="Page (*.txt)|*.txt|All files (*.*)|*.*",
                            # defaultFile="%s" % (self.get_current_page()),
                            defaultDir="",
                            style=wx.FD_SAVE
                            )
        if dlg.ShowModal() == wx.ID_OK:
            txt_path = dlg.GetPaths()[0]
            data = self.DG.GetCurrentPageValue()
            with open(txt_path, 'w') as w_file:
                w_file.write(data)
        dlg.Destroy()

    def on_import(self, event):
        dlg = wx.FileDialog(self,
                            message="Select Page",
                            wildcard="Page (*.txt)|*.txt|All files (*.*)|*.*",
                            defaultDir="",
                            style=wx.FD_OPEN
                            )
        if dlg.ShowModal() == wx.ID_OK:
            txt_path = dlg.GetPaths()[0]
            data = self.__read_page(txt_path)
            if data:
                r = self.DG.ImportValue(data=data)
                if r:
                    msg_dlg = wx.MessageDialog(self, u"成功", u"Import",
                                               wx.OK)
                    if msg_dlg.ShowModal() == wx.ID_OK:
                        msg_dlg.Destroy()
                else:
                    msg_dlg = wx.MessageDialog(self, u"失败", u"Import",
                                               wx.OK | wx.ICON_ERROR)
                    if msg_dlg.ShowModal() == wx.ID_OK:
                        msg_dlg.Destroy()

            else:
                msg_dlg = wx.MessageDialog(self, u"数据格式不正确，请检查后重新添加，具体错误原因请查看控制台输出。", u"   文件异常", wx.OK | wx.ICON_ERROR)
                if msg_dlg.ShowModal() == wx.ID_OK:
                    msg_dlg.Destroy()
        dlg.Destroy()

    def add_new_dialog(self, event):
        dialog = DataGridDialog(size=(600, 560), name=self.get_current_page())
        dialog.Show()

    def __read_page(self, file):
        def convert_line(l):
            if ":" in l:
                return l.strip('\r\n').split(':')[:2]
            else:
                return "", ""

        c = cell_label[:]
        d = dict()
        with open(file) as f:
            for line in f:
                address, value = convert_line(l=line)
                if address not in d.keys():
                    d[address] = value
                else:
                    Logger.error("Duplicate \"%s\",Old:<%s>  New:<%s>" % (address, d[address], value))
                    return False
        for k in d.keys():
            try:
                c.remove(k)
                v = int(d[k], 16)
                if v < 0 or v > 255:
                    raise ValueError
            except ValueError:
                Logger.error("Illegal data,Cell\"%s\", Value:<%s>" % (k, d[k]))
                return False
        if len(c) != 0:
            for x in c:
                Logger.error("Lack Cell\"%s\"" % x)
            return False
        return d

    def on_forward(self, event):
        current = int(self.get_current_page(), 16)
        tmp = current - 256 if current - 256 > 0 else 0
        self.set_current_page(address=tmp)
        self.DG.RefreshAllData()

    def on_fforward(self, event):
        current = int(self.get_current_page(), 16)
        tmp = current - 4096 if current - 4096 > 0 else 0
        self.set_current_page(address=tmp)
        self.DG.RefreshAllData()

    def on_backward(self, event):
        current = int(self.get_current_page(), 16)
        tmp = current + 256
        self.set_current_page(address=tmp)
        self.DG.RefreshAllData()

    def on_bbackward(self, event):
        current = int(self.get_current_page(), 16)
        tmp = current + 4096
        self.set_current_page(address=tmp)
        self.DG.RefreshAllData()

    def get_current_page(self):
        return self.st_current_address.GetValue()

    def set_current_page(self, address):
        self.st_current_address.SetValue(self.__convert_address(address=address))
        return True

    def on_refresh(self, event):
        # event.GetEventObject().Disable()
        try:
            self.DG.RefreshAllData()
        except Exception, e:
            Logger.error(e)
        finally:
            pass
            # event.GetEventObject().Enable()

    def AUTO_REFRESH(self):
        while self.AF_flag:
            wx.CallAfter(self.DG.RefreshAllData)
            time.sleep(1)

    def auto_refresh(self, event):
        obj = event.GetEventObject()
        state = obj.GetLabel()
        if state == u"Refresh":
            obj.SetLabel(u'Auto Refresh')
            self.AF_flag = True
            Utility.append_work(self.AUTO_REFRESH, allow_dupl=False)
        elif state == u'Auto Refresh':
            self.AF_flag = False
            obj.SetLabel(u"Refresh")
        else:
            self.AF_flag = False
            obj.SetLabel(u"Refresh")

    def after_start_address_input(self, event):
        value = self.st_current_address.GetValue()
        event.Skip()

    def on_item_select(self, event):
        select = self.LB_AddressCategory.GetStringSelection()
        address = self.RegisterMapping[select]
        self.st_current_address.SetValue(self.__convert_address(address))
        self.DG.RefreshAllData()

    def __convert_address(self, address):
        h = hex(address).upper()[2:]
        h = "0x" + "0" * (8 - len(h)) + h
        return h

    def SetBit(self, value):
        if value == u'' or value == NA:
            Logger.info("Cell Value is not valid: \"%s\"." % value)
            value = "0"
        b = bin(int(value, 16))[2:]
        b = "0" * (8 - len(b)) + b
        for x in range(len(b)):
            obj = self.__getattribute__(bit_str % x)
            obj.SetValue(True if b[x] == '1' else False)

    def on_bit_change(self, event):
        if not self.DG.GetSelectedCell():
            return False
        tmp = ""
        for x in range(8):
            obj = self.__getattribute__(bit_str % x)
            tmp += "1" if obj.GetValue() else "0"
        h = hex(int(tmp, 2))[2:]
        if len(h) == 1:
            h = "0" + h
        self.DG.ChangeCell(h)


class DataGridFF(grid.Grid):  ##, mixins.GridAutoEditMixin):
    def __init__(self, parent):
        self.parent = parent
        grid.Grid.__init__(self, parent, -1)
        self.CreateGrid(16, 16)
        self.__SetLabelValue()
        self.__SetAttr()
        self._data = [["" for x in range(16)] for y in range(16)]
        self.__SetAllCellValue()
        self.reg = Instrument.get_register()
        self.SelectedCell = None

        self.Bind(grid.EVT_GRID_CELL_RIGHT_DCLICK, self.OnCellRightDClick)
        self.Bind(grid.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.Bind(grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnCellRightClick)
        self.Bind(grid.EVT_GRID_CELL_CHANGED, self.OnCellChange)
        self.Bind(grid.EVT_GRID_SELECT_CELL, self.OnSelectCell)

    def GetSelectedCell(self):
        return self.SelectedCell

    def RefreshAllData(self):
        start = int(self.parent.get_current_page(), 16)
        data = list()
        for x in range(start, start + 256, 4):
            byte = self.reg.GetByte(x)
            if byte:
                for x in range(4):
                    data.append(binascii.b2a_hex(byte[x]).upper())
            else:
                for x in range(4):
                    data.append(NA)
        self._data = self.ConvertData(data=data)
        self.__SetAllCellValue()
        if self.SelectedCell:
            r, c = self.SelectedCell
            self.SetCellBackgroundColour(r, c, wx.WHITE)
        self.SelectedCell = None
        self.parent.SetBit("0")

    def ConvertData(self, data):
        if len(data) != 256:
            Logger.error(u"The number of results does not satisfy the expectation.")
            Logger.error(u"Except: \"64\",but was \"%s\"" % len(data))
            lst = [[NA for x in range(16)] for y in range(16)]
            return lst
        else:
            lst = [list(x) for x in zip(*[iter(data)] * 16)]
            return lst

    def HighlightCell(self, row, col):
        if self.SelectedCell:
            r, c = self.SelectedCell
            self.SetCellBackgroundColour(r, c, wx.WHITE)
        self.SetCellBackgroundColour(row, col, "#EEEE00")
        self.SelectedCell = (row, col)

    def RefreshCellValue(self, row, col):
        value = self.GetAddressValue(row=row, col=col)
        return self.__updata_cell_value(row=row, col=col, value=value)

    def __updata_cell_value(self, row, col, value):
        if not value:
            return False
        start_col = col / 4 * 4
        for x in range(4):
            t_col = start_col + x
            self._data[row][t_col] = binascii.b2a_hex(value[x]).upper()
            self.SetCellValue(row, t_col, self._data[row][t_col])
        return True

    def __change_cell_value(self, row, col, value):
        self.SetAddressValue(col=col, row=row, value=value.upper())
        r_value = self.GetAddressValue(row=row, col=col)
        if not r_value:
            return False
        if value != binascii.b2a_hex(r_value[col % 4]):
            Logger.warn("Cell (%d,%d) can not be set as \"%s\" ." % (row, col, value))
        if self.__updata_cell_value(row=row, col=col, value=r_value):
            self.Parent.SetBit(value=self.GetCellValue(row=row, col=col))
            return True
        return False

    def Get4Byte(self, row, col):
        tmp = []
        for x in range(4):
            t_col = col + x
            tmp.append(self._data[row][t_col])
        return tmp

    def ReplaceByte(self, lst_byte, idx, value):
        lst_byte[idx] = value
        return ''.join(lst_byte[::-1])

    def SetAddressValue(self, row, col, value):
        start_col = col / 4 * 4
        i = col - start_col
        data = self.ReplaceByte(lst_byte=self.Get4Byte(row, start_col), idx=i, value=value)

        address = self.GetAddress(row=row, col=start_col)
        if address is None:
            Logger.error('Can not find address.')
            return False
        if not self.reg.Set(address=address, data=data):
            Logger.error('Can not set the value to address.')
            return False
        self._data[row][col] = value
        return True

    def ImportValue(self, data, address=0x60680000):
        b = bin(int(data['00'], 16))[2:]
        b = "0" * (8 - len(b)) + b

        Logger.info(b)
        page_number = b[:-5]
        Logger.info(page_number)
        if not page_number:
            page_number = "00"
        page_number = int(page_number, 2)
        address = address + page_number * 256
        Logger.info("Import Page: %s" % hex(address))
        lst = zip(*[iter(cell_label[::-1])] * 4)
        result = True
        for m in lst:
            d = ""
            a = address + int(m[-1], 16)
            for e in m:
                d += data[e]
            result = result and self.reg.Set(address=a, data=d)
        if result:
            self.parent.set_current_page(address=address)
            self.RefreshAllData()
        return result

    def GetAddressValue(self, row, col):
        address = self.GetAddress(row=row, col=col)
        if address is None:
            Logger.error('Can not find address.')
            return False
        value = self.reg.GetByte(address)
        return value

    def GetAddress(self, row, col):
        start = self.parent.get_current_page()
        if start:
            start = self.parent.get_current_page()
            address = int(start, 16) + row * 16 + col
            return address
        return None

    def __SetAllCellValue(self):
        for row in range(self.GetNumberRows()):
            for col in range(self.GetNumberCols()):
                self.SetCellValue(row=row, col=col, s=self._data[row][col])

    def __SetLabelValue(self):
        cols = "0123456789ABCDEF"
        rows = "0123456789ABCDEF"
        self.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        self.SetRowLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        self.SetColLabelSize(-1)
        self.SetRowLabelSize(-1)
        for x in range(len(cols)):
            self.SetColLabelValue(x, cols[x])
        for x in range(len(rows)):
            self.SetRowLabelValue(x, rows[x])

    def __SetAttr(self):
        self.SetDefaultCellFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        self.DisableDragColSize()
        self.DisableDragRowSize()
        self.SetDefaultColSize(35, True)
        self.SetDefaultRowSize(28, True)

        self.SetSelectionMode(3)

        # for x in range(self.GetNumberRows()):
        #
        #     self.SetRowSize(x, 28)
        # for x in range(self.GetNumberCols()):
        #     self.SetColSize(x, 34)

    def OnCellRightDClick(self, event):
        event.Skip()

    def __CheckInput(self, value):
        if value.startswith('0x'):
            pass
        try:
            value = int(value, 16)
        except ValueError:
            return False
        if 0 <= value <= 255:
            return True
        return False

    def OnCellChange(self, event):
        row, col = event.GetRow(), event.GetCol()
        value = self.GetCellValue(row, col)
        if self.__CheckInput(value=value):
            if len(value) == 1:
                value = "0" + value
            return self.__change_cell_value(row=row, col=col, value=value)
        else:
            Logger.error("Wrong Value: %s" % value)
        self.SetCellValue(row, col, self._data[row][col])

    def OnCellLeftClick(self, event):
        event.Skip()

    def ChangeCell(self, value):
        row, col = self.SelectedCell
        return self.__change_cell_value(row=row, col=col, value=value)

    def OnCellRightClick(self, event):
        row, col = event.GetRow(), event.GetCol()
        self.RefreshCellValue(row=row, col=col)
        event.Skip()

    def OnSelectCell(self, event):
        row, col = event.GetRow(), event.GetCol()
        self.HighlightCell(row=row, col=col)
        value = self.GetCellValue(row=row, col=col)
        Logger.info("Selected (%d,%d) Cell: %s." % (row, col, value))
        self.Parent.SetBit(value=value)
        event.Skip()

    def GetCurrentPageValue(self):
        cols = "0123456789ABCDEF"
        rows = "0123456789ABCDEF"
        lst = list()
        for x in range(self.GetNumberRows()):
            for y in range(self.GetNumberCols()):
                lst.append("%s%s:%s" % (rows[x], cols[y], self.GetCellValue(x, y)))
        return '\n'.join(lst)


from lib.UserInterface.Dialog import DialogBase


class DataGridDialog(DialogBase.DialogBase):
    def __init__(self, size, name="", positon=wx.DefaultPosition):
        DialogBase.DialogBase.__init__(self, name=name, size=size, pos=positon)
        self.AF_flag = True
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        TopSizer = wx.BoxSizer(wx.HORIZONTAL)
        BitSizer = self.__init_bit()
        refresh_button = wx.Button(self, wx.ID_ANY, u"Refresh", wx.DefaultPosition, (100, 46), 0)
        refresh_button.Bind(wx.EVT_BUTTON, self.on_refresh)
        refresh_button.Bind(wx.EVT_RIGHT_DCLICK, self.auto_refresh)
        TopSizer.Add(BitSizer, 0, wx.EXPAND)
        TopSizer.Add(refresh_button, 0, wx.TOP, 8)
        self.DG = DataGridFF(self)
        MainSizer.Add(TopSizer, 0, wx.ALIGN_CENTER)
        MainSizer.Add(self.DG, 1, wx.ALIGN_CENTER | wx.TOP, 3)

        self.SetSizer(MainSizer)
        self.DG.RefreshAllData()
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def __init_bit(self):
        sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Bit"), wx.HORIZONTAL)
        toggle_size = (25, 25)
        for x in range(8):
            self.__setattr__(bit_str % x,
                             wx.ToggleButton(self, wx.ID_ANY, u"%s" % (7 - x), wx.DefaultPosition, toggle_size, 0))
            obj = self.__getattribute__(bit_str % x)
            obj.Bind(wx.EVT_TOGGLEBUTTON, self.on_bit_change)
            sizer.Add(obj, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)

        # for x in range(7, -1, -1):
        #     obj = self.__getattribute__(bit_str % x)
        #     obj.Bind(wx.EVT_TOGGLEBUTTON, self.on_bit_change)
        #     sizer.Add(obj, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)
        return sizer

    def get_current_page(self):
        return self.name

    def on_bit_change(self, event):
        if not self.DG.GetSelectedCell():
            return False
        tmp = ""
        for x in range(8):
            obj = self.__getattribute__(bit_str % x)
            tmp += "1" if obj.GetValue() else "0"
        h = hex(int(tmp, 2))[2:]
        if len(h) == 1:
            h = "0" + h
        self.DG.ChangeCell(h)

    def SetBit(self, value):
        if value == u'' or value == NA:
            Logger.info("Cell Value is not valid: \"%s\"." % value)
            value = "0"
        b = bin(int(value, 16))[2:]
        b = "0" * (8 - len(b)) + b
        for x in range(len(b)):
            obj = self.__getattribute__(bit_str % x)
            obj.SetValue(True if b[x] == '1' else False)

    def on_refresh(self, event):
        # event.GetEventObject().Disable()
        try:
            self.DG.RefreshAllData()
        except Exception, e:
            Logger.error(e)
        finally:
            pass
            # event.GetEventObject().Enable()

    def AUTO_REFRESH(self):
        while self.AF_flag:
            wx.CallAfter(self.DG.RefreshAllData)
            time.sleep(1)

    def auto_refresh(self, event):
        obj = event.GetEventObject()
        state = obj.GetLabel()
        if state == u"Refresh":
            obj.SetLabel(u'Auto Refresh')
            self.AF_flag = True
            Utility.append_work(self.AUTO_REFRESH, allow_dupl=False, thread_name="AUTO_REFRESH: %s" % self.name)
        elif state == u'Auto Refresh':
            self.AF_flag = False
            obj.SetLabel(u"Refresh")
        else:
            self.AF_flag = False
            obj.SetLabel(u"Refresh")

    def on_close(self, event):
        Logger.debug("Close Register Dialog: %s" % self.name)
        self.AF_flag = False
        event.Skip()
