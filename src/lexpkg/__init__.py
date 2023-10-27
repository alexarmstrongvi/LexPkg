"""
LexPkg
=======

Configure behavior of "import lexpkg"
Behavior enabled by default when adding __init__.py:
    >> lexpkg.add
    >> lexpkg.subpkg

"""
from pathlib import Path

# Enable lexpkg.module.<module objects>
from lexpkg.subpkg import module
# Enable lexpkg.<module objects>
from lexpkg.subpkg.module import MY_VARIABLE, MyClass, my_function

SRC_DIR = Path(__file__).parent
PACKAGE_DIR = SRC_DIR.parents[1]

__all__ = [
    "module",
    "SRC_DIR",
    "PACKAGE_DIR",
    "MY_VARIABLE",
    "MyClass",
    "my_function",
]
