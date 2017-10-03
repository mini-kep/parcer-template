import json
import requests
from datetime import datetime, date
import bs4

def get_date(string):
    dt = datetime.strptime(string, '%Y-%m-%dT%H:%M:%S')
    return dt.strftime('%Y-%m-%d')

def make_year(s):
    """Parse Year from given start date""" 
    cur_year = datetime.today().year
    year = s.year
    if year not in [x for x in range(1990, cur_year + 1)]:
        raise ValueError("Given year is not from year interval (1990 - "+str(cur_year)+")")
    else:
        return year

def make_url(year):
    """Creates Web Url based on the given year"""
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

def yield_ust_dict(start_date,downloader=fetch):
    """
    Yeild UST datapoints as dict
    """
    year = make_year(start_date)
    url = make_url(year)
    content = downloader(url)
    soup = bs4.BeautifulSoup(content, "xml")
    properties = soup.find_all('properties')
    for prop in properties:
        date = get_date(prop.find('NEW_DATE').text)
        children = prop.findChildren()
        for child in children:
            if child.name.startswith('BC_'):
                price = child.text
                name = child.name
                yield { "date" : date,
                        "freq": "d",
                        "name": name,
                        "value": price}

if __name__ == "__main__":
    s = date(1991, 7, 1)
    gen = yield_ust_dict(s)
    for g in gen:
        print(g)
