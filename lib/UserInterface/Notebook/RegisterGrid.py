# -*- encoding:UTF-8 -*-
import wx
from wx import grid
from NotebookBase import NotebookBase
from lib import Utility
from lib.Config import Instrument

Logger = Utility.getLogger(__name__)


class RegisterGrid(NotebookBase):
    def __init__(self, parent):
        NotebookBase.__init__(self, parent=parent, name="寄存器")
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        LeftSizer = wx.BoxSizer(wx.VERTICAL)
        RightSizer = wx.BoxSizer(wx.VERTICAL)
        self.RegisterMapping = {
            "BB AXI configure": (0x60640000, 0x6067FFFF),
            'b': (0x62000000, 0x620000FF),
            'c': (0x63000000, 0x630000FF),
            'd': (0x64000000, 0x640000FF),
            'e': (0x65000000, 0x650000FF),
            'f': (0x66000000, 0x660000FF),

        }

        self._start_address = ""
        self.LB_AddressCategory = wx.ListBox(parent=self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=(160, -1),
                                             choices=self.RegisterMapping.keys())
        self.LB_AddressCategory.Bind(wx.EVT_LISTBOX, self.on_item_select)
        refresh_button = wx.Button(self, wx.ID_ANY, "Refresh", wx.DefaultPosition, wx.DefaultSize, 0)
        import_button = wx.Button(self, wx.ID_ANY, "Import", wx.DefaultPosition, wx.DefaultSize, 0)
        export_button = wx.Button(self, wx.ID_ANY, "Export", wx.DefaultPosition, wx.DefaultSize, 0)
        refresh_button.Bind(wx.EVT_BUTTON, self.on_refresh)

        AddressSizer = wx.BoxSizer(wx.HORIZONTAL)
        ST_start_address = wx.StaticText(self, wx.ID_ANY, u"Start Address: ", wx.DefaultPosition, wx.DefaultSize, 0)
        ST_end_address = wx.StaticText(self, wx.ID_ANY, u"End Address: ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.TC_start_address = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.TC_end_address = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.TC_start_address.Bind(wx.EVT_KILL_FOCUS, self.after_start_address_input)
        self.DG = DataGrid(self)
        AddressSizer.Add(ST_start_address, 0, wx.ALL, 5)
        AddressSizer.Add(self.TC_start_address, 0, wx.ALL, 2)
        AddressSizer.Add(ST_end_address, 0, wx.ALL, 5)
        AddressSizer.Add(self.TC_end_address, 0, wx.ALL, 2)

        LeftSizer.Add(self.LB_AddressCategory, 1, wx.EXPAND | wx.ALL, 5)
        LeftSizer.Add(refresh_button, 0, wx.EXPAND | wx.ALL, 5)
        LeftSizer.Add(import_button, 0, wx.EXPAND | wx.ALL, 5)
        LeftSizer.Add(export_button, 0, wx.EXPAND | wx.ALL, 5)

        RightSizer.Add(AddressSizer, 0, wx.EXPAND | wx.ALL, 5)
        RightSizer.Add(self.DG, 1, wx.EXPAND | wx.ALL, 5)

        MainSizer.Add(LeftSizer, 1, wx.EXPAND)
        MainSizer.Add(RightSizer, 0, wx.EXPAND)
        self.SetSizer(MainSizer)

    def get_current_page(self):
        return self.TC_start_address.GetValue()

    def on_refresh(self, event):
        event.GetEventObject().Disable()
        try:
            self.DG.RefreshAllData()
        except Exception, e:
            print e

        finally:
            event.GetEventObject().Enable()

    def after_start_address_input(self, event):
        value = self.TC_start_address.GetValue()

        event.Skip()

    def on_item_select(self, event):
        select = self.LB_AddressCategory.GetStringSelection()
        start, end = self.RegisterMapping[select]
        self.TC_start_address.SetValue(self.__convert_address(start))
        self.TC_end_address.SetValue(self.__convert_address(end))

    def __convert_address(self, address):
        return hex(address).upper()


class DataGrid(grid.Grid):  ##, mixins.GridAutoEditMixin):
    def __init__(self, parent):
        self.parent = parent
        grid.Grid.__init__(self, parent, -1)
        self.CreateGrid(16, 4)
        self.__SetLabelValue()
        self.__SetAttr()
        self._data = [["", "", "", ""] for x in range(16)]
        self.__SetAllCellValue()
        self.reg = Instrument.get_register()

        self.Bind(grid.EVT_GRID_CELL_RIGHT_DCLICK, self.OnCellRightDClick)
        self.Bind(grid.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.Bind(grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnCellRightClick)
        self.Bind(grid.EVT_GRID_CELL_CHANGED, self.OnCellChange)

    def RefreshAllData(self):
        start = int(self.parent.get_current_page(), 16)
        data = list()
        for x in range(start, start + 256, 4):
            data.append(self.reg.Get(x))
        self._data = [list(x) for x in zip(*[iter(data)] * 4)]
        self.__SetAllCellValue()

    def RefreshCellData(self, row, col):
        address = self.GetAddress(row=row, col=col)
        if not address:
            Logger.error('Can not find address.')
            return False
        value = self.reg.Get(address)
        self._data[row][col] = value
        self.SetCellValue(row, col, self._data[row][col])
        return True

    def SetCellData(self, row, col, value):
        address = self.GetAddress(row=row, col=col)
        if not address:
            Logger.error('Can not find address.')
            return False
        self.reg.Set(address=address, data=value)
        self._data[row][col] = value
        return True

    def GetAddress(self, row, col):
        start = self.parent.get_current_page()
        if start:
            start = self.parent.get_current_page()
            address = int(start, 16) + row * 16 + col * 4
            return address
        return None

    def __SetAllCellValue(self):
        for row in range(self.GetNumberRows()):
            for col in range(self.GetNumberCols()):
                self.SetCellValue(row=row, col=col, s=self._data[row][col])

    def __SetLabelValue(self):
        cols = "048C"
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
        for x in range(self.GetNumberRows()):
            self.SetRowSize(x, 28)
        for x in range(self.GetNumberCols()):
            self.SetColSize(x, 130)

    def OnCellRightDClick(self, event):
        event.Skip()

    def __CheckInput(self, value):
        if value.startswith('0x'):
            pass
        try:
            value = int(value, 16)
        except ValueError:
            return False
        if value < 0 or value > 4294967295:
            return False
        return True

    def OnCellChange(self, event):
        row, col = event.GetRow(), event.GetCol()
        value = self.GetCellValue(row, col)
        if self.__CheckInput(value=value):
            self.SetCellData(col=col, row=row, value=value.upper())
        else:
            Logger.error("Wrong Value: %s" % value)
        self.SetCellValue(row, col, self._data[row][col])

    def OnCellLeftClick(self, event):
        event.Skip()
        # row, col = event.GetRow(), event.GetCol()
        # self.RefreshCellData(row=row, col=col)
        # event.Skip()

    def OnCellRightClick(self, event):
        row, col = event.GetRow(), event.GetCol()
        self.RefreshCellData(row=row, col=col)
        event.Skip()
