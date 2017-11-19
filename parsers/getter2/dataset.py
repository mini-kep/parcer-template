import json
from datetime import date
from getter.base import make_date
from getter import PARSERS

class Dataset(object):
    def __init__(self, start_date, end_date=None):
        self.start_date = make_date(start_date) 
        if end_date is None: 
            self.end_date = date.today()
        else: 
           self.end_date = make_date(end_date)

    @property    
    def items(self):
        for parser_cls in PARSERS:
            parser = parser_cls()
            parser.start_date = self.start_date,
            parser.end_date = self.end_date,
            for datapoint in parser.items:
                yield datapoint
        
    def save_json(filename): 
        fmt = {'separators': (',', ': '), 'indent': 4}           
        with open(filename, 'w') as f:
            json.dump(list(Dataset.items), f, **fmt)
            
def save_reference_dataset(): 
    dataset = Dataset(start='2016-06-01', end='2016-12-31')
    dataset.save_json('test_data_2016H2.json')
