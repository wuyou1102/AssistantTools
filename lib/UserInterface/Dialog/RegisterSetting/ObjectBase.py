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
