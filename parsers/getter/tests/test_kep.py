import pytest
import pandas as pd
from io import StringIO
from decimal import Decimal
from parsers.getter.kep import (make_url,
                                read_csv,
                                get_dataframe_from_repo,
                                yield_all_dicts,
                                is_valid, KEP)
url_a = ('https://raw.githubusercontent.com/mini-kep/'
         'parser-rosstat-kep/master/data/processed/latest/dfa.csv')


class Test_KEP():
    
    parser = KEP()

    def test_url(self):
        assert self.parser.url == url_a

    def test_parse_response(self):
        gen = self.parser.parse_response('time_index,CPI_ALCOHOL_rog\n31.12.1999,143.2')
        d = gen[0]
        assert d['date'] == '1999-12-31'
        assert d['freq'] == 'a'
        assert d['name'] == 'CPI_ALCOHOL_rog'
        assert d['value'] == Decimal('143.2')  

    # TODO: reposnse filtered to none         
    
         
def test_make_url():
    assert make_url('a') == url_a

# probably the slowest test
@pytest.mark.webtest
def test_get_dataframe_from_repo_on_real_data():
    return get_dataframe_from_repo('a') == read_csv(url_a)

    
#TODO: test KEP.parse_response()    
    
class Test_yeild_all_dicts():

    csv_data = 'time_index,CPI_ALCOHOL_rog\n31.12.1999,143.2'
    df = read_csv(StringIO(csv_data))
    assert isinstance(df, pd.DataFrame)

    def test_yield_all_dicts(self):
        gen = yield_all_dicts(df=self.df, freq='a')
        d = next(gen)
        assert d['date'] == '1999-12-31'
        assert d['freq'] == 'a'
        assert d['name'] == 'CPI_ALCOHOL_rog'
        assert d['value'] == Decimal('143.2')

class Test_is_valid():
    datapoint_with_nan = {'value': 'NaN', 'name': 'something'}
    datapoint_with_year = {'value': Decimal('123.1'), 'name': 'year'}
        
    def test_is_valid_with_nan_value_returns_false(self):
        assert is_valid(self.datapoint_with_nan) == False

    def test_is_valid_with_name_year_returns_false(self):
        assert is_valid(self.datapoint_with_year) == False

if __name__ == "__main__":
    pytest.main([__file__])
