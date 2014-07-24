import sys

from .magic import SelfWrapper


self = sys.modules[__name__]
sys.modules[__name__] = SelfWrapper(self)
