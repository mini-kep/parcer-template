import pytest
from decimal import Decimal

from parsers.uploader import convert_decimal_to_float, to_json, upload_datapoints


def test_convert_decimal_to_float_return_float():
    decimal_number = Decimal(1)
    assert convert_decimal_to_float(decimal_number) == float(decimal_number)

    
def test_convert_decimal_to_float_raises_exception():
    non_decimal_number = 'abc'
    with pytest.raises(Exception):
        convert_decimal_to_float(non_decimal_number)
    

# FIXME: refine test to close to actual data
@pytest.mark.parametrize("gen,s", [
    ([Decimal('1.01')], '[1.01]'),
    ([Decimal('1.0100000000000000088817841970012523233890533447265625')], '[1.01]'),
    ])
def test_to_json(gen, s):
    assert to_json(gen) == s
                          
 
if __name__ == '__main__':
    pytest.main([__file__])
