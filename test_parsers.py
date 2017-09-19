import arrow
import datetime
import pytest

from numbers import Number
from parsers import (today, make_date, 
                    Table, 
                    RosstatKEP, CBR_USD, BrentEIA)


class Test_today:
    def test_today(self):
        assert today() == datetime.date.today()


class Test_make_date:
    def test_make_date_on_valid_input(self):
        date = make_date('2007-01-25')
        assert date.day == 25
        assert date.month == 1
        assert date.year == 2007

    def test_make_date_on_valid_input_in_another_format(self):
        date = make_date('2007/01/25')
        assert date.day == 25
        assert date.month == 1
        assert date.year == 2007

    def test_make_date_on_valid_input_none(self):
        assert make_date(None) == datetime.date.today()

    def test_make_date_on_invalid_input_out_of_range(self):
        with pytest.raises(ValueError):
            make_date('2007-25-01')

    def test_make_date_on_invalid_input_empty_str(self):
        with pytest.raises(Exception):
            make_date('')

    def test_make_date_on_invalid_input_empty(self):
        with pytest.raises(TypeError):
            make_date()


class TestTable:
    
    #EP: better structure is to make the mock in setup method (as now), 
    #    or a fixture (at next round of testing)
    def setup_method(self):
        
        class MockParser:
            """A mock parser to test Table class"""
            info = dict(source_type='API')
            freqs = 'aqmwd'
            source_url = 'http://some.url'
            all_varnames = ['data_1', 'data_2']
        
        self.MockParser = MockParser
            
    def test_as_markdown_produces_correct_string_on_short_URL(self):
        expected = ('| Parser | MockParser |\n'
                    '| ------ | ---------- |\n'
                    '| Description | A mock parser to test Table class |\n'
                    '| URL | [http://some.url](http://some.url) |\n'
                1    '| Source type | API |\n'
                    '| Frequency | Annual, quarterly, monthly, weekly, daily |\n'
                    '| Variables | data_1, data_2 |')
        assert Table(self.MockParser).as_markdown() == expected

    def test_as_markdown_valid_input_long_link(self):
        self.MockParser.source_url = ("http://www.gks.ru/wps/wcm/connect/"
                                      "rosstat_main/rosstat/ru/statistics/"
                                      "publications/catalog/"
                                      "doc_1140080765391")
        expected = 'http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/st...'
        assert expected in Table(self.MockParser).as_markdown()

    #not sure we need this:
    def test_as_markdown_invalid_class(self):
        with pytest.raises(AttributeError):
            _ = Table(object)

    #not sure we need this:
    def test_as_markdown_invalid_input_none(self):
        with pytest.raises(AttributeError):
            _ = Table(None)


class Base_Test_Parser:
    
    def setup_method():
        #must overload this
        self.items = None

    def test_get_data_members_are_length_4(self):
        for item in self.items:
            assert len(item) == 4
            
    # TODO: уточнить какой замысел теста тут?          
    def test_get_data_members________(self):
        for item in self.items:
            assert item['date']
            assert item['freq']
            assert item['name']
            assert item['value']
            
    # TODO: rename           
    def test_get_data_types(self):
        for item in self.items:
            assert isinstance(item['date'], str)
            assert isinstance(item['freq'], str)
            assert isinstance(item['name'], str)
            assert isinstance(item['value'], Number)
 
#TODO:           
#    - use self.items
#    - rename test method to have expected result 
#    - может оттестировать еще что-то не только get_data? по идее - все публичные методы/аттрибуты надо 

    
#    @staticmethod
#    def test_get_data_valid_date_format(data):
#        dates = (item['date'] for item in data)
#        for date in dates:
#            assert arrow.get(date)
#
#    @staticmethod
#    def test_get_data_valid_date_range(data, min_date):
#        dates = (item['date'] for item in data)
#        for date in dates:
#            date = arrow.get(date).date()
#            assert (min_date <= date <= datetime.date.today())
#
#    @staticmethod
#    def test_get_data_freq_range(data, freqs):
#        for item in data:
#            assert item['freq'] in freqs and len(item['freq']) == 1
#
#    @staticmethod
#    def test_get_data_varnames_range(data, all_varnames):
#        for item in data:
#            assert item['name'] in all_varnames
#
#    @staticmethod
#    def test_get_data_values_range(data, min_value, max_value):
#        for item in data:
#            assert min_value < item['value'] < max_value


