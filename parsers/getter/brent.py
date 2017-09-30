"""Download Brent FOB price time series from EIA API."""

import json
from datetime import datetime
import requests
from decimal import Decimal
from parsers.config import EIA_ACCESS_KEY


def format_string(date_string):
    return datetime.strptime(date_string, "%Y%m%d").strftime("%Y-%m-%d")

# MS: can't understand why we have assert inside a codebase ?
# EP: please mark your comments initials, so that it is tracable who is writing 
#     the reason for this assert is that it should be converted to test
#     better way os saying that is TODO(MS): convert to test
assert format_string('20171231') == '2017-12-31'


def make_url(access_key=EIA_ACCESS_KEY):
    series_id = 'PET.RBRTE.D'
    return ("http://api.eia.gov/series/"
            f"?api_key={access_key}"
            f"&series_id={series_id}")


def fetch(url):
    r = requests.get(url)
    return r.text
    # EP: why json.loads(r.text) will not execute? 
    # return json.loads(r.text) this line will not execute. need to be deleted


def parse_response(text):
    """Returns list of rows."""
    json_data = json.loads(text)
    return json_data["series"][0]["data"]


def yield_brent_dicts(download_func=fetch):
    """Yeilds data from url as dicts."""
    url = make_url()
    text = download_func(url)
    for row in parse_response(text):
        date = format_string(row[0])
        price = round(Decimal(float(row[1])), 4)
        yield {"date": date,
               "freq": "d",
               "name": "BRENT",
               "value": price}


if __name__ == "__main__":
    url = make_url()
    gen = yield_brent_dicts()
    b = next(gen)
