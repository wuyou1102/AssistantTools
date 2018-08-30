import wx
import logging

logger = logging.getLogger(__name__)


class ObjectBase(object):
    def __init__(self, item):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.item = item
        self.lst = list()
        self.last_address = None
        self.last_value = None

    def get_sizer(self):
        return self.sizer

    def get_name(self):
        return self.item['name']

    def refresh(self):
        logger.error('%s has not the refresh function.' % self.__class__.__name__)

        # raise NotImplementedError('Chiild must have refresh function')

    def get_mpl_title(self):
        return '%s-%s' % (self.__class__.__name__, self.item['title'])

    def SetStringSelection(self, selection, wx_choice):
        if selection:
            wx_choice.SetStringSelection(selection)
        else:
            wx_choice.SetSelection(wx.NOT_FOUND)

    def SetCheck(self, value, wx_checkbox):
        if value == '1':
            wx_checkbox.SetValue(True)
        else:
            wx_checkbox.SetValue(False)
