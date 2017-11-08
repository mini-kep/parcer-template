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


def test_parse_valid_xml_with_null():
    gen = parse_xml("""<?xml ><pre>
    <entry xmlns="http://www.w3.org/2005/Atom">
        <content type="application/xml">
            <m:properties xmlns:m="http://schemas.microsoft.com/ado/2007/08/dataservices/metadata">
                <d:Id xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" m:type="Edm.Int32">3458</d:Id>
                <d:NEW_DATE xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" m:type="Edm.DateTime">2010-10-11T00:00:00</d:NEW_DATE>
                <d:BC_1MONTH xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" m:type="Edm.Double" m:null="true"/>
                <d:BC_3MONTH xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" m:type="Edm.Double" m:null="true"/>
                <d:BC_6MONTH xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" m:type="Edm.Double" m:null="true"/>
                <d:BC_1YEAR xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" m:type="Edm.Double" m:null="true"/>
                <d:BC_2YEAR xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" m:type="Edm.Double" m:null="true"/>
                <d:BC_3YEAR xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" m:type="Edm.Double" m:null="true"/>
                <d:BC_5YEAR xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" m:type="Edm.Double" m:null="true"/>
                <d:BC_7YEAR xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" m:type="Edm.Double" m:null="true"/>
                <d:BC_10YEAR xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" m:type="Edm.Double" m:null="true"/>
                <d:BC_20YEAR xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" m:type="Edm.Double" m:null="true"/>
                <d:BC_30YEAR xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" m:type="Edm.Double" m:null="true"/>
                <d:BC_30YEARDISPLAY xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" m:type="Edm.Double">0</d:BC_30YEARDISPLAY>
            </m:properties>
        </content>
    </entry></pre>
    """)
    l = list(gen)
    assert len(l) == 1
    assert l[0]['date'] == '2010-10-11'
    assert l[0]['value'] == Decimal('0')
    assert l[0]['freq'] == 'd'
    assert l[0]['name'] == 'UST_30YEARDISPLAY'


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
