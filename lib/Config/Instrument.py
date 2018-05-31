# -*- encoding:UTF-8 -*-
from logging import getLogger

from lib.Instrument.Register import Register
import time

__Logger = getLogger(__name__)

__register = Register()


def get_register():
    return __register




if __name__ == '__main__':
    import time

    reg = get_register()
    for x in range(19):
        time.sleep(1)
        print get_register()
