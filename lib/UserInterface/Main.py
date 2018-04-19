# -*- encoding:UTF-8 -*-
import sys
import wx
import Notebook

reload(sys)
sys.setdefaultencoding('utf-8')


class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, id=999, title="Assistant Tool V0.0.1", size=(640, 480))
        self.Center()

        notebook = wx.Notebook(self)
        for table in Notebook.DISPLAY_PANEL:
            table_page = table(parent=notebook)
            notebook.AddPage(table_page, table_page.name)
