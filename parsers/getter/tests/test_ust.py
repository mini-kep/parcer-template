import arrow
import pytest
from datetime import date
from decimal import Decimal
from parsers.getter.ust import (make_year,
                                make_url,
                                parse_xml,
                                get_ust_dict,
                                extract_date)


class Test_make_year:
    def test_make_year_on_good_date(self):
        assert make_year(date(2017, 1, 1)) == 2017

    def test_make_year_on_year_out_of_range_raises_ValueError(self):
        with pytest.raises(ValueError):
            make_year(date(1965, 1, 1))

    def test_make_year_on_Non_date_parameter_raises_AttributeError(self):
        with pytest.raises(AttributeError):
            make_year(None)

def test_make_url():
    year = 2000
    url = make_url(year)
    assert str(year) in url
    assert url.startswith("http")

def test_extract_date():
    assert extract_date('2017-01-03T00:00:00') == \
                       arrow.get('2017-01-03').format('YYYY-MM-DD')

XML_DOC_1 = """<?xml ><pre>
               <m:properties>
               <d:NEW_DATE>2017-01-03T00:00:00</d:NEW_DATE>
               <d:BC_1MONTH>0.52</d:BC_1MONTH>"""

def test_parse_xml_with_valid_xml_input():
    gen = parse_xml(XML_DOC_1)
    d = gen[0]
    assert d['date'] == '2017-01-03'
    assert d['value'] == Decimal('0.52')
    assert d['freq'] == 'd'
    assert d['name'] == 'UST_1MONTH'
    
# testing on larger input            
def test_parse_xml_with_valid_xml_input_2():
    xml_doc = ("""<?xml ><pre>
    <entry xmlns="http://www.w3.org/2005/Atom">
        <content type="application/xml">
            <m:properties xmlns:m="http://schemas.microsoft.com/ado/2007/08/dataservices/metadata">
                <d:Id xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" m:type="Edm.Int32">3458</d:Id>
                <d:NEW_DATE xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" m:type="Edm.DateTime">2010-10-11T00:00:00</d:NEW_DATE>
                <d:BC_30YEARDISPLAY xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" m:type="Edm.Double">1.72</d:BC_30YEARDISPLAY>
            </m:properties>
        </content>
    </entry></pre>
    """)
    result = list(parse_xml(xml_doc))
    assert len(result) == 1
    assert result[0]['date'] == '2010-10-11'
    assert result[0]['value'] == Decimal('1.72')
    assert result[0]['freq'] == 'd'
    assert result[0]['name'] == 'UST_30YEARDISPLAY'


XML_14_APRIL_2017 = """<entry><id>http://data.treasury.gov/Feed.svc/DailyTreasuryYieldCurveRateData(6832)
</id><title type="text"/><updated>2017-11-08T21:11:43Z</updated><author><name/>
</author><link rel="edit" title="DailyTreasuryYieldCurveRateDatum" 
href="DailyTreasuryYieldCurveRateData(6832)"/>
<category term="TreasuryDataWarehouseModel.DailyTreasuryYieldCurveRateDatum" 
scheme="http://schemas.microsoft.com/ado/2007/08/dataservices/scheme"/>
<content type="application/xml"><m:properties><d:Id m:type="Edm.Int32">6832</d:Id>
<d:NEW_DATE m:type="Edm.DateTime">2017-04-14T00:00:00</d:NEW_DATE>
<d:BC_1MONTH m:type="Edm.Double">0</d:BC_1MONTH>
<d:BC_3MONTH m:type="Edm.Double">0</d:BC_3MONTH>
<d:BC_6MONTH m:type="Edm.Double">0</d:BC_6MONTH>
<d:BC_1YEAR m:type="Edm.Double">0</d:BC_1YEAR>
<d:BC_2YEAR m:type="Edm.Double">0</d:BC_2YEAR>
<d:BC_3YEAR m:type="Edm.Double">0</d:BC_3YEAR>
<d:BC_5YEAR m:type="Edm.Double">0</d:BC_5YEAR>
<d:BC_7YEAR m:type="Edm.Double">0</d:BC_7YEAR>
<d:BC_10YEAR m:type="Edm.Double">0</d:BC_10YEAR>
<d:BC_20YEAR m:type="Edm.Double">0</d:BC_20YEAR>
<d:BC_30YEAR m:type="Edm.Double">0</d:BC_30YEAR>
<d:BC_30YEARDISPLAY m:type="Edm.Double">0</d:BC_30YEARDISPLAY>
</m:properties></content></entry>
"""


def test_parse_valid_xml_with_zero_value_on_April_14_2017_is_exluded():
    xml_doc = (XML_14_APRIL_2017)
    result = parse_xml(xml_doc)
    assert len(result) == 0


def test_parse_valid_xml_with_zero_value_on_day_other_than_April_14_2017():
    xml_doc = ("""<?xml ><pre>
    <entry xmlns="http://www.w3.org/2005/Atom">
        <content type="application/xml">
            <m:properties xmlns:m="http://schemas.microsoft.com/ado/2007/08/dataservices/metadata">
                <d:Id xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" m:type="Edm.Int32">3458</d:Id>
                <d:NEW_DATE xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" m:type="Edm.DateTime">2010-10-11T00:00:00</d:NEW_DATE>
                <d:BC_30YEAR xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" m:type="Edm.Double">0</d:BC_30YEAR>
                <d:BC_30YEARDISPLAY xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" m:type="Edm.Double">0</d:BC_30YEARDISPLAY>
            </m:properties>
        </content>
    </entry></pre>
    """)
    result = list(parse_xml(xml_doc))
    assert len(result) >= 1

def fake_fetch(url=None):
    return XML_DOC_1

def test_get_ust_dic():
    start_date = date(2017, 1, 1)
    gen = get_ust_dict(start_date, downloader=fake_fetch)
    d = gen[0]
    assert d['date'] == '2017-01-03'
    assert d['value'] == Decimal('0.52')
    assert d['freq'] == 'd'
    assert d['name'] == 'UST_1MONTH'


if __name__ == "__main__":
    pytest.main([__file__, "--maxfail=1"])
