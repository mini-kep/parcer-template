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
import bs4
from datetime import date
from time import time         
           
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


def parse_xml(content: str):
    result = parse_xml_raw(content)
    # exclude date 2017-04-14
    return [d for d in result if d['date'] != '2017-04-14'] 


# TODO: can elapsed time be calculated in a lcass method decorator?

class Getter(object):
    """Datapoints from US Treasury. Behaves as list after .extract() call."""
                                                                  
    def __init__(self, start_date, end_date, downloader=util.fetch):
        # FIXME: in this parser we may restrict period to one year only
        #        raise error when end_date - start_date  > 1 year 
        self.start_date, self.end_date = start_date, end_date
        self.response = None
        self.elapsed = None
        self.parsing_result = []
        self.downloader = downloader
    
    @property
    def url(self):
        raise NotImplementedError
        #return make_url(make_year(self.start_date))
    
    def extract(self):
        start_time = time() 
        self.response = self.downloader(self.url)
        self.parsing_result = None
        raise NotImplementedError
        self.elapsed = round(time() - start_time , 1)
        return self
        
    # 'magics' to make this class behave like a list 
    def __getitem__(self, i):
        if self.parsing_result:
            return self.parsing_result[i]
        return None

    def __len__(self):
        return len(self.parsing_result)

                  
# FIXME: in this parser we may restrict period to one year only
#        raise error when end_date - start_date  > 1 year 
class UST(object):
    """Datapoints from US Treasury. Behaves as list after .extract() call."""
                                                                  
    def __init__(self, start_date, end_date, downloader=util.fetch):
        self.start_date, self.end_date = start_date, end_date
        self.response = None
        self.elapsed = None
        self.parsing_result = []
        self.downloader = downloader
    
    @property
    def url(self):
        return make_url(make_year(self.start_date))
    
    def extract(self):
        start_time = time() 
        self.response = self.downloader(self.url)
        self.parsing_result = list(parse_xml(self.response))
        self.elapsed = round(time() - start_time, 1)
        return self
        
    # 'magics' to make this class behave like a list 
    def __getitem__(self, i):
        if self.parsing_result:
            return self.parsing_result[i]
        return None

    def __len__(self):
        return len(self.parsing_result)
    