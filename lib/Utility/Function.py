from lib.Config import Path
from lib.Config import Parameter
from logging import getLogger
from inspect import isfunction, ismodule, isclass, ismethod
from lib.Thread.Manager import append_work
from os.path import exists, basename
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
        __Logger.error('Can not find the pattern.')
        __Logger.error("Pattern:" + pattern)
        __Logger.error("String :" + repr(string))
        result = 'Illegal'
    finally:
        return result
