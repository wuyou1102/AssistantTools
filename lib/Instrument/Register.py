# -*- encoding:UTF-8 -*-
from lib.Config import Path
from ctypes import *
import binascii
import logging
import threading

Logger = logging.getLogger(__name__)


class Register(object):
    def __init__(self):
        __RegLib_dll = Path.DLL_AR_SIRIUS_REQ_LIB
        __CDLL = cdll.LoadLibrary(__RegLib_dll)
        self.lock = threading.Lock()
        self.__SetReg = __CDLL.SetReg
        self.__SetReg.argtypes = [c_uint32, c_uint32]
        self.__GetReg = __CDLL.GetReg
        self.__GetReg.argtypes = [c_uint32, c_char_p]
        self.__DeviceInit = __CDLL.DeviceInit
        self.__DeviceRelease = __CDLL.DeviceRelease

    def Init(self):
        result = self.__DeviceInit()
        Logger.info(
            'Register Device Init result:%s' % result)
        if result == 1:
            return True
        elif result == -256:
            Logger.error('The register instrument is being used by other application.')
            Logger.error('Please close other application and try again.')
            return False
        elif result == -2147483648:
            Logger.error('Can not find register instrument.')
            Logger.error('Register instrument maybe is not power on.')
            return False
        return False

    def Release(self):
        return self.__DeviceRelease()

    def Reconnect(self, times, in):
        import time
        Logger.info("Try reconnect the register device:")
        for x in range(1, times + 1):
            Logger.info('Reconnect: %s' % x)
            result = self.Init()
            if result:
                return True
            time.sleep(1)
        return False

    def Set(self, address, data):
        if self.lock.acquire():
            try:
                return self.__set(address=address, data=data)

            finally:
                self.lock.release()

    def __set(self, address, data):
        result = self.__SetReg(self.__ConvertAddress(address), self.__ConvertData(data))
        Logger.debug(
            'Set  Address \"%s\" value as \"%s\" and func result is  \"%s\"' % (hex(address), data, result))
        if result != -2147483647:
            if self.Reconnect():
                return self.__set(address=address, data=data)
            return False
        return True

    def Get(self, address):
        Logger.info('ssss')
        if self.lock.acquire():
            try:
                return self.__get(address=address)
            finally:
                self.lock.release()
        Logger.info('dddd')

    def __get(self, address):
        tmp_str = create_string_buffer(b"\0\0\0\0", 4)  # create a 4 byte buffer
        result = self.__GetReg(self.__ConvertAddress(address), tmp_str)
        if result != 1:
            if self.Reconnect():
                return self.__get(address=address)
            return False
            # raise IOError('Can not get address info.')
        value = binascii.b2a_hex(tmp_str.raw[::-1]).upper()
        Logger.debug(
            'Read Address \"%s\" value is \"%s\" and func result is  \"%s\"' % (hex(address), value, result))
        return value

    def __ConvertAddress(self, address):
        return c_uint32(address)

    def __ConvertData(self, data):
        t = type(data)
        if t == int:
            return data
        elif t == str:
            return int(data, 16)
        elif t == unicode:
            return int(data, 16)


if __name__ == '__main__':
    r = Register()
    r.Init()
    r.Get(0x60680000)
    r.Set(0x60680000, '000B0201')
    Logger.info('After set and read again.')
    r.Get(0x60680000)
    while True:
        if not r.Get(0x00000004):
            r.Init()
