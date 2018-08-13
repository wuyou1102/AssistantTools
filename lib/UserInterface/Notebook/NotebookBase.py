# -*- encoding:UTF-8 -*-
import wx
import logging

logger = logging.getLogger(__name__)

PanelNameStr = "WUYOU"
class NotebookBase(wx.Panel):
    def __init__(self, parent=None, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TAB_TRAVERSAL,
                 name=PanelNameStr):
        self._name = name
        wx.Panel.__init__(self, parent=parent, id=id, pos=pos, size=size, style=style, name=self._name)

    @property
    def name(self):
        return self._name

    def close(self):
        logger.debug("Close Window")