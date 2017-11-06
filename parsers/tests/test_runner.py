import pytest
import datetime
from decimal import Decimal

from parsers.runner import (ParserBase,
                            RosstatKEP_Monthly,
                            RosstatKEP_Quarterly,
                            RosstatKEP_Annual,
                            CBR_USD,
                            BrentEIA)

PARSER_CLASSES = [RosstatKEP_Monthly,
                  RosstatKEP_Quarterly,
                  RosstatKEP_Annual,
                  CBR_USD,
                  BrentEIA]

# class attributes

@pytest.mark.parametrize("cls", PARSER_CLASSES)
def test_parser_class_atributes_core(cls):
    for cls in PARSER_CLASSES:
        assert cls.freq.isalpha()
        assert len(cls.freq) == 1
        assert isinstance(cls.observation_start_date, datetime.date)

@pytest.mark.parametrize("cls", PARSER_CLASSES)
def test_parser_class_atributes_reference(cls):
        assert isinstance(cls.source_url, str)
        assert cls.source_url.startswith('http')
        

@pytest.mark.parametrize("cls", PARSER_CLASSES)
def test_parser_instance_created_without_date(cls):
    assert cls()


@pytest.mark.parametrize("cls", PARSER_CLASSES)
def test_parser_instance_created_with_date(cls):
    assert cls(start='2016-09-15', end='2016-12-15')


@pytest.mark.parametrize("cls", PARSER_CLASSES)
def test_parser_instance_has_callable_repr_method(cls):
    assert isinstance(cls().__repr__(), str)


@pytest.mark.parametrize("cls", PARSER_CLASSES)
def test_items_method_is_callable(cls):
    gen = cls().items
    a = next(gen)
    validate_datapoint(a)


@pytest.mark.parametrize("datapoint", [datapoint for datapoint in 
    [cls().sample() for cls in PARSER_CLASSES]])
def validate_datapoint(datapoint):
        # dict has 4 elements
    assert isinstance(datapoint, dict)
    assert len(datapoint) == 4
    # date
    assert isinstance(datapoint['date'], str)
    # frequency
    freq = datapoint['freq']
    assert isinstance(datapoint['freq'], str)
    assert freq in "aqmwd"
    # name
    assert isinstance(datapoint['name'], str)
    # value
    assert isinstance(datapoint['value'], Decimal)
    # precision - not too clear
    decimal_str = str(datapoint['value']).rstrip('0')
    float_str = str(round(float(datapoint['value']), 4))
    assert(decimal_str == float_str)


def test_CBR_USD_will_not_work_before_1992():
    with pytest.raises(Exception):
        next(CBR_USD('1991-07-15').items)

# NOT IMPLEMENTED - NOT TODO: date check
#import arrow
#def is_date_valid(date, parser_class)
#     
#     date = arrow.get(date).date()
#     assert parser_class.start <= date
#     assert date <= datetime.date.today()
#
#
#   def test_get_data_item_date_in_valid_range(self):
#       dates = (item['date'] for item in self.items)
#       for date in dates:

# NOT IMPLEMENTED - NOT TODO: value range check          
           
#   # valid code and good idea to check, but iplementation too copmplex
#   # for a base test class
#
#   def test_get_data_produces_values_in_valid_range(self, items, min, max):
#      for item in items:
#          assert min < item['value'] < max
#
#   def test_get_data_produces_values_in_valid_range(self):
#      cpi_data = [item for item in self.items
#                  if item['name'] == 'CPI_rog']
#      eur_data = [item for item in self.items
#                  if item['name'] == 'RUR_EUR_eop']
#      
#      # FIXME: must not use Super
#      super(TestRosstatKep, self)\
#          .test_get_data_produces_values_in_valid_range(cpi_data, 90, 110)
#      super(TestRosstatKep, self)\
#          .test_get_data_produces_values_in_valid_range(eur_data, 50, 80)
#
#   def test_get_data_produces_values_in_valid_range(self):
#       super(TestCBR_USD, self).test_get_data_produces_values_in_valid_range(self.items, 50, 70)
#
#   def test_get_data_produces_values_in_valid_range(self):
#       super(TestBrentEIA, self).test_get_data_produces_values_in_valid_range(self.items, 20, 120)

if __name__ == '__main__':
    pytest.main([__file__])