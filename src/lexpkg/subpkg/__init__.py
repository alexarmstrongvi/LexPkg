"""
LexPkg subpackage

Configure behavior of "from lexpkg import subpkg"
Behavior enabled by default when adding __init__.py:
    >> subpkg.module.<module objects>
"""

# Enable subpkg.<module objects>
from lexpkg.subpkg.module import MY_VARIABLE, MyClass, my_function

__all__ = ["MY_VARIABLE", "MyClass", "my_function"]
