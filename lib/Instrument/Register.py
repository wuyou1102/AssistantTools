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
        return self.__DeviceInit()

    def Release(self):
        return self.__DeviceRelease()

    def Set(self, address, data):
        if self.lock.acquire():
            try:
                result = self.__SetReg(self.__ConvertAddress(address), self.__ConvertData(data))
                if result == 0:
                    raise IOError('Can not set address info.')
                return True
            except Exception, e:
                Logger.error(e.message)
            finally:
                self.lock.release()

    def Get(self, address):
        if self.lock.acquire():
            try:
                tmp_str = create_string_buffer(b"\0\0\0\0", 4)  # create a 4 byte buffer
                result = self.__GetReg(self.__ConvertAddress(address), tmp_str)
                if result == 0:
                    raise IOError('Can not get address info.')
                value = binascii.b2a_hex(tmp_str.raw[::-1]).upper()
                Logger.info('Read Address: %s and Value is : %s' % (hex(address), value))
                return value
            except Exception:
                Logger.error('Exeption')
            finally:
                self.lock.release()

    def __ConvertAddress(self, address):
        return c_uint32(address)

    def __ConvertData(self, data):
        t=type(data)
        if t == int:
            return data
        elif t== str:
            return int(data, 16)
        elif t==unicode:
            return int(data, 16)

if __name__ == '__main__':
    r = Register()

    print r.Init()

    print r.Get(0x60680000)
    print r.Set(0x60680000, '000B0200')
    print r.Get(0x60680000)
