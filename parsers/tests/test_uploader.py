import pytest
import json
from decimal import Decimal

from parsers.uploader import convert_decimal_to_float, to_json


class Test_convert_decimal_to_float():
    def test_function_convert_decimal_to_float_return_float(self):
        decimal_number = Decimal(1)
        assert convert_decimal_to_float(decimal_number) == float(decimal_number)


class Test_convert_gen_object_to_json():
    def test_function_convert_decimal_to_float_return_float(self):
        #TODO add gen and expected result for comparision
        gen = ''
        expected_result = ''
        """
        result = json.dumps(list(gen), default=convert_decimal_to_float)
        assert result ==  expected_result
        """


class Test_upload_to_database():
    def test_function_upload_to_database_returns_code_200(self):
        pass


if __name__ == '__main__':
    pytest.main([__file__])
