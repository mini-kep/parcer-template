import unittest
import pandas as pd
from io import StringIO
from mock import patch
from decimal import Decimal
from parsers.getter.kep import (make_url,
                                read_csv,
                                get_dataframe_from_repo,
                                yield_all_dicts,
                                is_valid,
                                yield_kep_dicts)


class Kep_tests(unittest.TestCase):

    def setUp(self):
        csv_data = 'time_index,CPI_ALCOHOL_rog\n31.12.1999,143.2'
        self.datapoint_with_nan = {'value': 'NaN', 'name': 'something'}
        self.datapoint_with_year = {'value': Decimal('123.1'), 'name': 'year'}
        self.csv_dataframe = read_csv(StringIO(csv_data))
        self.url =( 'https://raw.githubusercontent.com/mini-kep/'
                    'parser-rosstat-kep/master/data/processed/latest/dfa.csv')

    def test_make_url(self):
        assert make_url('a') == self.url

    def test_read_csv(self):
        assert isinstance(self.csv_dataframe,pd.DataFrame)

    def test_get_dataframe_from_repo(self):
        return get_dataframe_from_repo('a') == read_csv(self.url)

    @patch('parsers.getter.kep.get_dataframe_from_repo')
    def test_function_to_test(self, mocked_dataframe):
        mocked_dataframe.return_value = self.csv_dataframe
        gen = yield_all_dicts('a')
        d = next(gen)
        assert d['date'] == '1999-12-31'
        assert d['freq'] == 'a'
        assert d['name'] == 'CPI_ALCOHOL_rog'
        assert d['value'] == Decimal('143.2')

    def test_is_valid_with_nan_value_returns_false(self):
        assert is_valid(self.datapoint_with_nan) == False

    def test_is_valid_with_name_year_returns_false(self):
        assert is_valid(self.datapoint_with_year) == False
