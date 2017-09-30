import pytest

@pytest.fixture
def foo_obj(**kwargs):
    """
    This is fixture which is very helpfull to create empty object with arguments.
    :param kwargs: The kwargs is a arguments of empty object.
    :return: Empty object
    """
    return type('', (object,), kwargs)()
