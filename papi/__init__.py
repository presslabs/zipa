import sys
from types import ModuleType
import requests
import json


class Model(dict):
    def __init__(self, *args, **kwargs):
        for arg in args:
            if isinstance(arg, dict):
                for key in arg:
                    self[key] = arg[key]
            else:
                raise TypeError('Argument %s is not an dict' % arg)

        for key in kwargs:
            self[key] = kwargs[key]

        self.__dict__ = self

    def __setattr__(self, name, value):
        if isinstance(value, dict) and name[0:2] != '__':
            self.__dict__[name] = Model(value)
        else:
            super(dict, self).__setattr__(name, value)


class Resource(dict):
    def __init__(self, url=None, name=None, params=None, config=None):
        self.url = url or '/'
        self.name = name
        self.params = params or {}
        self.config = config or {}

    def create(self, **kwargs):
        r = requests.post(self.url[:-1], data=json.dumps(kwargs),
                          auth=self.config['auth'])
        m = Model(r.json())
        return m

    def update(self, **kwargs):
        self.create(**kwargs)

    def delete(self):
        print 'DELETE', self.url

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        return Resource('%s%s/' % (self.url, name), name, config=self.config)

    def __getitem__(self, name):
        if isinstance(name, dict):
            params = name
            filtered = Resource(self.url, self.name, params, self.config)
            return filtered
        elif isinstance(name, slice):
            params = name.start or {}
            if name.stop:
                params['page'] = name.stop
            if slice.step:
                params['per_page'] = name.step

            filtered = Resource(self.url, self.name, params, self.config)
            return filtered
        else:
            return self.__getattr__(name)

    def __call__(self, **kwargs):
        if self.name is None:
            raise RuntimeError('Cannot call directly on root')
        r = requests.get(self.url[:-1], params=kwargs,
                         auth=self.config['auth'])
        return r.json()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '<Resource: %s>' % self.url

    def __iter__(self):
        r = requests.get(self.url[:-1], params=self.params,
                         auth=self.config['auth'])
        for x in r.json():
            yield Model(x)
        while 'next' in r.links and r.links['next']['url']:
            r = requests.get(r.links['next']['url'], auth=self.config['auth'])
            for x in r.json():
                yield Model(x)


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
            url = self._parse_name(name)
            self.env[name] = Resource("https://%s" % url)
        return self.env[name]

    def _parse_name(self, name):
        parts = name.split('__')
        url = parts[0].replace('_', '.')
        prefix = '/'
        if len(parts) > 1:
            prefix = parts[1].replace('_', '/')
        return "%s%s" % (url, prefix)


if __name__ != "__main__":
    self = sys.modules[__name__]
    sys.modules[__name__] = SelfWrapper(self)
