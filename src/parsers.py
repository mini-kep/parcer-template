import brent 
from helpers import DateHelper

class Parser:
    def __init__(self, freq, start=None):        
        self.freq = self._accept_frequency(freq)       
        if start is None:
            self.start = self.start_date
        else:    
            self.start = DateHelper.make_date(start) 
        self.end =  DateHelper.today()
        
    def _accept_frequency(self, letter):
        if all([letter.isalpha(),
                len(letter) == 1,
                letter in self.freqs]):
            return letter  
        else:
            raise ValueError(letter)

    @classmethod
    def get_default_args(self):
        return dict(freq=self.freqs[0])

class RosstatKEP(Parser):
    """Parse sections of Rosstat 'KEP' publication"""
    freqs = 'aqm'    
    start_date = DateHelper.make_date('1999-01-31')
    source_url = ("http://www.gks.ru/wps/wcm/connect/" 
                  "rosstat_main/rosstat/ru/statistics/" 
                  "publications/catalog/doc_1140080765391")
    # FIXME: change to actual method get_data? or count? 
    # or always retrun all variables?
    all_varnames = ['CPI_rog', 'RUR_EUR_eop']

    def sample(self):
        """Yield dictionaries with datapoints"""
        
        # this is a mock -----------------
       
        yield {"date": "2015-11-30",
            "freq": "m",
            "name": "CPI_rog",
            "value": 100.8}
        
        yield {"date": "2015-11-30",
            "freq": "m",
            "name": "RUR_EUR_eop",
            "value": 70.39}
        
        yield {"date": "2015-12-31",
            "freq": "m",
            "name": "CPI_rog",
            "value": 100.8}
        
        yield {"date": "2015-12-31",
            "freq": "m",
            "name": "RUR_EUR_eop",
            "value": 79.7}
        # end -----------------
 

class CBR_USD(Parser):
    """Retrieve Bank of Russia official USD to RUB exchange rate"""
    freqs = 'd'    
    start_date =  DateHelper.make_date('1991-07-01')
    source_url = "http://www.cbr.ru/scripts/Root.asp?PrtId=SXML"
    all_varnames = ['USDRUR_CB']

    def sample(self):
        """Yields dictionaries with mock datapoints"""
        dates =  ["2016-10-04", "2016-10-05", "2016-10-06", "2016-10-07"]
        values = [62.5477, 62.4323, 62.4583, 62.3900]
        for date, value in zip(dates, values):
            yield dict(freq="d",
                       name="USDRUR_CB",
                       date=date,
                       value=value)


class BrentEIA(Parser):
    """Retrieve Brent oil price from US EIA"""
    freqs = 'd'
    start_date =  DateHelper.make_date('1987-05-15')
    source_url = "https://www.eia.gov/opendata/qb.php?category=241335"
    all_varnames = ['BRENT']
    
    def get_data():
        return brent.yield_brent_dicts()        
    
    def sample(self):
        """Yields dictionaries with mock datapoints"""
        brent =  [("2016-07-29", 42.55),                  
                  ("2016-08-05", 40.88),
                  ("2016-08-12", 43.63),
                  ("2016-08-19", 48.60),
                  ("2017-03-16", 50.56),
                  ("2017-03-17", 50.58),
                  ("2017-03-20", 50.67)]
        for date, value in brent:
            yield {"date": date,
                   "freq": "d",
                   "name": "BRENT",
                   "value": value}             
      
    
if __name__ == "__main__":
    dataset_sample = []
    for cls in [RosstatKEP, CBR_USD, BrentEIA]:
        freq = cls.freqs[0]
        parser = cls(freq)
        gen = list(parser.sample())
        dataset_sample.extend(gen)
    print('Sample dataset:')
    print(dataset_sample)        
    