import pytest


from datetime import date
from decimal import Decimal


from parsers.getter.base import (ParserBase,
                                 format_date,
                                 format_value,
                                 make_date)

# def format_date(date_string: str, fmt):
#    """Convert *date_string* to YYYY-MM-DD"""
#    return datetime.strptime(date_string, fmt).strftime("%Y-%m-%d")


@pytest.mark.parametrize("date_string, fmt, expected", [
    ('2017-01-04T00:00:00', '%Y-%m-%dT%H:%M:%S', '2017-01-04'),
    ('20170104', '%Y%m%d', '2017-01-04'),
    ('2007/01/25', '%Y/%m/%d', '2007-01-25')
])
def test_format_date_on_valid_inputs(date_string, fmt, expected):
    assert format_date(date_string, fmt) == expected


@pytest.mark.parametrize("fargs", [
    dict(date_string='2017-01-04', fmt='%Y-%m-%dT%H:%M:%S'),
    dict(date_string='2017-01-04', fmt='%Y%m%d'),
])
def test_format_date_on_invalid_date_string_raises_ValueError(fargs):
    with pytest.raises(ValueError):
        format_date(**fargs)


@pytest.mark.parametrize("fargs", [
    dict(date_string=None, fmt='%Y-%m-%dT%H:%M:%S'),
    dict(date_string='2017-01-04', fmt=None),
])
def test_format_date_with_None_raises_TypeError(fargs):
    with pytest.raises(TypeError):
        format_date(**fargs)

# def format_value(value_string: str, precision=2):
#    return round(Decimal(value_string), precision)


class Test_format_value:
    def test_format_value_with_valid_parameters(self):
        assert format_value('2.26') == Decimal('2.26')

    def test_format_value_with_invalid_parameters(self):
        with pytest.raises(Exception):
            format_value('12 356')

    def test_format_value_with_None_parameter(self):
        with pytest.raises(TypeError):
            format_value(None)


# def make_date(x):
#    if '-' in str(x):
#        return arrow.get(x).date()
#    else:
#        return date(int(x), 1, 1)

@pytest.mark.parametrize("x, expected", [
    (2017, (2017, 1, 1)),
    ('2017-06-15', (2017, 6, 15)),
    ('2017-12', (2017, 12, 1)),
])
def test_make_date(x, expected):
    assert make_date(x) == date(*expected)


class Test_make_date:
    def test_returns_datetime_date_type(self):
        dt = make_date('2007-01-25')
        assert isinstance(dt, date)

    def test_accepts_YYYY_MM_DD(self):
        date = make_date('2007-01-25')
        assert date.day == 25
        assert date.month == 1
        assert date.year == 2007

    def test_on_none_returns_None(self):
        assert make_date(None) is None

    def test_make_date_on_empty_str_raises_Exception(self):
        with pytest.raises(Exception):
            make_date('')

    def test_make_date_on_no_argument_raises_TypeError(self):
        with pytest.raises(TypeError):
            make_date()

    def test_on_invalid_month_raises_ValueError(self):
        with pytest.raises(ValueError):
            make_date('2007-25-25')

    def test_on_invalid_format(self):
        with pytest.raises(TypeError):
            assert make_date('2000-01-01', '%dzzzk%m-%Y')


# class ParserBase(object):
#    """
#    Must customise in child class:
#       - observation_start_date
#       - url
#       - parse_response
#    """
#
#    # must change this to actual parser start date
#    observation_start_date = '1990-01-02'
#
#    def __init__(self, start_date=None, end_date=None):
#        self.start_date = (make_date(start_date)
#                           or make_date(self.observation_start_date))
#        if end_date is None:
#            self.end_date = date.today()
#        else:
#           self.end_date = make_date(end_date)
#
#        self.response = None
#        self.timer = Timer()
#        self.parsing_result = []
#
#    @property
#    def url(self):
#        raise NotImplementedError
#
#    def parse_response(self):
#        raise NotImplementedError
#
#    @property
#    def elapsed(self):
#        return self.timer.elapsed
#
#    def _extract(self, downloader=fetch, verbose=False):
#        if verbose:
#             print(f'Reading data from: {self.url}')
#        self.response = downloader(self.url)
#        self.parsing_result = self.parse_response(self.response)
#        return self
#
#    def extract(self):
#        self.timer.start()
#        self._extract(verbose=True)
#        self.timer.stop()
#        print(self.timer)
#        return self
#
#    @property
#    def items(self):
#        """Parsing result bound by start and end date"""
#        result = []
#        for item in self.parsing_result:
#            dt = make_date(item['date'])
#            if self.start_date <= dt <= self.end_date:
#                result.append(item)
#        return result
#
#    def _upload(self):
#        return upload_datapoints(self.items)
#
#    def upload(self):
#        self.timer.start()
#        result_bool = self._upload()
#        self.timer.stop()
#        print(f'Uploaded {len(self.parsing_result)} datapoints')
#        print(self.timer)
#        return result_bool
#
#    def __repr__(self):
#        # .. code changed

# class Test_ParserBase:
#
#    p = ParserBase(2017, 2018)
#
#    def test_url(self):
#        pass


class ParserBaseChild(ParserBase):
    observation_start_date = '1990-01-01'

    @property
    def url(self):
        return 'http://localhost'

    @staticmethod
    def get_datapoints(response_str):
        return [{}, {}]


class Test_ParserBaseChild:

    def test_parse_response_on_non_string_raises_error(self):
        p = ParserBaseChild()
        with pytest.raises(TypeError):
            p.parse_response(1)

    def test_parse_response_on_string_returns_list_of_dicts(self):
        p = ParserBaseChild()
        out = p.parse_response('abc')
        assert isinstance(out, list)
        assert all([isinstance(x, dict) for x in out])

    def test_date_attributes_on_init_without_args(self):
        pb = ParserBaseChild()
        assert pb.start_date == date(1990, 1, 1)
        assert pb.end_date == date.today()

    def test_dates_on_init_with_one_arg(self):
        pb = ParserBaseChild(2017)
        assert pb.start_date == date(2017, 1, 1)
        assert pb.end_date == date.today()

    def test_repr_returns_string(self):
        pb = ParserBaseChild(2017)
        assert pb.__repr__().startswith("ParserBase")

    def test_items(self):
        pb = ParserBaseChild('2017-01-01', '2017-11-19')
        pb.parsing_result = [dict(date='2016-12-31'),
                             dict(date='2017-01-01'),
                             dict(date='2017-06-01'),
                             dict(date='2017-11-19'),
                             dict(date='2017-12-31')]
        assert pb.items == [dict(date='2017-01-01'),
                            dict(date='2017-06-01'),
                            dict(date='2017-11-19')]


if __name__ == '__main__':
    pytest.main([__file__])
