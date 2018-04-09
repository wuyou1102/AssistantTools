# -*- encoding:UTF-8 -*-
from sys import argv
from os.path import join
from os.path import abspath as _abspath
from os.path import dirname as _dirname
from os.path import exists as _exists
from os import makedirs as _makedirs
from logging import getLogger


def make_dirs(path, *paths):
    p = join(path, *paths)
    if not _exists(p):
        _makedirs(p)
    return p


def get_workspace():
    return _abspath(_dirname(argv[0]))


if __name__ == '__main__':
    print make_dirs("C:/", 'a', 'b')
