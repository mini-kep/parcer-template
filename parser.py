import arrow

from to_markdown import to_markdown 

# FIXME: change assert to raise exception
def accept_frequency(letter, supported_frequencies):
    # must be single letter 
    assert letter.isalpha()
    assert len(letter) == 1
    # must be supported          
    assert letter in supported_frequencies
    return letter         

# FIXME: change assert to raise exception
def accept_varnames(varnames, supported_varnames):
    for vn in varnames:
        assert vn in supported_varnames
    return varnames    


def today():
    return arrow.now().date()


def make_date(dt):
    # may also use pandas.to_datetime('2017').date()
    return arrow.get(dt).date() 


class Parser:

    @property
    def last_updated(self):
        return None

    def __init__(self, freq, varnames, start=None, end=None):        
        self.freq = accept_frequency(freq, self.freqs)
        self.varnames = accept_varnames(varnames, self.all_varnames)
        if start is None:
            self.start = self.start_date
        else:    
            self.start = make_date(start) 
        if end is None:
            self.end = today()
        else:
            self.end = end

    @classmethod
    def as_markdown(cls):
        return Table(cls).as_markdown()
        
        
def short_link(url, n=60):
    if len(url) > n:
        text = url[:n] + '...'
    else:
        text = url    
    return f'[{text}]({url})'


def interpret_frequencies(freqs):
    mapper = dict(a='annual',
                  q='quarterly',
                  m='monthly',
                  w='weekly',
                  d='daily')
    freq_str = ", ".join([mapper[f] for f in freqs])
    return freq_str.capitalize() 
    
class Table:
    def __init__(self, cls):
        varname_str = ", ".join(cls.all_varnames)
        url_str = short_link(cls.source_url)        
        self.rows = [("Parser", cls.__name__),
            ("Description", cls.__doc__),
            ("URL", url_str),
            ("Source type", cls.info['source_type']),
            ("Frequency", interpret_frequencies(cls.freqs)),
            ("Variables", varname_str)]
        
    def as_markdown(self):
        return to_markdown(self.rows)


class RosstatKEP(Parser):
    """Parse sections of KEP Rosstat publication"""
    # reference information (not affecting parser call)
    info = dict(source_type = "Word")
    # class atrributes used in parser call
    freqs = 'aqm'    
    start_date = make_date('1999-01-31')
    source_url = ("http://www.gks.ru/wps/wcm/connect/" 
                  "rosstat_main/rosstat/ru/statistics/" 
                  "publications/catalog/doc_1140080765391")
    # FIXME: change to actual method get_data? or count? 
    # or always retrun all variables?
    all_varnames = ['CPI_rog', 'RUR_EUR_eop']

    def get_data(self):
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
    # reference information (not affecting parser call)
    info = dict(source_type = "API")
    # class attributes used in parser call
    freqs = 'd'    
    start_date = make_date('1991-07-01')
    source_url = "http://www.cbr.ru/scripts/Root.asp?PrtId=SXML"
    all_varnames = ['USDRUR_CB']

    def get_data(self):
        """Yields dictionaries with mock datapoints"""
        dates =  ["2016-10-04", "2016-10-05", "2016-10-06", "2016-10-07"]
        values = [62.5477, 62.4323, 62.4583, 62.3900]
        for date, value in zip(dates, values):
            yield dict(freq="d",
                       name="USDRUR_CB",
                       date=date,
                       value=value)


class BrentEIA(Parser):
    """Retrieve Brent Prices from the US EIA"""
    # reference information (not affecting parser call)
    info = dict(source_type = "API")
    # class attributes used in parser call
    freqs = 'dwma'
    start_date = make_date('1987-05-15')
    source_url = "https://www.eia.gov/opendata/qb.php?category=241335"
    all_varnames = ['EIA_BRENT']

    def get_data(self):
        """Yields dictionaries with mock datapoints"""
        dates =  ["2016-07-29", "2016-08-05", "2016-08-12", "2016-08-19"]
        values = [42.55, 40.88, 43.63, 48.6]
        for date, value in zip(dates, values):
            yield dict(freq="w",
                       name="EIA_BRENT",
                       date=date,
                       value=value)


def mock_parser_output_2():   

    # this is a mock -----------------
    brent = [("2017-03-16", 50.56),
             ("2017-03-17", 50.58),
             ("2017-03-20", 50.67)]   

    for date, value in brent:
        yield {"date": date,
               "freq": "d",
               "name": "BRENT",
               "value": value}
    # end   --------------------------               
  
    
if __name__ == "__main__":
    print(RosstatKEP.as_markdown())  
    print("\n")
    print(CBR_USD.as_markdown())