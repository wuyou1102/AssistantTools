# -*- encoding:UTF-8 -*-
from logging import getLogger

from lib.Instrument.Register import Register
import time
__Logger = getLogger(__name__)


def __init__register():
    reg = Register()
    init_result = reg.Init()
    if init_result == 1:
        return reg
    elif init_result == -256:
        __Logger.error('The register instrument is being used by other application.')
        __Logger.error('Please close other application and try again.')
        return None
    else:
        __Logger.error('Can not find register instrument.')
        __Logger.error('Register instrument maybe is not power on.')
        return None


def get_register():
    if Instrument.register is None:
        Instrument.register = __init__register()
        return Instrument.register
    else:
        res = Instrument.register.Get(0x60680000)
        if res == '00000000':
            __Logger.error('Connect to the register instrument error')
            __Logger.info('Try:')
            for x in range(1, 11):
                __Logger.info('Reconnect:%d' % x)
                Instrument.register = __init__register()
                if Instrument.register is not None:
                    return Instrument.register
                time.sleep(0.1)
        return Instrument.register


class Instrument(object):
    register = None


if __name__ == '__main__':
    import time
    reg = get_register()
    for x in range(19):
        time.sleep(1)
        print get_register()