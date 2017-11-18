"""Parser interfaces."""

import json
from parsers.helpers import make_date, today, as_string, as_markdown
from parsers.uploader import upload_datapoints

# individual parser functions
import parsers.getter.brent as brent
import parsers.getter.cbr_fx as cbr_fx
import parsers.getter.kep as kep
import parsers.getter.ust as ust


def get_dates(observation_start_date, start=None, end=None):
   start = make_date(start) or observation_start_date    
   end = make_date(end) or today() 
   return start, end 

class DateViewer:   
    def __init__(self, observation_start_date, start=None, end=None):
        self.start = make_date(start) or observation_start_date    
        self.end = make_date(end) or today() 
    
    def make_date_filter(self):
        def is_in_date_range(item):
            dt = make_date(item['date'])        
            return self.start <= dt and dt <= self.end
        return is_in_date_range

class ParserBase0:
    """Parent class for parser runner."""
    
    observation_start_date = make_date('1965-01-01')
    source_url = ''
    
    def __init__(self, start=None, end=None):
        dv = DateViewer(self.observation_start_date, start, end)
        self.start = dv.start
        self.end = dv.end
        self.date_filter = dv.make_date_filter()
        
    def make_date_filter(self):
        def is_in_date_range(item):
            dt = make_date(item['date'])        
            return self.start <= dt and dt <= self.end
        return is_in_date_range

    def all_items(self):
        raise NotImplementedError
        
    @property
    def items(self):
        gen = filter(self.date_filter, self.all_items())
        return list(gen)
                
    def upload(self):
        return upload_datapoints(self.items)
    
    def __repr__(self):
        start = as_string(self.start)
        end = as_string(self.end)
        return f'{self.__class__.__name__}(\'{start}\', \'{end}\')'


  
class Getter:
    def __init__(self, start_date, end_date):
        pass
    
    def extract(self):
        return []

# actual getter class from ust
   
#class UST(object):
#    """Datapoints from US Treasury. Behaves as list after .extract() call."""
#                                                                  
#    def __init__(self, start_date, end_date, downloader=util.fetch):
#        # FIXME: in this parser we may restrict period to one year only
#        #        raise error when end_date - start_date  > 1 year 
#        self.start_date, self.end_date = start_date, end_date
#        self.response = None
#        self.parsing_result = []
#        self.downloader = downloader
#    
#    @property
#    def url(self):
#        return make_url(make_year(self.start_date))
#    
#    def extract(self):
#        self.response = self.downloader(self.url)
#        self.parsing_result = list(parse_xml(self.response))
#        return self
#        
#    # 'magics' to make this class behave like a list 
#    def __getitem__(self, i):
#        if self.parsing_result:
#            return self.parsing_result[i]
#        return None
#
#    def __len__(self):
#        return len(self.parsing_result)    
    

#TODO: merge ParserBase and getter.ust.Getter classes
    
# NOT TODO: must replace ParserBase0 with ParserBase + kill DateViewer
# NOT TODO: getter modules kep, cbr_fx, brent must have getter class as above
class ParserBase:
    """Parent class for parser."""
    
    observation_start_date = make_date('1965-01-01')
    source_url = ''
    getter_class = Getter
    cls = getter_class.__class__.__name__

    def __init__(self, start=None, end=None):
        self.start = make_date(start) or self.observation_start_date    
        self.end = make_date(end) or today() 
        self.getter = self.getter_class(self.start, self.end)

    def date_filter(self, item):
        """Returns a function which is used in filtering dates""" 
        def f(item):
            dt = make_date(item['date'])        
            return self.start <= dt and dt <= self.end
        return f
        
    def get_parsing_result(self):
        try:
            return self.getter.extract()
        except TypeError:
            raise TypeError(f'{self.cls}: argument error')
        except AttributeError:
            raise TypeError(f'{self.cls}: no .extract() method')            
    
    @property
    def elapsed(self):
        return self.getter.elapsed
    
    @property
    def items(self):
        parsing_result = self.get_parsing_result() 
        return list(filter(self.date_filter, parsing_result))
                
    def upload(self):
        return upload_datapoints(self.items)
    
    def __repr__(self):
        start = as_string(self.start)
        end = as_string(self.end)
        return f'{self.__class__.__name__}(\'{start}\', \'{end}\')'


class BondsUST(ParserBase):
    """Import interest rates for US treasuries"""
    freq = 'd'
    observation_start_date = make_date('1990-01-02')
    source_url = "https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield"
    getter_class = ust.UST


class RosstatKEP_Base(ParserBase0):
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


class CBR_USD(ParserBase0):
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


class BrentEIA(ParserBase0):
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

REFERENCE_DATASET = dict(filename='test_data_2016H2.json',
                         start='2016-06-01',
                         end='2016-12-31')

class Dataset(ParserBase):
    """Operations related to all parsers."""

    parsers = [RosstatKEP_Monthly,
               RosstatKEP_Quarterly,
               RosstatKEP_Annual,
               CBR_USD,
               BrentEIA,
               BondsUST
               ]

    def as_markdown():
        return "\n\n".join([as_markdown(parser) for parser in Dataset.parsers])
        
    def sample():
        return [datapoint for parser in Dataset.parsers
                          for datapoint in parser().sample()]
    
    @property    
    def items(self):
        for parser_cls in Dataset.parsers:
            parser = parser_cls(as_string(self.start),
                                as_string(self.end))
            for datapoint in parser.items:
                yield datapoint
        
    #WARNING: may result in large file
    def save_json(filename, fmt={'separators': (',', ': '), 'indent': 4}):            
        with open(filename, 'w') as f:
            json.dump(list(Dataset.items), f, **fmt)
            
    def save_reference_dataset(): 
        Dataset.save_json(**REFERENCE_DATASET)
        

if __name__ == "__main__":
    import arrow
    
    dt1 = arrow.now().shift(months=-1).format('YYYY-MM-DD')
    dt2 = arrow.now().shift(months=-3).format('YYYY-MM-DD')
    
    # sample subsets
    #fx = CBR_USD(dt1).items
    #oil = BrentEIA(dt1).items
    u = BondsUST(dt1)
    values = u.items
    print("Elapsed", u.elapsed)
    
    #kep_m = RosstatKEP_Monthly(dt2).items
                              
  