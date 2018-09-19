# -*- encoding:UTF-8 -*-
import sys
import wx
import Notebook

reload(sys)
sys.setdefaultencoding('utf-8')


class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, id=999, title="Assistant Tool V1.0.1", size=(800, 600))
        self.Center()
        notebook = wx.Notebook(self)
        self.tables = list()
        for table in Notebook.DISPLAY_PANEL:
            table_page = table(parent=notebook)
            self.tables.append(table_page)
            notebook.AddPage(table_page, table_page.name)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        for table in self.tables:
            table.close()
        self.Destroy()
