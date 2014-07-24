import sys
from types import ModuleType

from .resource import Resource


class Model(dict):
    def __init__(self, *args, **kwargs):
        for arg in args:
            if isinstance(arg, dict):
                self.update(arg)
            else:
                raise TypeError('Argument %s is not an dict' % arg)
        self.update(kwargs)

        self.__dict__ = self

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            return super(Model, self).__getattr__(name)

    def __setattr__(self, name, value):
        if isinstance(value, dict) and name[0:2] != '__':
            self.__dict__[name] = Model(value)
        else:
            super(dict, self).__setattr__(name, value)


class SelfWrapper(ModuleType):
    def __init__(self, self_module, baked_args={}):
        for attr in ["__builtins__", "__doc__", "__name__", "__package__"]:
            setattr(self, attr, getattr(self_module, attr, None))

        self.__path__ = []
        self.self_module = self_module
        self.env = globals()

    def __setattr__(self, name, value):
        if hasattr(self, "env"):
             self.env[name] = value
        ModuleType.__setattr__(self, name, value)

    def __getattr__(self, name):
        if name == "env":
             raise AttributeError
        if name not in self.env:
            host, prefix = self._parse_name(name)
            self.env[name] = Resource()
            self.env[name].config.host = host
            self.env[name].config.prefix = prefix
        return self.env[name]

    def _parse_name(self, name):
        parts = name.split('__')
        host = parts[0].replace('_', '.')
        prefix = ''
        if len(parts) > 1:
            prefix = parts[1].replace('_', '/') + '/'
        return host, prefix


self = sys.modules[__name__]
sys.modules[__name__] = SelfWrapper(self)
