from pathlib import Path
from parsers.serialiser import to_json


class Dataset(object):
    def __init__(self, parsers, start_date, end_date=None):
        self.parsers = parsers
        self.start, self.end = start_date, end_date
        self.elapsed = 0
        self.datapoints = []

    def extract(self):
        self.datapoints = []
        for parser_cls in self.parsers:
            parser = parser_cls(self.start, self.end)
            parser.extract(verbose=True)
            for datapoint in parser.items:
                self.datapoints.append(datapoint)

    @property
    def json(self):
        fmt = {'separators': (',', ': '), 'indent': 4}
        return to_json(self.datapoints, **fmt)

    def save_json(self, filename):
        Path(filename).write_text(self.json)
        
    def upload(self):
        self.elapsed = 0
        for parser in self.parsers:
            print(parser.__doc__)
            p = parser(self.start, self.end)
            p.extract(verbose=True)
            assert p.parsing_result
            self.elapsed += p.elapsed
            assert p.upload(verbose=True)
            self.elapsed += p.elapsed
            print()
        print(f'Total extract and upload time: {self.elapsed:.2f}')
        
        
if __name__ == '__main__':
    from parsers.getter.cbr_fx import USDRUR
    from parsers.getter.brent import Brent
    d = Dataset([USDRUR, Brent], '2017-11-13')
    d.extract()
    assert d.datapoints[0]['name'] == 'USDRUR_CB'
    print(d.json)
    d.save_json('abc.txt')
