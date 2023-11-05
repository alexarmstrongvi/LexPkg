"""
LexPkg
=======
An example packaged python project

"""
# NOTE: lexpkg/__init__.py configures behavior of "import lexpkg". An empty
# __init__.py is often sufficient as it allows all modules (i.e. *.py
# files) and subpackages (i.e. directories with __init.__py) within the lexpkg
# directory to be imported
# >> import lexpkg.add    # import module
# >> import lexpkg.subpkg # import sub-package

# Standard library
from pathlib import Path

# 1st party
from lexpkg.subpkg import module
from lexpkg.subpkg.module import MY_VARIABLE, MyClass, my_function

__all__ = [
    "__version__",
    "PACKAGE_DIR",
    "SRC_DIR",
    "module",
    "MY_VARIABLE",
    "MyClass",
    "my_function",
]

# Globals
__version__ = "0.0.1"
PACKAGE_DIR = Path(__file__).parents[2]
SRC_DIR = PACKAGE_DIR / "src/lexpkg"  # same as Path(__path__[0])
