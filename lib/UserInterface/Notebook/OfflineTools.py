# -*- encoding:UTF-8 -*-
import wx
from NotebookBase import NotebookBase
from lib import Utility
from wx import CallAfter
import time

Logger = Utility.getLogger(__name__)


class OfflineTools(NotebookBase):
    def __init__(self, parent):
        NotebookBase.__init__(self, parent=parent, name="OFFLINE")
        MainSizer = wx.BoxSizer(wx.VERTICAL)

        LogAnalysisSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "LogAnalysis"), wx.VERTICAL)
        PickerSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.log_picker = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, "Select a file",
                                            "Log files (*.log)|*.log|All files (*.*)|*.*", wx.DefaultPosition,
                                            wx.DefaultSize, wx.FLP_DEFAULT_STYLE)
        analysis_button = wx.Button(self, wx.ID_ANY, "Analysis", wx.DefaultPosition, wx.DefaultSize, 0)
        analysis_button.Bind(wx.EVT_BUTTON, self.__analysis_log)
        PickerSizer.Add(self.log_picker, 1, wx.ALL, 1)
        PickerSizer.Add(analysis_button, 0, wx.ALL, 1)

        self.DVTC = DV.DataViewTreeCtrl(self, wx.ID_ANY,
                                        style=DV.DV_ROW_LINES | DV.DV_VERT_RULES)
        tree = self.DVTC
        il = wx.ImageList(16, 16)
        il.Add((wx.ArtProvider.GetBitmap(wx.ART_CDROM, wx.ART_OTHER, (16, 16))))
        il.Add((wx.ArtProvider.GetBitmap(wx.ART_ERROR, wx.ART_OTHER, (16, 16))))

        tree.AssignImageList(il)

        for d in range(3):
            itemd = tree.AppendContainer(DV.NullDataViewItem, text='dddddd', icon=1, expanded=1, data="asd")
            for c in range(10):
                itemc = tree.AppendContainer(itemd, 'cccccccc', 0)
                for b in range(10):
                    itema = tree.AppendItem(itemc, text='aaaaaaaaaaaaa', icon=0,  data="asd")

        self.SetSizer(mainSizer)

                    # self.DVTC.Create(self)
        # container = self.DVTC.AppendContainer(self.DVTC, text="ss")
        LogAnalysisSizer.Add(PickerSizer, 0, wx.EXPAND)
        LogAnalysisSizer.Add(self.DVTC, 1, wx.EXPAND | wx.ALL, 1)
        MainSizer.Add(LogAnalysisSizer, 1, wx.EXPAND, 5)
        self.SetSizer(MainSizer)

    def __analysis_log(self, event):
        def analysis(log_file):
            line_num = 0
            with open(log_file) as log:
                for line in log.readlines():
                    line_num += 1
                    data = [True, line, line_num]
<<<<<<< HEAD
                    CallAfter(self.data_ctrl.AppendItem, data)
<<<<<<< HEAD
=======
                    if line_num % 999 == 0:
                        time.sleep(0.1)
=======
                    CallAfter(self.DVTC.AppendItem, data)
>>>>>>> 47c8ca939bade19d0d07a985c031dd03dfbd38ce
>>>>>>> parent of 706b853... Revert "Merge branch 'master' of https://github.com/wuyou1102/AssistantTools"

        log_file = self.log_picker.GetPath()
        if Utility.exists(log_file):
            Utility.append_work(target=analysis, log_file=log_file)
        else:
            Logger.warn('\"%s\" does not exist.' % log_file)

    def asd(self):
        for x in range(999):
            data = [True, "hello world:%s" % x, x]
            CallAfter(self.DVTC.AppendItem, data)
