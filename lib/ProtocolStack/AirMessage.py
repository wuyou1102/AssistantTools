# -*- encoding:UTF-8 -*-
import six
from re import compile

__trace_begin_pattern = compile(r' Trace <(.*?)> air message begin ')
__trace_end_pattern = compile(r' Trace <(.*?)> air message end ')
trace_patterns = (__trace_begin_pattern, __trace_end_pattern)

__e2e_begin_pattern = compile(r' Print e2e msg header information start ')
__e2e_end_pattern = compile(r' Print e2e msg header information end ')
NPR_begin_pattern = compile(r'================ NPR proc recv stack_primitive <(.*?)> ')
NPR_end_pattern = compile(r'================ NPR proc recv stack_primitive <(.*?)> ')
NPR_patterns = (NPR_begin_pattern, NPR_end_pattern)
e2e_patterns = (__e2e_begin_pattern, __e2e_end_pattern)

src_pattern = compile(r'src_id       = (\d+)')
dest_pattern = compile(r'dest_id      = (\d+)')


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
