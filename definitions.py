from to_markdown import to_markdown 


class Description:
    
    @classmethod
    def as_markdown(cls):
        table = [['Parameter', 'Value']]
        table.append(['Job', cls.does_what])
        table.append(['Frequency', cls.freq])
        return to_markdown(table)       
        

class RosstatKEP(Description):
    name = 'rosstat-kep'
    does_what = 'Parse sections of KEP Rosstat publication'
    freq = 'aqm'    
    
    
class ParserCaller:    
    """Parent class to get parsing result from individual parser."""
    
    supported_frequencies = 'aqmd' #must overload this 
    supported_variables = ['BRENT'] #must overload this 
    
    # may be properties
    # must overload this 
    @property
    def varnames(self):
        return ['BRENT']      
    
    @property 
    def frequencies(self):
        return ['d']
    
    @property
    def start_date(self):
        return '1999-01-01'

    @property
    def end_date(self):
        return 'today'
    
    def pure_get_data(self, freq, varnames, start, end):
        """Yield ditionaries with datapoints"""
        
        brent = [("2017-03-16", 50.56),
                 ("2017-03-17", 50.58),
                 ("2017-03-20", 50.67)]   
    
        for date, value in brent:
            yield {"date": date,
                   "freq": "d",
                   "name": "BRENT",
                   "value": value}            
    
    def get_data(self, freq, varnames, start=None):
        assert freq in self.frequencies
        for vn in varnames:
            assert varnames in self.varnames
        if start is None:
            start = self.start_date
        end = 'it should be today'    
        return self.pure_get_data(freq, varnames, start, end)
      

def mock_parser_output_2():   

    brent = [("2017-03-16", 50.56),
             ("2017-03-17", 50.58),
             ("2017-03-20", 50.67)]   
    
    for date, value in brent:
        yield {"date": date,
               "freq": "d",
               "name": "BRENT",
               "value": value}
    

def mock_parser_output_1():   
    
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
    
    
if __name__ == "__main__":
    print(RosstatKEP.as_markdown())    
    