from parser import (today)

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
        """Returns a string containing parser parameters,
           and formatted to be represented as a markdown table.
        """

        # create table header
        table = [["Parameter", "Value"]]

        # define the first column values (parameters)
        params = ["Job", "Variables", "Frequency", 'Last updated',
                  'Expected update', "Source URL", "Source type"]

        # define the second column values (values of the parameters)
        not_available = 'NA'
        varname_str = not_available if cls.all_varnames is None \
            else ", ".join(cls.all_varnames)

        values = [cls.does_what, varname_str, cls.freqs, cls.last_updated,
                  cls.expected_update, cls.source_url, cls.source_type]

        # combine parameter-value pairs into lists
        for param, value in zip(params, values):
            value_or_na = not_available if value is None else value
            row = [param, value_or_na]
            table.append(row)

        # return string representation of the table formatted
        # for the markdown
        return to_markdown(table)       
            
        
class RosstatKEP(Parser):
    name = 'rosstat-kep'
    target = 'Sections of KEP Rosstat publication'
    freqs = 'aqm'    
    start_date = make_date('1999-01-31')
    source_url = ("http://www.gks.ru/wps/wcm/connect/" 
                  "rosstat_main/rosstat/ru/statistics/" 
                  "publications/catalog/doc_1140080765391")
    source_type = "Word"
    
    @property
    def last_updated():
        return None
        
    @property
    def all_varnames():
        # TODO: must change to actaula method 
        return ['CPI_rog', 'RUR_EUR_eop']


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


assert "| Parameter | Value |" in RosstatKEP.as_markdown()
assert "| Variables |" in RosstatKEP.as_markdown()


test_list = list(RosstatKEP('m', ['CPI_rog']).get_data())
assert test_list[1]['value'] == 70.39
assert test_list[3]['date'] == "2015-12-31"


class CBR_USD(Parser):
    """A parser to retrieve information about 
       the official USD to RUB exchange rate 
       from the Bank of Russia public API.
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


assert "| Frequency | d |" in CBR_USD.as_markdown()
assert "| Source URL | http://www.cbr.ru/scripts/Root.asp?PrtId=SXML |"\
       in CBR_USD.as_markdown()
assert "| Source type | API |" in CBR_USD.as_markdown()

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
    print(CBR_USD.as_markdown())
    print(list(CBR_USD('d', ['CBR_USD']).get_data()))
