# -*- coding: utf-8 -*-
import wx
from lib.UserInterface.Notebook.NotebookBase import NotebookBase


class Third(NotebookBase):
    def __init__(self, parent):
        NotebookBase.__init__(self, parent=parent, name="Third")
        main_box = wx.BoxSizer(wx.HORIZONTAL)  # 整个界面，水平布局
        self.start_button = wx.Button(self, -1, "Third")
        self.Bind(wx.EVT_BUTTON, self.on_start, self.start_button)
        main_box.Add(self.start_button, 1, wx.ALL, 50)

        self.SetSizer(main_box)

    def on_start(self, event):
        print 'Third'
