"""
LexPkg
=======

Configure behavior of "import lexpkg"
Behavior enabled by default when adding __init__.py:
    >> lexpkg.add
    >> lexpkg.subpkg

"""

# Enable lexpkg.module.<module objects> and lexpkg.<module objects>
from lexpkg.subpkg import module
from lexpkg.subpkg.module import MY_VARIABLE, MyClass, my_function

__all__ = ["module", "MY_VARIABLE", "MyClass", "my_function"]
