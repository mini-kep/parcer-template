""" Download Brent FOB price time series from EIA API. """

import json
from datetime import datetime
import requests

ACCESS_KEY = "15C0821C54636C57209B84FEEE3CE654"

def format_string(date_string):
    fmt = "%Y%m%d"    
    return datetime.strptime(date_string, fmt).strftime("%Y-%m-%d")

assert format_string('20171231') == '2017-12-31'

def make_url(access_key=ACCESS_KEY):
    series_id = 'PET.RBRTE.D'
    return ("http://api.eia.gov/series/"
            f"?api_key={access_key}"
            f"&series_id={series_id}")

def yield_brent_dicts():
    """Stream data from url as dicts."""
    url = make_url()
    r = requests.get(url)
    json_data = json.loads(r.text)    
    parsed_json_data = json_data["series"][0]["data"]
    for row in parsed_json_data:
        date = format_string(row[0]) 
        price = float(row[1])
        yield {"date": date,
               "freq": "d",
               "name": "BRENT",
               "value": price}    
        
if __name__ == "__main__":
    url = make_url()
    gen = yield_brent_dicts(url)
    b = next(gen)
    
    
   
    