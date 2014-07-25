class Entity(dict):
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
            return super(Entity, self).__getattr__(name)

    def __setattr__(self, name, value):
        if isinstance(value, dict) and name[0:2] != '__':
            self.__dict__[name] = Entity(value)
        else:
            super(dict, self).__setattr__(name, value)
