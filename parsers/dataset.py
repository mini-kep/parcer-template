import arrow
from pathlib import Path

from parsers import PARSERS_DICT
from parsers.serialiser import to_json
from parsers.uploader import Uploader, upload_datapoints


def shift(**kwargs):
    return arrow.now().shift(**kwargs).format("YYYY-MM-DD")

def get_start_date(freq):
    d = dict(a=shift(years=-1),
            q=shift(quarters=-1), 
            m=shift(months=-4),
            d=shift(weeks=-1))  
    return d[freq]

def update(freq):
    dt = get_start_date(freq)
    parsers = PARSERS_DICT[freq]
    d = Dataset(parsers, dt)
    d.extract()
    return d.upload()
    

class Dataset(object):
    def __init__(self, parsers, start_date, end_date=None):
        self.parsers = parsers
        self.start, self.end = start_date, end_date
        self.items = []
        

    def extract(self):
        self.items = []
        for parser_cls in self.parsers:
            parser = parser_cls(self.start, self.end, silent=False)
            parser.extract()
            for datapoint in parser.items:
                self.items.append(datapoint)
        return self.items

    @property
    def json(self):
        fmt = {'separators': (',', ': '), 'indent': 4}
        return to_json(self.items, **fmt)

    def save_json(self, filename):
        Path(filename).write_text(self.json)
        
    def upload(self):
        return Uploader(upload_datapoints, silent=False).post(self.items)
        
        
if __name__ == '__main__': #pragma: no cover
    from parsers.getter.cbr_fx import USDRUR
    from parsers.getter.brent import Brent
    d = Dataset([USDRUR, Brent], '2017-11-13')
    d.extract()
    assert d.items[0]['name'] == 'USDRUR_CB'
    assert isinstance(d.json, str)
    assert d.json
    #d.save_json('abc.txt')
    print()
    d.upload()
