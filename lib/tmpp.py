import wx


class Mywin(wx.Frame):

    def __init__(self, parent, title):
        super(Mywin, self).__init__(parent, title=title, size=(400, 300))
        self.InitUI()

    def InitUI(self):
        menubar = wx.MenuBar()

        fileMenu = wx.Menu()

        for x in range(10000):
            fileMenu.Append(self.__init_menu_item(fileMenu, 'hello'))
            fileMenu.Append(self.__init_menu_item(fileMenu, 'world'))
            fileMenu.Append(self.__init_menu_item(fileMenu, '!'))


        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
        self.text = wx.TextCtrl(self, -1, style=wx.EXPAND | wx.TE_MULTILINE)
        #self.Bind(wx.EVT_MENU, self.menuhandlerm, menu=fileMenu)
        self.Bind(wx.EVT_MENU, lambda evt, menu=fileMenu: self.menuhandlerm(evt, menu))

        self.SetSize((350, 250))
        self.Centre()
        self.Show(True)

    def aaa(self, event):
        print event.Lable

    def __init_menu_item(self, parent, text):
        item = wx.MenuItem(parent, wx.ID_ANY, text=text, kind=wx.ITEM_CHECK, helpString='dddddd')
        return item

    def menuhandlerm(self, event, menu):
        id = event.GetId()
        if id == wx.ID_NEW:
            self.text.AppendText("new" + "\n")
        print event.IsChecked()
        id = event.GetId()
        print id
        print menu.GetLabel(id)


ex = wx.App()
Mywin(None, 'MenuBar Demo - yiibai.com')
ex.MainLoop()
