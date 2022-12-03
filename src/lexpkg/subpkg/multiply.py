"""Example module in subpackage"""


def multiply_by_six(num: float) -> float:
    """Multiply the input number by six

    >>> multiply_by_six(3)
    18
    >>> multiply_by_six(3.1)
    18.6
    """
    return num * 6


def multiply_by_two(num: float) -> float:
    """Multiply the input number by two

    >>> multiply_by_two(3)
    6
    >>> multiply_by_two(3.1)
    6.2
    """
    return num * 2
