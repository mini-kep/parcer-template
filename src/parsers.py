"""Parser classes to get datapoints for the database.

Note:
 - each class is for one frequency now, this simplifies parser calls
"""

#TODO-1: restore tests in test_parsers.py
#TODO-2 (EP): put actual data in RosstatKEP_*.yield_dicts()
#TODO-3: save to database

import itertools

from helpers import DateHelper

import brent 
import cbr_fx


class RosstatKEP_Base(object):
    """Parse sections of Rosstat 'KEP' publication"""
    # must override frequencies
    freq = '_'    
    observation_start_date = DateHelper.make_date('1999-01-31')
    source_url = ("http://www.gks.ru/wps/wcm/connect/" 
                  "rosstat_main/rosstat/ru/statistics/" 
                  "publications/catalog/doc_1140080765391")
    # FIXME: change to actual method get_data? or count? 
    # or always retrun all variables?
    all_varnames = ['CPI_rog', 'RUR_EUR_eop']

    def __init__(self, start=None):        
        if start is None:
            self.start = self.observation_start_date
        else:    
            self.start = DateHelper.make_date(start) 
   

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

    #TODO-2: put actual data 
    
    def yield_dicts(self):
        return self.sample()


class RosstatKEP_Monthly(RosstatKEP_Base):
    freq = 'm'        
        

class RosstatKEP_Quarterly(RosstatKEP_Base):
    freq = 'q'        


class RosstatKEP_Annual(RosstatKEP_Base):    
    freq = 'a'
    

class CBR_USD(object):
    """Retrieve Bank of Russia official USD to RUB exchange rate"""
    freq = 'd'    
    observation_start_date = DateHelper.make_date('1991-07-01')
    source_url = "http://www.cbr.ru/scripts/Root.asp?PrtId=SXML"
    all_varnames = ['USDRUR_CB']
    
    def __init__(self, start=None):        
        if start is None:
            self.start = self.observation_start_date
        else:    
            self.start = DateHelper.make_date(start) 
        self.end = DateHelper.today()

    def yield_dicts(self):        
        return cbr_fx.get_cbr_er(self.start, self.end)
    
    def sample(self):
        """Yields dictionaries with sample datapoints."""
        return iter([{'date': '2017-09-15', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 57.7706},
 {'date': '2017-09-16', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 57.5336},
 {'date': '2017-09-19', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 57.6242},
 {'date': '2017-09-20', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 58.0993},
 {'date': '2017-09-21', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 58.129},
 {'date': '2017-09-22', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 58.2242},
 {'date': '2017-09-23', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 57.6527},
 {'date': '2017-09-26', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 57.566}])


class BrentEIA():
    """Retrieve Brent oil price from US EIA"""
    freq = 'd'
    observation_start_date =  DateHelper.make_date('1987-05-15')
    source_url = "https://www.eia.gov/opendata/qb.php?category=241335"
    all_varnames = ['BRENT']
    
    def __init__(self, start=None):        
        if start is None:
            self.start = self.observation_start_date
        else:    
            self.start = DateHelper.make_date(start) 
    
    def yield_dicts(self):
        for p in brent.yield_brent_dicts():
            if DateHelper.make_date(p['date']) >= self.start:
                yield p            
    
    def sample(self):
        """Yield a few dictionaries with datapoints."""
        return iter([{'date': '2017-09-18', 'freq': 'd', 'name': 'BRENT', 'value': 55.5},
 {'date': '2017-09-15', 'freq': 'd', 'name': 'BRENT', 'value': 56.18},
 {'date': '2017-09-14', 'freq': 'd', 'name': 'BRENT', 'value': 56.76},
 {'date': '2017-09-13', 'freq': 'd', 'name': 'BRENT', 'value': 55.52},
 {'date': '2017-09-12', 'freq': 'd', 'name': 'BRENT', 'value': 55.06},
 {'date': '2017-09-11', 'freq': 'd', 'name': 'BRENT', 'value': 54.2}] 
        )           
      

class Collection:
    """Operations related to aggreted reult of all parsers."""
    
    parsers = [RosstatKEP_Monthly, 
               RosstatKEP_Quarterly, 
               RosstatKEP_Annual,
               CBR_USD, 
               BrentEIA
               ]

    def get_sample():
        dataset_sample = []
        for cls in Collection.parsers:
            parser = cls()
            gen = list(parser.sample())
            dataset_sample.extend(gen)
        return dataset_sample
    
    def yield_full_dataset():
        gen_list = [p().yield_dicts() for p in Collection.parsers]
        return itertools.chain.from_iterable(gen_list)
       
    
if __name__ == "__main__":
    from pprint import pprint
    print('Sample dataset:')
    pprint(Collection.get_sample()) 

    gen_fx = list(CBR_USD('2017-09-01').yield_dicts())    
    
    # TODO-3: must put this generator into database
    gen = Collection.yield_full_dataset()  
