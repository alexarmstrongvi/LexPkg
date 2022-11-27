from lexpkg.subpkg import multiply


def test_multiply_by_six():
    assert multiply.multiply_by_six(3) == 18
