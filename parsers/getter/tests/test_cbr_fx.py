import mock
from parsers.getter import cbr_fx


def test_get_xml(mocker):
    foo_obj = type('', (object,), {"foo": 1})()
    foo_obj.text = 'some_text'
    mocker.patch('requests.get', mock.MagicMock(return_value=foo_obj))
    assert cbr_fx.get_xml("some_url") == foo_obj.text
    try:
        foo_obj.text = 'Error in parameters'
        cbr_fx.get_xml("some_url")
    except Exception as e:
        assert str(e) == 'Error in parameters: some_url'
