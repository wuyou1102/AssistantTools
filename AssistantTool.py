# -*- encoding:UTF-8 -*-
__author__ = 'wuyou'
from lib import Logger
import sys
import wx
from lib.UserInterface import Frame
from lib import Utility

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == "__main__":
    Utility.getLogger()
    app = wx.App()
    f = Frame()
    f.Show()
    app.MainLoop()

