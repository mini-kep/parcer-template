from parsers.getter.cbr_fx import USDRUR
from parsers.getter.brent import Brent
from parsers.dataset import Dataset
import arrow

#TODO: test save_json() on temp file + delete this temp file file in teardown method 

#TODO: separate below to class
def test_dataset():
    dt = arrow.now().shift(weeks=-1).format("YYYY-MM-DD")
    d = Dataset([USDRUR, Brent], dt)
    d.extract()
    assert d.items[0]['name'] == 'USDRUR_CB'
    assert isinstance(d.json, str)
    assert d.json
    d.upload()
