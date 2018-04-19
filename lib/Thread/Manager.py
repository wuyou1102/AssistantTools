# -*- encoding:UTF-8 -*-
import threading
import logging
from lib.Config.Parameter import ErrorCode
import types
from random import choice

Logger = logging.getLogger(__name__)

__thread_pool = dict()


def query_thread():
    Logger.debug(msg="%-10s|%50s" % ("STATE", "NAME"))
    for k, v in __thread_pool.items():
        Logger.debug(msg="%-10s|%50s" % ("RUNNING" if v.isAlive() else "DONE", k))


def append_work(target, allow_dupl=False, **kwargs):
    query_thread()
    if not isinstance(target, types.FunctionType) and not isinstance(target, types.MethodType):
        Logger.error(ErrorCode.TARGET_NOT_FUNCTION.MSG)
        return False
    if allow_dupl:
        return __append_thread_duplicate(target=target, **kwargs)
    else:
        return __append_thread(target=target, **kwargs)


def __append_thread_duplicate(target, **kwargs):
    def add_suffix(name):
        name += ':'
        for x in range(20):
            name += choice('0123456789ABCDEF')
        return name
    name = kwargs.get('name', target.__name__)
    name = add_suffix(name)
    return __start_thread(target=target, name=name, **kwargs)


def __append_thread(target, **kwargs):
    name = kwargs.get('name', target.__name__)
    _thread = __thread_pool.get(name)
    if _thread and _thread.isAlive():
        Logger.warn(ErrorCode.TARGET_ALREADY_EXIST)
        return False
    return __start_thread(target=target, name=name, **kwargs)


def __start_thread(target, name, **kwargs):
    t = threading.Thread(target=target, kwargs=kwargs)
    t.setDaemon(True)
    __thread_pool[name] = t
    t.start()
    Logger.debug(msg="%-10s|%50s" % ("STARTED", name))
    return True


if __name__ == '__main__':
    pass
