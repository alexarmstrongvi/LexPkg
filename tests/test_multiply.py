"""Test multiply module."""
# 1st party
from lexpkg.subpkg import multiply


def test_multiply_by_six():
    """Test multiply_by_six() method on different number types."""
    assert multiply.multiply_by_six(3) == 18
