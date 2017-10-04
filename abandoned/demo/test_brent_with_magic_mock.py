import pytest
import mock
from parsers.getter.brent import fetch

@pytest.fixture
def foo_obj(**kwargs):
    """
    This is fixture which is very helpfull to create empty object with arguments.
    :param kwargs: The kwargs is a arguments of empty object.
    :return: Empty object
    """
    return type('', (object,), kwargs)()


def test_fetch(mocker):
    return_value = foo_obj(**{"text": 'some_text'})
    mocker.patch('requests.get', mock.MagicMock(return_value=return_value))
    assert fetch('some_url') == 'some_text'
    
#FIXME: fails with:
    
#file C:\Users\Евгений\Documents\GitHub\parser-template\parsers\getter\tests\test_brent_with_magic_mock.py, line 15
#  def test_fetch(mocker):
#E       fixture 'mocker' not found
                
   
if __name__ == "__main__":
    pytest.main([__file__])
                        