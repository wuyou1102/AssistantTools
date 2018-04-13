# -*- encoding:UTF-8 -*-
import threading
from lib import Utility
from lib.Config.Parameter import ErrorCode

Logger = Utility.getLogger(__name__)

__thread_pool = dict()


def append_work(target, allow_dupl=False, **kwargs):
    if not Utility.isfunction(target):
        Logger.error(ErrorCode.TARGET_NOT_FUNCTION.MSG)
        return False
    if work_type in __thread_pool.keys():
        if __thread_pool.get(work_type).isAlive():
            Logger.warn(ErrorCode.THREAD_EXIST.message)
            return ErrorCode.THREAD_EXIST
    lib.Logger.debug("t_mgr|Add work: %s" % kwargs)




def __append_thread(work_type, func, **kwargs):
    name = kwargs.get('name')
    t = threading.Thread(target=func, kwargs=kwargs)
    t.setDaemon(True)
    __thread_pool[name] = t
    t.start()


if __name__ == '__main__':
    def add():
        return False
    print add.__name__
    append_work(target=add)