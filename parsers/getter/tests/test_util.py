import pytest
import requests_mock
from decimal import Decimal
from parsers.getter.util import (fetch,
                                 format_date,
                                 format_value)

class Test_fetch:
    def test_fetch_good_response(self):
        url = "http://www.testpage.com"
        with requests_mock.mock() as mocked_content:
            mocked_content.get(url, text="good response from url")
            assert fetch(url) == 'good response from url'

    def test_fetch_with_non_readable_URL_raises_ValueError(self):
        url = "http://www.testpage.com"
        with requests_mock.mock() as mocked_content:
            with pytest.raises(ValueError):
                mocked_content.get(url, text="Error reponse")
                fetch(url)

    def test_fetch_returns_Error_in_parameters_raises_Exception(self):
        url = "http://www.testpage.com"
        with requests_mock.mock() as mocked_content:
            with pytest.raises(Exception):
                mocked_content.get(url, text="Error in parameters")
                fetch(url)

class Test_format_date:
    def test_format_date_with_valid_date_string(self):
        assert format_date('2017-01-04T00:00:00', fmt='%Y-%m-%dT%H:%M:%S') == '2017-01-04'
        assert format_date('20170104', fmt="%Y%m%d") == '2017-01-04'

    def test_format_date_with_invalid_date_string_raises_ValueError(self):
        with pytest.raises(ValueError):
            format_date('bad_date_format', fmt='%Y-%m-%dT%H:%M:%S')
        with pytest.raises(ValueError):
            format_date('bad_date_format', fmt="%Y%m%d")

    def test_format_date_with_None_raises_TypeError(self):
        with pytest.raises(TypeError):
            format_date(None, fmt='%Y-%m-%dT%H:%M:%S')
        with pytest.raises(TypeError):
            format_date(None, fmt="%Y%m%d")

class Test_format_value:
    def test_format_value_with_valid_parameters(self):
        assert format_value('2.26') == Decimal('2.26')

    def test_format_value_with_invalid_parameters(self):
        with pytest.raises(ValueError):
            format_value(['123,56','something'])

    def test_format_value_with_None_parameter(self):
        with pytest.raises(TypeError):
            format_value(None)
