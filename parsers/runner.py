"""Parser interfaces."""

import json

from parsers.helpers import DateHelper, Markdown, interpret_frequency

# individual parser functions
import parsers.getter.brent as brent
import parsers.getter.cbr_fx as cbr_fx
import parsers.getter.kep as kep
#TODO: use ust function below
import parsers.getter.ust as ust


class ParserBase:
    """Parent class for parser runner."""
    
    def __init__(self, start=None, end=None):        
        if start is None:
            self.start = self.observation_start_date
        else:
            self.start = DateHelper.make_date(start)            
        if end is None:
            self.end = DateHelper.today()
        else:
            self.end = DateHelper.make_date(end)   
            
    def yield_dicts(self):
        # assumes self._yield_dicts() is present in child class
        def is_date_in_range(d):
            dt = DateHelper.make_date(d['date'])        
            return dt >= self.start and dt <= self.end 
        return filter(is_date_in_range, self._yield_dicts())
    
    def upload(self):
        # TODO: upload individual parser data to database
        
        # data to upload
        gen = self.yield_dicts()
        pass 
    
    def __repr__(self):
        start = DateHelper.as_string(self.start)
        end = DateHelper.as_string(self.end)
        return f'{self.__class__.__name__}(\'{start}\', \'{end}\')'

    @classmethod
    def as_markdown(cls):
        url_str = Markdown.short_link(cls.reference['source_url'])
        freq_str = interpret_frequency(cls.freq)
        varname_str = ", ".join(cls.reference['varnames'])
        rows = [("Parser", cls.__name__),
                ("Description", cls.__doc__ or ''),
                ("URL", url_str or ''),
                ("Frequency", freq_str),
                ("Variables", varname_str or '')]
        return Markdown.table(rows)


class RosstatKEP_Base(ParserBase):
    observation_start_date = DateHelper.make_date('1999-01-31')    
    reference = dict(source_url = ("http://www.gks.ru/wps/wcm/connect/"
                                   "rosstat_main/rosstat/ru/statistics/"
                                   "publications/catalog/doc_1140080765391"),
                     varnames = ['GDP', 'CPI', 'etc'])
    freq = None #overload this in child classes

    def _yield_dicts(self):
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
    observation_start_date = DateHelper.make_date('1992-01-01')  # '1991-07-01'
    reference = dict(source_url = "http://www.cbr.ru/scripts/Root.asp?PrtId=SXML",
                     varnames = ['USDRUR_CB'])
    
    def _yield_dicts(self):
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


class BrentEIA(ParserBase):
    """Brent oil price from US EIA"""
    freq = 'd'
    observation_start_date = DateHelper.make_date('1987-05-15')
    reference = dict(source_url = 'https://www.eia.gov/opendata/qb.php?category=241335',
                     varnames = ['BRENT'])

    def _yield_dicts(self):
        # brent always returns full dataset, need truncate for start_date
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
# TODO:
# class USTbonds(ParserBase):
#    """Brent oil price from US EIA"""
#    freq = 'd'
#    observation_start_date = DateHelper.make_date('1987-05-15')
#    source_url = "https://www.eia.gov/opendata/qb.php?category=241335"
#    all_varnames = ['BRENT']
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

    def sample():
        return [datapoint for parser in Dataset.parsers
                          for datapoint in parser().sample()]

    def yield_dicts(start=None, end=None):
        for parser_cls in Dataset.parsers:            
            parser = parser_cls(start, end)
            for datapoint in parser.yield_dicts():
                # convert to float
                datapoint['value'] = float(datapoint['value'])                
                yield datapoint

    def upload(self, start=None, end=None):
        # TODO: uplood gen to database
        
        # data to upload
        gen = Dataset.yield_dicts(start, end)
        pass 
        
        
    def as_markdown():
        tables_str = [cls.as_markdown() for cls in Dataset.parsers]
        return '\n\n'.join(tables_str)

    def save_json(filename='dataset.json', start=None, end=None, fmt={}):            
        gen = Dataset.yield_dicts(start, end)
        with open(filename, 'w') as f:
            json.dump(list(gen), f, **fmt)
            
    def save_json_readable(filename, start=None, end=None):
        fmt = dict(indent=4, separators=(',', ': '))
        Dataset.save_json(filename, start, end, fmt)      
    

if __name__ == "__main__":
    from pprint import pprint
    print('Sample dataset:')
    pprint(Dataset.sample())

    print('\nMarkdown descriptions:')
    print(Dataset.as_markdown())

    #sample subsets
    fx = list(CBR_USD('2017-09-01').yield_dicts())
    oil = list(BrentEIA('2017-09-01').yield_dicts())
    kep_m = list(RosstatKEP_Monthly('2017-06').yield_dicts())

    # reference dataset
    param = dict(filename='test_data_2016H2.json', 
                 start='2016-06-01', 
                 end='2016-12-31')      
    # Dataset.save_json_readable(**param)
    
    # full dataset
    # Dataset.save_json()
