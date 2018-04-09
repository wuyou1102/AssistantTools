# -*- encoding:UTF-8 -*-
import sys
import wx

reload(sys)
sys.setdefaultencoding('utf-8')
from lib.UserInterface import Notebook


class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, title="Assistant Tool V0.0.1", size=(1440, 800))
        self.Center()
        notebook = wx.Notebook(self)


        import string
        import random
        count = 0
        for x in (list(string.letters)):
            x= x+random.choice(string.letters)+random.choice(string.letters)+random.choice(string.letters)+random.choice(string.letters)+random.choice(string.letters)+random.choice(string.letters)+random.choice(string.letters)+random.choice(string.letters)+random.choice(string.letters)+random.choice(string.letters)+random.choice(string.letters)+random.choice(string.letters)+random.choice(string.letters)+random.choice(string.letters)+random.choice(string.letters)+random.choice(string.letters)+random.choice(string.letters)+random.choice(string.letters)

            count += 1
            if count % 3 == 2:
                notebook.AddPage(Notebook.First(parent=notebook, name=x), x)
            elif count % 3 == 1:
                notebook.AddPage(Notebook.Second(parent=notebook, name=x), x)
            elif count % 3 == 0:
                notebook.AddPage(Notebook.Third(parent=notebook, name=x), x)

        #
        # notebook.AddPage(Notebook.Third(notebook, 'c'), 'c')
        # notebook.AddPage(Notebook.First(notebook, 'a'), 'a')
        # notebook.AddPage(Notebook.Second(notebook, 'b'), 'b')
        self.Refresh()