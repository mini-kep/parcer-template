from pathlib import Path
from parsers.serialiser import to_json
from parsers.uploader import Uploader, upload_datapoints

class Dataset(object):
    def __init__(self, parsers, start_date, end_date=None, silent=False):
        self.parsers = parsers
        self.start, self.end = start_date, end_date
        self.items = []
        self.silent = silent

    def extract(self):
        self.items = []
        for parser_cls in self.parsers:
            parser = parser_cls(self.start, self.end, self.silent)
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
