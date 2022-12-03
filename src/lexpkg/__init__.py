"""import lexpkg"""
# Configure behavior of "import lexpkg"
# Enabled by default: lexpkg.module or lexpkg.subpkg

# Enable lexpkg.module.<module objects> and lexpkg.<module objects>
from lexpkg.subpkg import module
from lexpkg.subpkg.module import MY_VARIABLE, MyClass, my_function

__all__ = ["module", "MY_VARIABLE", "MyClass", "my_function"]
