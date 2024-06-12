import os
import ccxt.static_dependencies.toolz as toolz

d = os.path.dirname(toolz.__file__)
version_ = os.path.join(d, '__init__.py')

if os.path.exists(version_):
    print("exists")
    os.remove(toolz.__file__)
