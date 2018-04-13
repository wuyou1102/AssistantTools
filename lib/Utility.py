from lib.Config import Path
from lib.Config import Parameter
from logging import getLogger
from inspect import isfunction, ismodule, isclass
from time import time, localtime, strftime

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


def get_timestamp(time_fmt='%Y_%m_%d-%H_%M_%S'):
    return strftime(time_fmt, localtime(time()))
