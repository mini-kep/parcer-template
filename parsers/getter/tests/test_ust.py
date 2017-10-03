import pytest
from datetime import date, datetime
import requests_mock
from decimal import Decimal
from parsers.getter.ust import (make_year,
                                make_url,
                                fetch,
                                format_value,
                                get_date,
                                rename_variable,
                                parse_xml,
                                yield_ust_dict)

#fixture

def fake_content():
    return """<?xml version="1.0" encoding="utf-8" standalone="yes"?><pre>
                <m:properties>
                <d:NEW_DATE>2017-01-03T00:00:00</d:NEW_DATE>
                <d:BC_1MONTH>0.52</d:BC_1MONTH>"""

def fake_fetch(url=None):
    return """<?xml version="1.0" encoding="utf-8" standalone="yes"?><pre>
                <m:properties>
                <d:NEW_DATE>2017-01-03T00:00:00</d:NEW_DATE>
                <d:BC_1MONTH>0.52</d:BC_1MONTH>"""

class Test_make_year:
    def test_make_year_with_good_date(self):
        assert make_year(date(2017, 1, 1)) == 2017

    def test_make_year_with_year_out_of_range_raises_ValueError(self):
        with pytest.raises(ValueError):
            make_year(date(1989, 1, 1))

    def test_make_year_with_Non_date_parameter_raises_AttributeError(self):
        with pytest.raises(AttributeError):
            make_year(None)

def test_make_url():
    year = 1850
    url = make_url(year)
    assert str(year) in url
    assert url.startswith("http")

class Test_fetch:
    def test_fetch_good_response(self):
        url = "http://www.testpage.com"
        with requests_mock.mock() as mocked_content:
            mocked_content.get(url, text="good response from url")
            assert fetch(url) == 'good response from url'

    def test_fetch_error_response_raises_ValueError(self):
        url = "http://www.testpage.com"
        with requests_mock.mock() as mocked_content:
            with pytest.raises(ValueError):
                mocked_content.get(url, text="Error reponse")
                fetch(url)

def test_format_value():
    assert format_value('2.2600') == Decimal('2.2600')

class Test_get_date:
    def test_get_date_with_valid_date_string(self):
        assert get_date('2017-01-04T00:00:00') == '2017-01-04'

    def test_get_date_with_invalid_date_string_raises_ValueError(self):
        with pytest.raises(ValueError):
            get_date('bad_date_format')

    def test_get_date_with_None_raises_TypeError(self):
        with pytest.raises(TypeError):
            get_date(None)

def test_rename_variable_with_valid_varname():
    assert rename_variable("BC_Something") == 'UST_Something'

def test_parse_xml_with_valid_xml_input():
    fake_c = fake_content()
    gen = parse_xml(fake_c)
    d = next(gen)
    assert d['date'] == '2017-01-03'
    assert d['value'] == Decimal('0.52')
    assert d['freq'] == 'd'
    assert d['name'] == 'UST_1MONTH'


def test_yield_ust_dic():
    start_date = date(2017, 1, 1)
    fake_f = fake_fetch()
    gen = yield_ust_dict(start_date,fake_fetch)
    d = next(gen)
    assert d['date'] == '2017-01-03'
    assert d['value'] == Decimal('0.52')
    assert d['freq'] == 'd'
    assert d['name'] == 'UST_1MONTH'

if __name__ == "__main__":
    pytest.main([__file__])
