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

from datetime import datetime, date
import parsers.getter.util as util
import bs4


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


def parse_xml(content: str):
    soup = bs4.BeautifulSoup(content, "xml")
    properties = soup.find_all('properties')
    content = []
    for prop in properties:
        date_str = prop.find('NEW_DATE').text
        date = util.format_date(date_str, fmt='%Y-%m-%dT%H:%M:%S')
        children = prop.findChildren()
        for child in children:
            if child.name.startswith('BC_') and child.text != '':
                price = util.format_value(child.text)
                name = child.name.replace("BC_", "UST_")
                content.append({"date": date,
                       "freq": "d",
                       "name": name,
                       "value": price})
    return content


def get_ust_dict(start_date, downloader=util.fetch):
    """
    Yeild UST datapoints as dict
    """
    year = make_year(start_date)
    url = make_url(year)
    content = downloader(url)
    return parse_xml(content)


if __name__ == "__main__":
    s = date(2017, 1, 1)
    gen = get_ust_dict(s)
    for i in range(14):
        print(next(gen))
