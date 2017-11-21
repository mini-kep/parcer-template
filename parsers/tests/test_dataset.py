import pytest
from parsers.getter.cbr_fx import USDRUR
from parsers.getter.brent import Brent
from parsers.dataset import Dataset
from pathlib import Path

#TODO: test save_json() on temp file + delete this temp file file in teardown method 

#TODO: separate below to class

@pytest.mark.webtest
class Test_Dataset:
    def setup(self):
        self.sample_dataset = Dataset([USDRUR, Brent], '2017-11-13')
        self.sample_dataset.extract()
        self.temp_file = 'temp.json'

    def test_dataset(self):
        assert self.sample_dataset.items[0]['name'] == 'USDRUR_CB'
        assert isinstance(self.sample_dataset.json, str)
        assert self.sample_dataset.json
        self.sample_dataset.upload()

    def test_save_json(self):
        self.sample_dataset.save_json(self.temp_file)
        with Path(self.temp_file).open() as file:
            json = file.read()
            assert '"date": "2017-11-21",\n' in json
            assert '"freq": "d",\n'
            assert '"name": "USDRUR_CB",\n' in json
            assert '"value": 59.2746\n' in json

    def teardown(self):
        file = Path(self.temp_file)
        if file.exists():
            file.unlink()