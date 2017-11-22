"""Download Brent FOB price time series from EIA API.

The data is sevral days behind (Oct 5, 2017):

{'date': '2017-10-02', 'freq': 'd', 'name': 'BRENT', 'value': Decimal('55.67')}
{'date': '2017-09-29', 'freq': 'd', 'name': 'BRENT', 'value': Decimal('57.02')}
{'date': '2017-09-28', 'freq': 'd', 'name': 'BRENT', 'value': Decimal('58.80')}
{'date': '2017-09-27', 'freq': 'd', 'name': 'BRENT', 'value': Decimal('58.74')}
{'date': '2017-09-26', 'freq': 'd', 'name': 'BRENT', 'value': Decimal('59.77')}

"""

import json
from parsers.config import EIA_ACCESS_KEY
from parsers.getter.base import ParserBase, format_date, format_value

def make_url(access_key=EIA_ACCESS_KEY):
    series_id = 'PET.RBRTE.D'
    return ("http://api.eia.gov/series/"
            f"?api_key={access_key}"
            f"&series_id={series_id}")


def parse_response(text):
    """Returns list of rows based on response *text*."""
    json_data = json.loads(text)
    return json_data["series"][0]["data"]


def yield_brent_dicts(response_text):
    """Yields datapoints as dicts.

    Args:
        downloader(function) - function used to retrieve URL
    """
    rows = parse_response(response_text)
    for row in rows:
        yield {"date": format_date(row[0], fmt="%Y%m%d"),
               "freq": "d",
               "name": "BRENT",
               "value": format_value(row[1])}


class Brent(ParserBase):
    """Brent oil price (EIA)"""
    observation_start_date = '1987-05-20'
                                                                  
    @property
    def url(self):
        return make_url()
    
    @staticmethod
    def get_datapoints(response):
        return list(yield_brent_dicts(response)) 
    
if __name__ == '__main__': #pragma: no cover
   u = Brent(1992)
   u.extract()
   print(len(u.items))
   assert u.items[0]
   print(u.items[0])

