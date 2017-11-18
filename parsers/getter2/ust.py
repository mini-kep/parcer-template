"""Import interest rates for US treasuries at different durations.

Yield a stream of datapoint dictionaries like:

{'date': '2017-01-03', 'freq': 'd', 'name': 'UST_1MONTH', 'value': Decimal('0.52')}
{'date': '2017-01-03', 'freq': 'd', 'name': 'UST_3MONTH', 'value': Decimal('0.53')}
{'date': '2017-01-03', 'freq': 'd', 'name': 'UST_6MONTH', 'value': Decimal('0.65')}
{'date': '2017-01-03', 'freq': 'd', 'name': 'UST_1YEAR',  'value': Decimal('0.89')}
{'date': '2017-01-03', 'freq': 'd', 'name': 'UST_2YEAR',  'value': Decimal('1.22')}
{'date': '2017-01-03', 'freq': 'd', 'name': 'UST_3YEAR',  'value': Decimal('1.50')}
{'date': '2017-01-03', 'freq': 'd', 'name': 'UST_5YEAR',  'value': Decimal('1.94')}
{'date': '2017-01-03', 'freq': 'd', 'name': 'UST_7YEAR',  'value': Decimal('2.26')}
{'date': '2017-01-03', 'freq': 'd', 'name': 'UST_10YEAR', 'value': Decimal('2.45')}
{'date': '2017-01-03', 'freq': 'd', 'name': 'UST_20YEAR', 'value': Decimal('2.78')}
{'date': '2017-01-03', 'freq': 'd', 'name': 'UST_30YEAR', 'value': Decimal('3.04')}
{'date': '2017-01-03', 'freq': 'd', 'name': 'UST_30YEARDISPLAY', 'value': Decimal('3.04')}
"""

import parsers.getter.util as util
from parsers.ust.base import ParserBase

import bs4
from datetime import date
           
VALID_YEARS = list(range(1990, date.today().year + 1))   

def make_year(start_date):
    """Extract year form *start_date*

    Args:
       start_date(datetime.date)
    Retruns:
        year as (int)
    """
    year = start_date.year
    if year not in VALID_YEARS:
        raise ValueError(f"{year} not in {VALID_YEARS}")
    return year


def make_url(year):
    """Create urls based on *year*."""
    return ("https://www.treasury.gov/resource-center/"
            "data-chart-center/interest-rates/pages/"
            "XmlView.aspx?data=yieldyear&year={}".format(year))


def extract_date(date_str):
    """Returns string like '2017-04-14' from '2017-01-03T00:00:00'"""
    return util.format_date(date_str, fmt='%Y-%m-%dT%H:%M:%S')


def parse_xml_raw(content: str):
    soup = bs4.BeautifulSoup(content, "xml")
    properties = soup.find_all('properties')
    result = [{"date": extract_date(prop.find('NEW_DATE').text),
                "freq": "d",
                "name": child.name.replace("BC_", "UST_"),
                "value": util.format_value(child.text)}
                 for prop in properties
                 for child in prop.findChildren()
                 if child.name.startswith('BC_') and child.text]
    return result


def must_include(d):
    flag = True
    if (d['date'] == '2017-04-14' or
       d['name'] == 'UST_30YEARDISPLAY'):
       flag = False
    return flag    

assert must_include(dict(date='2017-04-14', name='UST_30YEARDISPLAY')) is False

def parse_xml(content: str):
    result = parse_xml_raw(content)
    return [d for d in result if must_include(d)] 

# FIXME: in this parser we may restrict period to one year only
#        raise error when end_date - start_date  > 1 year 
#        will disregars end dates beyond start +  1 year
         
class UST(ParserBase):
    """US Treasury bonds interest rates."""

    observation_start_date = '1990-01-01'
                                                                  
    @property
    def url(self):
        return make_url(make_year(self.start_date))
    
    # TODO: can response be binary?
    def parse_response(self, response):
        return parse_xml(response) 
    
if __name__ == '__main__':
   u = UST(2017)
   u.extract()
   print(len(u.items))
   assert u.items[0]
    
