"""Import interest rates for US treasuries for different bond durations.

Yield a stream of datapoint dictionaries like:
{'date': '2017-01-03', 'freq': 'd', 'name': 'UST_1MONTH', 'value': Decimal('0.5200')}
{'date': '2017-01-03', 'freq': 'd', 'name': 'UST_3MONTH', 'value': Decimal('0.5300')}
{'date': '2017-01-03', 'freq': 'd', 'name': 'UST_6MONTH', 'value': Decimal('0.6500')}
{'date': '2017-01-03', 'freq': 'd', 'name': 'UST_1YEAR', 'value': Decimal('0.8900')}
{'date': '2017-01-03', 'freq': 'd', 'name': 'UST_2YEAR', 'value': Decimal('1.2200')}
{'date': '2017-01-03', 'freq': 'd', 'name': 'UST_3YEAR', 'value': Decimal('1.5000')}
{'date': '2017-01-03', 'freq': 'd', 'name': 'UST_5YEAR', 'value': Decimal('1.9400')}
{'date': '2017-01-03', 'freq': 'd', 'name': 'UST_7YEAR', 'value': Decimal('2.2600')}
{'date': '2017-01-03', 'freq': 'd', 'name': 'UST_10YEAR', 'value': Decimal('2.4500')}
{'date': '2017-01-03', 'freq': 'd', 'name': 'UST_20YEAR', 'value': Decimal('2.7800')}
{'date': '2017-01-03', 'freq': 'd', 'name': 'UST_30YEAR', 'value': Decimal('3.0400')}
{'date': '2017-01-03', 'freq': 'd', 'name': 'UST_30YEARDISPLAY', 'value': Decimal('3.0400')}
"""

from datetime import datetime, date
from decimal import Decimal

import bs4
import requests


def make_year(start_date):
    """Extract year form *start_date*

    Args:
       start_date(datetime.date)
    Retruns:
        year as (int)
    """
    year = start_date.year
    cur_year = datetime.today().year
    if year not in [x for x in range(1990, cur_year + 1)]:
        raise ValueError(f"Year <{year}> must be in [1990, {cur_year}] range.")
    return year

def make_url(year):
    """Create urls based on *year*."""
    return ("https://www.treasury.gov/resource-center/"
            "data-chart-center/interest-rates/pages/"
            "XmlView.aspx?data=yieldyear&year={}".format(year))

def fetch(url):
    """Fetch content from *url* from internet."""
    content = requests.get(url).text
    if "Error" in content:
        raise ValueError(f"Cannot read from URL <{url}>")
    return content

#FIXME: this can be a importable util in the project
def format_value(value_string: str):
    return round(Decimal(value_string), 4)


def get_date(string):
    dt = datetime.strptime(string, '%Y-%m-%dT%H:%M:%S')
    return dt.strftime('%Y-%m-%d')


def rename_variable(varname):
    return varname.replace("BC_", "UST_")


def parse_xml(content: str):
    soup = bs4.BeautifulSoup(content, "xml")
    properties = soup.find_all('properties')
    for prop in properties:
        date = get_date(prop.find('NEW_DATE').text)
        children = prop.findChildren()
        for child in children:
            if child.name.startswith('BC_'):
                price = format_value(child.text)
                name = rename_variable(child.name)
                yield { "date" : date,
                        "freq": "d",
                        "name": name,
                        "value": price}


def yield_ust_dict(start_date,downloader=fetch):
    """
    Yeild UST datapoints as dict
    """
    year = make_year(start_date)
    url = make_url(year)
    content = downloader(url)
    return parse_xml(content)


if __name__ == "__main__":
    s = date(2017, 1, 1)
    gen = yield_ust_dict(s)
    for i in range(14):
       print(next(gen))
