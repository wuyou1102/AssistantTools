# -*- encoding:UTF-8 -*-
from lib.Config import Path
from lib.Config import Parameter
from logging import getLogger
from inspect import isfunction, ismodule, isclass
import re

__Logger = getLogger(__name__)
__builtin_attr_list = ['__doc__', '__file__', '__name__', '__package__', '__builtins__']


def print_config_value():
    def print_attributes(_class):
        __Logger.debug(_class.__name__)
        attributes = dir(_class)
        for attr_name in attributes:
            attribute = _class.__dict__.get(attr_name)
            if attr_name in __builtin_attr_list or isfunction(attribute) or ismodule(attribute) or isclass(attribute):
                continue
            __Logger.debug("%-20s: %s" % (attr_name, attribute))

    print_attributes(Path)
    print_attributes(Parameter)


def find_in_string(pattern, string):
    try:
        result = re.findall(pattern, string)[0]
    except IndexError:
        result = 'Illegal'
        __Logger.error('Can not find the pattern.')
        __Logger.error("Pattern:%s" % pattern)
        __Logger.error("String :" + repr(string))

    finally:
        return result


def convert2bin(value, reverse=1):
    b = '{0:08b}'.format(ord(value))[::reverse]
    return b


def replace_bits(byte, start, need_replace):
    if not need_replace:
        return byte
    b = '{0:08b}'.format(ord(byte))
    end = start + len(need_replace)
    if end > 8:
        raise ValueError("%s->%s[%s:%s]" % (b, need_replace, start, end))
    start, end = 8 - end, 8 - start
    bits = list(b)
    need_replace = list(need_replace)
    for x in range(start, end):
        bits[x] = need_replace[x - start]
    b = ''.join(bits)
    return b


def swap_to_d1d3(d3d1):
    d3d1 = [d3d1[i:i + 2] for i in xrange(0, len(d3d1), 2)]
    return ''.join(d3d1[::-1])


# TODO
def check_hex_input(string):
    pass


if __name__ == '__main__':
    replace_bits('2', start=3, need_replace='32')
