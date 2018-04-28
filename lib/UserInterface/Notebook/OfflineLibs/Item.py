from re import compile
from lib import Utility
import re

trace_begin_pattern = compile(r' Trace <(.*?)> air message begin ')
trace_end_pattern = compile(r' Trace <(.*?)> air message end ')
trace_patterns = (trace_begin_pattern, trace_end_pattern)

__e2e_begin_pattern = compile(r' Print e2e msg header information start ')
__e2e_end_pattern = compile(r' Print e2e msg header information end ')
NPR_begin_pattern = compile(r'================ NPR proc recv stack_primitive <(.*?)> ')
NPR_end_pattern = compile(r'================ NPR proc recv stack_primitive <(.*?)> ')
NPR_patterns = (NPR_begin_pattern, NPR_end_pattern)
time_pattern = compile(r'(\d+/\d+/\d+,MS:\d+) ')
e2e_patterns = (__e2e_begin_pattern, __e2e_end_pattern)

src_pattern = compile(r'src_id       = (\d+)')
dest_pattern = compile(r'dest_id      = (\d+)')
network_pattern = compile(r'networkId            : (\d+)')
node_pattern = compile(r'nodeId               : (\d+)')


class Message(object):
    def __init__(self, _no, block, line):

        self._line = line
        self._no = _no
        self._time = ''
        self._prot = ''
        self._src = ''
        self._dest = ''
        self._info = ''
        self._block = block
        self._type = ''
        self._assign_time()

    def _parse(self):
        raise NotImplementedError

    def _assign_time(self):
        for line in self._block:
            result = re.findall(time_pattern, line)
            if result:
                self._time = result[0].replace(',MS', '')


class AirMessage(Message):
    def __init__(self, _no, block, line):
        Message.__init__(self, _no=_no, block=block, line=line)
        self._type = "AirMessage"
        self._parse()

    def _parse(self):
        fl = self._block[0]
        if 'air message begin' in fl:
            self._prot = Utility.find_in_string(pattern=trace_begin_pattern, string=fl)
        if self._prot == "S_SMAC_BR":
            for line in self._block:
                if 'networkId            :' in line:
                    self._dest = Utility.find_in_string(pattern=network_pattern, string=line)
                elif 'nodeId               :' in line:
                    self._src = Utility.find_in_string(pattern=node_pattern, string=line)


class NprMessage(Message):
    def __init__(self, _no, block, line):
        Message.__init__(self, _no=_no, block=block, line=line)
        self._type = "NprMessage"
        self._parse()

    def _parse(self):
        fl = self._block[0]
        if 'NPR proc recv stack_primitive' in fl:
            self._prot = Utility.find_in_string(pattern=NPR_begin_pattern, string=fl)


class e2eMessage(Message):
    def __init__(self, _no, block, line):
        Message.__init__(self, _no=_no, block=block, line=line)
        self._type = "e2eMessage"
        self._parse()

    def _parse(self):

        for line in self._block:
            if 'dest_id      = ' in line:
                self._dest = Utility.find_in_string(pattern=dest_pattern, string=line)
            elif 'src_id       =' in line:
                self._src = Utility.find_in_string(pattern=src_pattern, string=line)


class IllegalMessage(Message):
    def __init__(self, _no, block, line):
        Message.__init__(self, _no=_no, block=block, line=line)
        self._type = "IllegalMessage"

    def _parse(self):
        for block in self._block:
            print block
