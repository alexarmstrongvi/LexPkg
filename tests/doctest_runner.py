import doctest
import pkgutil

import lexpkg

PATH = lexpkg.__path__
PREFIX = lexpkg.__name__ + "."


def load_tests(loader, tests, pattern):
    del loader, pattern  # Unused
    for _, name, _ in pkgutil.walk_packages(PATH, PREFIX):
        tests.addTests(doctest.DocTestSuite(name))
    return tests


def main():
    for importer, name, ispkg in pkgutil.walk_packages(PATH, PREFIX):
        print(f"{name} [{ispkg=}]\n\t{importer = }")


if __name__ == "__main__":
    main()
