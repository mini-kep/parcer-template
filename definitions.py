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

def make_date(dt):
    return arrow.get(dt).date() 


class Description:
    
    @classmethod
    def as_markdown(cls):
        table = [['Parameter', 'Value']]        
        table.append(['Job', cls.does_what])
        table.append(['Frequency', cls.freqs])         
        table.append(['Variables', 
                      ", ".join(cls.all_varnames)
                      ])
        return to_markdown(table)       

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
            
        
class RosstatKEP(Description):
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

def mock_parser_output_1():   

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