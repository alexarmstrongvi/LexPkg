"""Dummy module with dummy objects to illustrate importing"""

MY_VARIABLE = "module-scoped variable"


def my_function() -> None:
    """Dummy function"""
    return


class MyClass:
    """Dummy class"""

    def __init__(self, attribute=None):
        self.attribute = attribute

    def true(self) -> bool:
        """Dummy true method"""
        return True

    def false(self) -> bool:
        """Dummy false method"""
        return False