class TestRosstatKep:
    
    def setup_method(self):
        parser = RosstatKEP('m', ['CPI_rog', 'RUR_EUR_eop'])
        self.items = list(parser.get_data())
        
# TODO: Some tests may be inherited, some custom for this class, maybe

#
#    def test_get_data_structure(self):
#        _TestGenericParser.test_get_data_structure(self.data)
#
#    def test_get_data_types(self):
#        _TestGenericParser.test_get_data_types(self.data)
#
#    def test_get_data_valid_date_format(self):
#        _TestGenericParser.test_get_data_valid_date_format(self.data)
#
#    def test_get_data_valid_date_range(self):
#        _TestGenericParser\
#            .test_get_data_valid_date_range(self.data, RosstatKEP.start_date)
#
#    def test_get_data_freq_range(self):
#        _TestGenericParser\
#            .test_get_data_freq_range(self.data, RosstatKEP.freqs)
#
#    def test_get_data_varnames_range(self):
#        _TestGenericParser\
#            .test_get_data_varnames_range(self.data, RosstatKEP.all_varnames)
#
#    def test_get_data_values_range(self):
#        cpi_data = [item for item in self.data if item['name'] == 'CPI_rog']
#        eur_data = [item for item in self.data if item['name'] == 'RUR_EUR_eop']
#
#        _TestGenericParser\
#            .test_get_data_values_range(cpi_data, 90, 110)
#        _TestGenericParser \
#            .test_get_data_values_range(eur_data, 50, 80)


class TestCBR_USD:
    
    def setup_method(self):
        parser = CBR_USD('d', ['USDRUR_CB'])
        self.items = list(parser.get_data())

# TODO: Some tests may be inherited, some custom for this class, maybe


#    def test_get_data_structure(self):
#        _TestGenericParser.test_get_data_structure(self.data)
#
#    def test_get_data_types(self):
#        _TestGenericParser.test_get_data_types(self.data)
#
#    def test_get_data_valid_date_format(self):
#        _TestGenericParser.test_get_data_valid_date_format(self.data)
#
#    def test_get_data_valid_date_range(self):
#        _TestGenericParser \
#            .test_get_data_valid_date_range(self.data, CBR_USD.start_date)
#
#    def test_get_data_freq_range(self):
#        _TestGenericParser \
#            .test_get_data_freq_range(self.data, CBR_USD.freqs)
#
#    def test_get_data_varnames_range(self):
#        _TestGenericParser \
#            .test_get_data_varnames_range(self.data, CBR_USD.all_varnames)
#
#    def test_get_data_values_range(self):
#        _TestGenericParser \
#            .test_get_data_values_range(self.data, 50, 70)


class TestBrentEIA:
    
        def setup_method(self):
            parser = BrentEIA('d', ['EIA_BRENT'])
            self.items = list(parser.get_data())

# TODO: Some tests may be inherited, some custom for this class, maybe

#    def test_get_data_structure(self):
#        _TestGenericParser.test_get_data_structure(self.data)
#
#    def test_get_data_types(self):
#        _TestGenericParser.test_get_data_types(self.data)
#
#    def test_get_data_valid_date_format(self):
#        _TestGenericParser.test_get_data_valid_date_format(self.data)
#
#    def test_get_data_valid_date_range(self):
#        _TestGenericParser \
#            .test_get_data_valid_date_range(self.data, BrentEIA.start_date)
#
#    def test_get_data_freq_range(self):
#        _TestGenericParser \
#            .test_get_data_freq_range(self.data, BrentEIA.freqs)
#
#    def test_get_data_varnames_range(self):
#        _TestGenericParser \
#            .test_get_data_varnames_range(self.data, BrentEIA.all_varnames)
#
#    def test_get_data_values_range(self):
#        _TestGenericParser \
#            .test_get_data_values_range(self.data, 20, 120)

if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
    
