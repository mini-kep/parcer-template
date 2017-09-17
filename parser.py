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

assert today().year >= 2017

def make_date(dt):
    # may also use pandas.to_datetime('2017').date()
    return arrow.get(dt).date() 

assert make_date('2007-01-25').day == 25
assert make_date('2007-01-25').month == 1
assert make_date('2007-01-25').year == 2007

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
        if start is None:
            self.end = today()
        else:
            self.end = end

    @classmethod
    def as_markdown(cls):
        return Table(cls).as_markdown()
        
#    @classmethod
#    def as_markdown(cls):
#        """Returns a string containing parser parameters,
#           and formatted to be represented as a markdown table.
#        """
#
#        # create table header
#        table = [["Parameter", "Value"]]
#        
#        # define the first column values (parameters)
#        params = ["Job", "Variables", "Frequency", 'Last updated',
#                  'Expected update', "Source URL", "Source type"]
#
#        # define the second column values (values of the parameters)
#        not_available = 'NA'
#        varname_str = not_available if cls.all_varnames is None \
#            else ", ".join(cls.all_varnames())
#
#        values = [cls.info['target'], varname_str, cls.freqs, 
#                  cls.last_updated, cls.source_url, cls.info['source_type']
#                  ]
#
#        # combine parameter-value pairs into lists
#        for param, value in zip(params, values):
#            value_or_na = not_available if value is None else value
#            row = [param, value_or_na]
#            table.append(row)
#
#        # return string representation of the table formatted
#        # for the markdown
#        return to_markdown(table)       

         
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
 

assert "| Parser |" in RosstatKEP.as_markdown()
assert "| Variables |" in RosstatKEP.as_markdown()

#FIXME: need to change to some thing more generic, eg type checks
test_list = list(RosstatKEP('m', ['CPI_rog']).get_data())
assert test_list[1]['value'] == 70.39
assert test_list[3]['date'] == "2015-12-31"


class CBR_USD(Parser):
    """Retrieve Bank of Russia official USD to RUB exchange rate"""
    # reference information (not affecting parser call)
    info = dict(source_type = "API")
    # class atrributes used in parser call
    freqs = 'd'    
    start_date = make_date('1991-07-01')
    source_url = "http://www.cbr.ru/scripts/Root.asp?PrtId=SXML"
    all_varnames = ['CBR_USD']

    def get_data(self):
        """Yields dictionaries with mock datapoints"""
        dates =  ["2016-10-04", "2016-10-05", "2016-10-06", "2016-10-07"]
        values = [62.5477, 62.4323, 62.4583, 62.3900]
        for date, value in zip(dates, values):
            yield dict(freq="d",
                       name="USDRUR_CB",
                       date=date,
                       value=value)

assert "| Frequency |" in CBR_USD.as_markdown()
assert "| URL |" in CBR_USD.as_markdown()
assert "| Source type | API |" in CBR_USD.as_markdown()

#FIXME: need to change to some thing more generic, eg type checks
test_list = list(CBR_USD('d', ['CBR_USD']).get_data())
assert test_list[0]['value'] == 62.5477
assert test_list[2]['date'] == "2016-10-06"


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

    print(list(RosstatKEP('m', ['CPI_rog']).get_data()))
    print(list(CBR_USD('d', ['CBR_USD']).get_data()))
