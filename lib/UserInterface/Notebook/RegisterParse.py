# -*- encoding:UTF-8 -*-
import wx
from NotebookBase import NotebookBase
from lib import Utility
from MatplotPanel import MatplotPanel

Logger = Utility.getLogger(__name__)


class RegisterParse(NotebookBase):
    def __init__(self, parent):
        NotebookBase.__init__(self, parent=parent, name="Register")

        self.MPL = MatplotPanel(self)

        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        MplSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"信号强度"), wx.VERTICAL)
        MplSizer.Add(self.MPL, 1, wx.EXPAND)


        MainSizer.Add(MplSizer, 1, wx.EXPAND|wx.ALL,5)
        self.SetSizer(MainSizer)

        # 状态栏
        # self.StatusBar()

        # MPL_Frame界面居中显示
        self.Centre(wx.BOTH)
