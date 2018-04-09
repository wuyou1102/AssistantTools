from lib.Config import Path
from lib.Config import Parameter
from logging import getLogger

__Logger = getLogger(__name__)


def print_config_value():
    def print_attributes(_class):
        __Logger.debug(_class.__name__)
        attributes = dir(_class)
        for attribute in attributes:
            if attribute[0] != "_":
                __Logger.debug("%-20s: %s" % (attribute, _class.__dict__.get(attribute)))
    print_attributes(Path)
    print_attributes(Parameter)
