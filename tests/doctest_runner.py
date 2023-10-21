#!/usr/bin/env python
"""Module running doctest on all source files"""
import doctest
import pkgutil
from typing import Optional
from unittest import TestLoader, TestSuite

import lexpkg

PATH = lexpkg.__path__
PREFIX = lexpkg.__name__ + "."


def load_tests(
    loader: TestLoader, tests: TestSuite, pattern: Optional[str]
) -> TestSuite:
    """Load doctests for each source file"""
    del loader, pattern  # Unused
    for _, name, _ in pkgutil.walk_packages(PATH, PREFIX):
        tests.addTests(doctest.DocTestSuite(name))
    return tests


def main():
    """Print packages found by pkgutil"""
    for importer, name, ispkg in pkgutil.walk_packages(PATH, PREFIX):
        print(f"{name} [{ispkg=}]\n\t{importer=}")


if __name__ == "__main__":
    main()
