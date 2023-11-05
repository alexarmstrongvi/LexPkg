"""Example of module level script.

NOTE: This file will be called if the following is run from the command line:
python -m lexpkg
Technically, a __main__.py file can be added to any directory with an
__init__.py and it will allow that module to be run as a script. For example,
python -m lexpkg.subpkg
is possible but this is rarely done.
The main use case is when your package is built around providing a single script
entrypoint (e.g. pip). For a utility package with multiple CLI scripts, put the
developer scripts in bin/ and put user scripts in src/lexpkg/bin/ and list
them as entrypoints in pyproject.toml
"""

# 1st party
from lexpkg.lexpkg import main

print("Hello from lexpkg module script")
print(f"{__file__ = }")
print(f"{__name__ = }")
main()
