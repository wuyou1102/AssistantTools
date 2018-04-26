import time


def get_timestamp(time_fmt='%Y_%m_%d-%H_%M_%S', t=time.time()):
    return time.strftime(time_fmt, time.localtime(t))


def convert_timestamp(str, time_fmt='%Y_%m_%d-%H_%M_%S'):
    return time.mktime(time.strptime(str, time_fmt))


if __name__ == '__main__':
   print convert_timestamp('2018_04_25-17_46_14')