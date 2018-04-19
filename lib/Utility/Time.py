from time import time, localtime, strftime


def get_timestamp(time_fmt='%Y_%m_%d-%H_%M_%S'):
    return strftime(time_fmt, localtime(time()))
