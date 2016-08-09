import sys

from .magic import SelfWrapper


def register_module(name):
    zipa = sys.modules['zipa']
    sys.modules[name] = SelfWrapper(zipa)


class ModuleImporter(object):
    def __init__(self, module_name):
        self.module = module_name + '.'

    def find_module(self, name, path=None):
        if name.startswith(self.module):
            return self
        return None

    def load_module(self, name):
        register_module(name)
