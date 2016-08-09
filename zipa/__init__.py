import sys

from .module import register_module, ModuleImporter


if sys.version_info >= (3, 0):
    sys.meta_path.append(ModuleImporter(__name__))

register_module(__name__)
