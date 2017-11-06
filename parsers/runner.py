"""Parser interfaces."""

import json
from parsers.helpers import make_date, today, as_string, as_markdown
from parsers.uploader import upload_datapoints

# individual parser functions
import parsers.getter.brent as brent
import parsers.getter.cbr_fx as cbr_fx
import parsers.getter.kep as kep
#TODO: use ust function below
import parsers.getter.ust as ust


def get_dates(observation_start_date, start=None, end=None):
   start = make_date(start) or observation_start_date    
   end = make_date(end) or today() 
   return start, end 


class ParserBase:
    """Parent class for parser runner."""
    
    observation_start_date = make_date('1965-01-01')
    source_url = ''
    
    def __init__(self, start=None, end=None):
        self.start, self.end = get_dates(self.observation_start_date, start, end)
            
    def all_items(self):
        pass
    
    @property
    def items(self):
        # assumes self.all_items() is present in child class
        for item in self.all_items():            
            dt = make_date(item['date'])        
            if dt >= self.start and dt <= self.end:
                yield item
                
    def upload(self):
        return upload_datapoints(self.items)
    
    def __repr__(self):
        start = as_string(self.start)
        end = as_string(self.end)
        return f'{self.__class__.__name__}(\'{start}\', \'{end}\')'


class RosstatKEP_Base(ParserBase):
    observation_start_date = make_date('1999-01-31')    
    source_url = ("http://www.gks.ru/wps/wcm/connect/"
                  "rosstat_main/rosstat/ru/statistics/"
                  "publications/catalog/doc_1140080765391")
    freq = None #must overload in child classes

    def all_items(self):
        return kep.yield_kep_dicts(self.freq)
    
    def sample(self):
        yield {"date": "2015-11-30", "freq": self.freq, "name": "CPI_rog", "value": 100.8}
        yield {"date": "2015-11-30", "freq": self.freq, "name": "RUR_EUR_eop", "value": 70.39}
        yield {"date": "2015-12-31", "freq": self.freq, "name": "CPI_rog", "value": 100.8}
        yield {"date": "2015-12-31", "freq": self.freq, "name": "RUR_EUR_eop", "value": 79.7}


class RosstatKEP_Monthly(RosstatKEP_Base):
    """Monthly indicators from Rosstat 'KEP' publication"""
    freq = 'm'


class RosstatKEP_Quarterly(RosstatKEP_Base):
    """Quarterly indicators from Rosstat 'KEP' publication"""
    freq = 'q'


class RosstatKEP_Annual(RosstatKEP_Base):
    """Annual indicators from Rosstat 'KEP' publication"""
    freq = 'a'


class CBR_USD(ParserBase):
    """Bank of Russia official USD to RUB exchange rate"""
    freq = 'd'
    observation_start_date = make_date('1992-01-01')  # '1991-07-01'
    source_url = "http://www.cbr.ru/scripts/Root.asp?PrtId=SXML"
    
    def all_items(self):
        return cbr_fx.get_cbr_er(self.start, self.end)

    def sample(self):
        """Yields dictionaries with sample datapoints."""
        return iter([{'date': '2017-09-15', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 57.7706},
                     {'date': '2017-09-16', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 57.5336},
                     {'date': '2017-09-19', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 57.6242},
                     {'date': '2017-09-20', 'freq': 'd', 'name': 'USDRUR_CB', 'value': 58.0993},
                    ])


class BrentEIA(ParserBase):
    """Brent oil price from US EIA"""
    freq = 'd'
    observation_start_date = make_date('1987-05-15')
    source_url = 'https://www.eia.gov/opendata/qb.php?category=241335'

    def all_items(self):
        # brent always returns full dataset
        return brent.yield_brent_dicts()
            
    def sample(self):
        """Yield a few dictionaries with datapoints."""
        return iter([{'date': '2017-09-18', 'freq': 'd', 'name': 'BRENT', 'value': 55.5},
                     {'date': '2017-09-15', 'freq': 'd', 'name': 'BRENT', 'value': 56.18},
                     {'date': '2017-09-14', 'freq': 'd', 'name': 'BRENT', 'value': 56.76},
                     {'date': '2017-09-13', 'freq': 'd', 'name': 'BRENT', 'value': 55.52}]
                    )
# TODO:
# class USTbonds(ParserBase):
#    """Brent oil price from US EIA"""
#    freq = 'd'
#    observation_start_date = DateHelper.make_date('1987-05-15')
#    source_url = "https://www.eia.gov/opendata/qb.php?category=241335"
#
#    def __init__(self, start=None):
#        if start is None:
#            self.start = self.observation_start_date
#        else:
#            self.start = DateHelper.make_date(start)
#
#    def yield_dicts(self):
#        for p in brent.yield_brent_dicts():
#            if DateHelper.make_date(p['date']) >= self.start:
#                yield p
#
#    def sample(self):
#        """Yield a few dictionaries with datapoints."""
#        return iter([{'date': '2017-09-18', 'freq': 'd', 'name': 'BRENT', 'value': 55.5},
#                     {'date': '2017-09-15', 'freq': 'd', 'name': 'BRENT', 'value': 56.18},
#                     {'date': '2017-09-14', 'freq': 'd', 'name': 'BRENT', 'value': 56.76},
#                     {'date': '2017-09-13', 'freq': 'd', 'name': 'BRENT', 'value': 55.52},
#                     {'date': '2017-09-12', 'freq': 'd', 'name': 'BRENT', 'value': 55.06},
#                     {'date': '2017-09-11', 'freq': 'd', 'name': 'BRENT', 'value': 54.2}]
#                    )


class Dataset:
    """Operations related to all parsers."""

    parsers = [RosstatKEP_Monthly,
               RosstatKEP_Quarterly,
               RosstatKEP_Annual,
               CBR_USD,
               BrentEIA,
               # USTbonds
               ]

    def as_markdown():
        return "\n\n".join([as_markdown(parser) for parser in Dataset.parsers])
        
    def sample():
        return [datapoint for parser in Dataset.parsers
                          for datapoint in parser().sample()]

    def items(start=None, end=None):
        for parser_cls in Dataset.parsers:            
            parser = parser_cls(start, end)
            for datapoint in parser.items:
                # convert to float
                datapoint['value'] = float(datapoint['value'])                
                yield datapoint

    def upload(start=None, end=None):
        gen = Dataset.items(start, end)
        return upload_datapoints(gen)        
        
    def save_json(filename='dataset.json', start=None, end=None,
                  fmt={'separators': (',', ': '), 'indent': 4}):            
        gen = Dataset.items(start, end)
        with open(filename, 'w') as f:
            json.dump(list(gen), f, **fmt)
            
    def save_reference_dataset(): 
        param = dict(filename='test_data_2016H2.json',
                     start='2016-06-01',
                     end='2016-12-31')
        Dataset.save_json(**param)
        

if __name__ == "__main__":
    from pprint import pprint

    print('Sample dataset:')
    pprint(Dataset.sample())

    # sample subsets
    fx = list(CBR_USD('2017-09-01').items)
    oil = list(BrentEIA('2017-09-01').items)
    kep_m = list(RosstatKEP_Monthly('2017-06-01').items)
    
    print(Dataset.as_markdown())
    