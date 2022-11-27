import doctest
import pkgutil

import lexpkg

path = lexpkg.__path__
prefix = lexpkg.__name__ + "."


def load_tests(loader, tests, pattern):
    for _, name, ispkg in pkgutil.walk_packages(path, prefix):
        tests.addTests(doctest.DocTestSuite(name))
    return tests


if __name__ == "__main__":
    for importer, name, ispkg in pkgutil.walk_packages(path, prefix):
        print(f"{name} [{ispkg=}]\n\t{importer = }")
