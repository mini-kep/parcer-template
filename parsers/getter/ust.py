import json
import requests
from datetime import datetime
import bs4

def get_date(string):
    dt = datetime.strptime(string, '%Y-%m-%dT%H:%M:%S')
    return dt.strftime('%Y-%m-%d')

def make_url(year):
    """Creates Web Url based on the given year"""
    cur_year = datetime.today().year
    if year not in [x for x in range(1990, cur_year + 1)]:
        raise ValueError("Given year is not from year interval (1990 - "+str(cur_year)+")")
    else:
        return ("https://www.treasury.gov/resource-center/"
                "data-chart-center/interest-rates/pages/"
                "XmlView.aspx?data=yieldyear&year={}".format(year))

def fetch(url):
    """Fetch content from given url."""
    content = requests.get(url)
    if "Error" in content.text:
        raise ValueError("Cannot read {} from web. Try again later.".format(year))
    else:
        return content.text

def yield_ust_dict(year,downloader=fetch,period='UST_1M'):
    """
    Yeild Monthly UST datapoints ad dict
    """
    url = make_url(year)
    content = downloader(url)
    soup = bs4.BeautifulSoup(content, "xml")
    properties = soup.find_all('properties')
    for prop in properties:
        date = get_date(prop.find('NEW_DATE').text)
        if period == 'UST_1M':
            price = prop.BC_1MONTH.text
        elif period == 'UST_1Y':
            price = prop.BC_1YEAR.text
        else:
            raise ValueError("Wrong period > Periods only available: "
                             "UST_1M, UST_1Y")
        yield { "date" : date,
                "freq": "d",
                "name": period,
                "value": price}


gen = yield_ust_dict(2010)
for g in gen:
    print(g)
