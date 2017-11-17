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

from datetime import datetime
import parsers.getter.util as util
import bs4


def valid_years():
    cur_year = datetime.today().year
    return list(range(1990, cur_year + 1))                       

def make_year(start_date):
    """Extract year form *start_date*

    Args:
       start_date(datetime.date)
    Retruns:
        year as (int)
    """
    year = start_date.year
    cur_year = datetime.today().year
    if year not in valid_years():
        raise ValueError(f"<{year}> not in [1990, {cur_year}]")
    return year


def make_url(year):
    """Create urls based on *year*."""
    return ("https://www.treasury.gov/resource-center/"
            "data-chart-center/interest-rates/pages/"
            "XmlView.aspx?data=yieldyear&year={}".format(year))


def extract_date(date_str):
    """Returns string like '2017-04-14'."""
    return util.format_date(date_str, fmt='%Y-%m-%dT%H:%M:%S')


def parse_xml_raw(content: str):
    soup = bs4.BeautifulSoup(content, "xml")
    properties = soup.find_all('properties')
    content = [{"date": extract_date(prop.find('NEW_DATE').text),
                "freq": "d",
                "name": child.name.replace("BC_", "UST_"),
                "value": util.format_value(child.text)}
                 for prop in properties
                 for child in prop.findChildren()
                 if child.name.startswith('BC_') and child.text]
    return content


def parse_xml(content: str):
    exclude_date = '2017-04-14' 
    return [d for d in parse_xml_raw(content) if d['date'] != exclude_date] 


# IDEA: maybe add a vaidation decorator for all getter fucntions?
def get_ust_dict(start_date, downloader=util.fetch):
    """Return UST datapoints as list of dictionaries, based on *start_date*."""
    year = make_year(start_date)
    url = make_url(year)
    content = downloader(url)
    return parse_xml(content)

# ERROR: an start_Date - loads just one year, not all years from that date on

