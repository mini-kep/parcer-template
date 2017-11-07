import pytest
import bs4
from datetime import date
from decimal import Decimal
from parsers.getter.ust import (make_year,
                                make_url,
                                parse_xml,
                                yield_ust_dict)

@pytest.fixture
def fake_fetch(url=None):
    return """<?xml ><pre>
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
    year = 2000
    url = make_url(year)
    assert str(year) in url
    assert url.startswith("http")


def test_parse_xml_with_valid_xml_input(fake_fetch):
    gen = parse_xml(fake_fetch)
    d = next(gen)
    assert d['date'] == '2017-01-03'
    assert d['value'] == Decimal('0.52')
    assert d['freq'] == 'd'
    assert d['name'] == 'UST_1MONTH'


def test_parse_xml_with_valid_xml_input_with_null():
    gen = parse_xml("""<?xml ><pre>
                <m:properties>
                <d:NEW_DATE>2017-01-03T00:00:00</d:NEW_DATE>
                <d:BC_1MONTH m:null="true">
    """)
    d = next(gen)
    assert d['date'] == '2017-01-03'
    assert d['value'] is None
    assert d['freq'] == 'd'
    assert d['name'] == 'UST_1MONTH'


def test_yield_ust_dic():
    start_date = date(2017, 1, 1)
    gen = yield_ust_dict(start_date, downloader=fake_fetch)
    d = next(gen)
    assert d['date'] == '2017-01-03'
    assert d['value'] == Decimal('0.52')
    assert d['freq'] == 'd'
    assert d['name'] == 'UST_1MONTH'


if __name__ == "__main__":
    pytest.main([__file__])
