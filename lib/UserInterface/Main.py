# -*- encoding:UTF-8 -*-
import sys
import wx

reload(sys)
sys.setdefaultencoding('utf-8')
from lib.Config import Page

class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, title="Assistant Tool V0.0.1", size=(1440, 800))
        self.Center()
        notebook = wx.Notebook(self)
        for table in Page.KPI_TOOLS:
            table_page = table(parent=notebook)
            notebook.AddPage(table_page,table_page.name)

        for table in Page.OFFLINE_TOOLS:
            table_page = table(parent=notebook)
            notebook.AddPage(table_page,table_page.name)

        for table in Page.ONLINE_TOOLS:
            table_page = table(parent=notebook)
            notebook.AddPage(table_page,table_page.name)
