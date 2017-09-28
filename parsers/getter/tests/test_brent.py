import mock
from decimal import Decimal
from getter import brent


def test_yield_brent_dicts(mocker):
    mocker.patch('getter.brent.fetch', mock.MagicMock(return_value=None))
    mocker.patch('getter.brent.format_string', mock.MagicMock(return_value='2017-12-31'))
    mocker.patch('getter.brent.parse_response', mock.MagicMock(return_value=[['20171231', 2.23899]]))
    for data in brent.yield_brent_dicts():
        assert data == {'date': '2017-12-31', 'freq': 'd', 'name': 'BRENT', 'value': Decimal('2.2390')}
