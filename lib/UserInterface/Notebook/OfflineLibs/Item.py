from re import compile
from lib import Utility

__trace_begin_pattern = compile(r' Trace <(.*?)> air message begin ')
__trace_end_pattern = compile(r' Trace <(.*?)> air message end ')
trace_patterns = (__trace_begin_pattern, __trace_end_pattern)

__e2e_begin_pattern = compile(r' Print e2e msg header information start ')
__e2e_end_pattern = compile(r' Print e2e msg header information end ')
NPR_begin_pattern = compile(r'================ NPR proc recv stack_primitive <(.*?)> ')
NPR_end_pattern = compile(r'================ NPR proc recv stack_primitive <(.*?)> ')
NPR_patterns = (NPR_begin_pattern, NPR_end_pattern)
time_pattern = compile(r'(\d+/\d+/\d+,MS:\d+) ')
e2e_patterns = (__e2e_begin_pattern, __e2e_end_pattern)

src_pattern = compile(r'src_id       = (\d+)')
dest_pattern = compile(r'dest_id      = (\d+)')


class Message(object):
    def __init__(self, _no, blocks, line):
        self._line = line
        self._no = _no
        self._time = ''
        self._prot = ''
        self._src = ''
        self._dest = ''
        self._info = ''
        self._blocks = blocks
        self._type = ''

    def _parse(self):
        raise NotImplementedError

    def _convert_time(self, line):
        tmp = Utility.find_in_string(time_pattern, line)
        self._time = tmp.replace(',MS', '')


class AirMessage(Message):
    def __init__(self, _no, blocks, line):
        super(Message, self).__init__(_no, blocks, line)
        self._type = "AirMessage"


class NprMessage(Message):
    def __init__(self, _no, blocks, line):
        Message.__init__(self, _no=_no, blocks=blocks, line=line)
        self._type = "NprMessage"
        self._parse()

    def _parse(self):
        fl = self._blocks[0]
        if 'NPR proc recv stack_primitive' in fl:
            self._prot = Utility.find_in_string(pattern=NPR_begin_pattern, string=fl)
            self._convert_time(fl)


class IllegalMessage(Message):
    def __init__(self, _no, blocks, line):
        super(Message, self).__init__(_no, blocks, line)
        self._type = "IllegalMessage"
