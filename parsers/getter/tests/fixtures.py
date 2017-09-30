import pytest

@pytest.fixture
def foo_obj(**kwargs):
    return type('', (object,), kwargs)()


