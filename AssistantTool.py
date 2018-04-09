# -*- encoding:UTF-8 -*-
__author__ = 'wuyou'
import sys
import wx
from lib import Logger
from lib.UserInterface import Frame

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == "__main__":
    app = wx.App()
    f = Frame()
    f.Show()
    app.MainLoop()
