from parsers.getter.cbr_fx import USDRUR
from parsers.getter.brent import Brent
from parsers.dataset import Dataset

#TODO: test save_json() on temp file + delete this temp file file in teardown method 

#TODO: separate below to class
#
def test_dataset():
    d = Dataset([USDRUR, Brent], '2017-11-13')
    d.extract()
    assert d.items[0]['name'] == 'USDRUR_CB'
    assert isinstance(d.json, str)
    assert d.json
    d.upload()
