import sys
from types import ModuleType


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
        url, prefix = self._parse_name(name)
        return self.env[name]

    def _parse_name(self, name):
        raw_prefix = name.split('__')[1:]
        prefix = "/%s" % "/".join(raw_prefix)

        name = name.replace("__%s" % '__'.join(raw_prefix), "")
        url = ".".join(name.split('_'))
        return url, prefix


if __name__ != "__main__":
    self = sys.modules[__name__]
    sys.modules[__name__] = SelfWrapper(self)
