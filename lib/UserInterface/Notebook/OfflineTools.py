# -*- encoding:UTF-8 -*-
import wx
from NotebookBase import NotebookBase
from lib import Utility
from wx import dataview
from wx import CallAfter
import time

Logger = Utility.getLogger(__name__)


class OfflineTools(NotebookBase):
    def __init__(self, parent):
        NotebookBase.__init__(self, parent=parent, name="OFFLINE")
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        LogAnalysisSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "LogAnalysis"), wx.VERTICAL)
        PickerSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.log_picker = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, "Select a file",
                                            "Log files (*.log)|*.log|All files (*.*)|*.*", wx.DefaultPosition,
                                            wx.DefaultSize, wx.FLP_DEFAULT_STYLE)
        analysis_button = wx.Button(self, wx.ID_ANY, "Analysis", wx.DefaultPosition, wx.DefaultSize, 0)
        analysis_button.Bind(wx.EVT_BUTTON, self.__analysis_log)
        PickerSizer.Add(self.log_picker, 1, wx.ALL, 1)
        PickerSizer.Add(analysis_button, 0, wx.ALL, 1)

        self.data_ctrl = wx.dataview.DataViewListCtrl(self, wx.ID_ANY)
        self.data_ctrl.AppendToggleColumn("Toggle")
        self.data_ctrl.AppendTextColumn("Text")
        self.data_ctrl.AppendTextColumn("dd")
        LogAnalysisSizer.Add(PickerSizer, 0, wx.EXPAND)
        LogAnalysisSizer.Add(self.data_ctrl, 1, wx.EXPAND | wx.ALL, 1)

        mainSizer.Add(LogAnalysisSizer, 1, wx.EXPAND, 5)
        self.SetSizer(mainSizer)

    def __analysis_log(self, event):
        def analysis(log_file):
            line_num = 0
            with open(log_file) as log:
                for line in log.readlines():
                    line_num += 1
                    data = [True, line, line_num]
                    CallAfter(self.data_ctrl.AppendItem, data)

        log_file = self.log_picker.GetPath()
        if Utility.exists(log_file):
            Utility.append_work(target=analysis, log_file=log_file)
        else:
            Logger.warn('\"%s\" does not exist.' % log_file)
