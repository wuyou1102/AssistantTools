# -*- coding: utf-8 -*-
import wx
from lib.UserInterface.Notebook.NotebookBase import NotebookBase


class Second(NotebookBase):
    def __init__(self, parent,name):
        NotebookBase.__init__(self, parent=parent, name=name)
        main_box = wx.BoxSizer(wx.HORIZONTAL)  # 整个界面，水平布局
        self.start_button = wx.Button(self, -1, name)
        self.ss = wx.Button(self, -1, name)
        self.Bind(wx.EVT_BUTTON, self.on_start, self.start_button)
        main_box.Add(self.ss)
        main_box.Add(self.start_button, 1, wx.ALL, 50)

        self.SetSizer(main_box)

    def on_start(self, event):
        print 'hello world' + self.get_name()
