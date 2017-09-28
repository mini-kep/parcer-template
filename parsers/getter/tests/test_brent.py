import mock
import parsers.getter.brent as brent
from decimal import Decimal


def test_yield_brent_dicts(mocker):
    mocker.patch('parsers.getter.brent.fetch', mock.MagicMock(return_value=None))
    mocker.patch('parsers.getter.brent.format_string', mock.MagicMock(return_value='2017-12-31'))
    mocker.patch('parsers.getter.brent.parse_response', mock.MagicMock(return_value=[['20171231', 2.23899]]))
    for data in brent.yield_brent_dicts():
        assert data == {'date': '2017-12-31', 'freq': 'd', 'name': 'BRENT', 'value': Decimal('2.2390')}
