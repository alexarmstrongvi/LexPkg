# mypy: disable-error-code=truthy-function


def test_init():
    """Test importing objects from module"""
    # pylint: disable=import-outside-toplevel

    # Object import
    from lexpkg.subpkg.module import MY_VARIABLE, MyClass, my_function

    assert MY_VARIABLE
    assert my_function  # type: ignore
    assert MyClass

    # Module import
    from lexpkg.subpkg import module

    assert module.MY_VARIABLE
    assert module.my_function
    assert module.MyClass

    # Subpackage import
    from lexpkg import subpkg

    # if subpkg.module does not raise an attribute error, then anything
    # accessible from 'module' after 'from lexpkg.subpkg import module' is
    # accessible with subpkg.module
    assert subpkg.module
    assert subpkg.MY_VARIABLE
    assert subpkg.my_function
    assert subpkg.MyClass

    # Package import
    import lexpkg

    assert lexpkg.subpkg
    assert lexpkg.module
    assert lexpkg.MY_VARIABLE
    assert lexpkg.my_function
    assert lexpkg.MyClass

    # For 100% coverage
    assert my_function() is None
    my_class = MyClass()
    assert my_class.true()
    assert not my_class.false()
