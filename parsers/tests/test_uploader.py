import pytest
from decimal import Decimal

from parsers.uploader import convert_decimal_to_float, to_json, upload_to_database


def test_convert_decimal_to_float_return_float():
    decimal_number = Decimal(1)
    assert convert_decimal_to_float(decimal_number) == float(decimal_number)


# FIXME: refine test to close to actual data
# https://docs.pytest.org/en/latest/parametrize.html#pytest-mark-parametrize-parametrizing-test-functions
@pytest.mark.parametrize("gen,s", [
    (iter([Decimal(1.01)]), '[1.01]'),
    ([Decimal('1.0100000000000000088817841970012523233890533447265625')], '[1.01]'),
    ])
def test_to_json(gen, s):
    assert to_json(gen) == s
                          
       
def test_upload_to_database_returns_code_200():
    class MockResponse:
        status_code = 200
    
    def mock_post(*arg, **kwarg):        
        return MockResponse()
    
    gen = iter([1,2,3])
    assert upload_to_database(gen, upload_func=mock_post)    


if __name__ == '__main__':
    pytest.main([__file__])
