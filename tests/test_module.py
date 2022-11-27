def test_init():
    """Test importing objects from module"""
    # pylint: disable=import-outside-toplevel

    # Object import
    from lexpkg.subpkg.module import MY_VARIABLE, my_function, MyClass

    assert MY_VARIABLE
    assert my_function
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
