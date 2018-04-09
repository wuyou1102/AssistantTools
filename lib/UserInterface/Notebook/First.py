# -*- encoding:UTF-8 -*-
import wx
from NotebookBase import NotebookBase
from lib import Utility

Logger = Utility.getLogger(__name__)

class First(NotebookBase):
    def __init__(self, parent):
        NotebookBase.__init__(self, parent=parent, name="First")
        main_box = wx.BoxSizer(wx.HORIZONTAL)  # 整个界面，水平布局
        self.start_button = wx.Button(self, -1, "First")
        self.Bind(wx.EVT_BUTTON, self.on_start, self.start_button)
        main_box.Add(self.start_button, 1, wx.ALL, 50)

        self.SetSizer(main_box)

    def on_start(self, event):
        Logger.info(self.name)
        Logger.debug(self.name)
        Logger.info(Utility.Path.WORKSPACE)

