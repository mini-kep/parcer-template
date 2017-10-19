import pytest
import json
from decimal import Decimal

from parsers.uploader import convert_decimal_to_float, to_json


class Test_convert_decimal_to_float():
    def test_function_convert_decimal_to_float_return_float(self):
        #TODO test on something bad-loooking like 1.0999999999
        decimal_number = Decimal(1)
        assert convert_decimal_to_float(decimal_number) == float(decimal_number)


class Test_convert_gen_object_to_json():
    def test_on_iterable_with_Decimal_returns_string(self):
        #FIXME refine test to close to actual data
        gen_sample = iter([Decimal(1.01)])
        assert to_json(gen=gen_sample) == '[1.01]'
        """
        result = json.dumps(list(gen), default=convert_decimal_to_float)
        assert result ==  expected_result
        """
#
#str(Decimal(1.01))
#Out[22]: '1.0100000000000000088817841970012523233890533447265625'
        
        
class Test_upload_to_database():
    def test_function_upload_to_database_returns_code_200(self):
        #TODO write test here
        pass


if __name__ == '__main__':
    pytest.main([__file__])
