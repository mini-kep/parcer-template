import pytest

import arrow
import random 
from datetime import date
from decimal import Decimal


import parsers.getter.ust as ust
from parsers.getter.ust import parse_xml


def test_VALID_YEARS():
    assert ust.VALID_YEARS[0] == 1990
    assert ust.VALID_YEARS[-1] >= 2017                      

class Test_make_year:
    def test_make_year_on_good_date(self):
        assert ust.make_year(date(2017, 1, 1)) == 2017

    def test_make_year_on_year_out_of_range_raises_ValueError(self):
        with pytest.raises(ValueError):
            ust.make_year(date(1965, 1, 1))

    def test_make_year_on_Non_date_parameter_raises_AttributeError(self):
        with pytest.raises(AttributeError):
            ust.make_year(None)

def test_make_url():
    year = 2000
    url = ust.make_url(year)
    assert str(year) in url
    assert url.startswith("http")


def test_extract_date():
    assert ust.extract_date('2017-01-03T00:00:00') == \
                       arrow.get('2017-01-03').format('YYYY-MM-DD')

# WARNING: space in <?xml > is critical
XML_DOC_1 = ('<?xml ><pre>'
             '<m:properties>'
             '<d:NEW_DATE>2017-01-03T00:00:00</d:NEW_DATE>'
             '<d:BC_1MONTH>0.52</d:BC_1MONTH>')


def generate_xml(date, value, key='1MONTH'):
    return ('<?xml ><pre><m:properties>'
            f'<d:NEW_DATE>{date}T00:00:00</d:NEW_DATE>'
            f'<d:BC_{key}>{value}</d:BC_{key}>')
    

def test_selftest_generate_xml():
    assert generate_xml('2017-01-03', '0.52') == XML_DOC_1


def test_parse_xml_returns_list():
    assert isinstance(parse_xml(''), list)
    

def test_parse_xml_with_valid_xml_input():
    gen = parse_xml(XML_DOC_1)
    d = gen[0]
    assert d['date'] == '2017-01-03'
    assert d['value'] == Decimal('0.52')
    assert d['freq'] == 'd'
    assert d['name'] == 'UST_1MONTH'
                   
            
def test_parse_xml_on_skipped_value():
    result = parse_xml("""<?xml ><pre>
               <m:properties>
               <d:NEW_DATE>2017-01-03T00:00:00</d:NEW_DATE>
               <d:BC_1MONTH></d:BC_1MONTH>""")         
    assert len(result) == 0   
    
def test_parse_xml_on_skipped_value_by_gen():
    xml_str = generate_xml('2017-01-03', '', key='1MONTH')
    result = parse_xml(xml_str)         
    assert len(result) == 0   

def test_parse_xml_on_UST_30YEARDISPLAY_returns_None():
    xml_str = generate_xml('2017-01-03', '', key='1MONTH')
    result = parse_xml(xml_str)         
    assert len(result) == 0   

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
    result = parse_xml(xml_doc)
    assert len(result) >= 1

def fake_fetch(url):
    return XML_DOC_1

def test_UST_on_fake_fetch():
    u = ust.UST(2017, None, download_func=fake_fetch)
    u.extract()
    d = u.items[0]
    assert d['date'] == '2017-01-03'
    assert d['value'] == Decimal('0.52')
    assert d['freq'] == 'd'
    assert d['name'] == 'UST_1MONTH'


# FIXME: split into two tests
@pytest.mark.webtest
def test_UST_on_real_call():
    u = ust.UST(2017, None)
    assert not u.items
    u.extract()
    assert u.items[0] == {'date': '2017-01-03',
                    'freq': 'd',
                    'name': 'UST_1MONTH',
                    'value': Decimal('0.52')}


@pytest.mark.webtest
@pytest.mark.skip("This will test runs too long")
def test_UST_on_randomised_year_reads_whole_year_data():    
    year = random.choice(ust.VALID_YEARS)
    p = ust.UST(year, None)
    p.extract()
    assert len(p.items) >= 1

# TODO: make test with actual datapoints    
#   {'date': '2017-01-03', 'freq': 'd', 'name': 'UST_30YEAR', 'value': 3.04},
#   {'date': '2017-09-18', 'freq': 'd', 'name': 'UST_1MONTH', 'value': 55.5},
#   {'date': '2017-09-15', 'freq': 'd', 'name': 'UST_1MONTH', 'value': 56.18},


if __name__ == "__main__":
    pytest.main([__file__, "--maxfail=1"])
