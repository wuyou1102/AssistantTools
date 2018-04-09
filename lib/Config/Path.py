# -*- encoding:UTF-8 -*-

from lib import Utility

WORKSPACE = Utility.get_workspace()
REPOSITORY = Utility.make_dirs(WORKSPACE, 'repository')
RESOURCE = Utility.make_dirs(WORKSPACE, 'resource')
LOG = Utility.make_dirs(WORKSPACE, 'log')
