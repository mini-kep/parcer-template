from parser import (today, make_date, Parser, Table, RosstatKEP, CBR_USD)

# TODO: convert this to pytest
   

assert today().year >= 2017

assert make_date('2007-01-25').day == 25
assert make_date('2007-01-25').month == 1
assert make_date('2007-01-25').year == 2007

                
# EP: Parser does not seem very testable

# To test:   
#class Table:
#    def __init__(self, cls):
#        varname_str = ", ".join(cls.all_varnames)
#        url_str = short_link(cls.source_url)        
#        self.rows = [("Parser", cls.__name__),
#            ("Description", cls.__doc__),
#            ("URL", url_str),
#            ("Source type", cls.info['source_type']),
#            ("Frequency", interpret_frequencies(cls.freqs)),
#            ("Variables", varname_str)]
#        
#    def as_markdown(self):
#        return to_markdown(self.rows)

assert "| Parser |" in RosstatKEP.as_markdown()
assert "| Variables |" in RosstatKEP.as_markdown()

#FIXME: need to change to some thing more generic, eg type checks
test_list = list(RosstatKEP('m', ['CPI_rog']).get_data())
assert test_list[1]['value'] == 70.39
assert test_list[3]['date'] == "2015-12-31"


assert "| Frequency |" in CBR_USD.as_markdown()
assert "| URL |" in CBR_USD.as_markdown()
assert "| Source type | API |" in CBR_USD.as_markdown()

#FIXME: need to change to some thing more generic, eg type checks
test_list = list(CBR_USD('d', ['CBR_USD']).get_data())
assert test_list[0]['value'] == 62.5477
assert test_list[2]['date'] == "2016-10-06"

