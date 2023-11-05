#!/usr/bin/env python
"""Example of developer script."""

# 1st party
import lexpkg


def main():
    print("Hello from lexpkg developer script")
    print(f"{__file__           = }")
    print(f"{__name__           = }")
    print(f"{lexpkg.__version__ = }")
    print(f"{lexpkg.PACKAGE_DIR = !s}")
    print(f"{lexpkg.SRC_DIR     = !s}")


if __name__ == "__main__":
    main()
