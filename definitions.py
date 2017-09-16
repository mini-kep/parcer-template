from to_markdown import to_markdown 

import arrow

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
    # may also use 
    # pandas.to_datetime('2017').date()
    return arrow.get(dt).date() 

assert make_date('2007-01-25').day == 25

class Parser:
    
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
        table = [['Parameter', 'Value']]        
        table.append(['Job', cls.does_what])
        table.append(['Frequency', cls.freqs])         
        varname_str = ", ".join(cls.all_varnames)
        table.append(['Variables', varname_str])
        return to_markdown(table)       
            
        
class RosstatKEP(Parser):
    name = 'rosstat-kep'
    does_what = 'Parse sections of KEP Rosstat publication'
    freqs = 'aqm'    
    all_varnames = ['CPI_rog', 'RUR_EUR_eop']
    start_date = make_date('1999-01-31')
    
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
    """A parser to retrieve information about the official
       USD to RUB exchange rate from the Bank of Russia public API.
    """

    name = 'CBR_USD'
    does_what = 'Retrieve the official USD to RUB exchange rate ' \
                'from the Bank of Russia public API'
    freqs = 'd'
    all_varnames = ['CBR_USD']
    start_date = make_date('1991-07-01')
    source_url = "http://www.cbr.ru/scripts/Root.asp?PrtId=SXML"
    source_type = "API"
    last_updated = None
    expected_update = None

    def get_data(self):
        """Returns a list of dictionaries with mock datapoints"""

        labels = ["date", "freq", "name", "value"]
        dates = ["2016-10-04", "2016-10-05", "2016-10-06", "2016-10-07"]
        values = [62.5477, 62.4323, 62.4583, 62.3900]
        freq = "d"
        name = "CBR_USD"

        data = list()
        for date, value in zip(dates, values):
            datapoint = [date, freq, name, value]
            datapoint_dict = dict(zip(labels, datapoint))
            data.append(datapoint_dict)

        return data


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
    print(list(RosstatKEP('m', ['CPI_rog']).get_data()))
    print("\n")
    print(list(CBR_USD('d', ['CBR_USD']).get_data()))
