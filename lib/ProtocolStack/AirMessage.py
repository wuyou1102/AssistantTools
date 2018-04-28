# -*- encoding:UTF-8 -*-
import six


class AirMessageField(str):
    def __new__(cls, name, target, source, message='', ):
        obj = str.__new__(cls, name)
        obj.MSG = message
        obj.TARGET = target
        obj.SOURCE = source
        return obj


class AirMessageMetaClass(type):
    def __new__(cls, name, bases, namespace):
        code_message_map = {}
        for k, v in namespace.items():
            if getattr(v, '__class__', None) and isinstance(v, AirMessageField):
                if code_message_map.get(v):
                    raise ValueError("Duplicated name {0} {1}".format(k, v))
                code_message_map[v] = getattr(v, 'MSG', "")
        namespace["CODE_MESSAGE_MAP"] = code_message_map
        return type.__new__(cls, name, bases, namespace)


class BaseAirMessage(six.with_metaclass(AirMessageMetaClass)):
    CODE_MESSAGE_MAP = NotImplemented


W = AirMessageField(name="hello", source="a", target="b", message="hello")
HELLO = AirMessageField(name="world", source="a", target="b", message="world")
aaaa = AirMessageField(name="hello", source="a", target="b", message="world")
