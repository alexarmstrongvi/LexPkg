"""Test add module."""
# 1st party
from lexpkg import add


def test_add_six():
    """Test add_six() method on different number types."""
    assert add.add_six(3) == 9
    assert add.add_six(3.1) == 9.1
    assert add.add_six(3j) == 6 + 3j
