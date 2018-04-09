# -*- encoding:UTF-8 -*-
import Logger
import threading
import Utility
Logger = Utility.getLogger(__name__)

__thread_pool = dict()
__work_type_list = ['Refresh']


def append_work(**kwargs):
    Logger.debug("t_mgr|Add work: %s" % kwargs)
    __parse_work(**kwargs)


def __parse_work(type, **kwargs):
    if type in __thread_pool.keys():
        if __thread_pool.get(type).isAlive():
            Logger.debug("t_mgr|Same work is already in process.")
            return None


def __append_thread(**kwargs):
    target = kwargs.get("target")
    name = kwargs.get('name')
    t = threading.Thread(target=target, kwargs=kwargs)
    t.setDaemon(True)
    __thread_pool[name] = t
    t.start()
