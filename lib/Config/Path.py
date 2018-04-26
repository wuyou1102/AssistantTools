from os.path import join
from os.path import exists
from os import makedirs as __makedirs


def _makedirs(path, *paths):
    p = join(path, *paths)
    if not exists(p):
        __makedirs(p)
    return p


def _get_workspace():
    from sys import argv
    from os.path import abspath
    from os.path import dirname
    return abspath(dirname(argv[0]))


WORKSPACE = _get_workspace()
WORKSPACE = 'D:\AssistantTools'
REPOSITORY = _makedirs(WORKSPACE, 'repository')
RESOURCE = _makedirs(WORKSPACE, 'resource')
LOG = _makedirs(WORKSPACE, 'log')

EXE_NOTEPAD = join(RESOURCE, 'notepad++', 'notepad++.exe')
