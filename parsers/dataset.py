import json
from datetime import date
from parsers.getter.base import make_date


class Dataset(object):
    def __init__(self, parsers, start_date, end_date=None):
        self.parsers = parsers
        self.start_date = make_date(start_date) 
        self.end_date = make_date(end_date) or date.today()
        self.elapsed = 0   

    @property    
    def items(self):
        for parser_cls in self.parsers:
            parser = parser_cls()
            parser.start_date = self.start_date,
            parser.end_date = self.end_date,
            for datapoint in parser.extract().items:
                yield datapoint
        
    def save_json(self, filename): 
        fmt = {'separators': (',', ': '), 'indent': 4}           
        with open(filename, 'w') as f:
            json.dump(list(self.items), f, **fmt)
            
    def upload(self): 
        self.elapsed = 0 
        for parser in self.parsers:            
            print(parser.__doc__)
            p = parser(self.start_date, self.end_date)
            p.extract(verbose=True)
            assert p.parsing_result
            self.elapsed += p.elapsed
            assert p.upload(verbose=True)
            self.elapsed += p.elapsed
            print()
        print(f'Total extract and upload time: {self.elapsed:.2f}')   