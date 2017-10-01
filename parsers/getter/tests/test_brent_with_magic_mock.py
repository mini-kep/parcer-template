import pytest
import mock

from parsers.getter.tests.fixtures import foo_obj
from parsers.getter.brent import fetch

@pytest.fixture
def foo_obj(**kwargs):
    """
    This is fixture which is very helpfull to create empty object with arguments.
    :param kwargs: The kwargs is a arguments of empty object.
    :return: Empty object
    """
    return type('', (object,), kwargs)()


# EP: on me it fails with  fixture 'mocker' not found

#def test_fetch(mocker):
#    return_value = foo_obj(**{"text": 'some_text'})
#    mocker.patch('requests.get', mock.MagicMock(return_value=return_value))
#    assert fetch('some_url') == 'some_text'
    
                
   
if __name__ == "__main__":
    pytest.main([__file__])
                        