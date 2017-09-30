import pytest

@pytest.fixture
def foo_obj(**kwargs):
    foo_obj = type('', (object,), {})()
    for name, value in kwargs.items():
        setattr(foo_obj, name, value)
    return foo_obj
