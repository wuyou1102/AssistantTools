# -*- encoding:UTF-8 -*-
from lib.Config import Path
from ctypes import *
import binascii

__RegLib_dll = Path.DLL_AR_SIRIUS_REQ_LIB

__CDLL = cdll.LoadLibrary(__RegLib_dll)
__SetReg = __CDLL.SetReg
__SetReg.argtypes = [c_uint32, c_char]
__GetReg = __CDLL.GetReg
__GetReg.argtypes = [c_uint32, c_char_p]
__DeviceInit = __CDLL.DeviceInit


def Init():
    return __DeviceInit()


def IsConnect():
    tmp_str = c_char_p('\0' * 4)
    result = __GetReg(__ConvertAddress(0x00000000), tmp_str)
    if result == 0:
        return False
    return True


def Set(address, data):
    result = __SetReg(__ConvertAddress(address), __ConvertData(data))
    if result == 0:
        raise IOError('Can not set address info.')
    return True


def Get(address):
    tmp_str = c_char_p('\0' * 4)
    result = __GetReg(__ConvertAddress(address), tmp_str)
    if result == 0:
        raise IOError('Can not get address info.')
    return binascii.b2a_hex(tmp_str.value).upper()


def __ConvertAddress(address):
    return c_uint32(address)


def __ConvertData(data):
    return data


if __name__ == '__main__':
    Init()
    print Get(44020000)
