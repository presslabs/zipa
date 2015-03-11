import sys

from .magic import SelfWrapper

__version__ = "0.2.0"


self = sys.modules[__name__]
sys.modules[__name__] = SelfWrapper(self)
