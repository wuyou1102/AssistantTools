# -*- encoding:UTF-8 -*-
import lib.Logger
import threading
import lib.Utility
from lib.Config.Parameter import ErrorCode
Logger = lib.Utility.getLogger(__name__)

__thread_pool = dict()
__work_type_list = ['Refresh']


def append_work(**kwargs):
    lib.Logger.debug("t_mgr|Add work: %s" % kwargs)
    __parse_work(**kwargs)


def __parse_work(work_type, **kwargs):
    if work_type in __thread_pool.keys():
        if __thread_pool.get(type).isAlive():
            Logger.warn(ErrorCode.THREAD_EXIST.message)
            return ErrorCode.THREAD_EXIST



def __append_thread(**kwargs):
    target = kwargs.get("target")
    name = kwargs.get('name')
    t = threading.Thread(target=target, kwargs=kwargs)
    t.setDaemon(True)
    __thread_pool[name] = t
    t.start()
