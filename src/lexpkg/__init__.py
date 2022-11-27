"""import lexpkg"""
# Configure behavior of "import lexpkg"
# Enabled by default: lexpkg.subpkg.module.<module objects> (given subpkg has __init__.py)

# Enable lexpkg.module.<module objects> and lexpkg.<module objects>
from lexpkg.subpkg import module
from lexpkg.subpkg.module import MY_VARIABLE, MyClass, my_function
