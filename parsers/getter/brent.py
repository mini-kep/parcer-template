"""Download Brent FOB price time series from EIA API."""

import json
from datetime import datetime
import requests
from decimal import Decimal
from parsers.config import EIA_ACCESS_KEY

# transform privitives

def format_string(date_string: str):
    return datetime.strptime(date_string, "%Y%m%d").strftime("%Y-%m-%d")

def format_value(value_string: str):
    return round(Decimal(value_string), 4)    


# url to dicts


def make_url(access_key=EIA_ACCESS_KEY):
    series_id = 'PET.RBRTE.D'
    return ("http://api.eia.gov/series/"
            f"?api_key={access_key}"
            f"&series_id={series_id}")


def fetch(url):
    """Returns text found at *url*."""
    r = requests.get(url)
    return r.text


def parse_response(text):
    """Returns list of rows based on response *text*."""
    json_data = json.loads(text)
    return json_data["series"][0]["data"]


def yield_brent_dicts(downloader=fetch):
    """Yeilds datapoints as dicts.
    
    Args:
        url_maker(function) - function used to create URL address
        downloader(function) - function used to retrieve URL
    """
    url = make_url()
    text = downloader(url)
    for row in parse_response(text):
        date = format_string(row[0])
        price = format_value(row[1])
        yield {"date": date,
               "freq": "d",
               "name": "BRENT",
               "value": price}
        

if __name__ == "__main__":
    gen = yield_brent_dicts()
    b = next(gen)
